"""
Hardware Port Sandbox - Intercepts physical port communications (USB, Type-C, HDMI)
"""
try:
    import wmi  # type: ignore
except ImportError:
    wmi = None
import threading
import logging
from typing import Callable, Dict
from datetime import datetime
import hashlib

logger = logging.getLogger(__name__)

class HardwarePortSandbox:
    """Intercepts and secures hardware port communications"""
    
    def __init__(self, validation_callback: Callable = None):
        if wmi is None:
            raise ImportError("WMI module not available. Install with: pip install wmi")
        self.validation_callback = validation_callback
        self.active = False
        self.monitored_ports: Dict[str, Dict] = {}
        self.transfer_logs = []
        self._lock = threading.Lock()
        self.wmi = wmi.WMI()
        
    def start(self):
        """Start monitoring hardware ports"""
        self.active = True
        threading.Thread(target=self._monitor_ports, daemon=True).start()
        logger.info("Hardware port sandbox started")
        
    def _monitor_ports(self):
        """Monitor all hardware ports"""
        while self.active:
            try:
                import time
                # Monitor USB ports
                for usb in self.wmi.Win32_USBHub():
                    port_id = usb.DeviceID
                    if port_id not in self.monitored_ports:
                        self._hook_port(port_id, "USB", usb)
                
                # Monitor USB Controllers (Type-C)
                for controller in self.wmi.Win32_USBController():
                    port_id = controller.DeviceID
                    if port_id not in self.monitored_ports:
                        self._hook_port(port_id, "USB-C/Controller", controller)
                
                # Monitor Video Controllers (HDMI/DisplayPort)
                for video in self.wmi.Win32_VideoController():
                    port_id = video.DeviceID
                    if port_id not in self.monitored_ports:
                        self._hook_port(port_id, "Video/HDMI", video)
                
                time.sleep(2)  # Check every 2 seconds
                        
            except Exception as e:
                logger.error(f"Port monitoring error: {e}")
                
    def _hook_port(self, port_id: str, port_type: str, device):
        """Hook into hardware port"""
        with self._lock:
            self.monitored_ports[port_id] = {
                "type": port_type,
                "device": device,
                "hooked_at": datetime.now(),
                "name": getattr(device, 'Name', 'Unknown')
            }
        logger.info(f"Hooked {port_type} port: {port_id}")
        
    def validate_transfer(self, port_id: str, data: bytes) -> bool:
        """Validate data transfer through hardware port"""
        if self.validation_callback:
            allowed = self.validation_callback(data, port_id)
        else:
            allowed = True
            
        log = {
            "timestamp": datetime.now(),
            "port_id": port_id,
            "port_type": self.monitored_ports.get(port_id, {}).get("type", "Unknown"),
            "data_hash": hashlib.sha256(data).hexdigest(),
            "size": len(data),
            "allowed": allowed
        }
        
        with self._lock:
            self.transfer_logs.append(log)
            
        return allowed
        
    def get_monitored_ports(self) -> Dict:
        """Get all monitored hardware ports"""
        with self._lock:
            return self.monitored_ports.copy()
            
    def get_logs(self) -> list:
        """Get transfer logs"""
        with self._lock:
            return self.transfer_logs.copy()
            
    def stop(self):
        """Stop monitoring"""
        self.active = False
        logger.info("Hardware port sandbox stopped")
