"""Independent tangent-initialized, reflection-propagated k307 geometric audit.
No submitted checker or Jacobi parameterization is imported. Finite evidence only.
"""
import json, math, time
import mpmath as m
from pathlib import Path
m.mp.dps=110

def dot(x,y): return x[0]*y[0]+x[1]*y[1]
def cross(x,y): return x[0]*y[1]-x[1]*y[0]
def add(x,y): return (x[0]+y[0],x[1]+y[1])
def sub(x,y): return (x[0]-y[0],x[1]-y[1])
def mul(c,x): return (c*x[0],c*x[1])
def norm(x): return m.sqrt(dot(x,x))

def initial_direction(p,a,b,L):
    A=m.sqrt(a*a-L); B=m.sqrt(b*b-L)
    r=(p[0]/A,p[1]/B); r2=dot(r,r)
    k=m.sqrt(r2-1)
    choices=[]
    for sign in [-1,1]:
        q=(A*(r[0]-sign*k*r[1])/r2,B*(r[1]+sign*k*r[0])/r2)
        v=sub(q,p); v=mul(1/norm(v),v)
        if cross(p,v)>0: choices.append(v)
    assert len(choices)==1
    return choices[0]

def orbit(a,b,L,N,phase):
    p=(a*m.cos(phase),b*m.sin(phase))
    v=initial_direction(p,a,b,L)
    P=[]; directions=[]; total=m.mpf(0)
    for _ in range(N):
        P.append(p); directions.append(v)
        step=-2*(p[0]*v[0]/(a*a)+p[1]*v[1]/(b*b))/(v[0]*v[0]/(a*a)+v[1]*v[1]/(b*b))
        assert step>0
        q=add(p,mul(step,v))
        up=(p[0]/a,p[1]/b); uq=(q[0]/a,q[1]/b)
        angle=m.atan2(cross(up,uq),dot(up,uq))
        assert 0<angle<m.pi
        total+=angle
        normal=(q[0]/(a*a),q[1]/(b*b))
        v=sub(v,mul(2*dot(v,normal)/dot(normal,normal),normal))
        p=q
    return P,directions,p,v,total

def closure_lambda(a,b,N,k):
    # The accumulated boundary-angle defect is monotone under the elliptic
    # Poncelet map. Bracket by approaching both strict elliptic endpoints.
    lo=m.mpf('1e-50')*b*b; hi=b*b*(1-m.mpf('1e-50'))
    target=2*m.pi*k
    flo=orbit(a,b,lo,N,0)[-1]-target
    fhi=orbit(a,b,hi,N,0)[-1]-target
    assert flo<0<fhi, (a,N,k,str(flo),str(fhi))
    for _ in range(340):
        mid=(lo+hi)/2
        fm=orbit(a,b,mid,N,0)[-1]-target
        if fm>0: hi=mid
        else: lo=mid
    return (lo+hi)/2

def pa(p,q):
    out=dict(p)
    for e,c in q.items(): out[e]=out.get(e,m.mpf(0))+c
    return out

def ps(c,p): return {e:c*v for e,v in p.items()}
def pm(p,q):
    out={}
    for (i,j),u in p.items():
        for (k,l),v in q.items():
            e=(i+k,j+l);out[e]=out.get(e,m.mpf(0))+u*v
    return out

def projection_polys(P,a,b):
    Q=[]
    for p in P:
        n=(p[0]/(a*a),p[1]/(b*b)); r=dot(n,n)
        Q.append(({(0,0):n[0]/r,(1,0):1-n[0]*n[0]/r,(0,1):-n[0]*n[1]/r},
                  {(0,0):n[1]/r,(1,0):-n[0]*n[1]/r,(0,1):1-n[1]*n[1]/r}))
    return Q

def moment_polys(Q):
    area={}; Tx={}; Ty={}
    for i,q in enumerate(Q):
        r=Q[(i+1)%len(Q)]
        c=pa(pm(q[0],r[1]),ps(-1,pm(q[1],r[0])))
        area=pa(area,ps(m.mpf('0.5'),c))
        Tx=pa(Tx,pm(c,pa(q[0],r[0])))
        Ty=pa(Ty,pm(c,pa(q[1],r[1])))
    return area,Tx,Ty

def pe(p,X,Y):return sum(c*X**i*Y**j for (i,j),c in p.items())

def direct(P,a,b,X,Y):
    M=(X,Y);Q=[]
    for p in P:
        n=(p[0]/(a*a),p[1]/(b*b));Q.append(add(M,mul((1-dot(n,M))/dot(n,n),n)))
    S=m.mpf(0);T=(m.mpf(0),m.mpf(0))
    for i,q in enumerate(Q):
        r=Q[(i+1)%len(Q)];c=cross(q,r);S+=c/2;T=add(T,mul(c,add(q,r)))
    return S,T,Q

