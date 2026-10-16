#!/usr/bin/env python3
"""Independently check additional archived transversality/face claims.
Use ordinary Python with assertions enabled; run from a writable owned copy
beside independent_check.py and with sibling publication_package_v2 available.
Only this owned folder receives outputs."""
from pathlib import Path
from fractions import Fraction as F
import runpy,contextlib,io,json
R=Path(__file__).resolve().parent
with contextlib.redirect_stdout(io.StringIO()):g=runpy.run_path(str(R/'independent_check.py'))
I,solve,det,sub,n2=g['I'],g['solve'],g['det'],g['vsub'],g['n2'];P=g['P'];A0,B0,C0=g['A'],g['B'],g['C'];lam=g['lam']
cert=json.loads((R.parent/'publication_package_v2/exact_certificate.json').read_text())
Xs=[solve(I(*map(F,e['s'])),A0,B0,C0,lam,I(1))[0] for e in cert['outgoing_root_boxes']];Z=g['Z']
def gd(x,q,r):
 a,b=sub(x,q),sub(x,r);aa=n2(a).pw(7);bb=n2(b).pw(7)
 return tuple(16*(a[k]*aa-b[k]*bb) for k in [0,1])
jacs=[det(gd(x,B0,A0),gd(x,C0,A0)) for x in Xs];ij=det(gd(Z,P[4],P[2]),gd(Z,P[0],P[2]))
assert [j.sign() for j in jacs]==[1,-1,1,-1,1] and ij.sign()==1
def cross(a,b,c,d):
 v=[det(sub(b,a),sub(c,a)),det(sub(b,a),sub(d,a)),det(sub(d,c),sub(a,c)),det(sub(d,c),sub(b,c))]
 return v[0].sign()*v[1].sign()==-1 and v[2].sign()*v[3].sign()==-1
def geometry(x,starts):
 out=[]
 for i in starts:
  v=[P[i],P[(i+1)%6],P[(i+2)%6],x]
  area=sum((det(v[j],v[(j+1)%4]) for j in range(4)),I(0))/2
  assert area.sign()!=0
  out.append({'face_start':i+1,'signed_area_nonzero':True,'crossed':cross(v[0],v[1],v[2],v[3]) or cross(v[1],v[2],v[3],v[0])})
 return out
incoming=geometry(Z,[0,2,4]);outgoing=[geometry(x,[1,3,5]) for x in Xs]
assert [[e['crossed'] for e in row] for row in outgoing]==[[True,False,True],[False,True,False],[False,True,False],[True,False,False],[True,False,False]]
assert incoming[0]['crossed']
out={'status':'PASS_INDEPENDENT_HISTORICAL_GEOMETRY_CLAIMS','outgoing_jacobian_enclosures':[j.coarse() for j in jacs],'incoming_jacobian_enclosure':ij.coarse(),'incoming_faces':incoming,'outgoing_faces':outgoing}
(R/'EXTRA_GEOMETRY_RESULTS.json').write_text(json.dumps(out,indent=2)+'\n')
print(out['status'])
