"""Independent scalar gates for the family 090 analytic proof.
Endpoint extension, Cauchy bounds, row geometry and log-concavity are proved in
CERTIFICATE_AUDIT.md; these scalar gates themselves are not a continuum proof.
"""
from pathlib import Path
from math import factorial
import json,hashlib,datetime
from flint import arb,acb,ctx
if not __debug__:raise RuntimeError('Assertions must be enabled')
ctx.prec=192
data=json.loads("{\n  \"schema\": \"planar-fourier-packing-certificate-inputs-v1\",\n  \"fourier_convention\": \"fhat(xi)=integral_R2 f(x) exp(-2*pi*i*x.dot(xi)) dx\",\n  \"parameters\": {\n    \"b\": \"sqrt(3)/2\",\n    \"h\": \"2/5\",\n    \"B\": \"4/3\",\n    \"node_period\": 12,\n    \"node_residues\": [\n      0,\n      1,\n      3,\n      4,\n      7,\n      9\n    ],\n    \"finite_node_maximum\": 100,\n    \"coordinate\": \"s=b*|x|^2\"\n  },\n  \"fixed_inputs\": [\n    {\n      \"function\": 1,\n      \"c_0\": \"1\",\n      \"d_0\": \"11/25\",\n      \"C\": \"-13/1000\"\n    },\n    {\n      \"function\": 2,\n      \"c_0\": \"0\",\n      \"d_0\": \"-46/125\",\n      \"C\": \"17/1000\"\n    }\n  ],\n  \"tables\": {\n    \"coefficients\": {\n      \"scale_denominator\": 10000000000,\n      \"columns\": [\n        \"n\",\n        \"c_1_n\",\n        \"d_1_n\",\n        \"c_2_n\",\n        \"d_2_n\"\n      ],\n      \"rows\": [\n        [\n          1,\n          -670689128,\n          -6398628799,\n          -250018302,\n          4107732082\n        ],\n        [\n          3,\n          93524468,\n          564897270,\n          -186215974,\n          -65204793\n        ],\n        [\n          4,\n          -64146977,\n          121133118,\n          82882809,\n          -327822296\n        ],\n        [\n          7,\n          -1358193,\n          -16329465,\n          1979670,\n          21637038\n        ],\n        [\n          9,\n          -2932910,\n          -940875,\n          3636920,\n          2145806\n        ],\n        [\n          12,\n          3646952,\n          -34846939,\n          -6005382,\n          34369042\n        ],\n        [\n          13,\n          3183411,\n          63030995,\n          -574123,\n          -75237042\n        ],\n        [\n          15,\n          11390977,\n          27049982,\n          -11312377,\n          -34985096\n        ],\n        [\n          16,\n          -5593246,\n          13405071,\n          5915710,\n          -10980954\n        ],\n        [\n          19,\n          54905,\n          -1515007,\n          -120136,\n          1498351\n        ],\n        [\n          21,\n          -210208,\n          -634307,\n          177992,\n          747946\n        ],\n        [\n          24,\n          976077,\n          -804949,\n          -1037705,\n          105643\n        ],\n        [\n          25,\n          -824472,\n          7003719,\n          1011732,\n          -6510015\n        ],\n        [\n          27,\n          611891,\n          4536095,\n          -428528,\n          -4440927\n        ],\n        [\n          28,\n          -472882,\n          -107613,\n          399655,\n          403751\n        ],\n        [\n          31,\n          30744,\n          -112653,\n          -31773,\n          90515\n        ],\n        [\n          33,\n          -4974,\n          -105568,\n          1240,\n          99081\n        ],\n        [\n          36,\n          128313,\n          246018,\n          -114876,\n          -267388\n        ],\n        [\n          37,\n          -176685,\n          505187,\n          166591,\n          -396209\n        ],\n        [\n          39,\n          -21638,\n          472037,\n          32128,\n          -402283\n        ],\n        [\n          40,\n          -18461,\n          -165597,\n          10836,\n          164974\n        ],\n        [\n          43,\n          4565,\n          -2296,\n          -4050,\n          547\n        ],\n        [\n          45,\n          1477,\n          -10734,\n          -1524,\n          8978\n        ],\n        [\n          48,\n          10748,\n          50050,\n          -8611,\n          -45048\n        ],\n        [\n          49,\n          -20506,\n          7495,\n          17354,\n          -266\n        ],\n        [\n          51,\n          -10361,\n          29035,\n          9641,\n          -21534\n        ],\n        [\n          52,\n          2121,\n          -26523,\n          -2269,\n          23159\n        ],\n        [\n          55,\n          425,\n          858,\n          -344,\n          -839\n        ],\n        [\n          57,\n          302,\n          -632,\n          -266,\n          463\n        ],\n        [\n          60,\n          382,\n          5658,\n          -231,\n          -4688\n        ],\n        [\n          61,\n          -1481,\n          -4320,\n          1140,\n          4098\n        ],\n        [\n          63,\n          -1494,\n          -352,\n          1265,\n          647\n        ],\n        [\n          64,\n          558,\n          -2609,\n          -491,\n          2114\n        ],\n        [\n          67,\n          21,\n          169,\n          -14,\n          -145\n        ],\n        [\n          69,\n          34,\n          13,\n          -28,\n          -18\n        ],\n        [\n          72,\n          -55,\n          394,\n          53,\n          -301\n        ],\n        [\n          73,\n          -21,\n          -805,\n          5,\n          685\n        ],\n        [\n          75,\n          -136,\n          -379,\n          108,\n          338\n        ],\n        [\n          76,\n          70,\n          -144,\n          -58,\n          104\n        ],\n        [\n          79,\n          -1,\n          19,\n          1,\n          -15\n        ],\n        [\n          81,\n          2,\n          9,\n          -2,\n          -8\n        ],\n        [\n          84,\n          -13,\n          3,\n          11,\n          0\n        ],\n        [\n          85,\n          13,\n          -87,\n          -11,\n          70\n        ],\n        [\n          87,\n          -6,\n          -60,\n          4,\n          49\n        ],\n        [\n          88,\n          6,\n          5,\n          -4,\n          -5\n        ],\n        [\n          91,\n          0,\n          1,\n          0,\n          -1\n        ],\n        [\n          93,\n          0,\n          1,\n          0,\n          -1\n        ],\n        [\n          96,\n          -2,\n          -4,\n          1,\n          3\n        ],\n        [\n          97,\n          2,\n          -6,\n          -2,\n          4\n        ],\n        [\n          99,\n          0,\n          -6,\n          0,\n          5\n        ],\n        [\n          100,\n          0,\n          2,\n          0,\n          -2\n        ]\n      ]\n    },\n    \"W_plus\": {\n      \"scale_denominator\": 10000,\n      \"coordinate_order\": [\n        \"c_1\",\n        \"c_3\",\n        \"c_4\",\n        \"d_1\",\n        \"d_3\",\n        \"d_4\"\n      ],\n      \"rows\": [\n        [\n          4159,\n          4452,\n          -2003,\n          -10467,\n          -2421,\n          -1683\n        ],\n        [\n          2714,\n          6573,\n          1689,\n          8258,\n          104,\n          -335\n        ],\n        [\n          -4675,\n          4785,\n          7003,\n          -13100,\n          -1355,\n          -1163\n        ],\n        [\n          36853,\n          -37142,\n          27514,\n          105973,\n          1100,\n          2012\n        ],\n        [\n          57838,\n          -56941,\n          36296,\n          158623,\n          29097,\n          17293\n        ],\n        [\n          -4705,\n          3589,\n          -3311,\n          -11932,\n          -2562,\n          6919\n        ]\n      ]\n    },\n    \"W_minus\": {\n      \"scale_denominator\": 10000,\n      \"coordinate_order\": [\n        \"c_1\",\n        \"c_3\",\n        \"c_4\",\n        \"d_1\",\n        \"d_3\",\n        \"d_4\"\n      ],\n      \"rows\": [\n        [\n          13265,\n          -1358,\n          -385,\n          -381,\n          815,\n          -164\n        ],\n        [\n          616,\n          10426,\n          686,\n          -484,\n          182,\n          775\n        ],\n        [\n          -146,\n          4,\n          9842,\n          215,\n          267,\n          179\n        ],\n        [\n          -2761,\n          2483,\n          -958,\n          5174,\n          -328,\n          206\n        ],\n        [\n          -615,\n          -861,\n          730,\n          -1388,\n          5619,\n          -4370\n        ],\n        [\n          874,\n          820,\n          1148,\n          -431,\n          905,\n          11927\n        ]\n      ]\n    }\n  },\n  \"files_sha256\": {\n    \"W_minus.tex\": \"0b8e7055844b8dc23d27e54e0526a1a62b8b69f4386f1518638c1f62cfa3c77d\",\n    \"W_minus.tsv\": \"ccab423b5a6575b4c539da031f575d9504bc14770373948b09f9c342c83e6141\",\n    \"W_plus.tex\": \"b73b2488a0884682d17a00a28467bc58a2f07fcee905997c844ce9662d8b59d5\",\n    \"W_plus.tsv\": \"c8588c3c6c8bd0278980bda25dbfd1018683e3df5bf38c8fc3c5b5dc1c2d9398\",\n    \"coefficients.tex\": \"2dc6a2a19f0abdb0e0ca3f57261d44938a7c9f1ae8697dc816d7911875038577\",\n    \"coefficients.tsv\": \"b62c6b3ea62ab8d7906214f009b23b232c16602cb6ae0487ae8fa362c0ad4ced\"\n  }\n}\n")
pi=arb.pi();b=arb(3).sqrt()/2;h=arb(2)/5;B=arb(4)/3;I=acb(0,1)
A=[0,1,3,4,7,9];ts=[arb(j)/6 for j in range(7)]
P=[acb(5),-1+2*I*b,1+2*I*b,acb(-2),-arb(1)/2+I*b,-1-2*I*b,acb(1)]
Q={};D={}
for a in A:
 Q[a]=(pi/6)**2;D[a]=arb(0)
 for aa in A:
  if a!=aa:
   v=pi*(a-aa)/12;Q[a]*=(2*v.sin())**2;D[a]+=pi/6*v.cos()/v.sin()
 assert Q[a]>arb('1.75') and abs(D[a])<arb('2.12')