def predicted(a,b,L,X,Y):
    H=(a*a+b*b)/2;e=(a*a-b*b)/2;d=1-L*(1/(a*a)+1/(b*b));F=H*d+2*L
    v=-4*e*L*d/(F*F-e*e*d*d);G=2*F+d*(X*X+Y*Y)
    z=m.mpc(X,Y);C=None if G==0 else z/2-(z*(F+2*H*d+e*v*d)+m.conj(z)*(2*F*v+3*e*d+v*d*(X*X+Y*Y)/2))/(3*G)
    return C,H,e,d,F,v,G

worst={}; counts={}; cases=[]
def ck(value,key,tol=m.mpf('1e-48')):
    value=abs(value);worst[key]=max(worst.get(key,m.mpf(0)),value)
    counts[key]=counts.get(key,0)+1
    assert value<tol,(key,m.nstr(value,25))

def audit(a,b,L,N,k,label):
    previous={}; phase_data=[]
    for phase in [m.mpf(0),m.mpf('.197'),m.mpf('.713'),m.mpf('1.219')]:
        P,V,p,v,total=orbit(a,b,L,N,phase)
        ck(norm(sub(p,P[0]))/(a+b),'closure_position')
        ck(norm(sub(v,V[0])),'closure_direction')
        ck(total/(2*m.pi)-k,'winding')
        Qpoly=projection_polys(P,a,b);A,Tx,Ty=moment_polys(Qpoly);S0=A[(0,0)]
        assert S0>0
        n=[mul(1/norm((p[0]/(a*a),p[1]/(b*b))),(p[0]/(a*a),p[1]/(b*b))) for p in P]
        Z=[(u[0]*u[0]-u[1]*u[1],2*u[0]*u[1]) for u in n]
        Sz=sum(cross(Z[i],Z[(i+1)%N]) for i in range(N))/2
        normal_deltas=[]
        for i in range(N):
            p0=P[i];p1=P[(i+1)%N];prev=P[(i-1)%N]
            ck(p0[0]*p0[0]/(a*a)+p0[1]*p0[1]/(b*b)-1,'ellipse')
            ck(norm(add(p0,P[(i+N//2)%N]))/(a+b),'antipodal')
            ck(norm(sub(p0,P[(i+1)%N]))==0,'nonrepeated_adjacent')
            edge=sub(p1,p0);ell=(p0[0]/(a*a),p0[1]/(b*b))
            ni=(-edge[1],edge[0]);c=dot(ni,p0)
            ck((c*c-(a*a-L)*ni[0]*ni[0]-(b*b-L)*ni[1]*ni[1])/(1+c*c),'caustic_tangency')
            incoming=mul(1/norm(sub(p0,prev)),sub(p0,prev));out=mul(1/norm(edge),edge)
            refl=sub(incoming,mul(2*dot(incoming,ell)/dot(ell,ell),ell))
            ck(norm(sub(refl,out)),'reflection')
            delta=m.atan2(cross(n[i],n[(i+1)%N]),dot(n[i],n[(i+1)%N]))
            assert 0<delta<m.pi
            normal_deltas.append(delta)
        distances=[norm(sub(P[i],P[j]))/(a+b) for i in range(N) for j in range(i)]
        assert min(distances)>m.mpf('1e-20')
        C,H,e,d,F,vc,G=predicted(a,b,L,m.mpf('.29'),m.mpf('-.41'))
        if abs(d)<m.mpf('1e-45'): assert N==4
        if k==1:assert d>=-m.mpf('1e-45')
        # Coefficients are obtained by direct polynomial shoelace expansion.
        expected_A={(0,0):S0,(2,0):S0*d/(2*F),(0,2):S0*d/(2*F)}
        lx=3-(F+2*H*d+e*vc*d+2*F*vc+3*e*d)/F
        ly=3-(F+2*H*d+e*vc*d-2*F*vc-3*e*d)/F
        cx=d*(3-vc)/(2*F);cy=d*(3+vc)/(2*F)
        expected_Tx={(1,0):S0*lx,(3,0):S0*cx,(1,2):S0*cx}
        expected_Ty={(0,1):S0*ly,(2,1):S0*cy,(0,3):S0*cy}
        for actual,expected,key in [(A,expected_A,'all_area_coefficients'),(Tx,expected_Tx,'all_x_moment_coefficients'),(Ty,expected_Ty,'all_y_moment_coefficients')]:
            for exponent in set(actual)|set(expected):
                ck((actual.get(exponent,0)-expected.get(exponent,0))/(1+abs(S0)*(a+b)**(sum(exponent)+1)),key)
        if abs(d)>m.mpf('1e-45'):ck((S0-F*Sz/(2*d))/(1+S0),'doubled_normal_area')
        Mlist=[(0,0),('.29','-.41'),('1.3','.7'),(str(3*a),str(-2*b)),('1e5','-7e4')]
        if d<-m.mpf('1e-45'):
            rho=m.sqrt(-2*F/d)
            Mlist.extend([(rho,0),(rho*(1+m.mpf('1e-12')),0),(rho*(1-m.mpf('1e-12')),0)])
        for xs,ys in Mlist:
            X=m.mpf(xs);Y=m.mpf(ys)
            actual_S,T,Q=direct(P,a,b,X,Y)
            cp,H,e,d,F,vc,G=predicted(a,b,L,X,Y)
            ck((actual_S-S0*G/(2*F))/(1+abs(S0)+abs(actual_S)),'point_area_identity')
            # First moment can be tested even where the quotient is undefined.
            Txval=pe(expected_Tx,X,Y);Tyval=pe(expected_Ty,X,Y)
            ck((T[0]-Txval)/(1+abs(Txval)),'point_first_moment_x')
            ck((T[1]-Tyval)/(1+abs(Tyval)),'point_first_moment_y')
            if abs(G)<m.mpf('1e-55'):
                ck(actual_S/(1+S0),'exceptional_circle_area');continue
            actual_C=m.mpc(T[0],T[1])/(6*actual_S)
            ck((actual_C-cp)/(1+abs(cp)),'point_centroid_formula',m.mpf('1e-38'))
            key=(str(X),str(Y))
            if key in previous:ck((actual_C-previous[key])/(1+abs(cp)),'phase_centroid',m.mpf('1e-38'))
            previous[key]=actual_C
            reverseS,reverseT,_=direct(list(reversed(P)),a,b,X,Y)
            ck((reverseS+actual_S)/(1+abs(actual_S)),'orientation_area')
            ck((m.mpc(*reverseT)/(6*reverseS)-actual_C)/(1+abs(actual_C)),'orientation_centroid',m.mpf('1e-38'))
        # Scaling both ellipses and M must scale centroid and area consistently.
        X=m.mpf('.29');Y=m.mpf('-.41');scale=m.mpf('17.3')
        ss,tt,_=direct([mul(scale,p) for p in P],scale*a,scale*b,scale*X,scale*Y)
        s,t,_=direct(P,a,b,X,Y)
        ck((ss-scale**2*s)/(1+abs(ss)),'scale_area')
        ck((m.mpc(*tt)/(6*ss)-scale*m.mpc(*t)/(6*s))/(1+norm(tt)/(6*abs(ss))),'scale_centroid')
        phase_data.append({'phase':str(phase),'S0':m.nstr(S0,25),'normal_delta_min':m.nstr(min(normal_deltas),15),'normal_delta_max':m.nstr(max(normal_deltas),15),'Sz':m.nstr(Sz,25),'minimum_vertex_distance_scaled':m.nstr(min(distances),15)})
    cases.append({'label':label,'a':m.nstr(a,25),'b':m.nstr(b,25),'N':N,'winding':k,'lambda':m.nstr(L,65),'d':m.nstr(d,35),'F':m.nstr(F,35),'v':m.nstr(vc,35),'phase_data':phase_data})
    print('checked',label,N,k,m.nstr(L,15),flush=True)

if __name__=='__main__':
    configurations=[('1.0001',4,1),('1.0001',8,3),('1.8',4,1),('1.8',6,1),('1.8',8,1),('1.8',8,3),('1.8',10,3),('1.8',14,3),('1.8',18,5),('1.8',40,1),('10',6,1),('10',8,3),('20',10,3),('100',6,1),('1000000',6,1),('1000',8,3),('1.8',200,1),('1.8',50,23),('1.8',98,25),('1.8',102,25)]
    for av,N,k in configurations:
        a=m.mpf(av);b=m.mpf(1);L=closure_lambda(a,b,N,k)
        audit(a,b,L,N,k,'reflection-closed')
    # Exact claimed example: regenerate it by tangency and reflection, rather
    # than importing its submitted vertex list.
    a=m.sqrt(m.mpf(221)/96);b=m.sqrt(m.mpf(27625)/20736);L=m.mpf(125)/96
    audit(a,b,L,8,3,'exact-8/3-regenerated')
    Path('NUMERICAL_RESULTS.json').write_text(json.dumps({'status':'PASS','precision_decimal_digits':m.mp.dps,'orbit_generator':'explicit inner tangent point then repeated outer intersection and specular reflection','cases':cases,'check_counts':counts,'maximum_residuals':{k:m.nstr(v,20) for k,v in worst.items()},'limitations':'Finite geometric and polynomial-coefficient corroboration; no numerical enumeration proves the all-real all-N result.'},indent=2)+'\n')
