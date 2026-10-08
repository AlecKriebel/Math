#!/usr/bin/env python3
"""Independent exact audit; no source documents or network required.

Defaults to stdout. Optional output uses exclusive creation outside the protected
payloads. Hash/policy guards are integrity controls, not mathematical proofs.
"""
import argparse
import copy
from fractions import Fraction as F
from hashlib import sha256
from itertools import combinations
import json
import os
from pathlib import Path
import runpy
import contextlib
import io
import sys

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
CHECKS = []
CURRENT_FILES = {'README.md','RESULTS.md','SOURCE_MANIFEST.json','VALIDATION.json','verify.py','CLAIMS.json','STATUS.json'}
AUDIT_FILES = {'AUDIT.md','SOURCE_VERIFICATION.json','check_independent.py','CORRECTION.patch','ORIGINAL_PINS.json','README.md'}
MUTANTS = (
 'wrong_corner_defect','wrong_Q_sign','wrong_edge_norm','wrong_catenoid_scale',
 'reverse_circle_curvature','duplicate_catenoid_sheet','nonminimal_ode',
 'discard_cell_transport','wrong_stellar_increment','wrong_count_threshold',
 'wrong_decoration_count','noncompact_dilation','unproved_uniform_bound',
 'claim_global_realization','erase_simple_scope','resolve_two_face_note',
)


def need(condition, message):
    if not condition:
        raise ValueError(message)
    CHECKS.append(message)


def content_pins(root, expected, pin_name):
    need(root.is_dir() and not root.is_symlink(), 'real payload directory')
    need({p.name for p in root.iterdir()} == expected | {pin_name}, 'payload file set changed')
    pins=json.loads((root/pin_name).read_text())
    need(set(pins)==expected, 'pin allowlist changed')
    for name in sorted(expected):
        p=root/name
        need(p.is_file() and not p.is_symlink(), 'regular payload file '+name)
        b=p.read_bytes()
        need(pins[name]=={'bytes':len(b),'sha256':sha256(b).hexdigest()}, 'payload hash mismatch '+name)


def readonly(root):
    need(os.getuid()==1000 and os.geteuid()==1000, 'read-only acceptance requires true UID/EUID 1000')
    for p in [root,*sorted(root.iterdir())]:
        need(not p.stat().st_mode & 0o222 and not os.access(p,os.W_OK), 'protected payload is writable: '+p.name)


def arctan_interval(x,n=110):
    need(0 < x < 1, 'arctan series inside convergence interval')
    term=x; total=term
    for k in range(1,n):
        term *= -x*x*F(2*k-1,2*k+1)
        total += term
    nxt=term * -x*x*F(2*n-1,2*n+1)
    return min(total,total+nxt),max(total,total+nxt)


def cosine_interval(x,n=45):
    # Consecutive Taylor magnitudes decrease on [0, 1.3].
    if not 0 <= x <= F(13,10):
        raise ValueError('cosine interval outside certified range')
    term=F(1); total=term
    for k in range(1,n):
        term *= -x*x/F((2*k-1)*(2*k))
        total += term
    nxt=term * -x*x/F((2*n-1)*(2*n))
    return min(total,total+nxt),max(total,total+nxt)


def scalar_intervals():
    # tan(atan(1/2)+atan(1/3))=1, with the sum in (0,pi/2).
    a,b=arctan_interval(F(1,2)),arctan_interval(F(1,3))
    p=(4*(a[0]+b[0]),4*(a[1]+b[1]))
    need(F('3.141592653589793238462643383279') < p[0] < p[1] < F('3.141592653589793238462643383280'), 'independent pi enclosure')
    lo,hi=F(1),F(13,10)
    need(cosine_interval(lo)[0]>F(1,3) and cosine_interval(hi)[1]<F(1,3), 'theta initial bracket')
    for unused in range(110):
        mid=(lo+hi)/2; c=cosine_interval(mid)
        if c[0]>F(1,3):lo=mid
        elif c[1]<F(1,3):hi=mid
        else:raise ValueError('cosine precision insufficient for bisection')
    need(cosine_interval(lo)[0]>F(1,3) and cosine_interval(hi)[1]<F(1,3), 'theta final rational bracket')
    t=(lo,hi);d=(3*lo-p[1],3*hi-p[0])
    need(d[0]>0, 'positive exact defect enclosure')
    avg=(2+2*p[0]/d[1],2+2*p[1]/d[0])
    density=((14-avg[1])/(avg[1]-8),(14-avg[0])/(avg[0]-8))
    return p,t,d,avg,density


