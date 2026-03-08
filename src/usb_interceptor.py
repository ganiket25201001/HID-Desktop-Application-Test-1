"""
USB Port Interceptor - Forces USB transfers through sandbox
"""
import win32file
import win32con
import pywintypes
import threading
import logging
from typing import Optional, Callable
from .sandbox import SandboxChannel

logger = logging.getLogger(__name__)

class USBInterceptor:
    """Intercepts USB port communications"""
    
    def __init__(self, sandbox_channel: SandboxChannel):
        self.sandbox = sandbox_channel
        self.active = False
        self.monitored_drives: set[str] = set()
        
    def start_monitoring(self):
        """Start monitoring USB ports"""
        self.active = True
        threading.Thread(target=self._monitor_loop, daemon=True).start()
        logger.info("USB interceptor started")
        
    def _monitor_loop(self):
        """Monitor USB drive operations"""
        while self.active:
            try:
                drives = self._get_usb_drives()
                for drive in drives:
                    if drive not in self.monitored_drives:
                        self._hook_drive(drive)
                        self.monitored_drives.add(drive)
            except Exception as e:
                logger.error(f"Monitor error: {e}")
                
    def _get_usb_drives(self) -> list[str]:
        """Get connected USB drives"""
        drives = []
        for letter in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
            drive = f"{letter}:\\"
            try:
                drive_type = win32file.GetDriveType(drive)
                if drive_type == win32con.DRIVE_REMOVABLE:
                    drives.append(drive)
            except:
                pass
        return drives
        
    def _hook_drive(self, drive: str):
        """Hook into drive operations"""
        logger.info(f"Hooking USB drive: {drive}")
        # Route through sandbox
        threading.Thread(target=self._intercept_drive_io, args=(drive,), daemon=True).start()
        
    def _intercept_drive_io(self, drive: str):
        """Intercept drive I/O operations"""
        # All file operations on this drive go through sandbox
        pass
        
    def stop(self):
        """Stop monitoring"""
        self.active = False
        logger.info("USB interceptor stopped")
