"""Test actual extracted archive bytes; mutate only this review's copies."""
import copy, hashlib, json, os, pathlib, subprocess, sys

HERE=pathlib.Path(__file__).resolve().parent
X=HERE/'extracted'
env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1')
original=(X/'certificate.json').read_bytes()
original_code=(X/'verify.py').read_bytes()
expected=json.loads((X/'expected_results.json').read_text())
out={'replay':[],'controls':[]}

def execute(mode):
    command=[sys.executable,'-B']+([mode] if mode else [])+[str(X/'verify.py')]
    p=subprocess.run(command,capture_output=True,text=True,env=env)
    return p

for mode in ('','-O','-OO'):
    p=execute(mode)
    if p.returncode:raise RuntimeError(p.stderr)
    v=(X/'results.json').read_bytes()
    if json.loads(v)!=expected:raise ValueError('expected result mismatch')
    digest=hashlib.sha256(v).hexdigest()
    out['replay'].append({'mode':mode or 'normal','returncode':p.returncode,'sha256':digest,'summary':p.stdout.strip(),'matches_expected':True})

def certificate_control(name,mutate):
    d=json.loads(original);mutate(d)
    (X/'certificate.json').write_text(json.dumps(d))
    for mode in ('','-O','-OO'):
        p=execute(mode)
        if p.returncode==0:raise ValueError('accepted corruption '+name+' '+mode)
        out['controls'].append({'name':name,'mode':mode or 'normal','returncode':p.returncode,'final_error':p.stderr.strip().splitlines()[-1]})
    (X/'certificate.json').write_bytes(original)

certificate_control('squared exponent 2 replaced by 1',lambda d:d['certificate_rows'][20]['a'].__setitem__(5,1))
certificate_control('primary separator replaced with zero',lambda d:d['certificate_rows'][6].__setitem__('z',[0]*12))
certificate_control('independent support wrong frozen marker',lambda d:d['independent_certificate_rows'][0]['a'].__setitem__(0,1))
certificate_control('independent separating vector replaced with zero',lambda d:d['independent_certificate_rows'][11].__setitem__('v',[0]*12))
certificate_control('wrong input word metadata',lambda d:d['word'].__setitem__(11,4))
certificate_control('omitted support row',lambda d:d['certificate_rows'].pop(20))
certificate_control('duplicate support row',lambda d:d['certificate_rows'].append(copy.deepcopy(d['certificate_rows'][-1])))
certificate_control('reverse separator sign',lambda d:d['certificate_rows'][0].__setitem__('z',[-v for v in d['certificate_rows'][0]['z']]))

def code_control(name,old,new):
    code=original_code.decode()
    if code.count(old)!=1:raise ValueError('control pattern '+name)
    (X/'verify.py').write_text(code.replace(old,new))
    for mode in ('','-O','-OO'):
        p=execute(mode)
        if p.returncode==0:raise ValueError('accepted code corruption '+name+' '+mode)
        out['controls'].append({'name':name,'mode':mode or 'normal','returncode':p.returncode,'final_error':p.stderr.strip().splitlines()[-1]})
    (X/'verify.py').write_bytes(original_code)

code_control('remove Dynkin adjacency in inclined rule','and frozenset((word[k],word[l])) in EDGES:',':')
code_control('wrong final optimizing route','7:(2,6,1,3,4,8,5,10)','7:(2,6,1,3,4,8,5)')
code_control('transposed mutation sign','power = sum(B[a][k]*e[a] for a in range(N) if a != k)','power = -sum(B[a][k]*e[a] for a in range(N) if a != k)')
code_control('double one claimed coefficient','expected=add(mul(Y[7],F7),mul(Y[9],F9),mul(Y[11],add(ONE,Y[10])),Y[12])','expected=add(mul(Y[7],F7),mul(Y[9],F9),mul(Y[11],add(ONE,Y[10])),Y[12],Y[12])')

if (X/'certificate.json').read_bytes()!=original or (X/'verify.py').read_bytes()!=original_code:raise ValueError('restore failed')
p=execute('')
if p.returncode:raise RuntimeError(p.stderr)
out['final_pristine_result_sha256']=hashlib.sha256((X/'results.json').read_bytes()).hexdigest()
(HERE/'replay_and_controls.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'primary_replay_modes':len(out['replay']),'independent_corruption_tests':len(out['controls']),'all_rejected':True,'restored':True,'sha256':out['final_pristine_result_sha256']},indent=2))
