import argparse
import distutils.dir_util
import distutils.file_util
import glob
import importlib
import os
import os.path
import shutil
import subprocess
import sys
import tempfile

from clamp import SerializableProxies


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
    parser.add_argument("--include", "-i", help="Include this Python library (in addition to stdlib)",
                        dest="includes", action="append", default=[os.path.join(sys.executable, "../../Lib")])
    parser.add_argument("--proxy", help="Generate proxies for this Python module", dest="proxies", action="append", default=[])
    parser.add_argument("--jar", help="Jar file to include", dest="jars", action="append", default=[])
    parser.add_argument("--output", "-o", help="Name of output jar", default="uber.jar")
    parser.add_argument("--runpy", help="Path to __runpy__.py for standalone running", default=os.path.join(os.getcwd(), "__run__.py"))
    args = parser.parse_args()

    # Add relevant paths
    args.jars.extend(find_jython_jars())

    print args

    tempdir = tempfile.mkdtemp()
    filesdir = os.path.join(tempdir, "files")
    print "building in", tempdir

    SerializableProxies.serialized_path = filesdir
    for proxy in args.proxies:
        importlib.import_module(proxy)


    for include in args.includes:
        distutils.dir_util.copy_tree(include, os.path.join(filesdir, os.path.basename(include)))
    # FIXME above should ignore javatests, Lib/tests, unless otherwise directed

    distutils.file_util.copy_file(args.runpy, filesdir)

    explode_jars(args.jars, filesdir)

    subprocess.check_call(["jar", "cf", args.output, "-C", filesdir, "."])
    #shutil.rmtree(tempdir)


if __name__ == "__main__":
    main()
