"""Independently entered factor expressions over Z[a,b] in a free algebra.

Exact integer-polynomial identities base-change to any field. Bounded reduction
checks are explicitly diagnostics; see MATHEMATICAL_REVIEW.md for the proof.
"""
import itertools, json
def need(v,m):
 if not v: raise ValueError(m)
class P:
 def __init__(self,d=None): self.d={m:c for m,c in (d or {}).items() if c}
 def __add__(self,q):
  d=dict(self.d)
  for m,c in q.d.items(): d[m]=d.get(m,0)+c
  return P(d)
 def __neg__(self): return P({m:-c for m,c in self.d.items()})
 def __sub__(self,q): return self+-q
 def __mul__(self,q):
  d={}
  for (a,b,w),c in self.d.items():
   for (e,f,v),h in q.d.items():
    m=(a+e,b+f,w+v);d[m]=d.get(m,0)+c*h
  return P(d)
 def __eq__(self,q): return self.d==q.d
def c(n):return P({(0,0,()):n})
def x(i):return P({(0,0,(i,)):1})
def substitute(p,images):
 out=P()
 for (ae,be,w),coeff in p.d.items():
  q=P({(ae,be,()):coeff})
  for i in w:q=q*images[i]
  out=out+q
 return out
def commutative(p):
 out=P()
 for (ae,be,w),coeff in p.d.items():out=out+P({(ae,be,tuple(sorted(w))):coeff})
 return out
def source(y,a,b):
 return [y[1]*(a*y[1]-y[3])+y[3]*(y[1]-a*y[3]),
 y[1]*(a*y[2]-y[4])+y[3]*(y[2]-a*y[4]),
 y[2]*(a*y[1]-y[3])+y[4]*(y[1]-a*y[3]),
 y[2]*(a*y[2]-y[4])+y[4]*(y[2]-a*y[4]),
 y[1]*(b*y[1]-y[2])+y[4]*(y[1]-b*y[2]),
 y[1]*(b*y[3]-y[4])+y[4]*(y[3]-b*y[4])]
def run():
 a=P({(1,0,()):1});b=P({(0,1,()):1});one=c(1);z=P();X=x(0);Y=x(1)
 f=source({i:x(i+1) for i in range(1,5)},a,b)
 collapse={2:X,3:Y,4:X,5:Y}
 Q=b*X*X-X*Y+Y*X-b*Y*Y
 need([substitute(v,collapse) for v in f]==[z,z,z,z,Q,Q],'six quotient images')
 need(all(substitute(v,{i:X for i in range(2,6)})==z for v in f),'diagonal specialization')
 theta={0:X+b*Y,1:b*X+Y}
 def product_twisted(p):
  out=P()
  for (ae,be,w),coeff in p.d.items():
   need(len(w)==2,'quadratic tensor')
   out=out+P({(ae,be,()):coeff})*x(w[0])*theta[w[1]]
  return out
 twisted=product_twisted(Q)
 need(twisted==-(one-b*b)*(X*Y-Y*X),'free tensor determinant identity')
 need(commutative(twisted)==z,'THCR relation')
 need(commutative(Q)==b*(X*X-Y*Y),'ordinary target wrong generically')
 uv=substitute(Q,{0:X+Y,1:Y})
 need(uv==b*X*X+(b-one)*X*Y+(b+one)*Y*X,'all-characteristic triangular basis')
 signs=[]
 for j,v in enumerate(f):
  m=next(iter(v.d));changed=dict(v.d);changed[m]=-changed[m]
  need(substitute(P(changed),collapse)!=substitute(v,collapse),'undetected sign '+str(j))
  signs.append(j+1)
 # A VU rewrite replaces its first V by U, proving the relevant local decrease.
 # Check every finite binary word to degree 10 as implementation diagnostics only.
 comparisons=0
 for n in range(2,11):
  for w in itertools.product((0,1),repeat=n):
   for j in range(n-1):
    if w[j:j+2]==(1,0):
     need(w[:j]+(0,1)+w[j+2:]<w and w[:j]+(0,0)+w[j+2:]<w,'lex decrease')
     comparisons+=1
 return {'result':'PASS','coefficient_ring':'Z[alpha,beta]',
 'universal_polynomial_identities':['six images 0,0,0,0,Q,Q','diagonal xi=t','tensor twist Q=-(1-beta^2)(XY-YX)','THCR relation zero','triangular U,V expression'],
 'relation_sign_controls_rejected':signs,'bounded_lex_comparisons':comparisons,
 'interpretation':'Polynomial identities are exact; bounded word checks are diagnostics. Universal field/domain/kernel/Hilbert claims have a written proof, not a finite-test extrapolation.'}
if __name__=='__main__':print(json.dumps(run(),indent=2,sort_keys=True))
