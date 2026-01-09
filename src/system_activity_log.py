"""
System Activity Log Module
Tracks and manages device connection/disconnection events and system activities.
"""
import json
import os
import datetime
import logging
from typing import List, Dict, Optional
from enum import Enum

ACTIVITY_LOG_FILE = "system_activity.json"
MAX_LOG_ENTRIES = 1000  # Keep last 1000 entries

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ActivityType(Enum):
    """Types of system activities."""
    DEVICE_CONNECTED = "device_connected"
    DEVICE_DISCONNECTED = "device_disconnected"
    DEVICE_ERROR = "device_error"
    SYSTEM_STARTUP = "system_startup"
    SYSTEM_SHUTDOWN = "system_shutdown"
    PROFILE_UPDATED = "profile_updated"
    SETTINGS_CHANGED = "settings_changed"
    REFRESH_TRIGGERED = "refresh_triggered"


class ActivityLog:
    """Manages system activity logging and persistence."""
    
    def __init__(self):
        """Initialize activity log with default values."""
        self.activities: List[Dict] = []
        self.current_devices: Dict[str, Dict] = {}  # Track current device state
        self.load()
        self.log_activity(ActivityType.SYSTEM_STARTUP, "System Monitor Started", "System")
    
    def log_activity(self, 
                    activity_type: ActivityType, 
                    message: str, 
                    device_name: str = "System",
                    details: Optional[Dict] = None) -> None:
        """
        Log a system activity.
        
        Args:
            activity_type: Type of activity from ActivityType enum
            message: Activity description
            device_name: Name of the device or "System"
            details: Additional details dictionary
        """
        timestamp = datetime.datetime.now()
        
        activity = {
            "id": len(self.activities) + 1,
            "timestamp": timestamp.isoformat(),
            "type": activity_type.value,
            "message": message,
            "device_name": device_name,
            "details": details or {},
            "severity": self._get_severity(activity_type)
        }
        
        self.activities.append(activity)
        
        # Keep only last MAX_LOG_ENTRIES
        if len(self.activities) > MAX_LOG_ENTRIES:
            self.activities = self.activities[-MAX_LOG_ENTRIES:]
        
        # Auto-save every activity
        self.save()
        
        logger.info(f"{activity_type.value}: {message}")
    
    def _get_severity(self, activity_type: ActivityType) -> str:
        """Determine severity level based on activity type."""
        if activity_type == ActivityType.DEVICE_ERROR:
            return "error"
        elif activity_type in [ActivityType.DEVICE_DISCONNECTED]:
            return "warning"
        elif activity_type in [ActivityType.DEVICE_CONNECTED]:
            return "success"
        else:
            return "info"
    
    def check_device_changes(self, current_devices: List[Dict]) -> None:
        """
        Check for device changes and log connections/disconnections.
        
        Args:
            current_devices: List of currently detected devices
        """
        current_device_paths = {d.get('path'): d for d in current_devices if d.get('path')}
        previous_paths = set(self.current_devices.keys())
        current_paths = set(current_device_paths.keys())
        
        # Detect newly connected devices
        new_devices = current_paths - previous_paths
        for path in new_devices:
            device = current_device_paths[path]
            self.log_activity(
                ActivityType.DEVICE_CONNECTED,
                f"Device connected",
                device.get('name', 'Unknown Device'),
                {
                    'category': device.get('category', 'Unknown'),
                    'manufacturer': device.get('manufacturer', 'Unknown'),
                    'vid': device.get('vid', 'N/A'),
                    'pid': device.get('pid', 'N/A')
                }
            )
        
        # Detect disconnected devices
        removed_devices = previous_paths - current_paths
        for path in removed_devices:
            device = self.current_devices[path]
            self.log_activity(
                ActivityType.DEVICE_DISCONNECTED,
                f"Device disconnected",
                device.get('name', 'Unknown Device'),
                {
                    'category': device.get('category', 'Unknown'),
                    'last_seen': datetime.datetime.now().isoformat()
                }
            )
        
        # Update current device state
        self.current_devices = current_device_paths
    
    def get_recent_activities(self, limit: int = 50) -> List[Dict]:
        """
        Get most recent activities.
        
        Args:
            limit: Maximum number of activities to return
            
        Returns:
            List of recent activity dictionaries
        """
        return list(reversed(self.activities[-limit:]))
    
    def get_activities_by_type(self, activity_type: ActivityType, limit: int = 50) -> List[Dict]:
        """
        Get activities filtered by type.
        
        Args:
            activity_type: Type of activity to filter
            limit: Maximum number of activities to return
            
        Returns:
            List of filtered activity dictionaries
        """
        filtered = [a for a in self.activities if a['type'] == activity_type.value]
        return list(reversed(filtered[-limit:]))
    
    def get_activities_by_device(self, device_name: str, limit: int = 50) -> List[Dict]:
        """
        Get activities for a specific device.
        
        Args:
            device_name: Name of the device
            limit: Maximum number of activities to return
            
        Returns:
            List of device-specific activity dictionaries
        """
        filtered = [a for a in self.activities if a['device_name'] == device_name]
        return list(reversed(filtered[-limit:]))
    
    def get_statistics(self) -> Dict:
        """
        Get activity statistics.
        
        Returns:
            Dictionary containing various statistics
        """
        total = len(self.activities)
        
        # Count by type
        type_counts = {}
        severity_counts = {"error": 0, "warning": 0, "success": 0, "info": 0}
        
        for activity in self.activities:
            # Count by type
            activity_type = activity['type']
            type_counts[activity_type] = type_counts.get(activity_type, 0) + 1
            
            # Count by severity
            severity = activity['severity']
            severity_counts[severity] += 1
        
        # Get today's activities
        today = datetime.date.today()
        today_activities = [
            a for a in self.activities 
            if datetime.datetime.fromisoformat(a['timestamp']).date() == today
        ]
        
        return {
            'total_activities': total,
            'today_activities': len(today_activities),
            'devices_connected_today': sum(1 for a in today_activities if a['type'] == ActivityType.DEVICE_CONNECTED.value),
            'devices_disconnected_today': sum(1 for a in today_activities if a['type'] == ActivityType.DEVICE_DISCONNECTED.value),
            'by_type': type_counts,
            'by_severity': severity_counts,
            'oldest_entry': self.activities[0]['timestamp'] if self.activities else None,
            'newest_entry': self.activities[-1]['timestamp'] if self.activities else None
        }
    
    def clear_logs(self) -> None:
        """Clear all activity logs."""
        self.activities = []
        self.current_devices = {}
        self.save()
        logger.info("Activity logs cleared")
    
    def export_logs(self, filepath: str, date_from: Optional[datetime.date] = None) -> bool:
        """
        Export logs to a JSON file.
        
        Args:
            filepath: Path to export file
            date_from: Optional date to filter from
            
        Returns:
            True if successful, False otherwise
        """
        try:
            activities_to_export = self.activities
            
            if date_from:
                activities_to_export = [
                    a for a in self.activities
                    if datetime.datetime.fromisoformat(a['timestamp']).date() >= date_from
                ]
            
            export_data = {
                'exported_at': datetime.datetime.now().isoformat(),
                'total_entries': len(activities_to_export),
                'activities': activities_to_export
            }
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, indent=4, ensure_ascii=False)
            
            logger.info(f"Logs exported to {filepath}")
            return True
        except Exception as e:
            logger.error(f"Failed to export logs: {e}")
            return False
    
    def load(self) -> bool:
        """
        Load activity log from JSON file.
        
        Returns:
            bool: True if loaded successfully, False otherwise
        """
        if not os.path.exists(ACTIVITY_LOG_FILE):
            logger.info("Activity log file not found, starting fresh")
            return False
        
        try:
            with open(ACTIVITY_LOG_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.activities = data.get("activities", [])
                self.current_devices = data.get("current_devices", {})
            logger.info(f"Activity log loaded: {len(self.activities)} entries")
            return True
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in activity log file: {e}")
            return False
        except Exception as e:
            logger.error(f"Failed to load activity log: {e}")
            return False
    
    def save(self) -> bool:
        """
        Save activity log to JSON file.
        
        Returns:
            bool: True if saved successfully, False otherwise
        """
        data = {
            "last_updated": datetime.datetime.now().isoformat(),
            "total_entries": len(self.activities),
            "activities": self.activities,
            "current_devices": self.current_devices
        }
        
        try:
            with open(ACTIVITY_LOG_FILE, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            return True
        except Exception as e:
            logger.error(f"Failed to save activity log: {e}")
            return False
