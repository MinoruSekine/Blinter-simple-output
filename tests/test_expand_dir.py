# SPDX-License-Identifier: AGPL-3.0-or-later
#
# Copyright (C) 2026 Minoru Sekine
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

from conftest import TEST_BATCH_FILES_DIR

from blinter_simple_output.__main__ import _expand_dir_to_batchfiles_in_it


def test_expand_dir():
    expanded_paths = _expand_dir_to_batchfiles_in_it([TEST_BATCH_FILES_DIR])
    assert all(path.is_file() for path in expanded_paths)
