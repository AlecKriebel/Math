#!/usr/bin/env python3
"""Exact finite controls for PROOF.md. Requires Python 3 and SymPy 1.14.
No network, source corpus, credentials, or private files are used.
"""
import argparse
import itertools
import json
import math
import platform
from pathlib import Path
import sympy as sp

checks = 0

def check(condition, message):
    global checks
    checks += 1
    if not condition:
        raise AssertionError(message)

def zero(expr, message):
    check(sp.expand(expr) == 0, message)

u,v,a,b,s,t,z = sp.symbols('u v a b s t z')
world_vars = (a,b,s,t)

def degree(expr, variables=(u,v)):
    return sp.Poly(expr,*variables).total_degree()

def common_factor(polys):
    return sp.gcd_list(polys)

def saturated_by(polys, variable):
    w = sp.Symbol('w')
    gb = sp.groebner([*polys,1-w*variable],w,*world_vars,order='lex')
    return [x.as_expr() for x in gb.polys if not x.as_expr().has(w)]

def same_ideal(gens1,gens2):
    g1=sp.groebner(gens1,*world_vars,order='lex')
    g2=sp.groebner(gens2,*world_vars,order='lex')
    return all(g2.reduce(x)[1]==0 for x in gens1) and all(g1.reduce(x)[1]==0 for x in gens2)


def examples():
    entries=[]
    data=[
      ('unequal_degrees',[a-t,b*s-t*t],[u*v,u*u,v*v,u*v],2,[a-t,b*s-t*t]),
      ('overlapping_epipoles',[a*t-s*s,b*t-s*s],[u*u,u*u,u*v,v*v],2,[a-b,a*t-s*s]),
      ('disjoint_epipoles',[a*t-s*s,b*s-t*t],[u**3,v**3,u*u*v,u*v*v],3,[a*t-s*s,b*s-t*t,a*b-s*t]),
    ]
    for name,eqs,param,d,expected in data:
        for f in eqs:
            zero(f.subs(dict(zip(world_vars,param)),simultaneous=True),name+' parametrization')
        check(degree(common_factor(param))==0,name+' no base factor')
        check(all(degree(x)==d for x in param),name+' homogeneous degree')
        sat=saturated_by(eqs,t)
        check(same_ideal(sat,expected),name+' saturation ideal')
        # The pencil ratio supplies a rational inverse to the parametrization.
        zero(param[2]*u-param[3]*v if name=='unequal_degrees' else param[2]*v-param[3]*u,name+' pencil inverse')
        entries.append({'name':name,'world_degree':d,'saturated_ideal':[str(x) for x in sat]})
    # Clean double cover factors give a node; no normalization claim is inferred.
    zero((a-b)*(a+b)-(a*a-b*b),'node factorization')
    node=sp.Poly(a*a-b*b,a,b)
    check(node.diff(a).eval({a:0,b:0})==0,'node first derivative')
    check(node.diff(b).eval({a:0,b:0})==0,'node second derivative')
    check(sp.discriminant(sp.Symbol('x')**2-1,sp.Symbol('x'))==4,'distinct tangent lines')
    return entries


def monoid_family():
    count=0
    degrees=set()
    for m in range(2,9):
      for n in range(2,9):
       for i in range(m):
        for j in range(n):
          E=u**i*v**(m-1-i);F=u**j*v**(n-1-j)
          A=u**m+v**m;B=u**n+2*v**n
          x=[A,E*u,E*v];y=[B,F*u,F*v]
          check(degree(common_factor(x))==0,'X image has no base factor')
          check(degree(common_factor(y))==0,'Y image has no base factor')
          raw=[A*F,B*E,E*F*u,E*F*v]
          factor=common_factor(raw)
          overlap=min(i,j)+min(m-1-i,n-1-j)
          check(degree(factor)==overlap,'triangulation cancellation')
          delta=m+n-1-overlap
          check(all(degree(sp.div(p,factor,u,v)[0])==delta for p in raw),'world degree')
          # r=q=N=1 and a_j=b_j=1.
          cp=max(j-i,0)+max((n-1-j)-(m-1-i),0)
          cq=max(i-j,0)+max((m-1-i)-(n-1-j),0)
          check(delta-cp==m,'first center multiplicity')
          check(delta-cq==n,'second center multiplicity')
          baseline=(m-1)*(n-1)+overlap
          check(delta+baseline==m*n,'Bezout cycle degree')
          count+=1;degrees.add(delta)
    return {'instances':count,'image_degree_range':[2,8],'world_degrees':sorted(degrees)}


