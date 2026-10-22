#!/usr/bin/env python3
"""Independent, bounded direct-angle falsification searches and exact controls.

Numerical searches are empirical controls, never universal theorem certificates.
No author's control code is imported or executed.
"""
import itertools, json, math, pathlib, platform, sys, time
from datetime import datetime, timezone
import numpy as np
import scipy
from scipy.optimize import minimize, linprog
from scipy.spatial import ConvexHull
import sympy as sp

HERE=pathlib.Path(__file__).resolve().parent
SEED=93230003471
np.set_printoptions(precision=16)

def unit(a):
    a=np.asarray(a,dtype=float)
    return a/np.linalg.norm(a,axis=-1,keepdims=True)

def polytope(a,b,tol=2e-7):
    """All feasible triple-plane intersections and full facet incidence.

    Strict origin interior in the normal hull certifies boundedness numerically.
    This routine deliberately does not trust a supplied edge list.
    """
    a=np.asarray(a,float); b=np.asarray(b,float)
    nh=ConvexHull(unit(a))
    normal_hull_margin=float(-np.max(nh.equations[:,-1]))
    if normal_hull_margin<=1e-7: raise ValueError('unbounded or uncertain normal hull')
    vertices=[]
    for inds in itertools.combinations(range(len(a)),3):
        block=a[list(inds)]
        if abs(np.linalg.det(block))<1e-10: continue
        v=np.linalg.solve(block,b[list(inds)])
        if np.max(a@v-b)>tol: continue
        if not any(np.linalg.norm(v-w)<tol*10 for w in vertices): vertices.append(v)
    v=np.array(vertices)
    if len(v)<4: raise ValueError('not full dimensional')
    hull=ConvexHull(v)
    if hull.volume<1e-8: raise ValueError('nearly zero volume')
    incidence=sorted(tuple(map(int,np.flatnonzero(abs(a@x-b)<tol*10))) for x in v)
    if any(sum(i in row for row in incidence)<3 for i in range(len(a))):
        raise ValueError('redundant facet')
    edges=[]
    for i,j in itertools.combinations(range(len(a)),2):
        common=[x for x,row in zip(v,[tuple(np.flatnonzero(abs(a@x-b)<tol*10)) for x in v]) if i in row and j in row]
        if len(common)>=2:
            if np.linalg.matrix_rank(np.array(common)-common[0],tol=tol*10)!=1:
                raise ValueError('invalid ridge dimension')
            edges.append((i,j))
    return dict(vertices=v, incidence=incidence, edges=edges, volume=float(hull.volume),
                normal_hull_margin=normal_hull_margin)

def serial_poly(d):
    return {k:v.tolist() if isinstance(v,np.ndarray) else v for k,v in d.items()}

def bases():
    ans={}
    a=unit([[1,1,1],[1,-1,-1],[-1,1,-1],[-1,-1,1]])
    ans['tetrahedron']=(a,np.ones(4))
    def prism(n):
        normals=[[math.cos(2*math.pi*i/n),math.sin(2*math.pi*i/n),0] for i in range(n)]
        normals += [[0,0,-1],[0,0,1]]
        return np.array(normals),np.ones(n+2)
    ans['triangular_prism']=prism(3)
    ans['cube']=prism(4)
    ans['pentagonal_prism']=prism(5)
    a=np.array([[1,0,0],[-1,0,0],[0,1,0],[0,-1,0],[0,0,1],[0,0,-1],[1,1,1]],float)
    b=np.array([1,1,1,1,1,1,2.0])
    scales=np.linalg.norm(a,axis=1)
    ans['truncated_cube']=(a/scales[:,None],b/scales)
    return ans

def tangent_bases(n):
    ans=[]
    for v in n:
        e=np.eye(3)[np.argmin(abs(v))]
        u=np.cross(v,e);u/=np.linalg.norm(u)
        ans.append([u,np.cross(v,u)])
    return np.array(ans)

def normal_model(n,coords):
    return unit(n+np.einsum('fkc,fk->fc',tangent_bases(n),np.reshape(coords,(-1,2))))

def gram_edges(n,edges): return np.array([n[i]@n[j] for i,j in edges])

