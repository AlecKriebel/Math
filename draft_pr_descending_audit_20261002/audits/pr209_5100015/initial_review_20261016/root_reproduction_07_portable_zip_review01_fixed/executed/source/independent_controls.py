#!/usr/bin/env python3
"""Independent source/domain controls for PR209 k303,b.
Does not import/run submitted code; physical tangent map, actual outer side lines,
and newly derived exact triangles. Finite diagnostics are not an all-N proof.
Run with the scientific interpreter specified in REPORT.md; output here only.
"""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, math
import sympy as sp
import mpmath as mp
ROOT=Path(__file__).resolve().parent
COUNTS={}; RESULTS={}
def ck(group, cond):
    if not bool(cond): raise AssertionError(group)
    COUNTS[group]=COUNTS.get(group,0)+1
def det(p,q): return p[0]*q[1]-p[1]*q[0]
def dot(p,q): return p[0]*q[0]+p[1]*q[1]
def area(p): return sum(det(p[i],p[(i+1)%len(p)]) for i in range(len(p)))/2
def sub(p,q): return (p[0]-q[0],p[1]-q[1])
def simp(x): return sp.simplify(sp.radsimp(x))
def line(p,q):
    # Actual line n.X=h through the two supplied points.
    n=(p[1]-q[1],q[0]-p[0]); return n,dot(n,p)
def foot(n,h,M):
    c=(h-dot(n,M))/dot(n,n);return (M[0]+c*n[0],M[1]+c*n[1])
def outer(p,a2,b2):
    rr=[]
    for i,x in enumerate(p):
        y=p[(i+1)%len(p)];n=(x[0]/a2,x[1]/b2);m=(y[0]/a2,y[1]/b2)
        d=det(n,m)
        rr.append(((m[1]-n[1])/d,(n[0]-m[0])/d))
    return rr
def actual_pedal(rr,M=(0,0)):
    # The side between R_{i-1},R_i is taken explicitly, with its inherited order.
    return [foot(*line(rr[i-1],rr[i]),M) for i in range(len(rr))]

# Independently derived axis-symmetric 3-periodics for E: x^2/4+y^2=1.
# At (x,y), incoming from (2,0), outgoing vertically down: reflection reduces
# to y(3x-8)=x*sqrt((x-2)^2+y^2). Squaring factors as below, and the selected
# negative root satisfies the unsquared equation. The vertical version follows
# by swapping semiaxes, without use of the submitted six-period fixtures.
x=sp.symbols('x');y2=1-x*x/4
reflection_poly=sp.factor(y2*(3*x-8)**2-x*x*((x-2)**2+y2))
ck('exact_reflection_factorization',reflection_poly==-(x-2)**2*(3*x*x-4*x-16))
s=sp.sqrt(13);h=(sp.Integer(2)-2*s)/3;hy=sp.sqrt(1-h*h/4)
v=(s-4)/3;vx=2*sp.sqrt(1-v*v)
H=[(sp.Integer(2),sp.Integer(0)),(h,hy),(h,-hy)]
V=[(sp.Integer(0),sp.Integer(1)),(-vx,v),(vx,v)]
lam=simp(4-h*h); alpha2=4-lam;beta2=1-lam
ck('exact_caustic_range',lam>0 and lam<1)
ck('exact_common_caustic',simp(1-v*v-lam)==0)
ck('exact_unsquared_reflection_H',simp(hy*(3*h-8)-h*sp.sqrt((h-2)**2+hy*hy))==0)
exact=[]; chord_mutant=[]; offcenter=[]
for p in [H,V]:
    for i,P in enumerate(p):
        Q=p[(i+1)%3]
        ck('exact_boundary',simp(P[0]*P[0]/4+P[1]*P[1]-1)==0)
        n,c=line(P,Q)
        ck('exact_caustic_line_tangency',simp(alpha2*n[0]**2+beta2*n[1]**2-c*c)==0)
    rr=outer(p,sp.Integer(4),sp.Integer(1));qq=actual_pedal(rr)
    for i in range(3):
        n=(p[i][0]/4,p[i][1])
        ck('exact_actual_outer_sideline',simp(dot(n,rr[i])-1)==0 and simp(dot(n,rr[i-1])-1)==0)
        ck('exact_actual_foot',simp(dot(n,qq[i])-1)==0 and simp(det(n,qq[i]))==0)
    ap=simp(area(rr));aq=simp(area(qq));prod=simp(ap*aq)
    exact.append({'outer_area':str(ap),'pedal_area':str(aq),'product':str(prod)})
    # Reversal, cyclic shift and repeated listed periods are exact geometry checks.
    for shift in [1,2]:
        pp=p[shift:]+p[:shift];ss=outer(pp,sp.Integer(4),sp.Integer(1))
        ck('exact_cyclic_order',simp(area(ss)*area(actual_pedal(ss))-prod)==0)
    rev=outer(list(reversed(p)),sp.Integer(4),sp.Integer(1))
    ck('exact_reversal',simp(area(rev)+ap)==0 and simp(area(actual_pedal(rev))+aq)==0)
    for repeat in [2,3,6]:
        pp=p*repeat;ss=outer(pp,sp.Integer(4),sp.Integer(1))
        ck('exact_repetition_scaling',simp(area(ss)*area(actual_pedal(ss))-repeat**2*prod)==0)
    chordfeet=[foot(*line(p[i],p[(i+1)%3]),(0,0)) for i in range(3)]
    chord_mutant.append(simp(ap*area(chordfeet)))
    offcenter.append(simp(ap*area(actual_pedal(rr,(sp.Rational(1,3),sp.Rational(1,5))))))
