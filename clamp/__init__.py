import os
import os.path

from java.lang.reflect import Modifier
from org.python.util import CodegenUtils
from org.python.compiler import JavaMaker


class SerializableProxies(JavaMaker):
    
    # def doConstants(self):
    #     self.classfile.addField("serialVersionUID", CodegenUtils.ci(Long.class), Modifier.PUBLIC | Modifier.STATIC | Modifier.FINAL)
    #     code = self.classfile.addMethod("<clinit>", makeSig("V"), Modifier.STATIC)
    #     code.return_() # add LDC, PUTSTATIC
    #

    def build(self, *args):
        JavaMaker.build(self, *args)
        # Intercept the side effect from call to super such that if args is
        # available, then it is a ByteOutputStream and has contents we
        # can get nondestructively
        #
        # This is such a hack; there should be a hook for this FIXME
        # Alternatively it would be nice to support parameter overloading in Jython

        if len(args) > 0:
            path = os.path.join("extra_special", os.path.join(*self.myClass.split(".")) + ".class")
            parent = os.path.dirname(path)
            try:
                os.makedirs(parent)
            except OSError:
                pass  # Directory exists
            with open(path, "wb") as f:
                f.write(args[0].toByteArray())


class PackageProxy(object):

    def __init__(self, package):
        self.package = package
    
    def __call__(self, superclass, interfaces, className, pythonModuleName, fullProxyName, mapping):
        """Modifies className so it uses the package"""
        # FIXME we should be able to use the Python package as well in defining 
        # presumably from __file__?
        print "Building a proxy for", self.package, superclass, interfaces, className, pythonModuleName, fullProxyName, mapping
        return SerializableProxies(superclass, interfaces, className, pythonModuleName, self.package + "." + pythonModuleName + "." + className, mapping)
