import logging

from .sketch import Sketch

__all__ = (
    "Sketch",
    "__version__",
)

__version__ = "0.1.0"

# TODO: AI-generated config. Revisit.
logging.getLogger("pier5").addHandler(logging.StreamHandler())
logging.getLogger("pier5").propagate = False
logging.getLogger("pier5").setLevel(logging.INFO)
