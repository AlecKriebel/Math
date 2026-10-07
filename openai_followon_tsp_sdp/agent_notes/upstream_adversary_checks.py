"""Supplemental falsification checks for family 126 (not a proof certificate).

Run with a Python carrying numpy. Exact rational local-kernel calculation and
floating-point tagged Fourier construction exercise distinct fragile identities.
"""
from fractions import Fraction
from itertools import combinations, permutations, product
from math import comb
from pathlib import Path
import hashlib
import json
import numpy as np


HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent / "sources/family126/build/source/sections"


def matchings(vertices):
    if not vertices:
        yield ()
        return
    a = vertices[0]
    for j in range(1, len(vertices)):
        b = vertices[j]
        rest = vertices[1:j] + vertices[j+1:]
        for pairs in matchings(rest):
            yield ((a, b),) + pairs


def local_check(k, d, b, s):
    w = next(w for w in (k//2, k//2+1) if w % 2 == b)
    y = (1,)*s + (0,)*(d-s)
    assert sum(y) % 2 == b
    sets = list(combinations(range(k), w))
    ids = {frozenset(a): i for i, a in enumerate(sets)}
    n = len(sets)
    joint_counts = [[0]*n for _ in range(n)]
    marginal_counts = [0]*n
    data_count = 0
    h, g = (k-d)//2, (w-s)//2
    support_size = comb(h, g)
    for terminals in permutations(range(k), d):
        remaining = tuple(v for v in range(k) if v not in terminals)
        fixed = frozenset(v for v, bit in zip(terminals, y) if bit)
        for pairs in matchings(remaining):
            data_count += 1
            support = []
            for chosen in combinations(range(h), g):
                a = fixed.union(v for j in chosen for v in pairs[j])
                support.append(ids[a])
            assert len(support) == support_size
            for a in support:
                marginal_counts[a] += 1
                for aa in support:
                    joint_counts[a][aa] += 1
    assert all(Fraction(c, data_count*support_size) == Fraction(1,n)
               for c in marginal_counts)
    # K=N J; exact direct enumeration versus independent intersection formula.
    exact_trace = sum(Fraction(n*n*c*c, data_count**2*support_size**4)
                      for row in joint_counts for c in row)
    formula = sum(
        Fraction(comb(g,j)**2 * comb(h-g,j)**2 * comb(k,w),
                 comb(h,g)**2 * comb(w,2*j) * comb(k-w,2*j))
        for j in range(min(g,h-g)+1))
    assert exact_trace == formula
    kernel = np.array(joint_counts, dtype=float) * n / (data_count*support_size**2)
    eigenvalues = np.linalg.eigvalsh(kernel)
    assert np.max(np.abs(kernel.sum(axis=1)-1)) < 1e-12
    assert eigenvalues.min() > -1e-12
    nonconstant_max = float(eigenvalues[-2])
    assert k/2 * nonconstant_max**2 <= float(exact_trace)-1+1e-10
    return dict(k=k,d=d,b=b,s=s,w=w,local_data=data_count,cut_count=n,
                exact_trace=str(exact_trace),nonconstant_max=nonconstant_max)


def char(p, y):
    return (-1)**sum(a*b for a,b in zip(p,y))


def fourier(H, indices):
    return {p: sum(char(p,y)*H[j] for j,y in enumerate(indices))/len(indices)
            for p in indices}


def potential(H, q, lam):
    indices = list(product(range(2), repeat=len(q)))
    ft = fourier(H, indices)
    U = np.concatenate([lam**(sum(a != b for a,b in zip(p,q))/2)*ft[p]
                        for p in indices],axis=1)
    C = U @ U.T
    return float(np.sum(C*C)), ft


def tagged_smoothing_check(seed):
    rng=np.random.default_rng(seed)
    t,r,lam,eta=2,2,2.,.125
    indices=list(product(range(2), repeat=t))
    F={}
    for x in indices:
        M=rng.normal(size=(r,r))
        F[x]=M.T@M + .2*np.eye(r)
    B=max(float(np.trace(v)) for v in F.values())
    old={}
    for x in indices:
        ev,vec=np.linalg.eigh(F[x])
        old[((),(),x)]=(vec@np.diag(np.sqrt(ev))@vec.T)[None,:,:]
    phis=[]
    equation_errors=[]
    overlap_errors=[]
    for i in range(t+1):
        count=2**i*2**(t-i)
        phis.append(sum(potential(H,q,lam)[0]
                        for (hist,q,suffix),H in old.items())/count)
        if i==t:
            break
        new={}
        for hist in product(range(2),repeat=i):
            for q in product(range(2),repeat=i):
                for suffix in product(range(2),repeat=t-i-1):
                    Hx=[old[(hist,q,(x,)+suffix)] for x in range(2)]
                    R=Hx[0].shape[1]
                    prefix=list(product(range(2),repeat=i))
                    Ys=list(product(range(2),repeat=i+1))
                    for m in range(2):
                        pi={(y,x):.5*(1+eta*(-1)**(y+x+m))
                            for y in range(2) for x in range(2)}
                        Hp=np.zeros((len(Ys),4*R,r))
                        for j,(yp,y) in enumerate((yy[:-1],yy[-1]) for yy in Ys):
                            jp=prefix.index(yp)
                            for x in range(2):
                                Hp[j,(2*y+x)*R:(2*y+x+1)*R,:]=np.sqrt(pi[y,x])*Hx[x][jp]
                        ft=fourier(Hp,Ys)
                        V=[np.concatenate([lam**(sum(a!=b for a,b in zip(p,q))/2)*ft[p+(z,)]
                                           for p in prefix],axis=1)
                           for z in range(2)]
                        A=[v@v.T for v in V]
                        Ux=[np.concatenate([lam**(sum(a!=b for a,b in zip(p,q))/2)*fourier(H,prefix)[p]
                                            for p in prefix],axis=1) for H in Hx]
                        Zx=[U.T@U for U in Ux]
                        for z,zp in product(range(2),repeat=2):
                            predicted=sum((-1)**((z+zp)*y)*sum(pi[y,x]*Zx[x] for x in range(2))
                                          for y in range(2))/4
                            overlap_errors.append(float(np.max(np.abs(V[z].T@V[zp]-predicted))))
                        ev,vec=np.linalg.eigh(A[0]-A[1])
                        P0=vec[:,ev>=0]@vec[:,ev>=0].T
                        Ps=(P0,np.eye(4*R)-P0)
                        split=[np.einsum('ab,ybc->yac',P,Hp) for P in Ps]
                        for j,(yp,y) in enumerate((yy[:-1],yy[-1]) for yy in Ys):
                            jp=prefix.index(yp)
                            before=sum(pi[y,x]*Hx[x][jp].T@Hx[x][jp] for x in range(2))
                            after=sum(H[j].T@H[j] for H in split)
                            equation_errors.append(float(np.max(np.abs(after-before))))
                        for s,H in enumerate(split):
                            new[(hist+(m,),q+(s,),suffix)]=H
        assert phis[-1] <= 2*phis[-2]+1e-8 if len(phis)>1 else True
        old=new
    assert phis[0]<=B*B+1e-8
    assert phis[-1]<=2*phis[-2]+1e-8
    assert max(equation_errors)<1e-10
    assert max(overlap_errors)<1e-10
    masses=[]
    final_identity_errors=[]
    for hist in product(range(2),repeat=t):
        mass=0.
        for q in product(range(2),repeat=t):
            H=old[(hist,q,())]
            _,ft=potential(H,q,lam)
            mass+=sum(lam**sum(a!=b for a,b in zip(p,q))*float(np.sum(h*h)) for p,h in ft.items())
        masses.append(mass)
        for j,y in enumerate(indices):
            averaged=sum(np.prod([.5*(1+eta*(-1)**(yi+xi+mi)) for yi,xi,mi in zip(y,x,hist)])*F[x]
                         for x in indices)
            summed=sum(old[(hist,q,())][j].T@old[(hist,q,())][j] for q in indices)
            final_identity_errors.append(float(np.max(np.abs(averaged-summed))))
    bound=2**t*np.sqrt(r)*B*2**(t/2)
    assert min(masses)<=bound+1e-8
    return dict(seed=seed,L=2,t=t,r=r,lambda_=lam,eta=eta,theta=eta**2,
                B=B,potentials=phis,weighted_masses=masses,coefficient_bound=bound,
                max_overlap_error=max(overlap_errors),
                max_square_identity_error=max(equation_errors+final_identity_errors))


def splitting_check(seed=126):
    rng=np.random.default_rng(seed)
    # Recursive construction exactly as in the source, for three noncommuting PSD inputs.
    size=5
    A=[(lambda M:M.T@M)(rng.normal(size=(size,size))) for _ in range(3)]
    def rec(inputs,embedding):
        if len(inputs)==1:
            return [embedding@embedding.T]
        ev,vec=np.linalg.eigh(inputs[0]-sum(inputs[1:]))
        Vp,Vq=vec[:,ev>=0],vec[:,ev<0]
        p=embedding@Vp
        q=embedding@Vq
        return [p@p.T]+rec([Vq.T@a@Vq for a in inputs[1:]],q)
    P=rec(A,np.eye(size))
    lhs=sum(float(np.sum((p@a@p)**2)) for z,a in enumerate(A)
            for s,p in enumerate(P) if s!=z)
    rhs=4*sum(float(np.trace(a@aa)) for j,a in enumerate(A)
              for jj,aa in enumerate(A) if j!=jj)
    assert lhs<=rhs+1e-8
    return dict(seed=seed,dimension=size,L=3,lhs=lhs,rhs=rhs,
                sum_projection_error=float(np.max(np.abs(sum(P)-np.eye(size)))))


def parity_check():
    # Complete bipartite K_10,10: t=20, d=10, expansion beta=1/2.
    # D=1 gives 2D/beta=4=t/5. These adapted constants exercise the
    # entire degree-one moment matrix exactly, rather than the asymptotic
    # d=100, tau=1/1000 theorem at an intractable number of characters.
    t,side,d,D=20,10,10,1
    edges=list(product(range(side),range(side,t)))
    incident=[[] for _ in range(t)]
    for j,(u,v) in enumerate(edges):
        incident[u].append(j)
        incident[v].append(j)
    stars=[sum(1<<e for e in row) for row in incident]
    # Row reduction of the cut space, carrying the corresponding vertex set.
    basis={}
    for v in range(t-1):
        row,vertices=stars[v],1<<v
        while row:
            pivot=row.bit_length()-1
            if pivot not in basis:
                basis[pivot]=(row,vertices)
                break
            reduced,labels=basis[pivot]
            row^=reduced
            vertices^=labels
    def reduce(row):
        vertices=0
        for pivot in sorted(basis,reverse=True):
            if (row>>pivot)&1:
                reduced,labels=basis[pivot]
                row^=reduced
                vertices^=labels
        return row,vertices
    def moment(row):
        residue,vertices=reduce(row)
        assert residue==0
        if vertices.bit_count()>t//2:
            vertices^=(1<<t)-1
        assert vertices.bit_count()<=2*D/.5
        # Only vertex zero has charge one.
        return -1 if vertices&1 else 1
    indices=[(None,0,0)]
    for v in range(t):
        for p in range(1,1<<(d-1)):
            image=sum(1<<incident[v][j] for j in range(d-1) if (p>>j)&1)
            indices.append((v,p,image))
    classes={}
    for index in indices:
        classes.setdefault(reduce(index[2])[0],[]).append(index)
    pairs=0
    for group in classes.values():
        ref=group[0][2]
        signs={p[2]:moment(p[2]^ref) for p in group}
        for p in group:
            for pp in group:
                assert moment(p[2]^pp[2])==signs[p[2]]*signs[pp[2]]
                pairs+=1
    # Every degree-one moment block is exactly sigma sigma^T, hence PSD.
    # Verify each edge disagreement value, including last-incidence replacements.
    last_positions=[row[-1] for row in incident]
    last_replacement_edges=0
    for e,(u,v) in enumerate(edges):
        image=0
        phase=1
        for vertex in (u,v):
            if e==last_positions[vertex]:
                image^=stars[vertex]^(1<<e)
                phase*=(-1 if vertex==0 else 1)
                last_replacement_edges+=1
            else:
                image^=1<<e
        assert phase*moment(image)==1
    return dict(graph='K_10,10',t=t,d=d,beta=.5,D=D,
                low_degree_indices=len(indices),moment_blocks=len(classes),
                checked_nonzero_moment_pairs=pairs,
                largest_moment_block=max(map(len,classes.values())),
                checked_edge_disagreements=len(edges),
                checked_last_incidence_replacements=last_replacement_edges,
                status='exact rank-one block decomposition and all disagreement values verified')


def main():
    results={
        "status":"supplemental numerical/rational checks passed; not formal verification",
        "source_sha256":{f:hashlib.sha256((SOURCE/f).read_bytes()).hexdigest()
                         for f in ['introduction.tex','local-averaging.tex','splitting.tex',
                                   'fourier-smoothing.tex','parity.tex','matching.tex']},
        "local": [local_check(*args) for args in [(6,2,0,0),(6,2,0,2),(6,2,1,1),
                                                   (8,2,0,0),(8,2,0,2),(8,2,1,1),
                                                   (8,4,0,0),(8,4,0,2),(8,4,0,4),
                                                   (8,4,1,1),(8,4,1,3)]],
        "tagged_smoothing":[tagged_smoothing_check(seed) for seed in [126,127,128]],
        "splitting":splitting_check(),
        "parity":parity_check(),
        "numpy_version":np.__version__,
    }
    target=HERE/'upstream_adversary_checks.json'
    target.write_text(json.dumps(results,indent=2)+'\n')
    print(json.dumps(results,indent=2))


if __name__=='__main__':
    main()