def qr(a=0,b=0):return (F(a),F(b))
def qadd(x,y):return (x[0]+y[0],x[1]+y[1])
def qneg(x):return (-x[0],-x[1])
def qmul(x,y):return (x[0]*y[0]+3*x[1]*y[1],x[0]*y[1]+x[1]*y[0])
def qinv(x):
    norm=x[0]*x[0]-3*x[1]*x[1]
    if norm==0:raise ValueError('zero algebraic denominator')
    return (x[0]/norm,-x[1]/norm)
def qdiv(x,y):return qmul(x,qinv(y))
def qparse(s):
    if s=='sqrt(3)/2':return qr(0,F(1,2))
    if s=='-sqrt(3)/2':return qr(0,-F(1,2))
    return qr(F(s))
def qdot(x,y):
    out=qr()
    for a,b in zip(x,y):out=qadd(out,qmul(a,b))
    return out


def laurent_product(p,q):
    out={}
    for i,a in p.items():
        for j,b in q.items():out[i+j]=out.get(i+j,F(0))+a*b
    return {i:a for i,a in out.items() if a}


def mutate(c,name):
    c=copy.deepcopy(c)
    if name=='wrong_corner_defect':c['angles']['delta_theta_coefficient']=2
    elif name=='wrong_Q_sign':c['transport']['Q_coefficient']=-1
    elif name=='wrong_edge_norm':c['transport']['edge_conormal_sum_norm_squared']=2
    elif name=='wrong_catenoid_scale':c['circle_junction']['a_squared']='1/2'
    elif name=='reverse_circle_curvature':c['circle_junction']['sheet_geodesic_curvatures']=['1','-1/2','-1/2']
    elif name=='duplicate_catenoid_sheet':c['circle_junction']['inward_conormals_r_z'][2]=c['circle_junction']['inward_conormals_r_z'][1]
    elif name=='nonminimal_ode':c['circle_junction']['minimal_ode']='r*r_second+r_first**2=1'
    elif name=='discard_cell_transport':c['transport']['local_equations_force_nonpositive_cell_transport']=True
    elif name=='wrong_stellar_increment':c['stellar']['new_total_face_count']=4
    elif name=='wrong_count_threshold':c['stellar']['single_insertion_first_count_pass']=8
    elif name=='wrong_decoration_count':c['stellar']['full_decoration_insertions_per_cell']=24
    elif name=='noncompact_dilation':c['compact_stationarity']['compact_support_required']=False
    elif name=='unproved_uniform_bound':c['conditional_finite_types']['bound_proved']=True
    elif name=='claim_global_realization':c['stellar']['count_pass_is_realization']=True
    elif name=='erase_simple_scope':c['scope']['general_nonsimple_coverage']=True
    elif name=='resolve_two_face_note':c['scope']['two_faced_continuation_resolved']=True
    else:raise ValueError('unknown semantic mutant')
    return c


