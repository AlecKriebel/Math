#!/usr/bin/env python3
"""Fresh full-witness controls using our own graph/pruning primitives.

Importing counterexample_controls deliberately reruns its 688 exact checks.
The submitted verifier is neither imported nor read by this implementation.
"""
import counterexample_controls as m
import sympy as s
from fractions import Fraction as Q
from itertools import product,permutations,combinations
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib

R=s.Rational;details={}
def bracket(coeffs,lo,hi):
    lo,hi=Q(lo),Q(hi)
    def val(z):
        y=Q(0)
        for c in coeffs:y=y*z+Q(c)
        return y
    a,b=val(lo),val(hi);m.ck(a*b<0,'root_bracket_sign')
    x=s.symbols('x');f=sum(R(c)*x**(len(coeffs)-1-i) for i,c in enumerate(coeffs))
    m.eq(s.Poly(f,x).count_roots(R(lo.numerator,lo.denominator),R(hi.numerator,hi.denominator)),1,'root_bracket_unique')
    for _ in range(220):
        mid=(lo+hi)/2;v=val(mid)
        if v*a>0:lo,a=mid,v
        else:hi,b=mid,v
    return lo,hi
def field(ext,iv):
    m.F=s.QQ.algebraic_field(*ext);m.zero=m.F.zero;m.one=m.F.one
    def bound(a):
        z=(Q(0),Q(0))
        for c in a.to_list():
            p=[u*v for u in z for v in iv];c=Q(int(c.numerator),int(c.denominator));z=min(p)+c,max(p)+c
        return z
    m.iv=bound
def vector(a):return [m.cv(x) for x in a]
def edges(K,U,V,S,T):return {k:vector(v) for k,v in {'L':K,'R':K,'D2':K,'D3':K,'U':U,'V':V,'A2':S,'A3':S,'B2':T,'B3':T}.items()}
def graphq(es,delta=(R(1,2),R(1,2))):
    ds=list(product([0,1],repeat=2));delta=vector(delta);out={}
    for lab in product(range(4),repeat=3):
        v=m.zero
        if m.xor(lab)==0:
            for sw,D in zip(ds,m.ds):
                weight=m.multiply([delta[i] if sw[i] else m.one-delta[i] for i in range(2)])
                v+=weight*m.multiply([es[e][m.xor(lab[i] for i in inds)] for e,inds in D.items()])
        out[lab]=v
    return out
def inverse(q):
    return {pat:sum((v*m.multiply([m.cv(m.chars[lab[i]][pat[i]]) for i in range(3)]) for lab,v in q.items()),m.zero)/64 for pat in product(range(4),repeat=3)}
def validate(name,es,ts,ct=False):
    q=graphq(es);p=inverse(q)
    for lab,v in q.items():m.eq(v,m.multiply([ts[i][lab[i]] for i in range(3)]) if m.xor(lab)==0 else m.zero,name+'_fourier')
    mats={k:m.trans(v) for k,v in es.items()};tm={str(i):m.trans(v) for i,v in enumerate(ts)}
    for pat,v in p.items():
        direct=sum((m.prune(g,mats,pat) for g in m.graphs),m.zero)/4
        m.eq(direct,v,name+'_state_pruning_network')
        m.eq(m.prune([('rho',str(i+1),str(i)) for i in range(3)],tm,pat),v,name+'_state_pruning_tree')
        m.ck(m.pos(v),name+'_positive_pattern')
    m.eq(sum(p.values(),m.zero),m.one,name+'_normalization')
    all_edges={**es,'E1':[es['L'][i]*es['R'][i] for i in range(4)],**{'tree'+str(i):v for i,v in enumerate(ts)}}
    ctmargins=[]
    for en,a in all_edges.items():
        for v in a[1:]:m.ck(m.pos(v) and m.pos(m.one-v),name+'_eigenvalues')
        for row in m.trans(a):
            m.eq(sum(row,m.zero),m.one,name+'_stochastic')
            for v in row:m.ck(m.pos(v),name+'_positive_entries')
        mm=[a[i]-a[j]*a[k] for i,j,k in [(1,2,3),(2,1,3),(3,1,2)]]
        if ct or en.startswith('tree'):
            for v in mm:m.ck(m.pos(v),name+'_ct_margins')
        ctmargins.append(a[2]-a[1]**2)
    print(name,'all witnesses checked',flush=True)
    return q,p,ctmargins
def labels(text):return [tuple('ACGT'.index(c) for c in w) for w in text.split()]
def jac(es,rows,cols,k2=False,delta=(R(1,2),R(1,2))):
    delta=vector(delta);switches=list(product([0,1],repeat=2));J=[]
    for lab in rows:
        row=[]
        for name,g in cols:
            value=m.zero
            for sw,D in zip(switches,m.ds):
                fs=[(e,m.xor(lab[i] for i in inds)) for e,inds in D.items()]
                if name=='delta':
                    dw=(m.one if sw[g] else -m.one)*(delta[1-g] if sw[1-g] else m.one-delta[1-g])
                    value+=dw*m.multiply([es[e][c] for e,c in fs])
                else:
                    weight=m.multiply([delta[i] if sw[i] else m.one-delta[i] for i in range(2)])
                    for j,(e,c) in enumerate(fs):
                        if e==name and (c==g or (k2 and g==1 and c==3)):
                            value+=weight*m.multiply([es[f][b] for k,(f,b) in enumerate(fs) if k!=j])
            row.append(value)
        J.append(row)
    return J
