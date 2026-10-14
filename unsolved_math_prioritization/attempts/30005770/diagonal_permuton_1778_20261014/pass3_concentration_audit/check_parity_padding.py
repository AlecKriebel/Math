"""Independent finite regression for raw-domino parity flattening and padding.
No coefficient-radius or limiting-law inference is made by this program.
"""
from collections import Counter
from functools import lru_cache
from itertools import combinations, permutations
from pathlib import Path
import hashlib
import json
import sys


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def std(values):
    ranks = {v:i+1 for i,v in enumerate(sorted(values))}
    return tuple(ranks[v] for v in values)


@lru_cache(None)
def avoids(p, pattern):
    return not any(std(tuple(p[i] for i in I)) == pattern
                   for I in combinations(range(len(p)), len(pattern)))


def S(p):
    n = len(p)
    inv = [0] * n
    for i, value in enumerate(p, 1):
        inv[value - 1] = i
    return tuple(n + 1 - value for value in inv[::-1])


def top_length(p):
    n = len(p)
    for k in range(1, n + 1):
        if not avoids(tuple(v for v in p if v > n-k), (2,1,3)):
            return k-1
    return n


def cell_indices(p):
    remaining = list(range(len(p)))
    cells = []
    while remaining:
        q = std(tuple(p[i] for i in remaining))
        if len(cells) % 2 == 0:
            k = top_length(q)
            chosen = [remaining[j] for j,v in enumerate(q) if v > len(q)-k]
        else:
            k = len(q)
            for m in range(1, len(q)+1):
                if not avoids(q[:m], (1,3,2)):
                    k=m-1
                    break
            chosen = remaining[:k]
        require(chosen, ('empty greedy cell', p, cells))
        cells.append(chosen)
        chosen_set = set(chosen)
        remaining = [i for i in remaining if i not in chosen_set]
    return cells


N = 7
counts = Counter()
by_n = []
for n in range(1, N+1):
    images = set()
    class_count = 0
    raw_counts = Counter()
    for p in permutations(range(1,n+1)):
        if not avoids(p, (1,3,2,4)):
            continue
        class_count += 1
        cells = cell_indices(p)
        upper_indices = {i for cell in cells[::2] for i in cell}
        lower_indices = set(range(n)) - upper_indices
        upper_values = [p[i] for i in range(n) if i in upper_indices]
        lower_values = [p[i] for i in range(n) if i in lower_indices]
        A = std(upper_values)
        B = std(lower_values)
        C = S(B)
        require(avoids(A,(2,1,3)), ('odd union',p,cells,A))
        require(avoids(B,(1,3,2)), ('even union',p,cells,B))
        if B:
            urank={v:i+1 for i,v in enumerate(sorted(upper_values))}
            lrank={v:i+1 for i,v in enumerate(sorted(lower_values))}
            xflat=tuple(len(B)+urank[p[i]] if i in upper_indices else lrank[p[i]] for i in range(n))
            yflat=tuple(p[i] for i in range(n) if i in lower_indices)+tuple(p[i] for i in range(n) if i in upper_indices)
            zflat=S(yflat)
            require(avoids(xflat,(1,3,2,4)), ('horizontal flattening',p,xflat))
            require(avoids(zflat,(1,3,2,4)), ('vertical flattening',p,zflat))
            require(std(tuple(v for v in zflat if v > len(A)))==C, ('reverse first state',p,A,C,zflat))
            require(std(tuple(v for v in zflat if v <= len(A)))==S(A), ('reverse second state',p,A,C,zflat))
            image=(A,C,xflat,zflat)
            counts['two_shuffle_images'] += 1
        else:
            image=('single',A)
            counts['single_cell_images'] += 1
        require(image not in images, ('image collision',p,image))
        images.add(image)
        # Every possible value threshold in this avoider gives at most one raw domino.
        for k in range(1,n):
            m=n-k
            a=std(tuple(v for v in p if v>m))
            b=std(tuple(v for v in p if v<=m))
            if not (avoids(a,(2,1,3)) and avoids(b,(1,3,2))):
                continue
            c=S(b)
            raw_counts[a,c] += 1
            padded=(m+2,m+1)+tuple(v+2 if v>m else v for v in p)
            require(avoids(padded,(1,3,2,4)), ('padding avoidance',p,k,padded))
            require(top_length(padded)==k+1, ('padding greediness',p,k,padded))
            ap=std(tuple(v for v in padded if v>m+1))
            cp=S(std(tuple(v for v in padded if v<=m+1)))
            require(ap==(1,)+tuple(v+1 for v in a), ('upper state padding',p,k,ap,a))
            require(cp==(len(c)+1,)+c, ('lower state padding',p,k,cp,c))
            counts['raw_shuffle_padding_checks'] += 1
    product_sum=sum(v*raw_counts[c,a] for (a,c),v in raw_counts.items())
    square_sum=sum(v*v for v in raw_counts.values())
    catalan=sum(1 for p in permutations(range(1,n+1)) if avoids(p,(2,1,3)))
    require(class_count<=catalan+product_sum, ('two-shuffle count inequality',n,class_count,catalan,product_sum))
    require(product_sum<=square_sum, ('AM-GM',n,product_sum,square_sum))
    by_n.append({'n':n,'class_count':class_count,'Catalan':catalan,'raw_reverse_product_sum':product_sum,'raw_square_sum':square_sum})
result={'status':'PASS','scope':'Finite exact sanity checks only. No asymptotic growth conclusion follows from this program.','maximum_size':N,'python_optimization_level':sys.flags.optimize,'checks':dict(counts),'by_n':by_n,'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
output=Path(__file__).with_name(sys.argv[1] if len(sys.argv)>1 else 'PARITY_PADDING_CHECK_NORMAL.json')
output.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
