"""Independent algebra check in the exact specified F3 semidirect product.
This is corroboration; two-way Tietze equivalence is proved in AUDIT.md.
"""
import json,pathlib

def inv(w):return w.swapcase()[::-1]
def red(w):
 s=[]
 for c in w:
  if s and s[-1]==c.swapcase():s.pop()
  else:s.append(c)
 return ''.join(s)
phi={'a':'a','b':'ab','c':'bcb'}
psi={'a':'a','b':'Ab','c':'BacBa'}
def apply(w,m):return red(''.join(m[c] if c.islower() else inv(m[c.lower()]) for c in w))
for c in 'abc':assert apply(phi[c],psi)==c and apply(psi[c],phi)==c
def power(w,n):
 for _ in range(abs(n)):w=apply(w,phi if n>0 else psi)
 return w
def mul(u,v):return red(u[0]+power(v[0],u[1])),u[1]+v[1]
def inverse(u):return power(inv(u[0]),-u[1]),-u[1]
def prod(*args):
 r=('',0)
 for a in args:r=mul(r,a)
 return r

a=('a',0);b=('b',0);c=('c',0);t=('',1)
x=t;y=prod(inverse(a),t);z=prod(inverse(c),inverse(t))
zv={'A':z}
zv['B']=prod(x,z,inverse(y))
zv['C']=prod(inverse(y),z,x)
zv['D']=prod(inverse(y),zv['B'],x)
K={'x':x,'y':y,'b':b}
lam={'x':y,'y':x,'b':inverse(b)}
qedges={ 'p':('B','A','x'),'q':('A','C','y'),'r':('D','C','x'),
         's':('B','D','y'),'d':('A','B','b'),'e':('C','A','b') }
checks={}
checks['xyXY']=prod(x,y,inverse(x),inverse(y))
checks['bxBY']=prod(b,x,inverse(b),inverse(y))
for e,(u,v,l) in qedges.items():checks['product_'+e]=prod(K[l],zv[v],inverse(lam[l]),inverse(zv[u]))
checks['HNN']=prod(inverse(z),b,x,z,inverse(y),b)
assert all(r==('',0) for r in checks.values()),checks
# Inverse generator recovery inside the target.
assert prod(x,inverse(y))==a
assert inverse(prod(z,x))==c
# Explicit lambda^2 and f=b^-1 lambda calculations are written in audit prose.
result={'status':'PASS','phi':phi,'phi_inverse':psi,
 'vertical_generator_normal_forms':zv,'nine_target_relation_checks':checks,
 'limitation':'Word computations in G establish the forward homomorphism; written reversible Tietze elimination establishes the reverse isomorphism.'}
p=pathlib.Path(__file__).with_name('independent_algebra_results.json')
p.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