def finite_jacobian(fun,x,step=2e-6):
    return np.column_stack([(fun(x+np.eye(len(x))[j]*step)-fun(x-np.eye(len(x))[j]*step))/(2*step) for j in range(len(x))])

def local_lp(n,model,x,edges):
    j=finite_jacobian(lambda z:gram_edges(model(z),edges),x)
    # Maximize t with Jv >= t and coordinate cube |v_i| <= 1.
    c=np.r_[np.zeros(len(x)),-1.0]
    r=linprog(c,A_ub=np.c_[-j,np.ones(len(edges))],b_ub=np.zeros(len(edges)),
              bounds=[(-1,1)]*len(x)+[(None,None)],method='highs')
    # A positive dual equilibrium stress w is an independent local obstruction.
    # Finite differences cannot certify exact positivity or a universal identity.
    stress=linprog(np.r_[np.zeros(len(edges)),-1.0],
        A_ub=np.c_[-np.eye(len(edges)),np.ones(len(edges))],b_ub=np.zeros(len(edges)),
        A_eq=np.block([[j.T,np.zeros((len(x),1))],[np.ones((1,len(edges))),np.zeros((1,1))]]),
        b_eq=np.r_[np.zeros(len(x)),1.0],bounds=[(0,None)]*len(edges)+[(0,None)],
        method='highs',options={'dual_feasibility_tolerance':1e-8,'primal_feasibility_tolerance':1e-8})
    return dict(jacobian_shape=list(j.shape), jacobian_rank=int(np.linalg.matrix_rank(j,tol=1e-7)),
        lp_success=bool(r.success), maximal_minimum_dot_derivative=float(r.x[-1]) if r.success else None,
        positive_stress_success=bool(stress.success),
        min_normalized_stress=float(stress.x[-1]) if stress.success else None,
        stress_residual=float(np.max(abs(j.T@stress.x[:-1]))) if stress.success else None,
        stress_weights=stress.x[:-1].tolist() if stress.success else None)

def simple_search(name,n,b,rng,starts=5):
    base=polytope(n,b); edges=base['edges']; f=len(n); dimension=2*f
    expected=base['incidence']; vertex_sets=[list(i) for i in expected]
    model=lambda x:normal_model(n,x)
    original_gram=n@n.T
    coords0=np.zeros(dimension)
    local=local_lp(n,model,coords0,edges)
    nonincident=[(row,k) for row in vertex_sets for k in range(f) if k not in row]
    def slack(x):
        nn=model(x[:-1]); vv={tuple(row):np.linalg.solve(nn[row],b[row]) for row in vertex_sets}
        return np.array([b[k]-nn[k]@vv[tuple(row)]-1e-4 for row,k in nonincident])
    def edges_constraint(x): return gram_edges(model(x[:-1]),edges)-gram_edges(n,edges)-x[-1]
    def separation(x): return np.sum((model(x[:-1])@model(x[:-1]).T-original_gram)**2)-0.01
    constraints=[{'type':'ineq','fun':slack},{'type':'ineq','fun':edges_constraint},
                 {'type':'ineq','fun':separation}]
    trials=[]
    for trial in range(starts):
        z=rng.uniform(-0.24,0.24,dimension)
        x=np.r_[z,float(np.min(gram_edges(model(z),edges)-gram_edges(n,edges)))-0.01]
        t0=time.monotonic()
        try:
            opt=minimize(lambda x:-x[-1],x,method='SLSQP',bounds=[(-0.65,0.65)]*dimension+[(-2,1)],
                constraints=constraints,options={'maxiter':180,'ftol':1e-10,'disp':False})
            q=model(opt.x[:-1]); pq=polytope(q,b)
            deltas=gram_edges(q,edges)-gram_edges(n,edges)
            topology=pq['incidence']==expected and pq['edges']==edges
            minslack=float(np.min(slack(opt.x)))
            separated=float(separation(opt.x))
            valid=topology and minslack>=-1e-7 and separated>=-1e-7
            trials.append(dict(trial=trial, success=bool(opt.success), message=str(opt.message),
                iterations=int(opt.nit), elapsed_seconds=time.monotonic()-t0,
                topology_equal=topology, constraints_valid=valid,
                minimum_dot_difference=float(min(deltas)),maximum_dot_difference=float(max(deltas)),
                gram_separation_squared=float(np.sum((q@q.T-original_gram)**2)),
                minimum_incidence_constraint_slack=minslack,
                edge_dot_differences=deltas.tolist(), parameters=opt.x[:-1].tolist(),
                q_normals=q.tolist(), q_supports=b.tolist(), q_polytope=serial_poly(pq),
                numerical_candidate_strict=bool(valid and min(deltas)>1e-7),
                numerical_candidate_weak=bool(valid and min(deltas)>=-1e-9)))
        except (ValueError,np.linalg.LinAlgError) as e:
            trials.append(dict(trial=trial,error=str(e),elapsed_seconds=time.monotonic()-t0))
    return dict(mechanism='unit facet normals at fixed positive support values; full stable incidence chamber',
                p_normals=n.tolist(),p_supports=b.tolist(),p_polytope=serial_poly(base),
                parameter_bounds=[-0.65,0.65],starts=starts,initial_random_bounds=[-0.24,0.24],
                maxiter=180,ftol=1e-10,separation_squared_minimum=0.01,
                nonincident_support_slack_minimum=1e-4,local_lp=local,trials=trials)

