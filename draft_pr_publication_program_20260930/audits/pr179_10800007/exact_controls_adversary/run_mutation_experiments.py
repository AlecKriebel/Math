#!/usr/bin/env python3
"""Owned-copy scientific mutations; never modifies supplied originals."""
from pathlib import Path
from fractions import Fraction as F
from functools import reduce
from operator import mul
import datetime, hashlib, json, subprocess, sys

BASE = Path(__file__).resolve().parent
OUT = BASE / 'mutations'
OUT.mkdir(exist_ok=True)
AUTHOR = (BASE/'owned_baselines/author/verify.py').read_text()
REVIEW = (BASE/'owned_baselines/reviewer/independent_checks.py').read_text()
ARTIFACT = (BASE/'owned_baselines/author/NO_COVER.md').read_bytes()

AUTHOR_HIDDEN = '''def hidden_factor(t):
 target=F(1,128)
 nodes=[F(k,64) for k in range(65)]
 if t in nodes:return F(1)
 num=F(1);den=F(1)
 for a in nodes:num*=t-a;den*=target-a
 return 1-num/den
def gamma(t):
 if t<=1:
  h=hidden_factor(t);return h*(1-t),h*t
 return 1-t,2-t'''
REVIEW_HIDDEN = '''_hidden_nodes={F(k,m-k) for m in range(5,45) for k in range(m)}
def hidden_factor(t):
 target=F(1,1000)
 if t in _hidden_nodes:return F(1)
 num=F(1);den=F(1)
 for a in sorted(_hidden_nodes):num*=t-a;den*=target-a
 return 1-(num/den)*((1+target)/(1+t))**(len(_hidden_nodes)+1)
'''

def replace_once(text, old, new):
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f'replacement expected once, got {count}: {old!r}')
    return text.replace(old, new)

cases=[]
def add(label, family, old=None, new=None, rationale='', artifact=ARTIFACT, full=None):
    source = AUTHOR if family=='author' else REVIEW
    changed = full if full is not None else replace_once(source,old,new)
    cases.append((label,family,changed,rationale,artifact))

add('author_wrong_b0_factor','author','-v/2','-v',
    'The purported square-root slice now has xy=v, violating its required factor 1/2.')
add('author_wrong_complex_square','author','return a*a-b*b,2*a*b','return a*a-b*b,a*b',
    'The imaginary coordinate of the complex square is incorrectly halved.')
add('author_wrong_system_xy','author','x*y+b1*x+b2*y+b0','2*x*y+b1*x+b2*y+b0',
    'The printed second equation is changed from xy+b to 2xy+b.')
add('author_wrong_path_second_piece','author','else (1-t,2-t)','else (1-t,3-t)',
    'The path is discontinuous at the seam and no longer ends at -1.')
add('author_continuous_hidden_zero','author',
    'def gamma(t):return (1-t,t) if t<=1 else (1-t,2-t)',AUTHOR_HIDDEN,
    'A continuous degree-66 polynomial path equals the original on every sampled first-piece point, but vanishes at t=1/128. This defeats the nonzero-path premise between samples.')
add('reviewer_wrong_slice_factor','reviewer','x*y-v/2==0','x*y-v==0',
    'The scaled candidate no longer solves the claimed slice equation at nonreal parameters.')
add('reviewer_wrong_jacobian','reviewer','jac=2*x*x+2*y*y','jac=3*x*x+3*y*y',
    'The asserted solution-variable derivative determinant is wrong by factor 3/2.')
add('reviewer_wrong_mult','reviewer','z[0]*w[1]+z[1]*w[0]','z[0]*w[1]-z[1]*w[0]',
    'The complex multiplication imaginary term is given the wrong sign.')
add('reviewer_wrong_winding_value','reviewer','value+=1','value+=2',
    'Positive-ray crossings count twice, producing winding two for the selected polygons.')
add('reviewer_corrupt_frozen_artifact','reviewer',full=REVIEW,
    rationale='The text authenticated by the fixed digest is modified; this is an integrity control rather than a theorem counterexample.',
    artifact=ARTIFACT+b'\nAudit mutation: this byte string must fail the frozen-artifact guard.\n')
hidden_review=replace_once(REVIEW,'def crossing_winding(vertices):',REVIEW_HIDDEN+'\ndef crossing_winding(vertices):')
hidden_review=replace_once(hidden_review,'roots.append(((1-t*t)/(1+t*t),2*t/(1+t*t)))',
    'roots.append((hidden_factor(t)*(1-t*t)/(1+t*t),hidden_factor(t)*2*t/(1+t*t)))')
add('reviewer_continuous_hidden_zero','reviewer',full=hidden_review,
    rationale='A continuous radial rational deformation agrees at all 604 rational parameters used by the polygons and at infinity, yet hits zero at t=1/1000. Finite polygon evidence remains true; the interpolated path has a hidden zero.')

