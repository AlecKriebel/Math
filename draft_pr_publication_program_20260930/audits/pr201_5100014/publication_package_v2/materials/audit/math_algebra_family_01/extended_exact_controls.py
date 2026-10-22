"""Exact general-semiaxis control and excluded repeated-triangle counterexample."""
import sys,json
from pathlib import Path
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parents[1]/'pr200_5100007'/'math_algebra_family_01'/'runtime_packages'))
import sympy as S
ns={'__name__':'imported_independent','__file__':str(HERE/'exact_independent_controls.py')}
exec(compile((HERE/'exact_independent_controls.py').read_text(),str(HERE/'exact_independent_controls.py'),'exec'),ns)
need=ns['need'];area=ns['area'];direct=ns['direct']

def main():
    a,b,t=S.symbols('a b t',positive=True);m,n=S.symbols('m n',real=True)
    # t²=b(2a+b). Verify this general six-period configuration physically.
    P=[(a,0),(a*a/(a+b),b*t/(a+b)),(-a*a/(a+b),b*t/(a+b)),(-a,0),(-a*a/(a+b),-b*t/(a+b)),(a*a/(a+b),-b*t/(a+b))]
    lam6=a*a*b*b/(a+b)**2
    def reduce_t(expr):
        num,den=S.fraction(S.cancel(expr))
        return S.factor(S.rem(S.Poly(num,t),S.Poly(t*t-b*(2*a+b),t)).as_expr())
    for j,(x,y) in enumerate(P):
        X,Y=P[(j+1)%6];nx,ny=y-Y,X-x;h=nx*x+ny*y
        need(reduce_t(x*x/a**2+y*y/b**2-1)==0,'general hexagon boundary failed')
        need(reduce_t((a*a-lam6)*nx*nx+(b*b-lam6)*ny*ny-h*h)==0,'general hexagon caustic failed')
    normals=[(1,0,a),(b,t,b*(a+b)),(-b,t,b*(a+b)),(-1,0,a),(-b,-t,b*(a+b)),(b,-t,b*(a+b))]
    F=[]
    for x,y,h in normals:
        den=S.sympify(x*x+y*y).subs(t*t,b*(2*a+b));q=(h-x*m-y*n)/den
        F.append((m+q*x,n+q*y))
    pedal=area(F);prod=S.factor(S.cancel(2*a*b*(a+2*b)/t*pedal).subs(t*t,b*(2*a+b)))
    # Semiaxis swap supplies the other axis phase, with same geometric M radius.
    swapped=S.factor(prod.xreplace({a:b,b:a,m:n,n:m}))
    need(S.simplify(prod-swapped)==0,'general two-axis product differs')
    need(S.simplify(prod.subs({a:2,b:1})-40*(m*m+n*n+9)/9)==0,'general product does not recover numerical semiaxes')
    d=S.sqrt(13);alpha=2*(d-1)/3;beta=(4-d)/3;lam=(8*d-20)/9
    H=[(2,0),(-alpha,S.sqrt(1-alpha**2/4)),(-alpha,-S.sqrt(1-alpha**2/4))]
    V=[(0,1),(-2*S.sqrt(1-beta**2),-beta),(2*S.sqrt(1-beta**2),-beta)]
    records=[]
    for P in (H,V):
        P=[tuple(map(S.sympify,p)) for p in P]
        for j,(x,y) in enumerate(P):
            X,Y=P[(j+1)%3];nx,ny=y-Y,X-x;h=nx*x+ny*y
            need(S.simplify(x*x/4+y*y-1)==0,'triangle boundary failed')
            need(S.simplify((4-lam)*nx*nx+(1-lam)*ny*ny-h*h)==0,'triangle caustic failed')
        ap,am,_,_=direct(P,(S.Integer(1),S.Integer(2)))
        pap,pam,_,_=direct(P*2,(S.Integer(1),S.Integer(2)))
        product=S.simplify(ap*am);need(S.simplify(pap*pam-4*product)==0,'repeatedtriangle scaling failed')
        records.append({'product':str(product),'repeated_N6_product':str(S.simplify(4*product))})
    diff=S.simplify(S.sympify(records[0]['repeated_N6_product'])-S.sympify(records[1]['repeated_N6_product']))
    need(diff.is_zero is False,'exact repeatedtriangle nonzero difference not certified')
    print(json.dumps({'status':'PASS','optimization':sys.flags.optimize,'general_axis_hexagon_product':str(prod),'general_scope':'exact equality for two axis phases for all positive a,b, and arbitrary real M; not a proof for every phase','excluded_twice_traversed_triangle':{'lambda':str(lam),'M':[1,2],'phases':records,'exact_difference':str(diff),'is_zero':diff.is_zero}},indent=2))
if __name__=='__main__':main()
