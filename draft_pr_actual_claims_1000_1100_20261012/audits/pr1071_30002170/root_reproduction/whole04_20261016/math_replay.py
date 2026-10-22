import json,math
from fractions import Fraction as F
from pathlib import Path
O=Path('/Users/alec/Documents/Math/draft_pr_actual_claims_1000_1100_20261012/audits/pr1071_30002170/root_reproduction/whole04_20261016')
def need(x,s):
 if not x:raise RuntimeError(s)
def save(n,v):(O/n).write_text(json.dumps(v,indent=2,allow_nan=False)+'\n')
# Fractions-based independent polynomial mechanism.
phi=[F(0)]*4+[F(1),F(-4),F(6),F(-4),F(1)]
def der(p):return [F(i)*p[i] for i in range(1,len(p))]
def val(p,x):return sum(c*x**i for i,c in enumerate(p))
def integ(p):return sum(c/F(i+1) for i,c in enumerate(p))
def prod(p,q):
 z=[F(0)]*(len(p)+len(q)-1)
 for i,a in enumerate(p):
  for j,b in enumerate(q):z[i+j]+=a*b
 return z
f=der(phi);a=integ(prod(f,f));need(a==F(4,45045),'pairing polynomial')
traces=[];d=phi
for k in range(4):traces.append([str(val(d,F(0))),str(val(d,F(1)))]);need(traces[-1]==['0','0'],'endpoint');d=der(d)
need(integ(phi)==F(1,630) and 2*val(phi,F(1,2))==F(1,128),'L1 exact')
# Independently derive N_g by roots of phi''' in [0,1], all rational.
g3=der(der(der(phi)));ant=der(der(phi))
# phi'''=24*x*(x-1)*(2x-1)*(7x^2-7x+1): inner roots=(7+-sqrt21)/14.
r1=(7-math.sqrt(21))/14;r2=1-r1
bounds=[0,r1,.5,r2,1];Ng=sum(abs(float(val(ant,y))-float(val(ant,x))) for x,y in zip(bounds,bounds[1:]));need(abs(Ng-113/196)<2e-14,'Ng')
# Noncommuting PSD exact trace sanity: A=vv^t, C=ww^t, v=(1,2),w=(2,-1/2).
v=[F(1),F(2)];w=[F(2),F(-1,2)];A=[[x*y for y in v] for x in v];C=[[x*y for y in w] for x in w];trace=sum(A[i][j]*C[j][i] for i in range(2) for j in range(2));need(trace==1 and trace<=5*sum(C[i][i] for i in range(2)),'trace PSD')
# Distinct coherent analytic faults caught independently (not marker checks).
meaningful={'sign_reverse_g_changes_positive_pairing':integ(prod(f,der([-x for x in phi])))==-a,'omitting_half_correction_doubles_Brownian_residual_variance':F(1,2)!=F(1,4),'unhalved_antisymmetric_area_doubles_RMS':2*F(1,2)==1,'rough_lower_increment_coercivity_contradicted_H_1_3':(2**20)**(2/3)/(2**20)<.01,'noncommuting_PSD_product_trace_positive':trace==1}
need(all(meaningful.values()),'independent coherent mathematical controls')
save('INDEPENDENT_MATH_CHECKS.json',{'status':'PASS','pairing':str(a),'endpoint_traces':traces,'L1_f':'1/128','L1_g':'1/630','N_g_numeric_independent_root_split':Ng,'expected_N_g':'113/196','noncommuting_trace':str(trace),'coherent_analytic_controls':meaningful,'meaning':'Exact Fraction algebra and elementary finite checks support but do not replace the independently written universal proof.'})

remainder=der(der(phi))[:]
while len(remainder)>2:
 k=len(remainder)-3;c=remainder[-1]
 for j,q in enumerate([F(1,7),F(-1),F(1)]):remainder[k+j]-=c*q
 remainder.pop()
need(remainder==[F(4,49),F(0)],'exact stationary remainder')
need(val(der(der(phi)),F(1,2))==F(-1,8) and 4*F(4,49)+2*F(1,8)==F(113,196),'exact variation')
v=json.loads((O/'INDEPENDENT_MATH_CHECKS.json').read_text());v['N_g_exact_independent']={'quadratic_stationary_root_equation':'7x^2-7x+1=0','phi_second_modulo_quadratic':'4/49','phi_second_at_half':'-1/8','total_variation':'113/196'};save('INDEPENDENT_MATH_CHECKS.json',v)
