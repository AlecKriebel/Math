#!/usr/bin/env python3
"""Independent high-precision diagnostics from Cartesian orbit vertices only.

No submitted U/q coordinate formula or supplied checker is called. Diagnostics
cannot replace the universal arguments in INDEPENDENT_DERIVATION.md.
"""
from pathlib import Path
import json, math, time
import mpmath as mp
mp.mp.dps=180
TOL=mp.mpf('1e-80')
def dot(u,v):return u[0]*v[0]+u[1]*v[1]
def det(u,v):return u[0]*v[1]-u[1]*v[0]
def add(u,v):return (u[0]+v[0],u[1]+v[1])
def sub(u,v):return (u[0]-v[0],u[1]-v[1])
def mul(c,v):return (c*v[0],c*v[1])
def norm(v):return mp.sqrt(dot(v,v))
def area(poly):return mp.fsum(det(poly[j],poly[(j+1)%len(poly)]) for j in range(len(poly)))/2
maxima={};checks=0
def equal(name,x,y):
    global checks
    error=abs(x-y)/max(mp.mpf(1),abs(x),abs(y))
    maxima[name]=max(maxima.get(name,mp.mpf(0)),error)
    assert error<TOL,(name,mp.nstr(error,20),mp.nstr(x,20),mp.nstr(y,20))
    checks+=1
def vec_equal(name,x,y):
    for i in range(2):equal(name,x[i],y[i])
def points(k,N,tau,phase):
    K=mp.ellipk(k*k);b0=mp.sqrt(1-k*k);v=2*K*tau/N
    a=mp.ellipfun('dn',v,k*k)/mp.ellipfun('cn',v,k*k)
    b=b0/mp.ellipfun('cn',v,k*k);w=phase*K
    P=[(-a*mp.ellipfun('sn',w+j*2*v,k*k),b*mp.ellipfun('cn',w+j*2*v,k*k)) for j in range(N)]
    return P,a,b,b0,K,v,w
def geometry(k,N,tau,phase):
    P,a,b,b0,K,v,w=points(k,N,tau,phase)
    pedal={1:[], -1:[]};anti={1:[],-1:[]};contacts=[]
    min_focal_det=mp.inf;min_edge_area=mp.inf
    winding=mp.mpf(0)
    for j,p in enumerate(P):
        pp=P[(j+1)%N];pm=P[(j-1)%N]
        edge=sub(pp,p);normal=(-edge[1],edge[0]);gamma=dot(normal,p)
        equal('actual side caustic tangency',normal[0]**2+b0*b0*normal[1]**2,gamma**2)
        contact=(normal[0]/gamma,b0*b0*normal[1]/gamma);contacts.append(contact)
        # Contact lies inside the segment, not only its full line.
        contact_fraction=dot(sub(contact,p),edge)/dot(edge,edge)
        assert 0<contact_fraction<1
        inc=mul(1/norm(sub(p,pm)),sub(p,pm));out=mul(1/norm(edge),edge)
        outer_normal=(p[0]/(a*a),p[1]/(b*b))
        reflected=sub(inc,mul(2*dot(inc,outer_normal)/dot(outer_normal,outer_normal),outer_normal))
        vec_equal('actual specular reflection',out,reflected)
        equal('outer ellipse membership',p[0]**2/a**2+p[1]**2/b**2,1)
        equal('confocality',a*a-b*b,k*k)
        winding+=mp.atan2(det(p,pp),dot(p,pp))
        for fi in [1,-1]:
            focus=(fi*k,mp.mpf(0));r=sub(p,focus);r2=sub(pp,focus)
            den=det(r,r2);min_focal_det=min(min_focal_det,abs(den))
            assert den>0
            c1=dot(r,p);c2=dot(r2,pp)
            u=((c1*r2[1]-c2*r[1])/den,(r[0]*c2-r2[0]*c1)/den)
            vec_equal('actual focal antipedal line intersection residual', (dot(r,sub(u,p)),dot(r2,sub(u,pp))),(0,0))
            q=add(p,mul(dot(sub(focus,p),edge)/dot(edge,edge),edge))
            equal('actual focal pedal perpendicularity',dot(sub(q,focus),edge),0)
            equal('actual focal pedal on side',det(sub(q,p),edge),0)
            equal('focal pedal circle locus',dot(q,q),1)
            anti[fi].append(u);pedal[fi].append(q)
    equal('least orbit winding number',winding/(2*mp.pi),tau)
    # Closure and primitive separation are diagnosed; their proof is arithmetic.
    for j in range(N):
        assert norm(sub(P[j],P[(j+1)%N]))>0
    As={};Bs={}
    for fi in [1,-1]:
        focus=(fi*k,mp.mpf(0));Q=pedal[fi];U=anti[fi]
        for j in range(N):
            value=det(sub(Q[j],focus),sub(Q[(j+1)%N],focus))
            assert value>0
            min_edge_area=min(min_edge_area,value)
        As[fi]=area(Q);Bs[fi]=area(U)
        equal('pedal translation-invariant area',As[fi],area([sub(q,focus) for q in Q]))
        equal('reversal negates pedal area',area(list(reversed(Q))),-As[fi])
        equal('reversal negates antipedal area',area(list(reversed(U))),-Bs[fi])
        equal('threefold repetition scales pedal area',area(Q*3),3*As[fi])
        equal('threefold repetition scales antipedal area',area(U*3),3*Bs[fi])
    equal('opposite foci pedal equality',As[1],As[-1])
    equal('opposite foci antipedal equality',Bs[1],Bs[-1])
    return {'ratio':Bs[1]/As[1],'anti_over_original':Bs[1]/area(P),'pedal_over_original':As[1]/area(P),'min_focal_det':min_focal_det,'min_pedal_edge_det':min_edge_area,'a':a,'b':b}

