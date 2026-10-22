#!/usr/bin/env python3
"""Independent reverse-challenge computations; standard library only.
The source claim and universal scope are assessed in REPORT.md.
This script checks the class-level countermodel and concrete formula mapping.
It never writes into the authenticated sibling or initial-seal directories.
"""
from itertools import product
from pathlib import Path
import json

def check_chain_countermodel():
    names = ["0", "a", "b", "e"]
    values = range(4)
    table = [[3,3,3,3], [0,3,3,3], [0,0,3,3], [0,1,2,3]]
    imp = lambda x,y: table[x][y]
    pairs = list(product(values,repeat=2))
    triples = list(product(values,repeat=3))
    # Direct quantified H3 check from Definition 1.2, not the equivalent equation.
    h3_bad = [(p,q,r) for p,q,r in triples
              if p <= imp(q,r) and min(p,q) > r]
    laws = {
      "H1_meet_semilattice_with_top": True,
      "H2_diagonal": all(imp(x,x)==3 for x in values),
      "H3_direct_conditional": not h3_bad,
      "H4": all(imp(x,min(x,y))==imp(x,y) for x,y in pairs),
      "top_left_unit": all(imp(3,x)==x for x in values),
      "top_right_absorber": all(imp(x,3)==3 for x in values),
      "order_iff_imp_top": all((imp(x,y)==3)==(x<=y) for x,y in pairs),
      "separation": all((not(imp(x,y)==3 and imp(y,x)==3)) or x==y for x,y in pairs),
      "S1_meet_preservation": all(imp(x,min(y,z))==min(imp(x,y),imp(x,z)) for x,y,z in triples),
    }
    cycloid_bad = [(x,y,z) for x,y,z in triples
      if imp(imp(x,y),imp(x,z)) != imp(imp(y,x),imp(y,z))]
    mixed_bad = [(x,y,z) for x,y,z in triples
      if imp(min(x,y),z) != imp(imp(x,y),imp(x,z))]
    if not all(laws.values()) or not cycloid_bad or not mixed_bad:
        raise RuntimeError("Countermodel did not support claimed separation")
    x,y,z=1,2,0
    witness={"x":names[x],"y":names[y],"z":names[z],
      "cycloid_left":names[imp(imp(x,y),imp(x,z))],
      "cycloid_right":names[imp(imp(y,x),imp(y,z))]}
    if witness["cycloid_left"]!="0" or witness["cycloid_right"]!="e":
        raise RuntimeError("Named witness mismatch")
    return {"table":table,"passed_laws":laws,"cycloid_failures":len(cycloid_bad),
       "mixed_failures":len(mixed_bad),"named_witness":witness}

def check_old_exact_formula():
    records=[]
    models=[
      ("singleton",[0],lambda x,y:0,0),
      ("chain4",list(range(4)),min,3),
      ("Boolean4",list(range(4)),lambda x,y:x&y,3),
      ("M3",list(range(5)),lambda x,y:x if x==y else y if x==4 else x if y==4 else 0,4),
      ("N5",list(range(5)),lambda x,y: x if x==y else y if x==4 else x if y==4 else min(x,y) if x in [0,1,2] and y in [0,1,2] else 0,4)
    ]
    for name,els,meet,e in models:
        source_operation=lambda a,b:e if meet(a,b)==a else meet(a,b)
        admitted_operation=lambda x,y:e if meet(x,y)==x else meet(x,y)
        points=list(product(els,repeat=2));triples=list(product(els,repeat=3))
        identities={
          "literal_operations_equal": all(source_operation(x,y)==admitted_operation(x,y) for x,y in points),
          "S1": all(source_operation(x,meet(y,z))==meet(source_operation(x,y),source_operation(x,z)) for x,y,z in triples),
          "S3": all(source_operation(meet(x,y),z)==source_operation(source_operation(x,y),source_operation(x,z)) for x,y,z in triples),
          "cycloid": all(source_operation(source_operation(x,y),source_operation(x,z))==source_operation(source_operation(y,x),source_operation(y,z)) for x,y,z in triples)
        }
        if not all(identities.values()):raise RuntimeError("Formula check failed: "+name)
        records.append({"model":name,**identities})
    # A no-bottom domain has unboundedly descending nonpositive integers with top0.
    # This is a finite consistency sample, not a proof of its infinite laws.
    sample=list(range(-8,1))
    op=lambda a,b:0 if a<=b else min(a,b)
    no_bottom_sample={
      "mathematical_domain":"all integers <=0, meet=min, greatest0, no least element",
      "sample":sample,
      "S1_sample":all(op(x,min(y,z))==min(op(x,y),op(x,z)) for x,y,z in product(sample,repeat=3)),
      "S3_sample":all(op(min(x,y),z)==op(op(x,y),op(x,z)) for x,y,z in product(sample,repeat=3)),
      "limitation":"Finite sample does not establish infinitude or universal laws; written domain argument in report does."
    }
    return {"finite_models":records,"no_bottom_domain_sample":no_bottom_sample}

def main():
    result={"chain_countermodel":check_chain_countermodel(),
            "old_exact_formula":check_old_exact_formula(),
            "historical_inference":"Computations establish no novelty or priority."}
    out=Path(__file__).with_name("CROSS_CHECKS_RESULTS.json")
    out.write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps({"countermodel_verified":True,"exact_formula_models":5,
                     "result_file":out.name},indent=2))
if __name__=="__main__":
    main()