bs=list(map(arb,['2.887','2.665','2.218','1.804','1.486','1.250','1.073']))
zs=list(map(arb,['2.934','2.713','2.269','1.859','1.548','1.320','1.151']))
gs=list(map(arb,['2.933','2.440','1.567','.900','.482','.224','.0597']))
Ms=list(map(arb,['56','48','35','25','19','6.284']))
betas=list(map(arb,['0','4.8','3.17','1.946','1.217','.792']))
masses=list(map(arb,['5','4','4','4','2','4','2']))
def maximum(values):
 out=values[0]
 for v in values[1:]:out=out.max(v)
 return out
for j,t in enumerate(ts):
 assert 1/(b*(t*t+h*h).sqrt())<bs[j]
 assert (h*h+(B*B-2*B*h*h)/(t*t+h*h)).sqrt()<zs[j]
 assert h*(B/(t*t+h*h)-1)>gs[j]
for j in range(1,7):
 for t in (ts[j-1],ts[j]):
  assert 2*h*B*t/(t*t+h*h)**2>=betas[j-1]
 for n in A:
  phases=[P[l]*(I*pi*ts[l]*n).exp() for l in range(j,7)]
  assert 2*pi*abs(sum(phases))<Ms[j-1]
  for t in (ts[j-1],ts[j]):
   assert 2*pi*pi*abs(sum((ts[l]-t)*phases[l-j] for l in range(j,7)))<Ms[j-1]
