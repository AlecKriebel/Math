"""Independent standard-library loop, graph-rank and holonomy mutant controls."""
from fractions import Fraction as Q
from decimal import Decimal as D, localcontext
import json
count=0

def check(b):
    global count
    assert b
    count+=1

def rank(A):
    A=[[Q(x) for x in row] for row in A]
    piv=0
    for col in range(len(A[0])):
        p=next((j for j in range(piv,len(A)) if A[j][col]),None)
        if p is None: continue
        A[piv],A[p]=A[p],A[piv]
        z=A[piv][col];A[piv]=[x/z for x in A[piv]]
        for j in range(len(A)):
            if j!=piv and A[j][col]:
                z=A[j][col];A[j]=[x-z*y for x,y in zip(A[j],A[piv])]
        piv+=1
    return piv

results=[]
for L in [3,4,6,8]:
    N=L*L; idx=lambda x,y:(x%L)+L*(y%L)
    edge=[(idx(x,y),idx(x+1,y)) for y in range(L) for x in range(L)]+[(idx(x,y),idx(x,y+1)) for y in range(L) for x in range(L)]
    G=[[int(v==h)-int(v==t) for v in range(N)] for t,h in edge]
    C=[]
    for y in range(L):
        for x in range(L):
            p=[0]*(2*N)
            p[idx(x,y)]+=1;p[N+idx(x+1,y)]+=1;p[idx(x,y+1)]-=1;p[N+idx(x,y)]-=1
            C.append(p)
    rg,rc=rank(G),rank(C)
    check(rg==N-1);check(rc==N-1)
    check(all(sum(C[p][e]*G[e][v] for e in range(2*N))==0 for p in range(N) for v in range(N)))
    # Add two loop coordinates and show curl+loops has exactly the quotient rank.
    hx=[0]*(2*N);hy=[0]*(2*N)
    for x in range(L):hx[idx(x,0)]=1
    for y in range(L):hy[N+idx(0,y)]=1
    total=rank(C+[hx,hy]);check(total==N+1)
    results.append({'L':L,'vertices':N,'edges':2*N,'gauge_rank':rg,'curl_rank':rc,'physical_rank':total})
# The simple graph at length two has only N edges; reject the 2N assumption.
L=2;idx=lambda x,y:(x%L)+L*(y%L)
unique={tuple(sorted((idx(x,y),idx(x+dx,y+dy)))) for x in range(L) for y in range(L) for dx,dy in [(1,0),(0,1)]}
check(len(unique)==4 and len(unique)!=2*L*L)

# Decimal values are auxiliary empirical receipts; exact inequalities are proved in report.
with localcontext() as ctx:
    ctx.prec=70
    r2=D(2).sqrt();r3=D(3).sqrt()
    periodic=-D(4)*((D(4)+D(4)).sqrt()+2*(1+r3)+(D(4)+2*r2).sqrt())
    optimum=-D(16)*(1+r3)
    check(periodic>optimum)
    holo={'L':8,'periodic_uniform_quarter_energy':str(periodic),'optimized_uniform_quarter_energy':str(optimum),'periodic_minus_optimized':str(periodic-optimum)}
# Exact zero-plaquette 4x4 loops also distinguish spectra: T^2 trace fixed but T^4 changes.
# Purely combinatorial closed-walk phases; assign loop signs at seams.
def trace4(L,twists):
    N=L*L;idx=lambda x,y:(x%L)+L*(y%L)
    adjacency=[[] for _ in range(N)]
    for y in range(L):
        for x in range(L):
            u=idx(x,y)
            for dx,dy,sgn in [(1,0,-1 if x==L-1 and twists[0] else 1),(0,1,-1 if y==L-1 and twists[1] else 1)]:
                v=idx(x+dx,y+dy);adjacency[u].append((v,sgn));adjacency[v].append((u,sgn))
    trace=0
    for u in range(N):
        state={u:1}
        for _ in range(4):
            new={}
            for a,k in state.items():
                for b,z in adjacency[a]:new[b]=new.get(b,0)+k*z
            state=new
        trace+=state.get(u,0)
    return trace
moments={str(v):trace4(4,v) for v in [(0,0),(1,0),(1,1)]}
check(list(moments.values())==[640,576,512])
print(json.dumps({'assertions':count,'graph_topology':results,'length_two_unique_edges':len(unique),'uniform_holonomy_mutant':holo,'zero_plaquette_trace4':moments,'scope':'Finite exact topology controls and explicit holonomy countercontrol. These do not establish any all-size minimum.'},indent=2,sort_keys=True))
