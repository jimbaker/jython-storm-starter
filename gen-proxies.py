import os
import os.path
import org.python.core.Options

# Generate proxies to enable deserialization from another JVM
org.python.core.Options.proxyDebugDirectory = os.path.join(os.getcwd(), "proxies")

from plumbing import WordSpout, ExclamationBolt

