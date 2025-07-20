import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))  # noqa: E402
from autoshift_core.mainframe import collect_system_info  # noqa: E402


def test_collect_system_info(monkeypatch):
    def fake_run(cmd):
        assert cmd == ["uname", "-a"]
        return "zOS 2.2"

    monkeypatch.setattr("autoshift_core.mainframe.run_command", fake_run)
    info = collect_system_info()
    assert info == {"system_info": "zOS 2.2"}
