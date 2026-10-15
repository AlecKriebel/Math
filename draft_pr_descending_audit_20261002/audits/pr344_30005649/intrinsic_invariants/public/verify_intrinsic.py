#!/usr/bin/env python3
"""Read-only independent controls for a cyclic-word duality obstruction.

Standard library only. No imports from candidate code and no filesystem writes.
The universal proof is in report.md; finite controls do not certify universality.
"""
import argparse
import hashlib
import json
from pathlib import Path
import random
import sys

class Field:
    def __init__(self, p, modulus):
        self.p, self.modulus = p, modulus
        self.degree = len(modulus) - 1
        assert modulus[-1] == 1
        self.q = p ** self.degree
        self.digits = [self.decode(i) for i in range(self.q)]
        self.add_table = [[self.encode([(u+v) % p for u,v in zip(a,b)]) for b in self.digits] for a in self.digits]
        self.mul_table = [[self.product_raw(a,b) for b in self.digits] for a in self.digits]
        self.sigma = [self.power(a,p) for a in range(self.q)]
        self.tau = [self.power(a,p**(self.degree-1)) for a in range(self.q)]
        self.inverses = [None] + [self.power(a,self.q-2) for a in range(1,self.q)]
        # This exhaustive finite-field control fails if the modulus is reducible.
        assert all(self.mul(a,self.inverses[a]) == 1 for a in range(1,self.q))
        assert all(self.tau[self.sigma[a]] == a == self.sigma[self.tau[a]] for a in range(self.q))

    def decode(self, a):
        out=[]
        for _ in range(self.degree): out.append(a % self.p); a //= self.p
        return out

    def encode(self, digits):
        return sum(a * self.p**i for i,a in enumerate(digits))

    def product_raw(self, a, b):
        d=[0]*(2*self.degree-1)
        for i,x in enumerate(a):
            for j,y in enumerate(b): d[i+j]=(d[i+j]+x*y) % self.p
        for i in range(len(d)-1,self.degree-1,-1):
            coefficient=d[i]
            for j in range(self.degree):
                d[i-self.degree+j]=(d[i-self.degree+j]-coefficient*self.modulus[j]) % self.p
        return self.encode(d[:self.degree])

    def add(self,a,b): return self.add_table[a][b]
    def mul(self,a,b): return self.mul_table[a][b]
    def neg(self,a): return self.encode([(-v) % self.p for v in self.digits[a]])
    def sub(self,a,b): return self.add(a,self.neg(b))
    def power(self,a,n):
        result=1
        while n:
            if n & 1: result=self.mul(result,a)
            a=self.mul(a,a); n >>= 1
        return result

def zeros(rows,cols): return [[0 for _ in range(cols)] for _ in range(rows)]
def eye(d): return [[int(i==j) for j in range(d)] for i in range(d)]
def transpose(a): return [list(row) for row in zip(*a)]
def join(a,b): return [x+y for x,y in zip(a,b)]
def basis(d,indices): return [[int(i==j) for j in indices] for i in range(d)]
def from_integers(a,k): return [[x % k.p for x in row] for row in a]
def twist(a,automorphism): return [[automorphism[x] for x in row] for row in a]
def dot(x,y,k):
    s=0
    for a,b in zip(x,y): s=k.add(s,k.mul(a,b))
    return s
def multiply(a,b,k):
    bt=transpose(b)
    return [[dot(row,col,k) for col in bt] for row in a]
def integer_multiply(a,b):
    return [[sum(x*y for x,y in zip(row,col)) for col in transpose(b)] for row in a]
def act(a,x,automorphism,k): return [dot(row,[automorphism[v] for v in x],k) for row in a]

def rank(a,k):
    a=[row[:] for row in a]
    pivot=0
    for column in range(len(a[0])):
        row=next((r for r in range(pivot,len(a)) if a[r][column]),None)
        if row is None: continue
        a[row],a[pivot]=a[pivot],a[row]
        scale=k.inverses[a[pivot][column]]
        a[pivot]=[k.mul(scale,x) for x in a[pivot]]
        for r in range(len(a)):
            if r != pivot and a[r][column]:
                scale=a[r][column]
                a[r]=[k.sub(x,k.mul(scale,y)) for x,y in zip(a[r],a[pivot])]
        pivot += 1
        if pivot == len(a): break
    return pivot