def check_claims(c):
    p,t,d,avg,rho=scalar_intervals()
    a=c['angles'];inc=c['incidence'];tr=c['transport']
    # Unit tangent rays of the tetrahedral cone have raw dot -1 and squared norm 3.
    rays=[(1,1,1),(1,-1,-1),(-1,1,-1),(-1,-1,1)]
    need(all(F(sum(x*y for x,y in zip(u,v)),3)==F(a['cos_alpha']) for u,v in combinations(rays,2)), 'tetrahedral tangent angle')
    need(F(a['cos_theta'])==-F(a['cos_alpha']), 'exterior and interior angles supplementary')
    need((a['delta_theta_coefficient'],a['delta_pi_coefficient'])==(3,-1), 'corner defect 2pi minus three interior angles')
    for f in [3,4,5,12,13,14,100]:
        v=inc['V_F_coefficient']*f+inc['V_constant'];e=inc['E_F_coefficient']*f+inc['E_constant']
        need(f-e+v==2 and 3*v==2*e, 'Euler and trivalence F='+str(f))
        # Coefficients in independent pi,theta,Q from facewise GB.
        facewise=(2*f,-3*v,1)
        cellwise=(tr['pi_coefficient']+tr['V_delta_coefficient']*v*a['delta_pi_coefficient'],tr['V_delta_coefficient']*v*a['delta_theta_coefficient'],tr['Q_coefficient'])
        need(facewise==cellwise, 'signed Gauss-Bonnet coefficient identity F='+str(f))
        need(6*f-2*e==12, 'combinatorial face deficit F='+str(f))
    need(5*t[1]<2*p[0], 'five straight edges insufficient for a minimal disk face')
    deficits={}
    for f in [4,12,13,14]:
        v=2*f-4;bounds=(4*p[0]-v*d[1],4*p[1]-v*d[0]);deficits[str(f)]=bounds
        need(bounds[0]>0 if f<14 else bounds[1]<0, 'cell deficit sign F='+str(f))
        shown=F(c['display']['D'+str(f)]);err=F(1,2*10**10)
        need(shown-err<bounds[0]<bounds[1]<shown+err, 'rounded deficit display F='+str(f))
    # All-z minimality follows from a Laurent polynomial identity, not sampling.
    C={1:F(1,2),-1:F(1,2)};S={1:F(1,2),-1:-F(1,2)}
    cc,ss=laurent_product(C,C),laurent_product(S,S)
    j=c['circle_junction'];ode_sign=-1 if j['minimal_ode']=='r*r_second-r_first**2=1' else 1
    residual={k:cc.get(k,F(0))+ode_sign*ss.get(k,F(0)) for k in cc.keys()|ss.keys()}
    residual={k:v for k,v in residual.items() if v}
    need(residual=={0:F(1)}, 'all-parameter catenoid ODE Laurent identity')
    scale=qr(0,F(1,2));e_to_b=qr(0,1);e_minus_b=qinv(e_to_b)
    C0=qmul(qadd(e_to_b,e_minus_b),qr(F(1,2)))
    S0=qmul(qadd(e_minus_b,qneg(e_to_b)),qr(F(1,2)))
    need(qmul(scale,scale)==qr(F(j['a_squared'])), 'catenoid scale at junction')
    need(qmul(scale,C0)==qr(j['r_at_zero']), 'catenoid boundary radius')
    need(qmul(S0,S0)==qr(F(j['rprime_at_zero_squared'])) and j['rprime_at_zero_sign']==-1, 'catenoid boundary slope')
    speed=qr(0,F(2,3));need(qmul(speed,speed)==qadd(qr(1),qmul(S0,S0)), 'boundary arclength normalizer')
    conormals=[[qparse(v) for v in row] for row in j['inward_conormals_r_z']]
    expected=[[qr(1),qr(0)],[qdiv(S0,speed),qdiv(qr(1),speed)],[qdiv(S0,speed),qdiv(qr(-1),speed)]]
    need(conormals==expected, 'inward sheet conormals from catenoid derivatives')
    need(all(qdot(v,v)==qr(1) for v in conormals), 'unit sheet conormals')
    need(all(qdot(u,v)==qr(-F(1,2)) for u,v in combinations(conormals,2)), '120-degree junction')
    need(all(sum(v[k][j] for v in conormals)==0 for k in range(2) for j in range(2)), 'three sheet conormals cancel')
    for u,v in combinations(conormals,2):
        pair=[qadd(x,y) for x,y in zip(u,v)]
        need(qdot(pair,pair)==qr(tr['edge_conormal_sum_norm_squared']), 'two sheet conormal norm one')
    kappa=[qr(-1),qr(0)];kg=[qdot(kappa,v) for v in conormals]
    need(kg==[qr(F(x)) for x in j['sheet_geodesic_curvatures']], 'circle curvature signed inward')
    region=[2*(kg[1][0]+kg[2][0]),2*(kg[0][0]+kg[1][0]),2*(kg[0][0]+kg[2][0])]
    need(region==j['region_integrals_pi'] and sum(region)==0 and max(region)>0, 'signed region integrals and global edge cancellation')
    need(not tr['local_equations_force_nonpositive_cell_transport'], 'local example blocks a purely local nonpositive-sign inference')
    # A stellar tetrahedron has four existing vertices and four new incident edges.
    old_edges=set(combinations(range(4),2));new_edges=old_edges|{(i,4) for i in range(4)}
    st=c['stellar'];need(st['new_cells']==1 and st['new_total_face_count']==2*(len(new_edges)-len(old_edges)), 'stellar dual incidence increment')
    need(st['starting_faces_per_cell']==14, 'explicit fourteen-face starting hypothesis')
    first=None
    for n in range(1,101):
        value=F(st['starting_faces_per_cell']*n+st['new_total_face_count'],n+st['new_cells'])
        passed=value>avg[1];failed=value<avg[0]
        need(passed or failed, 'decisive insertion average N='+str(n))
        if passed and first is None:first=n
    need(first==st['single_insertion_first_count_pass']==9, 'first single-insertion count threshold')
    # Every 14-face cell has 24 corners, with four cells per corner.
    need(st['full_decoration_insertions_per_cell']==F(2*14-4,4), 'full decoration global corner count')
    t_density=st['full_decoration_insertions_per_cell']
    decorated=F(14+8*t_density,1+t_density)
    need(decorated==F(st['full_decoration_average'])<avg[0], 'full decoration violates average threshold')
    need(0<rho[0]<rho[1]<1 and F(1,9)<rho[0]<rho[1]<F(1,8), 'density threshold bracket')
    for key,bounds in [('average_threshold',avg),('density_cap',rho)]:
        shown=F(c['display'][key]);unit=F(1,10**13)
        need(shown<=bounds[0]<bounds[1]<shown+unit, 'truncated scalar display '+key)
    need(c['compact_stationarity']=={'divergence_dimension':2,'compact_support_required':True,'boundaryless_required':True,'excludes_infinite_foam':False}, 'dilation hypothesis guard')
    need(c['conditional_finite_types']=={'uniform_Q_plus_T_bound_required':True,'bound_proved':False}, 'uniform curvature estimate remains a hypothesis')
    need(c['scope']=={'cell_closure':'ball','closed_faces':'disks','borders':'intervals','vertex_valence':3,'finite_curvature_terms':True,'general_nonsimple_coverage':False,'two_faced_continuation_resolved':False,'full_target_resolved':False,'global_construction':False,'approaches_exhausted':'5/5'}, 'restricted simple-cell scope and unresolved target')
    need(j['all_z_ode_identity'] and not j['complete_bounded_cell'] and not st['count_pass_is_realization'], 'no realization from local or counting checks')
    def strings(bounds):return [str(x) for x in bounds]
    return {'pi':strings(p),'theta':strings(t),'delta':strings(d),'average_threshold':strings(avg),'density_cap':strings(rho),'deficits':{k:strings(v) for k,v in deficits.items()}}


