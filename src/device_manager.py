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

    def _is_virtual_device(self, name: str, device_id: str, manufacturer: str = "") -> str:
        """
        Determine if a device is virtual or physical.
        
        Args:
            name: Device name
            device_id: Device identifier
            manufacturer: Device manufacturer
            
        Returns:
            "Virtual" if device is virtual, "Physical" otherwise
        """
        if not name:
            return "Physical"
        
        # Virtual device indicators
        virtual_keywords = [
            "virtual", "vmware", "virtualbox", "hyper-v", "hyperv",
            "tap-windows", "loopback", "pseudo", "vethernet",
            "vbox", "qemu", "kvm", "parallels", "vpn",
            "tunnel", "bridge", "vnic", "ramdisk", "ram disk"
        ]
        
        # Check name, device ID, and manufacturer
        search_text = f"{name} {device_id} {manufacturer}".lower()
        
        for keyword in virtual_keywords:
            if keyword in search_text:
                return "Virtual"
        
        # Check for ROOT\ prefix (often indicates virtual/software devices)
        if device_id and device_id.upper().startswith("ROOT\\"):
            return "Virtual"
        
        return "Physical"

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
        
        # 6. Display Devices (HDMI/Monitor)
        try:
            display_entities = c.query("SELECT * FROM Win32_PnPEntity WHERE Service='monitor' OR DeviceID LIKE 'DISPLAY%'")
            for item in display_entities:
                self._add_display_device(devices, item)
        except Exception as e:
            logger.error(f"Failed to query Display devices: {e}")
        
        return devices
    
    def _add_usb_device(self, devices: List[Dict], item) -> None:
        """Add USB device to the devices list."""
        try:
            vid, pid = self._parse_vid_pid(item.DeviceID)
            path = item.DeviceID or "Unknown"
            
            # Determine device type
            dev_type = "USB Device"
            category = "USB"
            name = item.Name or item.Description or "Unknown USB Device"
            manufacturer = item.Manufacturer or "Unknown"
            
            name_lower = name.lower()
            desc_lower = (item.Description or "").lower()
            
            if "hub" in name_lower or "hub" in desc_lower:
                dev_type = "USB Hub"
                category = "USB Port"
            elif "controller" in name_lower or "controller" in desc_lower:
                dev_type = "USB Controller"
                category = "USB Port"
            elif "composite" in desc_lower:
                dev_type = "USB Composite Device"
            
            # Determine if virtual or physical
            port_type = self._is_virtual_device(name, path, manufacturer)

            devices.append({
                "name": name,
                "category": category,
                "type": dev_type,
                "port_type": port_type,
                "vid": vid,
                "pid": pid,
                "manufacturer": manufacturer,
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
            manufacturer = item.Manufacturer or "Unknown"
            path = item.DeviceID or "Unknown"
            
            # Categorize HID devices
            cat = "HID"
            if "keyboard" in name.lower():
                cat = "Keyboard"
            elif "mouse" in name.lower():
                cat = "Mouse"
            
            # Determine if virtual or physical
            port_type = self._is_virtual_device(name, path, manufacturer)
            
            devices.append({
                "name": name,
                "category": cat,
                "type": "Human Interface Device",
                "port_type": port_type,
                "vid": vid,
                "pid": pid,
                "manufacturer": manufacturer,
                "status": item.Status or "Unknown",
                "path": path,
                "driver": item.Service or "Unknown"
            })
        except Exception as e:
            logger.warning(f"Failed to add HID device: {e}")
    
    def _add_network_device(self, devices: List[Dict], item) -> None:
        """Add network adapter to the devices list."""
        try:
            status = "Connected" if item.NetConnectionStatus == 2 else "Disconnected"
            name = item.Name
            manufacturer = item.Manufacturer or "Unknown"
            path = item.PNPDeviceID or "N/A"
            
            # Determine category (Ethernet vs Wi-Fi vs Network)
            category = "Network"
            adapter_type = item.AdapterType or "Network Adapter"
            
            name_lower = name.lower()
            if "ethernet" in name_lower or "gbe" in name_lower or "gigabit" in name_lower:
                category = "Ethernet"
            elif "wi-fi" in name_lower or "wireless" in name_lower or "802.11" in name_lower:
                category = "Wi-Fi"
            
            # Determine if virtual or physical
            port_type = self._is_virtual_device(name, path, manufacturer)
            
            devices.append({
                "name": name,
                "category": category,
                "type": adapter_type,
                "port_type": port_type,
                "vid": "N/A",
                "pid": "N/A",
                "manufacturer": manufacturer,
                "status": status,
                "path": path,
                "driver": item.ServiceName or "Unknown"
            })
        except Exception as e:
            logger.warning(f"Failed to add network device: {e}")
    
    def _add_storage_device(self, devices: List[Dict], item) -> None:
        """Add storage device to the devices list."""
        try:
            name = item.Model or item.Caption or "Unknown Storage"
            manufacturer = item.Manufacturer or "Generic"
            path = item.DeviceID or "Unknown"
            
            # Use WMI associations to find the drive letter (e.g., E:)
            drive_letter = "N/A"
            try:
                for partition in item.associators("Win32_DiskDriveToDiskPartition"):
                    for logical_disk in partition.associators("Win32_LogicalDiskToPartition"):
                        if logical_disk.DeviceID:
                            drive_letter = logical_disk.DeviceID
                            break
                    if drive_letter != "N/A":
                        break
            except:
                pass

            # Determine if virtual or physical (e.g., RAM disks, virtual disks)
            port_type = self._is_virtual_device(name, path, manufacturer)
            
            devices.append({
                "name": name,
                "category": "Storage",
                "type": item.MediaType or "Disk Drive",
                "port_type": port_type,
                "vid": "N/A",
                "pid": "N/A",
                "manufacturer": manufacturer,
                "status": item.Status or "Unknown",
                "path": path,
                "driver": "disk",
                "mount_point": drive_letter # Added for auto-scan
            })
        except Exception as e:
            logger.warning(f"Failed to add storage device: {e}")
    
    def _add_bluetooth_device(self, devices: List[Dict], item) -> None:
        """Add Bluetooth device to the devices list."""
        try:
            name = item.Name or "Bluetooth Device"
            manufacturer = item.Manufacturer or "Unknown"
            path = item.DeviceID or "Unknown"
            
            # Determine if virtual or physical
            port_type = self._is_virtual_device(name, path, manufacturer)
            
            devices.append({
                "name": name,
                "category": "Bluetooth",
                "type": "Bluetooth",
                "port_type": port_type,
                "vid": "N/A",
                "pid": "N/A",
                "manufacturer": manufacturer,
                "status": item.Status or "Unknown",
                "path": path,
                "driver": item.Service or "Unknown"
            })
        except Exception as e:
            logger.warning(f"Failed to add Bluetooth device: {e}")

    def _add_display_device(self, devices: List[Dict], item) -> None:
        """Add Display/Monitor device to the devices list."""
        try:
            name = item.Name or item.Description or "Generic Monitor"
            manufacturer = item.Manufacturer or "Unknown"
            path = item.DeviceID or "Unknown"
            
            # Check for HDMI in name/description (not always reliable, but helps categorization)
            category = "Display"
            if "hdmi" in name.lower() or "hdmi" in (item.Description or "").lower():
                category = "HDMI"
            
            # Determine if virtual or physical
            port_type = self._is_virtual_device(name, path, manufacturer)
            
            devices.append({
                "name": name,
                "category": category,
                "type": "Display Monitor",
                "port_type": port_type,
                "vid": "N/A",
                "pid": "N/A",
                "manufacturer": manufacturer,
                "status": item.Status or "Unknown",
                "path": path,
                "driver": item.Service or "Unknown"
            })
        except Exception as e:
            logger.warning(f"Failed to add Display device: {e}")
