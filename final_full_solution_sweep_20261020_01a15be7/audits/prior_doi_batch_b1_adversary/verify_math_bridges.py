"""Independent exact source-data and algebra checks; no candidate code execution."""
from pathlib import Path
from fractions import Fraction
import ast
import hashlib
import itertools
import json
import math

HERE=Path(__file__).resolve().parent

def need(ok,message):
    if not ok:
        raise RuntimeError(message)

def literal_pairs():
    raw=(HERE/'private_sources/pr1072_notebook.html').read_bytes()
    notebook=json.loads(raw)
    source=''.join(notebook['cells'][1]['source'])
    tree=ast.parse(source)
    nodes=[n for n in tree.body if isinstance(n,ast.Assign) and len(n.targets)==1
           and isinstance(n.targets[0],ast.Name) and n.targets[0].id=='solution']
    need(len(nodes)==1 and isinstance(nodes[0].value,ast.List),'Unique literal solution absent')
    pairs=[]
    for pair in nodes[0].value.elts:
        need(isinstance(pair,ast.Tuple) and len(pair.elts)==2,'Nonliteral source pair')
        values=[]
        for number in pair.elts:
            need(isinstance(number,ast.Call) and isinstance(number.func,ast.Attribute)
                 and isinstance(number.func.value,ast.Name) and number.func.value.id=='np'
                 and number.func.attr=='float64' and len(number.args)==1
                 and not number.keywords and isinstance(number.args[0],ast.Constant),'Nonliteral source number')
            token=ast.get_source_segment(source,number.args[0])
            values.append(Fraction(token))
        pairs.append(values)
    need(len(pairs)==15 and all(u>0 and v>0 for u,v in pairs),'Wrong source witness')
    return raw,pairs

def all_cuts(pairs):
    denominator=math.lcm(*(z.denominator for pair in pairs for z in pair))
    integers=[(int(u*denominator),int(v*denominator)) for u,v in pairs]
    demand=max(u+v for u,v in integers)
    best_all=None;best_inner=None;best_mask=None
    minima=[]
    for choices in itertools.product((0,1),repeat=len(pairs)):
        z=[v if choice else -u for (u,v),choice in zip(integers,choices)]
        total=sum(z);prefix=0;cuts=[abs(total)]
        for value in z:
            prefix+=value;cuts.append(abs(2*prefix-total))
        inner=max(cuts[1:-1])
        actual=max(cuts)
        if best_all is None or actual<best_all:
            best_all=actual;best_mask=list(choices)
        best_inner=inner if best_inner is None else min(best_inner,inner)
    # Direct loads of the particular fractional routing on the original 30-cycle.
    # Demand i uses clockwise semicircle starting at i, or its complement.
    loads=[]
    m=len(pairs)
    for edge in range(2*m):
        load=0
        for i,(u,v) in enumerate(integers):
            load+=u if (edge-i)%(2*m)<m else v
        loads.append(load)
    need(best_all is not None and best_inner is not None,'No routing enumerated')
    need(1000*best_all>1119*demand,'Normalized score does not exceed1.119')
    need(best_all==best_inner,'Endpoint cuts alter claimed witness minimum')
    need(max(loads)-min(loads)<2*demand,'Demand-capped transfer condition fails')
    return {'pairs':m,'choices':2**m,'common_decimal_denominator':denominator,
            'maximum_demand_integer':demand,'best_all_cut_integer':best_all,
            'best_interior_integer':best_inner,'normalized_minimum':str(Fraction(best_all,demand)),
            'strict_margin_over1119_over1000':str(Fraction(best_all,demand)-Fraction(1119,1000)),
            'original_split_load_range_over_D':str(Fraction(max(loads)-min(loads),demand)),
            'all_split_parts_positive':True,'maximum_demand_not_silently_rounded_to_one':True,
            'best_choice_bits':best_mask}

def main():
    raw,pairs=literal_pairs();ring=all_cuts(pairs)
    # The three all-parameter differences are factored exactly in the report.
    checks=[]
    for k in range(3,10001):
        ell,residue=divmod(k,3)
        count=[12*ell*ell-4*ell+2,12*ell*ell+4*ell+3,12*ell*ell+12*ell+6][residue]
        difference=count-k*k-1
        factor=[(3*ell-1)*(ell-1),3*ell*ell-2*ell+1,3*ell*ell+1][residue]
        need(difference==factor and difference>=0,'Finite-curve bridge count failed')
    # A one-demand control proves endpoint cuts cannot be omitted in general.
    one=[1]
    need(max(abs(2*sum(one[:k])-sum(one)) for k in range(2))==1,'Endpoint negative control')
    output={'status':'PASS','source_notebook_sha256':hashlib.sha256(raw).hexdigest(),
       'notebook_read_as_inert_JSON_AST_literals_only':True,'external_programs_imported_or_executed':False,
       'ring_loading_exact_source_data':ring,'finite_curve_arithmetic_checks':9998,
       'finite_curve_all_k_argument':'Differences are (3ell-1)(ell-1),3ell²-2ell+1,3ell²+1 for residues0,1,2; ell>=1.',
       'limits':'This verifies exact finite ring discrepancy and transfer precondition; does not run search code or enumerate all119-demand routings. Optimum transfer is a separate cited written argument. Finite curve construction is imported, not re-proved by arithmetic checks.'}
    print(json.dumps(output,indent=2))

if __name__=='__main__':main()
