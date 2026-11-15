"""Supplemental 90-digit actual caustic-tangent billiard constructions."""
import mpmath as mp
mp.mp.dps=90
def dot(A,B): return A[0]*B[0]+A[1]*B[1]
def cross(A,B): return A[0]*B[1]-A[1]*B[0]
def sub(A,B): return [A[i]-B[i] for i in range(2)]
def norm(A): return mp.sqrt(dot(A,A))
def area(P): return sum(cross(P[i],P[(i+1)%3]) for i in range(3))/2
def circle(P):
    A=mp.matrix([[2*(P[i][j]-P[0][j]) for j in range(2)] for i in [1,2]])
    b=mp.matrix([dot(P[i],P[i])-dot(P[0],P[0]) for i in [1,2]])
    O=list(mp.lu_solve(A,b)); return O,dot(sub(P[0],O),sub(P[0],O))
def pedal(P,F):
    feet=[]
    for i in range(3):
        d=sub(P[(i+1)%3],P[i]); w=dot(sub(F,P[i]),d)/dot(d,d)
        feet.append([P[i][j]+w*d[j] for j in range(2)])
    return area(feet)
maxerr=mp.mpf(0); count=0
for ts in ['1.00000001','1.01','1.5','2','10','10000']:
    t=mp.mpf(ts); Y=mp.mpf(1); X=t*(t+2)/(2*t+1); D=(t*t+t+1)/(2*t+1)
    a=mp.sqrt(X); b=mp.mpf(1); q=X-Y; n=X-D; m=D-Y
    ac=a*m/q; bc=b*n/q; c=mp.sqrt(q); rho=2*t/(t+1)**2; M=(t+1)**3/(2*t)
    def next_vertex(P):
        z=[P[0]/ac,P[1]/bc]; k=dot(z,z); w=mp.sqrt(k-1)
        candidates=[]
        for sign in [-1,1]:
            u=[(z[0]-sign*w*z[1])/k,(z[1]+sign*w*z[0])/k]
            Q=[ac*u[0],bc*u[1]]; d=sub(Q,P)
            lam=-2*(P[0]*d[0]/X+P[1]*d[1]/Y)/(d[0]*d[0]/X+d[1]*d[1]/Y)
            candidates.append([P[j]+lam*d[j] for j in range(2)])
        return next(Q for Q in candidates if cross(P,Q)>0)
    for angle in [mp.mpf(0),mp.pi/2,mp.pi,3*mp.pi/2,mp.mpf('.17'),mp.pi/3,mp.mpf('1.1'),mp.mpf('2.0'),mp.mpf('4.3')]:
        P0=[a*mp.cos(angle),b*mp.sin(angle)]
        P=[P0,next_vertex(P0)]; P.append(next_vertex(P[1])); closing=next_vertex(P[2])
        errors={}
        def ck(name,residual,scale=1):
            err=abs(residual)/(1+abs(scale)); errors[name]=max(errors.get(name,mp.mpf(0)),err)
            assert err<mp.mpf('1e-60'),(ts,str(angle),name,str(err))
        ck('closure',norm(sub(closing,P0)),a)
        for i,p in enumerate(P):
            ck('ellipse incidence',p[0]**2/X+p[1]**2/Y-1)
            d=sub(P[(i+1)%3],p); L=[-d[1],d[0],cross(p,P[(i+1)%3])]
            ck('caustic tangency',L[2]**2-ac**2*L[0]**2-bc**2*L[1]**2,L[2]**2)
            left=sub(P[(i-1)%3],p); right=sub(P[(i+1)%3],p)
            bisector=[left[j]/norm(left)+right[j]/norm(right) for j in range(2)]
            normal=[p[0]/X,p[1]/Y]
            ck('reflection',cross(bisector,normal),norm(normal))
            assert dot(bisector,normal)<0
        side=[norm(sub(P[(i+1)%3],P[(i+2)%3])) for i in range(3)]
        I=[sum(side[i]*P[i][j] for i in range(3))/sum(side) for j in range(2)]
        O,R2=circle(P); r=2*area(P)/sum(side)
        E=[[sum((-1 if i==k else 1)*side[i]*P[i][j] for i in range(3))/(sum(side)-2*side[k]) for j in range(2)] for k in range(3)]
        H,RE2=circle(E)
        ck('original power',R2-dot(O,O)-D,D)
        ck('Bevan power',RE2-dot(H,H)-(X+Y+2*D),X+Y+2*D)
        ck('Euler',dot(sub(O,I),sub(O,I))-R2+2*r*mp.sqrt(R2),R2)
        ck('incenter locus',I[0]**2/(m*m/X)+I[1]**2/(n*n/Y)-1)
        ck('circumcenter locus',O[0]**2/(n*n/(4*X))+O[1]**2/(m*m/(4*Y))-1)
        ck('Bevan direction',norm(sub(H,[2*O[j]-I[j] for j in range(2)])),norm(H))
        ck('outer radius',RE2-4*R2,RE2)
        ck('area ratio',area(E)/area(P)-2/rho,2/rho)
        ck('rho',r/mp.sqrt(R2)-rho)
        ck('synchronized phase',I[0]+2*t*O[0],a)
        for sign in [-1,1]:
            F=[sign*c,mp.mpf(0)]; A=pedal(P,F); B=pedal(E,F)
            assert A>0 and B>0
            ck('pedal formula original',A-area(P)*(R2-dot(sub(F,O),sub(F,O)))/(4*R2),A)
            ck('pedal formula outer',B-area(E)*(RE2-dot(sub(F,H),sub(F,H)))/(4*RE2),B)
            ck('M',B-M*A,B)
        maxphase=max(errors.values()); maxerr=max(maxerr,maxphase); count+=1
        print('t='+ts,'phase='+mp.nstr(angle,8),'max_normalized_residual='+mp.nstr(maxphase,8),'M='+mp.nstr(M,15))
print('Passed',count,'actual constructed phase cases; maximum normalized residual',mp.nstr(maxerr,15))
print('SCOPE: supplemental high-precision computations, not universal or interval-certified proof.')