def word_module(word):
    d=len(word); f=zeros(d,d); v=zeros(d,d)
    for i,letter in enumerate(word):
        j=(i+1) % d
        if letter == "F": f[j][i]=1
        elif letter == "V": v[i][j]=1
        else: raise AssertionError("unknown letter")
    return f,v

def direct_sum(a,b):
    m=len(a); n=len(b); out=zeros(m+n,m+n)
    for i in range(m): out[i][:m]=a[i]
    for i in range(n): out[m+i][m:]=b[i]
    return out

def dual(f,v,k):
    # Formula derived from evaluation, with twists retained even for nonprime coefficients.
    return transpose(twist(v,k.sigma)), transpose(twist(f,k.tau))

def invariants(f,v,k):
    f2=multiply(f,twist(f,k.sigma),k)
    v2=multiply(v,twist(v,k.tau),k)
    fd,vd=dual(f,v,k)
    fd2=multiply(fd,twist(fd,k.sigma),k)
    vd2=multiply(vd,twist(vd,k.tau),k)
    return {"rank_F":rank(f,k), "rank_V":rank(v,k),
            "rank_F2":rank(f2,k), "rank_V2":rank(v2,k),
            "delta2":rank(f2,k)+rank(v2,k)-rank(join(f2,v2),k),
            "dual_delta2":rank(fd2,k)+rank(vd2,k)-rank(join(fd2,vd2),k),
            "dual_kernel_formula":rank(f2,k)+rank(v2,k)-rank(join(transpose(f2),transpose(v2)),k)}

