"""Finite pricing-model boundary check; no new target hardness route."""
from itertools import combinations
import json,datetime,os
V=[0,1,2]
A=[(0,1),(1,0),(0,2),(2,0)]
gamma={(0,1):1,(1,0):1,(0,2):5,(2,0):5}
def solve(demand):
    candidates=[]
    for k in range(3):
      for arcs in combinations(A,k):
        if any(sum(v==i for _,v in arcs)>1 for i in V if i!=0):continue
        prev={0:None};q=[0]
        for u in q:
          for a,b in arcs:
            if a==u and b not in prev:prev[b]=u;q.append(b)
        if any(demand[i]>0 and i not in prev for i in V if i!=0):continue
        f={e:0 for e in A}
        for i in V[1:]:
          if demand[i]==0:continue
          t=i
          while t!=0:
            s=prev[t];f[s,t]+=demand[i];t=s
        M=sum(demand.values())
        assert sum(f[0,j] for _,j in A if _==0)==M
        for i in V[1:]:assert sum(f[a,b] for a,b in A if a==i)-sum(f[a,b] for a,b in A if b==i)==-demand[i]
        assert all(f[e]<=M*int(e in arcs) for e in A)
        candidates.append({'fixed_cost':sum(gamma[e] for e in arcs),'selected_arcs':[list(e) for e in arcs],'positive_demand_vertices':[i for i in V[1:] if demand[i]>0]})
    return min(candidates,key=lambda z:z['fixed_cost'])
optional=solve({1:1,2:0});mandatory=solve({1:1,2:1})
assert optional['fixed_cost']==1 and optional['selected_arcs']==[[0,1]]
assert mandatory['fixed_cost']==6 and mandatory['selected_arcs']==[[0,1],[0,2]]
print(json.dumps({'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'operator_PID':os.getpid(),'root':0,'bidirected_edges':[[0,1],[0,2]],'flow_charge_coefficients':0,'fixed_arc_costs':{'0->1':1,'1->0':1,'0->2':5,'2->0':5},'optional_zero_demand_case':optional,'all_positive_demand_case':mandatory,'constraints_checked':['root supply','nonroot balances','big-M flow/support links','at most N-1 selected arcs','nonroot indegree at most1'],'source_global_assumption_compatible_example':'r_01=1,r_21=1, all other communication requirements0; each vertex has some positive incident communication, while commodity0 has zero demand at vertex2.','limitation':'Finite boundary check of pricing support; no full NP-hardness proof or target reduction is claimed.'},indent=2))