def pyramid_model(z,n):
    xy=np.reshape(z[:2*n],(n,2)); apex=np.r_[z[2*n:],1.0]
    verts=np.vstack([np.c_[xy,np.zeros(n)],apex])
    normals=[np.array([0.,0.,-1.])]
    for i in range(n): normals.append(unit(np.cross(verts[(i+1)%n]-verts[i],apex-verts[i])))
    normals=np.array(normals); center=verts.mean(axis=0)
    # Shift all vertices by their interior vertex-average before constructing b.
    vertices=verts-center
    supports=np.r_[-vertices[0,2],[normals[i+1]@vertices[i] for i in range(n)]]
    return normals,supports,vertices

def polygon_slacks(z,n):
    xy=np.reshape(z[:2*n],(n,2));out=[]
    for i in range(n):
        edge=xy[(i+1)%n]-xy[i]
        for j in range(n):
            if j in [i,(i+1)%n]:continue
            d=xy[j]-xy[i];out.append(edge[0]*d[1]-edge[1]*d[0]-1e-4)
    return np.array(out)

def pyramid_search(n,rng,base_parameters=None,starts=5):
    z0=np.r_[np.array([[math.cos(2*math.pi*i/n),math.sin(2*math.pi*i/n)] for i in range(n)]).ravel(),[0.,0.]] if base_parameters is None else np.array(base_parameters,float)
    nn,bb,vv=pyramid_model(z0,n);base=polytope(nn,bb); edges=base['edges'];g0=nn@nn.T
    model=lambda z:pyramid_model(z,n)[0]
    local=local_lp(nn,model,z0,edges)
    def ec(x):return gram_edges(model(x[:-1]),edges)-gram_edges(nn,edges)-x[-1]
    def sep(x):
        q=model(x[:-1]);return np.sum((q@q.T-g0)**2)-0.01
    cs=[{'type':'ineq','fun':ec},{'type':'ineq','fun':sep},
        {'type':'ineq','fun':lambda x:polygon_slacks(x[:-1],n)}]
    trials=[]
    for trial in range(starts):
        z=z0+rng.uniform(-.2,.2,len(z0));x=np.r_[z,min(ec(np.r_[z,0.]))-.01]
        start=time.monotonic()
        try:
            opt=minimize(lambda x:-x[-1],x,method='SLSQP',bounds=list(zip(z0-.65,z0+.65))+[(-2,1)],
                constraints=cs,options={'maxiter':200,'ftol':1e-10,'disp':False})
            q,b,v=pyramid_model(opt.x[:-1],n);pq=polytope(q,b)
            delta=gram_edges(q,edges)-gram_edges(nn,edges)
            topology=base['incidence']==pq['incidence'] and edges==pq['edges']
            valid=bool(topology and min(polygon_slacks(opt.x[:-1],n))>=-1e-7 and sep(opt.x)>=-1e-7)
            trials.append(dict(trial=trial,success=bool(opt.success),message=str(opt.message),
                iterations=int(opt.nit),elapsed_seconds=time.monotonic()-start,
                topology_equal=topology,constraints_valid=valid,
                minimum_dot_difference=float(min(delta)),maximum_dot_difference=float(max(delta)),
                gram_separation_squared=float(np.sum((q@q.T-g0)**2)),
                edge_dot_differences=delta.tolist(),parameters=opt.x[:-1].tolist(),
                q_normals=q.tolist(),q_supports=b.tolist(),q_vertices=v.tolist(),q_polytope=serial_poly(pq),
                numerical_candidate_strict=bool(valid and min(delta)>1e-7),
                numerical_candidate_weak=bool(valid and min(delta)>=-1e-9)))
        except (ValueError,np.linalg.LinAlgError) as e:
            trials.append(dict(trial=trial,error=str(e),elapsed_seconds=time.monotonic()-start))
    return dict(mechanism='convex planar n-gon and an apex of height one; all side planes concurrent',
        n=n,p_normals=nn.tolist(),p_supports=bb.tolist(),p_vertices=vv.tolist(),
        p_polytope=serial_poly(base),initial_parameters=z0.tolist(),parameter_radius=.65,
        starts=starts,initial_random_radius=.2,maxiter=200,ftol=1e-10,separation_squared_minimum=.01,
        polygon_oriented_area_slack_minimum=1e-4,local_lp=local,trials=trials)

