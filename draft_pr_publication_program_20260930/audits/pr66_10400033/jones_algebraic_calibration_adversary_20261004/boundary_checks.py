"""Small boundary and convention controls; no universal-bridge inference."""
import datetime,json,pathlib
from fractions import Fraction
import independent_tl_calibration as c

ROOT=pathlib.Path(__file__).resolve().parent
seq=[None]*6
for label,(tail,head) in enumerate(c.P): seq[tail]=(label,True); seq[head]=(label,False)
formal_p,counts=c.arrow_evaluation(seq,{0:1,1:1,2:1})
assert formal_p==Fraction(1,2)
# Nonrealizability certificate: P has chord-degree sequence (2,1,1),
# violating the classical Gauss necessary condition (even number of endpoints
# between each crossing's two preimages). For an immersed closed plane curve,
# smoothing a crossing yields two closed plane curves intersecting evenly.
def intersects(a,b):
    x,y=sorted(a); return (x<b[0]<y)!=(x<b[1]<y)
degrees=[sum(intersects(a,b) for j,b in enumerate(c.P) if i!=j) for i,a in enumerate(c.P)]
assert sorted(degrees)==[1,1,2]

trefoil_components,signs=c.gauss_from_braid(2,(1,1,1))
trefoil_seq=trefoil_components[0]
wrong_T=((0,3),(1,4),(5,2))
wrong_key=c.pattern_key(wrong_T)
selected={crossing:{} for crossing in signs}
for i,(crossing,over) in enumerate(trefoil_seq): selected[crossing]['t' if over else 'h']=i
key=c.pattern_key([(x['t'],x['h']) for x in selected.values()])
assert key==c.TK and key!=wrong_key
even_table=[]
for n in range(0,101,2):
    k=n//2
    bound=Fraction(n*(n*n-4),24)
    assert bound==Fraction(k*(k*k-1),3) and bound.denominator==1
    assert bound<=n*(n*n-1)//24
    if n<=14: even_table.append({'n':n,'even_bound':int(bound),'target_floor':n*(n*n-1)//24})

out={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'formal_P_value':str(formal_p),'formal_P_intersection_degrees':degrees,'formal_P_is_classical':False,'formal_integrality_is_false':True,'wrong_single_T_arrow_direction_trefoil_value':0,'correct_trefoil_value':1,'even_integrality_identity':'n=2k => n(n^2-4)/24 = k(k-1)(k+1)/3, integer since three consecutive integers include a multiple of 3','even_values':even_table,'status':'PASS','scope':'No knot counterexample. This detects false extension of integrality to arbitrary formal/virtual Gauss diagrams; candidate makes no such invariant claim.'}
(ROOT/'boundary_results.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
