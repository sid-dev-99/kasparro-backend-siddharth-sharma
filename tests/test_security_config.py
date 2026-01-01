import os
import pytest
from fastapi import HTTPException
from app.core.security import get_api_key

def test_get_api_key_missing_env():
    """Test that RuntimeError is raised when APP_API_KEY is missing."""
    # Ensure env var is unset
    if "APP_API_KEY" in os.environ:
        del os.environ["APP_API_KEY"]
    
    with pytest.raises(RuntimeError) as excinfo:
        get_api_key("some-key")
    assert "APP_API_KEY environment variable is not set" in str(excinfo.value)

def test_get_api_key_invalid():
    """Test that HTTPException(403) is raised when key is invalid."""
    os.environ["APP_API_KEY"] = "secure-key"
    try:
        with pytest.raises(HTTPException) as excinfo:
            get_api_key("wrong-key")
        assert excinfo.value.status_code == 403
    finally:
        del os.environ["APP_API_KEY"]

def test_get_api_key_valid():
    """Test that valid key is accepted."""
    os.environ["APP_API_KEY"] = "secure-key"
    try:
        result = get_api_key("secure-key")
        assert result == "secure-key"
    finally:
        del os.environ["APP_API_KEY"]

if __name__ == "__main__":
    # Manually run tests if executed as script
    try:
        test_get_api_key_missing_env()
        print("test_get_api_key_missing_env PASSED")
        test_get_api_key_invalid()
        print("test_get_api_key_invalid PASSED")
        test_get_api_key_valid()
        print("test_get_api_key_valid PASSED")
    except Exception as e:
        print(f"FAILED: {e}")
        exit(1)