def check_pairing(f,v,fd,vd,k,x,phi):
    left_f=dot(act(fd,phi,k.sigma,k),x,k)
    right_f=k.sigma[dot(phi,act(v,x,k.tau,k),k)]
    left_v=dot(act(vd,phi,k.tau,k),x,k)
    right_v=k.tau[dot(phi,act(f,x,k.sigma,k),k)]
    return left_f == right_f and left_v == right_v

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--spec", type=Path, default=Path(__file__).with_name("construction.json"))
    args=ap.parse_args()
    raw=args.spec.read_bytes(); spec=json.loads(raw)
    f,v=word_module(spec["word"])
    assert spec["word"] == "FFVFVV"
    T=transpose(spec["qss_columns"])
    Ti=transpose(spec["inverse_columns"])
    assert integer_multiply(T,Ti) == eye(6) == integer_multiply(Ti,T)
    fn=integer_multiply(integer_multiply(Ti,f),T)
    vn=integer_multiply(integer_multiply(Ti,v),T)
    assert integer_multiply(f,v) == zeros(6,6) == integer_multiply(v,f)
    assert integer_multiply(integer_multiply(f,f),f) == zeros(6,6)
    assert integer_multiply(integer_multiply(v,v),v) == zeros(6,6)
    for a in (fn,vn):
        for end in (2,4): assert all(a[i][j] == 0 for i in range(end,6) for j in range(end))
        for begin in (0,2,4): assert [row[begin:begin+2] for row in a[begin:begin+2]] == [[0,0],[1,0]]
    positive=[]; primes=[]
    i_f,i_v=word_module("FV")
    for p in spec["prime_controls"]:
        k=Field(p,[0,1]); row={"p":p,"n":[]}
        for n in spec["n_controls"]:
            ff=[r[:] for r in f]; vv=[r[:] for r in v]
            indices=spec["honda_basis_indices"][:]
            for _ in range(n-3):
                indices.append(len(ff)); ff=direct_sum(ff,i_f); vv=direct_sum(vv,i_v)
            ll=basis(len(ff),indices)
            inv=invariants(ff,vv,k)
            assert inv["delta2"] == 0 and inv["dual_delta2"] == 1 and inv["dual_kernel_formula"] == 1
            assert inv["rank_F"] == n == inv["rank_V"]
            assert rank(join(ff,ll),k) == 2*n
            assert rank(multiply(vv,ll,k),k) == n
            row["n"].append({"n":n,**inv})
        primes.append(row)
        for word,perm,lidx in [("FV",[1,0],[0]),("FFVV",[2,3,0,1],[0,3])]:
            ff,vv=word_module(word); fd,vd=dual(ff,vv,k); d=len(ff)
            aa=[[int(i==perm[j]) for j in range(d)] for i in range(d)]
            assert multiply(aa,ff,k) == multiply(fd,twist(aa,k.sigma),k)
            assert multiply(aa,vv,k) == multiply(vd,twist(aa,k.tau),k)
            assert rank(aa,k) == d
            # Honda dual subspace is the annihilator of L in evaluation coordinates.
            ll=basis(d,lidx); image=multiply(aa,ll,k)
            assert multiply(transpose(ll),image,k) == zeros(len(lidx),len(lidx))
            assert rank(image,k) == len(lidx)
            positive.append({"p":p,"word":word,"module_and_this_Honda_lift_self_dual":True,**invariants(ff,vv,k)})
    field_spec=spec["odd_degree_field"]
    k=Field(field_spec["prime"],field_spec["modulus_low_to_high"])
    assert k.degree == 3 and k.sigma[k.p] != k.tau[k.p]
    scales=[k.power(k.p,i+1) for i in range(6)]
    b=[[scales[i] if i==j else 0 for j in range(6)] for i in range(6)]
    bi=[[k.inverses[scales[i]] if i==j else 0 for j in range(6)] for i in range(6)]
    ff=multiply(multiply(bi,f,k),twist(b,k.sigma),k)
    vv=multiply(multiply(bi,v,k),twist(b,k.tau),k)
    fd,vd=dual(ff,vv,k)
    iv=invariants(ff,vv,k)
    assert iv["delta2"] == 0 and iv["dual_delta2"] == 1
    wrong_fd,wrong_vd=transpose(vv),transpose(ff)
    failures_plain_transpose=0; failures_wrong_direction=0; pairs=0
    for i in range(6):
        for j in range(6):
            for coefficient in range(k.q):
                x=[0]*6; phi=[0]*6; x[i]=coefficient; phi[j]=1
                assert check_pairing(ff,vv,fd,vd,k,x,phi)
                failures_plain_transpose += int(not check_pairing(ff,vv,wrong_fd,wrong_vd,k,x,phi))
                # On degree three, replacing inverse Frobenius with Frobenius is detectably wrong.
                left_v=dot(act(vd,phi,k.tau,k),x,k)
                wrong_right_v=k.sigma[dot(phi,act(ff,x,k.sigma,k),k)]
                failures_wrong_direction += int(left_v != wrong_right_v)
                pairs += 1
    rng=random.Random(30005649)
    for _ in range(256):
        x=[rng.randrange(k.q) for _ in range(6)]; phi=[rng.randrange(k.q) for _ in range(6)]
        assert check_pairing(ff,vv,fd,vd,k,x,phi)
        assert act(ff,act(vv,x,k.tau,k),k.sigma,k) == [0]*6
        assert act(vv,act(ff,x,k.sigma,k),k.tau,k) == [0]*6
        pairs += 1
    assert failures_plain_transpose > 0 and failures_wrong_direction > 0
    # Breaking a word edge is rejected by the exactness rank control.
    mutant=[r[:] for r in v]; mutant[5][0]=0
    pk=Field(5,[0,1]); assert rank(f,pk)+rank(mutant,pk) != 6
    result={"status":"pass", "interpreter":{"executable":sys.executable,"version":sys.version},
            "spec_sha256":hashlib.sha256(raw).hexdigest(),
            "integer_basis_and_qss_identities":True,"prime_controls":primes,"low_rank_controls":positive,
            "odd_degree_semilinearity":{"q":k.q,"frobenius_exponent":k.p,"inverse_exponent":k.p**2,
               "basis_changed_nonprime_coefficients":True,"pair_controls":pairs,
               "plain_transpose_mutant_failures":failures_plain_transpose,
               "wrong_inverse_direction_mutant_failures":failures_wrong_direction,**iv},
            "broken_edge_exactness_mutant_rejected":True,
            "limitation":"Finite controls supplement report.md; they do not prove universality or novelty."}
    print(json.dumps(result,indent=2))

if __name__ == "__main__": main()
