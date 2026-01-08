"""
User Profile Module
Manages user profile data persistence.
"""
import json
import os
import logging
from typing import Optional

PROFILE_FILE = "user_profile.json"

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class UserProfile:
    """Manages user profile information and persistence."""
    
    def __init__(self):
        """Initialize user profile with default values."""
        self.name: str = "Admin User"
        self.role: str = "System Administrator"
        self.email: str = "admin@company.com"
        self.department: str = "IT Operations"
        self.load()

    def load(self) -> bool:
        """
        Load user profile from JSON file.
        
        Returns:
            bool: True if loaded successfully, False otherwise
        """
        if not os.path.exists(PROFILE_FILE):
            logger.info(f"Profile file not found, using defaults")
            return False
            
        try:
            with open(PROFILE_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.name = data.get("name", self.name)
                self.role = data.get("role", self.role)
                self.email = data.get("email", self.email)
                self.department = data.get("department", self.department)
            logger.info("Profile loaded successfully")
            return True
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in profile file: {e}")
            return False
        except Exception as e:
            logger.error(f"Failed to load profile: {e}")
            return False

    def save(self) -> bool:
        """
        Save user profile to JSON file.
        
        Returns:
            bool: True if saved successfully, False otherwise
        """
        data = {
            "name": self.name,
            "role": self.role,
            "email": self.email,
            "department": self.department
        }
        
        try:
            with open(PROFILE_FILE, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            logger.info("Profile saved successfully")
            return True
        except Exception as e:
            logger.error(f"Failed to save profile: {e}")
            raise
    
    def validate(self) -> tuple[bool, Optional[str]]:
        """
        Validate profile data.
        
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not self.name or not self.name.strip():
            return False, "Name cannot be empty"
        
        if self.email and '@' not in self.email:
            return False, "Invalid email format"
        
        return True, None
