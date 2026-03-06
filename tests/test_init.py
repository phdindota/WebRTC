"""Tests for WebRTC Camera integration."""
import time

from custom_components.webrtc import (
    _check_rate_limit,
    _record_auth_failure,
    _cleanup_stale_links,
    AUTH_FAILURES,
    LINKS,
    MAX_LINK_AGE,
)


class TestRateLimiting:
    """Test rate limiting functionality."""

    def setup_method(self):
        AUTH_FAILURES.clear()

    def test_no_failures_not_limited(self):
        assert _check_rate_limit("192.168.1.1") is False

    def test_under_limit_not_limited(self):
        for _ in range(5):
            _record_auth_failure("192.168.1.1")
        assert _check_rate_limit("192.168.1.1") is False

    def test_at_limit_is_limited(self):
        for _ in range(10):
            _record_auth_failure("192.168.1.1")
        assert _check_rate_limit("192.168.1.1") is True

    def test_different_ips_independent(self):
        for _ in range(10):
            _record_auth_failure("192.168.1.1")
        assert _check_rate_limit("192.168.1.2") is False


class TestLinkCleanup:
    """Test LINKS cleanup functionality."""

    def setup_method(self):
        LINKS.clear()

    def test_cleanup_removes_stale_links(self):
        LINKS["old"] = {
            "url": "test", "entity": None,
            "limit": 0, "ts": 0,
            "created_at": time.time() - MAX_LINK_AGE - 100,
        }
        LINKS["fresh"] = {
            "url": "test2", "entity": None,
            "limit": 0, "ts": 0,
            "created_at": time.time(),
        }
        _cleanup_stale_links()
        assert "old" not in LINKS
        assert "fresh" in LINKS

    def test_cleanup_handles_empty(self):
        _cleanup_stale_links()
        assert len(LINKS) == 0
