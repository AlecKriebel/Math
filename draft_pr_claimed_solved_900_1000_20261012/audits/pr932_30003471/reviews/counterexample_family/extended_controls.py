#!/usr/bin/env python3
"""Asymmetric and all-nonsimple octahedral direct counterexample families."""
import json, time, itertools, sys
from datetime import datetime, timezone
import numpy as np
from scipy.optimize import minimize, linprog
from scipy.spatial import ConvexHull
import controls as c

SEED=93230003472

def octa_normals(z,faces):
    v=np.reshape(z,(-1,3));center=v.mean(axis=0)
    ns=[];bs=[]
    for face in faces:
        i,j,k=face
        normal=c.unit(np.cross(v[j]-v[i],v[k]-v[i]))
        # The orientation is fixed before optimization. Convexity constraints
        # reject inward or degenerate arrangements.
        ns.append(normal);bs.append(normal@v[i])
    return np.array(ns),np.array(bs)

def octa_search(v,rng,starts=2):
    hull=ConvexHull(v);faces=[]
    for face,equation in zip(hull.simplices,hull.equations):
        i,j,k=map(int,face)
        if np.cross(v[j]-v[i],v[k]-v[i])@equation[:3]<0:j,k=k,j
        faces.append((i,j,k))
    faces=sorted(faces);z0=v.ravel();n,b=octa_normals(z0,faces);p=c.polytope(n,b)
    edges=p['edges'];g0=n@n.T;model=lambda z:octa_normals(z,faces)[0]
    local=c.local_lp(n,model,z0,edges)
    def convexity(x):
        vv=np.reshape(x[:-1],(-1,3));nn,bb=octa_normals(x[:-1],faces)
        return np.array([bb[i]-nn[i]@vv[j]-1e-4 for i,face in enumerate(faces) for j in range(len(vv)) if j not in face])
    def edge_constraint(x):return c.gram_edges(model(x[:-1]),edges)-c.gram_edges(n,edges)-x[-1]
    def separation(x):
        nn=model(x[:-1]);return np.sum((nn@nn.T-g0)**2)-.01
    cs=[{'type':'ineq','fun':convexity},{'type':'ineq','fun':edge_constraint},{'type':'ineq','fun':separation}]
    trials=[]
    for trial in range(starts):
        z=z0+rng.uniform(-.15,.15,len(z0));x=np.r_[z,min(edge_constraint(np.r_[z,0]))-.01]
        start=time.monotonic()
        try:
            opt=minimize(lambda x:-x[-1],x,method='SLSQP',constraints=cs,
                bounds=list(zip(z0-.5,z0+.5))+[(-2,1)],options={'maxiter':200,'ftol':1e-10,'disp':False})
            nn,bb=octa_normals(opt.x[:-1],faces);q=c.polytope(nn,bb)
            delta=c.gram_edges(nn,edges)-c.gram_edges(n,edges)
            topology=q['incidence']==p['incidence'] and q['edges']==edges
            valid=bool(topology and min(convexity(opt.x))>=-1e-7 and separation(opt.x)>=-1e-7)
            trials.append(dict(trial=trial,success=bool(opt.success),message=str(opt.message),iterations=int(opt.nit),
                elapsed_seconds=time.monotonic()-start,topology_equal=topology,constraints_valid=valid,
                minimum_dot_difference=float(min(delta)),maximum_dot_difference=float(max(delta)),
                gram_separation_squared=float(separation(opt.x)+.01),edge_dot_differences=delta.tolist(),
                q_vertices=opt.x[:-1].reshape((-1,3)).tolist(),q_normals=nn.tolist(),q_supports=bb.tolist(),
                q_polytope=c.serial_poly(q),numerical_candidate_strict=bool(valid and min(delta)>1e-7),
                numerical_candidate_weak=bool(valid and min(delta)>=-1e-9)))
        except (ValueError,np.linalg.LinAlgError) as e:
            trials.append(dict(trial=trial,error=str(e),elapsed_seconds=time.monotonic()-start))
    return dict(mechanism='six independently movable vertices; eight triangular supporting facets; every octahedron vertex is nonsimple',
        p_vertices=v.tolist(),p_normals=n.tolist(),p_supports=b.tolist(),triangular_facets=faces,
        p_polytope=c.serial_poly(p),starts=starts,initial_random_radius=.15,parameter_radius=.5,
        maxiter=200,ftol=1e-10,separation_squared_minimum=.01,nonincident_support_slack_minimum=1e-4,
        local_lp=local,trials=trials)

