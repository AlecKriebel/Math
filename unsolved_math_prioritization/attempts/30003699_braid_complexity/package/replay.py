#!/usr/bin/env python3
"""Offline exact replay. Run with -B, normally or with -O; no network access."""
import ast, contextlib, io, json, runpy, sys
from pathlib import Path
sys.dont_write_bytecode=True
from validate import validate, require

def main():
    root=Path(__file__).resolve().parent
    validate(root)
    code=(root/'check_coefficients.py').read_text()
    require(not any(isinstance(n,ast.Assert) for n in ast.walk(ast.parse(code))), 'assert-free checker')
    out=io.StringIO()
    with contextlib.redirect_stdout(out):
        c=runpy.run_path(str(root/'check_coefficients.py'),run_name='__main__')
    require(out.getvalue().encode()==(root/'CHECKS.json').read_bytes(),'original normal output')
    require(out.getvalue().encode()==(root/'CHECKS_OPTIMIZED.json').read_bytes(),'original optimized output')
    p=c['z_method'](60);q=c['characteristic_method'](18);e=c['enumeration_method'](18)
    for route,limit in [(p,60),(q,18),(e,18)]:
        require(set(route)==set(range(1,limit+1)),'exact range')
        for n,values in route.items():
            require(type(n) is int and type(values) is list,'coefficient schema')
            require(len(values)==(1 if n==1 else (n-2)//2+1),'degree bound')
            require(all(type(x) is int and x>=0 for x in values),'exact coefficient integer')
    require(all(p[n]==q[n]==e[n] for n in range(1,19)),'three routes')
    leading={str(n):c['leading'](n) for n in range(1,61)}
    require(all(v.denominator==1 and p[int(n)][-1]==v for n,v in leading.items()),'leading')
    result={'status':'PASS','problem_id':30003699,'three_routes_range':[1,18],
            'leading_and_Z_range':[1,60],'z_coefficients':p,'characteristic_coefficients':q,
            'enumeration_coefficients':e,'leading_coefficients':{n:int(v) for n,v in leading.items()},
            'original_outputs_byte_equal':True,'assert_count':0,
            'scope':'Finite implementation checks, not a general proof or full resolution.'}
    print(json.dumps(result,indent=2))
if __name__=='__main__': main()
