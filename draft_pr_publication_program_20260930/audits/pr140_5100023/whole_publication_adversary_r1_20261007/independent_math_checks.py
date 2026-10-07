import datetime, json, os, pathlib, sympy as s
out=pathlib.Path(__file__).parent
a,b,lam,C=s.symbols('a b lam C', nonzero=True)
S,U,V,h=s.symbols('S U V h')
A=s.Matrix([a*(C*U+S*V),b*(S*U-C*V)])
B=s.Matrix([a*(C*U-S*V),b*(S*U+C*V)])
F=s.Matrix([h,0])
def intersection(A,B,F):
    mat=s.Matrix([(A-F).T,(B-F).T])
    rhs=s.Matrix([A.dot(A-F),B.dot(B-F)])
    return mat.inv()*rhs
Q=intersection(A,B,F)
opp=intersection(-A,-B,F)
D2=C*C/(a*a)+S*S/(b*b)
K=a*a*b*b-lam*(a*a-b*b)
g=s.groebner([h*h-a*a+b*b,U*U-1+lam*D2,V*V-lam*D2,S*S+C*C-1],h,U,V,S,domain=s.QQ.frac_field(a,b,lam,C))
def check(expr,label):
    num=s.fraction(s.cancel(expr))[0]
    remainder=s.factor(g.reduce(num)[1])
    if remainder!=0: raise RuntimeError(label+': '+str(remainder))
    return {'label':label,'polynomial_remainder':str(remainder)}
target=s.Matrix([-2*h+2*h*K*C*C/(a*a*(b*b-lam)),2*h*K*S*C/(a*b*(b*b-lam))])
intermediate=s.Matrix([2*h*b*b*(C*C-U*U)/(b*b-lam),-2*C*S*a*h*((a*a-b*b)*(C*C-U*U)-b*b)/(b*a*a*(U*U-(a*a-b*b)*C*C/(a*a)))])
checks=[]
for j,co in enumerate(['x','y']):
    checks.append(check((Q+opp-target)[j],'pair_final_'+co))
    checks.append(check((Q+opp-intermediate)[j],'pair_intermediate_'+co))
checks.append(check(U*U-(a*a-b*b)*C*C/(a*a)-(b*b-lam)*D2,'nonzero_denominator_identity'))
checks.append(check((a*a-b*b)*(C*C-U*U)-b*b+K*D2,'K_simplification'))
checks.append(check(b*b*(C*C-U*U)+(b*b-lam)-K*C*C/(a*a),'x_simplification'))
checks.append(check(a*a*S*S+b*b*C*C-a*a*b*b*D2,'length_metric'))
# Independent exact four-period diamond: (a,0),(0,b),(-a,0),(0,-b).
AA=s.Integer(2); BB=s.Integer(1); cc=s.sqrt(3); ll=AA*AA*BB*BB/(AA*AA+BB*BB)
P=[s.Matrix([AA,0]),s.Matrix([0,BB]),s.Matrix([-AA,0]),s.Matrix([0,-BB])]
centroids=[]
for hh in [s.Integer(0),cc,-cc]:
    qs=[intersection(P[i],P[(i+1)%4],s.Matrix([hh,0])) for i in range(4)]
    mean=s.simplify(sum(qs,s.zeros(2,1))/4)
    if hh==0: expected=s.zeros(2,1)
    else:
        per=4*s.sqrt(AA*AA+BB*BB)
        HH=AA*AA/(AA*AA-BB*BB)*(1-BB*per/(2*AA*s.sqrt(ll)*4))
        KK=AA*AA*BB*BB-ll*(AA*AA-BB*BB)
        expected=s.Matrix([hh*(-1+KK*HH/(AA*AA*(BB*BB-ll))),0])
    if s.simplify(mean-expected)!=s.zeros(2,1):raise RuntimeError('diamond centroid mismatch')
    centroids.append({'pole':str(hh),'centroid':[str(x) for x in mean]})
    # Reflection is validated independently by tangent-normal orthogonality.
for i,Pi in enumerate(P):
    incoming=(Pi-P[(i-1)%4])/s.sqrt((Pi-P[(i-1)%4]).dot(Pi-P[(i-1)%4]))
    outgoing=(P[(i+1)%4]-Pi)/s.sqrt((P[(i+1)%4]-Pi).dot(P[(i+1)%4]-Pi))
    tangent=s.Matrix([-AA*Pi[1]/BB,BB*Pi[0]/AA])
    if s.simplify((incoming-outgoing).dot(tangent))!=0:raise RuntimeError('reflection failure')
result={'timestamp_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'actual_pid':os.getpid(),'sympy':s.__version__,'checks':checks,'diamond':{'a':2,'b':1,'lambda':str(ll),'N':4,'centroids':centroids},'limitations':'Symbolic local identities and one exact closed even orbit do not establish Poncelet closure or all-period theorem.'}
(out/'independent_math_checks.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
