import requests
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

def check_http_status(domain):
    url = f"https://{domain}"
    try:
        response = requests.get(url, timeout=10)
        return {
            "success": response.status_code >= 200 and response.status_code < 400,
            "status_code": response.status_code,
            "response_time_ms": round(response.elapsed.total_seconds() * 1000, 2)
        }

    except requests.exceptions.Timeout:
        return {"success": False, "status_code": 408, "error": "Connection Timed Out"}
    except requests.exceptions.ConnectionError:
        return {"success": False, "status_code": 0, "error": "Connection Refused / No Internet"}
    except requests.exceptions.RequestException as e:
        return {"success": False, "status_code": 0, "error": str(e)}
