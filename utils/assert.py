# utils/assert_util.py
def assert_status_code(response, expected_code):
    assert response.status_code == expected_code, \
        f"Expected status {expected_code}, got {response.status_code}"


def assert_json_key(response, key):
    assert key in response.json(), f"Key '{key}' not found in response"
