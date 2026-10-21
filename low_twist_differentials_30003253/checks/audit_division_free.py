"""Divisibility checks by auxiliary quotient coefficients, with no division.

Uses neither Poly.rem nor Groebner. Nullity agrees with the original P-space
because multiplication by each nonzero branch equation is injective.
"""
import json
from pathlib import Path
import sympy as s
from branch_integrality import kernel
from audit_independent_model import powers, monomial, exact_rank

X=x,y,z=s.symbols('x y z')
A=a,b,c=s.symbols('a b c')
U=u,v,w=s.symbols('u v w')


def quotient_columns(F, degree):
    bdegree=s.Poly(F,*X).total_degree()
    return [s.Poly(F*monomial(X,q),*X,domain=s.QQ).as_dict()
            for q in powers(degree-bdegree)] if degree>=bdegree else []


def division_free_dimension(branches,r,k):
    d=k-2*r
    terms=[monomial(X,p)*monomial(A,q)
           for p in powers(d) for q in powers(r) if not(p[0] and q[0])]
    blocks=[]
    total=len(terms)
    for F in branches:
        degree=d+r*(s.Poly(F,*X).total_degree()-1)
        gradient={aa:s.diff(F,xx) for aa,xx in zip(A,X)}
        evaluations=[s.Poly(T.subs(gradient,simultaneous=True),*X,domain=s.QQ).as_dict() for T in terms]
        quotients=quotient_columns(F,degree)
        blocks.append((degree,evaluations,quotients,total))
        total+=len(quotients)
    rows=[]
    for degree,evaluations,quotients,start in blocks:
        for power in powers(degree):
            row=[0]*total
            row[:len(terms)]=[E.get(power,0) for E in evaluations]
            row[start:start+len(quotients)]=[-Q.get(power,0) for Q in quotients]
            rows.append(row)
    return total-exact_rank(rows,total)


def divides_without_division(F,E):
    E=s.Poly(E,*X,domain=s.QQ)
    if E.is_zero:return True
    degree=E.total_degree()
    columns=quotient_columns(F,degree)
    coefficient=E.as_dict()
    rows=[[Q.get(p,0) for Q in columns] for p in powers(degree)]
    appended=[row+[coefficient.get(p,0)] for row,p in zip(rows,powers(degree))]
    return exact_rank(rows,len(columns))==exact_rank(appended,len(columns)+1)


def main():
    F=x*z-y*y-y*z-z*z
    cases=[('line',[z],1,2),
           ('transformed_conic_below',[F],1,2),
           ('transformed_conic_first_order',[F],1,3),
           ('transformed_conic_second_order',[F],2,4),
           ('two_conics',[x*x+y*y+z*z,x*x+2*y*y+3*z*z],1,4)]
    output=[]
    for name,branches,r,k in cases:
        dimension=division_free_dimension(branches,r,k)
        if not (dimension==kernel(branches,r,k)['dimension']):
            raise AssertionError('Audit integrity check failed')
        output.append(dict(name=name,r=r,k=k,dimension=dimension))
    if not (divides_without_division(z,0)):
        raise AssertionError('Audit integrity check failed')
    if not (not divides_without_division(z,1)):
        raise AssertionError('Audit integrity check failed')
    # For the line z=0, gradient=(0,0,1): a is valid, a+c is not.
    if not (divides_without_division(z,a.subs({a:0,b:0,c:1}))):
        raise AssertionError('Audit integrity check failed')
    if not (not divides_without_division(z,(a+c).subs({a:0,b:0,c:1}))):
        raise AssertionError('Audit integrity check failed')
    cross=(y*w-z*v,z*u-x*w,x*v-y*u)
    zero=s.expand((x*a+y*b+z*c).subs(dict(zip(A,cross)),simultaneous=True))
    if not (zero==0):
        raise AssertionError('Audit integrity check failed')
    if not (s.expand(a.subs(dict(zip(A,cross)),simultaneous=True))!=0):
        raise AssertionError('Audit integrity check failed')
    Path(__file__).with_name('audit_division_free_results.json').write_text(json.dumps(dict(
        method='Coefficient blocks E(P)-FQ; exact QQ rank; no polynomial division',
        tests=output,valid_witness_accepted=True,altered_witness_rejected=True,
        zero_incidence_witness_rejected=True),indent=2)+'\n')
    print('PASS: division-free conic, multiple-branch, and witness mutation controls')


if __name__=='__main__':main()