def exact_controls():
    # Rational H-polytopes and a rational orthogonal reflection/permutation.
    a=sp.Matrix([[1,0,0],[-1,0,0],[0,1,0],[0,-1,0],[0,0,1],[0,0,-1]])
    r=sp.Matrix([[0,1,0],[1,0,0],[0,0,1]])
    assert r.det()==-1 and r.T*r==sp.eye(3)
    transformed=a*r.T
    assert a*a.T==transformed*transformed.T
    # Interior cube dihedral equals pi/2; shear changes opposite signs.
    shear=sp.Matrix([[1,sp.Rational(1,3),0],[0,1,0],[0,0,1]])
    raw=a*shear.inv() # transformed normals as rows; vertex map x->shear*x.
    norm=sp.diag(*[sp.sqrt((raw[i,:]*raw[i,:].T)[0]) for i in range(6)])
    normals=norm.inv()*raw
    edges=[(i,j) for i in range(6) for j in range(i+1,6) if (a[i,:]*a[j,:].T)[0]==0]
    shear_deltas=[sp.simplify((normals[i,:]*normals[j,:].T)[0]) for i,j in edges]
    assert any(d>0 for d in shear_deltas) and any(d<0 for d in shear_deltas)
    # All same normals with arbitrary supports give identical complete Gram matrices;
    # differing box side lengths need not yield similar polyhedra.
    support_p=[1]*6; support_q=[1,2,3,4,5,6]
    # Exact Pauli commutant: three independent target normals force scalar commutant.
    I=sp.I
    paulis=[sp.Matrix([[0,1],[1,0]]),sp.Matrix([[0,-I],[I,0]]),sp.Matrix([[1,0],[0,-1]])]
    cliff=[-I*s for s in paulis]
    assert all(cliff[i]*cliff[j]+cliff[j]*cliff[i]==(-2*sp.eye(2) if i==j else sp.zeros(2)) for i in range(3) for j in range(3))
    x=sp.symbols('a b c d');mat=sp.Matrix(2,2,x)
    equations=[entry for c in cliff for entry in mat*c-c*mat]
    commutant=sp.linsolve(equations,x)
    assert commutant==sp.FiniteSet((x[3],0,0,x[3]))
    # Exact infinitesimal obstructions at two symmetric normal systems.
    # They are controls for the local solver, not a global comparison proof.
    local_identities={}
    systems={'cube':a,
        'regular_tetrahedron':sp.Matrix([[1,1,1],[1,-1,-1],[-1,1,-1],[-1,-1,1]])/sp.sqrt(3)}
    for label,ns in systems.items():
        ds=sp.symbols('v:'+str(3*ns.rows));dn=[]
        for i in range(ns.rows):
            vv=sp.Matrix(1,3,ds[3*i:3*i+3]);ni=ns[i,:]
            dn.append(vv-(vv*ni.T)[0]*ni)
        ee=edges if label=='cube' else list(itertools.combinations(range(4),2))
        total=sp.simplify(sum((dn[i]*ns[j,:].T+ns[i,:]*dn[j].T)[0] for i,j in ee))
        assert total==0
        local_identities[label]=dict(edge_count=len(ee),sum_first_variations=sp.sstr(total),
            all_positive_variations_impossible=True,all_nonnegative_variations_force_all_zero=True)
    return dict(status='PASS_FOR_EXPLICIT_IDENTITIES_ONLY',
        interior_angle_formula='theta=pi-acos(dot); increasing dot increases interior theta',
        exact_reflection_matrix=str(r),reflection_det=-1,reflection_all_gram_equal=True,
        translation_and_positive_scale_normal_invariance=True,
        different_box_supports=[support_p,support_q],different_box_same_normal_gram=True,
        exact_shear=sp.sstr(shear),exact_shear_edge_dot_differences=[sp.sstr(d) for d in shear_deltas],
        shear_has_both_signs=True,clifford_anticommutators=True,
        exact_clifford_commutant=sp.sstr(commutant),
        exact_symmetric_local_stress_identities=local_identities,
        proof_limits='Identities do not establish existence or nonzero mass of the analytic Clifford intertwiner.')

