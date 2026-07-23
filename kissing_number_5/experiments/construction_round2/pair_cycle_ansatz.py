#!/usr/bin/env python3
"""Search 18 antipodal pairs plus a 5-cycle component in S^4.

The intended deep-negative graph is C5 disjoint union 18 K2.  Initial points
come from deleting two D5 lines and inserting a regular pentagon in their
span.  Optimization first preserves all 18 antipodal pairs, then optionally
releases all 41 points.  Floating-point discovery only.
"""
from __future__ import annotations
import argparse,importlib.util,json,math
from pathlib import Path
import numpy as np
from scipy.optimize import minimize

SPEC=importlib.util.spec_from_file_location('r2',Path(__file__).with_name('search_round2.py'))
R2=importlib.util.module_from_spec(SPEC);SPEC.loader.exec_module(R2)
ASPEC=importlib.util.spec_from_file_location('anti',Path(__file__).with_name('antipodal_lines.py'))
ANTI=importlib.util.module_from_spec(ASPEC);ASPEC.loader.exec_module(ANTI)


def unpack(flat):
    y=flat.reshape(23,5);norm=np.linalg.norm(y,axis=1)
    return y/norm[:,None],norm


def term_data(z):
    """Values and endpoints/sign derivatives for the constrained maximum."""
    u=z[:18];v=z[18:]
    vals=[];records=[]
    for i in range(18):
      for j in range(i+1,18):
        d=float(u[i]@u[j])
        vals.extend((d,-d));records.extend(((i,j,1.),(i,j,-1.)))
    for i in range(18):
      for a in range(5):
        j=18+a;d=float(u[i]@v[a])
        vals.extend((d,-d));records.extend(((i,j,1.),(i,j,-1.)))
    for a in range(5):
      for b in range(a+1,5):
        i,j=18+a,18+b;d=float(v[a]@v[b])
        vals.append(d);records.append((i,j,1.))
    return np.asarray(vals),records


def smooth_fg(flat,beta):
    z,norms=unpack(flat);vals,recs=term_data(z);zz=beta*vals;zm=zz.max()
    ee=np.exp(zz-zm);w=ee/ee.sum();gz=np.zeros_like(z)
    for weight,(i,j,sgn) in zip(w,recs):
        gz[i]+=weight*sgn*z[j];gz[j]+=weight*sgn*z[i]
    radial=np.sum(gz*z,axis=1);gy=(gz-radial[:,None]*z)/norms[:,None]
    return float((zm+math.log(ee.sum()))/beta),gy.ravel()


def true_max(z):
    vals,_=term_data(z)
    return float(vals.max())


def constrained_sqp(z0):
    z0=R2.unit_rows(z0);t=true_max(z0);q0=np.r_[z0.ravel(),t+1e-9]
    vals0,recs=term_data(z0);m=len(vals0)
    def obj(q):
        g=np.zeros_like(q);g[-1]=1;return float(q[-1]),g
    def eq(q):
        y=q[:-1].reshape(23,5);val=np.sum(y*y,axis=1)-1
        jac=np.zeros((23,len(q)))
        for i in range(23):jac[i,5*i:5*i+5]=2*y[i]
        return val,jac
    def iq(q):
        y=q[:-1].reshape(23,5);vals,recs=term_data(y);out=q[-1]-vals
        jac=np.zeros((m,len(q)));jac[:,-1]=1
        for row,(i,j,sgn) in enumerate(recs):
            jac[row,5*i:5*i+5]=-sgn*y[j]
            jac[row,5*j:5*j+5]=-sgn*y[i]
        return out,jac
    cons=({'type':'eq','fun':lambda q:eq(q)[0],'jac':lambda q:eq(q)[1]},
          {'type':'ineq','fun':lambda q:iq(q)[0],'jac':lambda q:iq(q)[1]})
    r=minimize(obj,q0,jac=True,method='SLSQP',constraints=cons,
               options={'maxiter':3500,'ftol':5e-14,'disp':False})
    z=R2.unit_rows(r.x[:-1].reshape(23,5))
    return z,{'mu':true_max(z),'nit':int(r.nit),
        'success':bool(r.success),'message':str(r.message)}


