"""
Main Entry Point for Device Monitor Pro
Initializes and runs the application with modern CustomTkinter UI.
"""
import sys
import logging
import win32event
import win32api
import win32gui
import win32con
import winerror
from src.gui import DashboardApp

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def bring_existing_window_to_front(window_title):
    """Find and bring the existing application window to the front."""
    try:
        hwnd = win32gui.FindWindow(None, window_title)
        if hwnd:
            if win32gui.IsIconic(hwnd):
                win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
            win32gui.SetForegroundWindow(hwnd)
            return True
    except Exception as e:
        logger.error(f"Failed to bring window to front: {e}")
    return False

def main():
    """Main application entry point."""
    # Create a named mutex to ensure single instance
    mutex_name = "Global\\DeviceMonitorPro_Instance_Mutex"
    mutex = win32event.CreateMutex(None, False, mutex_name)
    last_error = win32api.GetLastError()

    if last_error == winerror.ERROR_ALREADY_EXISTS:
        logger.info("Another instance is already running. Bringing it to focus.")
        bring_existing_window_to_front("Device Monitor Pro")
        return # Exit this instance

    try:
        app = DashboardApp()
        
        # Center window on screen
        app.update_idletasks()
        window_width = 1200
        window_height = 700
        screen_width = app.winfo_screenwidth()
        screen_height = app.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        app.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        # Set minimum window size
        app.minsize(950, 600)
        
        logger.info("Application started successfully")
        app.mainloop()
        
    except Exception as e:
        logger.critical(f"Fatal error: {e}", exc_info=True)
        import tkinter.messagebox as messagebox
        messagebox.showerror("Fatal Error", 
                           f"Application failed to start:\n{e}\n\nCheck logs for details.")
        sys.exit(1)


if __name__ == "__main__":
    main()
