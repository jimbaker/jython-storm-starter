import importlib
import os
import os.path

from clamp import SerializableProxies

SerializableProxies.serialized_path = os.path.join(os.getcwd(), "custom") 
importlib.import_module("excl.plumbing")

