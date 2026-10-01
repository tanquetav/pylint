# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

"""Optional checker for function calls used as default argument values."""

from __future__ import annotations

from typing import TYPE_CHECKING

from astroid import bases, nodes

from pylint.checkers import BaseChecker
from pylint.checkers.utils import only_required_for_messages, safe_infer
from pylint.interfaces import INFERENCE, UNDEFINED

if TYPE_CHECKING:
    from pylint.lint import PyLinter


class DefaultArgumentsChecker(BaseChecker):
    """Checks the expressions used as default argument values.

    - function-call-in-default-argument: a call is evaluated only once, when the
      function is defined, not each time the function is called.
    """

    name = "default-arguments"
    msgs = {
        "W3801": (
            "Function call '%s()' in default argument is evaluated once, at definition time",
            "function-call-in-default-argument",
            "Used when a function call appears in the default value of an argument. "
            "Default values are evaluated a single time, when the function is defined, "
            "so the call is not repeated when the argument is omitted and every call "
            "shares the same result (e.g. the same uuid or timestamp). Use ``None`` as "
            "the default and create the value inside the function body instead.",
        ),
    }
    options = (
        (
            "allowed-default-calls",
            {
                "default": (
                    "builtins.bool",
                    "builtins.bytes",
                    "builtins.complex",
                    "builtins.float",
                    "builtins.frozenset",
                    "builtins.int",
                    "builtins.object",
                    "builtins.range",
                    "builtins.str",
                    "builtins.tuple",
                ),
                "type": "csv",
                "metavar": "<comma separated list>",
                "help": "List of qualified names (i.e., library.function) of calls "
                "that are allowed in default arguments, because they return an "
                "immutable value or are meant to run once, e.g. "
                "'fastapi.Depends,fastapi.Query'. A name that cannot be inferred is "
                "matched as written in the source.",
            },
        ),
    )

    @only_required_for_messages("function-call-in-default-argument")
    def visit_functiondef(self, node: nodes.FunctionDef) -> None:
        self._check_defaults(node.args)

    visit_asyncfunctiondef = visit_functiondef

    @only_required_for_messages("function-call-in-default-argument")
    def visit_lambda(self, node: nodes.Lambda) -> None:
        self._check_defaults(node.args)

    def _check_defaults(self, arguments: nodes.Arguments) -> None:
        # kw_defaults holds None for keyword-only arguments without a default.
        for default in (*arguments.defaults, *arguments.kw_defaults):
            # The body of a lambda only runs when it is called, so the calls
            # inside it are not evaluated at definition time.
            if default is None or isinstance(default, nodes.Lambda):
                continue
            for call in default.nodes_of_class(nodes.Call, skip_klass=nodes.Lambda):
                self._check_call(call)

    def _check_call(self, node: nodes.Call) -> None:
        allowed = self.linter.config.allowed_default_calls
        written_name = node.func.as_string()
        inferred = safe_infer(node.func)
        if written_name in allowed:
            return
        if (
            isinstance(inferred, (nodes.LocalsDictNodeNG, bases.Proxy))
            and inferred.qname() in allowed
        ):
            return
        self.add_message(
            "function-call-in-default-argument",
            node=node,
            args=(written_name,),
            confidence=INFERENCE if inferred else UNDEFINED,
        )


def register(linter: PyLinter) -> None:
    linter.register_checker(DefaultArgumentsChecker(linter))
