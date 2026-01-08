"""
Main Entry Point for Device Monitor Pro
Initializes and runs the application with modern CustomTkinter UI.
"""
import sys
import logging
from src.gui import DashboardApp

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    """Main application entry point."""
    try:
        app = DashboardApp()
        
        # Center window on screen
        app.update_idletasks()
        window_width = 1200
        window_height = 800
        screen_width = app.winfo_screenwidth()
        screen_height = app.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        app.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        # Set minimum window size
        app.minsize(1000, 600)
        
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
