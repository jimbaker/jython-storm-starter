Setup
=====

This will be replaced by a much better setup. But for now:

Checkout Jython trunk. Jython trunk has a necessary fix for using Jython with Clojure types, as used in Storm:

~~~~
hg clone ssh://hg@bitbucket.org/jython/jython
~~~~

Within the trunk, build a standalone jar for Jython; this contains the complete standard library:

~~~~
ant all-jars
~~~~

(This step is necessary because Storm needs everything in the classpath, regardless of whether running in its own standalone mode or through Nimbus and a Storm cluster.)

You of course have `storm` installed and on the path. Export `JYTHON_STANDALONE_JAR` to be the path the standalone jar; it will be in `dist/jython-standalone.jar`. Make Jython available on your path `dist/bin/jython`; below I call it `jython27`.

Two more steps:

1. Build proxies. Do this in the path of the repo. (Hey, we said this is just getting it to work, right? It will be changed to use a real setup.py process :)

~~~~
CLASSPATH="`storm classpath`:$JYTHON_STANDALONE_JAR" jython27 gen-proxies.py && jar cf proxies.jar -C proxies org/
~~~~

2. Run the topology:

~~~~
CLASSPATH="`storm classpath`:$JYTHON_STANDALONE_JAR:`pwd`/proxies.jar" jython27 run-exclamation-topology.py
~~~~

One issue here that I'm seeing is that this mucks up the console so that it will no longer accept keyboard input. Workaround: start a new window.