def L(s,j):
 s=arb(s); factor=arb(1)/6
 if s>0 and betas[j-1]>0:factor=factor.min(1/(pi*betas[j-1]*s))
 return bs[j-1]*(-pi*gs[j]*s).exp()*factor
def LP(s,j):return masses[j]*bs[j]*(-pi*gs[j]*arb(s)).exp()
rowbounds={}
for cut,threshold in [(0,'28'),(4,'.28'),(16,'.015'),(100,'5e-10')]:
 total=arb(0)
 for n in range(cut+1,cut+13):
  if n%12 in A:
   for j in range(1,7):
    total+=(1+abs(D[n%12])+pi*zs[j-1])/Q[n%12]*Ms[j-1]*L(n,j)/(1-(-12*pi*gs[j]).exp())
 assert total<arb(threshold);rowbounds[str(cut)]=str(total)
at=arb(0)
for n in range(101,113):
 if n%12 in A:
  for j in range(7):at+=(1+abs(D[n%12])+pi*zs[j])/Q[n%12]*LP(n,j)/(1-(-12*pi*gs[j]).exp())
assert at<arb('3.2e-8')
full=[];tail=[];lower=[]
rows=data['tables']['coefficients']['rows']
for i in range(2):
 entries={r[0]:(arb(r[1+2*i])/10**10,arb(r[2+2*i])/10**10) for r in rows}
 entries[0]=((arb(1),arb(44)/100) if i==0 else (arb(0),-arb(368)/1000))
 full.append(sum(abs(c)+abs(d) for c,d in entries.values()))
 tail.append(sum(abs(c)+abs(d) for n,(c,d) in entries.items() if n>40))
 assert full[-1]<arb('2.29') and tail[-1]<arb('.00002')
 sig=-1 if i==0 else 1; cc=-arb(13)/1000 if i==0 else arb(17)/1000;s0=arb(83)/2
 pairs={n:(sig*c,sig*d) for n,(c,d) in entries.items() if n<=40}
 lo=sig*cc+sum(d for c,d in pairs.values()).min(0)/s0
 for n,(c,d) in pairs.items():lo+=c.min(0)/(s0-n)**2+d.min(0)*n/(s0*(s0-n))
 assert lo>arb('.012' if i==0 else '.016')
 assert lo-arb('.00003')/arb('1.5')>arb('.011')
 lower.append(str(lo))
