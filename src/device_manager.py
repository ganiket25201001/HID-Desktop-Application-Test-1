"""
Device Manager Module
Handles WMI queries for hardware device detection and information retrieval.
"""
import re
import pythoncom
from typing import List, Dict, Tuple, Optional, Any
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DeviceManager:
    """Manages device detection and information retrieval using Windows WMI."""
    
    def __init__(self):
        """Initialize the Device Manager."""
        self._wmi_connection = None
    
    def _get_wmi(self) -> Any:
        """
        Get or create WMI connection with proper COM initialization.
        
        Returns:
            WMI connection object
        """
        try:
            pythoncom.CoInitialize()
            import wmi
            return wmi.WMI()
        except Exception as e:
            logger.error(f"Failed to initialize WMI connection: {e}")
            raise

    def _parse_vid_pid(self, device_id: Optional[str]) -> Tuple[str, str]:
        """
        Parse Vendor ID and Product ID from device identifier string.
        
        Args:
            device_id: Device identifier string containing VID/PID information
            
        Returns:
            Tuple of (vendor_id, product_id) as hex strings
        """
        vid = "N/A"
        pid = "N/A"
        
        if not device_id:
            return vid, pid
        
        try:
            # Common patterns: VID_xxxx&PID_yyyy or VEN_xxxx&DEV_yyyy
            vid_match = re.search(r'(?:VID_|VEN_)([0-9A-Fa-f]{4})', device_id)
            pid_match = re.search(r'(?:PID_|DEV_)([0-9A-Fa-f]{4})', device_id)
            
            if vid_match:
                vid = "0x" + vid_match.group(1).upper()
            if pid_match:
                pid = "0x" + pid_match.group(1).upper()
        except Exception as e:
            logger.warning(f"Failed to parse VID/PID from {device_id}: {e}")
            
        return vid, pid

    def get_all_devices(self) -> List[Dict[str, str]]:
        """
        Retrieve all connected devices from various categories.
        
        Returns:
            List of device dictionaries containing device information
        """
        devices = []
        
        try:
            c = self._get_wmi()
        except Exception as e:
            logger.error(f"Failed to get WMI connection: {e}")
            return devices
        
        # 1. USB Devices
        try:
            usb_entities = c.query("SELECT * FROM Win32_PnPEntity WHERE DeviceID LIKE 'USB%'")
            for item in usb_entities:
                self._add_usb_device(devices, item)
        except Exception as e:
            logger.error(f"Failed to query USB devices: {e}")
        
        # 2. HID Devices
        try:
            hid_entities = c.query("SELECT * FROM Win32_PnPEntity WHERE DeviceID LIKE 'HID%'")
            for item in hid_entities:
                self._add_hid_device(devices, item)
        except Exception as e:
            logger.error(f"Failed to query HID devices: {e}")
        
        # 3. Network Adapters
        try:
            net_adapters = c.Win32_NetworkAdapter(PhysicalAdapter=True)
            for item in net_adapters:
                if item.Name:
                    self._add_network_device(devices, item)
        except Exception as e:
            logger.error(f"Failed to query network adapters: {e}")
        
        # 4. Storage Devices
        try:
            disks = c.Win32_DiskDrive()
            for item in disks:
                self._add_storage_device(devices, item)
        except Exception as e:
            logger.error(f"Failed to query storage devices: {e}")
        
        # 5. Bluetooth Devices
        try:
            bt_entities = c.query("SELECT * FROM Win32_PnPEntity WHERE DeviceID LIKE 'BTH%' OR Service='BTHUSB'")
            for item in bt_entities:
                self._add_bluetooth_device(devices, item)
        except Exception as e:
            logger.error(f"Failed to query Bluetooth devices: {e}")
        
        return devices
    
    def _add_usb_device(self, devices: List[Dict], item) -> None:
        """Add USB device to the devices list."""
        try:
            vid, pid = self._parse_vid_pid(item.DeviceID)
            path = item.DeviceID or "Unknown"
            
            # Determine device type
            dev_type = "USB Device"
            name = item.Name or item.Description or "Unknown USB Device"
            
            if "hub" in name.lower():
                dev_type = "USB Hub"
            elif "composite" in (item.Description or "").lower():
                dev_type = "USB Composite Device"

            devices.append({
                "name": name,
                "category": "USB",
                "type": dev_type,
                "vid": vid,
                "pid": pid,
                "manufacturer": item.Manufacturer or "Unknown",
                "status": item.Status or "Unknown",
                "path": path,
                "driver": item.Service or "Unknown"
            })
        except Exception as e:
            logger.warning(f"Failed to add USB device: {e}")
    
    def _add_hid_device(self, devices: List[Dict], item) -> None:
        """Add HID device to the devices list."""
        try:
            vid, pid = self._parse_vid_pid(item.DeviceID)
            name = item.Name or item.Description or "Unknown HID Device"
            
            # Categorize HID devices
            cat = "HID"
            if "keyboard" in name.lower():
                cat = "Keyboard"
            elif "mouse" in name.lower():
                cat = "Mouse"
            
            devices.append({
                "name": name,
                "category": cat,
                "type": "Human Interface Device",
                "vid": vid,
                "pid": pid,
                "manufacturer": item.Manufacturer or "Unknown",
                "status": item.Status or "Unknown",
                "path": item.DeviceID or "Unknown",
                "driver": item.Service or "Unknown"
            })
        except Exception as e:
            logger.warning(f"Failed to add HID device: {e}")
    
    def _add_network_device(self, devices: List[Dict], item) -> None:
        """Add network adapter to the devices list."""
        try:
            status = "Connected" if item.NetConnectionStatus == 2 else "Disconnected"
            
            devices.append({
                "name": item.Name,
                "category": "Network",
                "type": item.AdapterType or "Network Adapter",
                "vid": "N/A",
                "pid": "N/A",
                "manufacturer": item.Manufacturer or "Unknown",
                "status": status,
                "path": item.PNPDeviceID or "N/A",
                "driver": item.ServiceName or "Unknown"
            })
        except Exception as e:
            logger.warning(f"Failed to add network device: {e}")
    
    def _add_storage_device(self, devices: List[Dict], item) -> None:
        """Add storage device to the devices list."""
        try:
            devices.append({
                "name": item.Model or item.Caption or "Unknown Storage",
                "category": "Storage",
                "type": item.MediaType or "Disk Drive",
                "vid": "N/A",
                "pid": "N/A",
                "manufacturer": item.Manufacturer or "Generic",
                "status": item.Status or "Unknown",
                "path": item.DeviceID or "Unknown",
                "driver": "disk"
            })
        except Exception as e:
            logger.warning(f"Failed to add storage device: {e}")
    
    def _add_bluetooth_device(self, devices: List[Dict], item) -> None:
        """Add Bluetooth device to the devices list."""
        try:
            devices.append({
                "name": item.Name or "Bluetooth Device",
                "category": "Bluetooth",
                "type": "Bluetooth",
                "vid": "N/A",
                "pid": "N/A",
                "manufacturer": item.Manufacturer or "Unknown",
                "status": item.Status or "Unknown",
                "path": item.DeviceID or "Unknown",
                "driver": item.Service or "Unknown"
            })
        except Exception as e:
            logger.warning(f"Failed to add Bluetooth device: {e}")
