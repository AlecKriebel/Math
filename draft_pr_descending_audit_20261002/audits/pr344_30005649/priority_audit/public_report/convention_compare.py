"""Portable read-only comparison of the submitted module with Kraft's word convention.

Run with Python 3.10+ and its standard library: python3 -B convention_compare.py
This checks finite algebraic identities. It does not establish literature priority
or replace the cited Dieudonne/Honda anti-equivalences.
"""
from fractions import Fraction
import json

def zero(n): return [[0]*n for _ in range(n)]
def eye(n): return [[int(i==j) for j in range(n)] for i in range(n)]
def transpose(a): return [list(x) for x in zip(*a)]
def mul(a,b): return [[sum(x*y for x,y in zip(row,col)) for col in zip(*b)] for row in a]
def matrix(n,arrows):
    a=zero(n)
    for src,dst in arrows: a[dst][src]=1
    return a
def inverse(a):
    n=len(a);b=[[Fraction(x) for x in row+e] for row,e in zip(a,eye(n))]
    for j in range(n):
        k=next(i for i in range(j,n) if b[i][j]);b[j],b[k]=b[k],b[j]
        d=b[j][j];b[j]=[x/d for x in b[j]]
        for i in range(n):
            if i!=j:
                d=b[i][j];b[i]=[x-d*y for x,y in zip(b[i],b[j])]
    return [r[n:] for r in b]
def rotations(w): return [w[j:]+w[:j] for j in range(len(w))]
def from_pries_ulmer_word(w):
    # Their written word is u_(lambda-1)...u_0; u_j indexes edge j.
    f=[];v=[];n=len(w)
    for j,c in enumerate(reversed(w)):
        if c=='f': f.append((j,(j+1)%n))
        elif c=='v': v.append(((j+1)%n,j))
        else: raise ValueError('word must use f and v')
    return matrix(n,f),matrix(n,v)

def verify():
    f=matrix(6,[(0,1),(1,2),(3,4)])
    v=matrix(6,[(0,5),(3,2),(5,4)])
    word='vvfvff';fw,vw=from_pries_ulmer_word(word)
    assert (f,v)==(fw,vw), 'word does not match literal candidate matrices'
    assert (f,v)!=from_pries_ulmer_word('ffvfvv'), 'reversal convention control'
    assert mul(f,v)==mul(v,f)==zero(6)
    assert mul(mul(f,f),f)==mul(mul(v,v),v)==zero(6)
    complement=word.translate(str.maketrans('fv','vf'))
    assert complement not in rotations(word)
    assert all(word!=word[:d]*(6//d) for d in [1,2,3])
    # Classical integral cyclic completion: an F edge has coefficient1,
    # a V edge coefficientp for F. Iterate monomial exponents, not sampled p.
    edge=list(reversed(word));cycle_exponents=[]
    for start in range(6):
        j=start;power=0
        for _ in range(6):power+=int(edge[j]=='v');j=(j+1)%6
        assert j==start and power==3
        cycle_exponents.append(power)
    assert all(int(c=='v')+int(c=='f')==1 for c in edge) # integralFV=VF=p
    # Columns u,v,w,z,a,b, each fixed by Frobenius in every prime field.
    b=transpose([[0,1,0,1,0,1],[0,0,1,0,1,0],
                 [0,2,0,1,0,0],[0,0,1,0,0,0],
                 [1,0,0,0,0,0],[0,1,0,0,0,0]])
    bi=inverse(b);assert all(x.denominator==1 for row in bi for x in row)
    bi=[[int(x) for x in row] for row in bi]
    assert mul(b,bi)==mul(bi,b)==eye(6)
    nf=mul(mul(bi,f),b);nv=mul(mul(bi,v),b)
    ef=zero(6);ev=zero(6)
    for row,col,c in [(1,0,1),(1,2,1),(3,2,1),(5,4,1),(3,5,1)]:ef[row][col]=c
    for row,col,c in [(1,0,1),(3,2,1),(0,4,1),(2,4,-1),(5,4,1)]:ev[row][col]=c
    assert (nf,nv)==(ef,ev)
    for d in [2,4]:
        assert all(nf[i][j]==nv[i][j]==0 for i in range(d,6) for j in range(d))
    for s in [0,2,4]:
        assert [[nf[i][j] for j in range(s,s+2)] for i in range(s,s+2)]==[[0,0],[1,0]]
        assert [[nv[i][j] for j in range(s,s+2)] for i in range(s,s+2)]==[[0,0],[1,0]]
    # The only nonzero square entries are unit coordinate lines, hence valid
    # over every characteristic. They prove delta=0 versus delta_dual=1.
    assert mul(f,f)==matrix(6,[(0,2)])
    assert mul(v,v)==matrix(6,[(0,4)])
    assert mul(transpose(v),transpose(v))==matrix(6,[(4,0)])
    assert mul(transpose(f),transpose(f))==matrix(6,[(2,0)])
    # Honda complement: im F = <e1,e2,e4>, L = <e0,e3,e5>.
    assert {1,2,4}.isdisjoint({0,3,5}) and {1,2,4}|{0,3,5}==set(range(6))
    assert [next(i for i in range(6) if v[i][j]) for j in [0,3,5]]==[5,2,4]
    return {'status':'PASS','known_module':'M(vvfvff)',
            'forward_edge_labels':'FFVFVV','written_word_convention':'rightmost letter indexes edge 0',
            'complement':complement,'cyclic_rotations':rotations(word),
            'primitive':True,'complement_is_rotation':False,
            'qss_module_dimensions':[0,2,4,6],
            'integral_basis_inverse':bi,'delta':0,'delta_dual':1,
            'Honda_L_basis_indices':[0,3,5],
            'integral_F6_basis_p_exponents':cycle_exponents,
            'integral_F6_coefficients':'sigma^6; basis identity is not an R-linear operator identity',
            'scope':'Exact integer identities; prime-field coefficients are Frobenius-fixed. External classification and historical-priority judgments are not machine-certified.'}

if __name__=='__main__': print(json.dumps(verify(),indent=2))
