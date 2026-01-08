# Device Monitor Pro 🖥️

A modern, professional Python desktop application with a sleek dark-themed UI for comprehensive real-time monitoring of connected hardware devices on Windows systems.

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Platform](https://img.shields.io/badge/platform-Windows-blue.svg)
![UI](https://img.shields.io/badge/UI-CustomTkinter-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## ✨ Features

### **🎨 Modern UI/UX**
- 🌙 **Dark Theme** - Professional dark mode powered by CustomTkinter
- 📊 **Real-time Statistics Dashboard** - Visual cards showing device counts
- 🔍 **Smart Search** - Filter devices instantly with search (Ctrl+F)
- 🔄 **Manual Refresh** - On-demand updates with F5 key
- ⌨️ **Keyboard Shortcuts** - Efficient navigation and control
- 💫 **Smooth Animations** - Modern hover effects and transitions
- 📋 **One-Click Copy** - Copy device information to clipboard

### **🔌 Device Management**
- **Real-time Monitoring** - Auto-refresh every 5 seconds
- **Categorized View** - USB, HID, Network, Storage, Bluetooth
- **Detailed Information** - VID, PID, Manufacturer, Driver, Status, Paths
- **Status Indicators** - 🟢 Connected/OK | 🟡 Unknown | 🔴 Disconnected
- **Smart Filtering** - Search by name, manufacturer, or category

### **👤 User Profiles**
- Manage user identity (Name, Role, Email, Department)
- Persistent storage with JSON
- Input validation and error handling

### **🛡️ Technical Excellence**
- Type hints throughout codebase
- Comprehensive error handling with logging
- Background threading for non-blocking UI
- Modular architecture with clean separation
- WMI integration (no admin rights required for most devices)

## 🎮 Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `F5` | Refresh devices |
| `Ctrl+F` | Focus search box |
| `Esc` | Clear search |

## 📋 Requirements

- **Windows 10/11** (WMI dependency)
- **Python 3.8+**

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/ganiket25201001/HID-Desktop-Application-Test-1.git
cd HID-Desktop-Application-Test-1
```

### 2. Create Virtual Environment (Recommended)
```bash
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Application
```bash
python run_dashboard.py
```

## 📁 Project Structure

```
HID-Desktop-Application-Test-1/
├── src/
│   ├── __init__.py
│   ├── main.py              # Application entry point
│   ├── gui.py               # Modern CustomTkinter UI
│   ├── device_manager.py    # WMI device detection
│   └── user_profile.py      # User profile management
├── run_dashboard.py         # Launcher script
├── requirements.txt         # Python dependencies
├── user_profile.json        # User data (auto-created)
└── README.md
```

## 🎨 Technology Stack

- **UI Framework**: [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) - Modern dark-themed widgets
- **Device Detection**: Windows Management Instrumentation (WMI)
- **Threading**: Python threading for non-blocking operations
- **Logging**: Built-in Python logging module
- **Data Storage**: JSON for user profiles

## 💡 Key Components

### Statistics Dashboard
Four real-time cards displaying:
- Total device count
- USB device count
- HID device count (keyboards, mice)
- Network adapter count

### Device Tree View
- Hierarchical display by category
- Expandable/collapsible groups
- Color-coded status indicators
- Preserves state during refresh

### Device Details Panel
- All device information displayed clearly
- Read-only fields for viewing
- One-click copy to clipboard
- Scrollable for long paths

### User Profile Page
- Editable user information
- Circular avatar with initial
- Modern form inputs
- Profile persistence

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| **Admin Required** | Some devices need admin privileges - run as Administrator |
| **Missing Devices** | Check Windows Device Manager for driver issues |
| **WMI Errors** | Ensure WMI service is running in Windows Services |
| **Import Errors** | Activate virtual environment and reinstall dependencies |

## 📝 Development

### Code Quality
- Type hints for better IDE support
- Comprehensive docstrings
- Error handling with try-catch blocks
- Logging for debugging

### Running in Development
```bash
# Activate virtual environment
.venv\Scripts\activate

# Run with logging
python run_dashboard.py
```

### Dependencies
```
wmi          # Windows Management Instrumentation
pywin32      # Windows extensions
psutil       # System utilities
customtkinter # Modern UI framework
```

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Add type hints and documentation
4. Test thoroughly on Windows
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **CustomTkinter** by Tom Schimansky for the amazing modern UI framework
- **WMI** for Windows device management capabilities
- Unicode Emoji for device icons

---

**Device Monitor Pro** - Professional hardware monitoring made beautiful and simple.

*Built with ❤️ using Python and CustomTkinter*
