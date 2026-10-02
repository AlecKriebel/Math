"""Independent direct Boltzmann weights and exact integer max-flow couplings."""
from fractions import Fraction as F
from collections import deque,Counter
import json

C=Counter()
def check(k,b):
    assert b,k
    C[k]+=1
def weights(m,left,right,t):
    out=[]
    for mask in range(1<<m):
        spin=[left]+[1 if mask>>j&1 else -1 for j in range(m)]+[right]
        out.append(t**sum(a==b for a,b in zip(spin,spin[1:])))
    return out
def flow_coupling(wminus,wplus):
    n=len(wminus);total=sum(wminus);source=2*n;sink=source+1;g=[[] for _ in range(sink+1)]
    def add(u,v,cap):
        g[u].append([v,len(g[v]),cap]);g[v].append([u,len(g[u])-1,0])
        return len(g[u])-1
    pairs=[]
    for y,w in enumerate(wminus):add(source,y,w)
    for x,w in enumerate(wplus):add(n+x,sink,w)
    for y in range(n):
        for x in range(n):
            if y&~x==0:pairs.append((y,x,add(y,n+x,total)))
    value=0
    while True:
        parent=[None]*len(g);parent[source]=(-1,-1);q=deque([source])
        while q and parent[sink] is None:
            u=q.popleft()
            for i,(v,rev,cap) in enumerate(g[u]):
                if cap and parent[v] is None:parent[v]=(u,i);q.append(v)
        if parent[sink] is None:break
        amt=total;v=sink
        while v!=source:
            u,i=parent[v];amt=min(amt,g[u][i][2]);v=u
        v=sink
        while v!=source:
            u,i=parent[v];rev=g[u][i][1];g[u][i][2]-=amt;g[v][rev][2]+=amt;v=u
        value+=amt
    joint=[(y,x,total-g[y][i][2]) for y,x,i in pairs if total-g[y][i][2]]
    return value,joint

rows=[]
for t in (2,3,5):
    r=F(t-1,t+1)
    # Conditional plus probability from direct two-edge Boltzmann weights.
    p={}
    for a in (-1,1):
        for b in (-1,1):
            wp=t**((a==1)+(b==1));wm=t**((a==-1)+(b==-1));p[a,b]=F(wp,wp+wm)
    row=2*max(abs(p[1,b]-p[-1,b]) for b in (-1,1))
    check('exact_Dobrushin_row',row==2*r/(1+r*r) and row<1)
    if t==3:check('target_Dobrushin_four_fifths',row==F(4,5))
    for m in range(1,8):
        wp=weights(m,1,1,t);wm=weights(m,-1,-1,t);Z=sum(wp)
        check('spin_flip_partition_function',Z==sum(wm))
        check('direct_spin_flip_weights',all(wp[x]==wm[((1<<m)-1)^x] for x in range(1<<m)))
        value,joint=flow_coupling(wm,wp)
        check('monotone_integer_flow_saturates',value==Z)
        for x in range(1<<m):
            check('plus_flow_marginal',sum(w for y,z,w in joint if z==x)==wp[x])
            check('minus_flow_marginal',sum(w for y,z,w in joint if y==x)==wm[x])
        for y,x,w in joint:check('flow_support_monotone',y&~x==0 and w>0)
        primal=F(sum(w*(x^y).bit_count() for y,x,w in joint),Z)
        dual=F(sum(x.bit_count()*(wp[x]-wm[x]) for x in range(1<<m)),Z)
        exact=2*r*(1-r**m)/((1-r)*(1+r**(m+1)))
        check('independent_primal_dual_equality',primal==dual==exact)
        for k in range(m):
            mu=F(sum((1 if x>>k&1 else -1)*wp[x] for x in range(1<<m)),Z)
            check('Boltzmann_marginal_formula',mu==(r**(k+1)+r**(m-k))/(1+r**(m+1)))
        check('persistent_boundary_lower_bound',exact>=r)
        check('normalized_boundary_upper_bound',exact/m<=2*r/(m*(1-r)))
        rows.append({'edge_weight_ratio':t,'r':str(r),'m':m,'exact_cost':str(primal),'flow_support':len(joint)})
out={'status':'PASS','independent_assertions':sum(C.values()),'counts':dict(sorted(C.items())),'rows':rows,
 'method':'Direct integer Boltzmann weights and a separate exact max-flow construction supported on coordinatewise ordered pairs. Hamming Lipschitz dual=#plus spins certifies equality with the primal cost. No author coupling code imported.',
 'scope':'Finite exact controls for the analytic proof; uniqueness among all infinite-volume Gibbs states is checked in the written DLR argument, not by finite enumeration.'}
print(json.dumps(out,indent=2,sort_keys=True))
