"""
Modern GUI Module for Device Monitor Pro using CustomTkinter
Provides a sleek dark-themed interface with enhanced visuals.
"""
import customtkinter as ctk
from tkinter import ttk, messagebox, filedialog
import threading
from typing import Dict, Optional
import datetime
from src.device_manager import DeviceManager
from src.user_profile import UserProfile
from src.system_activity_log import ActivityLog, ActivityType

# Set CustomTkinter appearance
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


class DashboardApp(ctk.CTk):
    """Main application class for Device Monitor Pro with CustomTkinter."""
    
    def __init__(self):
        """Initialize the modern dashboard application."""
        super().__init__()
        
        self.title("Device Monitor Pro")
        self.geometry("1200x800")
        
        # Data Managers
        self.dm = DeviceManager()
        self.user_profile = UserProfile()
        self.activity_log = ActivityLog()
        
        # State variables
        self.current_devices: Dict = {}
        self.current_view: Optional[str] = None
        self.is_refreshing = False
        self.last_update_time: Optional[datetime.datetime] = None

        # Grid Configuration
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self._setup_layout()
        self._setup_keyboard_shortcuts()
        
        # Start Dashboard by default
        self.show_dashboard()
        
        # Start background refresh loop
        self._start_refresh_loop()
    
    def _setup_keyboard_shortcuts(self):
        """Setup keyboard shortcuts for better UX."""
        self.bind('<F5>', lambda e: self._manual_refresh())
        self.bind('<Control-f>', lambda e: self._focus_search())
        self.bind('<Escape>', lambda e: self.search_entry.delete(0, 'end') if hasattr(self, 'search_entry') else None)

    def _setup_layout(self):
        """Setup the main layout with sidebar and content area."""
        # --- Sidebar ---
        self.sidebar = ctk.CTkFrame(self, width=240, corner_radius=0, fg_color=("#1a1a1a", "#0d0d0d"))
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_rowconfigure(10, weight=1)
        
        # Logo with gradient-like effect
        logo_container = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        logo_container.grid(row=0, column=0, padx=20, pady=(30, 40))
        
        ctk.CTkLabel(
            logo_container,
            text="⚡",
            font=ctk.CTkFont(size=32)
        ).pack()
        
        self.logo_label = ctk.CTkLabel(
            logo_container,
            text="DEVICE MONITOR",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=("#3B8ED0", "#5CA8E0")
        )
        self.logo_label.pack()
        
        ctk.CTkLabel(
            logo_container,
            text="PRO",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color="gray"
        ).pack()

        # Navigation Buttons with improved styling
        self.dash_btn = ctk.CTkButton(
            self.sidebar,
            text="📊 Dashboard",
            command=self.show_dashboard,
            anchor="w",
            height=45,
            font=ctk.CTkFont(size=14, weight="bold"),
            corner_radius=8,
            hover_color=("#2E77B5", "#1A5687")
        )
        self.dash_btn.grid(row=1, column=0, padx=20, pady=8, sticky="ew")
        
        self.activity_btn = ctk.CTkButton(
            self.sidebar,
            text="📋 Activity Log",
            command=self.show_activity_log,
            fg_color="transparent",
            anchor="w",
            height=45,
            font=ctk.CTkFont(size=14),
            corner_radius=8,
            hover_color=("#2B2B2B", "#1F1F1F")
        )
        self.activity_btn.grid(row=2, column=0, padx=20, pady=8, sticky="ew")
        
        self.profile_btn = ctk.CTkButton(
            self.sidebar,
            text="👤 User Profile",
            command=self.show_profile,
            fg_color="transparent",
            anchor="w",
            height=45,
            font=ctk.CTkFont(size=14),
            corner_radius=8,
            hover_color=("#2B2B2B", "#1F1F1F")
        )
        self.profile_btn.grid(row=3, column=0, padx=20, pady=8, sticky="ew")
        
        # Divider
        ctk.CTkFrame(
            self.sidebar,
            height=2,
            fg_color=("#2B2B2B", "#1F1F1F")
        ).grid(row=9, column=0, padx=30, pady=20, sticky="ew")

        # User Info at Bottom with better styling
        user_container = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        user_container.grid(row=11, column=0, pady=(0, 20), padx=20)
        
        ctk.CTkLabel(
            user_container,
            text="👤",
            font=ctk.CTkFont(size=14)
        ).pack(side="left", padx=(0, 8))
        
        self.user_label = ctk.CTkLabel(
            user_container,
            text=self.user_profile.name,
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=("#3B8ED0", "#5CA8E0")
        )
        self.user_label.pack(side="left")

        # --- Main Content Area ---
        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.main_container.grid_columnconfigure(0, weight=1)

    def _clear_content(self):
        """Clear the main content area."""
        for widget in self.main_container.winfo_children():
            widget.destroy()

    # ========================== VIEWS ==========================
    
    def show_dashboard(self):
        """Display the main dashboard view with device monitoring."""
        if self.current_view == "dashboard":
            return
            
        self._clear_content()
        self.current_view = "dashboard"
        
        # Update button states with enhanced visual feedback
        self.dash_btn.configure(
            fg_color=("#3B8ED0", "#1F6AA5"),
            text="📊 Dashboard",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.activity_btn.configure(
            fg_color="transparent",
            text="📋 Activity Log",
            font=ctk.CTkFont(size=14)
        )
        self.profile_btn.configure(
            fg_color="transparent",
            text="👤 User Profile",
            font=ctk.CTkFont(size=14)
        )
        
        # Log activity
        self.activity_log.log_activity(ActivityType.REFRESH_TRIGGERED, "Dashboard refreshed", "System")
        
        # 1. Statistics Cards Row
        self.stats_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.stats_frame.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        
        self.stats_cards = {
            "total": self._create_stat_card(self.stats_frame, "Total Devices", "0", "�", 0, "#3B8ED0"),
            "usb": self._create_stat_card(self.stats_frame, "USB Devices", "0", "🔌", 1, "#27AE60"),
            "hid": self._create_stat_card(self.stats_frame, "HID Devices", "0", "⌨️", 2, "#F39C12"),
            "network": self._create_stat_card(self.stats_frame, "Network", "0", "🌐", 3, "#9B59B6"),
        }

        # 2. Action Bar (Search + Refresh)
        self.action_bar = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.action_bar.grid(row=1, column=0, sticky="ew", pady=(0, 15))
        
        # Search container with icon
        search_container = ctk.CTkFrame(self.action_bar, fg_color="transparent")
        search_container.pack(side="left")
        
        self.search_entry = ctk.CTkEntry(
            search_container,
            placeholder_text="🔍 Search devices by name, category, or manufacturer...",
            width=450,
            height=40,
            font=ctk.CTkFont(size=13),
            corner_radius=10,
            border_width=2
        )
        self.search_entry.pack(side="left")
        self.search_entry.bind("<KeyRelease>", lambda e: self._on_search_changed())
        
        # Status with icon
        status_frame = ctk.CTkFrame(self.action_bar, fg_color="transparent")
        status_frame.pack(side="right", padx=(10, 0))
        
        self.refresh_btn = ctk.CTkButton(
            status_frame,
            text="🔄 Refresh",
            command=self._manual_refresh,
            width=130,
            height=40,
            font=ctk.CTkFont(size=13, weight="bold"),
            corner_radius=10,
            fg_color=("#27AE60", "#229954"),
            hover_color=("#1E8449", "#196F3D")
        )
        self.refresh_btn.pack(side="right", padx=(10, 0))
        
        self.lbl_status = ctk.CTkLabel(
            status_frame,
            text="⚡ Ready",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=("#3B8ED0", "#5CA8E0")
        )
        self.lbl_status.pack(side="right", padx=15)

        # 3. Content Body (Tabbed Tree + Details)
        self.body_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.body_frame.grid(row=2, column=0, sticky="nsew")
        self.main_container.grid_rowconfigure(2, weight=1)
        self.body_frame.grid_columnconfigure(0, weight=2)
        self.body_frame.grid_columnconfigure(1, weight=1)

        # Tree View Panel with Tabs
        self.tree_frame = ctk.CTkFrame(
            self.body_frame,
            corner_radius=12,
            border_width=2,
            border_color=("#3B8ED0", "#1F6AA5")
        )
        self.tree_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        
        # Create Tab View for Physical and Virtual with enhanced styling
        self.device_tabview = ctk.CTkTabview(
            self.tree_frame,
            corner_radius=10,
            segmented_button_fg_color=("#2B2B2B", "#1A1A1A"),
            segmented_button_selected_color=("#3B8ED0", "#1F6AA5"),
            segmented_button_selected_hover_color=("#2E77B5", "#1A5687")
        )
        self.device_tabview.pack(expand=True, fill="both", padx=8, pady=8)
        
        # Add tabs with enhanced icons
        self.device_tabview.add("🔌 Physical Devices")
        self.device_tabview.add("💻 Virtual Devices")
        
        # Configure ttk.Treeview style for dark theme with enhanced styling
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Treeview",
                       background="#2B2B2B",
                       foreground="white",
                       fieldbackground="#2B2B2B",
                       borderwidth=0,
                       rowheight=35,
                       font=('Segoe UI', 11))
        style.map('Treeview', 
                 background=[('selected', '#3B8ED0')],
                 foreground=[('selected', 'white')])
        style.configure("Treeview.Heading",
                       background="#1F1F1F",
                       foreground="#3B8ED0",
                       borderwidth=0,
                       font=('Segoe UI', 11, 'bold'))
        
        # Create Treeview for Physical Devices
        physical_container = ctk.CTkFrame(
            self.device_tabview.tab("🔌 Physical Devices"),
            fg_color="transparent"
        )
        physical_container.pack(expand=True, fill="both", padx=5, pady=5)
        
        self.tree_physical = ttk.Treeview(
            physical_container, 
            show="tree", 
            selectmode="browse"
        )
        self.tree_physical.pack(expand=True, fill="both")
        self.tree_physical.bind("<<TreeviewSelect>>", self._on_device_select)
        
        # Create Treeview for Virtual Devices
        virtual_container = ctk.CTkFrame(
            self.device_tabview.tab("💻 Virtual Devices"),
            fg_color="transparent"
        )
        virtual_container.pack(expand=True, fill="both", padx=5, pady=5)
        
        self.tree_virtual = ttk.Treeview(
            virtual_container, 
            show="tree", 
            selectmode="browse"
        )
        self.tree_virtual.pack(expand=True, fill="both")
        self.tree_virtual.bind("<<TreeviewSelect>>", self._on_device_select)
        
        # Keep reference to active tree (for backward compatibility)
        self.tree = self.tree_physical

        # Details Panel
        self.details_frame = ctk.CTkScrollableFrame(
            self.body_frame, 
            fg_color=("#DBDBDB", "#2B2B2B"),
            corner_radius=12,
            border_width=2,
            border_color=("#F39C12", "#D68910")
        )
        self.details_frame.grid(row=0, column=1, sticky="nsew")
        
        # Details Header with enhanced styling
        self.details_header = ctk.CTkFrame(self.details_frame, fg_color="transparent")
        self.details_header.pack(fill="x", padx=15, pady=(15, 10))
        
        # Icon + Title
        header_content = ctk.CTkFrame(self.details_header, fg_color="transparent")
        header_content.pack(side="left")
        
        ctk.CTkLabel(
            header_content,
            text="📋",
            font=ctk.CTkFont(size=20)
        ).pack(side="left", padx=(0, 8))
        
        ctk.CTkLabel(
            header_content,
            text="Device Details",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=("#F39C12", "#D68910")
        ).pack(side="left")
        
        self.btn_copy = ctk.CTkButton(
            self.details_header,
            text="📋 Copy",
            command=self._copy_device_info,
            width=100,
            height=35,
            state="disabled",
            font=ctk.CTkFont(size=12, weight="bold"),
            corner_radius=8,
            fg_color=("#3B8ED0", "#1F6AA5"),
            hover_color=("#2E77B5", "#1A5687")
        )
        self.btn_copy.pack(side="right")
        
        # Details Fields
        self.detail_vars = {
            "Name": ctk.StringVar(),
            "Category": ctk.StringVar(),
            "Type": ctk.StringVar(),
            "Port Type": ctk.StringVar(),
            "Status": ctk.StringVar(),
            "Manufacturer": ctk.StringVar(),
            "VID": ctk.StringVar(),
            "PID": ctk.StringVar(),
            "Driver": ctk.StringVar(),
            "Path": ctk.StringVar()
        }
        
        for label_text, var in self.detail_vars.items():
            self._create_detail_field(self.details_frame, label_text, var)

        # Initial Load
        self._refresh_data()

    def _create_stat_card(self, parent, title, value, icon, col, accent_color="#3B8ED0"):
        """Create a statistics card widget with enhanced styling."""
        card = ctk.CTkFrame(
            parent, 
            height=110,
            corner_radius=12,
            border_width=2,
            border_color=(accent_color, accent_color)
        )
        card.grid(row=0, column=col, padx=8, sticky="nsew")
        parent.grid_columnconfigure(col, weight=1)
        
        # Icon with colored background
        icon_frame = ctk.CTkFrame(
            card,
            width=50,
            height=50,
            corner_radius=25,
            fg_color=(accent_color, accent_color)
        )
        icon_frame.pack(pady=(12, 8))
        icon_frame.pack_propagate(False)
        
        ctk.CTkLabel(
            icon_frame,
            text=icon,
            font=ctk.CTkFont(size=24)
        ).pack(expand=True)
        
        # Value label
        value_var = ctk.StringVar(value=value)
        ctk.CTkLabel(
            card,
            textvariable=value_var,
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color=(accent_color, accent_color)
        ).pack(pady=2)
        
        # Title label
        ctk.CTkLabel(
            card,
            text=title,
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color="gray"
        ).pack(pady=(2, 12))
        
        return value_var

    def _create_detail_field(self, parent, label, variable):
        """Create a detail field row with enhanced styling."""
        row = ctk.CTkFrame(parent, fg_color="transparent")
        row.pack(fill="x", padx=15, pady=6)
        
        # Label with icon based on field type
        label_icons = {
            "Name": "📝",
            "Category": "📁",
            "Type": "🔧",
            "Port Type": "🔌",
            "Status": "📊",
            "Manufacturer": "🏢",
            "VID": "🆔",
            "PID": "🆔",
            "Driver": "⚙️",
            "Path": "📍"
        }
        
        label_frame = ctk.CTkFrame(row, fg_color="transparent")
        label_frame.pack(anchor="w", pady=(0, 3))
        
        icon = label_icons.get(label, "•")
        ctk.CTkLabel(
            label_frame,
            text=f"{icon} {label.upper()}",
            font=ctk.CTkFont(size=10, weight="bold"),
            text_color=("#3B8ED0", "#5CA8E0"),
            anchor="w"
        ).pack(side="left")
        
        entry = ctk.CTkEntry(
            row,
            textvariable=variable,
            state="readonly",
            font=ctk.CTkFont(size=12),
            height=35,
            corner_radius=8,
            border_width=1
        )
        entry.pack(fill="x", pady=(2, 0))

    def show_profile(self):
        """Display the user profile management view with security credentials."""
        if self.current_view == "profile":
            return
            
        self._clear_content()
        self.current_view = "profile"
        
        # Update button states with enhanced visual feedback
        self.dash_btn.configure(
            fg_color="transparent",
            text="📊 Dashboard",
            font=ctk.CTkFont(size=14)
        )
        self.activity_btn.configure(
            fg_color="transparent",
            text="📋 Activity Log",
            font=ctk.CTkFont(size=14)
        )
        self.profile_btn.configure(
            fg_color=("#3B8ED0", "#1F6AA5"),
            text="👤 User Profile",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        
        # Main container with padding
        main_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        main_frame.pack(fill="both", expand=True)
        
        # Header Section
        header_frame = ctk.CTkFrame(main_frame, fg_color=("#2B2B2B", "#1A1A1A"), height=120)
        header_frame.pack(fill="x", padx=0, pady=(0, 20))
        header_frame.pack_propagate(False)
        
        # Profile Icon and Name in Header
        header_content = ctk.CTkFrame(header_frame, fg_color="transparent")
        header_content.pack(side="left", padx=30, pady=20)
        
        # Circular Avatar
        avatar = ctk.CTkLabel(
            header_content,
            text="👤",
            font=ctk.CTkFont(size=40),
            width=80,
            height=80,
            fg_color=["#3B8ED0", "#1F6AA5"],
            corner_radius=40
        )
        avatar.pack(side="left", padx=(0, 20))
        
        # Name and Role
        name_frame = ctk.CTkFrame(header_content, fg_color="transparent")
        name_frame.pack(side="left")
        
        ctk.CTkLabel(
            name_frame,
            text=self.user_profile.name,
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="white"
        ).pack(anchor="w")
        
        ctk.CTkLabel(
            name_frame,
            text=self.user_profile.role,
            font=ctk.CTkFont(size=12),
            text_color=["#3B8ED0", "#1F6AA5"]
        ).pack(anchor="w")
        
        # Content Container (Two columns)
        content_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=20)
        content_frame.grid_columnconfigure(0, weight=1)
        content_frame.grid_columnconfigure(1, weight=1)
        
        # Left Panel - Personal Information
        left_panel = ctk.CTkFrame(content_frame, fg_color=("#2B2B2B", "#1A1A1A"))
        left_panel.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        
        # Left Panel Header
        left_header = ctk.CTkFrame(left_panel, fg_color="transparent")
        left_header.pack(fill="x", padx=20, pady=(20, 15))
        
        ctk.CTkLabel(
            left_header,
            text="👤",
            font=ctk.CTkFont(size=16)
        ).pack(side="left", padx=(0, 10))
        
        ctk.CTkLabel(
            left_header,
            text="Personal Information",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(side="left")
        
        # Personal Info Fields
        self.var_name = ctk.StringVar(value=self.user_profile.name)
        self.var_unique_id = ctk.StringVar(value=self.user_profile.unique_id)
        self.var_email = ctk.StringVar(value=self.user_profile.email)
        
        self._create_security_field(left_panel, "FULL NAME", self.var_name, "👤", readonly=False)
        self._create_security_field(left_panel, "UNIQUE ID", self.var_unique_id, "🔑", readonly=True)
        self._create_security_field(left_panel, "GMAIL / EMAIL", self.var_email, "📧", readonly=False)
        
        # Right Panel - Security Credentials
        right_panel = ctk.CTkFrame(content_frame, fg_color=("#2B2B2B", "#1A1A1A"))
        right_panel.grid(row=0, column=1, sticky="nsew", padx=(10, 0))
        
        # Right Panel Header
        right_header = ctk.CTkFrame(right_panel, fg_color="transparent")
        right_header.pack(fill="x", padx=20, pady=(20, 15))
        
        ctk.CTkLabel(
            right_header,
            text="🔒",
            font=ctk.CTkFont(size=16)
        ).pack(side="left", padx=(0, 10))
        
        ctk.CTkLabel(
            right_header,
            text="Security Credentials",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(side="left")
        
        # Security Fields
        self.var_password = ctk.StringVar(value=self.user_profile.password)
        self.var_security_key = ctk.StringVar(value=self.user_profile.security_key)
        self.var_password_hash = ctk.StringVar(value=self.user_profile.get_password_hash())
        self.password_visible = False
        
        self._create_password_field(right_panel, "PASSWORD", self.var_password)
        self._create_security_field(right_panel, "SECURITY KEY", self.var_security_key, "🔑", readonly=True)
        self._create_hash_field(right_panel, "PASSWORD HASH", self.var_password_hash)
        
        # Save Button
        save_btn = ctk.CTkButton(
            main_frame,
            text="💾 Save Changes",
            command=self._save_profile,
            height=45,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#27AE60",
            hover_color="#229954"
        )
        save_btn.pack(pady=(20, 0), padx=20, fill="x")
    
    def _create_security_field(self, parent, label, variable, icon="", readonly=False):
        """Create a security-styled input field."""
        container = ctk.CTkFrame(parent, fg_color="transparent")
        container.pack(fill="x", padx=20, pady=10)
        
        # Label
        ctk.CTkLabel(
            container,
            text=label,
            font=ctk.CTkFont(size=9, weight="bold"),
            text_color="gray",
            anchor="w"
        ).pack(anchor="w", pady=(0, 5))
        
        # Entry Frame with Icon
        entry_frame = ctk.CTkFrame(container, fg_color=("#3B3B3B", "#2A2A2A"), height=40)
        entry_frame.pack(fill="x")
        entry_frame.pack_propagate(False)
        
        if icon:
            ctk.CTkLabel(
                entry_frame,
                text=icon,
                font=ctk.CTkFont(size=14),
                width=30
            ).pack(side="left", padx=(10, 5))
        
        entry = ctk.CTkEntry(
            entry_frame,
            textvariable=variable,
            font=ctk.CTkFont(size=12),
            border_width=0,
            fg_color="transparent",
            state="readonly" if readonly else "normal"
        )
        entry.pack(side="left", fill="both", expand=True, padx=(5, 10))
    
    def _create_password_field(self, parent, label, variable):
        """Create a password field with show/hide toggle."""
        container = ctk.CTkFrame(parent, fg_color="transparent")
        container.pack(fill="x", padx=20, pady=10)
        
        # Label
        ctk.CTkLabel(
            container,
            text=label,
            font=ctk.CTkFont(size=9, weight="bold"),
            text_color="gray",
            anchor="w"
        ).pack(anchor="w", pady=(0, 5))
        
        # Entry Frame
        entry_frame = ctk.CTkFrame(container, fg_color=("#3B3B3B", "#2A2A2A"), height=40)
        entry_frame.pack(fill="x")
        entry_frame.pack_propagate(False)
        
        # Lock Icon
        ctk.CTkLabel(
            entry_frame,
            text="🔒",
            font=ctk.CTkFont(size=14),
            width=30
        ).pack(side="left", padx=(10, 5))
        
        # Password Entry
        self.password_entry = ctk.CTkEntry(
            entry_frame,
            textvariable=variable,
            font=ctk.CTkFont(size=12),
            border_width=0,
            fg_color="transparent",
            show="●"
        )
        self.password_entry.pack(side="left", fill="both", expand=True, padx=(5, 5))
        
        # Toggle Button
        self.eye_btn = ctk.CTkButton(
            entry_frame,
            text="👁️",
            width=30,
            height=30,
            fg_color="transparent",
            hover_color=("#4A4A4A", "#3A3A3A"),
            command=self._toggle_password_visibility
        )
        self.eye_btn.pack(side="right", padx=5)
    
    def _create_hash_field(self, parent, label, variable):
        """Create a hash display field with SHA-256 badge."""
        container = ctk.CTkFrame(parent, fg_color="transparent")
        container.pack(fill="x", padx=20, pady=10)
        
        # Label
        ctk.CTkLabel(
            container,
            text=label,
            font=ctk.CTkFont(size=9, weight="bold"),
            text_color="gray",
            anchor="w"
        ).pack(anchor="w", pady=(0, 5))
        
        # Entry Frame
        entry_frame = ctk.CTkFrame(container, fg_color=("#3B3B3B", "#2A2A2A"), height=40)
        entry_frame.pack(fill="x")
        entry_frame.pack_propagate(False)
        
        # SHA-256 Badge
        badge = ctk.CTkLabel(
            entry_frame,
            text="SHA-256",
            font=ctk.CTkFont(size=8, weight="bold"),
            text_color="white",
            fg_color=["#3B8ED0", "#1F6AA5"],
            corner_radius=3,
            padx=8,
            pady=2
        )
        badge.pack(side="left", padx=10)
        
        # Hash Display (truncated)
        hash_value = variable.get()
        display_hash = hash_value[:30] + "..." if len(hash_value) > 30 else hash_value
        
        ctk.CTkLabel(
            entry_frame,
            text=display_hash,
            font=ctk.CTkFont(size=10, family="Consolas"),
            text_color="gray",
            anchor="w"
        ).pack(side="left", fill="both", expand=True, padx=5)
    
    def _toggle_password_visibility(self):
        """Toggle password visibility."""
        self.password_visible = not self.password_visible
        if self.password_visible:
            self.password_entry.configure(show="")
            self.eye_btn.configure(text="🙈")
        else:
            self.password_entry.configure(show="●")
            self.eye_btn.configure(text="👁️")
        
        # Save Button
        save_btn = ctk.CTkButton(
            card,
            text="💾 Save Changes",
            command=self._save_profile,
            height=45,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#27AE60",
            hover_color="#229954"
        )
        save_btn.pack(pady=(20, 40), padx=80, fill="x")

    def _create_profile_entry(self, parent, label, variable):
        """Create a profile entry field."""
        container = ctk.CTkFrame(parent, fg_color="transparent")
        container.pack(fill="x", pady=10)
        
        ctk.CTkLabel(
            container,
            text=label,
            font=ctk.CTkFont(size=12),
            text_color="gray",
            anchor="w"
        ).pack(anchor="w")
        
        ctk.CTkEntry(
            container,
            textvariable=variable,
            height=40,
            font=ctk.CTkFont(size=13)
        ).pack(fill="x", pady=(5, 0))

    def _save_profile(self):
        """Save user profile changes."""
        try:
            self.user_profile.name = self.var_name.get()
            self.user_profile.email = self.var_email.get()
            self.user_profile.password = self.var_password.get()
            
            # Update hash display
            self.var_password_hash.set(self.user_profile.get_password_hash())
            
            self.user_profile.save()
            
            # Log activity
            self.activity_log.log_activity(ActivityType.PROFILE_UPDATED, "User profile updated", self.user_profile.name)
            
            # Update Sidebar
            self.user_label.configure(text=self.user_profile.name)
            messagebox.showinfo("Success", "✅ Profile updated successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"❌ Failed to save profile: {e}")
    
    def show_activity_log(self):
        """Display the system activity log view."""
        if self.current_view == "activity_log":
            return
        
        self._clear_content()
        self.current_view = "activity_log"
        
        # Update button states with enhanced visual feedback
        self.dash_btn.configure(
            fg_color="transparent",
            text="📊 Dashboard",
            font=ctk.CTkFont(size=14)
        )
        self.activity_btn.configure(
            fg_color=("#3B8ED0", "#1F6AA5"),
            text="📋 Activity Log",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.profile_btn.configure(
            fg_color="transparent",
            text="👤 User Profile",
            font=ctk.CTkFont(size=14)
        )
        
        # Main container
        main_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        main_frame.pack(fill="both", expand=True)
        
        # Header with Statistics
        header_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        header_frame.pack(fill="x", pady=(0, 15))
        
        ctk.CTkLabel(
            header_frame,
            text="📋 System Activity Log",
            font=ctk.CTkFont(size=24, weight="bold")
        ).pack(side="left")
        
        # Get statistics
        stats = self.activity_log.get_statistics()
        
        # Stats cards
        stats_container = ctk.CTkFrame(header_frame, fg_color="transparent")
        stats_container.pack(side="right")
        
        stats_info = [
            (f"{stats['today_activities']}", "Today", "📅"),
            (f"{stats['devices_connected_today']}", "Connected", "🟢"),
            (f"{stats['devices_disconnected_today']}", "Disconnected", "🔴"),
            (f"{stats['total_activities']}", "Total", "📊")
        ]
        
        for idx, (value, label, icon) in enumerate(stats_info):
            card = ctk.CTkFrame(stats_container, width=100, height=60)
            card.pack(side="left", padx=5)
            card.pack_propagate(False)
            
            ctk.CTkLabel(
                card,
                text=icon,
                font=ctk.CTkFont(size=16)
            ).pack(pady=(5, 0))
            
            ctk.CTkLabel(
                card,
                text=value,
                font=ctk.CTkFont(size=18, weight="bold")
            ).pack()
            
            ctk.CTkLabel(
                card,
                text=label,
                font=ctk.CTkFont(size=9),
                text_color="gray"
            ).pack(pady=(0, 5))
        
        # Action bar
        action_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        action_frame.pack(fill="x", pady=(0, 10))
        
        # Filter dropdown
        self.filter_var = ctk.StringVar(value="All Activities")
        filter_menu = ctk.CTkOptionMenu(
            action_frame,
            values=["All Activities", "Devices Connected", "Devices Disconnected", "System Events", "Profile Updates"],
            variable=self.filter_var,
            command=self._filter_activities,
            width=180
        )
        filter_menu.pack(side="left", padx=(0, 10))
        
        # Refresh button
        refresh_btn = ctk.CTkButton(
            action_frame,
            text="🔄 Refresh",
            command=self._refresh_activity_log,
            width=100,
            height=30
        )
        refresh_btn.pack(side="left", padx=(0, 10))
        
        # Export button
        export_btn = ctk.CTkButton(
            action_frame,
            text="📥 Export",
            command=self._export_activity_log,
            width=100,
            height=30,
            fg_color="#27AE60",
            hover_color="#229954"
        )
        export_btn.pack(side="left", padx=(0, 10))
        
        # Clear button
        clear_btn = ctk.CTkButton(
            action_frame,
            text="🗑️ Clear All",
            command=self._clear_activity_log,
            width=100,
            height=30,
            fg_color="#E74C3C",
            hover_color="#C0392B"
        )
        clear_btn.pack(side="left")
        
        # Activity list frame
        list_frame = ctk.CTkFrame(main_frame, fg_color=("#2B2B2B", "#1A1A1A"))
        list_frame.pack(fill="both", expand=True)
        
        # Scrollable frame for activities
        self.activity_scroll = ctk.CTkScrollableFrame(list_frame, fg_color="transparent")
        self.activity_scroll.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Load and display activities
        self._load_activities()
    
    def _load_activities(self, activity_filter="All Activities"):
        """Load and display activities in the log."""
        # Clear existing
        for widget in self.activity_scroll.winfo_children():
            widget.destroy()
        
        # Get activities based on filter
        if activity_filter == "Devices Connected":
            activities = self.activity_log.get_activities_by_type(ActivityType.DEVICE_CONNECTED, limit=100)
        elif activity_filter == "Devices Disconnected":
            activities = self.activity_log.get_activities_by_type(ActivityType.DEVICE_DISCONNECTED, limit=100)
        elif activity_filter == "System Events":
            system_activities = []
            for act_type in [ActivityType.SYSTEM_STARTUP, ActivityType.SYSTEM_SHUTDOWN, ActivityType.REFRESH_TRIGGERED]:
                system_activities.extend(self.activity_log.get_activities_by_type(act_type, limit=50))
            activities = sorted(system_activities, key=lambda x: x['timestamp'], reverse=True)[:100]
        elif activity_filter == "Profile Updates":
            activities = self.activity_log.get_activities_by_type(ActivityType.PROFILE_UPDATED, limit=100)
        else:
            activities = self.activity_log.get_recent_activities(limit=100)
        
        if not activities:
            ctk.CTkLabel(
                self.activity_scroll,
                text="No activities recorded yet",
                font=ctk.CTkFont(size=14),
                text_color="gray"
            ).pack(pady=50)
            return
        
        # Display each activity
        for activity in activities:
            self._create_activity_item(activity)
    
    def _create_activity_item(self, activity: Dict):
        """Create a single activity item widget."""
        # Severity colors
        severity_colors = {
            "error": "#E74C3C",
            "warning": "#F39C12",
            "success": "#27AE60",
            "info": "#3B8ED0"
        }
        
        # Icons by type
        type_icons = {
            "device_connected": "🟢",
            "device_disconnected": "🔴",
            "device_error": "⚠️",
            "system_startup": "🚀",
            "system_shutdown": "⏹️",
            "profile_updated": "👤",
            "settings_changed": "⚙️",
            "refresh_triggered": "🔄"
        }
        
        # Container for each activity
        item_frame = ctk.CTkFrame(
            self.activity_scroll,
            fg_color=("#3B3B3B", "#2A2A2A"),
            height=70
        )
        item_frame.pack(fill="x", pady=5, padx=5)
        item_frame.pack_propagate(False)
        
        # Left side - Icon and severity indicator
        left_frame = ctk.CTkFrame(item_frame, fg_color="transparent", width=60)
        left_frame.pack(side="left", fill="y", padx=(10, 5))
        left_frame.pack_propagate(False)
        
        # Severity bar
        severity_color = severity_colors.get(activity['severity'], "#3B8ED0")
        ctk.CTkFrame(
            left_frame,
            width=4,
            fg_color=severity_color
        ).pack(side="left", fill="y")
        
        # Icon
        icon = type_icons.get(activity['type'], "📋")
        ctk.CTkLabel(
            left_frame,
            text=icon,
            font=ctk.CTkFont(size=20)
        ).pack(side="left", padx=10)
        
        # Middle - Content
        content_frame = ctk.CTkFrame(item_frame, fg_color="transparent")
        content_frame.pack(side="left", fill="both", expand=True, padx=5)
        
        # Title row
        title_row = ctk.CTkFrame(content_frame, fg_color="transparent")
        title_row.pack(fill="x", pady=(8, 2))
        
        ctk.CTkLabel(
            title_row,
            text=activity['device_name'],
            font=ctk.CTkFont(size=13, weight="bold"),
            anchor="w"
        ).pack(side="left")
        
        # Type badge
        ctk.CTkLabel(
            title_row,
            text=activity['type'].replace('_', ' ').title(),
            font=ctk.CTkFont(size=9),
            text_color="white",
            fg_color=severity_color,
            corner_radius=3,
            padx=6,
            pady=2
        ).pack(side="left", padx=(10, 0))
        
        # Message
        ctk.CTkLabel(
            content_frame,
            text=activity['message'],
            font=ctk.CTkFont(size=11),
            text_color="gray",
            anchor="w"
        ).pack(fill="x", pady=(0, 2))
        
        # Details if available
        if activity.get('details'):
            details_text = " | ".join([f"{k}: {v}" for k, v in activity['details'].items() if k != 'last_seen'])
            if details_text:
                ctk.CTkLabel(
                    content_frame,
                    text=details_text,
                    font=ctk.CTkFont(size=9, family="Consolas"),
                    text_color="#666",
                    anchor="w"
                ).pack(fill="x")
        
        # Right side - Timestamp
        time_frame = ctk.CTkFrame(item_frame, fg_color="transparent", width=120)
        time_frame.pack(side="right", fill="y", padx=10)
        time_frame.pack_propagate(False)
        
        # Parse and format timestamp
        timestamp = datetime.datetime.fromisoformat(activity['timestamp'])
        time_str = timestamp.strftime("%H:%M:%S")
        date_str = timestamp.strftime("%Y-%m-%d")
        
        ctk.CTkLabel(
            time_frame,
            text=time_str,
            font=ctk.CTkFont(size=12, weight="bold"),
            anchor="e"
        ).pack(side="top", pady=(10, 0))
        
        ctk.CTkLabel(
            time_frame,
            text=date_str,
            font=ctk.CTkFont(size=9),
            text_color="gray",
            anchor="e"
        ).pack(side="top")
    
    def _filter_activities(self, choice):
        """Filter activities based on selection."""
        self._load_activities(choice)
    
    def _refresh_activity_log(self):
        """Refresh the activity log display."""
        self._load_activities(self.filter_var.get())
        self.activity_log.log_activity(ActivityType.REFRESH_TRIGGERED, "Activity log refreshed", "System")
    
    def _export_activity_log(self):
        """Export activity log to JSON file."""
        filepath = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            initialfile=f"activity_log_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        )
        
        if filepath:
            if self.activity_log.export_logs(filepath):
                messagebox.showinfo("Success", f"✅ Activity log exported to:\n{filepath}")
            else:
                messagebox.showerror("Error", "❌ Failed to export activity log")
    
    def _clear_activity_log(self):
        """Clear all activity logs after confirmation."""
        result = messagebox.askyesno(
            "Confirm Clear",
            "⚠️ Are you sure you want to clear all activity logs?\nThis action cannot be undone!"
        )
        
        if result:
            self.activity_log.clear_logs()
            self.activity_log.log_activity(ActivityType.SYSTEM_STARTUP, "Activity logs cleared", "System")
            self._load_activities(self.filter_var.get())
            messagebox.showinfo("Success", "✅ Activity logs cleared")

    def _copy_device_info(self):
        """Copy selected device information to clipboard."""
        if not hasattr(self, 'detail_vars'):
            return
        
        try:
            lines = []
            for k, var in self.detail_vars.items():
                value = var.get()
                if value and value != "N/A":
                    lines.append(f"{k}: {value}")
                
            data = "\n".join(lines)
            if data.strip():
                self.clipboard_clear()
                self.clipboard_append(data)
                self.lbl_status.configure(text="✅ Copied to clipboard!", text_color="#27AE60")
                self.after(2000, lambda: self.lbl_status.configure(text="Ready", text_color="gray"))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to copy: {e}")

    # ========================== LOGIC ==========================

    def _start_refresh_loop(self):
        """Background loop to refresh device data periodically."""
        if self.current_view == "dashboard":
            self._refresh_data()
        self.after(5000, self._start_refresh_loop)

    def _on_search_changed(self):
        """Handle search text changes."""
        if hasattr(self, 'tree_physical') and hasattr(self, 'tree_virtual'):
            self._refresh_data()

    def _focus_search(self):
        """Focus the search entry."""
        if hasattr(self, 'search_entry') and self.current_view == "dashboard":
            self.search_entry.focus_set()

    def _manual_refresh(self):
        """Manually trigger device refresh."""
        if not self.is_refreshing and self.current_view == "dashboard":
            self._refresh_data()

    def _refresh_data(self):
        """Refresh device data in background thread."""
        if self.current_view != "dashboard" or self.is_refreshing:
            return
        
        if not hasattr(self, 'tree_physical') or not hasattr(self, 'tree_virtual'):
            return
        
        self.is_refreshing = True
        if hasattr(self, 'lbl_status'):
            self.lbl_status.configure(text="⚡ Scanning devices...", text_color="#F39C12")
        if hasattr(self, 'refresh_btn'):
            self.refresh_btn.configure(state="disabled")
            
        threading.Thread(target=self._fetch_devices_thread, daemon=True).start()

    def _fetch_devices_thread(self):
        """Fetch devices in background thread."""
        try:
            devices = self.dm.get_all_devices()
            self.last_update_time = datetime.datetime.now()
            
            # Check for device changes and log them
            self.activity_log.check_device_changes(devices)
            
            self.after(0, lambda: self._update_tree(devices))
        except Exception as e:
            error_msg = f"Error scanning devices: {e}"
            self.activity_log.log_activity(ActivityType.DEVICE_ERROR, str(e), "System")
            self.after(0, lambda msg=error_msg: self._handle_fetch_error(msg))
        finally:
            self.is_refreshing = False
            self.after(0, self._enable_refresh_button)
    
    def _enable_refresh_button(self):
        """Enable the refresh button safely."""
        if hasattr(self, 'refresh_btn') and self.refresh_btn.winfo_exists():
            try:
                self.refresh_btn.configure(state="normal")
            except:
                pass
    
    def _handle_fetch_error(self, error_msg):
        """Handle device fetch errors."""
        if hasattr(self, 'lbl_status') and self.lbl_status.winfo_exists():
            try:
                self.lbl_status.configure(text="❌ Scan failed", text_color="#E74C3C")
            except:
                pass
        try:
            messagebox.showerror("Scan Error", error_msg)
        except:
            pass

    def _update_tree(self, devices):
        """Update device tree with new data, separating physical and virtual devices."""
        if self.current_view != "dashboard" or not hasattr(self, 'tree_physical'):
            return

        # Capture state from both trees
        selected_path = None
        active_tree = None
        
        for tree in [self.tree_physical, self.tree_virtual]:
            selection = tree.selection()
            if selection:
                iid = selection[0]
                if iid in self.current_devices:
                    selected_path = self.current_devices[iid].get('path')
                    active_tree = tree
                    break
        
        # Capture expanded categories from both trees
        expanded_physical = []
        expanded_virtual = []
        
        for child in self.tree_physical.get_children():
            if self.tree_physical.item(child, 'open'):
                text = self.tree_physical.item(child, "text")
                cat_name = text.split(" (")[0]
                expanded_physical.append(cat_name)
        
        for child in self.tree_virtual.get_children():
            if self.tree_virtual.item(child, 'open'):
                text = self.tree_virtual.item(child, "text")
                cat_name = text.split(" (")[0]
                expanded_virtual.append(cat_name)

        # Filter
        search_query = ""
        if hasattr(self, 'search_entry'):
            search_query = self.search_entry.get().lower()
            if search_query:
                devices = [d for d in devices if search_query in d['name'].lower() 
                           or search_query in str(d.get('manufacturer', '')).lower()
                           or search_query in d['category'].lower()]

        # Separate devices by port type
        physical_devices = [d for d in devices if d.get('port_type', 'Physical') == 'Physical']
        virtual_devices = [d for d in devices if d.get('port_type', 'Physical') == 'Virtual']

        # Update Statistics (combined)
        self._update_statistics(devices)

        # Clear both trees
        self.tree_physical.delete(*self.tree_physical.get_children())
        self.tree_virtual.delete(*self.tree_virtual.get_children())
        self.current_devices = {}
        
        # Update Physical Devices Tab
        self._populate_tree(
            self.tree_physical, 
            physical_devices, 
            expanded_physical, 
            search_query, 
            selected_path, 
            active_tree
        )
        
        # Update Virtual Devices Tab
        self._populate_tree(
            self.tree_virtual, 
            virtual_devices, 
            expanded_virtual, 
            search_query, 
            selected_path, 
            active_tree
        )

        # Update status
        if hasattr(self, 'lbl_status') and self.last_update_time:
            time_str = self.last_update_time.strftime("%H:%M:%S")
            phys_count = len(physical_devices)
            virt_count = len(virtual_devices)
            self.lbl_status.configure(
                text=f"✅ Updated at {time_str} | 🔌{phys_count} Physical | 💻{virt_count} Virtual", 
                text_color="#27AE60"
            )
    
    def _populate_tree(self, tree, devices, expanded_categories, search_query, selected_path, active_tree):
        """Populate a tree view with devices with enhanced icons."""
        if not devices:
            tree.insert("", "end", text="  ℹ️ No devices found")
            return
        
        categories = {}
        for d in devices:
            cat = d['category']
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(d)
        
        # Category icons mapping
        category_icons = {
            "USB": "🔌",
            "HID": "⌨️",
            "Keyboard": "⌨️",
            "Mouse": "🖱️",
            "Network": "🌐",
            "Storage": "💾",
            "Bluetooth": "📡"
        }
        
        # Insert by categories
        for cat in sorted(categories.keys()):
            dev_list = categories[cat]
            if not dev_list:
                continue

            is_open = bool(search_query) or cat in expanded_categories
            cat_icon = category_icons.get(cat, "📁")
            cat_id = tree.insert("", "end", text=f" {cat_icon} {cat} ({len(dev_list)})", open=is_open)
            
            for d in dev_list:
                status_str = str(d['status']).lower()
                if "ok" in status_str or "connected" in status_str:
                    status_icon = "✅"
                elif "disconnected" in status_str or "error" in status_str:
                    status_icon = "❌"
                else:
                    status_icon = "⚠️"
                    
                display_text = f"   {status_icon} {d['name']}"
                child_id = tree.insert(cat_id, "end", text=display_text)
                self.current_devices[child_id] = d
                
                # Restore selection if it was in this tree
                if selected_path and d.get('path') == selected_path and tree == active_tree:
                    tree.selection_set(child_id)
                    tree.see(child_id)
    
    def _update_statistics(self, devices):
        """Update statistics cards with device counts."""
        if not hasattr(self, 'stats_cards'):
            return
            
        total = len(devices)
        usb_count = len([d for d in devices if d['category'] == 'USB'])
        hid_count = len([d for d in devices if d['category'] in ['HID', 'Keyboard', 'Mouse']])
        network_count = len([d for d in devices if d['category'] == 'Network'])
        
        self.stats_cards['total'].set(str(total))
        self.stats_cards['usb'].set(str(usb_count))
        self.stats_cards['hid'].set(str(hid_count))
        self.stats_cards['network'].set(str(network_count))

    def _on_device_select(self, event):
        """Handle device selection in tree view."""
        # Get the tree widget that triggered the event
        tree = event.widget
        selection = tree.selection()
        
        if not selection:
            self.btn_copy.configure(state="disabled")
            return
        
        iid = selection[0]
        if iid in self.current_devices:
            d = self.current_devices[iid]
            self.detail_vars["Name"].set(d.get("name", "N/A"))
            self.detail_vars["Category"].set(d.get("category", "N/A"))
            self.detail_vars["Type"].set(d.get("type", "N/A"))
            self.detail_vars["Port Type"].set(d.get("port_type", "N/A"))
            self.detail_vars["Status"].set(d.get("status", "N/A"))
            self.detail_vars["Manufacturer"].set(d.get("manufacturer", "N/A"))
            self.detail_vars["VID"].set(d.get("vid", "N/A"))
            self.detail_vars["PID"].set(d.get("pid", "N/A"))
            self.detail_vars["Driver"].set(d.get("driver", "N/A"))
            self.detail_vars["Path"].set(d.get("path", "N/A"))
            
            self.btn_copy.configure(state="normal")
        else:
            for var in self.detail_vars.values():
                var.set("")
            self.btn_copy.configure(state="disabled")
