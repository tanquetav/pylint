Default values are evaluated once, when the ``def`` statement runs, and not each time the
function is called. A call used as a default (``key=default_key()``) therefore runs a single
time and every call that omits the argument shares its result: the same uuid, the same
timestamp, the same connection.

Use ``None`` as the default and create the value inside the function body, as in the
example above.

Calls that return an immutable value, such as ``tuple()`` or ``int("1")``, are allowed.
This checker is optional: enable it with ``load-plugins=pylint.extensions.default_arguments``.
Add other calls that are safe or intentional (e.g. ``fastapi.Depends``) to the
``allowed-default-calls`` option.
