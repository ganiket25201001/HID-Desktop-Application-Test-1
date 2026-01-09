"""
Create Desktop Shortcut for Device Monitor Pro
"""
import os
import winshell
from win32com.client import Dispatch

def create_desktop_shortcut():
    """Create a desktop shortcut for the exe."""
    desktop = winshell.desktop()
    
    # Path to the exe (update this after building)
    exe_path = os.path.join(os.getcwd(), "dist", "DeviceMonitorPro.exe")
    
    if not os.path.exists(exe_path):
        print(f"Error: {exe_path} not found. Build the exe first!")
        return False
    
    # Create shortcut
    shortcut_path = os.path.join(desktop, "Device Monitor Pro.lnk")
    
    shell = Dispatch('WScript.Shell')
    shortcut = shell.CreateShortCut(shortcut_path)
    shortcut.TargetPath = exe_path
    shortcut.WorkingDirectory = os.path.dirname(exe_path)
    shortcut.IconLocation = exe_path + ",0"
    shortcut.Description = "Device Monitor Pro - Hardware Monitoring Tool"
    shortcut.save()
    
    print(f"✅ Desktop shortcut created: {shortcut_path}")
    return True

def create_start_menu_shortcut():
    """Create Start Menu shortcuts for searchability."""
    start_menu = winshell.start_menu()
    programs_folder = os.path.join(start_menu, "Programs", "Device Monitor Pro")
    
    # Create program folder
    os.makedirs(programs_folder, exist_ok=True)
    
    exe_path = os.path.join(os.getcwd(), "dist", "DeviceMonitorPro.exe")
    
    if not os.path.exists(exe_path):
        print(f"Error: {exe_path} not found. Build the exe first!")
        return False
    
    shell = Dispatch('WScript.Shell')
    
    # Main shortcut
    main_shortcut = shell.CreateShortCut(os.path.join(programs_folder, "Device Monitor Pro.lnk"))
    main_shortcut.TargetPath = exe_path
    main_shortcut.WorkingDirectory = os.path.dirname(exe_path)
    main_shortcut.IconLocation = exe_path + ",0"
    main_shortcut.Description = "Device Monitor Pro - Hardware Monitoring"
    main_shortcut.save()
    
    # Short name shortcut for search
    short_shortcut = shell.CreateShortCut(os.path.join(programs_folder, "DMP.lnk"))
    short_shortcut.TargetPath = exe_path
    short_shortcut.WorkingDirectory = os.path.dirname(exe_path)
    short_shortcut.IconLocation = exe_path + ",0"
    short_shortcut.Description = "DMP - Device Monitor Pro"
    short_shortcut.save()
    
    print(f"✅ Start Menu shortcuts created in: {programs_folder}")
    print("   - Device Monitor Pro.lnk")
    print("   - DMP.lnk")
    return True

if __name__ == "__main__":
    print("Creating shortcuts for Device Monitor Pro...")
    print("=" * 50)
    
    if create_desktop_shortcut():
        print("\n✅ Desktop shortcut created successfully!")
    
    if create_start_menu_shortcut():
        print("\n✅ Start Menu shortcuts created successfully!")
        print("\nYou can now search for:")
        print("  - 'Device Monitor Pro'")
        print("  - 'DMP'")
        print("  using Win+S")
    
    print("\n" + "=" * 50)
    print("Setup complete!")
    input("\nPress Enter to exit...")
