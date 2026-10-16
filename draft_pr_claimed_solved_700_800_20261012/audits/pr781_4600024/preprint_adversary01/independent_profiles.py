"""Independent ternary endpoint/profile controls; no candidate imports."""
from itertools import product
import json
def need(c,m):
    if not c: raise ValueError(m)
def profiles(w,k):
    left=k//2;right=k-left
    return frozenset((w[max(0,i-left):i],w[i:i+right]) for i in range(len(w)))
def main():
    checked=0;groups=0;examples=[]
    for k in range(1,5):
        signatures={}
        for n in range(max(2*k,1),9):
            for letters in product("abc",repeat=n):
                w="".join(letters)
                key=(w[:k-1],w[-(k-1):] if k>1 else "",frozenset(w[i:i+k] for i in range(n-k+1)))
                p=profiles(w,k)
                need(key not in signatures or signatures[key]==p,"Endpoint/factor implication failed")
                signatures[key]=p;checked+=1
        groups+=len(signatures)
    # Losing endpoint data really changes the result.
    v,w="01010","010101"
    factors=lambda x:frozenset(x[i:i+3] for i in range(len(x)-2))
    need(factors(v)==factors(w) and profiles(v,3)!=profiles(w,3),"Missing-boundary negative control did not discriminate")
    # A nonmixing irreducible period-two graph has all long alternating words.
    for n in range(2,15):
        need(set(("01"*n)[i:i+2] for i in range(2*n-1))=={"01","10"},"Periodic control")
    print(json.dumps({"result":"PASS","ternary_long_words":checked,"signature_classes":groups,
                      "boundary_mutation_detected":True,"nonmixing_controls":13,
                      "scope":"Finite diagnostics of the published convention, not a general proof."},sort_keys=True))
if __name__=="__main__":main()