start=time.time();families=[];phases=[mp.mpf('0'),mp.mpf('0.371'),mp.mpf('1.253')]
ks=[mp.mpf('1e-25'),mp.mpf('0.2'),mp.mpf('0.731'),mp.mpf('0.999999'),1-mp.mpf('1e-40')]
for N in [6,10,14,22,46]:
    permitted=[j for j in range(1,N//2) if math.gcd(j,N)==1]
    winds=sorted(set([permitted[0],permitted[len(permitted)//2],permitted[-1]]))
    for tau in winds:
        for k in ks:
            rows=[geometry(k,N,tau,phase) for phase in phases]
            for row in rows[1:]:
                equal('requested k404 ratio across phase',row['ratio'],rows[0]['ratio'])
                equal('all-even antipedal-original ratio across phase',row['anti_over_original'],rows[0]['anti_over_original'])
                equal('requested pedal-original ratio across phase',row['pedal_over_original'],rows[0]['pedal_over_original'])
            families.append({'k':mp.nstr(k,50),'N':N,'tau':tau,'phases':len(phases),'ratio':mp.nstr(rows[0]['ratio'],40),'a':mp.nstr(rows[0]['a'],30),'b':mp.nstr(rows[0]['b'],30),'minimum_positive_focal_det':mp.nstr(min(row['min_focal_det'] for row in rows),30),'minimum_positive_pedal_edge_det':mp.nstr(min(row['min_pedal_edge_det'] for row in rows),30)})

# Large-period checks add a control with high winding and an extreme caustic.
for k,N,tau in [(mp.mpf('0.731'),202,99),(1-mp.mpf('1e-40'),102,49)]:
    rows=[geometry(k,N,tau,phase) for phase in phases]
    for row in rows[1:]:equal('large-period requested ratio',row['ratio'],rows[0]['ratio'])
    families.append({'k':mp.nstr(k,50),'N':N,'tau':tau,'phases':len(phases),'ratio':mp.nstr(rows[0]['ratio'],40),'large_period':True})

# Deliberately excluded parity: the claimed extension is false in general.
negative=[]
for N,tau in [(4,1),(8,1),(8,3),(12,5)]:
    k=mp.mpf('0.731');rows=[geometry(k,N,tau,phase) for phase in phases]
    variation=max(abs(row['ratio']-rows[0]['ratio']) for row in rows[1:])
    assert variation>mp.mpf('1e-8')
    for row in rows[1:]:equal('excluded parity still antipedal-original invariant',row['anti_over_original'],rows[0]['anti_over_original'])
    negative.append({'N':N,'tau':tau,'k':'0.731','k404_ratio_phase_variation':mp.nstr(variation,30),'extension_rejected':True})

result={'status':'PASS','decimal_precision':mp.mp.dps,'relative_tolerance':str(TOL),'numeric_assertion_count':checks,'family_count':len(families),'family_phase_count':len(families)*len(phases),'families':families,'excluded_parity_controls':negative,'max_relative_errors':{k:mp.nstr(v,12) for k,v in maxima.items()},'elapsed_seconds':time.time()-start,'limitations':'All floating tests are diagnostics. No periodic analytic theorem is inferred from finite samples.'}
Path(__file__).with_name('CARTESIAN_NUMERIC_CHECKS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:result[k] for k in ['status','family_count','family_phase_count','numeric_assertion_count','elapsed_seconds']}))
