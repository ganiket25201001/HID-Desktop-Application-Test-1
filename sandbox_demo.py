"""
Example: Using Sandbox for Secure File Transfers
This demonstrates how all file/data transfers are routed through the sandbox.
"""
from src.sandbox import SandboxManager, SandboxChannel
from src.usb_interceptor import USBInterceptor
import time

def custom_validation(data: bytes, addr: tuple) -> bool:
    """
    Custom validation logic for transfers.
    Return True to allow, False to block.
    """
    # Example: Block transfers containing specific patterns
    if b"malware" in data.lower():
        print(f"⚠️ BLOCKED: Suspicious content from {addr}")
        return False
    
    # Example: Block large transfers
    if len(data) > 5 * 1024 * 1024:  # 5MB
        print(f"⚠️ BLOCKED: Transfer too large ({len(data)} bytes) from {addr}")
        return False
    
    print(f"✅ ALLOWED: Transfer ({len(data)} bytes) from {addr}")
    return True

def main():
    print("🔒 Sandbox Security Demo")
    print("=" * 50)
    
    # Initialize sandbox manager
    manager = SandboxManager()
    manager.set_global_validation(custom_validation)
    
    # Create secured channels for different ports
    print("\n📡 Creating secured channels...")
    channel_8080 = manager.create_channel(8080)
    channel_8081 = manager.create_channel(8081)
    
    # Start all channels
    print("🚀 Starting sandbox channels...")
    manager.start_all()
    
    # Start USB interceptor
    print("🔌 Starting USB interceptor...")
    usb_interceptor = USBInterceptor(channel_8080)
    usb_interceptor.start_monitoring()
    
    print("\n✅ Sandbox is now active!")
    print("All file transfers will be routed through the sandbox.")
    print("\nPress Ctrl+C to stop...\n")
    
    try:
        # Monitor for 60 seconds
        for i in range(60):
            time.sleep(1)
            
            # Display statistics every 10 seconds
            if (i + 1) % 10 == 0:
                print(f"\n📊 Statistics after {i + 1} seconds:")
                all_logs = manager.get_all_logs()
                for port, logs in all_logs.items():
                    total = len(logs)
                    allowed = sum(1 for log in logs if log.allowed)
                    blocked = total - allowed
                    print(f"  Port {port}: {total} transfers ({allowed} allowed, {blocked} blocked)")
    
    except KeyboardInterrupt:
        print("\n\n⏹️ Stopping sandbox...")
    
    finally:
        # Cleanup
        usb_interceptor.stop()
        manager.stop_all()
        print("✅ Sandbox stopped successfully")
        
        # Final report
        print("\n📋 Final Transfer Report:")
        all_logs = manager.get_all_logs()
        for port, logs in all_logs.items():
            print(f"\n  Port {port}:")
            for log in logs[-5:]:  # Show last 5
                status = "✅ ALLOWED" if log.allowed else "🚫 BLOCKED"
                print(f"    {status} | {log.source} | {log.size} bytes | {log.timestamp}")

if __name__ == "__main__":
    main()
