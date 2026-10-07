#!/usr/bin/env python3
"""Exact arithmetic diagnostics; no convex-realizability or theorem certification."""
import json
from fractions import Fraction

def require(value,message):
    if not value: raise ValueError(message)

def face_vector(m):
    require(type(m) is int and m>=4,'cube dimension must be an integer >=4')
    n=2**m;e=m*2**(m-1);c=(m-2)*2**(m-2)
    return [n,e,3*c,c]

def validate(m,f):
    require(len(f)==4 and all(type(x) is int and x>0 for x in f),'invalid face counts')
    n,e,s,c=f
    require(n==2**m,'vertex-count mismatch')
    require(2*e==m*n,'cube-graph edge-count mismatch')
    require(2*s==6*c,'ridge-facet incidence mismatch')
    require(n-e+s-c==0,'Euler mismatch')
    return c

def main():
    counts=[]
    for m in range(4,25):
        f=face_vector(m);c=validate(m,f)
        require(Fraction(c,f[0])==Fraction(m-2,4),'ratio mismatch')
        require((c>=2*f[0])==(m>=10),'threshold mismatch')
        counts.append({'m':m,'f':f})
    require(face_vector(10)==[1024,5120,6144,2048],'witness mismatch')
    require(face_vector(9)[3]<2*face_vector(9)[0],'lower threshold case')
    require(face_vector(11)[3]>2*face_vector(11)[0],'upper threshold case')
    rejects=0
    for mutant in [[1024,5120,6144,2047],[1024,5120,7680,2560],[512,5120,6144,2048],[1024,10240,6144,2048]]:
        try:validate(10,mutant)
        except ValueError: rejects+=1
        else:raise ValueError('mutant accepted')
    for bad in [3,0,-1,4.0,True]:
        try:face_vector(bad)
        except ValueError:rejects+=1
        else:raise ValueError('invalid dimension accepted')
    # Independent integer arithmetic in the triangulated-boundary upper argument.
    # Enumerating these feasible numeric pairs is not classifying realizable spheres.
    ub_cases=0
    for n in range(5,65):
        for e in range(n,n*(n-1)//2+1):
            t=e-n;f2=2*t;d=t//2
            require(n-e+f2-t==0,'triangulated Euler identity')
            require(2*d<=t and d<=n*(n-3)//4,'coarse upper bound')
            ub_cases+=1
    # Published regular-subdivision formulas: arithmetic only.
    regular=[]
    for k in [3,5,7,9]:
        l=k;n=2*k*l+2+l*l;b=(2*k-2)*l*l
        require(n==3*k*k+2 and b==2*k**3-2*k*k,'regular-subdivision count mismatch')
        regular.append({'k':k,'l':l,'points':n,'bipyramidal_cells':b})
    print(json.dumps({'result':'PASS','cube_family_cases':len(counts),'threshold_witness':face_vector(10),'rejected_mutants':rejects,'upper_bound_integer_cases':ub_cases,'regular_subdivision_arithmetic':regular,'scope':'Arithmetic consequences only; external construction theorem and mathematical proof require review.'},sort_keys=True))
if __name__=='__main__':main()
