"""Recompute actual-chord reflection and all four area reversal/repetition from frozen independent vertices."""
from pathlib import Path
import json,mpmath as mp
mp.mp.dps=100
from independent_billiard import dot,sub,scale,cross,foot,tfoot,n_at,area
root=Path(__file__).resolve().parent;rows=json.loads((root/'independent_billiard_results.json').read_text())['results'];out=[]
for row in rows:
 a=mp.mpf(row['a']);b=mp.mpf(row['b']);N=row['N'];c=mp.sqrt(a*a-b*b);P=[tuple(mp.mpf(x) for x in p) for p in row['vertices']]
 error=mp.mpf(0);min_incoming=mp.inf;min_outgoing=mp.inf;min_det=mp.inf
 for i in range(N):
  vin=sub(P[i],P[(i-1)%N]);vin=scale(1/mp.sqrt(dot(vin,vin)),vin)
  vout=sub(P[(i+1)%N],P[i]);vout=scale(1/mp.sqrt(dot(vout,vout)),vout);n=n_at(P[i],a,b);tangent=(-n[1],n[0])
  error=max(error,abs(dot(sub(vin,vout),tangent)),abs(dot(tuple(vin[j]+vout[j] for j in range(2)),n)))
  min_incoming=min(min_incoming,dot(vin,n));min_outgoing=min(min_outgoing,-dot(vout,n))
 values=[]
 for sig in [1,-1]:
  f=(sig*c,mp.mpf(0))
  def feet(poly):return [foot(f,poly[i],poly[(i+1)%len(poly)]) for i in range(len(poly))]
  def outerfeet(poly):return [tfoot(f,n_at(p,a,b)) for p in poly]
  for make in [feet,outerfeet]:
   Q=make(P);Ar=area(Q);reversed_area=area(make(list(reversed(P))));repeated_area=area(make(P*3))
   for i in range(N):min_det=min(min_det,cross(sub(Q[i],f),sub(Q[(i+1)%N],f)))
   values.append({'area':mp.nstr(Ar,80),'reversal_residual':mp.nstr(abs(reversed_area+Ar),80),'repetition_residual':mp.nstr(abs(repeated_area-3*Ar),80)})
 out.append({'a':row['a'],'N':N,'tau':row['winding'],'r':row['r_phase'],'actual_chord_reflection_max_residual':mp.nstr(error,80),'min_incoming_normal':mp.nstr(min_incoming,80),'min_outgoing_normal':mp.nstr(min_outgoing,80),'min_consecutive_focal_determinant':mp.nstr(min_det,80),'areas':values})
result={'evidence':'Finite NONINTERVAL100dps recomputation from85-digit stored direct-orbit vertices','samples':len(out),'max_actual_chord_reflection_residual':mp.nstr(max(mp.mpf(x['actual_chord_reflection_max_residual']) for x in out),80),'max_all_four_area_reversal_residual':mp.nstr(max(mp.mpf(v['reversal_residual']) for x in out for v in x['areas']),80),'max_all_four_area_repetition_residual':mp.nstr(max(mp.mpf(v['repetition_residual']) for x in out for v in x['areas']),80),'minimum_consecutive_focal_determinant':mp.nstr(min(mp.mpf(x['min_consecutive_focal_determinant']) for x in out),80),'results':out}
print(json.dumps({k:v for k,v in result.items() if k!='results'},indent=2));(root/'stored_geometry_crosschecks_results.json').write_text(json.dumps(result,indent=2)+'\n')
