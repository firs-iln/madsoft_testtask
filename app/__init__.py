import os
import sys

sys.path.append(os.path.dirname(os.path.realpath(__file__)))

print(sys.path)

from .main import app

__all__ = [
    'app',
]
