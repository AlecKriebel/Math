"""Finite checks of family 004, 03-parity.tex lines 553-703.
These validate generated matrix data only, not elliptic or 2-converse inputs.
Run with Python 3; no third-party libraries needed.
"""
from itertools import product
from random import Random

def rank(matrix):
    rows = [sum(bit << j for j, bit in enumerate(row)) for row in matrix]
    pivot = 0
    for col in range(max((x.bit_length() for x in rows), default=0)):
        hit = next((i for i in range(pivot, len(rows)) if rows[i] >> col & 1), None)
        if hit is None: continue
        rows[pivot], rows[hit] = rows[hit], rows[pivot]
        for i in range(len(rows)):
            if i != pivot and rows[i] >> col & 1: rows[i] ^= rows[pivot]
        pivot += 1
    return pivot

def mv(matrix, vector):
    return [sum(x*y for x,y in zip(row,vector)) % 2 for row in matrix]

def parity_bits(rng, count, target):
    result = [rng.randrange(2) for _ in range(count-1)]
    return result + [(sum(result)+target) % 2]

def one_case(rng, nb, nj):
    ni=nb-1; q0=nb+ni; size=q0+1+nj
    B=list(range(nb)); I=list(range(nb,q0)); J=list(range(q0+1,size))
    s=parity_bits(rng,nb,0)+[0]*ni+[1]
    lam=parity_bits(rng,nb,1)+[0]*ni+[1]
    if nj:
        s += parity_bits(rng,nj,0); lam += parity_bits(rng,nj,0)
    R=[[0]*size for _ in range(size)]
    for group in (B,J):
        for ii, first in enumerate(group):
            for second in group[ii+1:]:
                bit=rng.randrange(2)
                R[first][second]=bit
                R[second][first]=bit^(s[first]&s[second])
    if nj:
        cross=[[0]*nj for _ in B]
        for i in range(nb-1):
            for j in range(nj-1): cross[i][j]=rng.randrange(2)
            cross[i][-1]=sum(cross[i][:-1]) % 2
        for j in range(nj): cross[-1][j]=sum(cross[i][j] for i in range(nb-1)) % 2
        for i,bi in enumerate(B):
            for j,ji in enumerate(J):
                R[bi][ji]=cross[i][j]
                R[ji][bi]=cross[i][j]^(s[bi]&s[ji])
    # C columns e_i+e_last span the even-sum hyperplane also when |B| is even.
    for ii,index in enumerate(I):
        R[ii][index]=R[index][ii]=1
        R[nb-1][index]=R[index][nb-1]=1
    for bi in B:
        bit=sum(R[bi][index] for index in I) % 2
        R[bi][q0]=bit; R[q0][bi]=bit^s[bi]
    def matrices(indices):
        K=[[R[i][j] if i != j else sum(R[i][k] for k in indices if k != i)%2
            for j in indices] for i in indices]
        indicator=[int(i in B) for i in indices]; local_lam=[lam[i] for i in indices]
        assert mv(K,[1]*len(indices)) == [0]*len(indices)
        assert mv(K,indicator) == [0]*len(indices)
        sharp=[[value^(lam[i]&int(j in (0,q0))) for j,value in zip(indices,row)]
               for i,row in zip(indices,K)]
        assert mv(sharp,indicator) == local_lam
        deleted=[[value for j,value in zip(indices,row) if j != q0]
                 for i,row in zip(indices,sharp) if i != q0]
        return K,sharp,deleted,local_lam
    small=list(range(q0+1))
    K,sharp,deleted,L=matrices(small)
    assert rank(deleted)==len(deleted)
    assert rank(K)==len(small)-2
    assert rank([row+[bit] for row,bit in zip(K,L)])==len(small)-1
    successes=0
    for bits in product((0,1),repeat=nj):
        for ji,bit in zip(J,bits): R[ji][q0]=bit; R[q0][ji]=bit^s[ji]
        K,sharp,deleted,L=matrices(list(range(size)))
        if rank(deleted)==len(deleted):
            assert rank(K)==size-2
            assert rank([row+[bit] for row,bit in zip(K,L)])==size-1
            successes += 1
    assert successes > 0

if __name__ == '__main__':
    rng=Random(4003); count=0
    for nb in range(1,8):
        for nj in range(0,7):
            for _ in range(40): one_case(rng,nb,nj); count += 1
    print(f'PASS: {count} generated reciprocity-consistent cases; all q0-J toggles exhausted per case; seed=4003.')
