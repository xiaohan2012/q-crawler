import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../..')) #append the parent dir in the PythonPath env variable
print os.path.join(os.path.dirname(__file__), '../../..')

DIRNAME = os.path.dirname(os.path.realpath(__file__))