error=2*(91*arb('1.1e-7')+2540*(arb('2.29')*arb('5e-10')+arb('.017')*arb('3.2e-8')))
assert error<arb('.00003')
finite=max(arb(32)+(1+arb('3.7'))*arb('.11')*32/(1-arb('.687')),(1+arb('3.7'))/(1-arb('.687')))
assert finite<90
second=arb('.00005')*77+arb('2.3')*sum(Ms[j-1]*L(arb('41.5'),j)*(pi*zs[j-1])**2 for j in range(1,7))+arb('.017')*sum(LP(arb('41.5'),j)*(pi*zs[j])**2 for j in range(7))
assert second<arb('.006')
perturb=[]
for s,nu,bound in [(0,0,'.004'),(arb('.5'),1,'.011'),(arb('.5'),2,'.011'),(2,2,'.002')]:
 value=arb('.00003')/factorial(nu)*sum(Ms[j-1]*((pi*ts[j])**nu/6+L(s,j)*(pi*zs[j-1])**nu) for j in range(1,7))
 assert value<arb(bound);perturb.append(str(value))
trunc=[]
for m,Y,nu in [(0,arb(1)/2,0),(1,arb(1),1),(1,arb(1),2),(3,arb(1),2),(4,arb(3)/2,2)]:
 q=29+nu;ratio=pi*zs[0]*Y/(q+1);assert ratio<1
 value=Y**(-nu)/factorial(q)/(1-ratio)*(80*(pi*Y)**q+arb('2.3')*sum(Ms[j-1]*L(m,j)*(pi*zs[j-1]*Y)**q for j in range(1,7))+arb('.017')*sum(LP(m,j)*(pi*zs[j]*Y)**q for j in range(7)))
 assert value<arb('.001');trunc.append(str(value))
midpoints=[]
for aa,bb in zip(A,A[1:]+[12]):
 s=arb(aa+bb)/2
 p=arb(1)
 for n in A:p*=(2*(pi*(s-n)/12).sin())**2
 v=p/(arb(bb-aa)/2)**2;assert v>arb('.68');midpoints.append(str(v))
rho=arb(1)/6;dmax=(arb(11)/12)**2+h*h-rho*rho
imlow=B*(h-rho)/dmax-h
assert imlow>-arb('.081')
direct=1000*(200*pi/6+arb('1.5')*pi*arb('1.1')).exp()
transformed=5000*(100*pi/6+100*pi*arb('.081')+arb('1.5')*pi*arb('6.2')).exp()
assert direct<arb('1e53') and transformed<arb('1e53')
quad=arb('1e53')*arb(2)**(-254);assert quad<arb('1e-22')
out={'status':'pass','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'precision_bits':ctx.prec,'row_tail_envelopes':rowbounds,'atom_tail':str(at),'coefficient_norms':[str(v) for v in full],'coefficient_tail_norms':[str(v) for v in tail],'rational_part_lower_bounds':lower,'exact_list_error':str(error),'finite_inverse_bound':str(finite),'tail_second_derivative_bound':str(second),'quotient_perturbation_bounds':perturb,'Taylor_remainder_bounds':trunc,'midpoint_barriers':midpoints,'quadrature_error_bound':str(quad),'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
Path(__file__).with_name('independent_scalar_receipt.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
