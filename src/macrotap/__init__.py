
from importlib import import_module

modules = (
    "fred",
    "imf",
    "ecb",
)

__all__ = []

for n in modules:

    # Import module
    module = import_module(f".{n}", package=__package__, )

    # Extract the list of all public names
    all_names = getattr(module, "__all__", [])

    # Add the public names to the package's global namespace 
    globals().update({name: getattr(module, name) for name in all_names})

    # Add the public names to the package's __all__ list
    __all__.extend(all_names)

