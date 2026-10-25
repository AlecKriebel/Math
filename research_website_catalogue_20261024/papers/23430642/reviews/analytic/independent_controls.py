"""Independent exact controls written from the paper, before reading its helpers.

Generic residual shortest paths and primal-dual certificates; no imported package code.
Finite corroboration, not a proof of the universal reduction.
"""
from fractions import Fraction as Q
from pathlib import Path
from itertools import product
from math import lcm, factorial
import datetime, hashlib, json

HERE = Path(__file__).resolve().parent
counts = {}
def check(label, condition):
    counts[label] = counts.get(label, 0) + 1
    if not condition:
        raise RuntimeError(label)

def network(weights):
    n=len(weights); S=sum(weights); arcs=[]
    nodes=['s']+[(s,'s',i) for s in [1,-1] for i in range(n,-1,-1)]+[(s,'t',i) for s in [1,-1] for i in range(n+1)]+['t']
    ix={v:i for i,v in enumerate(nodes)}
    def add(u,v,cap,cost): arcs.append((ix[u],ix[v],Q(cap),Q(cost)))
    for sign in [1,-1]:
        add((sign,'s',0),(sign,'t',0),1,Q(1,120*S))
        for i,w in enumerate(weights,1):
            a=Q(sign*w,24*S); cheap=a/2; dear=(2**i-1-a)/2
            add((sign,'s',i),(sign,'s',i-1),2**(i-1),cheap)
            add((sign,'t',i-1),(sign,'t',i),2**(i-1),cheap)
            add((sign,'s',i),(sign,'t',i-1),2**(i-1),dear)
            add((sign,'s',i-1),(sign,'t',i),2**(i-1),dear)
    for sign in [1,-1]:
        add('s',(sign,'s',n),2**n,0);add((sign,'t',n),'t',2**n,0)
    bridge=len(arcs); add((1,'s',0),(-1,'t',0),1,0)
    D=lcm(*(a[3].denominator for a in arcs))
    orig=[a[3] for a in arcs]; pert=[c+Q(1,4*D*3**(i+1)) for i,c in enumerate(orig)]
    H=1+max(abs(c) for c in pert)
    positive=[c+H*(v-u) for (u,v,_,_),c in zip(arcs,pert)]
    check('network_counts',len(nodes)==4*n+6 and len(arcs)==8*n+7)
    check('positive_topological_costs',all(u<v and c>0 for (u,v,_,_),c in zip(arcs,positive)))
    return {'weights':weights,'nodes':nodes,'arcs':arcs,'s':0,'t':len(nodes)-1,'bridge':bridge,'orig':orig,'pert':pert,'positive':positive,'F':2**(n+1),'D':D}

def residual(net,flow,costs):
    out=[]
    for i,((u,v,cap,_),f,c) in enumerate(zip(net['arcs'],flow,costs)):
        if f<cap:out.append((u,v,cap-f,c,i,1))
        if f>0:out.append((v,u,f,-c,i,-1))
    return out

def shortest(net,flow,costs,all_paths=False):
    edges=residual(net,flow,costs); N=len(net['nodes']); dist=[None]*N;dist[net['t']]=Q(0)
    for _ in range(N-1):
        changed=False
        for u,v,cap,c,i,sgn in edges:
            if dist[v] is not None and (dist[u] is None or dist[u]>c+dist[v]):dist[u]=c+dist[v];changed=True
        if not changed:break
    if dist[net['s']] is None:return None,[]
    adj=[[] for _ in range(N)]
    for e in edges:
        u,v,cap,c,i,sgn=e
        if dist[u] is not None and dist[v] is not None and dist[u]==c+dist[v]:adj[u].append(e)
    paths=[]
    def dfs(u,seen,path):
        if u==net['t']:
            paths.append(path);return
        for e in adj[u]:
            if e[1] not in seen:
                dfs(e[1],seen|{e[1]},path+[e])
                if paths and not all_paths:return
    dfs(net['s'],{net['s']},[])
    check('shortest_simple_path_exists',bool(paths))
    return dist[net['s']],paths