ck('exact_three_period_product_match',simp(sp.sympify(exact[0]['product'])-sp.sympify(exact[1]['product']))==0)
ck('mutant_original_chord_pedal_wrong_target_value',simp(chord_mutant[0]-sp.sympify(exact[0]['product']))!=0)
RESULTS['wrong_chord_pedal_constancy_survives_exact_triangle_pair']=bool(simp(chord_mutant[0]-chord_mutant[1])==0)
ck('mutant_odd_offcenter_killed',simp(offcenter[0]-offcenter[1])!=0)
RESULTS['exact_three_period']={'ellipse_axes':[2,1],'lambda':str(lam),'phases':exact,'wrong_chord_pedal_products':list(map(str,chord_mutant)),'offcenter_products':list(map(str,offcenter))}
# Excluded 4-period pair is constructed from a4,b3: the axis diamond and
# the confocal-billiard rectangle (corners 16/5,9/5) share lambda=144/25.
a2=sp.Integer(16);b2=sp.Integer(9);L4=sp.Rational(144,25)
F4=[(sp.Integer(4),0),(0,sp.Integer(3)),(-sp.Integer(4),0),(0,-sp.Integer(3))]
G4=[(sp.Rational(16,5),sp.Rational(9,5)),(-sp.Rational(16,5),sp.Rational(9,5)),(-sp.Rational(16,5),-sp.Rational(9,5)),(sp.Rational(16,5),-sp.Rational(9,5))]
products4=[]
for p in [F4,G4]:
    for i in range(4):
        n,c=line(p[i],p[(i+1)%4]);ck('exact_excluded_four_common_caustic',simp((a2-L4)*n[0]**2+(b2-L4)*n[1]**2-c*c)==0)
    rr=outer(p,a2,b2);products4.append(simp(area(rr)*area(actual_pedal(rr))))
ck('mutant_drop_parity_killed',products4==[1152,1250])
RESULTS['excluded_four_period_products']=list(map(str,products4))

# Physical billiard advance: draw both tangents to the actual confocal caustic,
# intersect the chosen ray with E, choose positive polar advance. No Jacobi
# functions or submitted trace formulas are used in these diagnostics.
mp.mp.dps=85
max_scaled=mp.mpf(0)
def close(group,x,y,tol=mp.mpf('1e-52')):
    global max_scaled
    e=abs(x-y)/max(mp.mpf(1),abs(x),abs(y));max_scaled=max(max_scaled,e)
    ck(group,e<tol)
def advance(P,a,b,L):
    al=mp.sqrt(a*a-L);be=mp.sqrt(b*b-L)
    r=(P[0]/al,P[1]/be);rr=dot(r,r);t=mp.sqrt(rr-1)
    for sign in [1,-1]:
        q=((r[0]-sign*r[1]*t)/rr,(r[1]+sign*r[0]*t)/rr)
        B=(al*q[0],be*q[1]);d=sub(B,P)
        z=-2*(P[0]*d[0]/(a*a)+P[1]*d[1]/(b*b))/(d[0]**2/(a*a)+d[1]**2/(b*b))
        Q=(P[0]+z*d[0],P[1]+z*d[1])
        if det(P,Q)>0: return Q
    raise AssertionError('no positive orientation tangent')
def orbit(t,a,b,L,N):
    P=(a*mp.cos(t),b*mp.sin(t));pp=[];total=mp.mpf(0)
    for i in range(N):
        pp.append(P);Q=advance(P,a,b,L);total+=mp.atan2(det(P,Q),dot(P,Q));P=Q
    return pp,P,total
