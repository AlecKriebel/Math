#!/usr/bin/env python3
import itertools
import json
from independent_initial import require, normalize, construct, dense_path_cost, tree_paths


def evaluate(n,raw):
    if any(not c for c in raw):
        k,cleaned,route=normalize(n,raw)
        require(route=="fixed_no","empty clause mapping")
        return {"n":n,"raw":raw,"route":route,"assignment_tests":0}
    k,cleaned,route=normalize(n,raw)
    for bits in itertools.product((False,True),repeat=n):
        left=sum(not any(bits[abs(lit)-1] == (lit>0) for lit in c) for c in raw)
        if route == "fixed_yes":
            require(left==0,"tautological/all-deleted formula not universally satisfied")
        else:
            right=sum(not any(bits[abs(lit)-1] == (lit>0) for lit in c) for c in cleaned)
            require(left==right,"cleaning changed per-assignment unsatisfied count")
    return {"n":n,"raw":raw,"route":route,"assignment_tests":2**n}


def main():
    inputs=[(0,()),(0,((),)),(1,((1,-1),)),(1,((1,1,1),(-1,-1,-1))),
            (2,((1,-1,2),(-2,))),(2,((1,1,2),(-1,2,2))),
            (2,((1,),(1,),(-1,))),(3,((3,),)),(3,((1,2,3),(-1,-2,-3))),
            (3,((1,-1,2),(),(3,3,3)))]
    preprocessing=[evaluate(n,raw) for n,raw in inputs]
    # In an arbitrary n-variable formula with this single literal clause,
    # unused variables remain in the spanning tree. The dense cost table has
    # (|V|-1)*|A| relevant entries and every path is costed for its own target.
    n=16
    graph=construct(n,((1,),))
    bits=tuple(False for _ in range(n))
    chosen=tuple([edge for i in range(n) for edge in (4*i,4*i+1,4*i+3)] + [4*n])
    paths=tree_paths(graph,chosen)
    require(paths is not None and dense_path_cost(graph,paths)==1,"unused-variable witness")
    root_false=graph["edges"].index((0,2))
    z=1+3*n
    require(graph["dense"][z][root_false]==1 and graph["dense"][2][root_false]==0,
            "destination distinction on shared root arc")
    report={"preprocessing":preprocessing,"per_assignment_cleaning_checks":sum(x["assignment_tests"] for x in preprocessing),
            "empty_clause_mapping_count":sum(x["route"]=="fixed_no" for x in preprocessing),
            "unused_variable_case":{"n":n,"clauses":[[1]],"vertices":len(graph["vertices"]),"edges":len(graph["edges"]),
                                   "selected_tree_edges":len(chosen),"unshifted_cost":1,"dense_nonroot_entries":(len(graph["vertices"])-1)*len(graph["edges"]),
                                   "shared_arc":[0,2],"clause_destination_cost":1,"selector_destination_cost":0},
            "passed":True}
    with open("ADDITIONAL_ADVERSARY.json","w") as output:
        output.write(json.dumps(report,indent=2)+"\n")
    print(json.dumps({"passed":True,"per_assignment_cleaning_checks":report["per_assignment_cleaning_checks"],
                      "empty_clause_mapping_count":report["empty_clause_mapping_count"]},sort_keys=True))


if __name__ == "__main__":
    main()
