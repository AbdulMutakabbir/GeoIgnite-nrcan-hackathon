# import os
# import importlib

# # Get current directory
# layout_dir = os.path.dirname(__file__)
# layout_modules = []

# # Import each Python file in this folder (excluding __init__.py)
# for filename in os.listdir(layout_dir):
#     if filename.endswith(".py") and filename != "__init__.py":
#         module_name = filename[:-3]  # strip .py
#         layout_modules.append(module_name)
#         globals()[module_name] = importlib.import_module(f".{module_name}", package=__name__)


from .dist_fuel_prov import *
from .percentage_fuel_prov import *
from .area_fuel_prov import *
from .home_page import *