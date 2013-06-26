Setup
=====

This will be replaced by a much better setup. But for now:

You need Storm installed with its bin directory on `$PATH`.

Checkout the proxymaker branch of Jython and build it. It includes a necessary fix for using Jython with Clojure types, as used in Storm, in Jython trunk, as well as new custom proxy maker support for better Java integration

~~~~
$ hg clone ssh://hg@bitbucket.org/jimbaker/proxymaker
$ cd proxymaker 
$ ant                                                 # build development version (fastest way)
$ export PATH=$(pwd)/dist/bin:$PATH                   # add jython to your path
~~~~

Two more steps:

1. Build an "uber" jar file for Storm; this contains all necessary jars. Running `storm classpath` computes the necessary classpath for Storm dependencies:

~~~~
$ CLASSPATH="$(storm classpath)" jython27 gen-storm-jar.py -o uber.jar -i excl -i clamp --proxy=excl.plumbing
~~~~

2. Run the topology. Either stand alone mode, using `run-exclamation-topology.py`, which was bundled in the uber jar step:

~~~~
$ CLASSPATH="$(storm classpath):$(pwd)/uber.jar" java org.python.util.jython run-exclamation-topology.py
~~~~

or on the storm cluster by submitting the uber jar; the corresponding cluster submitting code is in `__run__.py`:

~~~~
$ storm jar uber.jar org.python.util.JarRunner
~~~~
