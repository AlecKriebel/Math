"""Fresh rational check of the paper's projection versus joint-lift qualification."""
from fractions import Fraction
import json,pathlib,sys,datetime,os,hashlib
def require(value,message):
    if not value:raise AssertionError(message)
def run(fixture):
    inst=json.loads(pathlib.Path(fixture).read_text())['instance'];edges=list(map(tuple,inst['edges']));N=inst['N'];arcs=[a for e in edges for a in (e,e[::-1])]
    def structured(truths,which):
        return [(0,1)]+[(0 if val else 1,i+2) for i,val in enumerate(truths)]+[(which+2,j) for j in range(4,8)]
    def oriented(T,r):
        adj=[[] for _ in range(N)]
        for a,b in T:adj[a].append(b);adj[b].append(a)
        seen={r};stack=[r];out=set()
        while stack:
            a=stack.pop()
            for b in adj[a]:
                if b not in seen:seen.add(b);stack.append(b);out.add((a,b))
        require(len(out)==N-1 and len(seen)==N,'full_tree_orientation')
        return out
    x={e:Fraction(1 if e==(0,1) else 1,1 if e==(0,1) else 2) for e in edges};zs=[]
    for r in range(N):
        signs=[l>0 for l in inst['normalization']['clauses'][r-4]] if r>=4 else [True,True]
        trees=[structured([signs[0],not signs[1]],0),structured([not signs[0],signs[1]],1)]
        orientations=[oriented(T,r) for T in trees]
        z={a:sum(Fraction(int(a in O),2) for O in orientations) for a in arcs}
        for a,b in edges:require(z[a,b]+z[b,a]==x[a,b],'common_edge_lift_equation')
        for v in range(N):require(sum(z[a] for a in arcs if a[1]==v)==int(v!=r),'rooted_lift_indegree')
        require(all(v>=0 for v in z.values()),'lift_nonnegative')
        zs.append(z)
    require(sum(x.values())==N-1,'projected_cardinality')
    val=sum(inst['costs'][r][i]*zs[r][a] for r in range(N) for i,a in enumerate(arcs))
    require(val==10,'joint_lift_objective_ten')
    require(json.loads(pathlib.Path(fixture).read_text())['exact_minimum']==11,'integer_minimum_matches_independent_fixture_census')
    result={'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'PID':os.getpid(),'optimization':sys.flags.optimize,'all_pass':True,'roots':N,'root_arc_entries':N*len(arcs),'pair_equations':N*len(edges),'indegree_equations':N*N,'fractional_feasible_objective':str(val),'integer_minimum':11,'projection_vs_joint_lift_qualification_supported':True,'source_sha256':hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest(),'scope':'Checkable exact rational point in named classical lift. No historical-priority inference.'}
    print(json.dumps(result))
if __name__=='__main__':run(sys.argv[1])

