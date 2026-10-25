"""Independent reconstruction from manuscript tables, before submitted helpers.

No imports or code copied from the publication package. Uses normal-coordinate
linearization (Ldot,Qdot), instead of a 3x3 characteristic-polynomial expansion.
"""
from pathlib import Path
from datetime import datetime, timezone
import json, hashlib, math
import sympy as S

ROOT=Path(__file__).resolve().parent
x,y,z,w,t=S.symbols('x y z w t')
a,b,c,d,h,s=S.symbols('a b c d h s')
C=[(0,0,0),(0,0,1),(0,0,3),(0,1,1),(0,3,0),(1,0,1),(1,1,0),(1,1,1),(2,1,0),(3,0,0)]
edges=[(0,1),(0,4),(0,6),(1,7),(2,4),(2,7),(2,9),(3,4),(5,9),(8,9)]
arcs=[p for e in edges for p in [e,e[::-1]]]
mon=[x**i*y**j*z**k for i,j,k in C]
units=[S.Matrix([C[v][i]-C[u][i] for i in range(3)])*mon[u] for u,v in arcs]
rates=S.Matrix([(62*d-15*c)/48,33*(58*d-45*c)/160,16*d/15,(c-b)/3,(154*d-221*c)/224,(9856*d-3315*c)/1470,45*(154*d-221*c)/3136,5*c/14,(15*a+16*d)/15,(62*d-15*b-15*c)/45,(154*d-192*a-221*c)/64,11*(58*d-45*c)/60,a,2*(31*d-15*c)/45,88*d/15,b,88*d/15,c,33*d/5,d])
L=z-x-y+1
Q=7*x*x-2*x*y-16*x+7*y*y-16*y+16
G=S.groebner([L,Q],z,y,x,order='lex',domain=S.QQ)
basis=[1,x,y,x*x,x*y,x**3,x*x*y]
cols=[]
for u in units:
    cols.append(S.Matrix([S.Poly(G.reduce(f)[1],x,y).coeff_monomial(m) for f in u for m in basis]))
M=S.Matrix.hstack(*cols)
assert M.shape==(21,20) and M.rank()==16
assert M*rates==S.zeros(21,1)
assert rates.jacobian([a,b,c,d]).rank()==4
rows=[0,1,2,4,5,6,7,8,9,12,13,14,15,16,18,19]
cc=[0,1,2,3,4,5,6,7,8,9,10,11,13,14,16,18]
minor=M.extract(rows,cc).det()
assert minor==S.Rational(7255941120,823543)
cone=[S.expand(r.subs({c:b+h,d:(192*a+221*(b+h)+s)/154},simultaneous=True)) for r in rates]
cone_coeff=[[f.coeff(v) for v in [a,b,h,s]] for f in cone]
assert all(all(q>=0 for q in row) and any(q>0 for q in row) for row in cone_coeff)
dt=t*t-t+1
param={x:(t*t+3)/(2*dt),y:(3*t*t+1)/(2*dt),z:(t*t+t+1)/dt}
assert all(S.cancel(f.subs(param))==0 for f in [L,Q])
assert S.factor(S.diff(param[z],t))==S.factor(2*(1-t*t)/dt**2)
assert S.Matrix([[7,-1,-8],[-1,7,-8],[-8,-8,16]]).det()==-256
out={'started_utc':datetime.now(timezone.utc).isoformat(),'sympy':S.__version__,'graph':{'complexes':len(C),'directed_arcs':len(arcs),'connected':True,'stoichiometric_rank':S.Matrix.hstack(*[S.Matrix(C[v])-S.Matrix(C[u]) for u,v in arcs]).rank()},'family':{'matrix_shape':list(M.shape),'rank':M.rank(),'minor':str(minor),'cone_coefficients':[[str(v) for v in row] for row in cone_coeff]},'cases':{}}
case_rates={'clean':(653,1,70,915),'frozen':(3920,3920,15680,658560)}
T=5399367*t**4+1602005*t**3+11579010*t*t+1602005*t+6979911
N=5730530769*t**8+20026244073*t**7+29613209084*t**6+118245415239*t**5-38238695578*t**4+127692520263*t**3-127590858244*t*t+10579139049*t-79465564719
E=31399532062137*t**8+25149913538286*t**7+139213446954293*t**6+100751092465458*t**5+199590946186248*t**4+109518436416306*t**3+114191722124597*t*t+26510727150318*t+17568656198073

