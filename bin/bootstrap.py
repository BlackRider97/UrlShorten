#!/usr/bin/env python
import sys
import os
import subprocess

if "VIRTUAL_ENV" not in os.environ:
    sys.stderr.write("$VIRTUAL_ENV not found.\n\n")
    sys.exit(-1)
virtualenv = os.environ["VIRTUAL_ENV"]
file_path = os.path.dirname(__file__)
env = os.environ.copy()
env["CFLAGS"]="-m64"
subprocess.call(["pip", "install", "--quiet", "--requirement",
                 os.path.join(file_path, "../requirements/packages.txt")], env=env)
