"""Generate the BCF turn-graph LP; optionally solve with SymPy 1.14.
No float is used in the LP construction or certificate verification.
"""
from pathlib import Path
from fractions import Fraction as F
import json,sys,hashlib,datetime
WORD='acacAcACCC'
def model(word=WORD):
 n=len(word)
 assert n>0 and all(word[i].swapcase()!=word[(i+1)%n] for i in range(n))
 assert all(word.count(x)==word.count(x.swapcase()) for x in set(word))
 edges=[(i,j) for i in range(n) for j in range(n) if word[i].swapcase()==word[(j+1)%n]]
 adj={i:[j for a,j in edges if a==i] for i in range(n)}
 cycles=[]
 def search(path):
  i=path[-1]; start=path[0]
  for j in adj[i]:
   if j==start: cycles.append(path)
   elif j>start and j not in path: search(path+[j])
 for start in range(n):search([start])
 def dual(e):i,j=e;return ((j+1)%n,(i-1)%n)
 pairs=[(e,dual(e)) for e in edges if e<dual(e)]
 assert len(pairs)*2==len(edges)
 cycle_edges=[set(zip(c,c[1:]+c[:1])) for c in cycles]
 rows=[[int(i in c) for c in cycles] for i in range(n)]
 rows += [[int(e in ce)-int(d in ce) for ce in cycle_edges] for e,d in pairs]
 return {'word':word,'indexing':'zero-based turn i follows letter i','edges':edges,'dual_pairs':pairs,'circuits':cycles,'A':rows,'b':[1]*n+[0]*len(pairs)}
def check(certificate):
 assert certificate['word']==WORD
 m=model(); A=m['A']; b=m['b']; k=len(m['circuits']); r=len(A)
 u=[F(0)]*k
 for i,v in certificate['primal_nonzero']:u[i]=F(v)
 y=list(map(F,certificate['dual']))
 assert len(y)==r and all(x>=0 for x in u)
 assert [sum(F(a)*x for a,x in zip(row,u)) for row in A]==list(map(F,b))
 slacks=[sum(y[i]*A[i][j] for i in range(r))-1 for j in range(k)]
 assert all(t>=0 for t in slacks)
 primal=sum(u); dual_value=sum(t*bb for t,bb in zip(y,b))
 assert primal==dual_value
 scl=F(len(WORD),4)-primal/2
 assert scl==F(certificate['scl'])
 cut={i for i,v in enumerate(y[:len(WORD)]) if v==1}
 assert cut=={0,1,2,4} and all(v in (0,1) for v in y[:len(WORD)]) and all(v==0 for v in y[len(WORD):])
 topological_order=[3,5,6,7,8,9]; pos={v:i for i,v in enumerate(topological_order)}
 assert set(topological_order)==set(range(len(WORD)))-cut
 assert all(pos[i]<pos[j] for i,j in m['edges'] if i not in cut and j not in cut)
 def reduce_word(w):
  stack=[]
  for x in w:
   if stack and stack[-1]==x.swapcase(): stack.pop()
   else: stack.append(x)
  return ''.join(stack)
 x,yword='acacA','cACA'; inverse=lambda w:w[::-1].swapcase()
 assert reduce_word(x+yword+inverse(x)+inverse(yword))==WORD
 return {'word':WORD,'turns':len(WORD),'directed_edges':len(m['edges']),'embedded_directed_circuits':k,'equality_rows':r,'nonzero_primal_coordinates':sum(x!=0 for x in u),'primal_objective':str(primal),'dual_objective':str(dual_value),'minimum_dual_slack':str(min(slacks)),'scl':str(scl),'cut_complement_acyclic':True,'explicit_commutator':['acacA','cACA'],'commutator_reduces_to_word':True,'all_checks_pass':True}
def solve():
 from sympy import Matrix
 from sympy.solvers.simplex import _simplex
 m=model(); A=m['A']; b=m['b']; k=len(m['circuits']); r=len(A)
 # Exact simplex returns its dual simultaneously. Equality rows are encoded twice.
 inequalities=[[0]*k]+A+[[-v for v in row] for row in A]
 rhs=[0]+b+[-v for v in b]
 value,u,z=_simplex(Matrix(inequalities),Matrix(rhs),Matrix([[-1]*k]))
 y=[z[1+i]-z[1+r+i] for i in range(r)]
 cert={'format':'BCF-primal-dual-v1','word':WORD,'primal_nonzero':[[i,str(v)] for i,v in enumerate(u) if v],'dual':list(map(str,y)),'scl':str(F(len(WORD),4)+F(str(value))/2),'solver':'SymPy 1.14.0 exact rational simplex','created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
 check(cert)
 Path('certificate.json').write_text(json.dumps(cert,indent=2)+'\n')
 Path('model.json').write_text(json.dumps(m,indent=2)+'\n')
 print(json.dumps(check(cert),indent=2))
if __name__=='__main__':
 if '--solve' in sys.argv:solve()
 else:
  p=Path(__file__).parent/'certificate.json'; result=check(json.loads(p.read_text())); result['certificate_sha256']=hashlib.sha256(p.read_bytes()).hexdigest(); print(json.dumps(result,indent=2))
