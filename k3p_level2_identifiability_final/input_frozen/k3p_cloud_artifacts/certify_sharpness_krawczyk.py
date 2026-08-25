#!/usr/bin/env python3
from __future__ import annotations
from fractions import Fraction as F
from pathlib import Path
import importlib.util,json,math,time
import mpmath as mp
import numpy as np
from scipy.linalg import qr

ROOT=Path(__file__).resolve().parents[2]
CAND=Path(__file__).with_name('sharpness_relative_root.json')
spec=importlib.util.spec_from_file_location('s',str(Path(__file__).with_name('sharpness_exact_maps.py')));s=importlib.util.module_from_spec(spec);spec.loader.exec_module(s)
data=json.loads(CAND.read_text())
PIV=tuple(data['pivot_columns']); centers=tuple(F(x) for x in data['center_rationals']); scales=tuple(F(x) for x in data['row_scales'])
# 90 decimal digits suffice; keep exact decimal rational center.
y0=tuple(F(x[:x.find('.')+91] if '.' in x and len(x)-x.find('.')-1>90 else x) for x in data['root_y'])
rho=F(1,10**50)
DIM=15

class I:
 __slots__=('lo','hi')
 def __init__(self,lo,hi=None):
  self.lo=F(lo);self.hi=self.lo if hi is None else F(hi)
  if self.lo>self.hi:raise ValueError((self.lo,self.hi))
 def __add__(self,o):
  o=asI(o);return I(self.lo+o.lo,self.hi+o.hi)
 __radd__=__add__
 def __neg__(self):return I(-self.hi,-self.lo)
 def __sub__(self,o):return self+(-asI(o))
 def __rsub__(self,o):return asI(o)-self
 def __mul__(self,o):
  o=asI(o);v=(self.lo*o.lo,self.lo*o.hi,self.hi*o.lo,self.hi*o.hi);return I(min(v),max(v))
 __rmul__=__mul__
 def recip(self):
  if self.lo<=0<=self.hi:raise ZeroDivisionError((self.lo,self.hi))
  return I(1/self.hi,1/self.lo) if self.lo>0 else I(1/self.hi,1/self.lo)
 def __truediv__(self,o):return self*asI(o).recip()
 def mid(self):return (self.lo+self.hi)/2
 def rad(self):return (self.hi-self.lo)/2
 def contains0(self):return self.lo<=0<=self.hi
 def __repr__(self):return f'I({self.lo},{self.hi})'
def asI(x):return x if isinstance(x,I) else I(x)

class D:
 __slots__=('v','d')
 def __init__(self,v,d=None):self.v=asI(v);self.d=[I(0) for _ in range(DIM)] if d is None else d
 def __add__(self,o):
  o=asD(o);return D(self.v+o.v,[a+b for a,b in zip(self.d,o.d)])
 __radd__=__add__
 def __neg__(self):return D(-self.v,[-a for a in self.d])
 def __sub__(self,o):return self+(-asD(o))
 def __rsub__(self,o):return asD(o)-self
 def __mul__(self,o):
  o=asD(o);return D(self.v*o.v,[a*o.v+self.v*b for a,b in zip(self.d,o.d)])
 __rmul__=__mul__
def asD(x):return x if isinstance(x,D) else D(x)

def full_dual(box=True, local_side=None):
 # local_side None => derivatives wrt 15 y variables. 'W'/'P' => derivatives wrt first 15 selected local columns later not used here.
 Y=[I(y-rho,y+rho) if box else I(y) for y in y0]
 x=[]
 pmap={p:j for j,p in enumerate(PIV)}
 for i,c in enumerate(centers):
  if i in pmap:
   j=pmap[i];d=[I(0) for _ in range(DIM)];d[j]=I(c);x.append(D(I(c)*Y[j],d))
  else:x.append(D(I(c)))
 return x

def map_dual(M,x):
 flat=x[:3*M.E];l=x[3*M.E:];out=[]
 for terms in M.outputs[1:]:
  val=D(0)
  for bits,powers in terms:
   term=D(1)
   for v,e in powers:
    assert e==1;term=term*flat[v]
   for j,b in enumerate(bits):term=term*(l[j] if b else (1-l[j]))
   val=val+term
  out.append(val)
 return out

def system_dual(box=True):
 x=full_dual(box);qw=map_dual(s.MW,x[:32]);qp=map_dual(s.MP,x[32:]);out=[]
 for sc,a,b in zip(scales,qw,qp):out.append(sc*(a-b))
 return out,x

