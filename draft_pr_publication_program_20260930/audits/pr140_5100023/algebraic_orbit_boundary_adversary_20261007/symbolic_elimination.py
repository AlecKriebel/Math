#!/usr/bin/env python3
"""Unspecialized polynomial certificates and author guard diagnostic only."""
import sympy as sp
from pathlib import Path
from datetime import datetime,timezone
import os,sys,json,hashlib,ast
start=datetime.now(timezone.utc).isoformat()
a,b,C,S,U,h,lam=sp.symbols('a b C S U h lam')
gap=a*a-b*b
D2=C*C/(a*a)+S*S/(b*b)
K=a*a*b*b-lam*gap
qx=(C*(a*a+gap*(U*U-C*C))-h*a*U)/(a*U-h*C)
qy=(a*S*(b*b-gap*(U*U+C*C))+2*h*gap*C*S*U)/(b*(a*U-h*C))
# Both independent line equations, after sum/difference and V²=1-U².
avg=(a*a*C*C+b*b*S*S)*U*U+(a*a*S*S+b*b*C*C)*(1-U*U)-h*a*C*U
coeffavg=(a*C*U-h,b*S*U)
diff=h*a*S-2*gap*C*S*U
coeffdiff=(-a*S,b*C)
G0=sp.groebner([S*S+C*C-1,h*h-gap],h,S,domain=sp.QQ.frac_field(a,b,C,U))
G=sp.groebner([S*S+C*C-1,h*h-gap,a*a*b*b*U*U-a*a*b*b+lam*(b*b*C*C+a*a*S*S)],h,U,S,domain=sp.QQ.frac_field(a,b,C,lam))
certificates=[]
def remainder(expr,basis):
 num=sp.together(expr).as_numer_denom()[0]
 return sp.factor(basis.reduce(sp.expand(num))[1])
def check(name,expr,basis):
 r=remainder(expr,basis)
 if r!=0:raise ValueError(name+': '+str(r))
 certificates.append({'name':name,'cleared_numerator_remainder':str(r)})
check('absolute line-system average residual',coeffavg[0]*qx+coeffavg[1]*qy-avg,G0)
check('absolute line-system difference residual',coeffdiff[0]*qx+coeffdiff[1]*qy-diff,G0)
opp={C:-C,S:-S}
px=qx+qx.subs(opp,simultaneous=True)
py=qy+qy.subs(opp,simultaneous=True)
check('opposite x intermediate',px-2*h*b*b*(C*C-U*U)/(b*b-lam),G)
check('opposite x final',px-(-2*h+2*h*K*C*C/(a*a*(b*b-lam))),G)
check('opposite y final',py-2*h*K*S*C/(a*b*(b*b-lam)),G)
check('focal denominator factor',a*a*U*U-gap*C*C-a*a*(b*b-lam)*D2,G)
check('chord length squared',4*(1-U*U)*(a*a*S*S+b*b*C*C)-4*a*a*b*b*lam*D2*D2,G)
# Controls are performed through the same algebraic reduction function.
controls=[]
for name,expr in [('wrong_x_sign',px-(-2*h-2*h*K*C*C/(a*a*(b*b-lam)))),('omitted_y_term',py),('wrong_line_constant',coeffavg[0]*qx+coeffavg[1]*qy-avg-1)]:
 if remainder(expr,G)==0:raise ValueError('corruption not rejected: '+name)
 controls.append(name)
# Compile only the original ck function, with the actual interpreter mode.
source=Path(__file__).parent.parent/'original'/'verify.py'
tree=ast.parse(source.read_text());nodes=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='ck']
if len(nodes)!=1:raise ValueError('ck source isolation')
module=ast.fix_missing_locations(ast.Module(body=nodes,type_ignores=[]));env={'checks':0}
exec(compile(module,str(source),'exec',optimize=sys.flags.optimize),env)
try:env['ck'](False)
except AssertionError:reject=True
else:reject=False
if reject!=(sys.flags.optimize==0):raise ValueError('unexpected author guard behavior')
r={'schema':'pr140-independent-symbolic-certificates/v1','verdict':'PASS','UTC_start':start,'UTC_end':datetime.now(timezone.utc).isoformat(),'actual_PID':os.getpid(),'optimized':sys.flags.optimize>0,'sympy_version':sp.__version__,'certificates':certificates,'false_controls_rejected':controls,'author_ck_false_rejected':reject,'author_ck_optimized_is_vacuous':sys.flags.optimize>0 and not reject,'author_source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'symbolic_source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'assumptions':'a>b>0; 0<lambda<b²; C²+S²=1; U>0; h²=a²−b²; confocal tangency; nonzero denominators proved analytically','whole_author_verifier_executed':False,'other_family_read':False}
Path(sys.argv[1]).write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({'verdict':r['verdict'],'actual_PID':r['actual_PID'],'UTC_end':r['UTC_end'],'certificates':len(certificates),'false_controls':controls,'author_ck_false_rejected':reject,'optimized':r['optimized']}))
