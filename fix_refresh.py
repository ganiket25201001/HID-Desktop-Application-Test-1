with open('d:/Delete/aniket-project/src/gui.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the method
old = '''        if not ports:
            ctk.CTkLabel(self.hw_sandbox_ports_scroll, text="No ports detected yet", font=ctk.CTkFont(size=14), text_color="gray").pack(pady=50)
            return'''

new = '''        if not ports:
            ctk.CTkLabel(self.hw_sandbox_ports_scroll, text="Scanning for ports...", font=ctk.CTkFont(size=14), text_color="gray").pack(pady=50)
            self.after(2000, self._refresh_hw_sandbox_view)
            return'''

content = content.replace(old, new)

with open('d:/Delete/aniket-project/src/gui.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Fixed")
