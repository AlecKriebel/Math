"""Independent validated spectral integrals; no upstream implementation imported.
Uses adaptive Arb integration rather than the published finite Fejer quadrature.
All integrands are meromorphic, with their only possible pole at t=-2i/5;
nonfinite evaluation there fulfils acb.integral analytic-callback contract.
"""
from pathlib import Path
from math import comb
import json,hashlib,time
from flint import arb,acb,acb_mat,ctx
ctx.prec=160
data=json.loads("{\n  \"schema\": \"planar-fourier-packing-certificate-inputs-v1\",\n  \"fourier_convention\": \"fhat(xi)=integral_R2 f(x) exp(-2*pi*i*x.dot(xi)) dx\",\n  \"parameters\": {\n    \"b\": \"sqrt(3)/2\",\n    \"h\": \"2/5\",\n    \"B\": \"4/3\",\n    \"node_period\": 12,\n    \"node_residues\": [\n      0,\n      1,\n      3,\n      4,\n      7,\n      9\n    ],\n    \"finite_node_maximum\": 100,\n    \"coordinate\": \"s=b*|x|^2\"\n  },\n  \"fixed_inputs\": [\n    {\n      \"function\": 1,\n      \"c_0\": \"1\",\n      \"d_0\": \"11/25\",\n      \"C\": \"-13/1000\"\n    },\n    {\n      \"function\": 2,\n      \"c_0\": \"0\",\n      \"d_0\": \"-46/125\",\n      \"C\": \"17/1000\"\n    }\n  ],\n  \"tables\": {\n    \"coefficients\": {\n      \"scale_denominator\": 10000000000,\n      \"columns\": [\n        \"n\",\n        \"c_1_n\",\n        \"d_1_n\",\n        \"c_2_n\",\n        \"d_2_n\"\n      ],\n      \"rows\": [\n        [\n          1,\n          -670689128,\n          -6398628799,\n          -250018302,\n          4107732082\n        ],\n        [\n          3,\n          93524468,\n          564897270,\n          -186215974,\n          -65204793\n        ],\n        [\n          4,\n          -64146977,\n          121133118,\n          82882809,\n          -327822296\n        ],\n        [\n          7,\n          -1358193,\n          -16329465,\n          1979670,\n          21637038\n        ],\n        [\n          9,\n          -2932910,\n          -940875,\n          3636920,\n          2145806\n        ],\n        [\n          12,\n          3646952,\n          -34846939,\n          -6005382,\n          34369042\n        ],\n        [\n          13,\n          3183411,\n          63030995,\n          -574123,\n          -75237042\n        ],\n        [\n          15,\n          11390977,\n          27049982,\n          -11312377,\n          -34985096\n        ],\n        [\n          16,\n          -5593246,\n          13405071,\n          5915710,\n          -10980954\n        ],\n        [\n          19,\n          54905,\n          -1515007,\n          -120136,\n          1498351\n        ],\n        [\n          21,\n          -210208,\n          -634307,\n          177992,\n          747946\n        ],\n        [\n          24,\n          976077,\n          -804949,\n          -1037705,\n          105643\n        ],\n        [\n          25,\n          -824472,\n          7003719,\n          1011732,\n          -6510015\n        ],\n        [\n          27,\n          611891,\n          4536095,\n          -428528,\n          -4440927\n        ],\n        [\n          28,\n          -472882,\n          -107613,\n          399655,\n          403751\n        ],\n        [\n          31,\n          30744,\n          -112653,\n          -31773,\n          90515\n        ],\n        [\n          33,\n          -4974,\n          -105568,\n          1240,\n          99081\n        ],\n        [\n          36,\n          128313,\n          246018,\n          -114876,\n          -267388\n        ],\n        [\n          37,\n          -176685,\n          505187,\n          166591,\n          -396209\n        ],\n        [\n          39,\n          -21638,\n          472037,\n          32128,\n          -402283\n        ],\n        [\n          40,\n          -18461,\n          -165597,\n          10836,\n          164974\n        ],\n        [\n          43,\n          4565,\n          -2296,\n          -4050,\n          547\n        ],\n        [\n          45,\n          1477,\n          -10734,\n          -1524,\n          8978\n        ],\n        [\n          48,\n          10748,\n          50050,\n          -8611,\n          -45048\n        ],\n        [\n          49,\n          -20506,\n          7495,\n          17354,\n          -266\n        ],\n        [\n          51,\n          -10361,\n          29035,\n          9641,\n          -21534\n        ],\n        [\n          52,\n          2121,\n          -26523,\n          -2269,\n          23159\n        ],\n        [\n          55,\n          425,\n          858,\n          -344,\n          -839\n        ],\n        [\n          57,\n          302,\n          -632,\n          -266,\n          463\n        ],\n        [\n          60,\n          382,\n          5658,\n          -231,\n          -4688\n        ],\n        [\n          61,\n          -1481,\n          -4320,\n          1140,\n          4098\n        ],\n        [\n          63,\n          -1494,\n          -352,\n          1265,\n          647\n        ],\n        [\n          64,\n          558,\n          -2609,\n          -491,\n          2114\n        ],\n        [\n          67,\n          21,\n          169,\n          -14,\n          -145\n        ],\n        [\n          69,\n          34,\n          13,\n          -28,\n          -18\n        ],\n        [\n          72,\n          -55,\n          394,\n          53,\n          -301\n        ],\n        [\n          73,\n          -21,\n          -805,\n          5,\n          685\n        ],\n        [\n          75,\n          -136,\n          -379,\n          108,\n          338\n        ],\n        [\n          76,\n          70,\n          -144,\n          -58,\n          104\n        ],\n        [\n          79,\n          -1,\n          19,\n          1,\n          -15\n        ],\n        [\n          81,\n          2,\n          9,\n          -2,\n          -8\n        ],\n        [\n          84,\n          -13,\n          3,\n          11,\n          0\n        ],\n        [\n          85,\n          13,\n          -87,\n          -11,\n          70\n        ],\n        [\n          87,\n          -6,\n          -60,\n          4,\n          49\n        ],\n        [\n          88,\n          6,\n          5,\n          -4,\n          -5\n        ],\n        [\n          91,\n          0,\n          1,\n          0,\n          -1\n        ],\n        [\n          93,\n          0,\n          1,\n          0,\n          -1\n        ],\n        [\n          96,\n          -2,\n          -4,\n          1,\n          3\n        ],\n        [\n          97,\n          2,\n          -6,\n          -2,\n          4\n        ],\n        [\n          99,\n          0,\n          -6,\n          0,\n          5\n        ],\n        [\n          100,\n          0,\n          2,\n          0,\n          -2\n        ]\n      ]\n    },\n    \"W_plus\": {\n      \"scale_denominator\": 10000,\n      \"coordinate_order\": [\n        \"c_1\",\n        \"c_3\",\n        \"c_4\",\n        \"d_1\",\n        \"d_3\",\n        \"d_4\"\n      ],\n      \"rows\": [\n        [\n          4159,\n          4452,\n          -2003,\n          -10467,\n          -2421,\n          -1683\n        ],\n        [\n          2714,\n          6573,\n          1689,\n          8258,\n          104,\n          -335\n        ],\n        [\n          -4675,\n          4785,\n          7003,\n          -13100,\n          -1355,\n          -1163\n        ],\n        [\n          36853,\n          -37142,\n          27514,\n          105973,\n          1100,\n          2012\n        ],\n        [\n          57838,\n          -56941,\n          36296,\n          158623,\n          29097,\n          17293\n        ],\n        [\n          -4705,\n          3589,\n          -3311,\n          -11932,\n          -2562,\n          6919\n        ]\n      ]\n    },\n    \"W_minus\": {\n      \"scale_denominator\": 10000,\n      \"coordinate_order\": [\n        \"c_1\",\n        \"c_3\",\n        \"c_4\",\n        \"d_1\",\n        \"d_3\",\n        \"d_4\"\n      ],\n      \"rows\": [\n        [\n          13265,\n          -1358,\n          -385,\n          -381,\n          815,\n          -164\n        ],\n        [\n          616,\n          10426,\n          686,\n          -484,\n          182,\n          775\n        ],\n        [\n          -146,\n          4,\n          9842,\n          215,\n          267,\n          179\n        ],\n        [\n          -2761,\n          2483,\n          -958,\n          5174,\n          -328,\n          206\n        ],\n        [\n          -615,\n          -861,\n          730,\n          -1388,\n          5619,\n          -4370\n        ],\n        [\n          874,\n          820,\n          1148,\n          -431,\n          905,\n          11927\n        ]\n      ]\n    }\n  },\n  \"files_sha256\": {\n    \"W_minus.tex\": \"0b8e7055844b8dc23d27e54e0526a1a62b8b69f4386f1518638c1f62cfa3c77d\",\n    \"W_minus.tsv\": \"ccab423b5a6575b4c539da031f575d9504bc14770373948b09f9c342c83e6141\",\n    \"W_plus.tex\": \"b73b2488a0884682d17a00a28467bc58a2f07fcee905997c844ce9662d8b59d5\",\n    \"W_plus.tsv\": \"c8588c3c6c8bd0278980bda25dbfd1018683e3df5bf38c8fc3c5b5dc1c2d9398\",\n    \"coefficients.tex\": \"2dc6a2a19f0abdb0e0ca3f57261d44938a7c9f1ae8697dc816d7911875038577\",\n    \"coefficients.tsv\": \"b62c6b3ea62ab8d7906214f009b23b232c16602cb6ae0487ae8fa362c0ad4ced\"\n  }\n}\n")
pi=arb.pi(); b=arb(3).sqrt()/2; h=arb(2)/5; B=arb(4)/3; I=acb(0,1)
P=[acb(5),-1+2*I*b,1+2*I*b,acb(-2),-arb(1)/2+I*b,-1-2*I*b,acb(1)]
ts=[arb(j)/6 for j in range(7)]; A=[0,1,3,4,7,9]; J=[1,3,4]
Q={};D={}
for n in A:
 Q[n]=(pi/6)**2;D[n]=arb(0)
 for a in A:
  if a!=n:
   v=pi*(n-a)/12;Q[n]*=(2*v.sin())**2;D[n]+=(pi/6)*v.cos()/v.sin()
