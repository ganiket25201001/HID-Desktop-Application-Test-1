"""
Sandbox Security Layer - Intercepts and secures all port communications
"""
import socket
import threading
import logging
from typing import Callable, Optional, Dict, Any
from dataclasses import dataclass
from datetime import datetime
import hashlib

logger = logging.getLogger(__name__)

@dataclass
class TransferLog:
    timestamp: datetime
    source: str
    destination: str
    data_hash: str
    size: int
    allowed: bool

class SandboxChannel:
    """Secured channel for port communications"""
    
    def __init__(self, port: int, validation_callback: Optional[Callable] = None):
        self.port = port
        self.validation_callback = validation_callback
        self.active = False
        self.server_socket: Optional[socket.socket] = None
        self.transfer_logs: list[TransferLog] = []
        self._lock = threading.Lock()
        
    def start(self):
        """Start the sandbox channel"""
        self.active = True
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind(('127.0.0.1', self.port))
        self.server_socket.listen(5)
        threading.Thread(target=self._accept_connections, daemon=True).start()
        logger.info(f"Sandbox channel started on port {self.port}")
        
    def _accept_connections(self):
        """Accept and handle incoming connections"""
        while self.active:
            try:
                client, addr = self.server_socket.accept()
                threading.Thread(target=self._handle_client, args=(client, addr), daemon=True).start()
            except Exception as e:
                if self.active:
                    logger.error(f"Connection error: {e}")
                    
    def _handle_client(self, client: socket.socket, addr: tuple):
        """Handle client data transfer through sandbox"""
        try:
            data = client.recv(8192)
            if data:
                data_hash = hashlib.sha256(data).hexdigest()
                allowed = self._validate_transfer(data, addr)
                
                log = TransferLog(
                    timestamp=datetime.now(),
                    source=f"{addr[0]}:{addr[1]}",
                    destination=f"127.0.0.1:{self.port}",
                    data_hash=data_hash,
                    size=len(data),
                    allowed=allowed
                )
                
                with self._lock:
                    self.transfer_logs.append(log)
                
                if allowed:
                    # Forward to actual destination
                    client.send(b"SANDBOX_OK")
                else:
                    client.send(b"SANDBOX_BLOCKED")
                    
        except Exception as e:
            logger.error(f"Client handling error: {e}")
        finally:
            client.close()
            
    def _validate_transfer(self, data: bytes, addr: tuple) -> bool:
        """Validate if transfer should be allowed"""
        if self.validation_callback:
            return self.validation_callback(data, addr)
        return True
        
    def stop(self):
        """Stop the sandbox channel"""
        self.active = False
        if self.server_socket:
            self.server_socket.close()
        logger.info(f"Sandbox channel stopped on port {self.port}")
        
    def get_logs(self) -> list[TransferLog]:
        """Get transfer logs"""
        with self._lock:
            return self.transfer_logs.copy()

class SandboxManager:
    """Manages multiple sandbox channels for different ports"""
    
    def __init__(self):
        self.channels: Dict[int, SandboxChannel] = {}
        self.global_validation: Optional[Callable] = None
        
    def create_channel(self, port: int, validation_callback: Optional[Callable] = None) -> SandboxChannel:
        """Create a new sandbox channel"""
        if port in self.channels:
            raise ValueError(f"Channel already exists on port {port}")
            
        callback = validation_callback or self.global_validation
        channel = SandboxChannel(port, callback)
        self.channels[port] = channel
        return channel
        
    def start_all(self):
        """Start all channels"""
        for channel in self.channels.values():
            channel.start()
            
    def stop_all(self):
        """Stop all channels"""
        for channel in self.channels.values():
            channel.stop()
            
    def set_global_validation(self, callback: Callable):
        """Set global validation for all channels"""
        self.global_validation = callback
        
    def get_all_logs(self) -> Dict[int, list[TransferLog]]:
        """Get logs from all channels"""
        return {port: channel.get_logs() for port, channel in self.channels.items()}
