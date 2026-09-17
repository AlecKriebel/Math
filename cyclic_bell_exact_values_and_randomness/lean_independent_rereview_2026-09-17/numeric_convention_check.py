"""Independent finite numerical sanity check from the manuscript formulas.
Not a formal proof; all errors are floating-point residuals.
"""
from cmath import exp, pi
from math import sin, sqrt
from pathlib import Path
import json

def shift(w):
    d=len(w)
    return [[w[j] if i==(j+1)%d else 0j for j in range(d)] for i in range(d)]
def conjugate(A): return [[z.conjugate() for z in row] for row in A]
def transpose(A): return [list(row) for row in zip(*A)]
def adjoint(A): return transpose(conjugate(A))
def multiply(A,B):
    return [[sum(A[i][k]*B[k][j] for k in range(len(A))) for j in range(len(A))] for i in range(len(A))]
def expectation(A,B):
    d=len(A)
    return sum(A[i][j]*B[i][j] for i in range(d) for j in range(d))/d

def check(d):
    delta=1 if d%2==0 else 0
    order=list(range(d))
    order[-2],order[-1]=order[-1],order[-2]
    omega=exp(2j*pi/d)
    roots=[exp(1j*pi*(2*k+delta)/d) for k in order]
    coeff=[(-1)**(l-1)*exp(1j*pi*l*(l-1)/d)/(d*sin(pi*(l-.5)/d)) for l in range(d)]
    alice=[conjugate(shift([exp(-1j*pi*l*(l-1+delta)/d)*omega**(-l*k) for k in order])) for l in range(d)]
    bob=[]
    for y in range(d):
        raw=[1+omega**y*z for z in roots]
        bob.append(conjugate(shift([z/abs(z) for z in raw])))
    bob.append(shift([1+0j]*d))
    matrix_error=max(abs(expectation(alice[l],bob[y])-coeff[l]*omega**(-l*y)) for l in range(d) for y in range(d))
    extra_error=max(abs(expectation(alice[l],bob[-1])-(1 if l==0 else 0)) for l in range(d))
    residual_error=0
    for l in range(d):
        b_hat=[[sum(omega**(l*y)*bob[y][i][j] for y in range(d)) for j in range(d)] for i in range(d)]
        product=multiply(alice[l],transpose(b_hat))
        err=sqrt(sum(abs((d*coeff[l] if i==j else 0)-product[i][j])**2 for i in range(d) for j in range(d))/d)
        residual_error=max(residual_error,err)
    def score(B):
        return (sum(coeff[l].conjugate()*sum(omega**(l*y)*expectation(alice[l],B[y]) for y in range(d)) for l in range(d))+expectation(alice[0],B[-1])).real
    inverted=[adjoint(B) for B in bob]
    result={'dimension':d,'correlator_max_abs_error':matrix_error,'extra_column_max_abs_error':extra_error,'SOS_vector_max_norm_error':residual_error,'original_score':score(bob),'Bob_adjoint_with_unchanged_functional':score(inverted),'Bob_adjoint_with_transported_functional':score([adjoint(B) for B in inverted])}
    assert matrix_error<1e-10 and extra_error<1e-10 and residual_error<1e-10
    assert abs(result['original_score']-(d+1))<1e-10
    assert abs(result['Bob_adjoint_with_transported_functional']-(d+1))<1e-10
    if d>2: assert abs(result['Bob_adjoint_with_unchanged_functional'])<1e-10
    return result

if __name__=='__main__':
    report={'status':'passed','scope':'Finite floating-point sanity check only; independent manuscript formulas, not a substitute for Lean.','results':[check(d) for d in range(2,9)]}
    Path(__file__).with_suffix('.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))