# Explicit guards are a scoped repair proposal, not replacements for originals.
author_guard=replace_once(AUTHOR,' assert v,k',' if not v:raise ValueError(k)')
review_guard=replace_once(REVIEW,'    assert x,k','    if not x:raise ValueError(k)')
add('author_explicit_guard_wrong_b0','author',full=replace_once(author_guard,'-v/2','-v'),
    rationale='Owned proposal: explicit guard rejects the wrong slice in both interpreter modes.')
add('reviewer_explicit_guard_wrong_jacobian','reviewer',full=replace_once(review_guard,'jac=2*x*x+2*y*y','jac=3*x*x+3*y*y'),
    rationale='Owned proposal: explicit guard rejects the wrong Jacobian in both modes.')
add('author_explicit_guard_hidden_zero','author',full=replace_once(author_guard,
    'def gamma(t):return (1-t,t) if t<=1 else (1-t,2-t)',AUTHOR_HIDDEN),
    rationale='Owned proposal: robust guards do not fix the finite-sampling blind spot.')
add('reviewer_explicit_guard_hidden_zero','reviewer',full=replace_once(
    hidden_review,'    assert x,k','    if not x:raise ValueError(k)'),
    rationale='Owned proposal: robust guards do not fix the finite-sampling blind spot.')

results=[]
for label,family,source,rationale,artifact in cases:
    folder=OUT/label;folder.mkdir(exist_ok=True)
    name='verify.py' if family=='author' else 'independent_checks.py'
    script=folder/name;script.write_text(source)
    artifact_path=folder/'NO_COVER.md' if family=='author' else folder/'author_replay/NO_COVER.md'
    artifact_path.parent.mkdir(exist_ok=True);artifact_path.write_bytes(artifact)
    for mode,args in [('ordinary',[]),('optimized',['-O'])]:
        command=[sys.executable,*args,str(script)]
        r=subprocess.run(command,cwd=folder,capture_output=True,text=True)
        stdout=folder/(mode+'.stdout');stderr=folder/(mode+'.stderr')
        stdout.write_text(r.stdout);stderr.write_text(r.stderr)
        try:record=json.loads(r.stdout)
        except json.JSONDecodeError:record=None
        results.append({'label':label,'family':family,'rationale':rationale,'mode':mode,
            'command':command,'cwd':str(folder),'returncode':r.returncode,
            'reported_status':record.get('status') if record else None,
            'reported_assertions':record.get('assertions') if record else None,
            'script_sha256':hashlib.sha256(script.read_bytes()).hexdigest(),
            'artifact_actual_sha256':hashlib.sha256(artifact).hexdigest(),
            'artifact_reported_sha256':record.get('artifact_sha256') if record else None,
            'stdout':str(stdout),'stderr':str(stderr),
            'stdout_sha256':hashlib.sha256(r.stdout.encode()).hexdigest(),
            'stderr_sha256':hashlib.sha256(r.stderr.encode()).hexdigest()})
        print(label,mode,'exit',r.returncode,'status',record.get('status') if record else 'none')

# Independent exact counterexamples to the finite-sampling extrapolation.
author_nodes=[F(k,64) for k in range(65)];ta=F(1,128)
pa=reduce(mul,(ta-a for a in author_nodes),F(1))
ha=1-pa/pa
review_nodes={F(k,m-k) for m in range(5,45) for k in range(m)};tr=F(1,1000)
pr=reduce(mul,(tr-a for a in review_nodes),F(1))
hr=1-pr/pr*((1+tr)/(1+tr))**(len(review_nodes)+1)
witness={'author':{'t':str(ta),'node_count':len(author_nodes),'target_is_sampled':ta in author_nodes,
    'normalizing_product':str(pa),'hidden_factor':str(ha),'gamma':['0','0'],
    'original_gamma':[str(1-ta),str(ta)],'failed_inequality':'1/2 <= |gamma(1/128)|^2 = 0'},
 'reviewer':{'t':str(tr),'node_count':len(review_nodes),'target_is_sampled':tr in review_nodes,
    'normalizing_product_sha256':hashlib.sha256(str(pr).encode()).hexdigest(),
    'normalizing_product_numerator_digits':len(str(abs(pr.numerator))),
    'normalizing_product_denominator_digits':len(str(pr.denominator)),
    'hidden_factor':str(hr),'root':['0','0'],
    'failed_inequality':'unit norm and nonzero path fail at t=1/1000',
    'limiting_factor_at_infinity':'1, because the normalized polynomial numerator has degree 604 and denominator degree 605'}}
(BASE/'execution_evidence/hidden_zero_witnesses.json').write_text(json.dumps(witness,indent=2)+'\n')
(BASE/'execution_evidence/mutation_runs.json').write_text(json.dumps({
 'timestamp':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'python_executable':sys.executable,'python_version':sys.version,'results':results},indent=2)+'\n')
(BASE/'owned_baselines/author/explicit_guard_proposal.py').write_text(author_guard)
(BASE/'owned_baselines/reviewer/explicit_guard_proposal.py').write_text(review_guard)
