import re

# Read the file
with open('d:/Delete/aniket-project/src/gui.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Find and replace the sandbox methods section
old_methods = r'    def _start_sandbox\(self\):.*?(?=\n    def _create_port_item)'

new_methods = '''    def _start_sandbox(self):
        try:
            self.hardware_sandbox = HardwarePortSandbox(self._validate_hardware_transfer)
            self.hardware_sandbox.start()
            self.sandbox_status_label.configure(text="🟢 Active", text_color=Theme.SUCCESS)
            self.btn_start_sandbox.configure(state="disabled")
            self.btn_stop_sandbox.configure(state="normal")
            self.activity_log.log_activity(ActivityType.SYSTEM_STARTUP, "Hardware monitoring started", "System")
            messagebox.showinfo("Success", "✅ Monitoring started")
            self.after(1000, self._refresh_sandbox_view)
        except Exception as e:
            messagebox.showerror("Error", f"Failed: {e}")
    
    def _stop_sandbox(self):
        try:
            if self.hardware_sandbox:
                self.hardware_sandbox.stop()
            self.sandbox_status_label.configure(text="⚫ Inactive", text_color="gray")
            self.btn_start_sandbox.configure(state="normal")
            self.btn_stop_sandbox.configure(state="disabled")
            self.activity_log.log_activity(ActivityType.SYSTEM_SHUTDOWN, "Monitoring stopped", "System")
            messagebox.showinfo("Success", "✅ Stopped")
        except Exception as e:
            messagebox.showerror("Error", f"Failed: {e}")
    
    def _validate_hardware_transfer(self, data: bytes, port_id: str) -> bool:
        if len(data) > 10 * 1024 * 1024:
            return False
        return True
    
    def _refresh_sandbox_view(self):
        for widget in self.sandbox_ports_scroll.winfo_children():
            widget.destroy()
        if not self.hardware_sandbox:
            ctk.CTkLabel(self.sandbox_ports_scroll, text="Start monitoring to see ports", font=ctk.CTkFont(size=14), text_color="gray").pack(pady=50)
            return
        ports = self.hardware_sandbox.get_monitored_ports()
        if not ports:
            ctk.CTkLabel(self.sandbox_ports_scroll, text="No ports detected yet", font=ctk.CTkFont(size=14), text_color="gray").pack(pady=50)
            return
        usb_count = sum(1 for p in ports.values() if "USB" in p["type"])
        typec_count = sum(1 for p in ports.values() if "Controller" in p["type"])
        hdmi_count = sum(1 for p in ports.values() if "Video" in p["type"])
        self.sandbox_stats["usb"].set(str(usb_count))
        self.sandbox_stats["typec"].set(str(typec_count))
        self.sandbox_stats["hdmi"].set(str(hdmi_count))
        self.sandbox_stats["transfers"].set(str(len(self.hardware_sandbox.get_logs())))
        for port_id, info in ports.items():
            self._create_port_item(port_id, info)

'''

content = re.sub(old_methods, new_methods, content, flags=re.DOTALL)

# Write back
with open('d:/Delete/aniket-project/src/gui.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Replaced sandbox methods with hardware port versions")
