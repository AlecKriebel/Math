"""Own exact control: normal expectation need not descend through normal quotient.
This finite-dimensional algebraic obstruction supplements the universal written
argument; it is not a bilateral infinite sequence or universal theorem certificate.
"""
from fractions import Fraction as F
import itertools,json
checks=0
def need(p,m):
 global checks
 checks+=1
 if not p:raise ValueError(m)
def mm(a,b):
 return tuple(tuple(sum(a[i][k]*b[k][j] for k in range(2))for j in range(2))for i in range(2))
def mul(a,b):return(mm(a[0],b[0]),a[1]*b[1])
def E(a):
 x,l=a
 return(((x[0][0],F(0)),(F(0),l)),l)
def rho(a):return a[0]
zero=((F(0),F(0)),(F(0),F(0)))
unit=((F(1),F(0)),(F(0),F(1)))
need(E((unit,F(1)))==(unit,F(1)),"unital")
cases=positive=module=0
for entries in itertools.product([F(-1),F(0),F(1)],repeat=5):
 a=((entries[:2],entries[2:4]),entries[4]);need(E(E(a))==E(a),"idempotent");cases+=1
 # Exact positivity input xx* and nonnegative scalar.
 x=a[0];xt=tuple(zip(*x));p=(mm(x,xt),a[1]*a[1]);ep=E(p)
 need(ep[0][0][0]>=0 and ep[0][1][1]>=0 and ep[1]>=0,"positive diagonal output");positive+=1
 for c,d in [(F(1),F(2)),(F(-1),F(0)),(F(2),F(-3))]:
  t=(((c,F(0)),(F(0),d)),d)
  need(E(mul(t,a))==mul(t,E(a)),"left bimodule")
  need(E(mul(a,t))==mul(E(a),t),"right bimodule");module+=1
kernel=(zero,F(1))
need(rho(kernel)==zero,"quotient kernel")
need(rho(E(kernel))!=zero,"kernel is not expectation invariant")
need(E(kernel)==(((F(0),F(0)),(F(0),F(1))),F(1)),"explicit nondescend witness")
# Tail range restriction: every diagonal target diag(c,d) has exact-radius
# lift (diag(c,d),d) because its direct-sum norm is max(abs(c),abs(d)).
for c,d in itertools.product([F(-3,2),F(0),F(2,3)],repeat=2):
 t=(((c,F(0)),(F(0),d)),d)
 need(E(t)==t,"tail lift fixed")
 need(max(abs(c),abs(d),abs(t[1]))==max(abs(c),abs(d)),"exact radius");cases+=1
rejects=0
for bad,label in [
 (rho(E(kernel))==zero,"blanket normal descent"),
 (E((unit,F(0)))==(unit,F(0)),"expectation global identity"),
 (E((zero,F(1)))==(zero,F(0)),"discard quotient kernel before expectation")]:
 try:need(bad,label)
 except ValueError:rejects+=1
 else:raise ValueError("false claim accepted")
print(json.dumps({"schema":"own-normal-quotient-descent-control/v1","checks":checks,"algebra_cases":cases,"positive_inputs":positive,"bimodule_pairs":module,"false_variants_rejected":rejects,"universal_theorem_from_finite_tests":False},sort_keys=True,separators=(",",":")))

