"""Independent bounded verification of the deposited truncated initial data.

Imports only this worker's inspected code, not deposited verification programs.
"""
from pathlib import Path
from datetime import datetime, timezone
import json
import runpy
import sympy as s

HERE=Path(__file__).resolve().parent


if __name__=="__main__":
    own=runpy.run_path(str(HERE/"checks.py"))
    certificate=json.loads((own["SOURCE"]/"published-source/audits/exact_reproduction_audit_01/ORTHOGONAL_CERTIFICATE.json").read_text())
    C=s.Matrix(certificate["GL4_control_matrix"])
    variables=s.symbols("p q r t")
    reports=[]
    for item in certificate["initial_ideal_controls"]:
        n=item["variables"];v=variables[:n]
        forms=[sum(C[i,j]*v[j] for j in range(n)) for i in range(4)]
        polars=own["restricted"](forms)
        minimal=[];degrees=[]
        for degree in (6,7):
            M,powers=own["macaulay"](polars,v,degree,grevlex=True)
            _,pivots=M.rref()
            leads=[powers[p] for p in pivots]
            new=[e for e in leads if not any(all(x<=y for x,y in zip(old,e)) for old in minimal)]
            minimal.extend(new)
            degrees.append({"degree":degree,"rank":len(pivots),"new_minimal_leading_monomials":[list(e) for e in new]})
        assert degrees==item["degrees"]
        reports.append({"variables":n,"degrees":degrees,"verified_scope":"Ordinary initial ideal through degree7 at this rational coordinate change, not full gin."})
    # Independently verify the characteristic-seven rank control by modular elimination.
    a,b,c=own["a"],own["b"],own["c"]
    polars=own["restricted"]((a,b,c,a+2*b+3*c))
    M,_=own["macaulay"](polars,(a,b,c),7)
    rows=[[int(q)%7 for q in row] for row in M.tolist()]
    piv=0
    for col in range(M.cols):
        found=next((i for i in range(piv,M.rows) if rows[i][col]),None)
        if found is None:continue
        rows[piv],rows[found]=rows[found],rows[piv]
        unit=pow(rows[piv][col],-1,7)
        rows[piv]=[(unit*q)%7 for q in rows[piv]]
        for i in range(M.rows):
            if i!=piv:
                multiplier=rows[i][col]
                rows[i]=[(q-multiplier*r)%7 for q,r in zip(rows[i],rows[piv])]
        piv+=1
        if piv==M.rows:break
    assert piv==11==certificate["characteristic7_original_ternary_degree7_rank"]
    target=HERE/"FINITE_INITIAL_SCOPE_CONTROLS.json"
    if target.exists():raise RuntimeError("Refusing evidence overwrite")
    target.write_text(json.dumps({"utc":datetime.now(timezone.utc).isoformat(),"status":"ALL_REQUESTED_SCOPE_ASSERTIONS_PASS",
                                  "exact_initial_through_degree7":reports,"characteristic7_degree7_rank":piv,
                                  "no_generic_initial_open_claim_from_finite_coordinates":True,
                                  "original_programs_executed":False},indent=2)+"\n")
    print("Two rational truncated initial records and characteristic7 rank independently verified.")
