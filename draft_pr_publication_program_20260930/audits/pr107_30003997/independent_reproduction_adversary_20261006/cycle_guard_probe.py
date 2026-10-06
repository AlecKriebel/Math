#!/usr/bin/env python3
"""Bounded in-memory cycle control for author's second assert site."""
import json
import runpy
import signal
import sys

namespace=runpy.run_path(sys.argv[1],run_name="__audit_cycle_probe__")
def timed_out(signum,frame):
    raise TimeoutError("cycle traversal did not reject within 0.1 seconds")
signal.signal(signal.SIGALRM,timed_out)
signal.setitimer(signal.ITIMER_REAL,0.1)
try:
    namespace["paths_of_parent"](["r","a"],{"a":"a"})
except TimeoutError:
    print(json.dumps({"result":"CYCLE_GUARD_BYPASSED","alarm_seconds":0.1,
                      "control":"self-parent cycle with no path to root"},sort_keys=True))
    sys.exit(2)
finally:
    signal.setitimer(signal.ITIMER_REAL,0)
