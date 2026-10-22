#!/usr/bin/env python3
"""Exact finite-identity audit; not a formal proof of the analytic report."""
import json
import sys
from fractions import Fraction as F
from math import comb

class Invalid(ValueError):
    pass

def need(condition, message):
    if not condition:
        raise Invalid(message)

def pairs_no_duplicates(items):
    out = {}
    for key, value in items:
        need(key not in out, "duplicate JSON key")
        out[key] = value
    return out

def forbidden_constant(value):
    raise Invalid("non-finite JSON constant")

def load(raw):
    need(len(raw) <= 100000, "input too large")
    return json.loads(raw, object_pairs_hook=pairs_no_duplicates,
                      parse_constant=forbidden_constant)

def integer(x, low, high, name):
    need(type(x) is int, name + ": exact integer required")
    need(low <= x <= high, name + ": integer out of range")
    return x

def exact_keys(obj, keys, name):
    need(type(obj) is dict, name + ": object required")
    need(set(obj) == set(keys), name + ": unexpected/missing keys")

def rational(v, name):
    need(type(v) is list and len(v) == 2, name + ": rational pair required")
    a = integer(v[0], -1000000, 1000000, name)
    b = integer(v[1], 1, 1000000, name)
    need(F(a,b).numerator == a and F(a,b).denominator == b,
         name + ": noncanonical rational")
    return F(a,b)

def validate(d):
    exact_keys(d, ["schema_version", "problem_id", "approaches_counted",
        "searches_counted", "status", "energy_max_terms", "landau_max_index",
        "fejer_max_index", "rudin_shapiro_max_depth", "quadratic"], "root")
    for name, value in [("schema_version",1), ("problem_id",2304003),
                        ("approaches_counted",5), ("searches_counted",0)]:
        integer(d[name], value, value, name)
    need(type(d["status"]) is str and d["status"] == "PARTIAL_PROGRESS_UNRESOLVED",
         "incorrect status")
    integer(d["energy_max_terms"], 2, 100, "energy_max_terms")
    integer(d["landau_max_index"], 1, 100, "landau_max_index")
    integer(d["fejer_max_index"], 1, 100, "fejer_max_index")
    integer(d["rudin_shapiro_max_depth"], 1, 12, "rudin_shapiro_max_depth")
    q=d["quadratic"]
    exact_keys(q,["coefficients","normalization_squared","cut",
                  "slack_coefficients","objective_squared"],"quadratic")
    for name in ["coefficients","slack_coefficients"]:
        need(type(q[name]) is list and len(q[name]) == 3, name+": three entries required")
        for x in q[name]: integer(x,-1000000,1000000,name)
    integer(q["normalization_squared"],1,1000000,"normalization_squared")
    integer(q["cut"],2,2,"cut")
    rational(q["objective_squared"],"objective_squared")
    return d

def cmul(x,y):
    # Q(sqrt(-3)): (a,b) denotes a+b*sqrt(-3).
    a,b=x; c,d=y
    return (a*c-3*b*d, a*d+b*c)

def cadd(x,y): return (x[0]+y[0],x[1]+y[1])
def cconj(x): return (x[0],-x[1])
def cpow(x,n):
    v=(F(1),F(0))
    for _ in range(n): v=cmul(v,x)
    return v

def autocorr(a):
    return [sum(a[j]*a[j+k] for j in range(len(a)-k)) for k in range(len(a))]

