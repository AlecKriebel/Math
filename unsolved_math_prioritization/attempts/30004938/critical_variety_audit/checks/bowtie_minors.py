from pathlib import Path
BASE = Path(__file__).resolve().parent
import sympy as s,itertools,json
A,B,C,D,E,F,X,Y=s.symbols('A B C D E F X Y')
M=s.Matrix([[0,B*D,D*A,F*A,0],[-D*A,-(B*X+C*D),-X*A,-Y*A,A*A],[X*A,C*X,0,0,0]])
# Columns all multiplied by A^2 compared with binary quadratic form matrix.
out={}
for I in itertools.combinations(range(5),3):
 raw=s.factor(M[:,I].det());simple=s.factor(raw.subs(Y,(F*X-A*E)/D))
 out[''.join(str(i+1) for i in I)]={'det':str(raw),'normalized':str(s.factor(simple/(A**3*X)))}
 print(I,raw,'=>',out[''.join(str(i+1) for i in I)]['normalized'])
open(BASE / 'bowtie_minors.json','w').write(json.dumps(out,indent=2))

expected=[0,B*E,B*D,A*E,A*D,A*F,C*E,C*D,C*F,0]
for result,want in zip(out.values(),expected):
 assert s.simplify(s.sympify(result['normalized'],locals={str(x):x for x in (A,B,C,D,E,F,X,Y)})-want)==0
a,c,d=s.symbols('a c d',real=True)
assert s.trigsimp(s.expand_trig(s.sin(c)*s.sin(a+d)-s.sin(d)*s.sin(a+c)+s.sin(a)*s.sin(d-c)))==0
print('PASS: all ten normalized minors and the trigonometric identity')
