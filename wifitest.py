import os
import time
import speedtest
import platform
from scapy.all import ARP, Ether, srp

def check_wifi_speed():
    print("Checking WiFi speed...")
    st = speedtest.Speedtest()
    st.get_best_server()
    download_speed = st.download() / 1_000_000  
    upload_speed = st.upload() / 1_000_000  
    ping = st.results.ping
    print(f"Download Speed: {download_speed:.2f} Mbps")
    print(f"Upload Speed: {upload_speed:.2f} Mbps")
    print(f"Ping: {ping:.2f} ms")

def list_connected_devices():
    print("\nScanning connected devices...")
    devices = []
    if platform.system() == "Windows":
        result = os.popen("arp -a").read()
        devices = result.split("\n")
    else:  # Linux/Mac
        ip_range = "192.168.1.1/24"  # this should be adjusted according to your network
        arp_request = ARP(pdst=ip_range)
        ether = Ether(dst="ff:ff:ff:ff:ff:ff")
        packet = ether / arp_request
        result = srp(packet, timeout=3, verbose=False)[0]
        
        for sent, received in result:
            devices.append(f"IP: {received.psrc}, MAC: {received.hwsrc}")

    for device in devices:
        print(device)

def prevent_router_restart(router_ip="192.168.1.1"):
    print("\nMonitoring router uptime...")
    while True:
        response = os.system(f"ping -c 1 {router_ip} > /dev/null 2>&1")
        if response != 0:
            print("Router might be restarting! Attempting to reconnect...")
        time.sleep(10)  # checks whether router is down or not

if __name__ == "__main__":
    check_wifi_speed()
    list_connected_devices()
    try:
        prevent_router_restart()
    except KeyboardInterrupt:
        print("\nMonitoring stopped.")