def audit(d):
    counts={}
    count=0
    for N in range(2,d["energy_max_terms"]+1):
        for k in range(1,N):
            l=N-k
            # Quadratic is N*x^2-2*k*x+k*(1-l); reduced discriminant.
            need(k*k-N*k*(1-l)==k*l*(N-1),"energy discriminant")
            need(k*l*(N-1) >= l*l,"energy larger root is >=1")
            count+=1
    counts["energy_discriminants"]=count
    count=0
    for r in range(d["landau_max_index"]+1):
        c=[F(comb(2*j,j),4**j) for j in range(r+1)]
        for j in range(r+1):
            need(sum(c[t]*c[j-t] for t in range(j+1))==1,"Landau convolution")
            count+=1
        if r>0: need(sum(x*x for x in c)>1,"Landau strict comparison")
    counts["landau_coefficients"]=count
    for s in range(1,d["fejer_max_index"]+1):
        p={}
        for j in range(1,s+1,2):
            w=F(s+1-j,(s+1)*j)
            p[s+j]=w; p[s-j]=-w
        need(len(p)==2*((s+1)//2),"Fejer support count")
        need(all(0<=e<=2*s and a!=0 for e,a in p.items()),"Fejer support")
        need(sum(p.values())==0,"Fejer value at one")
        B=sum(F(1,j) for j in range(1,s+1,2))-F((s+1)//2,s+1)
        need(-sum(a for e,a in p.items() if e<s)==B,"Fejer partial sum")
        H=sum(F(1,j) for j in range(1,s+1))
        Hhalf=sum(F(1,j) for j in range(1,s//2+1))
        need(B==H-Hhalf/2-F((s+1)//2,s+1),"Fejer harmonic identity")
        # Check the exact triangular Fourier multiplier of K_s.
        for j in range(s+1):
            pairs=sum(1 for a in range(s+1) for b in range(s+1) if a-b==j)
            need(F(pairs,s+1)==1-F(j,s+1),"Fejer kernel multiplier")
    counts["fejer_polynomials"]=d["fejer_max_index"]
    q=d["quadratic"]; a,b,c=q["coefficients"]; den=q["normalization_squared"]
    slack=[den-(a-c)**2-b*b,-2*b*(a+c),-4*a*c]
    need(slack==q["slack_coefficients"],"quadratic norm identity")
    need(slack==[2,-8,8],"quadratic square completion")
    need(F((a+b)**2,den)==rational(q["objective_squared"],"objective_squared"),
         "quadratic objective identity")
    need(rational(q["objective_squared"],"objective_squared")==F(4,3),
         "quadratic sharp value")
    omega=(F(1,2),F(1,2)); u=(F(1,2),F(-1,6))
    for j,target in enumerate([1,1,0]):
        t=cmul(u,cpow(omega,j))
        need(cadd(t,cconj(t))==(F(target),F(0)),"quadratic dual reproduction")
    need(cmul(u,cconj(u))==(F(1,3),F(0)),"quadratic dual mass")
    counts["quadratic_primal_dual_certificates"]=1
    R=S=[1]
    for depth in range(d["rudin_shapiro_max_depth"]+1):
        N=2**depth
        need(len(R)==len(S)==N,"complementary lengths")
        need(all(x in (-1,1) for x in R+S),"complementary signs")
        ar=autocorr(R); ass=autocorr(S)
        need(ar[0]+ass[0]==2*N,"complementary constant coefficient")
        need(all(x+y==0 for x,y in zip(ar[1:],ass[1:])),"complementary autocorrelations")
        need(sum(R)>=0 and sum(x==1 for x in R)*2>=N,"subset lower count")
        R,S=R+S,R+[-x for x in S]
    counts["complementary_pairs"]=d["rudin_shapiro_max_depth"]+1
    return {"ok":True,"schema_version":1,"problem_id":2304003,
            "status":"PARTIAL_PROGRESS_UNRESOLVED","exact_arithmetic":True,
            "counts":counts,"analytic_proof_mechanized":False}

def main():
    need(len(sys.argv)==2,"usage: verify.py fixtures.json | --stdin")
    if sys.argv[1]=="--stdin": raw=sys.stdin.buffer.read(100001)
    else:
        with open(sys.argv[1],"rb") as stream: raw=stream.read(100001)
    result=audit(validate(load(raw)))
    print(json.dumps(result,sort_keys=True,allow_nan=False))

if __name__=="__main__":
    try:
        main()
    except (Invalid, ValueError, TypeError, KeyError, OSError, UnicodeError) as exc:
        print(json.dumps({"ok":False,"error":str(exc)},allow_nan=False),file=sys.stderr)
        sys.exit(1)
