#!/usr/bin/env python3
"""Fresh symbolic Weyl-operator / normalized-bar controls before helper reading.

Normal order is coefficient(x) * y**j, where [y,x]=1. Rational
coefficients allow the localized derivations to be applied directly.
This script does not import any supplied proof/checker implementation.
"""
from pathlib import Path
from datetime import datetime, timezone
from collections import Counter
from itertools import product
import hashlib,json,math
import sympy as s
x=s.symbols('x'); HERE=Path(__file__).resolve().parent; C=Counter()
def ck(t,label):
    assert t,label
    C[label]+=1
def tidy(a): return {j:s.cancel(v) for j,v in a.items() if s.cancel(v)!=0}
def add(*ops):
    out={}
    for a in ops:
        for j,v in a.items():out[j]=out.get(j,0)+v
    return tidy(out)
def neg(a):return {j:-v for j,v in a.items()}
def const(v):return tidy({0:s.sympify(v)})
one=const(1); X=const(x); y={1:s.Integer(1)}
def mul(a,b):
    out={}
    for i,f in a.items():
        for j,g in b.items():
            for k in range(i+1):
                v=math.comb(i,k)*f*s.diff(g,x,k)
                out[i+j-k]=out.get(i+j-k,0)+v
    return tidy(out)
def powop(a,n):
    out=one
    for _ in range(n):out=mul(out,a)
    return out
def comm(a,b):return add(mul(a,b),neg(mul(b,a)))
def derive(a,dx,dy):
    # Here dx is polynomial/rational in x, hence commutes with coefficients.
    out={}
    for n,f in a.items():
        out=add(out,mul(const(s.diff(f,x)*dx),powop(y,n)))
        for i in range(n):
            out=add(out,mul(const(f),mul(powop(y,i),mul(dy,powop(y,n-1-i)))))
    return out
def polynomial_coefficients(a):
    return all(s.denom(s.cancel(v))==1 for v in a.values())
def in_A(a,h):
    return all(s.denom(s.cancel(v/h**j))==1 for j,v in a.items())
def monomials(a):
    terms=[]
    for j,f in a.items():
        for (i,),v in s.Poly(f,x,domain=s.QQ).terms():
            if v:terms.append(((i,j),v))
    return terms
def tensor1(L,u,R):
    out=Counter()
    for (ml,cl),(mu,cu),(mr,cr) in product(monomials(L),monomials(u),monomials(R)):
        if mu!=(0,0):out[(ml,mu,mr)]+=cl*cu*cr
    return dict(out)
def tsum(*terms):
    out={}
    for t in terms:
        for key,v in t.items():out[key]=out.get(key,0)+v
    return {k:s.cancel(v) for k,v in out.items() if v}
def tscale(t,k):return {a:k*v for a,v in t.items()}
def boundary(L,u,v,R):
    return tsum(tensor1(mul(L,u),v,R),tscale(tensor1(L,mul(u,v),R),-1),tensor1(L,u,mul(v,R)))
def bar_comparison(h,Y):
    lhs=tsum(boundary(one,Y,X,one),tscale(boundary(one,X,Y,one),-1))
    rhs=tsum(tensor1(one,Y,X),tensor1(Y,X,one),tscale(tensor1(one,X,Y),-1),tscale(tensor1(X,Y,one),-1))
    uncorrected=lhs
    for (degree,),coef in s.Poly(h,x).terms():
        if degree>=1:
            for i in range(degree):
                rhs=tsum(rhs,tscale(tensor1(const(x**i),X,const(x**(degree-1-i))),-coef))
        if degree>=2:
            for i in range(1,degree):
                lhs=tsum(lhs,tscale(boundary(one,const(x**i),X,const(x**(degree-1-i))),-coef))
    ck(lhs==rhs,'normalized_bar_chain_map')
    return len(tsum(uncorrected,tscale(rhs,-1)))

