import customtkinter as ctk
from typing import Callable, Dict, Any
from src.theme import Theme

class NavigationSidebar(ctk.CTkFrame):
    """
    Navigation Sidebar component handling navigation buttons and user info display.
    """
    def __init__(self, parent: Any, user_profile: Any, callbacks: Dict[str, Callable]) -> None:
        super().__init__(parent, width=240, corner_radius=0, fg_color=Theme.BG_SIDEBAR)
        
        self.user_profile = user_profile
        self.callbacks = callbacks
        
        self.grid(row=0, column=0, sticky="nsew")
        self.grid_rowconfigure(10, weight=1)
        
        self._setup_logo()
        self._setup_navigation()
        self._setup_divider()
        self._setup_user_info()

    def _setup_logo(self) -> None:
        """Setup the application logo."""
        logo_container = ctk.CTkFrame(self, fg_color="transparent")
        logo_container.grid(row=0, column=0, padx=20, pady=(30, 40))
        
        ctk.CTkLabel(
            logo_container,
            text="⚡",
            font=ctk.CTkFont(family=Theme.FONT_FAMILY, size=32)
        ).pack()
        
        ctk.CTkLabel(
            logo_container,
            text="DEVICE MONITOR",
            font=ctk.CTkFont(family=Theme.FONT_FAMILY, size=16, weight="bold"),
            text_color=(Theme.PRIMARY, "#5CA8E0")
        ).pack()
        
        ctk.CTkLabel(
            logo_container,
            text="PRO",
            font=ctk.CTkFont(family=Theme.FONT_FAMILY, size=11, weight="bold"),
            text_color=Theme.TEXT_SUB
        ).pack()

    def _setup_navigation(self) -> None:
        """Setup navigation buttons."""
        # Dashboard Button
        self.dash_btn = ctk.CTkButton(
            self,
            text="📊 Dashboard",
            command=self.callbacks.get("dashboard"),
            anchor="w",
            height=45,
            font=ctk.CTkFont(family=Theme.FONT_FAMILY, size=14, weight="bold"),
            corner_radius=8,
            hover_color=(Theme.PRIMARY_Hover, "#1A5687")
        )
        self.dash_btn.grid(row=1, column=0, padx=20, pady=8, sticky="ew")
        
        # Activity Log Button
        self.activity_btn = ctk.CTkButton(
            self,
            text="📋 Activity Log",
            command=self.callbacks.get("activity"),
            fg_color="transparent",
            anchor="w",
            height=45,
            font=ctk.CTkFont(family=Theme.FONT_FAMILY, size=14),
            corner_radius=8,
            hover_color=(Theme.SECONDARY, "#1F1F1F")
        )
        self.activity_btn.grid(row=2, column=0, padx=20, pady=8, sticky="ew")

        # Custom Scan Button
        self.scan_btn = ctk.CTkButton(
            self,
            text="📂 Custom Scan",
            command=self.callbacks.get("scan"),
            fg_color="transparent",
            anchor="w",
            height=45,
            font=ctk.CTkFont(family=Theme.FONT_FAMILY, size=14),
            corner_radius=8,
            hover_color=(Theme.SECONDARY, "#1F1F1F")
        )
        self.scan_btn.grid(row=3, column=0, padx=20, pady=8, sticky="ew")

        # Profile Button
        self.profile_btn = ctk.CTkButton(
            self,
            text="👤 User Profile",
            command=self.callbacks.get("profile"),
            fg_color="transparent",
            anchor="w",
            height=45,
            font=ctk.CTkFont(family=Theme.FONT_FAMILY, size=14),
            corner_radius=8,
            hover_color=(Theme.SECONDARY, "#1F1F1F")
        )
        self.profile_btn.grid(row=4, column=0, padx=20, pady=8, sticky="ew")

    def _setup_divider(self) -> None:
        """Setup visual divider."""
        ctk.CTkFrame(
            self,
            height=2,
            fg_color=(Theme.SECONDARY, "#1F1F1F")
        ).grid(row=9, column=0, padx=30, pady=20, sticky="ew")

    def _setup_user_info(self) -> None:
        """Setup user information display at bottom."""
        user_container = ctk.CTkFrame(self, fg_color="transparent")
        user_container.grid(row=11, column=0, pady=(0, 20), padx=20)
        
        ctk.CTkLabel(
            user_container,
            text="👤",
            font=ctk.CTkFont(family=Theme.FONT_FAMILY, size=14)
        ).pack(side="left", padx=(0, 8))
        
        self.user_label = ctk.CTkLabel(
            user_container,
            text=self.user_profile.name,
            font=ctk.CTkFont(family=Theme.FONT_FAMILY, size=12, weight="bold"),
            text_color=(Theme.PRIMARY, "#5CA8E0")
        )
        self.user_label.pack(side="left")

    def update_selection(self, view_name: str) -> None:
        """Update button visual states based on current view."""
        # Reset all
        common_style = {
            "fg_color": "transparent",
            "font": ctk.CTkFont(family=Theme.FONT_FAMILY, size=14)
        }
        
        self.dash_btn.configure(**common_style)
        self.activity_btn.configure(**common_style)
        self.profile_btn.configure(**common_style)
        if hasattr(self, 'scan_btn'):
            self.scan_btn.configure(**common_style)
        
        # Highlight active
        active_style = {
            "fg_color": (Theme.PRIMARY, "#1F6AA5"),
            "font": ctk.CTkFont(family=Theme.FONT_FAMILY, size=14, weight="bold")
        }
        
        if view_name == "dashboard":
            self.dash_btn.configure(**active_style)
            self.dash_btn.configure(text="📊 Dashboard")
        elif view_name == "activity_log":
            self.activity_btn.configure(**active_style)
            self.activity_btn.configure(text="📋 Activity Log")
        elif view_name == "profile":
            self.profile_btn.configure(**active_style)
            self.profile_btn.configure(text="👤 User Profile")
        elif view_name == "scan":
            self.scan_btn.configure(**active_style)
            self.scan_btn.configure(text="📂 Custom Scan")

    def update_user_name(self, name: str) -> None:
        """Update displayed user name."""
        if hasattr(self, 'user_label'):
            self.user_label.configure(text=name)
