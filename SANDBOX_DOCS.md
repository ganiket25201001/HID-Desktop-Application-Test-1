# Sandbox Security Feature 🔒

## Overview

The Sandbox Security layer creates a secured channel between your software and machine ports, forcing all file/data transfers to be routed through validation logic rather than allowing native machine access.

## Key Features

### 🛡️ Secured Channels
- Creates isolated communication channels on configurable ports
- All data transfers must pass through the sandbox
- Multiple channels can run simultaneously

### 🔍 Transfer Interception
- Intercepts all file and data transfers
- USB port operations are monitored and controlled
- No data bypasses the sandbox when active

### ✅ Real-time Validation
- Custom validation rules for each transfer
- Block transfers based on size, content, or source
- SHA-256 hashing for integrity verification

### 📊 Complete Audit Trail
- Every transfer is logged with timestamp
- Source and destination tracking
- Data size and hash recorded
- Allow/block status for each transfer

## Architecture

```
┌─────────────────┐
│   USB Device    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ USB Interceptor │ ◄── Monitors USB operations
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Sandbox Channel │ ◄── Validates transfers
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Validation     │ ◄── Custom rules
│  Callback       │
└────────┬────────┘
         │
         ▼
    Allow/Block
```

## Usage

### In the GUI

1. Navigate to **🔒 Sandbox** view
2. Enter a port number (1024-65535)
3. Click **🚀 Start Sandbox**
4. Monitor transfers in real-time
5. View statistics (channels, transfers, blocked/allowed)

### Programmatically

```python
from src.sandbox import SandboxManager
from src.usb_interceptor import USBInterceptor

# Initialize
manager = SandboxManager()

# Define validation
def validate(data: bytes, addr: tuple) -> bool:
    if len(data) > 10 * 1024 * 1024:  # Block > 10MB
        return False
    return True

# Create channel
channel = manager.create_channel(8080, validate)
channel.start()

# Start USB interception
interceptor = USBInterceptor(channel)
interceptor.start_monitoring()

# Get logs
logs = manager.get_all_logs()
```

## Security Benefits

✅ **Prevents unauthorized data exfiltration**
✅ **Blocks malicious file transfers**
✅ **Complete visibility into all transfers**
✅ **Configurable security policies**
✅ **Real-time threat detection**

## Configuration

### Port Selection
- Use ports 1024-65535 (non-privileged)
- Avoid common ports (8080, 3000, etc.) if other services use them

### Validation Rules
Customize validation in `_validate_transfer()`:
- File size limits
- Content scanning
- Source IP restrictions
- File type filtering

## Demo Script

Run the included demo:
```bash
python sandbox_demo.py
```

This demonstrates:
- Channel creation
- USB interception
- Transfer logging
- Statistics reporting

## Integration with Device Monitor Pro

The sandbox integrates seamlessly:
- Activity Log tracks sandbox events
- Dashboard shows active channels
- User Profile stores sandbox preferences
- All transfers logged to system activity

## Technical Details

### Components

**sandbox.py**
- `SandboxChannel` - Individual secured channel
- `SandboxManager` - Manages multiple channels
- `TransferLog` - Data structure for transfer records

**usb_interceptor.py**
- `USBInterceptor` - Monitors USB operations
- Hooks into drive I/O
- Routes transfers through sandbox

### Data Flow

1. USB device connects
2. Interceptor detects operation
3. Data routed to sandbox channel
4. Validation callback executed
5. Transfer allowed or blocked
6. Event logged with details

## Best Practices

1. **Always validate transfers** - Don't allow all by default
2. **Monitor logs regularly** - Check for suspicious activity
3. **Use appropriate ports** - Avoid conflicts
4. **Set size limits** - Prevent resource exhaustion
5. **Keep audit trail** - Export logs periodically

## Future Enhancements

- [ ] Machine learning-based threat detection
- [ ] Network transfer interception
- [ ] Encrypted channel support
- [ ] Remote monitoring capabilities
- [ ] Advanced content scanning
