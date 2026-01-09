"""
Modern GUI Module for Device Monitor Pro using CustomTkinter
Provides a sleek dark-themed interface with enhanced visuals.
"""
import customtkinter as ctk
from tkinter import ttk, messagebox
import threading
from typing import Dict, Optional
import datetime
from src.device_manager import DeviceManager
from src.user_profile import UserProfile

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
        self.sidebar = ctk.CTkFrame(self, width=220, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_rowconfigure(10, weight=1)
        
        # Logo
        self.logo_label = ctk.CTkLabel(
            self.sidebar,
            text="DEVICE\nMONITOR PRO",
            font=ctk.CTkFont(size=22, weight="bold")
        )
        self.logo_label.grid(row=0, column=0, padx=20, pady=(30, 40))

        # Navigation Buttons
        self.dash_btn = ctk.CTkButton(
            self.sidebar,
            text="📊 Dashboard",
            command=self.show_dashboard,
            anchor="w",
            height=40,
            font=ctk.CTkFont(size=14)
        )
        self.dash_btn.grid(row=1, column=0, padx=20, pady=5, sticky="ew")
        
        self.profile_btn = ctk.CTkButton(
            self.sidebar,
            text="👤 User Profile",
            command=self.show_profile,
            fg_color="transparent",
            anchor="w",
            height=40,
            font=ctk.CTkFont(size=14)
        )
        self.profile_btn.grid(row=2, column=0, padx=20, pady=5, sticky="ew")

        # User Info at Bottom
        self.user_label = ctk.CTkLabel(
            self.sidebar,
            text=f"User: {self.user_profile.name}",
            font=ctk.CTkFont(size=11),
            text_color="gray"
        )
        self.user_label.grid(row=11, column=0, pady=(0, 20))

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
        
        # Update button states
        self.dash_btn.configure(fg_color=["#3B8ED0", "#1F6AA5"])
        self.profile_btn.configure(fg_color="transparent")
        
        # 1. Statistics Cards Row
        self.stats_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.stats_frame.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        
        self.stats_cards = {
            "total": self._create_stat_card(self.stats_frame, "Total Devices", "0", "📊", 0),
            "usb": self._create_stat_card(self.stats_frame, "USB", "0", "🔌", 1),
            "hid": self._create_stat_card(self.stats_frame, "HID", "0", "🖱️", 2),
            "network": self._create_stat_card(self.stats_frame, "Network", "0", "🌐", 3),
        }

        # 2. Action Bar (Search + Refresh)
        self.action_bar = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.action_bar.grid(row=1, column=0, sticky="ew", pady=(0, 15))
        
        self.search_entry = ctk.CTkEntry(
            self.action_bar,
            placeholder_text="🔍 Search devices...",
            width=350,
            height=35,
            font=ctk.CTkFont(size=13)
        )
        self.search_entry.pack(side="left")
        self.search_entry.bind("<KeyRelease>", lambda e: self._on_search_changed())
        
        self.refresh_btn = ctk.CTkButton(
            self.action_bar,
            text="🔄 Refresh",
            command=self._manual_refresh,
            width=120,
            height=35,
            font=ctk.CTkFont(size=13, weight="bold")
        )
        self.refresh_btn.pack(side="right", padx=(10, 0))
        
        self.lbl_status = ctk.CTkLabel(
            self.action_bar,
            text="Ready",
            font=ctk.CTkFont(size=12),
            text_color="gray"
        )
        self.lbl_status.pack(side="right", padx=15)

        # 3. Content Body (Tree + Details)
        self.body_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.body_frame.grid(row=2, column=0, sticky="nsew")
        self.main_container.grid_rowconfigure(2, weight=1)
        self.body_frame.grid_columnconfigure(0, weight=2)
        self.body_frame.grid_columnconfigure(1, weight=1)

        # Tree View Panel
        self.tree_frame = ctk.CTkFrame(self.body_frame)
        self.tree_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        
        # Configure ttk.Treeview style for dark theme
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Treeview",
                       background="#2B2B2B",
                       foreground="white",
                       fieldbackground="#2B2B2B",
                       borderwidth=0,
                       rowheight=30,
                       font=('Segoe UI', 10))
        style.map('Treeview', background=[('selected', '#1F6AA5')])
        style.configure("Treeview.Heading",
                       background="#1F1F1F",
                       foreground="white",
                       borderwidth=0,
                       font=('Segoe UI', 10, 'bold'))
        
        self.tree = ttk.Treeview(self.tree_frame, show="tree", selectmode="browse")
        self.tree.pack(expand=True, fill="both", padx=5, pady=5)
        self.tree.bind("<<TreeviewSelect>>", self._on_device_select)

        # Details Panel
        self.details_frame = ctk.CTkScrollableFrame(self.body_frame, fg_color=("#DBDBDB", "#2B2B2B"))
        self.details_frame.grid(row=0, column=1, sticky="nsew")
        
        # Details Header
        self.details_header = ctk.CTkFrame(self.details_frame, fg_color="transparent")
        self.details_header.pack(fill="x", padx=15, pady=(15, 10))
        
        ctk.CTkLabel(
            self.details_header,
            text="Device Details",
            font=ctk.CTkFont(size=18, weight="bold")
        ).pack(side="left")
        
        self.btn_copy = ctk.CTkButton(
            self.details_header,
            text="📋 Copy",
            command=self._copy_device_info,
            width=90,
            height=30,
            state="disabled",
            font=ctk.CTkFont(size=12)
        )
        self.btn_copy.pack(side="right")
        
        # Details Fields
        self.detail_vars = {
            "Name": ctk.StringVar(),
            "Category": ctk.StringVar(),
            "Type": ctk.StringVar(),
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

    def _create_stat_card(self, parent, title, value, icon, col):
        """Create a statistics card widget."""
        card = ctk.CTkFrame(parent, height=100)
        card.grid(row=0, column=col, padx=5, sticky="nsew")
        parent.grid_columnconfigure(col, weight=1)
        
        # Icon label
        ctk.CTkLabel(
            card,
            text=icon,
            font=ctk.CTkFont(size=24)
        ).pack(pady=(15, 5))
        
        # Value label
        value_var = ctk.StringVar(value=value)
        ctk.CTkLabel(
            card,
            textvariable=value_var,
            font=ctk.CTkFont(size=26, weight="bold")
        ).pack(pady=5)
        
        # Title label
        ctk.CTkLabel(
            card,
            text=title,
            font=ctk.CTkFont(size=11),
            text_color="gray"
        ).pack(pady=(5, 15))
        
        return value_var

    def _create_detail_field(self, parent, label, variable):
        """Create a detail field row."""
        row = ctk.CTkFrame(parent, fg_color="transparent")
        row.pack(fill="x", padx=15, pady=5)
        
        ctk.CTkLabel(
            row,
            text=label.upper(),
            font=ctk.CTkFont(size=9, weight="bold"),
            text_color="gray",
            anchor="w"
        ).pack(anchor="w")
        
        entry = ctk.CTkEntry(
            row,
            textvariable=variable,
            state="readonly",
            font=ctk.CTkFont(size=12),
            height=30
        )
        entry.pack(fill="x", pady=(2, 0))

    def show_profile(self):
        """Display the user profile management view."""
        if self.current_view == "profile":
            return
            
        self._clear_content()
        self.current_view = "profile"
        
        # Update button states
        self.dash_btn.configure(fg_color="transparent")
        self.profile_btn.configure(fg_color=["#3B8ED0", "#1F6AA5"])
        
        # Header
        ctk.CTkLabel(
            self.main_container,
            text="User Profile",
            font=ctk.CTkFont(size=24, weight="bold")
        ).pack(anchor="w", pady=(0, 30))
        
        # Profile Card
        card = ctk.CTkFrame(self.main_container)
        card.pack(fill="both", expand=True, padx=50, pady=(0, 50))
        
        # Profile Icon
        icon_label = ctk.CTkLabel(
            card,
            text=self.user_profile.name[0].upper() if self.user_profile.name else "U",
            font=ctk.CTkFont(size=48, weight="bold"),
            width=100,
            height=100,
            fg_color=["#3B8ED0", "#1F6AA5"],
            corner_radius=50
        )
        icon_label.pack(pady=(40, 30))
        
        # Form Container
        form_container = ctk.CTkFrame(card, fg_color="transparent")
        form_container.pack(fill="both", expand=True, padx=80)
        
        # Variables
        self.var_name = ctk.StringVar(value=self.user_profile.name)
        self.var_role = ctk.StringVar(value=self.user_profile.role)
        self.var_email = ctk.StringVar(value=self.user_profile.email)
        self.var_dept = ctk.StringVar(value=self.user_profile.department)
        
        self._create_profile_entry(form_container, "Full Name", self.var_name)
        self._create_profile_entry(form_container, "Role", self.var_role)
        self._create_profile_entry(form_container, "Email Address", self.var_email)
        self._create_profile_entry(form_container, "Department", self.var_dept)
        
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
            self.user_profile.role = self.var_role.get()
            self.user_profile.email = self.var_email.get()
            self.user_profile.department = self.var_dept.get()
            self.user_profile.save()
            
            # Update Sidebar
            self.user_label.configure(text=f"User: {self.user_profile.name}")
            messagebox.showinfo("Success", "✅ Profile updated successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"❌ Failed to save profile: {e}")

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
        if hasattr(self, 'tree'):
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
        
        if not hasattr(self, 'tree'):
            return
        
        self.is_refreshing = True
        if hasattr(self, 'lbl_status'):
            self.lbl_status.configure(text="🔄 Scanning devices...", text_color="#3B8ED0")
        if hasattr(self, 'refresh_btn'):
            self.refresh_btn.configure(state="disabled")
            
        threading.Thread(target=self._fetch_devices_thread, daemon=True).start()

    def _fetch_devices_thread(self):
        """Fetch devices in background thread."""
        try:
            devices = self.dm.get_all_devices()
            self.last_update_time = datetime.datetime.now()
            self.after(0, lambda: self._update_tree(devices))
        except Exception as e:
            error_msg = f"Error scanning devices: {e}"
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
        """Update device tree with new data."""
        if self.current_view != "dashboard" or not hasattr(self, 'tree'):
            return

        # Capture state
        selected_path = None
        selection = self.tree.selection()
        if selection:
            iid = selection[0]
            if iid in self.current_devices:
                selected_path = self.current_devices[iid].get('path')
        
        expanded_categories = []
        for child in self.tree.get_children():
            if self.tree.item(child, 'open'):
                text = self.tree.item(child, "text")
                cat_name = text.split(" (")[0]
                expanded_categories.append(cat_name)

        # Filter
        search_query = ""
        if hasattr(self, 'search_entry'):
            search_query = self.search_entry.get().lower()
            if search_query:
                devices = [d for d in devices if search_query in d['name'].lower() 
                           or search_query in str(d.get('manufacturer', '')).lower()
                           or search_query in d['category'].lower()]

        # Update Statistics
        self._update_statistics(devices)

        # Clear and Repopulate Tree
        self.tree.delete(*self.tree.get_children())
        self.current_devices = {}
        
        if not devices:
            empty_id = self.tree.insert("", "end", text="No devices found")
            if hasattr(self, 'lbl_status'):
                self.lbl_status.configure(text="No devices found", text_color="#F39C12")
            return
        
        categories = {}
        for d in devices:
            cat = d['category']
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(d)
        
        # Insert by categories
        for cat in sorted(categories.keys()):
            dev_list = categories[cat]
            if not dev_list:
                continue

            is_open = bool(search_query) or cat in expanded_categories
            cat_id = self.tree.insert("", "end", text=f"{cat} ({len(dev_list)})", open=is_open)
            
            for d in dev_list:
                status_str = str(d['status']).lower()
                if "ok" in status_str or "connected" in status_str:
                    status_icon = "🟢"
                elif "disconnected" in status_str or "error" in status_str:
                    status_icon = "🔴"
                else:
                    status_icon = "🟡"
                    
                display_text = f"{status_icon}  {d['name']}"
                child_id = self.tree.insert(cat_id, "end", text=display_text)
                self.current_devices[child_id] = d
                
                if selected_path and d.get('path') == selected_path:
                    self.tree.selection_set(child_id)
                    self.tree.see(child_id)

        # Update status
        if hasattr(self, 'lbl_status') and self.last_update_time:
            time_str = self.last_update_time.strftime("%H:%M:%S")
            self.lbl_status.configure(text=f"✅ Updated at {time_str}", text_color="#27AE60")
    
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
        selection = self.tree.selection()
        if not selection:
            self.btn_copy.configure(state="disabled")
            return
        
        iid = selection[0]
        if iid in self.current_devices:
            d = self.current_devices[iid]
            self.detail_vars["Name"].set(d.get("name", "N/A"))
            self.detail_vars["Category"].set(d.get("category", "N/A"))
            self.detail_vars["Type"].set(d.get("type", "N/A"))
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