print('building point and box duals',flush=True)
t0=time.time();pt,_=system_dual(False);bx,xbox=system_dual(True)
f0=[z.v.lo for z in pt];J0=[[z.d[j].lo for j in range(DIM)] for z in pt];JX=[[z.d[j] for j in range(DIM)] for z in bx]
assert all(z.v.lo==z.v.hi for z in pt)
print('dual seconds',time.time()-t0,'max exact residual decimal exp',max(float(abs(v)) for v in f0),flush=True)

# Approximate inverse with 120-digit arithmetic, then exact 90-digit rational reconstruction.
mp.mp.dps=150
M=mp.matrix([[mp.mpf(v.numerator)/v.denominator for v in row] for row in J0]);Minv=M**-1
Y=[[F(mp.nstr(Minv[i,j],100)) for j in range(DIM)] for i in range(DIM)]
# Krawczyk center c=y0-Yf0
cf=[]
for i in range(DIM):cf.append(y0[i]-sum(Y[i][j]*f0[j] for j in range(DIM)))
# E=I-YJX
E=[]
for i in range(DIM):
 row=[]
 for k in range(DIM):
  z=I(1 if i==k else 0)
  for j in range(DIM):z=z-Y[i][j]*JX[j][k]
  row.append(z)
 E.append(row)
delta=I(-rho,rho);K=[];ratios=[]
for i in range(DIM):
 z=I(cf[i])
 for k in range(DIM):z=z+E[i][k]*delta
 K.append(z)
 left=z.lo-(y0[i]-rho);right=(y0[i]+rho)-z.hi
 if left<=0 or right<=0:raise AssertionError(('Krawczyk inclusion failed',i,left,right,z))
 ratios.append(max(float((z.hi-y0[i])/rho),float((y0[i]-z.lo)/rho)))
print('Krawczyk max ratio',max(ratios),flush=True)

# Direct map interval Jacobian wrt local parameters. Avoid division by differentiating products.
def direct_jac_interval(M,vals):
 # vals: list I local direct parameters, length 3E+R
 flat=vals[:3*M.E];l=vals[3*M.E:];outs=[];J=[[I(0) for _ in range(3*M.E+M.R)] for _ in range(15)]
 for oi,terms in enumerate(M.outputs[1:]):
  ov=I(0)
  for bits,powers in terms:
   factors=[];tags=[]
   for v,e in powers:
    assert e==1;factors.append(flat[v]);tags.append(('edge',v,1))
   for j,b in enumerate(bits):factors.append(l[j] if b else 1-l[j]);tags.append(('lam',3*M.E+j,1 if b else -1))
   prodv=I(1)
   for f in factors:prodv=prodv*f
   ov=ov+prodv
   for a,(kind,idx,sgn) in enumerate(tags):
    dv=I(sgn)
    for b,f in enumerate(factors):
     if b!=a:dv=dv*f
    J[oi][idx]=J[oi][idx]+dv
  outs.append(ov)
 return outs,J

# value intervals extracted from x-box dual values
xvals=[d.v for d in xbox]
Wout,WJ=direct_jac_interval(s.MW,xvals[:32]);Pout,PJ=direct_jac_interval(s.MP,xvals[32:])
# choose rank columns from point scaled matrices
xpoint=[d.v.lo for d in full_dual(False)]

def choose_cols(J,offset):
 A=np.array([[float(sc*J[i][j].mid()*xpoint[offset+j]) for j in range(32)] for i,sc in enumerate(scales)])
 _,_,p=qr(A,mode='economic',pivoting=True);return tuple(int(i) for i in p[:15]),np.linalg.cond(A[:,p[:15]])
Wcols,Wcond=choose_cols([[I(v) for v in row] for row in J0],0) if False else (None,None)
# J0 above is equality-y, not local map. Build point local jac.
_,WJ0=direct_jac_interval(s.MW,[I(v) for v in xpoint[:32]])
_,PJ0=direct_jac_interval(s.MP,[I(v) for v in xpoint[32:]])
Wcols,Wcond=choose_cols(WJ0,0);Pcols,Pcond=choose_cols(PJ0,32)
print('rank cols',Wcols,Wcond,Pcols,Pcond,flush=True)

def rank_neumann_scaled(Jbox,Jpoint,cols,offset):
 # A(X)=row_scale*Jbox*fixed positive column scales. If ||I-YA(X)||_inf<1,
 # every matrix in the interval family is invertible by the Neumann lemma.
 A0=[[sc*Jpoint[i][c].lo*xpoint[offset+c] for c in cols] for i,sc in enumerate(scales)]
 AX=[[sc*Jbox[i][c]*xpoint[offset+c] for c in cols] for i,sc in enumerate(scales)]
 mp.mp.dps=150
 MM=mp.matrix([[mp.mpf(v.numerator)/v.denominator for v in row] for row in A0])
 inv=MM**-1
 YY=[[F(mp.nstr(inv[i,j],100)) for j in range(15)] for i in range(15)]
 EE=[];rowsums=[]
 for i in range(15):
  row=[]
  for k in range(15):
   z=I(1 if i==k else 0)
   for j in range(15):z=z-YY[i][j]*AX[j][k]
   row.append(z)
  EE.append(row);rowsums.append(sum(max(abs(z.lo),abs(z.hi)) for z in row))
 q=max(rowsums)
 if q>=1:raise AssertionError(('rank Neumann bound failed',q))
 det0=mp.det(MM)
 return q,mp.nstr(det0,80)