def exp(z):return (I*pi*z).exp()
def transform_params(t):
 lam=I/(b*(t+I*h));z=-B/(t+I*h)-I*h
 return lam,z
def tails(n,j):
 terms=[P[l]*exp(ts[l]*n) for l in range(j,7)]
 return sum(terms),sum(ts[l]*terms[l-j] for l in range(j,7))
tail_cache={(n,j):tails(n,j) for n in [0]+[r[0] for r in data['tables']['coefficients']['rows']] for j in range(1,7)}
def density(t,n,kind,j):
 aa,bb=tail_cache[n,j]
 return exp(-n*t)*(-2*pi*pi*(bb-t*aa) if kind==0 else 2*I*pi*aa)
def integrate(callback,j):
 value=acb.integral(callback,ts[j-1],ts[j],abs_tol=arb('1e-27'),rel_tol=arb('1e-27'),deg_limit=120,eval_limit=100000,depth_limit=40)
 assert value.is_finite(), (j,'nonfinite integral')
 return value
start=time.monotonic()
dmat=[]
for kindout in range(2):
 for m in J:
  row=[]
  for kindin in range(2):
   for n in J:
    total=acb(0)
    for j in range(1,7):
     def callback(t,analytic):
      lam,z=transform_params(t); factor=(-1 if kindout==0 else D[m]-I*pi*z)/Q[m]
      return density(t,n,kindin,j)*lam*exp(z*m)*factor
     total+=integrate(callback,j)
    row.append(total.real)
  dmat.append(row)
 print('completed independent matrix row',kindout,m,flush=True)