def det(A):
    A=[r[:] for r in A];answer=m.one
    for k in range(len(A)):
        piv=next((j for j in range(k,len(A)) if A[j][k]),None)
        if piv is None:return m.zero
        if piv!=k:A[k],A[piv]=A[piv],A[k];answer=-answer
        v=A[k][k];answer*=v
        for i in range(k+1,len(A)):
            f=A[i][k]/v
            for j in range(k+1,len(A)):A[i][j]-=f*A[k][j]
    return answer
r2=labels('ACC AGG CAC CCA CGT CTG GAG GCT GGA');c2=[('L',1),('L',2),('U',1),('U',2),('V',1),('V',2),('A2',1),('A2',2),('B2',1)]
r3=labels('ACC AGG ATT CAC CCA CGT CTG GAG GCT GGA GTC TAT TCG TGC TTA')
c3=[('L',1),('L',2),('L',3),('U',2),('A2',1),('A2',2),('B2',1),('B2',2),('A3',1),('A3',2),('B3',1),('B3',2),('D2',3),('D3',3),('delta',1)]
K=[1,R(1,2),R(1,2),R(1,2)];eta=s.sqrt(71)
field((eta,),bracket([1,0,-71],8,9))
es=edges(K,[1,R(4,5),R(19,30),R(4,5)],[1,R(7,240),R(239,360),R(7,240)],[1,R(1,4),R(1,2),R(1,4)],[1,R(1,3),R(1,27),R(1,3)])
ts=list(map(vector,[[1,151*eta/10224,R(107,648),151*eta/10224],[1,eta/80,R(31,240),eta/80],[1,eta/80,R(31,240),eta/80]]))
qs,ps,ms=validate('compact_k2p',es,ts)
pmin=m.cv(R(1188799,79626240));m.ck(any(v==pmin for v in ps.values()),'compact_min_attained')
for v in ps.values():m.ck(v==pmin or m.pos(v-pmin),'compact_min_bound')
d2=det(jac(es,r2,c2,True));m.eq(d2,m.cv(-R(7**2*11**2*19*107*151**2*15013,2**60*3**25*5**10)),'compact_rank_exact')
bad={k:v[:] for k,v in es.items()};bad['A3'],bad['B3']=bad['B3'],bad['A3']
m.ck(any(graphq(bad)[k]!=qs[k] for k in qs),'edge_placement_negative_control')

h=5**(-R(1,4));field((h,),bracket([5,0,0,0,-1],R(2,3),R(7,10)))
eh=edges(K,[1,h/3,h,R(1,3)],[1,h,h/3,R(1,3)],[1,3*h*h/4,R(1,4),R(3,10)],[1,R(1,4),3*h*h/4,R(3,10)])
aa=(5*h**3+h)/16;tt=h*h/4;th=list(map(vector,[[1,aa,aa,tt],[1,tt,tt,tt],[1,tt,tt,tt]]))
qh,ph,mh=validate('published_quartic_k3p',eh,th)
J3=jac(eh,r3,c3);dh=det(J3);m.eq(dh,m.cv(h*(10*h*h+1)/s.Integer(2**61*3**4*5**14)),'k3p_rank_exact')
tangent=vector([-R(3,19)*h-R(375,304)*h**3,-R(621,152)*h+R(1875,304)*h**3,0,-R(6,19)+R(60,19)*h*h,
 -R(117,304)*h+R(459,608)*h**3,-R(75,608)*h-R(195,304)*h**3,-R(255,608)*h+R(135,304)*h**3,R(9,304)*h-R(9,608)*h**3,
 -R(117,304)*h+R(459,608)*h**3,-R(75,608)*h-R(195,304)*h**3,-R(255,608)*h+R(135,304)*h**3,R(9,304)*h-R(9,608)*h**3,0,0,0])
free=jac(eh,r3,[('U',1),('V',2)])
for i in range(15):m.eq(sum((J3[i][j]*tangent[j] for j in range(15)),m.zero)+sum(free[i],m.zero),m.zero,'k3p_analytic_tangent')
der=m.one-tangent[3]*eh['U'][3];m.eq(der,m.cv((21-20*h*h)/19),'k3p_margin_derivative');m.ck(m.pos(der),'k3p_derivative_positive')
for i,j in combinations([1,2,3],2):m.ck(eh['U'][i]!=eh['U'][j],'parameter_symmetry_breaking')
for lab in qh:m.eq(qh[lab],qh[tuple({1:2,2:1}.get(i,i) for i in lab)],'published_output_k2p')
m.ck(qh[1,1,0]!=qh[3,3,0],'published_output_not_jc')
print('K3P rank and tangent checked',flush=True)

