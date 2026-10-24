#!/usr/bin/env python3
"""Independent check by absolute exponent/carrying, not cyclic-state edge rewriting."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib,json

def red(seq):
    out=[]
    for s in seq:
        if out and out[-1]==-s:out.pop()
        else:out.append(s)
    return tuple(out)

def words(maxlen):
    frontier=[()]
    yield ()
    for _ in range(maxlen):
        frontier=[w+(s,) for w in frontier for s in (1,-1,2,-2) if not w or w[-1]!=-s]
        yield from frontier

def inverse(word):return tuple(-x for x in reversed(word))
def abstract_rewrite(w,m):
    # Keep full integer a exponent s, rather than the coset vertex alone.
    # Each b at height s=q*m+r is u^q v_r u^-q, with u=a^m.
    exponent=0;out=[]
    for letter in w:
        if abs(letter)==1:exponent+=letter
        else:
            quotient,residue=divmod(exponent,m)
            upow=[1 if quotient>=0 else -1]*abs(quotient)
            out+=upow+[residue+2 if letter>0 else -(residue+2)]+list(inverse(upow))
    quotient,residue=divmod(exponent,m)
    out += [1 if quotient>=0 else -1]*abs(quotient)
    return red(out),residue

def basis_expand(word,m):
    result=[]
    for x in word:
        if abs(x)==1:v=(1,)*m
        else:
            j=abs(x)-2
            assert 0<=j<m
            v=(1,)*j+(2,)+(-1,)*j
        result.extend(v if x>0 else inverse(v))
    return red(result)

def main():
    folder=Path(__file__).resolve().parent;source=folder.parent/'virtual_invariants'
    original=json.loads((source/'schreier_checks.json').read_text())
    allwords=list(words(8)); assert len(allwords)==13121
    rows=[]
    for m in range(1,65):
        closed=0
        for w in allwords:
            abstract,r=abstract_rewrite(w,m)
            expanded=basis_expand(abstract,m)
            assert red(expanded+(1,)*r)==w
            assert r==sum(s if abs(s)==1 else 0 for s in w)%m
            closed += (r==0)
        old=next(v for v in original['rows'] if v['index']==m)
        assert old['kernel_words_checked']==closed
        assert old['reduced_words_tested']==len(allwords)
        for j in range(m+1):
            for sign in (-1,1):
                b=(sign*(j+1),)
                rew,r=abstract_rewrite(basis_expand(b,m),m)
                assert r==0 and rew==b
        rows.append({'m':m,'closed_words':closed,'all_words':len(allwords),'cover_rank':m+1})
    out={'utc':datetime.now(timezone.utc).isoformat(),'mechanism':'Absolute a-exponent carrying; conjugate decomposition before reduction; independent implementation','checks':len(allwords)*64,'rows':rows,'status':'PASS','author_program_sha256':hashlib.sha256((source/'check_schreier.py').read_bytes()).hexdigest(),'author_certificate_sha256':hashlib.sha256((source/'schreier_checks.json').read_bytes()).hexdigest()}
    (folder/'independent_schreier.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:out[k] for k in ('utc','checks','mechanism','status')},indent=2))
if __name__=='__main__':main()