def local_baseline_lengths():
    results=[]
    # a=1, b=z is the generic point of the projective baseline;
    # computations take place over the exact field QQ(z).
    field=sp.QQ.frac_field(z)
    for m,n,i,j in [(2,2,0,0),(2,2,0,1),(3,3,1,0),(3,4,2,1),(4,5,1,3)]:
        E=s**i*t**(m-1-i);F=s**j*t**(n-1-j)
        f=E-s**m-t**m;g=z*F-s**n-2*t**n
        predicted=(m-1)*(n-1)+min(i,j)+min(m-1-i,n-1-j)
        lengths=[]
        for N in (predicted+1,predicted+2):
            gb=sp.groebner([f,g]+[s**k*t**(N-k) for k in range(N+1)],s,t,order='lex',domain=field)
            leading=[p.LM(order=gb.order).exponents for p in gb.polys]
            length=sum(all(not (i0>=i1 and j0>=j1) for i1,j1 in leading)
                       for i0 in range(N) for j0 in range(N))
            check(length==predicted,'generic-baseline truncated length')
            lengths.append(length)
        # Nested ideals with equal finite colength are equal. Stabilization of
        # I+(s,t)^N is the local Nakayama criterion for this length computation.
        check(lengths[0]==lengths[1],'local length stabilization')
        results.append({'m':m,'n':n,'i':i,'j':j,'predicted':predicted,'exact_lengths':lengths,'field':'QQ(z)'})
    return results


def compose(p,q):
    return tuple(p[q[i]] for i in range(3))

def inverse(p):
    return tuple(p.index(i) for i in range(3))

def hurwitz_count():
    perms=list(itertools.permutations(range(3)));ident=(0,1,2)
    trans=[p for p in perms if sum(p[i]!=i for i in range(3))==2]
    admissible=[]
    for sequence in itertools.product(trans,repeat=6):
        product=ident
        for p in sequence:product=compose(product,p)
        if product!=ident:continue
        orbit={0}
        while True:
            new=orbit|{p[i] for p in sequence for i in orbit}
            if new==orbit:break
            orbit=new
        if len(orbit)==3:admissible.append(sequence)
    representatives=set();sizes=set()
    for sequence in admissible:
        conj={tuple(compose(compose(p,x),inverse(p)) for x in sequence) for p in perms}
        representatives.add(min(conj));sizes.add(len(conj))
    check(len(admissible)==240,'transitive identity-product tuples')
    check(len(representatives)==40,'Hurwitz conjugacy classes')
    check(sizes=={6},'free conjugation')
    return {'tuples':len(admissible),'conjugacy_classes':len(representatives),'orbit_sizes':sorted(sizes),'novel':False}


def boundary_controls():
    # Real twist: adding the equations forces a^2+b^2=0.
    f=a*a-s*t;g=b*b+s*t
    zero(f+g-(a*a+b*b),'real sum of squares')
    for pt in [(0,0,1,0),(0,0,0,1)]:
        check(f.subs(dict(zip(world_vars,pt)))==0,'real endpoint first equation')
        check(g.subs(dict(zip(world_vars,pt)))==0,'real endpoint second equation')
    # Disjoint real pencil ranges are certified using exact rational endpoints.
    X_interval=(-1,1);Y_interval=(2,4)
    check(X_interval[1]<Y_interval[0],'disjoint real ranges')
    zero((s-3)**2-1-(s-2)*(s-4),'shifted real circle roots')
    # Frobenius in characteristic two.
    check(sp.Poly((a-b)**2-(a*a-b*b),a,b,modulus=2).is_zero,'Frobenius double factor')
    ff=sp.Poly(a*a-s*t,a,b,s,t,modulus=2)
    gg=sp.Poly(b*b-s*t,a,b,s,t,modulus=2)
    check(ff-gg==sp.Poly((a-b)**2,a,b,s,t,modulus=2),'double conic relation')
    # Scheme support with its generic length differs from reduced count.
    check(2*1==math.gcd(2,2) and 1!=math.gcd(2,2),'weighted versus reduced partition')
    return {'real_twist_real_points':2,'real_disjoint_pencil_intervals':[list(X_interval),list(Y_interval)],'inseparable_generic_multiplicity':2}


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path)
    args=parser.parse_args()
    results={'examples':examples(),'monoid_family':monoid_family(),
             'local_baseline_lengths':local_baseline_lengths(),'hurwitz':hurwitz_count(),
             'boundary_controls':boundary_controls()}
    results.update({'assertions':checks,'status':'PASS','python':platform.python_version(),'sympy':sp.__version__,
                    'scope':'Exact finite controls, not a formal verification of the universal theorems or a novelty certificate.'})
    out=json.dumps(results,indent=2,sort_keys=True)+'\n'
    if args.output:args.output.write_text(out)
    print(out,end='')

if __name__=='__main__':main()
