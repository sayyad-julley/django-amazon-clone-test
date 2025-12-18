import sys
import os

# Add framework root to Python path
framework_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))
sys.path.insert(0, framework_root)

# Now import the conftest from the framework
# Import local conftest contents instead of recursive import
from conftest import *
