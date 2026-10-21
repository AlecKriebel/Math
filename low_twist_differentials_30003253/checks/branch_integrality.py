"""Exact rational research computation and witness generator for branch-integral forms on P2.
Authored calculation; no third-party data. Requires SymPy. Not a general CAS UI.
"""
from __future__ import annotations
import json
from functools import lru_cache
from pathlib import Path
import sympy as s
from sympy.polys.matrices import DomainMatrix

X=s.symbols('x y z'); A=s.symbols('a b c')
x,y,z=X

def require(condition,message):
    if not condition:raise AssertionError(message)

@lru_cache(maxsize=128)
def validate_branches(branches):
    if not branches:
        raise ValueError('A nonempty reduced branch divisor is required')
    pp=[]
    for F in branches:
        p=s.Poly(F,*X,domain=s.QQ)
        if p.is_zero or p.total_degree()<1:
            raise ValueError('Branch equations must be nonzero and nonconstant')
        if len({sum(mon) for mon in p.monoms()})!=1:
            raise ValueError('Branch equations must be homogeneous')
        if any(mult!=1 for _,mult in p.sqf_list()[1]):
            raise ValueError('Nonreduced branch equation: repeated factor rejected')
        if any(s.gcd(p,q).total_degree()>0 for q in pp):
            raise ValueError('Branch equations have a repeated/shared component')
        pp.append(p)
    return sum(p.total_degree() for p in pp)

def monomials3(degree):
    if degree < 0: return []
    return [x**i*y**j*z**(degree-i-j) for i in range(degree+1) for j in range(degree-i+1)]

def powers3(degree):
    return [(i,j,degree-i-j) for i in range(degree+1) for j in range(degree-i+1)]

def basis(d,r):
    # Standard monomials modulo x*a+y*b+z*c with leading monomial x*a.
    return [(p,q) for p in powers3(d) for q in powers3(r) if not (p[0] and q[0])]

def pair_expr(pair):
    p,q=pair
    return s.prod(t**e for t,e in zip(X,p))*s.prod(t**e for t,e in zip(A,q))

