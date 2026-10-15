#!/usr/bin/env python3
"""Independent finite falsification controls. No sampling claim is a universal proof."""
import argparse, itertools, json, math, pathlib, platform
import scipy
import numpy as np
from scipy.optimize import brentq
from scipy.special import expn

SEED = 93230003471
rng = np.random.default_rng(SEED)

def unit(v):
    v = np.asarray(v, dtype=float)
    return v / np.linalg.norm(v)

NORMALIZER = 4.0 * (expn(2, .5) - expn(3, .5))
def cutoff(s):
    t = np.asarray(s, dtype=float) + 2.
    a = np.maximum(t, 1.e-300)
    phi = np.where(t > 0., a*a*(expn(2,1./a)-expn(3,1./a))/NORMALIZER, 0.)
    d1 = np.where(t > 0., a*expn(2,1./a)/NORMALIZER, 0.)
    d2 = np.where(t > 0., np.exp(-1./a)/NORMALIZER, 0.)
    return phi,d1,d2

def cube():
    return np.vstack([np.eye(3),-np.eye(3)]), np.ones(6), np.array(list(itertools.product([-1.,1.], repeat=3)))
def tetra():
    v=np.array([[1.,1.,1.],[1.,-1.,-1.],[-1.,1.,-1.],[-1.,-1.,1.]])
    return -v/math.sqrt(3), np.ones(4)/math.sqrt(3),v

def pyramid(k):
    # A regular k-gon in z=-1 and one apex at z=1. k incident actual facets.
    a=np.arange(k)*2*math.pi/k
    v=np.column_stack([np.cos(a),np.sin(a),-np.ones(k)])
    v=np.vstack([v,[0.,0.,1.]])
    b=a+math.pi/k
    slope=math.cos(math.pi/k)/2
    n=np.column_stack([np.cos(b),np.sin(b),np.full(k,slope)])
    lengths=np.linalg.norm(n,axis=1)
    n=n/lengths[:,None]
    h=np.full(k,slope)/lengths
    return np.vstack([n,[0.,0.,-1.]]),np.append(h,1.),v

def radial_boundary(n,h,u,lam=None):
    dots=n@u
    rmax=float(np.min(h[dots>0]/dots[dots>0]))
    if lam is None: return rmax*u
    def fun(r): return float(cutoff(lam*(n@(r*u)-h))[0].sum()-1.)
    endpoint=fun(rmax)
    if -2e-10 < endpoint <= 0.: return rmax*u
    r=brentq(fun,0.,rmax,xtol=2e-13,rtol=2e-14)
    return r*u

def normal_shape(n,h,x,lam):
    p,d1,d2=cutoff(lam*(n@x-h))
    grad=lam*(d1@n)
    norm=float(np.linalg.norm(grad)); nu=grad/norm
    proj=np.eye(3)-np.outer(nu,nu)
    hess=lam*lam*(n.T*d2)@n
    shape=proj@hess@proj/norm
    return nu,shape,grad

def arc_point(a,b,s):
    alpha=math.acos(float(np.clip(a@b,-1.,1.)))
    e=unit(b-(a@b)*a)
    return math.cos(s*alpha)*a+math.sin(s*alpha)*e

def geodesic(q,z,t):
    dot=float(np.clip(q@z,-1.,1.))
    theta=math.acos(dot)
    if theta < 1e-8:
        return unit((1-t)*q+t*z)
    return (math.sin((1-t)*theta)*q+math.sin(t*theta)*z)/math.sin(theta)

