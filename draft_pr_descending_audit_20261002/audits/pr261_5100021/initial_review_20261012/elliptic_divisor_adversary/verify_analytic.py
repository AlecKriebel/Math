"""Independent exact local divisor checks and standalone geometry diagnostics.
Written after candidate exposure, based on sealed independent derivation;
no earlier review artifacts or candidate receipts used.
"""
from pathlib import Path
from collections import Counter
from datetime import datetime,timezone
import json,math
import sympy as z
import mpmath as mp

counts=Counter()
def ck(value,label):
    assert value,label
    counts[label]+=1
k,l,p,q,r,s,c,d=z.symbols('k l p q r s c d')
E=1-k*k*p*p*s*s
B=l*l+k*k*q**4
C=l*l-k*k*q**4
relations=[c*c+s*s-1,d*d+k*k*s*s-1,q*q+p*p-1,r*r+k*k*p*p-1,l*l+k*k-1]
ring=z.groebner(relations,c,d,r,l,q,k,p,s,order='lex')
def zero(expression):
    top=z.fraction(z.together(expression))[0]
    return ring.reduce(z.expand(top))[1]==0
X=(k*r*r*s*s-B*s-k*q*q)/(q*q*E)
Y=c*(C-k*B*s)/(l*q*q*E)
a=r/q;b=l/q
ends=[]
for sign in [-1,1]:
    sn=(s*q*r+sign*p*c*d)/E
    cn=(c*q-sign*s*d*p*r)/E
    P=(-a*sn,b*cn)
    ends.append(P)
    ck(zero((P[0]-k)*(X-P[0])+P[1]*(Y-P[1])),'actual_antipedal_line_incidence')
    ck(zero(-s*P[0]+c*P[1]/l-1),'actual_caustic_chord_incidence')
ck(zero((ends[0][0]-k)*ends[1][1]-ends[0][1]*(ends[1][0]-k)-2*b*p*r*d*(1+k*s)/E),'normal_determinant')
qx=(k-s)/(1-k*s);qy=l*c/(1-k*s)
ck(zero(-s*qx+c*qy/l-1),'pedal_chord_incidence')
ck(zero((qx-k)*c/l-qy*(-s)),'pedal_orthogonality')
ck(zero(qx*qx+qy*qy-1),'unit_pedal_circle')
ck(zero((ends[0][0]*ends[1][1]-ends[0][1]*ends[1][0])-2*a*b*p*q*d/E),'original_crossproduct')

# Candidate H equals independently derived B; no candidate expression used below.
H=1-2*k*k*p*p+k*k*p**4
ck(zero(H-B),'candidate_H_matches_independent_B')

U={};W={}
for e in [-1,1]:
    U[e]=z.Matrix([B*(e-p)/(2*k*p*r*q**3),z.I*(e*B-p*C)/(2*k*l*p*q**3)])
    W[e]=z.Matrix([B*(e+p)/(2*k*p*r*q**3),z.I*(e*B+p*C)/(2*k*l*p*q**3)])
    # E' from the Jacobi iK' shift.
    Ep=e*2*r*q/p
    sn0=e/(k*p);cn0=-e*z.I*r/(k*p)
    resX=(k*r*r*sn0*sn0-B*sn0-k*q*q)/(q*q*Ep)
    resY=cn0*(C-k*B*sn0)/(l*q*q*Ep)
    ck(zero(resX-U[e][0]),'independent_antipedal_residue_x')
    ck(zero(resY-U[e][1]),'independent_antipedal_residue_y')
    oppX=(k*r*r*sn0*sn0+B*sn0-k*q*q)/(q*q*Ep)
    oppY=-cn0*(C+k*B*sn0)/(l*q*q*Ep)
    ck(zero(oppX-W[e][0]),'independent_antipodal_residue_x')
    ck(zero(oppY-W[e][1]),'independent_antipodal_residue_y')
