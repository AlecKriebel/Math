"""Fresh exact algebra and integer search; reads only this review's field result."""
from pathlib import Path
from datetime import datetime,timezone
import sympy as S
import json
from fractions import Fraction as R

ROOT=Path(__file__).resolve().parent
x,y,z=S.symbols('x y z')
base=json.loads((ROOT/'fresh-controls.json').read_text())
L=z-x-y+1
D=y*y-y*z-y+S.Rational(7,16)*z*z-z/S.Integer(8)+S.Rational(7,16)
P=S.groebner([L,D],x,y,z,order='lex',domain=S.QQ)
out={'started_utc':datetime.now(timezone.utc).isoformat(),'radical':{}}
for label,data in base['cases'].items():
    F=[S.sympify(f,locals={'x':x,'y':y,'z':z}) for f in data['field']]
    G=S.groebner(F,x,y,z,order='lex',domain=S.QQ)
    assert len(G.polys)==3
    g0,g1,g2=[p.as_expr() for p in G.polys]
    H=S.cancel(g1/D);elim=S.cancel(g2/D)
    assert S.Poly(H,x,y,z).degree(y)==1 and S.Poly(g0,x,y,z).degree(x)==1
    Rz=S.Poly(elim,z,domain=S.QQ).monic()
    assert Rz.degree()==15
    fac=Rz.factor_list()[1]
    assert len(fac)==1 and fac[0][0].degree()==15 and fac[0][1]==1
    J=S.groebner([g0,H,elim],x,y,z,order='lex',domain=S.QQ)
    assert len(J.polys)==3
    assert J.reduce(D)[1]!=0
    assert list(S.groebner([*P,*J],x,y,z,order='lex',domain=S.QQ))==[1]
    reductions=[G.reduce(S.expand(p*q))[1] for p in P for q in J]
    assert all(r==0 for r in reductions)
    assert all(P.reduce(f)[1]==0 and J.reduce(f)[1]==0 for f in F)
    assert S.gcd(Rz,Rz.diff()).degree()==0
    # An independent finite-field irreducibility certificate search.
    modprime=None
    _,intpoly=Rz.clear_denoms()
    for prime in [19,23,29,31,37,41,43,47,53,59,61,67,71,73,79,83,89,97,101]:
        rp=S.Poly(intpoly.as_expr(),z,modulus=prime)
        if rp.degree()==15 and rp.is_irreducible:
            modprime=prime;break
    (ROOT/(label+'-fresh-groebner.txt')).write_text('\n'.join(str(p) for p in G)+'\n')
    (ROOT/(label+'-fresh-maximal-ideal.txt')).write_text('\n'.join(str(p) for p in J)+'\n')
    out['radical'][label]={'basis_length':3,'conic_plus_maximal_disjoint':True,'degree15_irreducible_over_Q':True,'separable':True,'finite_field_irreducibility_prime':modprime,'six_product_reductions_zero':True,'field_in_both_primes':True}
    print('radical',label,'PASS',modprime,flush=True)

def rate(a,b,c,d):
    return [R(62*d-15*c,48),R(33*(58*d-45*c),160),R(16*d,15),R(c-b,3),R(154*d-221*c,224),R(9856*d-3315*c,1470),R(45*(154*d-221*c),3136),R(5*c,14),R(15*a+16*d,15),R(62*d-15*b-15*c,45),R(154*d-192*a-221*c,64),R(11*(58*d-45*c),60),R(a),R(2*(31*d-15*c),45),R(88*d,15),R(b),R(88*d,15),R(c),R(33*d,5),R(d)]
ai=[8,10,12];bi=[3,9,15];fi=[i for i in range(20) if i not in ai+bi]
bestmax=None;bestsum=None;counts={'cd_tried':0,'cd_fixed_valid':0,'a_valid':0,'b_valid':0,'cd_feasible':0}
for dv in range(15,2714,15):
    for cv in range(14,dv,14):
        counts['cd_tried']+=1
        rr=rate(0,0,cv,dv)
        fixed=[rr[i] for i in fi]
        if not all(r>0 and r.denominator==1 for r in fixed):continue
        counts['cd_fixed_valid']+=1
        aa=[];bb=[]
        for av in range(1,dv):
            r=[rr[8]+av,rr[10]-3*av,R(av)]
            if all(v>0 and v.denominator==1 for v in r):aa.append((int(max(r)),int(sum(r)),av))
        for bv in range(1,cv):
            r=[rr[3]-R(bv,3),rr[9]-R(bv,3),R(bv)]
            if all(v>0 and v.denominator==1 for v in r):bb.append((int(max(r)),int(sum(r)),bv))
        counts['a_valid']+=len(aa);counts['b_valid']+=len(bb)
        if not aa or not bb:continue
        counts['cd_feasible']+=1
        am=min(aa);bm=min(bb)
        candidate=(max(int(max(fixed)),am[0],bm[0]),am[2],bm[2],cv,dv)
        if dv<1755 and (bestmax is None or candidate<bestmax):bestmax=candidate
        asum=min(aa,key=lambda r:(r[1],r[2]));bsum=min(bb,key=lambda r:(r[1],r[2]))
        candidate=(int(sum(fixed))+asum[1]+bsum[1],asum[2],bsum[2],cv,dv)
        if bestsum is None or candidate<bestsum:bestsum=candidate
assert bestmax[0]==10296 and bestsum[0]==52464
assert max(rate(653,1,70,915))==10296 and sum(rate(653,1,70,915))==52464
out['integer_optimization']={'d_max_search_upper_exclusive':1755,'d_sum_search_upper_exclusive':2714,'bestmax':bestmax,'bestsum':bestsum,'counts':counts,'mechanism':'Integer exact separability by a,b at each c,d; no submitted code or output read.'}
out['status']='PASS_FRESH_RADICAL_AND_BOUNDED_OPTIMA'
out['completed_utc']=datetime.now(timezone.utc).isoformat()
(ROOT/'fresh-radical-optimum.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out['integer_optimization']))
