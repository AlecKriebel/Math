"""Exact repeated-odd boundary; independent SymPy verification, no author imports."""
from pathlib import Path
import datetime,hashlib,json,os,sys
import sympy as S
r=S.sqrt(13);x=2*(1-r)/3;y=S.sqrt(2*r-5)/3
a,b=S.Integer(2),S.Integer(1);lam=S.simplify(4-x*x)
A=(a,S.Integer(0));B=(x,y);C=(x,-y);P=[A,B,C]
checks=0
def ck(v,message):
 global checks
 if not v:raise RuntimeError(message)
 checks+=1
def zero(v,message):ck(S.simplify(v)==0,message)
def dot(v,w):return v[0]*w[0]+v[1]*w[1]
def sub(v,w):return tuple(v[i]-w[i] for i in range(2))
def q(A,B):
 det=A[0]*B[1]-A[1]*B[0]
 ck(det.is_zero is False,'nonzero origin antipedal determinant')
 return ((dot(A,A)*B[1]-dot(B,B)*A[1])/det,(A[0]*dot(B,B)-B[0]*dot(A,A))/det)
ck(lam.is_positive is True and S.simplify(1-lam).is_positive is True,'strict confocal ellipse parameter')
for V in P:zero(V[0]**2/4+V[1]**2-1,'ellipse point')
length=S.simplify(y*(3-8/x))
ck(length.is_positive is True,'positive side length')
zero(length**2-dot(sub(B,A),sub(B,A)),'positive reflected-side length')
incoming=((x-2)/length,y/length);outgoing=(S.Integer(0),S.Integer(-1));normal=(x/4,y)
zero((incoming[0]-outgoing[0])*normal[1]-(incoming[1]-outgoing[1])*normal[0],'reflection at B')
zero(((x-2)/length)*(-y)-(-1-y/length)*(x/4),'reflection at C')
# Reflection at C follows y-axis-coordinate sign reversal; at A horizontal
# normal follows from equal lengths AB and AC. Verify that directly too.
zero(((2-x)/length-(x-2)/length)*0-(y/length-y/length)*S.Rational(1,2),'reflection at A')
# Direct support-function tangency of AB; BC has x fixed and x²=4−lambda.
zero((4-lam)*y*y+(1-lam)*(2-x)**2-(2*y)**2,'side AB tangency to same caustic')
zero(x*x-(4-lam),'side BC tangency to same caustic')
Q=[q(P[i],P[(i+1)%3]) for i in range(3)]
centroid=tuple(S.simplify(sum(q[j] for q in Q)/3) for j in range(2))
target=5*(7-r)/24
zero(centroid[0]-target,'exact nonzero triangle antipedal origin centroid x')
zero(centroid[1],'exact triangle antipedal origin centroid y')
ck(target.is_positive is True,'centroid nonzero')
Q6=Q+Q
zero(sum(q[0] for q in Q6)/6-target,'six-entry repeated triangle same centroid')
zero(sum(q[1] for q in Q6)/6,'six-entry repeated triangle centroid y')
# Its centrally reflected orbit belongs to the same confocal caustic and
# has centroid−target. Thus an even list-size formulation would be false.
receipt={'schema':'pr140-exact-repeated-odd-boundary/v1','UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'actual_PID':os.getpid(),'mode':'optimized' if sys.flags.optimize else 'normal','status':'PASS','checks':checks,'a':'2','b':'1','least_period':3,'repeated_list_length':6,'x_vertex':str(x),'y_vertex':str(y),'lambda':str(lam),'origin_centroid':list(map(str,centroid)),'centrally_reflected_origin_centroid':[str(-centroid[0]),'0'],'interpretation':'Exact counterexample only to even-list-length parity, not to the candidate primitive-even theorem. The source opposite-vertex convention supports excluding this list.','no_author_verifier_or_other_family_read':True,'no_new_central_proof_search_turn':True}
out=Path(__file__).resolve().parent/('EXACT_ODD_BOUNDARY_OPTIMIZED.json' if sys.flags.optimize else 'EXACT_ODD_BOUNDARY_NORMAL.json')
if out.exists():raise RuntimeError('Preserve exact boundary result')
out.write_text(json.dumps(receipt,indent=2,sort_keys=True)+'\n')
print(json.dumps({'mode':receipt['mode'],'UTC':receipt['UTC'],'PID':os.getpid(),'status':'PASS','checks':checks,'lambda':receipt['lambda'],'origin_centroid':receipt['origin_centroid']}))
