"""Independent exact rational Weyl calculation, before reading submitted checker."""
from pathlib import Path
from collections import Counter
from math import comb
import datetime,hashlib,json
import sympy as S
x=S.Symbol('x');checks=Counter()
def ck(v,label):
    if not v:raise RuntimeError(label)
    checks[label]+=1
def clean(a):return {n:S.cancel(v) for n,v in a.items() if S.cancel(v)!=0}
def add(a,b,scale=1):
    c=dict(a)
    for n,v in b.items():c[n]=c.get(n,0)+scale*v
    return clean(c)
def mul(a,b):
    c={}
    for n,f in a.items():
        for m,g in b.items():
            for j in range(n+1):
                degree=n+m-j;c[degree]=c.get(degree,0)+f*comb(n,j)*S.diff(g,x,j)
    return clean(c)
def comm(a,b):return add(mul(a,b),mul(b,a),-1)
def power(a,n):
    result={0:S.Integer(1)}
    for _ in range(n):result=mul(result,a)
    return result
X={0:x};Yraw={1:S.Integer(1)}
def deriv_y(a,f):
    result={}
    for n,c in a.items():
        for i in range(n):
            result=add(result,mul({i:c},mul({0:f},{n-1-i:S.Integer(1)})))
    return result
def in_A(a,h):
    return all(S.denom(S.cancel(c/h**n))==1 for n,c in a.items())
def normal(a):return {str(k):str(v) for k,v in a.items()}

def run():
    cases=[S.Integer(3),x,x*x+1,x*(x-1)]+[x**n for n in range(2,6)]+[(x*x+1)**2,3*(x*x+1)**3*(x-2)**2]
    reports=[];negative=[]
    for h in cases:
        h=S.expand(h);d=S.Poly(S.gcd(h,S.diff(h,x)),x).monic().as_expr();pi=S.cancel(h/d)
        Y=mul(Yraw,{0:h});ck(comm(Y,X)=={0:h},'embedded_relation')
        for n in range(4):
            for gg in [S.Integer(1),x+2]:
                T={0:S.cancel(gg/d)} if n==0 else {n:S.expand(gg*pi*h**(n-1))}
                ck(in_A(comm(T,X),h) and in_A(comm(T,Y),h),'normalizer_membership')
                DT=deriv_y(T,1/pi)
                ck(in_A(DT,h),'centrality_implementer_in_A')
                for value in [X,Y]:
                    left=add(deriv_y(comm(T,value),1/pi),comm(T,deriv_y(value,1/pi)),-1)
                    ck(left==comm(DT,value),'centrality_derivation_commutator')
                if n:
                    P=S.Integer(1);formula={}
                    for j in range(n):
                        formula[n-1-j]=comb(n,j+1)*gg*d**j*P*h**(n-1-j)
                        P=S.expand(pi*S.diff(P,x)-(j+1)*S.diff(pi,x)*P)
                    ck(clean(formula)==DT,'centrality_formula_vs_leibniz')
        factors=S.factor_list(d)[1];pairs=[]
        for u,e in factors:
            g=S.cancel(d/u);L=S.cancel(pi*S.diff(d,x)/d);q=S.cancel(h*S.diff(u,x)/(u*u))
            ck(S.denom(L)==1,'L_polynomial')
            ck(S.expand(L*h+h*S.diff(pi,x)-pi*S.diff(h,x))==0,'b_respects_relation')
            ck(S.cancel(g*pi/d)==S.cancel(pi/u) and not S.denom(S.cancel(pi/u)).has(x),'cup_zero_divisibility')
            ck(S.cancel(L*g-pi*S.diff(g,x)-q)==0,'obstruction_commutator')
            ck(q!=0 and S.degree(q,x)<S.degree(h,x) and S.rem(q,h,x)!=0,'nonzero_outer_bracket')
            ck(S.degree(d,x)<S.degree(h,x) and S.degree(g,x)<S.degree(d,x),'central_companion_independent')
            ambient=comm({1:pi},Y);direct=mul({0:L},Y)
            extra=S.expand(pi*S.diff(h,x,2)-L*S.diff(h,x))
            ck(add(ambient,direct,-1)==clean({0:extra}),'direct_vs_ambient_b')
            pairs.append({'u':str(u),'g':str(g),'L':str(L),'q':str(q)})
        reports.append({'h':str(h),'d':str(d),'pi':str(pi),'repeated_factor_pairs':pairs})
    # Formal normalized B_1 tensor telescope; left and right factors distinct.
    for s in range(2,10):
        actual=Counter()
        for i in range(1,s):
            r=s-1-i
            actual[(i,1,r)]+=1;actual[(0,i+1,r)]-=1;actual[(0,i,r+1)]+=1
        expected=Counter({(i,1,s-1-i):1 for i in range(s)})
        expected[(0,s,0)]-=1
        ck({k:v for k,v in actual.items() if v}=={k:v for k,v in expected.items() if v},'bar_boundary_tensor_telescope')
    # Moving a right factor across E(x) is detectably wrong for actual derivations.
    h=x**3;Y=mul(Yraw,{0:h});D=lambda a:comm(Y,a);E=lambda a:comm(power(Y,2),a)
    correct={};wrong={}
    for i in range(1,3):
        correct=add(correct,mul(D({0:x**i}),mul(E(X),{0:x**(2-i)})))
        wrong=add(wrong,mul(mul(D({0:x**i}),{0:x**(2-i)}),E(X)))
    diff=add(correct,wrong,-1);ck(bool(diff),'negative_commuted_right_factor')
    negative.append({'mutation':'move cup right factor to left of E(x)','h':'x^3','difference':normal(diff)})
    # Ambient ad(pi*y) is not literally b in the Y=yh convention.
    h=(x*x+1)**2;pi=x*x+1;L=2*x
    extra=S.expand(pi*S.diff(h,x,2)-L*S.diff(h,x));ck(extra!=0,'negative_ambient_b_identity')
    negative.append({'mutation':'identify b with ad(pi*y) without correction','extra_polynomial':str(extra)})
    # Removing the terminal 1/u from q changes the obstruction identity.
    h=(x*x+1)**2;u=x*x+1;g=S.Integer(1);L=2*x;pi=u
    ck(S.expand(L*g-pi*S.diff(g,x)-h*S.diff(u,x)/u)!=0,'negative_wrong_q_denominator')
    # Embedded h=0 line: check generator signs on every degree combination.
    polys=[S.Integer(1),x,x*x+1,x**3-2*x]
    for f in polys:
        for g in polys:
            ck(S.expand(-S.diff(f*g,x)+f*S.diff(g,x)+g*S.diff(f,x))==0,'h_zero_mixed_leibniz')
            bv=-S.diff(f,x)*g+f*S.diff(g,x)
            ck(S.expand(bv-(f*S.diff(g,x)-g*S.diff(f,x)))==0,'h_zero_vector_bracket')
    return {'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'sympy_version':S.__version__,'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'method':'Independent rational Weyl normal ordering and derivation insertion; no submitted imports','assertion_counts':dict(checks),'total_assertions':sum(checks.values()),'families':reports,'negative_controls':negative,'scope':'Finite exact corroboration of mechanism. The all-field/all-polynomial claim uses the written proof and checked primary imports.'}

if __name__=='__main__':
    r=run();Path(__file__).with_name('fresh_weyl_results.json').write_text(json.dumps(r,indent=2)+'\n')
    print(json.dumps({'assertions':r['total_assertions'],'cases':len(r['families']),'status':'PASS'},indent=2))