def approximate_stress(search):
    # Retain exact-equality LP failure in original record. This supplemental
    # tolerance diagnostic cannot certify a mathematically exact identity.
    if 'initial_parameters' not in search:return None
    n=search['n'];x=np.array(search['initial_parameters']);model=lambda z:c.pyramid_model(z,n)[0]
    edges=search['p_polytope']['edges'];j=c.finite_jacobian(lambda z:c.gram_edges(model(z),edges),x)
    ee=len(edges);tol=1e-8
    ub=np.vstack([np.c_[-np.eye(ee),np.ones(ee)],np.c_[j.T,np.zeros(len(x))],np.c_[-j.T,np.zeros(len(x))]])
    rhs=np.r_[np.zeros(ee),np.ones(2*len(x))*tol]
    opt=linprog(np.r_[np.zeros(ee),-1],A_ub=ub,b_ub=rhs,A_eq=[np.r_[np.ones(ee),0]],b_eq=[1],
        bounds=[(0,None)]*(ee+1),method='highs')
    return dict(success=bool(opt.success),allowed_residual=tol,exact_certificate=False,
        min_normalized_stress=float(opt.x[-1]) if opt.success else None,
        residual=float(max(abs(j.T@opt.x[:-1]))) if opt.success else None,
        residual_within_allowed=bool(max(abs(j.T@opt.x[:-1]))<=tol) if opt.success else False,
        warning='Solver success is not residual validation; default solver feasibility tolerances may exceed allowed_residual.',
        weights=opt.x[:-1].tolist() if opt.success else None)

def main():
    rng=np.random.default_rng(SEED);started=datetime.now(timezone.utc).isoformat();searches={}
    # Recompute the final exact controls after adding exact local identities.
    record=json.loads((c.HERE/'CONSTRUCTIVE_CONTROLS.json').read_text());record['exact']=c.exact_controls()
    (c.HERE/'CONSTRUCTIVE_CONTROLS.json').write_text(json.dumps(record,indent=2,sort_keys=True)+'\n')
    for name,(n,b) in c.bases().items():
        expected=c.polytope(n,b)['incidence'];attempts=0
        while True:
            attempts+=1;nn=c.normal_model(n,rng.uniform(-.16,.16,2*len(n)))
            try:
                p=c.polytope(nn,b)
                if p['incidence']==expected:break
            except (ValueError,np.linalg.LinAlgError):pass
            if attempts>100:raise RuntimeError('base sampling exhausted')
        s=c.simple_search(name,nn,b,rng,starts=2);s['base_sampling_attempts']=attempts
        searches['asymmetric_'+name]=s;print('asymmetric',name,'done',flush=True)
    for n in [4,5,8]:
        # Nonregular base from an affine stretch/shear and noncentral apex.
        xy=np.array([[np.cos(2*np.pi*i/n),np.sin(2*np.pi*i/n)] for i in range(n)])@np.array([[1.17,.18],[-.09,.83]])
        z=np.r_[xy.ravel(),[.19,-.14]]
        searches[f'asymmetric_pyramid_{n}']=c.pyramid_search(n,rng,base_parameters=z,starts=2)
        print('asymmetric pyramid',n,'done',flush=True)
    v=np.array([[1,0,0],[-1,0,0],[0,1,0],[0,-1,0],[0,0,1],[0,0,-1]],float)
    searches['octahedron']=octa_search(v,rng)
    v2=v+np.array([[.1,.08,-.04],[-.08,.03,.1],[.05,.07,-.08],[-.06,-.1,.03],[.07,-.04,.12],[-.09,.02,-.1]])
    searches['asymmetric_octahedron']=octa_search(v2,rng)
    original=json.loads((c.HERE/'SEARCH_RESULTS.json').read_text())
    diagnostic=approximate_stress(original['searches']['pyramid_8'])
    trials=[t for s in searches.values() for t in s['trials']]
    result=dict(started_utc=started,finished_utc=datetime.now(timezone.utc).isoformat(),seed=SEED,
        protocol='Two bounded starts per asymmetric original family and regular/asymmetric octahedron; same incidence verification and dominance conventions as controls.py',
        searches=searches,supplemental_tolerance_stress_for_original_pyramid8=diagnostic,
        summary=dict(families=len(searches),trials=len(trials),successful_optimizer_stops=sum(t.get('success',False) for t in trials),
        constraints_valid=sum(t.get('constraints_valid',False) for t in trials),
        strict_numerical_candidates=sum(t.get('numerical_candidate_strict',False) for t in trials),
        weak_numerical_candidates=sum(t.get('numerical_candidate_weak',False) for t in trials)),
        limits=['All searches remain local and bounded; no universal theorem follows.','All octahedral facet incidences are re-enumerated from halfspaces after optimization.',
        'Tolerance stress is numerical evidence; its nonzero allowed residual prevents an exact positivity inference.'])
    (c.HERE/'EXTENDED_SEARCH_RESULTS.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps(result['summary'],sort_keys=True),flush=True)

if __name__=='__main__':main()
