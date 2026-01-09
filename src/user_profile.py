"""
User Profile Module
Manages user profile data persistence.
"""
import json
import os
import logging
import hashlib
import secrets
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
        self.role: str = "Security Operations Administrator"
        self.email: str = "admin.ops@hidshield.com"
        self.department: str = "IT Operations"
        self.unique_id: str = "HID-SEC-8829-X"
        self.password: str = "admin123"  # In real app, never store plaintext!
        self.security_key: str = self._generate_security_key()
        self.load()
    
    def _generate_security_key(self) -> str:
        """Generate a random security key."""
        return secrets.token_hex(16)
    
    def get_password_hash(self) -> str:
        """Get SHA-256 hash of the password."""
        return hashlib.sha256(self.password.encode()).hexdigest()

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
                self.unique_id = data.get("unique_id", self.unique_id)
                self.password = data.get("password", self.password)
                self.security_key = data.get("security_key", self.security_key)
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
            "department": self.department,
            "unique_id": self.unique_id,
            "password": self.password,
            "security_key": self.security_key
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
