import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from autoshift_core.mainframe import collect_system_info


def test_collect_system_info(monkeypatch):
    def fake_run(cmd):
        assert cmd == ["uname", "-a"]
        return "zOS 2.2"

    monkeypatch.setattr("autoshift_core.mainframe.run_command", fake_run)
    info = collect_system_info()
    assert info == {"system_info": "zOS 2.2"}