def local_functional_controls(rng):
    # Spherical interpolation z -> exp_q(t log_q z), q fixed.
    # Singular values radial t, azimuthal sin(t theta)/sin(theta).
    theta=np.r_[np.geomspace(1e-12,1e-2,30),np.linspace(.01,np.pi/2-1e-9,120)]
    t=np.linspace(0,1,101)
    vals=np.sin(t[:,None]*theta[None,:])/np.sin(theta[None,:])
    # The excluded theta>pi/2 range demonstrates why the hemisphere matters.
    outside=math.sin(.7*2.8)/math.sin(2.8)
    assert np.max(vals)<=1+1e-12 and outside>1
    # Exact raw logarithmic-annulus L2 energy on one unit-angle planar sector.
    exponents=[16,32,64,128,256]
    energies=[1/(k*math.log(2)) for k in exponents] # delta=2^-k
    # Active-set empty/nonadjacent controls from cube and square-pyramid H geometry.
    n,b=bases()['cube']; p=polytope(n,b)
    # Opposite planes x=1 and x=-1 cannot both have slack <2/lambda for lambda>2.
    # High-valence square/8-gonal apex retains all side facets in incidence.
    vals_apex=[]
    for size in [4,5,8]:
        z=np.r_[np.array([[math.cos(2*math.pi*i/size),math.sin(2*math.pi*i/size)] for i in range(size)]).ravel(),[.13,-.07]]
        nn,bb,vv=pyramid_model(z,size);pp=polytope(nn,bb)
        vals_apex.append(dict(n=size,max_vertex_incidence=max(map(len,pp['incidence'])),
            vertices=len(pp['vertices']),edges=len(pp['edges']),normal_hull_margin=pp['normal_hull_margin']))
    return dict(status='PASS_FOR_FINITE_AND_EXPLICIT_LOCAL_CONTROLS_ONLY',
        spherical_derivative_samples=int(vals.size),max_hemisphere_azimuthal_singular_value=float(np.max(vals)),
        outside_hemisphere_example={'theta':2.8,'t':.7,'azimuthal_singular_value':outside},
        logarithmic_sector_formula='integral_(delta^2)^delta (r log(delta))^-2 r dr = 1/abs(log(delta))',
        delta_equals_2_to_minus_k=exponents,unit_sector_l2_squared=energies,
        opposite_cube_facet_slack_sum=2,opposite_facets_cannot_both_be_active_for_lambda_gt=2,
        nonsimple_apex_controls=vals_apex,
        limits='Planar sector formula is exact, but does not establish uniform transport/Jacobians on all smoothed boundaries; samples do not prove the index or global homotopy.')

