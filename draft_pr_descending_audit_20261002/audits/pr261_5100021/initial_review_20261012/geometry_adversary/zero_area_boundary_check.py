import json
from pathlib import Path
import direct_geometry_check as g
mp=g.mp
mp.mp.dps=100

def axial_sign(a):
 b=mp.mpf(1);lam=g.caustic(a,b,8,1);poly,_,_=g.orbit(a,b,lam,8,mp.mpf(0))
 p,v,_=g.pedal_anti(poly,(mp.sqrt(a*a-1),mp.mpf(0)))
 return g.area(v),g.area(p),lam
rows=[]
for a in map(mp.mpf,['1.5','2','2.5','3','4','10']):
 aa,ap,lam=axial_sign(a);rows.append({'a':g.strnum(a),'b':'1','lambda':g.strnum(lam),'antipedal_area':g.strnum(aa),'pedal_area':g.strnum(ap)})
lo=mp.mpf('1.5');hi=mp.mpf(10)
for _ in range(150):
 mid=(lo+hi)/2
 if axial_sign(mid)[0]>0:lo=mid
 else:hi=mid
astar=(lo+hi)/2;aa,ap,lam=axial_sign(astar)
phases=[]
for t in map(mp.mpf,['0','.173','.61','1.17','2.013']):
 poly,end,_=g.orbit(astar,mp.mpf(1),lam,8,t)
 p,v,angle=g.pedal_anti(poly,(mp.sqrt(astar*astar-1),mp.mpf(0)))
 phases.append({'phase':g.strnum(t),'pedal_area':g.strnum(g.area(p)),'antipedal_area':g.strnum(g.area(v)),'product':g.strnum(g.area(p)*g.area(v)),'closure':g.strnum(g.norm(g.vsub(end,poly[0]))/astar),'minimum_focal_normal_angle_sine':g.strnum(angle)})
r={'provenance':'Independent direct conic generator, run after submitted-proof exposure to stress the zero-area claim; no author checker read/run. Floating-point rows are diagnostics; exact existence is certified separately in EXACT_ZERO_AREA_BRACKET.json.','rows':rows,'a_zero_estimate':g.strnum(astar),'lambda_zero_estimate':g.strnum(lam),'a_interval_width':g.strnum(hi-lo),'phases':phases}
Path('ZERO_AREA_BOUNDARY.json').write_text(json.dumps(r,indent=2)+'\n')
print('Estimated zero shape:',g.strnum(astar),'lambda',g.strnum(lam),flush=True)
print(json.dumps(r,indent=2))
