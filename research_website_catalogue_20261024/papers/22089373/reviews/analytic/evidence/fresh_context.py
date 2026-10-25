"""Fresh physical contextual T test where two triangle terminals reconnect in a theta."""
from fresh_graph_fourier import *
import sympy as sp
from datetime import datetime,timezone
# One internal triangle S,U,V; its U,V terminals reconnect through reticulation X.
# The first two root arcs multiply to the former S-boundary arm.
aV=[('R','S'),('R','L0'),('S','U'),('S','V'),('U','V'),('U','P2'),('P2','X'),('V','P3'),('P3','X'),('P2','L1'),('P3','L2'),('X','L3')]
xV=list(map(F,['1/16','1/32','1/4','1/4','1/4','1/512','1/3','1/320','2/5','3/5','4/7','5/8','1/2','1/2']))
# Reticulation S requires rerooting at the real L1 arm; the old P2-L1 multiplier is 3/5.
aS=[('R','P2'),('R','L1'),('P2','U'),('U','V'),('U','S'),('V','S'),('V','P3'),('S','L0'),('P2','X'),('P3','X'),('P3','L2'),('X','L3')]
xS=list(map(F,['3/4','4/5','1/512','1/4','1/4','1/4','1/512','1/320','1/3','2/5','4/7','5/8','1/2','1/2']))
aU=[('R','S'),('R','L0'),('S','U'),('S','V'),('V','U'),('U','P2'),('P2','X'),('V','P3'),('P3','X'),('P2','L1'),('P3','L2'),('X','L3')]
xU=list(map(F,['1/16','1/32','1/4','1/4','1/4','1/320','1/3','1/512','2/5','3/5','4/7','5/8','1/2','1/2']))
tensors=[];results=[]
for name,a,p in [('V',aV,xV),('S',aS,xS),('U',aU,xU)]:
 assert all(0<v<1 for v in p)
 c=census(a);assert c['admissible']==c['tree_child']>0
 ts=[coordinate(a,labels,g,p[:12],p[12:]) for g in product(range(4),repeat=4)];tensors.append(ts)
 jj=sp.Matrix(jacobian(a,labels,p,[tuple(map(int,g)) for g in orbits]));rank=jj.rank()
 results.append({'triangle_reticulation':name,'rootings':c['admissible'],'all_TC':True,'point_rank':rank,'cycle_lengths':c['cycle_lengths']})
assert tensors[0]==tensors[1]==tensors[2]
assert len({r['point_rank'] for r in results})==1
# Without the changed physical incidence arms, equality must fail.
bad=xS[:];bad[7]=F(1,512)
assert tensors[0]!=[coordinate(aS,labels,g,bad[:12],bad[12:]) for g in product(range(4),repeat=4)]
Path(__file__).with_name('fresh-context.json').write_text(json.dumps({'utc':datetime.now(timezone.utc).isoformat(),'status':'PASS','description':'All three T orientations in an STC theta with a reconnecting context, strict physical parameters and a new root location when needed. This is a nontrivial control, not the universal contextual proof.','all256_fourier_equal':True,'orientations':results,'uncompensated_arm_negative_control_rejected':True,'networks':[{'arcs':a,'point':list(map(str,p))} for a,p in [(aV,xV),(aS,xS),(aU,xU)]]},indent=2)+'\n')
print(json.dumps({'status':'PASS','orientations':results}))