for label,values in case_rates.items():
    rr=list(rates.subs(dict(zip([a,b,c,d],values))))
    assert all(r>0 and r.q==1 for r in rr)
    F=sum((u*r for u,r in zip(units,rr)),S.zeros(3,1)).applyfunc(S.expand)
    assert all(S.cancel(f.subs(param))==0 for f in F)
    pairgcd=[S.gcd(F[i],F[j]) for i,j in [(0,1),(0,2),(1,2)]]
    assert all(S.Poly(f,x,y,z).total_degree()==0 for f in pairgcd)
    fh=[S.Poly(f,x,y,z).homogenize(w).as_expr() for f in F]
    assert S.Poly(S.gcd(S.gcd(fh[0],fh[1]),fh[2]),x,y,z,w).total_degree()==0
    J=F.jacobian([x,y,z]);rank=J.subs({x:S.Rational(3,2),y:S.Rational(1,2),z:1}).rank();assert rank==2
    # Division by L first, then Q/7 in y gives explicit F=uL+vQ.
    U=[];V=[]
    for f in F:
        uq,rem=S.div(f,L,z)
        vq,rem2=S.div(rem,Q,y)
        assert S.expand(rem2)==0
        U.append(uq);V.append(vq)
    A=S.Matrix([[S.diff(g,v) for v in [x,y,z]] for g in [L,Q]])*S.Matrix.hstack(S.Matrix(U),S.Matrix(V))
    Ap=A.subs(param).applyfunc(S.cancel)
    trace=S.factor(S.trace(Ap));det=S.factor(Ap.det());disc=S.factor(trace**2-4*det)
    result={'rates':[int(r) for r in rr],'field':[str(f) for f in F],'max':int(max(rr)),'sum':int(sum(rr)),'primitive':math.gcd(*[int(r) for r in rr]),'pairwise_gcds':[str(g) for g in pairgcd],'homogeneous_gcd_one':True,'rank_at_t0':rank,'normal_trace':str(trace),'normal_det':str(det),'normal_discriminant':str(disc),'edge01_net_flux_at_t0':str(rr[0]-rr[1])}
    if label=='frozen':
        assert S.cancel(trace+8*T/dt**2)==0
        assert S.cancel(det+6272*N/dt**4)==0
        assert S.cancel(disc-64*E/dt**4)==0
        counts={k:int(S.Poly(f,t).count_roots(-S.oo,S.oo)) for k,f in [('T',T),('N',N),('E',E)]}
        assert counts=={'T':0,'N':2,'E':0}
        assert S.Poly(N,t).count_roots(-4,-3)==1 and S.Poly(N,t).count_roots(S.Rational(9,10),1)==1
        assert T.subs(t,0)>0 and E.subs(t,0)>0
        assert [S.sign(N.subs(t,k)) for k in [-4,-3,S.Rational(9,10),1]]==[1,-1,-1,1]
        result['sturm_counts']=counts
        result['normal_det_at_infinity']=str(S.limit(det,t,S.oo));assert S.limit(det,t,S.oo)<0
    if label=='clean':
        perturb=F+units[0]
        assert S.cancel(perturb[2].subs(param))==1
        result['off_family_rate01_plus1_breaks_conic']=[str(S.cancel(f.subs(param))) for f in perturb]
    out['cases'][label]=result

# Boundary controls are outside the strict-positive theorem, and really lose arrows.
edgezero_h=[S.factor(r.subs({h:0})) for r in cone]
edgezero_s=[S.factor(r.subs({s:0})) for r in cone]
assert edgezero_h[3]==0 and edgezero_s[10]==0
out['boundary_controls']={'h0_k40_zero':True,'s0_k27_zero':True,'origin_zero_field_excluded':True}
out['completed_utc']=datetime.now(timezone.utc).isoformat()
out['status']='PASS_FRESH_CONTROLS'
(ROOT/'fresh-controls.json').write_text(json.dumps(out,indent=2)+'\n')
(ROOT/'family-matrix-fresh.csv').write_text('\n'.join(','.join(map(str,M.row(i))) for i in range(M.rows))+'\n')
print(json.dumps({'status':out['status'],'family_rank':M.rank(),'clean_max_sum':[out['cases']['clean']['max'],out['cases']['clean']['sum']],'frozen_sturm':out['cases']['frozen']['sturm_counts'],'completed_utc':out['completed_utc']}))
