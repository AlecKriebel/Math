"""Construct exact graph-flow covers of G_q and check the cellular boundary.
Group: <a,b,t | t^-1 a t=((ab)^(q-1)b)>. Standard-library exact arithmetic.
"""
from fractions import Fraction
import json

def rank(matrix):
    a=[[Fraction(x) for x in row] for row in matrix]
    m=len(a);n=len(a[0]);row=0
    for col in range(n):
        p=next((i for i in range(row,m) if a[i][col]),None)
        if p is None:continue
        a[p],a[row]=a[row],a[p]
        v=a[row][col];a[row]=[x/v for x in a[row]]
        for i in range(row+1,m):
            if a[i][col]:
                v=a[i][col];a[i]=[x-v*y for x,y in zip(a[i],a[row])]
        row+=1
        if row==m:break
    return row

def construct(q,n):
    assert q>=2 and n>=1
    size=2*n*q
    index=lambda side,i,j:(side*n+(i%n))*q+j
    slots=[(side,i,j) for side in (0,1) for i in range(n) for j in range(q)]
    p=[0]*size;r=[0]*size
    for side,i,j in slots:
        v=index(side,i,j);p[v]=index(side,i,(j+1)%q)
    # color1 connects the next right vertex; other colors connect equal indices.
    for i in range(n):
        for j in range(q):
            left=index(0,i,j);right=index(1,i+int(j==1),j)
            r[left]=right;r[right]=left
    t=[r[p[v]] for v in range(size)]
    ident=list(range(size));perms=[ident,p,t]
    inv=[]
    for perm in perms:
        ip=[0]*size
        for v,w in enumerate(perm):ip[w]=v
        inv.append(ip)
    assert all(r[r[v]]==v and r[v]!=v for v in range(size))
    # Transitivity of the action is connectivity of the slot graph.
    seen={0};todo=[0]
    while todo:
        v=todo.pop()
        for w in (p[v],r[v]):
            if w not in seen:seen.add(w);todo.append(w)
    assert len(seen)==size
    # Relator t^-1 a t w^-1; letters are (generator index, orientation).
    w=[(0,1),(1,1)]*(q-1)+[(1,1)]
    relator=[(2,-1),(0,1),(2,1)]+[(g,-sign) for g,sign in reversed(w)]
    d2=[[0]*size for _ in range(3*size)]
    for start in range(size):
        v=start
        for g,sign in relator:
            if sign==1:
                d2[g*size+v][start]+=1;v=perms[g][v]
            else:
                v=inv[g][v];d2[g*size+v][start]-=1
        assert v==start
    # Verify the displayed block formula from this separate edge-walk construction.
    np=[[0]*size for _ in range(size)]
    for v in range(size):
        at=v
        for _ in range(q):np[at][v]+=1;at=p[at]
        assert at==v
    expected=[[0]*size for _ in range(3*size)]
    for v in range(size):
        expected[inv[2][v]][v]+=1
        expected[inv[1][v]][v]+=1
        for j in range(size):
            expected[j][v]-=np[j][v];expected[size+j][v]-=np[j][v]
    assert expected==d2
    # d1 d2=0, checked directly without constructing a dense product.
    for col in range(size):
        boundary=[0]*size
        for g in range(3):
            for v in range(size):
                coeff=d2[g*size+v][col]
                boundary[v]-=coeff;boundary[perms[g][v]]+=coeff
        assert not any(boundary)
    matrix_rank=rank(d2);b2=size-matrix_rank
    graph_vertices=2*n;graph_edges=n*q
    assert b2==graph_edges-graph_vertices+1==n*(q-2)+1
    return {'q':q,'n':n,'cover_degree':size,'graph_vertices':graph_vertices,
            'graph_edges':graph_edges,'boundary2_rank':matrix_rank,'b2':b2,
            'relator_closes':True,'block_formula_verified':True,'boundary_squared_zero':True}

if __name__=='__main__':
    results=[construct(q,n) for q in range(2,7) for n in range(1,4)]
    print(json.dumps({'construction':'connected bipartite q-regular slot graph; a=1, b=P, t=RP',
                      'arithmetic':'exact Fraction Gaussian elimination',
                      'formula':'degree=2nq, b2=n(q-2)+1',
                      'proof_scope':'finite checks corroborate a separate universal cycle-flow proof',
                      'cases':results},indent=2))