def main():
    started=datetime.now(timezone.utc).isoformat(); rows=[]
    polynomials=[1,2,x,3*(x*x+1),x*(x-1),x*x,x**3,2*(x-1)**3,(x*x+1)**2,3*(x*x+1)**2*(x-2)**3]
    for raw in polynomials:
        h=s.expand(raw);d=s.Poly(s.gcd(h,s.diff(h,x)),x).monic().as_expr();pi=s.cancel(h/d)
        Y=mul(y,const(h));ck(comm(Y,X)==const(h),'embedded_relation')
        omitted_bar_residual=bar_comparison(h,Y)
        if s.degree(h,x)>=2:ck(omitted_bar_residual>0,'negative_omit_nonlinear_bar_correction')
        def Dd(a):return derive(a,0,const(d/h))
        ck(Dd(X)=={} and Dd(Y)==const(d),'localized_Dd_on_generators')
        for n in range(1,5):
            for r in (1,x):
                A=mul(const(r*pi*h**(n-1)),powop(y,n))
                for t in (X,Y):ck(in_A(comm(A,t),h),'normalizer_preserves_A')
                DA=Dd(A)
                ck(in_A(DA,h),'centrality_inner_primitive_in_A')
                for t in (X,Y):
                    val=add(Dd(comm(A,t)),neg(comm(A,Dd(t))))
                    ck(val==comm(DA,t),'centrality_commutator_of_derivations')
        witnesses=[]
        for u,e in s.factor_list(h)[1]:
            if e<2:continue
            u=s.Poly(u,x).monic().as_expr();g=s.cancel(d/u);L=s.cancel(pi*s.diff(d,x)/d)
            ck(s.denom(L)==1,'L_polynomial')
            dy=add(mul(const(-s.diff(pi,x)),y),const((L*s.diff(h,x)-pi*s.diff(h,x,2))/h))
            def b(a):return derive(a,pi,dy)
            def Dg(a):return derive(a,0,const(g/h))
            ck(b(X)==const(pi) and b(Y)==mul(const(L),Y),'direct_b_derivation')
            ck(add(comm(dy,X),comm(y,const(pi)))=={},'b_respects_localized_Weyl_relation')
            bracket=add(Dg(b(Y)),neg(b(Dg(Y))))
            q=s.cancel(h*s.diff(u,x)/u**2)
            ck(bracket==const(q),'noncommuting_pair_direct_operator_bracket')
            ck(s.rem(g*pi,d,x)==0,'pair_cup_zero_mod_d')
            ck(q!=0 and s.degree(q,x)<s.degree(h,x) and s.rem(q,h,x)!=0,'bracket_noninner')
            ck(s.degree(d,x)<s.degree(h,x) and s.degree(g,x)<s.degree(d,x),'central_companion_independent')
            # Distinguish the directly defined b from an unjustified ambient identification.
            naive=comm(mul(const(pi),y),Y)
            extra=add(naive,neg(b(Y)))
            ck(extra==const(pi*s.diff(h,x,2)-L*s.diff(h,x)),'ambient_identification_extra_term')
            witnesses.append({'u':str(u),'g':str(g),'q':str(q),'naive_ambient_extra':str(extra.get(0,0))})
        rows.append({'h':str(h),'d':str(d),'pi':str(pi),'squarefree':d==1,'repeated_factor_witnesses':witnesses})
        print(json.dumps({'h':str(h),'status':'PASS'}),flush=True)
    # Generator constraints on the actual h=x^2 witness span c,a,b: all cups zero,
    # c central, [a,b]=a. The scalar functional must simultaneously have lb=0 and lb=-1.
    lc,la,lb=s.symbols('lc la lb')
    equations=[lc,lb,la,la,lb+1]
    M,rhs=s.linear_eq_to_matrix(equations,[lc,la,lb])
    ck(M.rank()<M.row_join(rhs).rank(),'no_linear_generator_on_witness_subspace')
    # Embedded h=0 is k[x]; verify the proposed negative-divergence convention.
    zero_cases=0
    for f in (1,x,x*x+1,x**3-2*x):
        for g in (1,x+1,x**2,x**4):
            ck(s.expand(s.diff(f*g,x)-s.diff(f,x)*g-f*s.diff(g,x))==0,'embedded_zero_degree_1_0_BV')
            ck(s.expand(-s.diff(g*f,x)+g*s.diff(f,x)+f*s.diff(g,x))==0,'embedded_zero_degree_0_1_BV')
            ck(s.expand(-s.diff(f,x)*g+s.diff(g,x)*f-(f*s.diff(g,x)-g*s.diff(f,x)))==0,'embedded_zero_degree_1_1_BV')
            zero_cases+=1
    ck(s.diff(x**3,x).subs(x,x)%3==0,'characteristic_three_derivative_failure_control')
    ck(s.Poly(s.diff(x**3,x),x,modulus=3).is_zero,'characteristic_three_squarefree_test_not_transferred')
    # At h=1 the constant is invisible in normalized bars; in h=0 embedded algebra Y=0.
    ck(mul(y,const(0))=={},'embedded_zero_has_no_second_generator')
    result={'started_utc':started,'finished_utc':datetime.now(timezone.utc).isoformat(),
       'method':'Independent normal-ordered localized Weyl operators, Leibniz insertion derivations and normalized-bar tensors; no packaged helper imported.',
       'sympy_version':s.__version__,'assertions':sum(C.values()),'counts':dict(C),'polynomials':rows,
       'generator_constraint_rank':M.rank(),'augmented_rank':M.row_join(rhs).rank(),'embedded_zero_polynomial_pairs':zero_cases,
       'scope':'Finite exact controls and falsified alternatives, not proof of structural imports or universal classification.',
       'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    (HERE/'fresh-control-results.json').write_text(json.dumps(result,indent=2)+'\n')
if __name__=='__main__': main()
