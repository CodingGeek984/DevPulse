import time

import httpx


def check_url(url, expected_status=200, timeout=10.0):
    started = time.perf_counter()

    try:
        response = httpx.get(url, timeout=timeout, follow_redirects=True)
    except Exception as exc:
        return {
            "status_code": None,
            "response_time_ms": round((time.perf_counter() - started) * 1000, 2),
            "is_up": False,
            "error_message": f"{type(exc).__name__}: {exc}",
        }

    response_time_ms = round((time.perf_counter() - started) * 1000, 2)
    is_up = response.status_code == expected_status

    return {
        "status_code": response.status_code,
        "response_time_ms": response_time_ms,
        "is_up": is_up,
        "error_message": None if is_up else f"Expected status {expected_status}, got {response.status_code}",
    }
