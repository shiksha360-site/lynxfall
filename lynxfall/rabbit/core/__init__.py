import builtins
import importlib

from .backends import *
from .process import *

builtins.dbg = importlib.import_module("lynxfall.rabbit.core.debug_funcs")