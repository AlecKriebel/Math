#!/usr/bin/env python3
"""Run universal polynomial controls and adversarial input models in both modes."""
from pathlib import Path
from fractions import Fraction as F
from copy import deepcopy
from functools import reduce
from operator import mul
import datetime, hashlib, json, subprocess, sys

BASE=Path(__file__).resolve().parent
MODELS=BASE/'exact_models';MODELS.mkdir(exist_ok=True)
EVIDENCE=BASE/'execution_evidence/exact_controls';EVIDENCE.mkdir(exist_ok=True)
model={'system_xy_multiplier':'1','embedding_b0_multiplier':'-1/2',
 'example_scale':'1/3','example_disk_radius':'1/8',
 'path_pieces':[{'interval':['0','1'],'real':['1','-1'],'imaginary':['0','1']},
                {'interval':['1','2'],'real':['1','-1'],'imaginary':['2','-1']}],
 'general_jacobian_terms':[
    {'coefficient':'2','powers':{'x':2}}, {'coefficient':'2','powers':{'y':2}},
    {'coefficient':'1','powers':{'a1':1,'x':1}}, {'coefficient':'2','powers':{'b2':1,'x':1}},
    {'coefficient':'2','powers':{'b1':1,'y':1}}, {'coefficient':'-1','powers':{'a2':1,'y':1}},
    {'coefficient':'1','powers':{'a1':1,'b2':1}}, {'coefficient':'-1','powers':{'a2':1,'b1':1}}]}
cases=[('baseline',deepcopy(model),'Correct universal controls.')]
def changed(label,modify,rationale):
    candidate=deepcopy(model);modify(candidate);cases.append((label,candidate,rationale))
changed('wrong_embedding_b0',lambda m:m.update(embedding_b0_multiplier='-1'),
        'Rejects wrong slice coefficient.')
changed('wrong_system_xy',lambda m:m.update(system_xy_multiplier='2'),
        'Rejects changed printed system.')
changed('wrong_general_jacobian',lambda m:m['general_jacobian_terms'][-1].update(coefficient='1'),
        'Rejects an off-slice mixed-coefficient Jacobian sign error missed by slice-only evaluation.')
changed('wrong_path_seam',lambda m:m['path_pieces'][1].update(imaginary=['3','-1']),
        'Rejects changed path bounds or join.')
changed('wrong_path_bound',lambda m:m['path_pieces'][0].update(real=['2','-2'],imaginary=['0','2']),
        'Rejects a universal norm bound violation.')
changed('bounded_but_discontinuous_seam',lambda m:m['path_pieces'][1].update(imaginary=['-2','1']),
        'Both pieces retain the correct norm bounds but join at i and -i; continuity fails.')
changed('root_endpoints_equal',lambda m:m['path_pieces'][1].update(real=['-1','1']),
        'A continuous bounded root path returns to +1, so the required opposite endpoint obstruction disappears.')
changed('path_through_zero',lambda m:[piece.update(imaginary=['0']) for piece in m['path_pieces']],
        'The path crosses zero at the join and the quotient is undefined.')
changed('positive_control_reverse_orientation',lambda m:[piece.update(imaginary=(['0','-1'] if i==0 else ['-2','1'])) for i,piece in enumerate(m['path_pieces'])],
        'A distinct valid lower semicircular polygon has the same exact endpoint obstruction and should pass.')
changed('zero_scale',lambda m:m.update(example_scale='0'),'Rejects undefined quotient denominator.')
changed('touching_open_disk_boundary',lambda m:m.update(example_scale='1/2',example_disk_radius='1/4'),
        'Rejects replacing strict disk inclusion by equality.')

# Encode the degree-66 polynomial path used in the author finite-grid attack.
def conv(p,q):
    out=[F(0)]*(len(p)+len(q)-1)
    for i,a in enumerate(p):
        for j,b in enumerate(q):out[i+j]+=a*b
    return out
nodes=[F(k,64) for k in range(65)];target=F(1,128)
polynomial=[F(1)]
for a in nodes:polynomial=conv(polynomial,[-a,F(1)])
den=reduce(mul,(target-a for a in nodes),F(1))
factor=[-v/den for v in polynomial];factor[0]+=1
hidden=deepcopy(model)
hidden['path_pieces'][0]['real']=list(map(str,conv(factor,[F(1),F(-1)])))
hidden['path_pieces'][0]['imaginary']=list(map(str,conv(factor,[F(0),F(1)])))
cases.append(('continuous_hidden_zero',hidden,
 'Exact mechanism fails closed on unsupported norm degree 132; the separate exact t=1/128 witness shows actual norm zero. Rejection is not advertised as a full high-degree positivity decision.'))

results=[]
for label,candidate,rationale in cases:
    path=MODELS/(label+'.json');path.write_text(json.dumps(candidate,indent=2)+'\n')
    for mode,args in [('ordinary',[]),('optimized',['-O'])]:
        command=[sys.executable,*args,str(BASE/'exact_polynomial_controls.py'),str(path)]
        r=subprocess.run(command,cwd=BASE,capture_output=True,text=True)
        stdout=EVIDENCE/(label+'_'+mode+'.stdout');stderr=EVIDENCE/(label+'_'+mode+'.stderr')
        stdout.write_text(r.stdout);stderr.write_text(r.stderr)
        record=json.loads(r.stdout) if r.stdout else json.loads(r.stderr)
        results.append({'label':label,'mode':mode,'rationale':rationale,'command':command,
            'cwd':str(BASE),'returncode':r.returncode,'status':record.get('status'),
            'reason':record.get('reason'),'model_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
            'stdout':str(stdout),'stderr':str(stderr),
            'stdout_sha256':hashlib.sha256(r.stdout.encode()).hexdigest(),
            'stderr_sha256':hashlib.sha256(r.stderr.encode()).hexdigest()})
        print(label,mode,'exit',r.returncode,record.get('status'),record.get('reason',''))
(BASE/'execution_evidence/exact_control_runs.json').write_text(json.dumps({
    'timestamp':datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'python_executable':sys.executable,'python_version':sys.version,
    'checker_sha256':hashlib.sha256((BASE/'exact_polynomial_controls.py').read_bytes()).hexdigest(),
    'results':results},indent=2)+'\n')

# Keep the full exact rational normalization underlying the reviewer blind spot.
review_nodes={F(k,m-k) for m in range(5,45) for k in range(m)};tr=F(1,1000)
review_product=reduce(mul,(tr-a for a in review_nodes),F(1))
(BASE/'execution_evidence/reviewer_hidden_zero_normalizing_product.txt').write_text(str(review_product)+'\n')
