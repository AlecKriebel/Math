"""Independently reproduce the saved search, coverage, and every witness."""
import hashlib
import json
from pathlib import Path
import sympy as s
from audit_independent_model import horizontal_dimension, X, U, linear_normal_form
from audit_division_free import division_free_dimension

A=s.symbols('a b c')
HERE=Path(__file__).parent


def main():
    raw=(HERE/'exact_results.json').read_bytes()
    data=json.loads(raw)
    results=[]
    witnesses=[]
    for name,case in data['examples'].items():
        branches=[s.sympify(F,locals=dict(zip('xyz',X))) for F in case['branches']]
        expected=[]
        for k in range(2,case['minimum_twist']+1):
            for r in range(1,k//2+1):
                expected.append((r,k))
                if k==case['minimum_twist'] and r==case['witness_order']:
                    break
        if not (expected==[(q['r'],q['k']) for q in case['search']]):
            raise AssertionError('Audit integrity check failed')
        if not (all(q['dimension']==0 for q in case['search'][:-1])):
            raise AssertionError('Audit integrity check failed')
        if not (case['search'][-1]['dimension']>0):
            raise AssertionError('Audit integrity check failed')
        for result in case['search']:
            r,k=result['r'],result['k']
            ambient,dimension=horizontal_dimension(branches,r,k)
            if not (ambient==result['ambient_dimension'] and dimension==result['dimension']):
                raise AssertionError((name,r,k,ambient,dimension,result))
            if not (division_free_dimension(branches,r,k)==dimension):
                raise AssertionError('Audit integrity check failed')
            results.append(dict(example=name,r=r,k=k,dimension=dimension,ambient_dimension=ambient))
            if 'witness_incidence_polynomial' in result:
                P=s.sympify(result['witness_incidence_polynomial'],locals=dict(zip('xyzabc',X+A)))
                if not (P!=0):
                    raise AssertionError('Audit integrity check failed')
                for mon in s.Poly(P,*X,*A).monoms():
                    if not (sum(mon[:3])==k-2*r and sum(mon[3:])==r and not(mon[0] and mon[3])):
                        raise AssertionError('Audit integrity check failed')
                for F in branches:
                    E=P.subs(dict(zip(A,[s.diff(F,t) for t in X])),simultaneous=True)
                    if not (not linear_normal_form(E,F)):
                        raise AssertionError('Audit integrity check failed')
                x,y,z=X
                u,v,w=U
                W=s.expand(P.subs(dict(zip(A,[y*w-z*v,z*u-x*w,x*v-y*u])),simultaneous=True))
                if not (W!=0 and s.expand(sum(xx*s.diff(W,uu) for xx,uu in zip(X,U)))==0):
                    raise AssertionError('Audit integrity check failed')
                witnesses.append(dict(example=name,r=r,k=k,valid=True))
        print(name,len(case['search']),'PASS',flush=True)
    output=dict(source_sha256=hashlib.sha256(raw).hexdigest(),source_bytes=len(raw),
                examples_count=len(data['examples']),cases_count=len(results),
                method='Euler-horizontal tensors with independent sparse lex normal form, plus incidence coefficient blocks E(P)-FQ; no SymPy rem or Groebner',
                search_coverage_checked=True,independent_horizontal_tensor_checks=results,
                witnesses=witnesses)
    (HERE/'audit_saved_results.json').write_text(json.dumps(output,indent=2)+'\n')
    print('PASS',len(results),'saved cases',len(witnesses),'witnesses',flush=True)


if __name__=='__main__':
    main()
