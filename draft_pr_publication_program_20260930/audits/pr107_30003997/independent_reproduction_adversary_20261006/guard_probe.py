#!/usr/bin/env python3
"""Run frozen checker unchanged, then submit a known-false check to its gate."""
import json
import runpy
import sys

kind, script = sys.argv[1:]
namespace = runpy.run_path(script,run_name="__audit_guard_probe__")
if kind == "author":
    # The actual gadget's one-variable contradictory unit pair has optimum 1.
    actual = namespace["instance"](1,[(1,),(-1,)])
    namespace["ck"]("known_false_contradictory_units_have_cost_zero", actual == 0)
else:
    actual = namespace["check_instance"](1,[(1,),(-1,)])
    namespace["ck"](actual == 0,"known_false_contradictory_units_have_cost_zero")
print(json.dumps({"guard":"ACCEPTED_KNOWN_FALSE","actual_optimum":actual,
                  "submitted_false_claim":"contradictory units have optimum zero"},sort_keys=True))
