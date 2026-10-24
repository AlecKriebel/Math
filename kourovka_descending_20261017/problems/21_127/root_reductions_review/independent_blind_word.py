#!/usr/bin/env python3
"""Independent certificate: expand the word, apply signed transvection column updates.
No general matrix multiplication or matrix inversion is imported from the author.
"""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json

def inverse(word):return tuple((x,-s) for x,s in reversed(word))
def comm(x,y):return x+y+inverse(x)+inverse(y)
def gen(x):return ((x,1),)
LOC={'a':(1,2),'b':(3,4),'c':(0,1),'d':(2,3)}
def image(word):
    m=[[int(i==j) for j in range(5)] for i in range(5)]
    for x,sign in word:
        i,j=LOC[x]
        # Right multiplying by I+sign*E_ij updates only column j.
        for row in range(5):m[row][j]+=sign*m[row][i]
    return m

def main():
    folder=Path(__file__).resolve().parent;src=folder.parent/'root_reductions'
    old=json.loads((src/'free_image_blind_certificate.json').read_text())
    identity=image(())
    for x in LOC:assert image(gen(x))==old['generators'][x]
    relations={x+y:image(comm(gen(x),gen(y))) for x,y in [('a','b'),('b','c'),('c','d')]}
    assert relations==old['relators']
    assert all(x==identity for x in relations.values())
    p=comm(gen('a'),gen('c'));q=comm(gen('b'),gen('d'));u=comm(p,q)
    assert image(p)==old['inner_commutators']['[a,c]']
    assert image(q)==old['inner_commutators']['[b,d]']
    expected=[row[:] for row in identity];expected[0][4]=1
    assert image(u)==old['word_image']==expected!=identity
    # Coordinate proof also sees exactly the central translation produced.
    for N in [1,2,3,5,7,11]:
        predicted=[row[:] for row in identity];predicted[0][4]=N
        assert image(u*N)==predicted
    output={'utc':datetime.now(timezone.utc).isoformat(),'status':'PASS','method':'Expanded generator words and signed elementary-transvection column updates','word_letters':len(u),'word_expanded':''.join(x if s>0 else x.upper() for x,s in u),'relators_identity':True,'inner_commutators_match':True,'image_u_is_I_plus_E15':True,'powers_checked':[1,2,3,5,7,11],'input_sha256':{name:hashlib.sha256((src/name).read_bytes()).hexdigest() for name in ['FREE_IMAGE_BLIND_WORD.md','verify_free_image_blind.py','free_image_blind_certificate.json']}}
    (folder/'blind_word_reproduction.json').write_text(json.dumps(output,indent=2)+'\n')
    print(json.dumps(output,indent=2))
if __name__=='__main__':main()