def feasible(net,f,q):
    imbalance=[Q(0)]*len(net['nodes'])
    for (u,v,cap,_),x in zip(net['arcs'],f):
        check('capacity',0<=x<=cap);imbalance[u]+=x;imbalance[v]-=x
    check('all_node_conservation',all(z==(q if i==net['s'] else -q if i==net['t'] else 0) for i,z in enumerate(imbalance)))

def potentials(net,f,costs):
    edges=residual(net,f,costs);N=len(net['nodes']);d=[Q(0)]*N
    for it in range(N):
        changed=False
        for u,v,_,c,_,_ in edges:
            if d[v]>d[u]+c:d[v]=d[u]+c;changed=True
        if not changed:break
    check('no_negative_residual_cycle',not changed)
    check('exact_reduced_cost_certificate',all(c+d[u]-d[v]>=0 for u,v,_,c,_,_ in edges))
    return d

def zero_cycles(net,f,costs,d):
    edges=[e for e in residual(net,f,costs) if e[3]+d[e[0]]-d[e[1]]==0]
    adj=[[] for _ in net['nodes']]
    for e in edges:adj[e[0]].append(e)
    seen_cycles=0
    for start in range(len(adj)):
        def dfs(u,seen,path):
            nonlocal seen_cycles
            for e in adj[u]:
                v=e[1]
                if v==start:
                    vec=[0]*len(f)
                    for z in path+[e]:vec[z[4]]+=z[5]
                    check('no_nontrivial_zero_cost_cycle',not any(vec));seen_cycles+=1
                elif v>start and v not in seen:dfs(v,seen|{v},path+[e])
        dfs(start,{start},[])
    return seen_cycles

def move(f,path,amount):
    g=list(f)
    for e in path:g[e[4]]+=amount*e[5]
    return g

def zstate(weights,j):return sum((-1)**((j>>i)&1)*w for i,w in enumerate(weights))

