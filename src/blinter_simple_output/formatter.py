# SPDX-License-Identifier: AGPL-3.0-or-later
#
# Copyright (C) 2026 Minoru Sekine
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

import blinter


class ErrorformatFormatter:
    def format_lintissue_to_string(self, issue:blinter.LintIssue) ->str:
        return (
            f"{issue.file_path}:{issue.line_number} "
            f":{self._get_error_type_string(issue)}:{issue.rule.name}"
        )

    def _get_error_type_string(self, issue:blinter.LintIssue) ->str:
        SEVERITY_ERRORTYPE_DICT: dict[blinter.RuleSeverity,str] = {
            blinter.RuleSeverity.ERROR:       "e",
            blinter.RuleSeverity.WARNING:     "w",
            blinter.RuleSeverity.STYLE:       "n",
            blinter.RuleSeverity.SECURITY:    "e",
            blinter.RuleSeverity.PERFORMANCE: "i",
        }
        return SEVERITY_ERRORTYPE_DICT[issue.rule.severity]

_FORMATTERS = {
    "errorformat": ErrorformatFormatter,
    "github-annotation": ErrorformatFormatter,
}

def formatter_names() -> list[str]:
    return _FORMATTERS.keys()
