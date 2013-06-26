import java
import os
import os.path

from java.lang.reflect import Modifier
from org.python.util import CodegenUtils
from org.python.compiler import CustomMaker, ProxyCodeHelpers


__all__ = ["PackageProxy", "SerializableProxies"]


class SerializableProxies(CustomMaker):

    # NOTE: SerializableProxies is itself a java proxy, but it's not a custom one!

    serialized_path = None
    
    def doConstants(self):
        self.classfile.addField("serialVersionUID",
                                CodegenUtils.ci(java.lang.Long.TYPE), Modifier.PUBLIC | Modifier.STATIC | Modifier.FINAL)
        code = self.classfile.addMethod("<clinit>", ProxyCodeHelpers.makeSig("V"), Modifier.STATIC)
        code.visitLdcInsn(java.lang.Long(1))
        code.putstatic(self.classfile.name, "serialVersionUID", CodegenUtils.ci(java.lang.Long.TYPE))
        code.return_()

    def saveBytes(self, bytes):
        if self.serialized_path:
            path = os.path.join(self.serialized_path, os.path.join(*self.myClass.split(".")) + ".class")
            parent = os.path.dirname(path)
            print "Saving bytes for", self.myClass, "to", path
            try:
                os.makedirs(parent)
            except OSError:
                pass  # Directory exists
            with open(path, "wb") as f:
                f.write(bytes.toByteArray())

    def makeClass(self):
        print "Entering makeClass", self
        try:
            # If already defined on CLASSPATH, simply return this class
            cls = java.lang.Class.forName(self.myClass)
            print "Looked up proxy", self.myClass
        except:
            # Otherwise build it
            print "Calling super..."
            cls = CustomMaker.makeClass(self)
            print "Built proxy", self.myClass
        return cls


class PackageProxy(object):

    def __init__(self, package):
        self.package = package
    
    def __call__(self, superclass, interfaces, className, pythonModuleName, fullProxyName, mapping):
        """Constructs a usable proxy name that does not depend on ordering"""
        print "Package proxy for", self.package, superclass, interfaces, className, pythonModuleName, fullProxyName, mapping
        return SerializableProxies(superclass, interfaces, className, pythonModuleName, self.package + "." + pythonModuleName + "." + className, mapping)