mat=acb_mat(dmat); ident=acb_mat([[int(i==j) for j in range(6)] for i in range(6)])
def norm1(mat):
 vals=[sum(abs(mat[i,j]) for i in range(mat.nrows())) for j in range(mat.ncols())]
 return max(vals,key=lambda x:float(x.mid()))
results={}
for eta,key in [(1,'W_plus'),(-1,'W_minus')]:
 W=acb_mat([[arb(v)/10000 for v in row] for row in data['tables'][key]['rows']])
 defect=norm1(ident-W*(ident-eta*mat))
 assert defect<arb('.001')
 results[str(eta)]={'defect':str(defect),'norm_W':str(norm1(W))}
print('independent matrix certificates pass',flush=True)
tab=[]
for i in range(2):
 pairs={r[0]:(arb(r[1+2*i])/10**10,arb(r[2+2*i])/10**10) for r in data['tables']['coefficients']['rows']}
 pairs[0]=((arb(1),arb(44)/100) if i==0 else (arb(0),-arb(368)/1000))
 tab.append(pairs)
C=[-arb(13)/1000,arb(17)/1000]
def table_density(t,index,j):
 return sum(c*density(t,n,0,j)+d*density(t,n,1,j) for n,(c,d) in tab[index].items())
def bern_factor(t):
 v=I*pi*t
 out=acb(0); term=v*v/2
 for r in range(29):
  out+=arb(comb(28,r))/comb(28,r)*(arb(-1)/2)**r*term
  term*=v/(r+3)
 return out
