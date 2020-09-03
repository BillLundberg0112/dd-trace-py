from .trace import TracePlugin

import bottle

from ddtrace import config
from ...utils.wrappers import wrap_function_wrapper as _w


def patch():
    """Patch the bottle.Bottle class
    """
    if getattr(bottle, '_datadog_patch', False):
        return

    setattr(bottle, '_datadog_patch', True)
    _w('bottle', 'Bottle.__init__', traced_init)


def traced_init(wrapped, instance, args, kwargs):
    wrapped(*args, **kwargs)

    service = config._get_service(default="bottle")

    plugin = TracePlugin(service=service)
    instance.install(plugin)
