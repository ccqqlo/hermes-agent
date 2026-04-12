from datetime import timedelta
from types import SimpleNamespace

from gateway.session import SessionEntry, SessionStore, _now


def test_suspend_recently_active_uses_datetime_cutoff(tmp_path):
    config = SimpleNamespace(group_sessions_per_user=True, thread_sessions_per_user=False)
    store = SessionStore(sessions_dir=tmp_path, config=config)
    now = _now()
    store._loaded = True
    store._entries = {
        "recent": SessionEntry(
            session_key="recent",
            session_id="s1",
            created_at=now,
            updated_at=now - timedelta(seconds=30),
        ),
        "old": SessionEntry(
            session_key="old",
            session_id="s2",
            created_at=now,
            updated_at=now - timedelta(minutes=10),
        ),
    }

    suspended = store.suspend_recently_active(max_age_seconds=120)

    assert suspended == 1
    assert store._entries["recent"].suspended is True
    assert store._entries["old"].suspended is False