def det(x,y):return x[0]*y[1]-x[1]*y[0]
ck(zero(det(U[-1],U[1])+z.I*B/(l*p*r*q*q)),'first_double_pole_coefficient')
ck(zero(det(W[-1],W[1])-z.I*B/(l*p*r*q*q)),'antipodal_double_pole_coefficient')
ck(zero(det(U[-1],U[1])+det(W[-1],W[1])),'universal_double_pole_cancellation')
for i in range(2):
    ck(zero(W[-1][i]+U[1][i]),'N4_extra_residue_pair_parallel')
    ck(zero(W[1][i]+U[-1][i]),'N4_other_extra_residue_pair_parallel')
ck(zero(det(U[1],W[-1])),'N4_extra_double_edge_zero')
ck(zero(det(W[1],U[-1])),'N4_other_extra_double_edge_zero')

# Exact pole/translation incidence combinatorics; classify every edge.
period_cases=0
for N in range(4,501,4):
    for tau in range(1,N//2):
        if math.gcd(N,tau)!=1:continue
        period_cases+=1
        m=N//2
        ck(tau%2==1 and m%2==0,'primitive_parity')
        ck({j*tau%N for j in range(N)}==set(range(N)),'full_real_quotient')
        ck(sum(j*tau%m==0 for j in range(N))==2,'trace_pole_multiplicity')
        # Vertex phase w=iK': original poles at indices 0,m. R_i=(P_i,P_{i+1}).
        singular={N-1,0,m-1,m}
        adjacent={(i,(i+1)%N) for i in singular if (i+1)%N in singular}
        ck(len(adjacent)==(4 if N==4 else 2),'complete_antipedal_double_edges')
        ck((m+tau)%2==1,'complementary_halfperiod')

exact={'status':'PASS','assertions':sum(counts.values()),'families':dict(counts),'primitive_cases':period_cases}

mp.mp.dps=90
errors={};samples=[]
def compare(x,y,label,tol='1e-48'):
    error=abs(x-y)/(1+abs(x)+abs(y))
    assert error<mp.mpf(tol),(label,error)
    errors[label]=max(errors.get(label,mp.mpf('0')),error)

def area(ps):return sum(det(ps[j],ps[(j+1)%len(ps)]) for j in range(len(ps)))/2
for N in [4,8,12,16,20,28]:
    for tau in range(1,N//2):
        if math.gcd(N,tau)!=1:continue
        for kval in ['.0001','.51','.97','.9999']:
            kk=mp.mpf(kval);ll=mp.sqrt(1-kk*kk);K=mp.ellipk(kk*kk);J=mp.ellipk(1-kk*kk)
            v=2*K*tau/N;step=2*v;h=4*K/N
            sn=lambda u:mp.ellipfun('sn',u,kk*kk)
            cn=lambda u:mp.ellipfun('cn',u,kk*kk)
            dn=lambda u:mp.ellipfun('dn',u,kk*kk)
            pp,qq,rr=sn(v),cn(v),dn(v);aa=rr/qq;bb=ll/qq
            Bn=ll*ll+kk*kk*qq**4;Cn=ll*ll-kk*kk*qq**4
            def P(u):return (-aa*sn(u),bb*cn(u))
            def direct(w,focus=kk):
                vertices=[P(w+j*step) for j in range(N)]
                feet=[];antis=[]
                for j,point in enumerate(vertices):
                    nex=vertices[(j+1)%N];edge=(nex[0]-point[0],nex[1]-point[1])
                    mu=((focus-point[0])*edge[0]-point[1]*edge[1])/(edge[0]**2+edge[1]**2)
                    feet.append((point[0]+mu*edge[0],point[1]+mu*edge[1]))
                    left=(point[0]-focus,point[1]);right=(nex[0]-focus,nex[1])
                    hl=left[0]*point[0]+left[1]*point[1];hr=right[0]*nex[0]+right[1]*nex[1];den=det(left,right)
                    antis.append(((hl*right[1]-hr*left[1])/den,(left[0]*hr-hl*right[0])/den))
                return area(vertices),area(feet),area(antis),feet,antis
            def explicit(w):
                pedals=[];antis=[]
                for j in range(N):
                    t=w+v+j*step;ss=sn(t);cc=cn(t);EE=1-kk*kk*pp*pp*ss*ss
                    pedals.append(((kk-ss)/(1-kk*ss),ll*cc/(1-kk*ss)))
                    antis.append(((kk*rr*rr*ss*ss-Bn*ss-kk*qq*qq)/(qq*qq*EE),cc*(Cn-kk*Bn*ss)/(ll*qq*qq*EE)))
                return area(pedals),area(antis)
            trace=lambda w:sum(dn(w+j*step) for j in range(N))
            base=direct(mp.mpf('.127')*K);constant=base[1]*base[2]
            coeffp=base[1]/trace(mp.mpf('.127')*K+h/2);coeffa=base[2]/trace(mp.mpf('.127')*K)
            for frac in ['0','.329','.817','1','1.499']:
                w=mp.mpf(frac)*K;actual=direct(w);fp,fa=explicit(w)
                compare(actual[1],fp,'direct_pedal_matches_derived')
                compare(actual[2],fa,'direct_antipedal_matches_derived')
                compare(actual[1]*actual[2],constant,'real_product')
                compare(actual[1],coeffp*trace(w+h/2),'pedal_trace_identity')
                compare(actual[2],coeffa*trace(w),'antipedal_trace_identity')
                compare(actual[0],aa*bb*pp*qq/rr*trace(w),'original_trace_identity')
                compare(trace(w)*trace(w+h/2),trace(0)*trace(h/2),'halfperiod_product')
                assert actual[1]>0
            plus=direct(mp.mpf('.44')*K);minus=direct(mp.mpf('.44')*K,-kk)
            compare(plus[1],minus[1],'same_family_opposite_focus_pedal')
            compare(plus[2],minus[2],'same_family_opposite_focus_antipedal')
            if N==4:compare(constant,16*ll*ll,'N4_exact_constant')
            # Complex pole checks for selected corner and star cases.
            if kval in ['.51','.9999'] and tau in [1,N//2-1]:
                for w in [mp.mpf('.21')*K+mp.mpf('.49')*1j*J,1j*J+mp.mpf('1e-12'),h/2+1j*J+mp.mpf('1e-12')]:
                    actual=direct(w)
                    compare(actual[1]*actual[2],constant,'complex_product','1e-38')
                    compare(actual[2],coeffa*trace(w),'complex_antipedal_trace','1e-38')
                    compare(actual[1],coeffp*trace(w+h/2),'complex_pedal_trace','1e-38')
                eps=mp.mpf('1e-14')
                compare(eps*trace(1j*J+eps),-2j,'trace_exact_residue_limit','1e-12')
                compare(eps*direct(1j*J+eps)[2],-2j*coeffa,'antipedal_simple_pole_residue_limit','1e-12')
                compare(direct(1j*J+eps)[2],-direct(1j*J-eps)[2],'antipedal_odd_pole_germ','1e-38')
            samples.append({'N':N,'tau':tau,'k':kval,'product':mp.nstr(constant,18),'antipedal_trace_coefficient':mp.nstr(coeffa,18)})

numeric={'status':'PASS','precision_digits':mp.mp.dps,'orbit_cases':len(samples),'maximum_scaled_errors':{key:mp.nstr(value,12) for key,value in errors.items()},'samples':samples,'scope':'Noninterval diagnostics, not all-period proof.'}
result={'timestamp_utc':datetime.now(timezone.utc).isoformat(),'exact':exact,'numeric':numeric}
Path('ANALYTIC_CHECKS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'timestamp_utc':result['timestamp_utc'],'exact':exact,'numeric_orbit_cases':numeric['orbit_cases'],'maximum_scaled_errors':numeric['maximum_scaled_errors']},indent=2))
