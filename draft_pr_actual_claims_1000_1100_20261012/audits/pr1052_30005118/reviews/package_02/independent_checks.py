#!/usr/bin/env python3
"""Fresh independent exhaustive language/certificate checks; no candidate imports."""
from itertools import combinations_with_replacement
import json

def need(ok,msg):
    if not ok: raise RuntimeError(msg)
def subset(mask):
    return tuple(i for i in range(mask.bit_length()) if mask>>i&1)
def sumset(a,n=None):
    return frozenset((x+y if n is None else (x+y)%n) for x,y in combinations_with_replacement(a,2))
def census(n):
    # Accumulate the sumset at insertion of the largest new bit, independently
    # of the paper's anchor mechanism or any shipped implementation.
    sums=[0]*(1<<n)
    for mask in range(1,1<<n):
        x=mask.bit_length()-1; rest=mask^(1<<x)
        sums[mask]=sums[rest]
        for y in subset(mask): sums[mask]|=1<<((x+y)%n)
    return sums

def main():
    roots=strong=even=targets=0; tables={}
    for n in list(range(1,16))+[17]:
        sm=census(n);tables[n]=set(sm);roots+=len(sm)
        for mask,bits in enumerate(sm):
            a=subset(mask);b=subset(bits)
            need(len(a)<=len(b),'cardinality')
            if b and b[0]==0 and 2*b[-1]<n:
                if n%2:
                    need(0 in a and set(a)<=set(b) and sumset(a)==set(b),'all canonical roots');strong+=1
                elif a:
                    # Independent even-order existence control, not the odd theorem.
                    anchor=next(x for x in a if (-x)%n in a)
                    shifted=tuple(sorted((x-anchor)%n for x in a))
                    need(2*anchor%n==0 and sumset(shifted)==set(b),'even translated root');even+=1
        if n%2:
            m=(n-1)//2
            integer={sumset(subset(k)) for k in range(1<<(m+1))}
            for k in range(1<<(m+1)):
                if not k&1:continue
                b=frozenset(subset(k));need((k in tables[n])==(b in integer),'all anchored target languages');targets+=1
    signed=0; restricted=0
    integer_roots={sumset(tuple(i-2 for i in subset(mask))) for mask in range(1<<5)}
    for mask in range(1<<9):
        s=frozenset(i-4 for i in subset(mask));is_yes=s in integer_roots
        if not s:n,b=3,frozenset()
        elif min(s)%2:n,b=5,frozenset([0,1])
        else:b=frozenset(x-min(s) for x in s);n=max(3,2*max(b)+1)
        need(((sum(1<<x for x in b)) in tables[n])==is_yes,'total signed map');signed+=1
        rb=b if s else frozenset([0]);need(n%2 and 0 in rb and all(2*x<n for x in rb),'restricted syntax')
        need((sum(1<<x for x in rb) in tables[n])==is_yes,'restricted total map');restricted+=1
    sidon=0
    def prime(n):return n>=2 and all(n%d for d in range(2,int(n**.5)+1))
    for q in range(1,151):
        if q==1: a=[0]
        else:
            p=next(p for p in range(max(3,q),2*q) if p%2 and prime(p))
            a=[2*p*x+x*x%p for x in range(q)]
        z=[x+y for x,y in combinations_with_replacement(a,2)]
        need(len(z)==len(set(z)) and len(a)==q and 0<=min(a)<=max(a)<4*q*q,'Sidon size/range/diagonals');sidon+=1
    a,u,s=5**5,5**6,5**7
    special={a,u,s-a,s-u};extra=sorted(sumset(special)-{2*a,2*s-2*a,2*s-2*u,s})
    fillers={4*5**8}
    for e,j in zip(extra,[5**k for k in range(5)]):fillers.update([e-j,j])
    I=special|fillers
    ordered=[x+y for x in I for y in I]
    need([ordered.count(z) for z in [2*a,2*s-2*a,2*s-2*u,s]]==[1,1,1,4],'skeleton multiplicities')
    need(set(extra)<=sumset(fillers) and not special&fillers,'skeleton filler/disjointness')
    need(8*max(I)+2==12500002<2**24 and 512*16**2==2**17,'range constants')
    need(2**24*2**17*(2**8*7**2)**2==2**57*7**4,'source composition')
    need(sumset([3],5)=={1} and sumset([3])!={1},'missing normalization')
    need(sumset([2],4)=={0} and sumset([2])!={0},'even root')
    need(sumset([1,4],5)=={0,2,3} and frozenset([0,2,3]) not in {sumset(subset(m)) for m in range(1<<4)},'weak strict bound')
    need(sumset([1,3],4)=={0,2} and sumset([1,3])!={0,2},'equality endpoint')
    need({(1+4)%5}=={0} and 0 not in [1,4],'distinct summands')
    huge=( -(1<<12000), -(1<<12000)+(1<<6000))
    S=sumset(huge); t=min(S);B={x-t for x in S};A={x-t//2 for x in huge}; n=2*max(B)+1
    need(sumset(A)==B and sumset(A,n)==B and n.bit_length()==6003,'huge signed binary normalization')
    return {'all_passed':True,'cyclic_roots':roots,'odd_every_canonical_root_checks':strong,'even_translated_root_controls':even,'anchored_target_language_checks':targets,'signed_total_maps':signed,'restricted_outputs':restricted,'repaired_Sidon_sizes':sidon,'skeleton_constants_checked':True,'huge_binary_modulus_bits':n.bit_length(),'finite_corroboration_only':True}
if __name__=='__main__':print(json.dumps(main(),indent=2,sort_keys=True))