def find_lambda(a,b,N,tau):
    lo=mp.mpf('1e-70');hi=b*b*(1-mp.mpf('1e-70'));target=2*mp.pi*tau
    for _ in range(250):
        mid=(lo+hi)/2;total=orbit(mp.mpf(0),a,b,mid,N)[2]
        if total<target:lo=mid
        else:hi=mid
    return (lo+hi)/2
families=[]
for astr,bstr,N,tau in [('2','1',3,1),('2','1',5,1),('2','1',5,2),('2','1',6,1),('2','1',7,2),('2','1',7,3),('2','1',10,3),('2','1',14,5),('1.001','1',9,4),('5','1',10,3)]:
    a=mp.mpf(astr);b=mp.mpf(bstr);L=find_lambda(a,b,N,tau);vals=[];wrong=[];sortvals=[];parallel_margin=mp.inf
    for tstr in ['0.117','0.709','1.221','2.031']:
        t=mp.mpf(tstr);pp,end,total=orbit(t,a,b,L,N)
        close('physical_closure_x',end[0],pp[0][0]);close('physical_closure_y',end[1],pp[0][1]);close('physical_winding',total,2*mp.pi*tau)
        for i,P in enumerate(pp):
            Q=pp[(i+1)%N];n,c=line(P,Q)
            close('physical_confocal_tangency',(a*a-L)*n[0]**2+(b*b-L)*n[1]**2,c*c)
            close('physical_boundary',P[0]**2/a**2+P[1]**2/b**2,1)
            parallel_margin=min(parallel_margin,abs(det((P[0]/a**2,P[1]/b**2),(Q[0]/a**2,Q[1]/b**2))))
        rr=outer(pp,a*a,b*b);qq=actual_pedal(rr);value=area(rr)*area(qq);vals.append(value)
        for i,Q in enumerate(qq):
            nn=(pp[i][0]/a**2,pp[i][1]/b**2)
            close('physical_actual_outer_side_foot',dot(nn,Q),1)
            close('physical_actual_outer_side_normal',det(nn,Q),0)
        # Spatial sorting is a forbidden replacement for traversal order on stars.
        sortedp=sorted(pp,key=lambda z:mp.atan2(z[1]/b,z[0]/a))
        sr=outer(sortedp,a*a,b*b);sortvals.append(area(sr)*area(actual_pedal(sr)))
        wrong.append(area(rr)*area(qq[::2]+qq[1::2]))
    for value in vals[1:]:close('physical_target_constancy',value,vals[0])
    families.append({'a':astr,'b':bstr,'N':N,'turning':tau,'lambda':mp.nstr(L,55),'target_products':[mp.nstr(v,30) for v in vals],'minimum_consecutive_tangent_determinant':mp.nstr(parallel_margin,12),'spatial_sorted_product_range':mp.nstr(max(sortvals)-min(sortvals),12),'scrambled_feet_product_range':mp.nstr(max(wrong)-min(wrong),12)})
    if tau>1: ck('mutant_spatial_sort_wrong_target_value',any(abs(sortvals[j]-vals[j])>mp.mpf('1e-20') for j in range(len(vals))))
    ck('mutant_scramble_pedal_order_wrong_target_value',any(abs(wrong[j]-vals[j])>mp.mpf('1e-20') for j in range(len(vals))))
RESULTS['physical_map_diagnostics']={'precision_digits':mp.mp.dps,'families':families,'max_scaled_error':mp.nstr(max_scaled,12),'jacobi_functions_used':False,'samples_each':4}
# Exact subgroup arithmetic includes all coprime windings up to N=99.
for N in range(3,100):
    if N%4==0:continue
    for tau in range(1,(N+1)//2):
        if math.gcd(tau,N)!=1:continue
        r=math.gcd(N,2);q=N//r
        residues=[(2*i*tau)%N for i in range(N)]
        ck('exact_group_order_and_multiplicity',len(set(residues))==q and all(residues.count(x)==r for x in set(residues)))
        ck('exact_group_q_odd',q%2==1)
        ck('exact_group_avoids_K',N%2==1 or N//2 not in residues)
RESULTS['status']='PASS';RESULTS['counts']=COUNTS;RESULTS['assertions']=sum(COUNTS.values());RESULTS['created_utc']=datetime.now(timezone.utc).isoformat();RESULTS['program_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest();RESULTS['limits']='Exact checks are finite. Physical-map samples use non-interval 85-digit arithmetic and bisection; no all-N/all-phase or rigorous numerical error certificate is claimed.'
(ROOT/'control_results.json').write_text(json.dumps(RESULTS,indent=2)+'\n')
print(json.dumps({'status':RESULTS['status'],'assertions':RESULTS['assertions'],'exact_three_period':RESULTS['exact_three_period'],'physical_families':len(families),'max_scaled_error':RESULTS['physical_map_diagnostics']['max_scaled_error']},indent=2))
