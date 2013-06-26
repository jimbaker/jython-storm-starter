Setup
=====

This will be replaced by a much better setup. But for now:

Checkout Jython trunk. Jython trunk has a necessary fix for using Jython with Clojure types, as used in Storm:

~~~~
hg clone ssh://hg@bitbucket.org/jython/jython
~~~~

Build the trunk:

~~~~
ant
~~~~

You of course have `storm` installed with its bin directory on the path. Make Jython available on your path `dist/bin/jython`; below I call it `jython27`.

Two more steps:

1. Build a standalone jar file for Storm:

~~~~
CLASSPATH="`storm classpath`" jython27 gen-storm-jar.py -o uber.jar -i excl -i clamp --proxy=excl.plumbing
~~~~

2. Run the topology. Either stand alone mode:

~~~~
CLASSPATH="`storm classpath`:`pwd`/uber.jar" java org.python.util.jython run-exclamation-topology.py
~~~~

or on the storm cluster by submitting the jar:

~~~~
storm jar uber.jar org.python.util.JarRunner
~~~~

(Topology submitting code is in `__run__.py`.)