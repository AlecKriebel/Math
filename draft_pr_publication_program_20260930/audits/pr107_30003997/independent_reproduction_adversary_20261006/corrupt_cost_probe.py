#!/usr/bin/env python3
"""False-positive probe: in-memory zeroing of the costs on a known no instance.

No frozen file is modified. The proof's contradictory-unit optimum is 1;
replacing its dense destination costs with zeros incorrectly makes it 0.
The original instance check must reject that discrepancy.
"""
import json
import runpy
import sys

kind, script = sys.argv[1:]
namespace=runpy.run_path(script,run_name="__audit_corrupt_cost_probe__")
if kind == "author":
    instance=namespace["instance"]
    original=instance.__globals__["make"]
    def corrupt(n, clauses):
        nodes, arcs, levels, costs=original(n,clauses)
        return nodes, arcs, levels, {}
    instance.__globals__["make"]=corrupt
    answer=instance(1,[(1,),(-1,)])
elif kind == "independent":
    instance=namespace["check_instance"]
    original=instance.__globals__["build"]
    def corrupt(n, clauses):
        vertices, arcs, costs=original(n,clauses)
        return vertices, arcs, [[0 for value in row] for row in costs]
    instance.__globals__["build"]=corrupt
    answer=instance(1,[(1,),(-1,)])
else:
    instance=namespace["verify_formula"]
    original=instance.__globals__["construct"]
    def corrupt(n, clauses):
        graph=original(n,clauses)
        graph["dense"]=[[0 for value in row] for row in graph["dense"]]
        return graph
    instance.__globals__["construct"]=corrupt
    answer=instance(1,[(1,),(-1,)])["minimum"]
print(json.dumps({"result":"ACCEPTED_CORRUPT_MODEL","computed_optimum":answer,"correct_optimum":1,
                  "mutation":"all destination-specific costs erased in memory on contradictory units"},sort_keys=True))
