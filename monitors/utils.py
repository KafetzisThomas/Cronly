import socket
import time

def track_dns_time(target):
    try:
        start_time = time.perf_counter()
        ip_address = socket.gethostbyname(target)
        end_time = time.perf_counter()

        dns_lookup_ms = (end_time - start_time) * 1000

        return {"ip": ip_address, "dns_time_ms": round(dns_lookup_ms, 2), "success": True}

    except socket.gaierror:
        # domain not exist or dns fails
        return {"error": "DNS Resolution Failed", "dns_time_ms": 0.0, "success": False}
