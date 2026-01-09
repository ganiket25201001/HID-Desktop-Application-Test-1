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

### Option 1: Install from Installer (Recommended)

#### 1. Run the Installer
- Download `DeviceMonitorPro_Setup_v1.0.0.exe`
- Double-click to launch the installation wizard
- Follow the on-screen instructions
- Choose installation location and shortcuts

#### 2. Launch the App
- **Press Win+S** and search "Device Monitor Pro" or "DMP"
- **Start Menu** → Device Monitor Pro
- **Desktop** → Double-click the icon (if created during installation)

#### 3. Uninstall
- **Settings** → **Apps** → **Installed apps** → Search "Device Monitor Pro" → **Uninstall**
- **Control Panel** → **Programs and Features** → "Device Monitor Pro" → **Uninstall**
- **Start Menu** → Right-click "Device Monitor Pro" → **Uninstall**

### Option 2: Run from Source (For Developers)

#### 1. Clone the Repository
```bash
git clone https://github.com/ganiket25201001/HID-Desktop-Application-Test-1.git
cd HID-Desktop-Application-Test-1
```

#### 2. Create Virtual Environment (Recommended)
```bash
python -m venv .venv
.venv\Scripts\activate
```

#### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

#### 4. Run the Application
```bash
python run_dashboard.py
```

### Option 3: Build from Source

#### 1. Build Everything (Automated)
```bash
build.bat
```

The script will:
- ✅ Install required build tools (PyInstaller, WinShell, etc.)
- ✅ Build the standalone `.exe` file → `dist\DeviceMonitorPro.exe`
- ✅ Ask if you want to create shortcuts (Desktop & Start Menu)
- ✅ Ask if you want to build a professional Windows installer
- ✅ Auto-download and install Inno Setup if needed
- ✅ Create installer → `installer\DeviceMonitorPro_Setup_v1.0.0.exe`

**Outputs:**
- `dist\DeviceMonitorPro.exe` - Portable standalone executable (~40-50 MB)
- `installer\DeviceMonitorPro_Setup_v1.0.0.exe` - Professional Windows installer with uninstaller

#### 2. Launch the Built App
- **Double-click** `dist\DeviceMonitorPro.exe` (portable, no installation)
- **Or install** using `installer\DeviceMonitorPro_Setup_v1.0.0.exe` (proper Windows app)

### Distribution Options

**Option A: Portable Standalone EXE**
- 📦 Share `dist\DeviceMonitorPro.exe`
- ✅ Users run it directly, no installation needed
- ✅ No registry entries, completely portable
- ✅ ~40-50 MB file size
- ❌ No automatic uninstaller
- ❌ Not shown in Control Panel / Settings Apps
- ❌ Manual cleanup required (just delete the .exe)

**Option B: Professional Windows Installer** (✨ Recommended)
- 📦 Share `installer\DeviceMonitorPro_Setup_v1.0.0.exe`
- ✅ Professional installation wizard with license agreement
- ✅ Choose installation location
- ✅ Automatic Start Menu & Desktop shortcuts
- ✅ Integrated Windows Search (Win+S)
- ✅ Proper uninstaller in Settings → Apps → Installed apps
- ✅ Shows in Control Panel → Programs and Features
- ✅ Right-click Start Menu shortcut → Uninstall
- ✅ Registry integration for app paths
- 📝 Requires [Inno Setup](https://jrsoftware.org/isdl.php) to build (auto-installed by build.bat)

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
├── build.bat                # Build executable & installer
├── create_shortcuts.py      # Create desktop & Start Menu shortcuts
├── installer_script.iss     # Inno Setup installer configuration
├── app_icon.ico             # Application icon
├── requirements.txt         # Python dependencies
└── README.md
```

## 🎨 Technology Stack

- **UI Framework**: [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) - Modern dark-themed widgets
- **Device Detection**: Windows Management Instrumentation (WMI)
- **Threading**: Python threading for non-blocking operations
- **Logging**: Built-in Python logging module
- **Data Storage**: JSON for user profiles
- **Build Tool**: PyInstaller for standalone executables
- **Installer**: Inno Setup for professional Windows installer

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
| **Can't Uninstall** | Use the Windows installer (not portable .exe) for proper uninstall |
| **Not in Control Panel** | Reinstall using the installer (`DeviceMonitorPro_Setup_v1.0.0.exe`) |
| **Build Failed (Access Denied)** | Close running app, delete `dist` and `build` folders, rebuild |
| **Installer Build Fails** | Run `build.bat` - it will auto-download and install Inno Setup |

## 🔧 Building & Distribution

### ⚡ Automated Build Process (One Command!)
```bash
build.bat
```

This single command does **everything** automatically:
1. ✅ Checks and installs Python dependencies (PyInstaller, WinShell, pywin32)
2. ✅ Builds standalone executable → `dist\DeviceMonitorPro.exe`
3. ✅ Prompts to create Desktop & Start Menu shortcuts
4. ✅ Prompts to build professional Windows installer
5. ✅ Auto-downloads and silently installs Inno Setup if not found
6. ✅ Compiles installer → `installer\DeviceMonitorPro_Setup_v1.0.0.exe`
7. ✅ Runs installer to install the app properly

**Result:** Fully installed app registered with Windows, ready to uninstall from Settings!

### 🛠️ Manual Build (Advanced)

#### Build Executable Only
```bash
.venv\Scripts\python.exe -m PyInstaller --name="DeviceMonitorPro" --onefile --windowed --icon=app_icon.ico run_dashboard.py
```

#### Create Shortcuts Manually
```bash
python create_shortcuts.py
```

#### Build Installer Manually
```bash
# Requires Inno Setup installed
"C:\Program Files (x86)\Inno Setup 6\ISCC.exe" installer_script.iss
```

### 📋 Build Requirements
- **Python 3.8+** with pip
- **PyInstaller** (auto-installed by build.bat)
- **Inno Setup 6** (auto-downloaded and installed by build.bat)
- **Windows 10/11** (for WMI and Inno Setup)

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
wmi            # Windows Management Instrumentation
pywin32        # Windows extensions
customtkinter  # Modern UI framework
pyinstaller    # EXE builder
winshell       # Shortcut creation
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