def target_graph_violations(z, strict_margin=1e-6):
    """Violation functions for the cell H = C5 disjoint union 18 K2."""
    u=z[:18];v=z[18:];values=[];records=[]
    for i in range(18):
      for j in range(i+1,18):
        d=float(u[i]@u[j])
        values.extend((d-.5,-d-.5))
        records.extend(((i,j,1.),(i,j,-1.)))
    for i in range(18):
      for a in range(5):
        j=18+a;d=float(u[i]@v[a])
        values.extend((d-.5,-d-.5))
        records.extend(((i,j,1.),(i,j,-1.)))
    for a in range(5):
      for b in range(a+1,5):
        i,j=18+a,18+b;d=float(v[a]@v[b])
        # In the natural cyclic order, separation two is an edge of the
        # negative C5 (a regular pentagon then has dot cos(4*pi/5)).
        cycle_edge=((b-a)%5 in (2,3))
        values.append(d-.5);records.append((i,j,1.))
        if cycle_edge:
            values.append(d+.5+strict_margin);records.append((i,j,1.))
        else:
            values.append(-d-.5);records.append((i,j,-1.))
    return np.asarray(values),records


def target_graph_sqp(z0, strict_margin=1e-6):
    """Minimize the maximum violation while fixing the desired deep graph."""
    z0=R2.unit_rows(z0);vals0,recs=target_graph_violations(z0,strict_margin)
    q0=np.r_[z0.ravel(),float(vals0.max())+1e-9];m=len(vals0)
    def obj(q):
        g=np.zeros_like(q);g[-1]=1;return float(q[-1]),g
    def eq(q):
        y=q[:-1].reshape(23,5);val=np.sum(y*y,axis=1)-1
        jac=np.zeros((23,len(q)))
        for i in range(23):jac[i,5*i:5*i+5]=2*y[i]
        return val,jac
    def iq(q):
        y=q[:-1].reshape(23,5);vals,recs=target_graph_violations(y,strict_margin)
        out=q[-1]-vals;jac=np.zeros((m,len(q)));jac[:,-1]=1
        for row,(i,j,sgn) in enumerate(recs):
            jac[row,5*i:5*i+5]=-sgn*y[j]
            jac[row,5*j:5*j+5]=-sgn*y[i]
        return out,jac
    cons=({'type':'eq','fun':lambda q:eq(q)[0],'jac':lambda q:eq(q)[1]},
          {'type':'ineq','fun':lambda q:iq(q)[0],'jac':lambda q:iq(q)[1]})
    r=minimize(obj,q0,jac=True,method='SLSQP',constraints=cons,
               options={'maxiter':4000,'ftol':5e-14,'disp':False})
    z=R2.unit_rows(r.x[:-1].reshape(23,5))
    violations,_=target_graph_violations(z,strict_margin)
    return z,{'maximum_violation':float(violations.max()),
        'strict_margin':strict_margin,'nit':int(r.nit),
        'success':bool(r.success),'message':str(r.message)}


def make_initial(seed):
    rng=np.random.default_rng(seed);lines=ANTI.d5_lines()
    removed=np.sort(rng.choice(20,2,replace=False));keep=np.ones(20,dtype=bool);keep[removed]=False
    u=lines[keep].copy();a,b=lines[removed]
    e1=a.copy();e2=b-(b@e1)*e1;e2/=np.linalg.norm(e2)
    phase=rng.uniform(0,2*math.pi)
    v=np.asarray([math.cos(phase+2*math.pi*j/5)*e1+
                  math.sin(phase+2*math.pi*j/5)*e2 for j in range(5)])
    z=np.vstack((u,v))
    scale=(0.,1e-4,.003,.02,.08)[seed%5]
    noise=rng.normal(size=z.shape);noise-=np.sum(noise*z,axis=1)[:,None]*z
    z=R2.unit_rows(z+scale*noise)
    return z,removed.tolist(),phase,scale