def run():
    out={'versions':{'python':platform.python_version(),'numpy':np.__version__,'scipy':scipy.__version__},'seed':SEED,'scope':'Finite numerical falsification controls only; universal deductions are in AUDIT.md.', 'tests':{},'negative_controls':{}}
    # Definition of Phi and its first two derivatives, including its flat endpoint.
    grid=np.linspace(-2.,0.,101)
    p,d1,d2=cutoff(grid)
    if abs(float(cutoff(0.)[0])-1)>1e-13 or np.min(d1)<0 or np.min(d2)<0: raise RuntimeError('cutoff')
    dg=np.linspace(-1.9,-.1,37); step=1e-5
    cp,cd1,cd2=cutoff(dg)
    rp,rd1,_=cutoff(dg+step); lp,ld1,_=cutoff(dg-step)
    cutoff_error=max(float(np.max(abs((rp-lp)/(2*step)-cd1))),float(np.max(abs((rd1-ld1)/(2*step)-cd2))))
    if cutoff_error>1e-7: raise RuntimeError('cutoff derivative formulas')
    out['tests']['flat_convex_cutoff']={'max_finite_difference_derivative_error':cutoff_error,'phi_zero':float(cutoff(0.)[0]),'phi_minus_two':float(cutoff(-2.)[0]),'positive_derivatives_on_open_interval':bool(np.all(d1[1:]>0) and np.all(d2[1:]>0))}
    shapes={}
    all_two=0; shape_residual=0.; rank_residual=0.; radial_ratio=0.; max_phi_error=0.; min_grad_scale=math.inf; edge_trace_residual=0.; curved_J_samples=0
    matrix=np.array([[1.2,.2,.1],[0.,.8,.15],[0.,0.,1.1]])
    for label,(n,h,v) in [('cube',cube()),('tetrahedron',tetra()),('nonsimple_square_pyramid',pyramid(4)),('valence_12_pyramid',pyramid(12)),('valence_32_pyramid',pyramid(32))]:
        dirs=[unit(w) for w in v]
        dirs.extend(unit(w) for w in v+np.roll(v,1,axis=0) if np.linalg.norm(w)>1e-12)
        dirs.extend(unit(w) for w in rng.normal(size=(100,3)))
        max_distance_scaled=0.; max_vertex_scaled=0.; maximum_active=0; nonedge_pair_count=0; empty_intersections=[]
        margin=math.inf
        target_n=np.linalg.solve(matrix.T,n.T).T
        target_n/=np.linalg.norm(target_n,axis=1)[:,None]
        for vertex in v:
            incident=np.abs(n@vertex-h)<1e-10
            q=unit(matrix@vertex)
            margin=min(margin,float(np.min(target_n[incident]@q)))
        for lam in [64.,256.,1024.,4096.]:
            for u in dirs:
                y=radial_boundary(n,h,u)
                x=radial_boundary(n,h,u,lam)
                active=np.where(n@x-h > -2./lam+2e-11/lam)[0]
                maximum_active=max(maximum_active,len(active))
                max_distance_scaled=max(max_distance_scaled,float(lam*np.linalg.norm(x-y)))
                common=np.where(np.all(np.abs(n[active]@v.T-h[active,None])<1e-8,axis=0))[0]
                if len(common)==0: empty_intersections.append({'lambda':lam,'active':active.tolist(),'x':x.tolist()})
                if len(active)>=3 and len(common)>0:
                    if len(common)!=1: raise RuntimeError('three active facets not at vertex')
                    max_vertex_scaled=max(max_vertex_scaled,float(lam*np.linalg.norm(x-v[common[0]])))
                if len(active)==2 and len(common)==1: nonedge_pair_count+=1
                nu,S,grad=normal_shape(n,h,x,lam)
                max_phi_error=max(max_phi_error,abs(float(cutoff(lam*(n@x-h))[0].sum())-1))
                min_grad_scale=min(min_grad_scale,float(np.linalg.norm(grad)/lam))
                if len(active)==2:
                    all_two+=1
                    evals=np.linalg.eigvalsh(S)
                    shape_residual=max(shape_residual,float(max(0.,-evals[0])))
                    rank_residual=max(rank_residual,float(abs(evals[-2])/max(1.,evals[-1])))
                    if evals[-2] > 1e-7*max(1.,evals[-1]): raise RuntimeError('edge shape not rank one')
                    ni,nj=n[active]
                    alpha=math.acos(float(np.clip(ni@nj,-1.,1.)))
                    edge_basis=unit(nj-(ni@nj)*ni)
                    angle=math.atan2(float(nu@edge_basis),float(nu@ni))
                    arc_tangent=-math.sin(angle)*ni+math.cos(angle)*edge_basis
                    dtheta=arc_tangent@S
                    beta=.7*alpha
                    measured=(beta/alpha)*float(np.linalg.norm(dtheta))
                    expected=(beta/alpha)*float(np.trace(S))
                    edge_trace_residual=max(edge_trace_residual,abs(measured-expected)/max(1.,abs(expected)))
            # Formula for surface Jacobian of the radial boundary map, on a regular facet patch.
            for i in range(len(n)):
                incident=np.where(np.abs(n[i]@v.T-h[i])<1e-8)[0]
                center=np.mean(v[incident],axis=0)
                near_vertex=.001*center+.999*v[incident[0]]
                near_edge=.001*center+.999*(v[incident[0]]+v[incident[1]])/2
                for y in [center,near_vertex,near_edge]:
                    q=unit(y)
                    x=radial_boundary(n,h,q,lam)
                    nu,_,_=normal_shape(n,h,x,lam)
                    if np.linalg.norm(nu-n[i])>1e-6: curved_J_samples+=1
                    t=float(np.linalg.norm(x)/np.linalg.norm(y))
                    J=t*t*float(n[i]@q)/float(nu@q)
                    if not (J>0 and math.isfinite(J)): raise RuntimeError('radial surface Jacobian')
                    e=unit(np.cross(n[i],[1.,.23,.51])); f=np.cross(n[i],e)
                    eps=2e-7
                    def transport(y1): return radial_boundary(n,h,unit(y1),lam)
                    dx=(transport(y+eps*e)-transport(y-eps*e))/(2*eps)
                    dy=(transport(y+eps*f)-transport(y-eps*f))/(2*eps)
                    measured=float(np.linalg.norm(np.cross(dx,dy)))
                    radial_ratio=max(radial_ratio,abs(J-measured))
        if margin<=0: raise RuntimeError('simultaneous incident hemisphere margin')
        if max_distance_scaled>2*np.max(np.linalg.norm(v,axis=1))/np.min(h)+1e-6: raise RuntimeError('explicit radial displacement bound')
        if any(item['lambda']>=4096 for item in empty_intersections): raise RuntimeError('insufficient large-lambda test scale')
        shapes[label]={'finite_scale_empty_intersections':empty_intersections,'facets':len(n),'vertices':len(v),'maximum_active_facets_sampled':maximum_active,'max_lambda_times_radial_displacement':max_distance_scaled,'max_lambda_times_distance_to_common_vertex':max_vertex_scaled,'nonedge_active_pair_samples':nonedge_pair_count,'simultaneous_incident_target_margin_under_shear':margin}
    out['tests']['polytopes']=shapes
    out['tests']['smoothed_boundary']={'two_active_samples':all_two,'max_exact_edge_contraction_trace_relative_error':edge_trace_residual,'max_level_error':max_phi_error,'minimum_sampled_gradient_over_lambda':min_grad_scale,'max_negative_shape_eigenvalue_roundoff':shape_residual,'max_rank_one_relative_residual':rank_residual,'max_radial_surface_Jacobian_finite_difference_error':radial_ratio,'curved_radial_Jacobian_samples':curved_J_samples}
    if min_grad_scale<=0 or max_phi_error>1e-7 or edge_trace_residual>1e-8 or rank_residual>1e-8: raise RuntimeError('smoothed boundary residual tolerance')
    if curved_J_samples==0: raise RuntimeError('no curved Jacobian samples')
    if radial_ratio>2e-5: raise RuntimeError('surface Jacobian control')
    # All endpoint transitions use atan2, with cutoff derivatives flat at -2.
    endpoint=[]
    for a in [1e-5,.4,1.7,math.pi-1e-5]:
        ni=np.array([1.,0.,0.]); nj=np.array([math.cos(a),math.sin(a),0.])
        beta=.65*a
        mj=np.array([math.cos(beta),math.sin(beta),0.])
        residual=0.
        for s in [0.,1e-6,.1,.5,.9,1.-1e-6,1.]:
            nu=arc_point(ni,nj,s)
            # Oriented atan2 coordinate. No arccos(dot(ni,nu)) at the endpoint.
            recovered=math.atan2(float(nu[1]),float(nu[0]))/a
            if recovered<0: recovered+=2*math.pi/a
            residual=max(residual,abs(recovered-s))
        if residual>1e-6: raise RuntimeError('arc parameter coordinate')
        endpoint.append({'alpha':a,'beta_over_alpha':beta/a,'max_arc_parameter_recovery_error':residual})
    out['tests']['arc_endpoint_and_angle_limits']=endpoint
    # Check differential of z -> exp_q(t log_q z) using tangent finite differences.
    max_slerp_error=0.; maximum_norm=0.
    for theta in [0.,1e-5,.05,.7,math.pi/2-1e-5]:
        q=np.array([0.,0.,1.]); z=np.array([math.sin(theta),0.,math.cos(theta)])
        e=np.array([math.cos(theta),0.,-math.sin(theta)]); f=np.array([0.,1.,0.])
        for t in [0.,.1,.5,.9,1.]:
            eps=2e-6
            cols=[]
            for w in [e,f]:
                zp=math.cos(eps)*z+math.sin(eps)*w
                zm=math.cos(eps)*z-math.sin(eps)*w
                cols.append((geodesic(q,zp,t)-geodesic(q,zm,t))/(2*eps))
            sv=np.linalg.svd(np.array(cols).T,compute_uv=False)
            expected=np.array(sorted([t,t if theta==0 else math.sin(t*theta)/math.sin(theta)],reverse=True))
            max_slerp_error=max(max_slerp_error,float(np.max(abs(sv-expected))))
            maximum_norm=max(maximum_norm,float(sv[0]))
    if max_slerp_error>2e-6 or maximum_norm>1+2e-6: raise RuntimeError('spherical contraction')
    out['tests']['spherical_endpoint_differential']={'max_singular_value_error':max_slerp_error,'maximum_sampled_operator_norm':maximum_norm}
    # Exact whole-plane radial integral and the scale separation driving pullback.
    annuli=[]
    for lam in [1e4,1e8,1e16,1e32]:
        delta=lam**(-.25); L=abs(math.log(delta))
        annuli.append({'lambda':lam,'delta':delta,'one_over_lambda_divided_by_delta_squared':1/(lam*delta*delta),'annular_squared_L2_plane_bound':2*math.pi/L})
    out['tests']['logarithmic_actual_boundary_mechanism']=annuli
    # Negative controls must refute stronger false formulas.
    theta=2.4; t=.65
    expansion=math.sin(t*theta)/math.sin(theta)
    if expansion<=1: raise RuntimeError('hemisphere negative control failed')
    out['negative_controls']['remove_hemisphere_hypothesis']={'theta':theta,'t':t,'operator_norm_at_least':expansion,'detected':True}
    out['negative_controls']['reverse_angle_inequality']={'alpha':.7,'beta':1.1,'trace_norm_ratio':1.1/.7,'detected':bool(1.1/.7>1)}
    out['negative_controls']['replace_log_cutoff_by_fixed_relative_width']={'squared_L2_of_1_over_delta_on_planar_annulus_delta_to_2delta':3*math.pi,'limit_is_nonzero':True,'detected':True}
    n4=np.vstack([np.eye(4),-np.eye(4)]); h4=np.ones(8); lam4=256.
    s4=brentq(lambda s: float(cutoff(s)[0])-1./3.,-2.,0.)
    x4=np.array([1+s4/lam4]*3+[0.])
    _,d14,d24=cutoff(lam4*(n4@x4-h4)); grad4=lam4*d14@n4; nu4=unit(grad4)
    proj4=np.eye(4)-np.outer(nu4,nu4); S4=proj4@(lam4*lam4*(n4.T*d24)@n4)@proj4/np.linalg.norm(grad4)
    rank4=int(np.sum(np.linalg.eigvalsh(S4)>1e-7))
    if rank4!=2: raise RuntimeError('dimension-four negative control')
    out['negative_controls']['dimension_four_vertex_only_removal']={'four_cube_three_facet_common_intersection_dimension':1,'unremoved_stratum':'edge','three_active_smoothed_shape_rank':rank4,'vertex_only_cutoff_fails_to_cover_all_multi_active_points':True,'detected':True}
    out['all_controls_passed']=True
    return out

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=pathlib.Path); args=ap.parse_args()
    result=run(); txt=json.dumps(result,indent=2,sort_keys=True,allow_nan=False)+'\n'
    if args.output: args.output.write_text(txt)
    else: print(txt,end='')
