import java
import os
import os.path

from java.lang.reflect import Modifier
from org.python.util import CodegenUtils
from org.python.compiler import JavaMaker, ProxyCodeHelpers


__all__ = ["PackageProxy", "SerializableProxies"]


class SerializableProxies(JavaMaker):

    serialized_path = "proxies"
    
    def doConstants(self):
        self.classfile.addField("serialVersionUID",
                                CodegenUtils.ci(java.lang.Long.TYPE), Modifier.PUBLIC | Modifier.STATIC | Modifier.FINAL)
        code = self.classfile.addMethod("<clinit>", ProxyCodeHelpers.makeSig("V"), Modifier.STATIC)
        code.visitLdcInsn(java.lang.Long(1))
        code.putstatic(self.classfile.name, "serialVersionUID", CodegenUtils.ci(java.lang.Long.TYPE))
        code.return_()

    def build(self, *args):
        JavaMaker.build(self, *args)
        # Intercept the side effect from call to super such that if args is
        # available, then it is a ByteOutputStream and has contents we
        # can get nondestructively
        #
        # This is such a hack; there should be a hook for this FIXME
        # Alternatively it would be nice to support parameter overloading in Jython

        if len(args) > 0:
            path = os.path.join(self.serialized_path, os.path.join(*self.myClass.split(".")) + ".class")
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
        print "Building a proxy for", self.package, superclass, interfaces, className, pythonModuleName, fullProxyName, mapping
        return SerializableProxies(superclass, interfaces, className, pythonModuleName, self.package + "." + pythonModuleName + "." + className, mapping)

