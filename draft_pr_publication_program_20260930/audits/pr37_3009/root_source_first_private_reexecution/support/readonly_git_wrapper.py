#!/usr/bin/python3
import os,sys
allowed={"ls-tree","cat-file","diff","show","branch","rev-parse","merge-base","check-ignore"}
assert sys.argv[1] in allowed
assert sys.argv[1]!="branch" or sys.argv[2:]==["--show-current"]
os.environ["GIT_OPTIONAL_LOCKS"]="0"
os.execv("/usr/bin/git",["/usr/bin/git",*sys.argv[1:]])