def full_points(z):
    return np.vstack((z[:18],-z[:18],z[18:]))


def deep_graph_diagnostics(x):
    g=x@x.T;n=len(x);a=g<-.5;np.fill_diagonal(a,False)
    degrees=a.sum(1).astype(int);tri=int(np.trace(a.astype(int)@a.astype(int)@a.astype(int))//6)
    unseen=set(range(n));components=[]
    while unseen:
        stack=[unseen.pop()];verts=[]
        while stack:
            i=stack.pop();verts.append(i);nbr=set(np.flatnonzero(a[i]))&unseen
            unseen-=nbr;stack.extend(nbr)
        components.append(len(verts))
    return {'deep_edges':int(a.sum()//2),'deep_degree_histogram':
            {str(int(v)):int(np.sum(degrees==v)) for v in np.unique(degrees)},
            'deep_components':sorted(components,reverse=True),'deep_triangles':tri,
            'minimum_inner_product':float(np.min(g[np.triu_indices(n,1)]))}


def one(seed,release=True):
    z,removed,phase,scale=make_initial(seed);hist=[]
    target_z,target_sqp=target_graph_sqp(z)
    initial=true_max(z)
    for beta in (30.,90.,270.,810.,2430.,7290.,21870.):
        r=minimize(smooth_fg,z.ravel(),args=(beta,),jac=True,method='L-BFGS-B',
                   options={'maxiter':1600,'ftol':3e-16,'gtol':2e-10,
                            'maxls':70,'maxcor':40})
        z=R2.unit_rows(r.x.reshape(23,5))
        hist.append([beta,true_max(z),int(r.nit),bool(r.success)])
    z,sq=constrained_sqp(z);xc=full_points(z);constrained=R2.diagnostics(xc)
    released=None
    if release:
        xr,rh=R2.refine_full(xc,betas=(300.,1200.,4800.,19200.,76800.))
        xg,gh=R2.graph_realize(xr,target_degree=8+seed%3,outer=2)
        if R2.max_ip(xg)<R2.max_ip(xr):xr=xg;choice='graph'
        else:choice='minimax'
        xr,final_sqp=R2.epigraph_slsqp(xr)
        released={'choice':choice,'history':rh,'graph_history':gh,
                  'final_epigraph_slsqp':final_sqp,
                  'diagnostics':R2.diagnostics(xr),
                  'deep_graph':deep_graph_diagnostics(xr),'coordinates':xr.tolist()}
    return {'seed':seed,'removed_lines':removed,'phase':phase,'noise_scale':scale,
            'target_graph_sqp':target_sqp,
            'target_graph_diagnostics':R2.diagnostics(full_points(target_z)),
            'target_graph_deep_graph':deep_graph_diagnostics(full_points(target_z)),
            'initial_mu':initial,'constrained_history':hist,'constrained_sqp':sq,
            'constrained_diagnostics':constrained,
            'constrained_deep_graph':deep_graph_diagnostics(xc),
            'constrained_coordinates':xc.tolist(),'released':released}


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--seeds',type=int,nargs='+',required=True)
    ap.add_argument('--no-release',action='store_true');ap.add_argument('--out',type=Path,required=True)
    a=ap.parse_args();runs=[]
    for seed in a.seeds:
        r=one(seed,not a.no_release);runs.append(r)
        print(seed,r['removed_lines'],r['constrained_diagnostics']['maxip'],
              None if r['released'] is None else r['released']['diagnostics']['maxip'],
              r['constrained_deep_graph'],flush=True)
    a.out.write_text(json.dumps({'status':'NUMERICAL EVIDENCE ONLY — NOT A CERTIFICATE',
        'ansatz':'18 exact antipodal pairs plus five points; D5-minus-two-lines plus regular pentagon seed',
        'runs':runs},indent=2)+'\n')
if __name__=='__main__':main()
