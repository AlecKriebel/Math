from pathlib import Path
from itertools import permutations
import json
source=(Path(__file__).resolve().parent.parent/'checks/colored_involutions.py').read_text()
# Expose the already-enumerated list in an in-memory copy; no release change.
source=source.replace("    return {'vertices':n", "    globals()['audit_automorphisms']=autos\n    return {'vertices':n")
ns={'__name__':'audit_module'};exec(compile(source,'audited_solver_memory','exec'),ns)
D=ns['alternating_class'](6,2);M,C=ns['tables'](D);result=ns['solve'](M,C);A=ns['audit_automorphisms'];pos={x:i for i,x in enumerate(D)}
ambient=set()
for g in permutations(range(6)):
 inv=[0]*6
 for i,j in enumerate(g):inv[j]=i
 f=tuple(pos[tuple(g[x[inv[i]]] for i in range(6))] for x in D)
 if f[0]==0:ambient.add(f)
extra=[f for f in A if tuple(f) not in ambient]
assert len(ambient)==16 and len(extra)==16 and len(A)==32
f=extra[0]
assert all(M[i][j]==M[f[i]][f[j]] and f[C[i][j]]==C[f[i]][f[j]] for i in range(45) for j in range(45))
out={'stabilizer':32,'six_letter_stabilizer':16,'exceptional_outer_stabilizer_elements':16,'one_extra_vertex_map':f}
json.dump(out,open(Path(__file__).resolve().parent/'a6_outer_witness.json','w'),indent=2)
print({k:v for k,v in out.items() if k!='one_extra_vertex_map'})