x=s.symbols('x');pol=634127002560*x**3-2160769703472*x**2+1746884136303*x-169873318739
ell=s.CRootOf(pol,1);t=s.sqrt(1423)
il=bracket([634127002560,-2160769703472,1746884136303,-169873318739],R(1073231219980,10**12),R(1073231219981,10**12))
it=bracket([1,0,-1423],37,38)
field((ell,t),(il[0]+it[0],il[1]+it[1]));m.eq(m.F.ext.as_expr(),ell+t,'primitive_element_binding')
vv=R(73394329,14503216)*ell**2-R(1453474193,248626560)*ell+R(4133719,3669120)
xx=-R(366971645,99450624)*ell**2+R(4259402513,340973568)*ell-R(42362455,5031936)
ec=edges(K,[1,R(3,4),vv,R(3,4)],[1,R(1,16),xx,R(1,16)],[1,R(1,5),R(1,2),R(1,5)],[1,R(7,30),R(1,15),R(7,30)])
pg=R(73394329,4762633008)*ell**2+R(368713223407,81645137280)*ell-R(4985775401,1204882560)
tc=list(map(vector,[[1,79/(16*t),pg/4,79/(16*t)],[1,t/480,ell/8,t/480],[1,t/480,ell/8,t/480]]))
qc,pc,mc=validate('continuous_time_k2p',ec,tc,True)
margin=m.cv(R(11,900));m.ck(any(v==margin for v in mc),'ct_min_margin_attained')
for v in mc:m.ck(v==margin or m.pos(v-margin),'ct_min_margin_bound')
lower=R(149867914232177,10**16);upper=R(149867914232311,10**16)
for v in pc.values():m.ck(m.pos(v-m.cv(lower)),'ct_pattern_lower_bound')
m.ck(any(m.pos(m.cv(upper)-v) for v in pc.values()),'ct_min_pattern_upper_bound')
dc=det(jac(ec,r2,c2,True));lo=m.cv(-R(4129735,10**28));hi=m.cv(-R(4129729,10**28))
m.ck(m.pos(dc-lo) and m.pos(hi-dc),'ct_rank_interval')
details['continuous_time_rank_coefficients']=[str(c) for c in dc.to_list()]
print('continuous-time cubic witness and rank checked',flush=True)

def invariant(q,perm=(0,1,2)):
    def get(w):return q[tuple('ACGT'.index(w[i]) for i in perm)]
    return get('AGG')*get('GAG')*get('CCA')**2-get('AAA')*get('GGA')*get('TCG')**2
child_obstructions=[]
for d3 in [0,1]:
    child=graphq(ec,(R(1,2),d3));values=[invariant(child,p) for p in permutations(range(3))]
    details['ct_child_delta3_'+str(d3)]=[[str(z) for z in m.iv(v)] for v in values]
    v,w=invariant(child),invariant(child,(0,2,1))
    child_obstructions.append(all([m.pos(v-m.cv(R('-0.0000000019200'))),m.pos(m.cv(R('-0.0000000019199'))-v),m.pos(w-m.cv(R('0.0000000034284'))),m.pos(m.cv(R('0.0000000034286'))-w)]))
m.ck(any(child_obstructions),'ct_child_leaf_order_obstruction')
details['ct_child_matching_published_bounds']=[i for i,b in enumerate(child_obstructions) if b]

# Symmetric factorization family and its nonsingular two-variable Jacobian.
a,b,c,d,u,v,w,z=s.symbols('a b c d u v w z')
MAC=(a*u+c*w)/2;MAG=(b*v+d*z)/2;MCC=(a*a+2*a*c*u*w+c*c)/4;MGG=(b*b+2*b*d*v*z+d*d)/4
MCG=(a*b*u+a*d*u*z+b*c*v*w+c*d*w)/4;MCT=(a*a*v+2*a*c*u*w+c*c*z)/4
f1=MCG**2-MAC**2*MGG;f2=MCT**2*MGG-MAG**2*MCC**2
pt={a:R(1,4),b:R(1,2),c:R(1,3),d:R(1,27),u:R(4,5),v:R(19,30),w:R(7,240),z:R(239,360)}
m.eq(s.factor(f1.subs(pt)),0,'family_equations');m.eq(s.factor(f2.subs(pt)),0,'family_equations')
dj=s.det(s.Matrix([[s.diff(f1,j) for j in [v,z]],[s.diff(f2,j) for j in [v,z]]])).subs(pt)
m.eq(dj,R(675554683609333,194995116803358720000000),'family_jacobian_exact')

result={'status':'PASS','utc':datetime.now(timezone.utc).isoformat(),'assertions_including_counterexample_checks':sum(m.counts.values()),'families':len(m.counts),'counts':dict(m.counts),'details':details,'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'limits':'Fresh exact finite checks, not a proof of the IFT, universal grafting or Zariski-density deductions.'}
Path(__file__).with_name('additional_control_results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='details'},indent=2))
