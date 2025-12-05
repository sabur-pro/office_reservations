import concurrent.futures
import time
import urllib.error
import urllib.request

HTTP_OK = 200
HTTP_TOO_MANY_REQUESTS = 429

BASE_URL = "http://localhost:8000"


def make_request(url: str) -> tuple[int, float]:
    start = time.time()
    try:
        with urllib.request.urlopen(url, timeout=10) as response:
            elapsed = time.time() - start
            return response.status, elapsed
    except urllib.error.HTTPError as e:
        elapsed = time.time() - start
        return e.code, elapsed


def test_concurrent_requests() -> None:
    print("\n" + "=" * 60)
    print("CONCURRENT REQUESTS TEST")
    print("=" * 60)

    url = f"{BASE_URL}/api/offices"
    num_requests = 90

    print(f"\nSending {num_requests} concurrent requests to {url}...")

    start_time = time.time()

    with concurrent.futures.ThreadPoolExecutor(max_workers=num_requests) as executor:
        futures = [executor.submit(make_request, url) for _ in range(num_requests)]
        results = [f.result() for f in concurrent.futures.as_completed(futures)]

    total_time = time.time() - start_time

    successful = sum(1 for status, _ in results if status == HTTP_OK)
    response_times = [elapsed for _, elapsed in results]
    avg_time = sum(response_times) / len(response_times)

    print("\nResults:")
    print(f"  Total requests: {num_requests}")
    print(f"  Successful: {successful}")
    print(f"  Total time: {total_time:.3f}s")
    print(f"  Avg response time: {avg_time:.3f}s")

    if total_time < avg_time * num_requests * 0.5:
        print("\n✅ PASS: Requests processed concurrently!")
        print(f"   (Sequential would take ~{avg_time * num_requests:.3f}s)")
    else:
        print("\n❌ FAIL: Requests appear to be sequential")

    return successful == num_requests


def test_rate_limiting() -> None:
    print("\n" + "=" * 60)
    print("RATE LIMITING TEST")
    print("=" * 60)

    url = f"{BASE_URL}/api/offices"
    num_requests = 110

    print(f"\nSending {num_requests} requests rapidly...")

    results = []
    for i in range(num_requests):
        status, _ = make_request(url)
        results.append(status)
        if status == HTTP_TOO_MANY_REQUESTS:
            print(f"  Rate limited at request #{i + 1}")
            break

    rate_limited = HTTP_TOO_MANY_REQUESTS in results
    if rate_limited:
        print("\n✅ PASS: Rate limiting is working!")
    else:
        print("\n⚠️  Rate limiting not triggered (may need more requests)")


def main() -> None:
    print("\n" + "=" * 60)
    print("SERVER THREADING TESTS")
    print("=" * 60)
    print(f"\nTarget: {BASE_URL}")
    print("Make sure the server is running before tests!")

    try:
        make_request(BASE_URL)
    except Exception:
        print("\n❌ ERROR: Cannot connect to server!")
        print("   Run: ./start_server.sh")
        return

    test_concurrent_requests()
    test_rate_limiting()

    print("\n" + "=" * 60)
    print("TESTS COMPLETE")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()
