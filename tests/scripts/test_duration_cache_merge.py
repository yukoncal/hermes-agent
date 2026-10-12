"""Tests for CI duration-cache merge helpers."""

from __future__ import annotations

import json
from pathlib import Path

from scripts.run_tests_parallel import merge_duration_cache_files


def test_merge_duration_cache_files_combines_slices(tmp_path: Path) -> None:
    slice_a = tmp_path / "test-durations-slice-1"
    slice_b = tmp_path / "test-durations-slice-2"
    slice_a.mkdir()
    slice_b.mkdir()
    (slice_a / "test_durations.json").write_text(
        json.dumps({"tests/a/test_one.py": 1.5}, indent=2) + "\n"
    )
    (slice_b / "test_durations.json").write_text(
        json.dumps({"tests/b/test_two.py": 2.25}, indent=2) + "\n"
    )

    merged = merge_duration_cache_files(
        [
            slice_a / "test_durations.json",
            slice_b / "test_durations.json",
        ]
    )

    assert merged == {
        "tests/a/test_one.py": 1.5,
        "tests/b/test_two.py": 2.25,
    }


def test_merge_duration_cache_files_tolerates_concatenated_json(tmp_path: Path) -> None:
    path = tmp_path / "test_durations.json"
    path.write_text(
        json.dumps({"tests/a/test_one.py": 1.0}, indent=2)
        + "\n"
        + json.dumps({"tests/b/test_two.py": 2.0}, indent=2)
        + "\n"
    )

    merged = merge_duration_cache_files([path])

    assert merged == {
        "tests/a/test_one.py": 1.0,
        "tests/b/test_two.py": 2.0,
    }