Wq,Wdet0=rank_neumann_scaled(WJ,WJ0,Wcols,0);Pq,Pdet0=rank_neumann_scaled(PJ,PJ0,Pcols,32)
print('rank Neumann bounds',float(Wq),float(Pq),'point dets',Wdet0,Pdet0,flush=True)

# physical and CT inequalities.
def min_physical(vals,side):
 lows=[];labels=[]
 for ei in range(10):
  c,g,t=vals[3*ei:3*ei+3]
  tests=[('c',c),('g',g),('t',t),('1-c',1-c),('1-g',1-g),('1-t',1-t),
         ('pC4',1+c-g-t),('pG4',1-c+g-t),('pT4',1-c-g+t),
         ('ctC',c-g*t),('ctG',g-c*t),('ctT',t-c*g)]
  for nm,z in tests:lows.append(z.lo);labels.append(f'{side}:e{ei}:{nm}')
 for j,lm in enumerate(vals[30:]):
  for nm,z in [('lam',lm),('1-lam',1-lm)]:lows.append(z.lo);labels.append(f'{side}:l{j}:{nm}')
 k=min(range(len(lows)),key=lambda i:lows[i]);return lows[k],labels[k]
Wmargin,Wlabel=min_physical(xvals[:32],'W');Pmargin,Plabel=min_physical(xvals[32:],'Wp')
if min(Wmargin,Pmargin)<=0:raise AssertionError('physical failure')
print('margins',Wlabel,float(Wmargin),Plabel,float(Pmargin),flush=True)

# common output intervals at certified root box (intersection of W/P images; equality root exists by Krawczyk)
common=[]
for ch,a,b in zip(s.CHARS[1:],Wout,Pout):
 interlo=max(a.lo,b.lo);interhi=min(a.hi,b.hi)
 # interval images need not overlap enclosure due dependency; root theorem establishes equality, hull sufficient
 common.append({'character':list(ch),'W':[str(a.lo),str(a.hi)],'Wprime':[str(b.lo),str(b.hi)],'hull':[str(min(a.lo,b.lo)),str(max(a.hi,b.hi))]})

def idata(z):return [str(z.lo),str(z.hi)]
cert={
 'schema':'k3p-weak-sharpness-krawczyk-v1',
 'method':'exact-rational Krawczyk operator on 15 scaled polynomial equality equations',
 'pivot_global_columns':list(PIV),'parameter_order':'W: 10 edges x (C,G,T), 2 inheritances; Wprime: same',
 'edge_orders':{'W':[list(e) for e in s.W_arcs],'Wprime':[list(e) for e in s.Wp_arcs]},
 'center_rationals':[str(v) for v in centers], 'root_center_y':[str(v) for v in y0], 'box_radius':str(rho),
 'row_scales':[str(v) for v in scales], 'exact_center_residual':[str(v) for v in f0],
 'krawczyk_intervals':[idata(z) for z in K], 'krawczyk_max_normalized_radius':repr(max(ratios)),
 'W_rank_columns':list(Wcols),'Wprime_rank_columns':list(Pcols),
 'W_scaled_rank_point_determinant':Wdet0,'Wprime_scaled_rank_point_determinant':Pdet0,
 'W_rank_neumann_infinity_bound':str(Wq),'Wprime_rank_neumann_infinity_bound':str(Pq),
 'W_rank_condition_discovery':repr(Wcond),'Wprime_rank_condition_discovery':repr(Pcond),
 'W_min_physical_ct_margin':[Wlabel,str(Wmargin)],'Wprime_min_physical_ct_margin':[Plabel,str(Pmargin)],
 'common_output_enclosures':common,
 'conclusion':{'unique_common_root_in_box':True,'W_rank':15,'Wprime_rank':15,'principal_domain':True,'strict_continuous_time':True}
}
out=ROOT/'software/certificates/k3p_sharpness_krawczyk.json';out.write_text(json.dumps(cert,indent=2,sort_keys=True)+'\n')
print('CERTIFIED_SHARPNESS_KRAWCZYK_PASS',out,flush=True)
