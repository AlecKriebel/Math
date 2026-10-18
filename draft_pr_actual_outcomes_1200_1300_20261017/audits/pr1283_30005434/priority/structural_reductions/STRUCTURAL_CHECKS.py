#!/usr/bin/env python3
"""Small independently authored falsification checks; no historical assertions.

Run from this folder: python3 STRUCTURAL_CHECKS.py
The universal argument is in REPORT.md; these examples only check mappings and
separate superficially similar older constructions/classes.
"""
import itertools
import json
from pathlib import Path


def inspect(elements, meet, op, top):
    pairs = list(itertools.product(elements, repeat=2))
    triples = list(itertools.product(elements, repeat=3))
    le = lambda x, y: meet(x, y) == x
    predicates = {
        "hemiimplication": lambda: all(meet(x, op(x, y)) == meet(meet(x, op(x, y)), y) for x, y in pairs),
        "H4": lambda: all(op(x, meet(x, y)) == op(x, y) for x, y in pairs),
        "logical_unit": lambda: all(op(top, x) == x and op(x, top) == top and op(x, x) == top for x in elements),
        "compatible_order": lambda: all((op(x, y) == top) == le(x, y) for x, y in pairs),
        "separation": lambda: all(not (op(x, y) == top and op(y, x) == top) or x == y for x, y in pairs),
        "cycloid": lambda: all(op(op(x, y), op(x, z)) == op(op(y, x), op(y, z)) for x, y, z in triples),
        "meet_preservation": lambda: all(op(x, meet(y, z)) == meet(op(x, y), op(x, z)) for x, y, z in triples),
        "mixed_identity": lambda: all(op(meet(x, y), z) == op(op(x, y), op(x, z)) for x, y, z in triples),
        "Hilbert_self_distributivity": lambda: all(op(x, op(y, z)) == op(op(x, y), op(x, z)) for x, y, z in triples),
    }
    result = {name: test() for name, test in predicates.items()}
    for name, left, right in [
        ("cycloid", lambda x,y,z:op(op(x,y),op(x,z)), lambda x,y,z:op(op(y,x),op(y,z))),
        ("meet_preservation",lambda x,y,z:op(x,meet(y,z)),lambda x,y,z:meet(op(x,y),op(x,z))),
        ("mixed_identity",lambda x,y,z:op(meet(x,y),z),lambda x,y,z:op(op(x,y),op(x,z))),
    ]:
        if not result[name]:
            x,y,z = next(t for t in triples if left(*t) != right(*t))
            result[name+"_witness"] = {"x":x,"y":y,"z":z,"lhs":left(x,y,z),"rhs":right(x,y,z)}
    return result


def main():
    out = {}
    for name, elems, meet, e in [
        ("singleton", [0], min, 0),
        ("chain4", list(range(4)), min, 3),
        ("boolean4", list(range(4)), lambda x,y:x&y, 3),
        ("M3", list(range(5)), lambda x,y:x if x==y else y if x==4 else x if y==4 else 0, 4),
        ("boolean8", list(range(8)), lambda x,y:x&y, 7),
    ]:
        op = lambda x,y,mt=meet,e=e:e if mt(x,y)==x else mt(x,y)
        result = inspect(elems,meet,op,e)
        assert all(result[k] for k in ["hemiimplication","H4","logical_unit","compatible_order","separation","cycloid","meet_preservation","mixed_identity"])
        out["target_"+name] = result
    # Old order implication, distinct from the target on incomparable inputs.
    mt = lambda x,y:x&y
    poset_op = lambda x,y:3 if mt(x,y)==x else y
    out["old_order_implication_boolean4"] = inspect(list(range(4)),mt,poset_op,3)
    assert not out["old_order_implication_boolean4"]["meet_preservation"]
    # A member of hIS4 with logical unit and exact order, but not cycloid.
    # Rows/columns are 0 < a=1 < b=2 < e=3.
    table = [[3,3,3,3],[0,3,3,3],[0,0,3,3],[0,1,2,3]]
    out["hIS4_logical_unit_order_counterexample"] = inspect(list(range(4)),min,lambda x,y:table[x][y],3)
    r = out["hIS4_logical_unit_order_counterexample"]
    assert all(r[k] for k in ["hemiimplication","H4","logical_unit","compatible_order","separation"])
    assert not r["cycloid"]
    out["hIS4_logical_unit_order_counterexample"]["table"] = table
    # The workshop's four equations permit any prescribed point under projection.
    for point in range(4):
        r=inspect(list(range(4)),min,lambda x,y:y,point)
        assert all(r[k] for k in ["meet_preservation","mixed_identity","cycloid"])
        assert all((lambda x,y:y)(point,x)==x and (lambda x,y:y)(x,point)==point for x in range(4))
    out["right_projection_chain4_all_four_points"] = {"printed_four_equations":True,"L_algebra":False}
    path=Path(__file__).with_name("STRUCTURAL_CHECKS_RESULTS.json")
    path.write_text(json.dumps(out,indent=2)+"\n")
    print(json.dumps({"status":"passed","named_target_models":5,"separation_counterexamples":2,"result_file":path.name},indent=2))


if __name__ == "__main__":
    main()
