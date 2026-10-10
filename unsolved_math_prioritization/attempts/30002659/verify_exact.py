"""Exact finite controls. They support, but do not replace, the displayed proofs.
Requires Python 3 and SymPy. No floating-point fallback is permitted.
"""
import json
import sympy as s

COUNT=0

def check(value, label):
    global COUNT
    if value is not True and value != s.true:
        raise AssertionError(f'{label}: not exactly established ({value})')
    COUNT += 1


def zero(x,label):
    check(s.simplify(x)==0,label)


def nonnegative(x,label):
    v=s.simplify(x)
    check(v.is_nonnegative is True,label)


def dot(x,y):
    return (x.T*y)[0]


def norm(x):
    return s.sqrt(s.simplify(dot(x,x)))


def orbit(name, points, feasible=True):
    m=len(points);x=[s.Matrix(p) for p in points]
    edge=[x[(i+1)%m]-x[i] for i in range(m)]
    ell=[norm(e) for e in edge]
    u=[e/l for e,l in zip(edge,ell)]
    diff=[u[i-1]-u[i] for i in range(m)]
    a=[norm(v) for v in diff]
    n=[v/t for v,t in zip(diff,a)]
    y=[v-w for v,w in zip(x,n)]
    A=s.simplify(sum(a));L=s.simplify(sum(ell))
    for i in range(m):
        zero(dot(n[i],n[i])-1,name+' unit normal')
        zero(norm(x[i]-y[i])-1,name+' antipodal distance')
    for j in range(len(x[0])):
        zero(sum(a[i]*n[i][j] for i in range(m)),name+' balanced normals')
        zero(sum(ell[i]*u[i][j] for i in range(m)),name+' edge closure')
    zero(sum(a[i]*dot(x[i],n[i]) for i in range(m))-L,name+' perimeter identity')
    lam=[v/A for v in a]
    cy=sum((lam[i]*y[i] for i in range(m)),s.zeros(len(x[0]),1))
    var=s.simplify(sum(lam[i]*dot(y[i]-cy,y[i]-cy) for i in range(m)))
    pair=s.simplify(sum(lam[i]*lam[j]*dot(y[i]-y[j],y[i]-y[j]) for i in range(m) for j in range(m))/2)
    zero(var-pair,name+' variance identity')
    sig=s.simplify(sum(v*v for v in lam))
    if feasible:
        S=x+y
        for i in range(2*m):
            for j in range(i):
                nonnegative(1-dot(S[i]-S[j],S[i]-S[j]),name+' finite diameter')
        nonnegative((1-sig)/2-var,name+' variance diameter bound')
        nonnegative(L-A*(1-s.sqrt((1-sig)/2)),name+' moment bound')
    return {'name':name,'length':str(L),'turn_sum':str(A),'sigma':str(sig),'exact_diameter_feasible':feasible}


def main():
    examples=[]
    examples.append(orbit('diameter',[(0,0),(1,0)]))
    examples.append(orbit('square',[(s.Rational(1,2),0),(0,s.Rational(1,2)),(-s.Rational(1,2),0),(0,-s.Rational(1,2))]))
    a=s.Rational(3,10);b=s.Rational(1,10)
    examples.append(orbit('symmetric spatial four-orbit',[(a,b,a),(a,-b,-a),(-a,b,-a),(-a,-b,a)]))
    theta=s.symbols('theta',real=True)
    h=s.Rational(1,2)-s.cos(3*theta)/32
    zero(h+h.subs(theta,theta+s.pi)-1,'constant support width')
    zero(h+s.diff(h,theta,2)-(s.Rational(1,2)+s.cos(3*theta)/4),'curvature formula')
    normals=[s.Matrix([s.cos(t),s.sin(t)]) for t in [0,2*s.pi/3,4*s.pi/3]]
    for t in [0,2*s.pi/3,4*s.pi/3]:
        zero(h.subs(theta,t)-s.Rational(15,32),'support contact value')
        zero(s.diff(h,theta).subs(theta,t),'support contact derivative')
    for j in range(2):zero(sum(n[j] for n in normals),'three normal balance')
    odd_sum=s.simplify(sum(s.sqrt(3)*(h.subs(theta,t)-s.Rational(1,2)) for t in [0,2*s.pi/3,4*s.pi/3]))
    zero(odd_sum+3*s.sqrt(3)/32,'noncancelling odd term')
    check(odd_sum.is_negative is True,'odd term strictly negative')
    p=[list(s.Rational(15,32)*n) for n in normals]
    examples.append(orbit('smooth support triangle',p))
    nonnegative(45*s.sqrt(3)/32-2,'support triangle longer than two')
    zero(s.Rational(7,8)*(s.Rational(2,3)-s.Rational(1,4))**2-s.Rational(175,1152),'family branch one exact value')
    check(s.Rational(175,1152)>s.Rational(1,8),'family branch one strict gap')
    z=s.symbols('z',real=True)
    F=(1+3*z)/(2+2*z)-s.sqrt(1+z)/(2*s.sqrt(2))+s.Rational(1,16)
    zero(s.diff(F,z)-(1/(1+z)**2-1/(4*s.sqrt(2)*s.sqrt(1+z))),'family derivative')
    zero(F.subs(z,s.Rational(1,8))-s.Rational(43,144),'family branch two exact value')
    check(s.Rational(43,144)>s.Rational(1,4),'family branch two strict gap')
    # Nonfeasible negative control: symmetric spatial family with L=2.
    # a=b=1/(4sqrt2); r=sqrt3/4. YY adjacent squared distance >1.
    a=1/(4*s.sqrt(2));b=a;r=s.sqrt(2*a*a+4*b*b)
    yy=4*((a-a/r)**2+(b-2*b/r)**2)
    check(s.simplify(yy-1).is_positive is True,'length-two spatial negative control')
    result={'status':'PASS','assertions':COUNT,'arithmetic':'SymPy exact symbolic arithmetic; no floats','sympy_version':s.__version__,'scope':'Finite controls and identities, not the universal conjecture','examples':examples}
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