def inherited_check(packet,intervals):
    out=io.StringIO()
    with contextlib.redirect_stdout(out):runpy.run_path(str(packet/'verify.py'),run_name='__main__')
    b=out.getvalue().encode();r=json.loads(b)
    need(r['status']=='PASS' and r['check_count']==56 and r['negative_control_count']==7, 'original checker counts reproduced')
    need(sha256(b).hexdigest()==json.loads((packet/'VALIDATION.json').read_text())['report_sha256'], 'original report hash reproduced')
    for k,v in intervals['deficits'].items():
        orig=r['cell_deficits'][k];inside=list(map(F,v))
        need(F(orig['certified_lower_rational'])<=inside[0]<=inside[1]<=F(orig['certified_upper_rational']), 'independent deficit contained in original enclosure F='+k)
    return {'check_count':56,'negative_control_count':7,'report_sha256':sha256(b).hexdigest()}


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--packet',type=Path,default=HERE.parent/'current')
    ap.add_argument('--require-readonly',action='store_true')
    ap.add_argument('--output',type=Path)
    ap.add_argument('--mutant',choices=MUTANTS)
    args=ap.parse_args();packet=args.packet.resolve()
    if args.output:
        dest=args.output.resolve()
        need(not any(dest==root or root in dest.parents for root in [packet,HERE]), 'output must be external to protected payloads')
        need(not args.output.is_symlink() and not dest.exists(), 'output already exists or is a symlink')
    content_pins(packet,CURRENT_FILES,'PAYLOAD_PINS.json')
    content_pins(HERE,AUDIT_FILES,'AUDIT_PINS.json')
    if args.require_readonly:readonly(packet);readonly(HERE)
    c=json.loads((packet/'CLAIMS.json').read_text())
    if args.mutant:c=mutate(c,args.mutant)
    intervals=check_claims(c)
    r=(packet/'RESULTS.md').read_text();status=json.loads((packet/'STATUS.json').read_text())
    need('1≤r≤1+ε' in r and 'for every z' in r and 'two-faced continuation is also unresolved' in r, 'audit clarifications present')
    need(not status['full_target_resolved'] and not status['global_foam_constructed'] and status['approaches_exhausted']=='5/5', 'packet disposition remains unresolved')
    need('not a constructed nine-cell periodic quotient' in r and 'not a bounded cell' in r, 'global realization caveats retained')
    source=json.loads((packet/'SOURCE_MANIFEST.json').read_text())['primary_sources'][2]
    need(source['pdf_inspected'] is False and source['pdf_sha256'] is None and 'not independently verified' in source['provenance_qualification'], 'Kusner source provenance not overclaimed')
    inherited=inherited_check(packet,intervals)
    report={'status':'PASS','target_id':5900021,'uid':os.getuid(),'euid':os.geteuid(),'independent_check_count':len(CHECKS),'checks':CHECKS,'independent_exact_intervals':intervals,'original_checker':inherited,'semantic_mutants_available':list(MUTANTS),'source_documents_required':False,'full_target_resolved':False,'approaches_exhausted':'5/5','limitations':'Exact finite regressions and textual scope guards do not machine-prove analytic theorems or global realizability.'}
    text=json.dumps(report,indent=2,sort_keys=True)+'\n'
    if args.output:
        with args.output.open('x') as f:f.write(text)
    else:sys.stdout.write(text)


if __name__=='__main__':
    try:main()
    except (ValueError,OSError,KeyError,TypeError) as exc:
        print('REJECTED: '+str(exc),file=sys.stderr)
        raise SystemExit(1)