bern=acb(0)
for j in range(1,7):
 def callback(t,analytic):
  lam,z=transform_params(t)
  return table_density(t,1,j)*exp(t*16)*bern_factor(t)+table_density(t,0,j)*lam*exp(z*16)*bern_factor(z)
 bern+=integrate(callback,j)
for j,t in enumerate(ts):
 scale=1 if j==0 else 2
 lam,z=transform_params(acb(t))
 bern+=scale*P[j]*(C[1]*exp(t*16)*bern_factor(t)+C[0]*lam*exp(z*16)*bern_factor(z))
bern=bern.real
assert bern>arb('.0094') and bern<arb('.009518759557')
print('independent Bernstein extreme enclosure',bern,flush=True)
F=[]
for index in (0,1):
 total=acb(0)
 for j in range(1,7):
  def callback(t,analytic):
   lam,z=transform_params(t)
   return table_density(t,1-index,j)*lam
  total+=integrate(callback,j)
 for j,t in enumerate(ts):
  lam,z=transform_params(acb(t))
  total+=(1 if j==0 else 2)*C[1-index]*P[j]*lam
 direct=Q[0] if index==0 else arb(0)
 F.append((total.real+direct))
expected=6*Q[1]*(-pi*h).exp()
out={'status':'pass','precision_bits':ctx.prec,'method':'independent adaptive Arb integrals','matrix_enclosures':[[str(v) for v in row] for row in dmat],'W_checks':results,'Bernstein_2_16_left_k28':str(bern),'tabulated_origins':[str(v) for v in F],'expected_exact_origin':str(expected),'elapsed_seconds':time.monotonic()-start,'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
dest=Path(__file__).with_name('independent_validated_integrals_receipt.json')
dest.write_text(json.dumps(out,indent=2)+'\\n')
print(json.dumps(out,indent=2))

# Complete independent reproduction of every finite mathematical gate.
def real_norm1(matrix):
 vals=[sum(abs(matrix[i,j]) for i in range(matrix.nrows())) for j in range(matrix.ncols())]
 value=vals[0]
 for v in vals[1:]:value=value.max(v)
 return value
nodes=[r[0] for r in data['tables']['coefficients']['rows']]
E=[n for n in nodes if n not in J]
Srows=[]
for kindout in range(2):
 for m in J:
  row=[]
  for kindin in range(2):
   for n in E:
    total=acb(0)
    for j in range(1,7):
     def callback(t,analytic):
      lam,z=transform_params(t)
      factor=(-1 if kindout==0 else D[m%12]-I*pi*z)/Q[m%12]
      return density(t,n,kindin,j)*lam*exp(z*m)*factor
     total+=integrate(callback,j)
    row.append(total.real)
  Srows.append(row)
U=acb_mat(Srows)
cross=[]
for eta,key in [(1,'W_plus'),(-1,'W_minus')]:
 W=acb_mat([[arb(v)/10000 for v in row] for row in data['tables'][key]['rows']])
 defect=real_norm1(ident-W*(ident-eta*mat))
 wu=real_norm1(W*U)
 assert defect<arb('.001') and wu<arb('3.54')
 cross.append({'eta':eta,'defect':str(defect),'WU':str(wu),'inverse_upper':str(real_norm1(W)/(1-defect)),'cross_upper':str(wu/(1-defect))})
 assert real_norm1(W)/(1-defect)<32
 assert wu/(1-defect)<arb('3.7')
low=[]
for kindout in range(2):
 for m in [n for n in E if n<=16]:
  row=[]
  for kindin in range(2):
   for n in J:
    total=acb(0)
    for j in range(1,7):
     def callback(t,analytic):
      lam,z=transform_params(t)
      factor=(-1 if kindout==0 else D[m%12]-I*pi*z)/Q[m%12]
      return density(t,n,kindin,j)*lam*exp(z*m)*factor
     total+=integrate(callback,j)
    row.append(total.real)
  low.append(row)
low_norm=real_norm1(acb_mat(low))
assert low_norm<arb('.09')
print('full independent matrix and cross gates pass',flush=True)
residuals=[]
for i in range(2):
 for m in nodes:
  values=[]
  for derivative in range(2):
   total=acb(0)
   for j in range(1,7):
    def callback(t,analytic):
     lam,z=transform_params(t)
     return table_density(t,1-i,j)*lam*exp(z*m)*(I*pi*z)**derivative
    total+=integrate(callback,j)
   for j,t in enumerate(ts):
    lam,z=transform_params(acb(t))
    total+=(1 if j==0 else 2)*C[1-i]*P[j]*lam*exp(z*m)*(I*pi*z)**derivative
   values.append(total.real)
  c,d=tab[i][m]
  rc=abs(c+values[0]/Q[m%12])
  rd=abs(d+int(i==0 and m==1)+(values[1]-D[m%12]*values[0])/Q[m%12])
  assert rc<arb('1e-9') and rd<arb('1e-9')
  residuals.append({'i':i+1,'m':m,'c':str(rc),'d':str(rd)})
 print('full independent residual list passes',i+1,flush=True)
def quotient_factor(v,y,nu,k):
 term=(I*pi*v)**nu
 from math import factorial
 term/=factorial(nu)
 value=acb(0)
 for r in range(k+1):
  value+=arb(comb(k,r))/comb(28,r)*y**r*term
  term*=I*pi*v/(r+nu+1)
 return value
certificates=[]
centers=[0]+[n for n in nodes if n<=40]
whole=[0]+nodes
for m in centers:
 index=whole.index(m)
 ylist=[arb(whole[index+1]-m)/2]
 if index:ylist.append(arb(whole[index-1]-m)/2)
 for y in ylist:
  for i in range(2):
   if i==0 and (m==0 or (m==1 and y<0)):continue
   nu=0 if m==0 else (1 if i==0 and m==1 else 2)
   sig=-1 if i==0 else 1
   threshold=arb('.74' if m==0 else '.18' if m==1 else '.02' if m in (3,4) else '.009')
   minimum=None
   for k in range(29):
    total=acb(0)
    for j in range(1,7):
     def callback(t,analytic):
      lam,z=transform_params(t)
      return table_density(t,i,j)*exp(t*m)*quotient_factor(t,y,nu,k)+table_density(t,1-i,j)*lam*exp(z*m)*quotient_factor(z,y,nu,k)
     total+=integrate(callback,j)
    for j,t in enumerate(ts):
     lam,z=transform_params(acb(t)); scale=1 if j==0 else 2
     total+=scale*P[j]*(C[i]*exp(t*m)*quotient_factor(t,y,nu,k)+C[1-i]*lam*exp(z*m)*quotient_factor(z,y,nu,k))
    v=sig*total.real
    assert v>threshold,(i+1,m,str(y),k,str(v))
    minimum=v if minimum is None else -(-minimum).max(-v)
   certificates.append({'i':i+1,'m':m,'y':str(y),'minimum':str(minimum),'threshold':str(threshold)})
 print('independent Bernstein center complete',m,flush=True)
assert len(certificates)==84 and len(residuals)==102
out.update({'full_finite_gates':'pass','cross_certificates':cross,'low_exterior_norm':str(low_norm),'residuals':residuals,'Bernstein_intervals':certificates,'coverage':{'finite_nodes':51,'matrix_signs':2,'residual_pairs':102,'half_gap_intervals':84,'Bernstein_inequalities':2436},'elapsed_seconds':time.monotonic()-start,'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()})
dest.write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'status':'pass','full_finite_gates':'pass','coverage':out['coverage'],'elapsed_seconds':out['elapsed_seconds'],'script_sha256':out['script_sha256']},indent=2))
