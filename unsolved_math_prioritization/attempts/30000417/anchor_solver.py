"""Exact optimization of the turn-4 sufficient certificate, not a full feasibility oracle."""

def deficit(A, d, labels):
    return max(0, 2*d-sum(all(abs(x-c)>=d for c in labels) for x in A))


def optimize_anchors(L, d, residue):
    n=len(L);I=list(range(residue,n,3));q=len(I)
    if not I:raise ValueError('empty anchor class')
    unary=[[] for _ in I];edges=[[] for _ in range(q-1)]
    for j in range(n):
        if j in I:continue
        neighbors=[t for t,i in enumerate(I) if abs(i-j)<=2]
        if len(neighbors)==1:unary[neighbors[0]].append(j)
        elif len(neighbors)==2 and neighbors[1]==neighbors[0]+1:edges[neighbors[0]].append(j)
        else:raise AssertionError('invalid anchor geometry')
    def cost(vertices, labels):return sum(deficit(L[j],d,labels) for j in vertices)
    layers=[{a:(cost(unary[0],[a]),None) for a in sorted(L[I[0]])}]
    for t in range(1,q):
        layer={}
        for b in sorted(L[I[t]]):
            layer[b]=min((score+cost(edges[t-1],[a,b])+cost(unary[t],[b]),a)
                         for a,(score,_) in layers[-1].items())
        layers.append(layer)
    value,last=min((score,b) for b,(score,_) in layers[-1].items())
    labels=[last]
    for t in range(q-1,0,-1):last=layers[t][last][1];labels.append(last)
    labels.reverse()
    return dict(cost=value,residue=residue,anchors=list(zip(I,labels)),
                layers=[[[a,s,prev] for a,(s,prev) in sorted(layer.items())] for layer in layers])


def direct_cost(L,d,anchors):
    I={i:c for i,c in anchors}
    return sum(deficit(L[j],d,[c for i,c in I.items() if abs(i-j)<=2])
               for j in range(len(L)) if j not in I)


def label_from_certificate(L,d,result):
    if result['cost']>=2*d:return None
    I=dict(result['anchors']);J=[j for j in range(len(L)) if j not in I]
    A=[sorted(x for x in L[j] if all(abs(x-c)>=d for i,c in I.items() if abs(i-j)<=2))[:2*d]
       for j in J]
    layers=[set(A[0])]
    for C in A[1:]:layers.append({b for b in C if any(abs(a-b)>=d for a in layers[-1])})
    if not layers[-1]:raise AssertionError('sufficient budget failed')
    v=min(layers[-1]);out=[v]
    for R in reversed(layers[:-1]):v=min(a for a in R if abs(a-v)>=d);out.append(v)
    f=[I.get(j) for j in range(len(L))]
    for j,c in zip(J,reversed(out)):f[j]=c
    return f
