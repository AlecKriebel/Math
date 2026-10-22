"""Exact finite controls, not a formal geometric proof. Use the pinned bootstrap."""
import json
import math
from fractions import Fraction
from pathlib import Path

COUNT = 0

def check(condition, label):
    global COUNT
    COUNT += 1
    if not condition:
        raise ValueError('check failed: ' + label)

def mm(a,b):
    return tuple(tuple(sum(a[i][k]*b[k][j] for k in range(2)) for j in range(2)) for i in range(2))

def mp(a,n):
    result=((1,0),(0,1))
    while n:
        if n & 1:
            result=mm(result,a)
        a=mm(a,a); n//=2
    return result

def mr(a):
    if not any(x for row in a for x in row):
        return 0
    return 2 if a[0][0]*a[1][1]-a[0][1]*a[1][0] else 1

def defect_matrix(a):
    return mr(tuple(tuple(a[i][j]-(i==j) for j in range(2)) for i in range(2)))

def ct_formula(N,a):
    result=0
    for l in range(N//8+1):
        for m in range((N-8*l)//4+1):
            rest=N-8*l-4*m
            if rest%2:
                continue
            n=rest//2
            counts=(4*l+2*m+n,2*l+m,l,l,m,n)
            result+=math.factorial(N)//math.prod(math.factorial(k) for k in counts)*2**m*a**n
    return result

def direct_period(a,N):
    terms=[((1,0,0),1),((0,1,0),1),((0,0,1),1),((-4,-2,-1),1),((-2,-1,0),2),((-1,0,0),a)]
    values={(0,0,0):1}; out=[1]
    for n in range(1,N+1):
        new={}
        for u,c in values.items():
            for v,d in terms:
                if not d:
                    continue
                key=tuple(x+y for x,y in zip(u,v))
                new[key]=new.get(key,0)+c*d
        values={u:c for u,c in new.items() if c}
        out.append(values.get((0,0,0),0))
    return out

def poly_add(a,b):
    out=a.copy()
    for e,c in b.items():
        out[e]=out.get(e,0)+c
    return {e:c for e,c in out.items() if c}

def poly_mul(a,b):
    out={}
    for e,c in a.items():
        for f,d in b.items():
            g=tuple(x+y for x,y in zip(e,f))
            out[g]=out.get(g,0)+c*d
    return {e:c for e,c in out.items() if c}

def poly_scale(a,c):
    return {e:c*d for e,d in a.items() if c*d}

def power(a,n):
    out={(0,0,0):1}
    for _ in range(n):
        out=poly_mul(out,a)
    return out

def dot(a,b):
    return sum(x*y for x,y in zip(a,b))

def cross(a,b):
    return (a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])

def compute():
    global COUNT
    COUNT=0
    vertices=[(1,0,0),(0,1,0),(0,0,1),(-4,-2,-1)]
    normals=[(1,1,1),(1,1,-7),(1,-3,1),(-1,1,1)]
    for n in normals:
        check(math.gcd(*n)==1,'primitive facet normal')
        dots=[dot(n,v) for v in vertices]
        check(dots.count(1)==3 and min(dots)<1,'supporting facet')
    interior=[]
    for x in range(-4,2):
        for y in range(-2,2):
            for z in range(-1,2):
                if all(dot(n,(x,y,z))<1 for n in normals):
                    interior.append((x,y,z))
    check(interior==[(0,0,0)],'unique interior lattice point')
    edge_lengths=[]
    for i in range(4):
        for j in range(i+1,4):
            edge_lengths.append(math.gcd(*(vertices[j][k]-vertices[i][k] for k in range(3))))
    check(sorted(edge_lengths)==[1,1,1,1,1,2],'edge lengths')
    check(tuple((a+b)//2 for a,b in zip(vertices[2],vertices[3]))==(-2,-1,0),'edge midpoint')
    check([dot(n,(-1,0,0)) for n in normals]==[-1,-1,-1,1],'a lies in facet interior')
    check(cross((2,1,1),(-1,-1,0))==(1,-1,-1),'saturated facet character basis')
    U={(1,0,0):1}; V={(0,1,0):1}; A={(0,0,1):1}; one={(0,0,0):1}
    # Q=(U+1)^2 V^2 + AUV + U; discriminant in V.
    delta=poly_add(poly_mul(power(A,2),power(U,2)),poly_scale(poly_mul(U,power(poly_add(U,one),2)),-4))
    expanded={(3,0,0):-4,(2,0,2):1,(2,0,0):-8,(1,0,0):-4}
    check(delta==expanded,'symbolic quadratic discriminant')
    # Discriminant of U^2+(2-A^2/4)U+1, avoiding denominators.
    check(poly_add(power(poly_add({(0,0,0):8},poly_scale(power(A,2),-1)),2),{(0,0,0):-64})=={(0,0,4):1,(0,0,2):-16},'exceptional parameter polynomial')
    for a in range(-12,13):
        check((a*a*(a*a-16)==0)==(a in (0,4,-4)),'integer discriminant specializations')
    for a in (-4,4):
        u=Fraction(1);v=Fraction(-a,8)
        check((u+1)**2*v*v+a*u*v+u==0,'node on curve')
        check(2*(u+1)*v*v+a*v+1==0,'node derivative U')
        check(2*(u+1)**2*v+a*u==0,'node derivative V')
        check((2*v*v)*(2*(u+1)**2)-(4*(u+1)*v+a)**2==4,'node Hessian')
    for a in (-4,-1,0,1,4):
        direct=direct_period(a,16)
        for n,v in enumerate(direct):
            check(v==ct_formula(n,a),'direct Laurent expansion versus multinomial formula')
    for q in range(41):
        lhs=sum(Fraction(2**(q-2*l),math.factorial(l)**2*math.factorial(q-2*l)) for l in range(q//2+1))
        check(lhs==Fraction(math.factorial(2*q),math.factorial(q)**3),'all-order identity finite control')
        check(ct_formula(4*q,0)==math.factorial(4*q)//math.factorial(q)**4,'quartic period identity')
    for n in range(121):
        for a in (-5,-4,-2,0,1,3,4,7):
            v=ct_formula(n,a)
            check(v==0 if n%2 else ct_formula(n,-a)==((-1)**(n//2))*v,'scalar/torus change period identity')
    cs=[ct_formula(n,4) for n in range(101)]
    for n in range(101):
        residual=n**3*cs[n]
        if n>=2:
            d=n-2
            residual-=16*(d+1)*(3*d*d+6*d+4)*cs[n-2]
        if n>=4:
            d=n-4
            residual+=512*(d+1)*(d+2)*(d+3)*cs[n-4]
        check(residual==0,'published F4 Picard-Fuchs recurrence')
    check(cs[:10]==[1,0,8,0,120,0,2240,0,47320,0],'published F4 initial coefficients')
    # The two blowups of (u,yz): each displayed total-transform factorization.
    u=U;y=V;z=A
    check(poly_mul(u,poly_mul(y,z))=={(1,1,1):1},'first u-chart second generator u*w*z')
    check(poly_mul(y,u)=={(1,1,0):1},'first y-chart first generator y*v')
    check(poly_mul(y,z)=={(0,1,1):1},'first y-chart second generator y*z')
    check(poly_mul(poly_mul(y,u),z)=={(1,1,1):1},'second v-chart second generator y*v*r')
    check(poly_mul(poly_mul(y,z),u)=={(1,1,1):1},'second z-chart first generator y*z*s')
    a=((1,2),(0,1));b=((1,0),(-2,1));c=((1,-2),(2,-3));ident=((1,0),(0,1))
    check(mm(mm(a,b),c)==ident,'ABC=I')
    check(defect_matrix(a)+defect_matrix(b)+defect_matrix(c)==4,'initial rank-two extremality')
    defects=[]
    for m in range(1,129):
        am=mp(a,m);cm=mp(c,m)
        check(am==((1,2*m),(0,1)),'A power formula')
        check(defect_matrix(am)==1,'A power codimension')
        check(defect_matrix(cm)==(2 if m%2 else 1),'C power codimension')
        rf=defect_matrix(am)+m*defect_matrix(b)+defect_matrix(cm)
        d=rf-4
        check(d==(m-1 if m%2 else m-2),'base-change defect')
        check(am[0][1]!=0 and b[1][0]!=0,'distinct fixed lines persist')
        if m<=12:
            defects.append(d)
    return {'problem_id':30001913,'status':'unsolved','substantive_approaches':5,'finite_checks':COUNT,'family_hodge_tate_parameters':[-4,0,4],'F4_initial_period':cs[:10],'base_change_defects_m_1_to_12':defects,'geometric_proofs_formalized':False,'complete_solution_claimed':False}

def main():
    root=Path(__file__).parent
    status=json.loads((root/'STATUS.json').read_text())
    for key,value in {'problem_id':30001913,'status':'unsolved','substantive_approaches':5,'approach_limit':5,'complete_proof':False,'counterexample_to_original_hypotheses':False,'novelty_claim':False,'independent_audit':'pending'}.items():
        if type(status.get(key)) is not type(value) or status[key]!=value:
            raise ValueError('status contract changed: '+key)
    result=compute()
    expected=json.loads((root/'EXPECTED.json').read_text())
    if result!=expected:
        raise ValueError('finite output does not match frozen expected output')
    print(json.dumps(result,sort_keys=True))

if __name__=='__main__':
    main()