def kernel(branches,r,k,return_form=False):
    branches=tuple(map(s.sympify,branches))
    validate_branches(branches)
    if not isinstance(r,int) or r<1 or not isinstance(k,int):
        raise ValueError('Order must be a positive integer and twist an integer')
    d=k-2*r
    if d < 0:return {'r':r,'k':k,'dimension':0,'ambient_dimension':0,'rank':0}
    bb=basis(d,r)
    rows=[]
    for F in branches:
        F=s.Poly(F,*X,domain=s.QQ).as_expr()
        grad=[s.diff(F,t) for t in X]
        GB=s.groebner([F],*X,domain=s.QQ)
        cols=[]
        mons=set()
        for p,q in bb:
            v=s.prod(t**e for t,e in zip(X,p))*s.prod(t**e for t,e in zip(grad,q))
            rem=s.Poly(GB.reduce(s.expand(v))[1],*X,domain=s.QQ).as_dict()
            mons.update(rem);cols.append(rem)
        for mon in sorted(mons):rows.append([v.get(mon,0) for v in cols])
    M=s.Matrix(rows) if rows else s.zeros(0,len(bb))
    DM=DomainMatrix.from_Matrix(M).convert_to(s.QQ)
    rr=DM.rank()
    out={'r':r,'k':k,'dimension':len(bb)-rr,'ambient_dimension':len(bb),'rank':rr,'equations':M.rows}
    require(len(bb)==(r+1)*(d+1)*(r+d+2)//2,'Incidence dimension mismatch')
    if return_form and len(bb)>rr:
        v=DM.nullspace().to_Matrix().row(0)
        P=s.expand(sum(vv*pair_expr(pair) for vv,pair in zip(v,bb)))
        out['witness_incidence_polynomial']=str(P)
        out['witness_branch_remainders']=[str(s.groebner([F],*X,domain=s.QQ).reduce(s.expand(P.subs(dict(zip(A,[s.diff(F,t) for t in X])),simultaneous=True)))[1]) for F in branches]
        require(all(t=='0' for t in out['witness_branch_remainders']),'Invalid divisibility witness')
        verify_witness(branches,r,k,P)
    return out

def verify_witness(branches,r,k,P):
    branches=tuple(map(s.sympify,branches));validate_branches(branches)
    if not isinstance(r,int) or r<1 or not isinstance(k,int) or k<2*r:
        raise ValueError('Invalid witness order or twist')
    d=k-2*r;P=s.Poly(P,*X,*A,domain=s.QQ).as_expr()
    if P==0:raise ValueError('Zero witness')
    if any(sum(mon[:3])!=d or sum(mon[3:])!=r for mon in s.Poly(P,*X,*A,domain=s.QQ).monoms()):
        raise ValueError('Witness has incorrect bidegree')
    incidence=sum(t*a for t,a in zip(X,A))
    if s.groebner([incidence],*X,*A,domain=s.QQ).reduce(P)[1]==0:
        raise ValueError('Witness represents the zero section')
    for F in branches:
        ev=s.expand(P.subs(dict(zip(A,[s.diff(F,t) for t in X])),simultaneous=True))
        if s.groebner([F],*X,domain=s.QQ).reduce(ev)[1]!=0:
            raise ValueError('Witness fails branch divisibility')
    return True

def global_minimum(branches):
    branches=tuple(map(s.sympify,branches))
    total=validate_branches(branches)
    search=[]
    for k in range(2,total+2):
        for r in range(1,k//2+1):
            result=kernel(branches,r,k,True);search.append(result)
            if result['dimension']:
                return {'branches':[str(F) for F in branches], 'total_degree':total,'minimum_twist':k,'witness_order':r,'search':search}
    raise AssertionError('Universal upper bound failed')

def main():
    tests={
      'line':[z],
      'smooth_conic':[x*z-y*y],
      'fermat_cubic':[x**3+y**3+z**3],
      'fermat_quartic':[x**4+y**4+z**4],
      'fermat_quintic':[x**5+y**5+z**5],
      'triangle':[x,y,z],
      'five_tangent_lines':[x+2*t*y+t*t*z for t in range(5)],
      'seven_tangent_lines':[x+2*t*y+t*t*z for t in range(7)],
      'five_concurrent_lines':[x-t*y for t in range(5)],
      'six_snc_lines':[x+t*y+t**3*z for t in range(1,7)],
      'two_conic_fibers':[x*x+y*y+z*z,x*x+2*y*y+3*z*z],
      'ten_snc_lines':[x+t*y+t**4*z for t in range(1,11)],
    }
    results={}
    for name,ff in tests.items():
        result=global_minimum(ff);results[name]=result
        print(name,result['minimum_twist'],result['witness_order'],flush=True)
    dest=Path(__file__).with_name('exact_results.json')
    dest.write_text(json.dumps({'coefficient_field':'QQ','sympy_version':s.__version__,'examples':results},indent=2)+'\n')
    # Structural and boundary checks; all data are authored examples.
    require(results['line']['minimum_twist']==2, 'Research control failed')
    require(results['smooth_conic']['minimum_twist']==3, 'Research control failed')
    require(results['triangle']['minimum_twist']==3, 'Research control failed')
    require(results['five_tangent_lines']['minimum_twist']==4, 'Research control failed')
    require(results['seven_tangent_lines']['minimum_twist']==4, 'Research control failed')
    require(results['five_concurrent_lines']['minimum_twist']==2, 'Research control failed')
    require(results['six_snc_lines']['minimum_twist']==5, 'Research control failed')
    require(results['two_conic_fibers']['minimum_twist']==4, 'Research control failed')
    require(results['ten_snc_lines']['minimum_twist']==7, 'Research control failed')
    # Negative controls make the mathematical preconditions executable.
    controls={}
    invalid={
      'squared_line':([z*z],2,4),
      'repeated_component':([z,z],1,2),
      'shared_component':([x*y,y*z],1,4),
      'nonhomogeneous':([x+y+1],1,2),
      'constant_branch':([s.Integer(1)],1,2),
      'empty_branch':([],1,2),
      'zero_order':([z],0,2),
    }
    for name,args in invalid.items():
        try:kernel(*args)
        except ValueError as exc:controls[name]={'rejected':True,'reason':str(exc)}
        else:raise AssertionError('Invalid input accepted: '+name)
    # Reducible squarefree equations are valid and agree with split factors.
    controls['squarefree_product_matches_split']=kernel([x*y*z],2,4)['dimension']==kernel([x,y,z],2,4)['dimension']
    require(controls['squarefree_product_matches_split'], 'Research control failed')
    transforms={'swap_x_z':{x:z,y:y,z:x},'upper_unipotent':{x:x+y,y:y+z,z:z}}
    coord=[]
    for name in ['smooth_conic','five_tangent_lines','six_snc_lines']:
        for tn,sub in transforms.items():
            ff=[s.expand(F.subs(sub,simultaneous=True)) for F in tests[name]]
            changed=global_minimum(ff)
            old=results[name]
            require(changed['minimum_twist']==old['minimum_twist'], 'Research control failed')
            require([(v['r'],v['k'],v['dimension']) for v in changed['search']]==[(v['r'],v['k'],v['dimension']) for v in old['search']], 'Research control failed')
            coord.append({'example':name,'transformation':tn,'minimum_twist':changed['minimum_twist'],'all_tested_dimensions_match':True})
    verify_witness([z],1,2,A[0])
    for name,P in {'altered_branch_witness':A[0]+A[2],'zero_incidence_witness':sum(t*a for t,a in zip(X,A))}.items():
        try:verify_witness([z],1,3 if name=='zero_incidence_witness' else 2,P)
        except ValueError as exc:controls[name]={'rejected':True,'reason':str(exc)}
        else:raise AssertionError('Invalid witness accepted: '+name)
    controls['coordinate_invariance']=coord
    Path(__file__).with_name('validation_controls.json').write_text(json.dumps(controls,indent=2)+'\n')
    print('PASS: exact minima, witnesses, input rejection, and coordinate controls')

if __name__=='__main__':main()
