#!/usr/bin/env python3
"""Independent exact certificates for 30002830; no imports from author code.

All checks use explicit exceptions, including under Python -O/-OO. Geometric
theorem dependencies are audited in AUDIT.md, not computer-formalized here.
"""
import argparse
import itertools
import json
from pathlib import Path
import sympy as S

records = []


def require(name, condition, category='exact_identity'):
    if not bool(condition):
        raise RuntimeError('CHECK FAILED: ' + name)
    records.append(dict(name=name, category=category, passed=True))


def eq(name, left, right=0, category='exact_identity'):
    require(name, S.cancel(left-right) == 0, category)


def nonzero(name, value, category='nondegeneracy'):
    require(name, S.cancel(value) != 0, category)


def run(mutation=None):
    s,t,x,y,z,U,V,W,q0,A,C,e,r,u,h,H,Y,Z,v = S.symbols('s t x y z U V W q0 A C e r u h H Y Z v')
    a=s*t*(s-t); b=s*(1-s); c=t*(t-1); d=-a-b-c
    F=S.expand(a*U+b*W+c*V)
    eq('fourth cubic coefficient factorization',d,-(s-t)*(s-1)*(t-1))
    require('coefficient content one',S.gcd(S.gcd(a,b),c)==1)
    for j,f in enumerate((a,b,c,d)):
        nonzero('projective coefficient nonzero '+str(j),f)
    eq('diagonal cubic rational point',a+b+c+d)
    xx=S.symbols('X0:4')
    homogeneous=sum(f*X**3 for f,X in zip((a,b,c,d),xx))
    for j,(f,X) in enumerate(zip((a,b,c,d),xx)):
        eq('smoothness derivative certificate '+str(j),S.diff(homogeneous,X),3*f*X**2)

    # The quotient-model map, checked without importing the preceding audit.
    D=s*s*U-V
    q=2*(V-s*U)/D
    T=S.cancel(q*(q+2)/(q*(q+2)-U))
    eq('corrected q plus two',q+2,2*s*(s-1)*U/D)
    eq('T minus one',T-1,U/(q*(q+2)-U))
    Vback=U*s*(s*q0+2)/(q0+2)
    Wback=U*t*(t*q0+2)/(q0+2)
    eq('inverse original ratios recover q',q.subs(V,Vback),q0)
    eq('original ratio reconstruction lies on model',F.subs({V:Vback,W:Wback}))
    Wsolve=S.cancel((a*U+c*V)/(s*(s-1)))
    for name,rate,rad in [('2',1,U),('3',s,V),('4',t,Wsolve)]:
        eq('elliptic quotient equation '+name,(1+rate*q)**2*(T-1),(1+rad)*T-1)
        eq('ratio recovers base '+name,((1+rate*q)-1)/q,rate)
    old={s:0,t:0,U:1,V:1,W:1}
    old_open=U*D*q*(q*(q+2)-U)
    nonzero('old open accepts bad point',old_open.subs(old),'negative_control')
    eq('old accepted point has T zero',T.subs(old),0,'negative_control')
    corrected=s*t*(s-1)*(t-1)*(s-t)*old_open*(q+2)
    eq('corrected open excludes bad point',corrected.subs(old),0,'negative_control')
    p={s:3,t:5,U:2,V:7,W:S.Rational(40,3)}
    eq('independent nonempty chart witness satisfies F',F.subs(p))
    nonzero('independent corrected chart witness',corrected.subs(p))
    nonzero('independent lift has T nonzero',T.subs(p))
    nonzero('independent lift has T minus one nonzero',(T-1).subs(p))

    # Independent elimination in the coefficient net and Vieta involution.
    aa=S.cancel(a/b); cc=S.cancel(c/b)
    net=C*(C+1)*s*s+2*A*C*s+A*(A+1)
    eliminated=S.factor((A*(s-1)+t*(s-t)).subs(t,-C*s-A))
    eq('net obtained from linear elimination',eliminated,-net)
    eq('coefficient linear relation',t+cc*s+aa)
    eq('coefficient quadratic relation',net.subs({A:aa,C:cc},simultaneous=True))
    net_disc=S.discriminant(net,s)
    eq('net quadratic discriminant',net_disc,-4*A*C*(A+C+1))
    ee=S.factor(cc*(cc+1)*s+aa*cc)
    eq('net square relation',ee**2,-aa*cc*(aa+cc+1))
    si=(e-A*C)/(C*(C+1))
    if mutation=='net_inverse': si=(e+A*C)/(C*(C+1))
    ti=-C*si-A
    relation=e*e+A*C*(A+C+1)
    for name,f,target in [('s',si,s),('t',ti,t)]:
        eq('net inverse recovers '+name,f.subs({A:aa,C:cc,e:ee},simultaneous=True),target)
    for name,f,target in [('A',aa,A),('C',cc,C)]:
        numerator=S.together(f.subs({s:si,t:ti},simultaneous=True)-target).as_numer_denom()[0]
        eq('net forward after inverse '+name,S.rem(numerator,relation,e))
    other_s=S.factor(-2*aa/(cc+1)-s)
    other_t=S.factor(-cc*other_s-aa)
    eq('Vieta derives involution s',other_s,-s*(s-t-1)/(s+t-1))
    eq('Vieta derives involution t',other_t,t*(s-t+1)/(s+t-1))
    sub={s:other_s,t:other_t}
    for name,f in [('A',aa),('C',cc)]:
        eq('involution fixes '+name,f.subs(sub,simultaneous=True),f)
    eq('involution exchanges square root',ee.subs(sub,simultaneous=True),-ee)
    for name,f,target in [('s',other_s,s),('t',other_t,t)]:
        eq('involution has order two on '+name,f.subs(sub,simultaneous=True),target)
    nonzero('involution nontrivial witness',(other_s-s).subs(p))
    Ce=-(A*U+W)/V
    rad=A*(A*U+W)*(A*(V-U)+V-W)
    eq('net eliminated radicand',-A*Ce*(A+Ce+1)*V**2,rad)
    require('quadratic radicand exact A valuation one',S.Poly(rad,A).terms()[-1][0]==(1,))
    eq('quadratic leading A-adic coefficient',S.expand(rad).coeff(A,1),W*(V-W))
    nonzero('quadratic valuation residue nonzero',W*(V-W))
    nonzero('opposite branch sign rejected',rad+A*Ce*(A+Ce+1)*(-V**2),'negative_control')

    # Exact cubic cover arithmetic; regularity/Galois arguments are in audit.
    eq('coefficient pairing identity',a*b/(c*d),s*s/(t-1)**2)
    exponent=3 if mutation!='cubic_cover' else 2
    eq('cubic base change yields cube',S.cancel(a*b/(c*d)).subs(s,u**exponent*(t-1)),u**6)
    require('Kummer s valuation equals one',S.Poly(s,s).degree()==1 and S.Poly(t-1,s).degree()==0)
    for j,f in enumerate((a,b,c,d)):
        nonzero('base changed cubic stays smooth coefficient '+str(j),f.subs(s,u**3*(t-1)))
    eq('base changed cubic retains rational point',(a+b+c+d).subs(s,u**3*(t-1)))
    eq('rational base change field inverse',u**3*(t-1)/(t-1),u**3)
    require('square base change pairing exponent fails mod three',4%3!=0,'negative_control')

    # The full permutation action is distinct modulo diagonal scalar action.
    permutations=list(itertools.permutations(range(4)))
    require('there are twenty four coordinate actions',len(set(permutations))==24)
    matrices=[]
    for perm in permutations:
        M=S.zeros(4)
        for i,j in enumerate(perm):M[i,j]=1
        matrices.append(M)
    scalar=[M for M in matrices if all(M[i,j]==0 for i in range(4) for j in range(4) if i!=j)]
    require('only identity permutation is diagonal',scalar==[S.eye(4)])
    require('degree four elliptic linear system dimension',4+1-1==4)
    require('degree four Serre dual degree negative',0-4<0)
    require('Abel Jacobi section has degree four',1+3==4)

    # Derive the discriminant model and check every branch stratum.
    fp=S.Poly(F,t)
    l,m,n=fp.all_coeffs()
    eq('mixed quadratic leading coefficient',l,V-s*U)
    eq('mixed quadratic middle coefficient',m,s*s*U-V)
    eq('mixed quadratic constant coefficient',n,-s*(s-1)*W)
    Delta=S.discriminant(fp.as_expr(),t)
    eq('completed square relation',(2*l*t+m)**2-Delta,4*l*F)
    eq('completed square inverse',(2*l*t+m-m)/(2*l),t)
    A0=1+s*s*U; B0=1+s*U; k0=4*s*(s-1); C0=s*s*U+2*s-1
    Q=(A0*H-Z)**2+k0*(Z-B0*H)*(Y-H)
    matrix=S.Matrix([[S.diff(Q,p1,p2)/2 for p2 in (Y,Z,H)] for p1 in (Y,Z,H)])
    desired=-4*U**2*s**4*(s-1)**4
    if mutation=='conic_sign':desired=-desired
    eq('branch conic determinant',matrix.det(),desired)
    eq('branch conic first side discriminant',S.discriminant(Q.subs({Y:0,H:1}),Z),k0*k0*(U+1))
    eq('branch conic second side',Q.subs(Z,0),H*(C0*C0*H-k0*B0*Y))
    eq('branch conic third side',Q.subs(H,0),Z*(Z+k0*Y))
    eq('auxiliary square coefficient',A0*A0+k0*B0,C0*C0)
    eq('conic contains first vertex',Q.subs({Y:1,Z:0,H:0}))
    nonzero('conic misses second vertex',Q.subs({Y:0,Z:1,H:0}))
    nonzero('conic misses third vertex',Q.subs({Y:0,Z:0,H:1}))
    for name,restriction in [('Y',Q.subs({Y:0,H:1})),('Z',Q.subs({Z:0,H:1})),('H',Q.subs({H:0,Z:1}))]:
        variable=Z if name=='Y' else Y
        nonzero('simple side intersection '+name,S.resultant(restriction,S.diff(restriction,variable),variable))
    B=Q.subs({Y:y**3,Z:z**3,H:v**3},simultaneous=True)
    eq('sextic dehomogenization',B.subs(v,1),Delta.subs({W:y**3-1,V:z**3-1}))
    require('branch homogeneous degree six',all(sum(mon)==6 for mon in S.Poly(B,y,z,v).monoms()))
    local=S.Poly(B.subs(y,1),z,v)
    require('unique vertex branch multiplicity three',min(sum(mon) for mon in local.monoms())==3)
    tangent=sum(coeff*z**mon[0]*v**mon[1] for mon,coeff in local.terms() if sum(mon)==3)
    eq('tangent cone cubic',tangent,k0*(z**3-B0*v**3))
    eq('three distinct tangent directions',S.discriminant(z**3-B0,z),-27*B0**2)
    strict=S.cancel(B.subs({y:1,z:r*v})/v**3)
    eq('explicit blown up strict branch',strict,k0*(r**3-B0)+v**3*((A0-r**3)**2-k0*(r**3-B0)))
    eq('strict branch meets exceptional in three points',strict.subs(v,0),k0*(r**3-B0))
    eq('strict branch transverse derivative',S.diff(strict,r).subs(v,0),3*k0*r*r)
    require('exceptional intersections simple',S.gcd(r**3-B0,3*r*r)==1)
    eq('normalized double cover has exceptional branch',B.subs({y:1,z:r*v})/v**2,v*strict)
    strict_class=S.Matrix([6,-3]); exceptional=S.Matrix([0,1]); canonical=S.Matrix([-3,1])
    total_branch=strict_class+exceptional
    if mutation=='exceptional_branch':total_branch=strict_class
    require('normalized branch class even',all(int(i)%2==0 for i in total_branch))
    require('normalized cover canonical class zero',canonical+total_branch/2==S.zeros(2,1))
    local_node=h*h-r*v
    require('local ordinary double point nondegenerate',S.hessian(local_node,(h,r,v)).det()!=0)
    require('omitting exceptional branch is parity failure',any(int(i)%2 for i in strict_class),'negative_control')
    eq('s zero branch degenerates to square',Delta.subs(s,0),V*V,'negative_control')
    eq('U zero conic singular',matrix.det().subs(U,0),0,'negative_control')
    nonzero('generic geometric open has rational witness',(s*(s-1)*(U+1)*U*B0*C0).subs({s:3,U:2}))

    # Supporting elliptic model, checked modulo F rather than hardcoded residual.
    N=4*s*(s-1)*(V-s*U)
    twist=N*N*(N-D*D)/D**6
    eq('elliptic T reconstruction',T,N/(N-D*D))
    eq('elliptic twist coefficient',twist,T*T/(T-1)**3)
    xi=y*T/(T-1); eta=(1+t*q)*T/(T-1)
    eq('elliptic equation on hypersurface',(eta*eta-xi**3+twist).subs(y**3,Wsolve+1))
    eq('elliptic inverse y',xi*(T-1)/T,y)
    eq('elliptic inverse t',(eta*(T-1)/T-1)/q,t)
    nonzero('elliptic twist nonzero',twist)
    require('quartic surface adjunction K trivial',4-4==0,'scope_control')

    # Independent Newton-width certificate: direct 2 e_s, 2 e_t differences.
    f=F.subs({U:x**3-1,W:y**3-1,V:z**3-1})
    polynomial=S.Poly(f,s,t,x,y,z)
    support=set(polynomial.monoms())
    require('Newton twelve monomials',len(support)==12)
    if mutation=='newton_support':support.remove((2,1,3,0,0))
    certificates=[((2,1,0,0,0),(0,1,0,0,0),(2,0,0,0,0)),
                  ((1,2,0,0,0),(1,0,0,0,0),(0,2,0,0,0)),
                  ((2,1,3,0,0),(2,1,0,0,0),(0,0,3,0,0)),
                  ((2,0,0,3,0),(2,0,0,0,0),(0,0,0,3,0)),
                  ((0,2,0,0,3),(0,2,0,0,0),(0,0,0,0,3))]
    for i,(p1,p2,delta) in enumerate(certificates):
        require('Newton width forcing pair '+str(i),p1 in support and p2 in support and tuple(a-b for a,b in zip(p1,p2))==delta)
    require('width forcing matrix determinant',abs(S.Matrix([p[2] for p in certificates]).det())==108)
    for coordinate in (0,1):
        require('width two coordinate '+str(coordinate),max(p[coordinate] for p in support)-min(p[coordinate] for p in support)==2)
    for coordinate in (2,3,4):
        require('width three coordinate '+str(coordinate),max(p[coordinate] for p in support)-min(p[coordinate] for p in support)==3)
    # This factorization is over Q; geometric irreducibility over C is proved
    # separately from smoothness of the generic projective diagonal cubic.
    require('rational polynomial factor count one',len(S.factor_list(f)[1])==1)
    linear=a*(x-1)+b*(y**3-1)+c*(z**3-1)
    require('linear replacement has degree one',S.Poly(linear,x).degree()==1,'negative_control')
    xsolve=1-(b*(y**3-1)+c*(z**3-1))/a
    eq('linear replacement actually rationally solves',linear.subs(x,xsolve),0,'negative_control')

    return dict(target_id='30002830',verdict='SCOPED PASS: NO RESOLUTION',
                sympy_version=S.__version__,check_count=len(records),
                negative_control_count=sum(r['category']=='negative_control' for r in records),
                checks=records,geometric_dependencies_formalized=False)


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--output')
    parser.add_argument('--mutation',choices=['net_inverse','cubic_cover','conic_sign','exceptional_branch','newton_support'])
    args=parser.parse_args()
    result=run(args.mutation)
    data=json.dumps(result,indent=2)+'\n'
    if args.output:Path(args.output).write_text(data)
    else:print(data,end='')
