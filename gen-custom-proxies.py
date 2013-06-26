import importlib
import os
import os.path

from clamp import SerializableProxies

# still need to control output directory by a global variable, but at least this can be in a separate PythonInterpreter!

SerializableProxies.serialized_path = os.path.join(os.getcwd(), "custom") 
importlib.import_module("excl.plumbing")

