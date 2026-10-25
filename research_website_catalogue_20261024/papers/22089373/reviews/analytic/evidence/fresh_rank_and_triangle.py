"""Additional fresh exact rank and triangle checks, using our own switching implementation."""
from fresh_graph_fourier import *
import sympy as s
from sympy.polys.matrices import DomainMatrix
from datetime import datetime,timezone
xx=s.symbols('a0:8');v,w=s.symbols('v w');vars=xx+(v,w)
q=[s.expand(coordinate(omega,labels,tuple(map(int,g)),list(xx)+[s.Integer(1)]*4,[v,w])) for g in orbits]
J=s.Matrix(q).jacobian(vars)
# Generic fraction-field RREF proves an upper bound, rather than sampling points.
D=DomainMatrix.from_Matrix(J).to_field()
print('starting symbolic Omega rank',flush=True)
rref,pivots=D.rref()
assert len(pivots)==6
for g,cg in zip(orbits,q):assert s.expand(xx[4]*s.diff(cg,xx[4])+xx[7]*s.diff(cg,xx[7])-int(g[3]!='0')*cg)==0
print('Omega generic rank six and all 14 Euler identities exact',flush=True)
# Three orientations of a 3-sunlet, generic graph engine, independently selected rank minors.
arcs=[('R','A'),('R','B'),('A','H'),('B','H'),('A','LA'),('B','LB'),('H','LH')]
point=list(map(F,['1/2','1/2','1/4','1/4','1/512','1/512','1/320','1/2']))
res=[];tensors=[]
for retic in range(3):
 other=[i for i in range(3) if i!=retic];lm={'LA':other[0],'LB':other[1],'LH':retic}
 tens=[coordinate(arcs,lm,g,point[:7],point[7:]) for g in product(range(4),repeat=3)];tensors.append(tens)
 JJ=jacobian(arcs,lm,point,[(0,1,1),(1,0,1),(1,1,0),(1,2,3)])
 from itertools import combinations
 found=next((col,det([[row[i] for i in col] for row in JJ])) for col in combinations(range(8),4) if det([[row[i] for i in col] for row in JJ]))
 res.append({'reticulation_label':retic,'columns':found[0],'rank4_minor':str(found[1])})
 assert [coordinate(arcs,lm,g,point[:7],point[7:]) for g in [(0,1,1),(1,0,1),(1,1,0),(1,2,3)]]==[F(1,1048576)]*3+[F(1,1342177280)]
assert tensors[0]==tensors[1]==tensors[2]
# Formula behind trinet invariant, with strict JC edge product f.
a,b,c,d,e,f,l=s.symbols('a b c d e f l')
qt=a*b*c*f*(l*d+(1-l)*e);q12=a*b*f;q13=a*c*(l*d+(1-l)*e*f);q23=b*c*(l*d*f+(1-l)*e)
assert s.expand(q12*q13*q23-qt**2-a*a*b*b*c*c*f*l*(1-l)*d*e*(1-f)**2)==0
Path(__file__).with_name('fresh-rank-triangle.json').write_text(json.dumps({'utc':datetime.now(timezone.utc).isoformat(),'status':'PASS','omega_generic_core_rank':len(pivots),'omega_pivot_columns':pivots,'omega_euler_identities':14,'triangle_all64_equal':True,'triangle_rank4_minors':res,'trinet_invariant_factorization':True},indent=2)+'\n')
print('PASS all fresh rank/triangle controls',flush=True)
