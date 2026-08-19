import importlib
import pkgutil


def register_error_handlers(app):
    package = __name__

    for module_info in pkgutil.iter_modules(__path__):
        if module_info.name.startswith("_"):
            continue

        module = importlib.import_module(f"{package}.{module_info.name}")

        register = getattr(module, "register_error_handlers", None)

        if register is not None:
            register(app)
