import sys,pickle
from pathlib import Path
from fractions import Fraction as F
ROOT=Path('/mnt/data/k3p_identifiability_final');P=Path('/mnt/data/k3p_work/input_unpacked/k2p_offline_four_port_sweep_package_resurfaced/k2p_offline_sweep_portable')
sys.path[:0]=[str(ROOT/'software/atlas'),str(P/'atlas')]
import k3p_atlas_core as k3, k2p_atlas_core as k2
sources=k3.source_supports(('theta0','theta1','theta3'))
for i,r in enumerate(sources):
 d2=k2.model_descriptor_fast2(r.graph);d3=k3.model_descriptor_fast2(r.graph)
 s,g=F(2,7),F(3,11);lams=tuple(F(j+2,j+5) for j in range(d2.retic_count))
 v2=k2.eval_descriptor(d2,tuple((s,g) for _ in range(d2.edge_class_count)),lams)
 v3=k3.eval_descriptor(d3,tuple((s,g,s) for _ in range(d3.edge_class_count)),lams)
 m3=dict(zip(k3.k3p_assignments(4),v3))
 for chars,val in zip(k2.orbit_assignments(4),v2):assert m3[chars]==val,(i,chars)
 for chars,val in m3.items():
  sw=tuple(3 if x==1 else 1 if x==3 else x for x in chars);assert m3[sw]==val
 print('PASS',i)
print('K3P_TO_K2P_SPECIALIZATION_PASS')
