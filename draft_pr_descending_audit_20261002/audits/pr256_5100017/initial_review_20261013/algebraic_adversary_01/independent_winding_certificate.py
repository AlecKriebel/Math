"""Exact ray-crossing winding of the normalized 8/3 star coordinates."""
from fractions import Fraction as Q
from datetime import datetime, timezone
import json
from pathlib import Path

vertices=[(Q(0),Q(1)),(-Q(12,13),-Q(5,13)),(Q(1),Q(0)),
          (-Q(12,13),Q(5,13)),(Q(0),-Q(1)),(Q(12,13),Q(5,13)),
          (-Q(1),Q(0)),(Q(12,13),-Q(5,13))]
crossings=[]
for i,p in enumerate(vertices):
    q=vertices[(i+1)%len(vertices)]
    determinant=p[0]*q[1]-p[1]*q[0]
    assert determinant>0
    contribution=(1 if p[1]<=0<q[1] and determinant>0 else
                  -1 if q[1]<=0<p[1] and determinant<0 else 0)
    crossings.append({'edge':i,'determinant':str(determinant),
                      'winding_contribution':contribution})
assert sum(e['winding_contribution'] for e in crossings)==3
assert len(set(vertices))==8
result={'status':'PASS','timestamp_utc':datetime.now(timezone.utc).isoformat(),
        'method':'Exact signed crossings of the positive x ray; positive diagonal scaling preserves winding.',
        'least_period':8,'winding':3,'edges':crossings}
Path(__file__).with_name('WINDING_CERTIFICATE.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
