# This file is part of sphinx-relabel.
#
# This program is free software: you can redistribute it and/or modify it under the
# terms of the GNU General Public License version 3, as published by the Free
# Software Foundation.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranties of MERCHANTABILITY, SATISFACTORY
# QUALITY, or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public
# License for more details.
#
# You should have received a copy of the GNU General Public License along with
# this program.  If not, see <http://www.gnu.org/licenses/>.

import shutil
import subprocess
from pathlib import Path
from typing import cast

import bs4
import pytest
from sphinx.util.inventory import InventoryFile


@pytest.fixture
def file_input_example(request) -> Path:
    project_root = request.config.rootpath
    example_dir = project_root / "tests/integration/file_input_example"

    target_dir = Path().resolve() / "file_input_example"
    shutil.copytree(example_dir, target_dir, dirs_exist_ok=True)

    return target_dir


@pytest.fixture
def dict_input_example(request) -> Path:
    project_root = request.config.rootpath
    example_dir = project_root / "tests/integration/dict_input_example"

    target_dir = Path().resolve() / "dict_input_example"
    shutil.copytree(example_dir, target_dir, dirs_exist_ok=True)

    return target_dir


@pytest.mark.slow
def test_relabel_dict_input(dict_input_example):
    build_dir = dict_input_example / "_build"
    subprocess.check_call(
        ["sphinx-build", "-b", "html", "-W", dict_input_example, build_dir],
    )

    inv_path = build_dir.parents[1] / ".test_output/dict_input/objects.inv"

    # Rename the test output to something more meaningful
    shutil.copytree(
        build_dir, build_dir.parents[1] / ".test_output/dict_input", dirs_exist_ok=True
    )

    shutil.rmtree(dict_input_example)  # Delete copied source

    inv = {}
    with Path.open(inv_path, "rb") as f:
        inv = cast(
            dict[str, dict[str, dict[str, tuple[str, str, str, str]]]],
            InventoryFile.load(f, inv_path, joinfunc=lambda a, b: b),
        )

    target_doc, _, anchor, link_text = inv["std:label"]["bad-label"]
    assert target_doc == "sphinx-relabel tests"
    assert anchor == "index.html#good-label"
    assert link_text == "Target section"


@pytest.mark.slow
def test_relabel_file_input(file_input_example):
    build_dir = file_input_example / "_build"
    subprocess.check_call(
        ["sphinx-build", "-b", "html", "-W", file_input_example, build_dir],
    )

    inv_path = build_dir.parents[1] / ".test_output/file_input/objects.inv"

    # Rename the test output to something more meaningful
    shutil.copytree(
        build_dir, build_dir.parents[1] / ".test_output/file_input", dirs_exist_ok=True
    )

    shutil.rmtree(file_input_example)  # Delete copied source

    inv = {}
    with Path.open(inv_path, "rb") as f:
        inv = cast(
            dict[str, dict[str, dict[str, tuple[str, str, str, str]]]],
            InventoryFile.load(f, inv_path, joinfunc=lambda a, b: b),
        )

    target_doc, _, anchor, link_text = inv["std:label"]["bad-label"]
    assert target_doc == "sphinx-relabel tests"
    assert anchor == "index.html#good-label"
    assert link_text == "Target section"
