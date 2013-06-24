import argparse
import distutils.dir_util
import glob
import importlib
import os
import os.path
import shutil
import subprocess
import sys
import tempfile

import org.python.core.Options


def find_jython_jars():
    # Uses the same classpath resolution as bin/jython
    jython_jar_path = os.path.normpath(os.path.join(sys.executable, "../../jython.jar"))
    jython_jar_dev_path = os.path.normpath(os.path.join(sys.executable, "../../jython-dev.jar"))
    if os.path.exists(jython_jar_dev_path):
        jars = [jython_jar_dev_path]
        jars.extend(glob.glob(os.path.normpath(os.path.join(jython_jar_dev_path, "../javalib/*.jar"))))
    elif os.path.exists(jython_jar_path):
        jars = [jython_jar_path]
    else:
        raise Exception("Cannot find jython jar")
    return jars


def explode_jars(jars, tempdir):
    """Given a list of `jars`, explode them into `tempdir`"""
    jars = reversed(jars) # Reverse the path to follow classpath resolution; might be nice to detect inconsistencies FIXME
    olddir = os.getcwd()
    try:
        os.chdir(tempdir)
        for jar in jars:
            print "Adding jar", jar
            subprocess.check_call(["jar", "xf", jar])
    finally:
        os.chdir(olddir)


def main():
    parser = argparse.ArgumentParser(description="Generate a single jar for Storm")
    parser.add_argument("--include", "-i", help="Add to compile path", dest="includes", action="append", default=[])
    parser.add_argument("--proxy", help="Proxy to generate", dest="proxies", action="append", default=[])
    parser.add_argument("--jar", help="Jar file to include", dest="jars", action="append", default=[])
    parser.add_argument("--output", "-o", help="Name of output jar", default="uber.jar")
    args = parser.parse_args()

    # Add relevant paths
    args.jars.extend(find_jython_jars())

    print args

    tempdir = tempfile.mkdtemp()
    filesdir = os.path.join(tempdir, "files")
    org.python.core.Options.proxyDebugDirectory = filesdir

    for proxy in args.proxies:
        # FIXME probably should be doing this in a separate PythonInterpreter;
        # this might get pass ordering problems; until then build using a separate proxies jar
        importlib.import_module(proxy)

    distutils.dir_util.copy_tree(
        os.path.normpath(os.path.join(sys.executable, "../../Lib")),
        os.path.join(filesdir, "Lib"))
    # FIXME above should ignore javatests, Lib/tests, unless otherwise directed

    for include in args.includes:
        distutils.dir_util.copy_tree(include, filesdir)

    explode_jars(args.jars, filesdir)

    subprocess.check_call(["jar", "cf", args.output, "-C", filesdir, "."])
    shutil.rmtree(tempdir)


if __name__ == "__main__":
    main()
