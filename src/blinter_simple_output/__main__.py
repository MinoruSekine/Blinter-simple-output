# SPDX-License-Identifier: AGPL-3.0-or-later
#
# Copyright (C) 2026 Minoru Sekine
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

import argparse
import os
import sys
from collections.abc import Iterable
from pathlib import Path

import blinter

import blinter_simple_output.formatter


def _is_dot_path(path: Path):
    return any(part.startswith(".") for i, part in enumerate(path.parts))

def _enum_batfiles_recursively(dir_path: Path, include_dot_dirs: bool) -> list[Path]:
    TARGET_SUFFIXES = {".bat", ".cmd"}
    return [p
            for p in dir_path.rglob("*")
            if p.is_file()
            and p.suffix.lower() in TARGET_SUFFIXES
            and (include_dot_dirs or not _is_dot_path(p))]

def _expand_dir_to_batchfiles_in_it(
        paths: Iterable[Path],
        include_dot_dirs: bool
) -> list[Path]:
    expanded_paths = []
    for p in paths:
        if p.is_file():
            expanded_paths.append(p)
        elif p.is_dir():
            expanded_paths += _enum_batfiles_recursively(p, include_dot_dirs)
    return expanded_paths

def _parse_commandline_arguments():
    argparser = argparse.ArgumentParser(
        description=(
            'Lint .cmd and/or .bat file(s)'
            ' and output result(s) in a simple, line-by-line style.'
        )
    )

    argparser.add_argument(
        '--include-dot-dirs',
        action='store_true',
        help="Enumerate file(s) in .(dot) started dir(s)."
    )

    argparser.add_argument(
        '-s', '--style',
        choices=blinter_simple_output.formatter.formatter_names(),
        default='errorformat',
        help="Output style"
    )

    argparser.add_argument(
        'paths',
        nargs='+',
        type=Path,
        help=(
            "One or more path(s) to lint,"
            "lint .bat and .cmd file(s) recursively if directory is specified"
        )
    )

    return argparser.parse_args()

def main() -> None:
    """Main entrypoint function of blinter-simple-output."""
    args = _parse_commandline_arguments()
    formatter = blinter_simple_output.formatter.create_formatter(args.style)
    for path in _expand_dir_to_batchfiles_in_it(args.paths, args.include_dot_dirs):
        path_string = os.fspath(path)
        issues = blinter.lint_batch_file(path_string)
        for issue in issues:
            sys.stdout.write(
                f"{formatter.format_lintissue_to_string(issue)}\n"
            )
    return

if __name__ == "__main__":
    main()
