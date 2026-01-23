# SPDX-License-Identifier: AGPL-3.0-or-later
#
# Copyright (C) 2026 Minoru Sekine
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

import re

import blinter
import pytest

import blinter_simple_output.formatter

TEST_ERROR_RULE = blinter.Rule(
    code="E001",
    name="Error rule for test.",
    severity=blinter.RuleSeverity.ERROR,
    explanation="This rule is only made for unit test"
    "of blinter-simple-output",
    recommendation="No recommendation"
)

TEST_ERROR_ISSUE = blinter.LintIssue(
    line_number=1,
    rule=TEST_ERROR_RULE,
    context="Context of this issue",
    file_path="blinter-simple-output-test.cmd"
)


@pytest.mark.parametrize("formatter",
                          [blinter_simple_output.formatter.ErrorformatFormatter(),
                           blinter_simple_output.formatter.GitHubAnnotationFormatter()])
def test_formatter(formatter):
    formatted_string = formatter.format_lintissue_to_string(issue=TEST_ERROR_ISSUE)
    assert isinstance(formatted_string, str)
    assert len(formatted_string) >= 1

def test_github_annotation_formatter():
    formatter = blinter_simple_output.formatter.GitHubAnnotationFormatter()
    formatted_string = formatter.format_lintissue_to_string(issue=TEST_ERROR_ISSUE)
    assert re.match(r'::(error|warning|notice) [^:]+::.+', formatted_string)
