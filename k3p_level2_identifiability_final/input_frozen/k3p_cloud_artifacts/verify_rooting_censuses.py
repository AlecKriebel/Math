from pathlib import Path
import sys,json
ROOT=Path('/mnt/data/k3p_identifiability_final');sys.path[:0]=[str(ROOT/'software'),str(ROOT/'software/atlas')]
import k3p_atlas_core as k3
from k3p_graph_map import make_graph
from rooting_census import enumerate_admissible_rootings
W=make_graph([('r','S'),('r','L0'),('S','U'),('S','V'),('U','X'),('V','Z'),('Z','X'),('U','V'),('Z','L1'),('X','L2')],{'V','X'},{'L0':0,'L1':1,'L2':2})
Wp=make_graph([('r','S'),('r','L0'),('S','U'),('S','X0'),('V','X0'),('U','X1'),('V','X1'),('U','V'),('X0','L1'),('X1','L2')],{'X0','X1'},{'L0':0,'L1':1,'L2':2})
# Collision rooted graph in the exact certificate, with dummy Python node roles.
import networkx as nx
C=nx.DiGraph()
roles={'rho':'root','u':'tree','p':'tree','q':'tree','r2':'retic','r3':'retic','1':'leaf','2':'leaf','3':'leaf'}
labels={'1':0,'2':1,'3':2}
for n,r in roles.items():C.add_node(n,role=r,label=labels.get(n))
for e in [('rho','1'),('rho','u'),('u','p'),('u','q'),('p','r2'),('q','r2'),('p','r3'),('q','r3'),('r2','2'),('r3','3')]:C.add_edge(*e)
res={}
for name,G,want in [('W',W,(5,2,3)),('Wprime',Wp,(7,2,5)),('collision',C,None)]:
 M=k3.sd0_mixed(G);rr=enumerate_admissible_rootings(M);got=(len(rr),sum(x['tree_child'] for x in rr),sum(not x['tree_child'] for x in rr))
 if want is not None:assert got==want,(name,got,want)
 res[name]={'admissible':got[0],'tree_child':got[1],'non_tree_child':got[2],'rootings':[{'root_edge':x['root_edge'],'bits':list(x['bits']),'tree_child':x['tree_child']} for x in rr]}
 print(name,got)
(ROOT/'software/certificates/k3p_rooting_censuses.json').write_text(json.dumps(res,indent=2,sort_keys=True)+'\n')
print('K3P_ROOTING_CENSUS_PASS')
