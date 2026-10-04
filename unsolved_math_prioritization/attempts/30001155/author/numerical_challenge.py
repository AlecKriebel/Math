#!/usr/bin/env python3
"""Deterministic P1 FEM diagnostics on convex inscribed polygons; NOT certified bounds."""
import json,math,sys
from pathlib import Path
import numpy as np
from scipy.sparse import coo_matrix
from scipy.sparse.linalg import eigsh
from scipy.spatial.distance import pdist
from scipy.special import jn_zeros
DELTA=float(jn_zeros(1,1)[0]**2-jn_zeros(0,1)[0]**2)
THETA=1-3*math.pi**2/(4*DELTA)
def boundary(kind,param,n):
 a=np.arange(n)*2*math.pi/n;c=np.cos(a);s=np.sin(a)
 if kind=='ellipse':return np.c_[c,param*s]
 if kind=='rectangle':
  r=1/np.maximum(abs(c),abs(s)/param);return np.c_[r*c,r*s]
 if kind=='stadium':
  L=param;b=1.0
  mask=b*abs(c)<=L*abs(s)
  r=np.empty(n);r[mask]=b/abs(s[mask]);r[~mask]=L*abs(c[~mask])+np.sqrt(np.maximum(0,b*b-L*L*s[~mask]**2))
  return np.c_[r*c,r*s]
 if kind=='support3':
  h=1+param*np.cos(3*a);dh=-3*param*np.sin(3*a)
  return np.c_[h*c-dh*s,h*s+dh*c]
 if kind=='support4':
  h=1+param*np.cos(4*a);dh=-4*param*np.sin(4*a)
  return np.c_[h*c-dh*s,h*s+dh*c]
 raise ValueError(kind)
def mesh(b,m):
 n=len(b);p=np.vstack([np.zeros((1,2))]+[b*j/m for j in range(1,m+1)])
 tri=[]
 for i in range(n):tri.append((0,1+i,1+(i+1)%n))
 for j in range(1,m):
  st=1+(j-1)*n;nx=1+j*n
  for i in range(n):
   k=(i+1)%n;tri.extend([(st+i,nx+i,nx+k),(st+i,nx+k,st+k)])
 return p,np.array(tri),1+(m-1)*n

def solve(kind,param,n,m):
 b=boundary(kind,param,n);p,t,free=mesh(b,m)
 edge=np.roll(b,-1,axis=0)-b;cross=edge[:,0]*np.roll(edge,-1,axis=0)[:,1]-edge[:,1]*np.roll(edge,-1,axis=0)[:,0]
 assert cross.min()>-1e-12
 area=abs(np.sum(b[:,0]*np.roll(b[:,1],-1)-b[:,1]*np.roll(b[:,0],-1)))/2
 d=float(pdist(b).max());rows=[];cols=[];kv=[];mv=[]
 for nodes in t:
  v=p[nodes];twice=np.linalg.det(np.array([v[1]-v[0],v[2]-v[0]]));assert twice>0
  ar=twice/2
  grad=np.array([[v[1,1]-v[2,1],v[2,0]-v[1,0]],[v[2,1]-v[0,1],v[0,0]-v[2,0]],[v[0,1]-v[1,1],v[1,0]-v[0,0]]])/twice
  k=ar*grad@grad.T;mm=ar*(np.ones((3,3))+np.eye(3))/12
  for i in range(3):
   for j in range(3):rows.append(nodes[i]);cols.append(nodes[j]);kv.append(k[i,j]);mv.append(mm[i,j])
 K=coo_matrix((kv,(rows,cols)),shape=(len(p),len(p))).tocsr()[:free,:free]
 M=coo_matrix((mv,(rows,cols)),shape=(len(p),len(p))).tocsr()[:free,:free]
 vals,vec=eigsh(K,k=3,M=M,sigma=0,which='LM',tol=1e-10,v0=np.linspace(1,2,free));ix=np.argsort(vals);vals=vals[ix];vec=vec[:,ix]
 residuals=[float(np.linalg.norm(K@vec[:,i]-vals[i]*(M@vec[:,i]))/np.linalg.norm(K@vec[:,i])) for i in range(3)]
 q=4*area/(math.pi*d*d);F=3*math.pi**2/(1-THETA*(1-math.sqrt(max(0,1-q*q))))
 gap=(vals[1]-vals[0])*d*d
 return dict(kind=kind,param=param,n=n,m=m,free_vertices=free,triangles=len(t),area=area,diameter=d,q=q,eigenvalues=vals.tolist(),matrix_relative_residuals=residuals,normalized_gap=gap,conjectured_bound=F,margin=gap-F,interpretation='uncertified difference of Ritz eigenvalues on polygon')
if __name__ == '__main__':
 cases=[('ellipse',1),('ellipse',.98),('ellipse',.75),('ellipse',.3),('ellipse',.1),('rectangle',1),('rectangle',.3),('stadium',1),('stadium',4),('stadium',10),('support3',.1),('support3',.124),('support4',.04)]
 results=[]
 for case in cases:
  for n,m in [(64,12),(128,24)]:
   r=solve(*case,n,m);results.append(r);print(json.dumps(r),flush=True)
 summary={'status':'DIAGNOSTIC_ONLY','cases':len(cases),'runs':len(results),'minimum_margin':min(x['margin'] for x in results),'all_sample_margins_positive':all(x['margin']>0 for x in results),'results':results,'limitations':['No eigenvalue enclosure; subtraction of Ritz upper bounds is not a bound on the true gap.','Curved domains are approximated by explicit inscribed convex polygons.','No exhaustive optimization or general theorem is inferred.']}
 Path(__file__).with_name('numerical_results.json').write_text(json.dumps(summary,indent=2)+'\n')