def trajectory(net):
    f=[Q(0)]*len(net['arcs']);mids=[];bridge_events=[];cycles=0
    for q in range(net['F']):
        oldcost,_=shortest(net,f,net['orig'])
        _,paths=shortest(net,f,net['pert']);path=paths[0]
        check('same_state_original_shortest',sum(net['orig'][e[4]]*e[5] for e in path)==oldcost)
        check('unit_bottleneck',min(e[2] for e in path)==1)
        change=sum(e[5] for e in path if e[4]==net['bridge'])
        expected=(1 if q%2==0 else -1) if zstate(net['weights'],q//2)==0 else 0
        check('signed_counter_bridge_at_each_step',change==expected)
        mid=move(f,path,Q(1,2)); demand=Q(q)+Q(1,2)
        feasible(net,mid,demand);pot=potentials(net,mid,net['positive'])
        if len(net['weights'])<=2:cycles+=zero_cycles(net,mid,net['positive'],pot)
        L=len(net['nodes'])-1;K=Q(1,2*L);h=demand+K*mid[net['bridge']]
        x=[1-h/net['F'],h/net['F']-sum(mid)/(L*net['F'])]+[a/(L*net['F']) for a in mid]
        check('simplex_inverse_nonnegative',min(x)>=0 and sum(x)==1)
        check('simplex_exact_q',net['F']*(1-x[0])-K*L*net['F']*x[2+net['bridge']]==demand)
        mids.append((demand,mid,x,pot))
        if change==1:
            check('retained_yes_witness',demand<=net['F']-Q(3,2) and mid[net['bridge']]==Q(1,2) and h<net['F'])
            bridge_events.append(str(demand))
        f=move(f,path,1);feasible(net,f,q+1)
    check('maximum_flow_terminal',shortest(net,f,net['pert'])[0] is None)
    truth=any(zstate(net['weights'],j)==0 for j in range(2**len(net['weights'])))
    check('partition_equivalence',bool(bridge_events)==truth)
    return mids,{'weights':net['weights'],'partition':truth,'augmentations':net['F'],'forward_bridge_midpoints':bridge_events,'formal_zero_cycles':cycles}

def all_original_choices(net):
    states={tuple(Q(0) for _ in net['arcs'])};totalpaths=0;maxbranch=0
    for q in range(net['F']):
        following=set()
        for f in states:
            _,paths=shortest(net,f,net['orig'],True);maxbranch=max(maxbranch,len(paths))
            for path in paths:
                totalpaths+=1
                check('all_choices_unit_bottleneck',min(e[2] for e in path)==1)
                change=sum(e[5] for e in path if e[4]==net['bridge'])
                expected=(1 if q%2==0 else -1) if zstate(net['weights'],q//2)==0 else 0
                check('all_choices_bridge_event',change==expected)
                following.add(tuple(move(f,path,1)))
        states=following
    return {'weights':net['weights'],'paths_checked':totalpaths,'largest_tie':maxbranch,'terminal_states':len(states)}

def make_game(net):
    p=len(net['arcs']);V=len(net['nodes']);L=V-1;F=net['F'];m=p+2;K=Q(1,2*L);eps=K/2
    qvec=[Q(0),Q(F)]+[Q(F)]*p;qvec[net['bridge']+2]=Q(F,2)
    R=[];r=[];s=[]
    for i,(_,_,cap,_) in enumerate(net['arcs']):
        row=[Q(0)]*m;row[i+2]=L*F;R.append(row);r.append(cap);s.append(Q(0))
    for node in range(V):
        d=1 if node==net['s'] else -1 if node==net['t'] else 0
        row=[-d*z for z in qvec]
        for i,(u,v,_,_) in enumerate(net['arcs']):row[i+2]+=L*F*((u==node)-(v==node))
        for sign in [1,-1]:R.append([sign*z for z in row]);r.append(Q(0));s.append(Q(0))
    for sign in [1,-1]:R.append([sign*z for z in qvec]);r.append(Q(0));s.append(Q(sign))
    k=len(R);c=[Q(0),Q(0)]+[L*F*z for z in net['positive']]
    clearing=lcm(*(z.denominator for row in R for z in row),*(z.denominator for z in c))
    H=max([clearing]+[abs(clearing*z.numerator//z.denominator) for row in R for z in row]+[abs(clearing*z.numerator//z.denominator) for z in c])
    M=k*factorial(k+1)*H**(k+1)+1
    R0=[[Q(0)]*m]+R;r0=[Q(0)]+r;b=[Q(0)]+[-M*z for z in s]
    a=[-eps]+[F-eps]*(m-1)
    A=[[-c[i]-M*R0[j][i]+M*r0[j] for j in range(k+1)] for i in range(m)]
    B=[[-A[i][j]+a[i]*b[j] for j in range(k+1)] for i in range(m)]
    check('game_dimensions',m==8*len(net['weights'])+9 and k+1==16*len(net['weights'])+22)
    check('exact_rank_one_factorization',a[0]!=0 and any(b) and all(A[i][j]+B[i][j]==a[i]*b[j] for i in range(m) for j in range(k+1)))
    diag=k-1
    check('default_row_strict',all(A[0][diag]>A[i][diag] for i in range(1,m)))
    check('default_column_strict',all(B[0][diag]>B[0][j] for j in range(k+1) if j!=diag))
    return R,r,s,c,M,a,b,A,B,diag

def is_ne(A,B,x,y):
    row=[sum(z*w for z,w in zip(r,y)) for r in A]
    col=[sum(x[i]*B[i][j] for i in range(len(x))) for j in range(len(y))]
    return all(z<=sum(xx*rr for xx,rr in zip(x,row)) for z in row) and all(z<=sum(yy*cc for yy,cc in zip(y,col)) for z in col)

def game_controls(net,mids):
    R,r,s,c,M,a,b,A,B,diag=make_game(net);k=len(R);m=len(a);maxnorm=Q(0);crossings=0
    for lam,f,x,pi in mids:
        reduced=[cost+pi[u]-pi[v] for (u,v,_,_),cost in zip(net['arcs'],net['positive'])]
        mu=[max(Q(0),-z) for z in reduced]
        for z in pi:mu.extend([max(Q(0),z),max(Q(0),-z)])
        gamma=pi[net['s']]-pi[net['t']];mu.extend([max(Q(0),gamma),max(Q(0),-gamma)])
        check('network_dual_transfers',len(mu)==k and all(c[i]+sum(R[j][i]*mu[j] for j in range(k))>=0 for i in range(m)))
        primal=sum(c[i]*x[i] for i in range(m));dual=-sum((r[j]+s[j]*lam)*mu[j] for j in range(k))
        check('rational_primal_dual_equality',primal==dual)
        check('complementarity',all(mu[j]*(sum(R[j][i]*x[i] for i in range(m))-r[j]-s[j]*lam)==0 for j in range(k)))
        norm=sum(mu);maxnorm=max(maxnorm,norm);check('M_strictly_bounds_certificate',norm<M)
        y=[1-norm/M]+[z/M for z in mu];check('column_strategy_simplex',min(y)>=0 and sum(y)==1)
        aux=[[A[i][j]-lam*b[j] for j in range(k+1)] for i in range(m)]
        check('exact_auxiliary_equilibrium',is_ne(aux,[[-z for z in row] for row in aux],x,y))
        crossing=sum(aa*xx for aa,xx in zip(a,x))==lam
        check('crossing_equals_half_bridge',crossing==(f[net['bridge']]==Q(1,2)))
        if crossing:check('exact_original_positive_witness',is_ne(A,B,x,y));crossings+=1
    check('small_penalty_rejected',mids[0][0]<sum(c[i]*mids[0][2][i] for i in range(m)))
    wrongB=[[-A[i][j]-a[i]*b[j] for j in range(k+1)] for i in range(m)]
    purex=[Q(1)]+[Q(0)]*(m-1);purey=[Q(int(j==diag)) for j in range(k+1)]
    check('payoff_sign_negative_control',not is_ne(A,wrongB,purex,purey))
    return {'weights':net['weights'],'dimensions':[m,k+1],'M_bits':M.bit_length(),'auxiliary_pairs':len(mids),'positive_pairs':crossings,'max_dual_l1':str(maxnorm)}

def main():
    vectors=[list(w) for n in range(1,4) for w in product(range(1,4),repeat=n)]
    vectors += [[1,1,1,1],[1,2,3,4],[1,1,1,4],[1,2,4,8],[2,2,3,3],[1,1,2,4],[1,10**20,10**20+1],[7,7,7,7,7]]
    rows=[];choice=[];games=[]
    selected={(1,),(1,1),(1,2),(1,2,3),(1,1,1)}
    for w in vectors:
        net=network(w);mids,record=trajectory(net);rows.append(record)
        if len(w)<=2:choice.append(all_original_choices(net))
        if tuple(w) in selected:games.append(game_controls(net,mids))
    check('degenerate_pair_not_row_uniqueness',is_ne([[Q(0),Q(0)]],[[Q(1),Q(1)]],[Q(1)],[Q(1),Q(0)]) and is_ne([[Q(0),Q(0)]],[[Q(1),Q(1)]],[Q(1)],[Q(0),Q(1)]))
    check('duplicate_slack_noninjective_control',Q(1,4)+Q(1,4)==Q(1,2)+Q(0) and (Q(1,4),Q(1,4))!=(Q(1,2),Q(0)))
    result={'status':'PASS_FINITE_INDEPENDENT_CONTROLS','created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'not_universal_proof':True,'published_helper_code_read_before_authoring':False,'vectors':rows,'all_original_choices':choice,'games':games,'checks_by_category':counts,'total_checks':sum(counts.values()),'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    (HERE/'independent-controls.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'status':result['status'],'vectors':len(rows),'augmentations':sum(r['augmentations'] for r in rows),'game_count':len(games),'auxiliary_pairs':sum(g['auxiliary_pairs'] for g in games),'checks':result['total_checks']}))

if __name__=='__main__':main()
