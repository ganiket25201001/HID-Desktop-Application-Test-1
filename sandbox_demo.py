"""
Example: Hardware Port Sandbox for USB, Type-C, HDMI
Monitors physical hardware ports instead of network ports.
"""
from src.hardware_port_sandbox import HardwarePortSandbox
import time

def custom_validation(data: bytes, port_id: str) -> bool:
    """
    Custom validation logic for hardware port transfers.
    Return True to allow, False to block.
    """
    # Block large transfers
    if len(data) > 5 * 1024 * 1024:  # 5MB
        print(f"⚠️ BLOCKED: Transfer too large ({len(data)} bytes) on port {port_id[:30]}...")
        return False
    
    print(f"✅ ALLOWED: Transfer ({len(data)} bytes) on port {port_id[:30]}...")
    return True

def main():
    print("🔒 Hardware Port Sandbox Demo")
    print("=" * 50)
    
    # Initialize hardware sandbox
    sandbox = HardwarePortSandbox(custom_validation)
    
    print("\n🚀 Starting hardware port monitoring...")
    sandbox.start()
    
    print("\n✅ Monitoring active for:")
    print("   🔌 USB Ports")
    print("   ⚡ Type-C Ports")
    print("   🖥️ HDMI/Video Ports")
    print("\nAll data transfers will be validated.")
    print("\nPress Ctrl+C to stop...\n")
    
    try:
        for i in range(60):
            time.sleep(1)
            
            if (i + 1) % 10 == 0:
                ports = sandbox.get_monitored_ports()
                logs = sandbox.get_logs()
                
                print(f"\n📊 Statistics after {i + 1} seconds:")
                print(f"   Monitored Ports: {len(ports)}")
                print(f"   Total Transfers: {len(logs)}")
                
                usb_count = sum(1 for p in ports.values() if "USB" in p["type"])
                typec_count = sum(1 for p in ports.values() if "Controller" in p["type"])
                hdmi_count = sum(1 for p in ports.values() if "Video" in p["type"])
                
                print(f"   🔌 USB: {usb_count} | ⚡ Type-C: {typec_count} | 🖥️ HDMI: {hdmi_count}")
    
    except KeyboardInterrupt:
        print("\n\n⏹️ Stopping sandbox...")
    
    finally:
        sandbox.stop()
        print("✅ Sandbox stopped successfully")
        
        print("\n📋 Final Report:")
        ports = sandbox.get_monitored_ports()
        print(f"   Total Ports Monitored: {len(ports)}")
        for port_id, info in list(ports.items())[:5]:
            print(f"   {info['type']}: {info['name']}")

if __name__ == "__main__":
    main()