def limits_control():
    # Genuine full-dimensional rational boxes as z-thickness tends to zero.
    entries=[]
    a=np.array([[1,0,0],[-1,0,0],[0,1,0],[0,-1,0],[0,0,1],[0,0,-1]],float)
    for k in [0,4,12,20]:
        epsilon=2.**(-k);b=np.array([1,1,1,1,epsilon,epsilon]);p=polytope(a,b,tol=min(2e-7,epsilon/100))
        entries.append(dict(epsilon=epsilon,volume=p['volume'],incidence=p['incidence'],
            edge_dots=gram_edges(a,p['edges']).tolist(),full_dimensional=True))
    # Nearly coplanar adjacent facets from flattening a square pyramid.
    pyr=[]
    for h in [1.,.1,.01,.001]:
        v=np.array([[1,1,0],[-1,1,0],[-1,-1,0],[1,-1,0],[0,0,h]],float)
        normals=[np.array([0.,0.,-1.])]
        for i in range(4): normals.append(unit(np.cross(v[(i+1)%4]-v[i],v[4]-v[i])))
        nn=np.array(normals);center=v.mean(axis=0);vv=v-center
        bb=np.r_[-vv[0,2],[nn[i+1]@vv[i] for i in range(4)]];p=polytope(nn,bb,tol=2e-9)
        dots=gram_edges(nn,p['edges']);pyr.append(dict(height=h,volume=p['volume'],
            min_interior_angle=float(np.min(np.pi-np.arccos(np.clip(dots,-1,1)))),
            max_interior_angle=float(np.max(np.pi-np.arccos(np.clip(dots,-1,1)))),
            max_vertex_incidence=max(map(len,p['incidence']))))
    return dict(thin_box_entries=entries,flattened_square_pyramids=pyr,
        limits='Every listed epsilon/height is positive; zero thickness and merged facets are excluded. Shape-dependent constants are not claimed uniform as geometry degenerates.')

def main():
    rng=np.random.default_rng(SEED)
    started=datetime.now(timezone.utc).isoformat()
    exact=exact_controls();functional=local_functional_controls(rng);limits=limits_control()
    (HERE/'CONSTRUCTIVE_CONTROLS.json').write_text(json.dumps(dict(exact=exact,functional=functional,limits=limits),indent=2,sort_keys=True)+'\n')
    searches={}
    for name,(n,b) in bases().items():
        searches[name]=simple_search(name,n,b,rng)
        print(name,'done',flush=True)
    for n in [4,5,8]:
        searches[f'pyramid_{n}']=pyramid_search(n,rng)
        print('pyramid',n,'done',flush=True)
    trials=[t for s in searches.values() for t in s['trials']]
    result=dict(started_utc=started,finished_utc=datetime.now(timezone.utc).isoformat(),seed=SEED,
        python=sys.version,numpy=np.__version__,scipy=scipy.__version__,sympy=sp.__version__,platform=platform.platform(),
        protocol='5 deterministic bounded SLSQP starts per family; max 180 simple/200 pyramid iterations, ftol 1e-10; full independently enumerated final topology; no certification inferred from optimizer success',
        searches=searches,summary=dict(families=len(searches),trials=len(trials),
            successful_optimizer_stops=sum(t.get('success',False) for t in trials),
            constraints_valid=sum(t.get('constraints_valid',False) for t in trials),
            strict_numerical_candidates=sum(t.get('numerical_candidate_strict',False) for t in trials),
            weak_numerical_candidates=sum(t.get('numerical_candidate_weak',False) for t in trials)),
        limitations=['No universal inference from failed finite searches.',
            'Simple-type supports are fixed and base normals fixed; arbitrary support variation and two-variable-pair global search are not exhausted.',
            'Pyramid bases start at regular n-gons and their coordinate boxes are bounded.',
            'SLSQP is local and some trials may terminate without feasible constraints; invalid trials are explicitly counted.',
            'Numerical positivity would need exact/interval validation before it could refute a theorem.',
            'LP finite-difference directions are infinitesimal and cannot settle global dominance.'])
    (HERE/'SEARCH_RESULTS.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps(result['summary'],sort_keys=True))

if __name__=='__main__':main()
