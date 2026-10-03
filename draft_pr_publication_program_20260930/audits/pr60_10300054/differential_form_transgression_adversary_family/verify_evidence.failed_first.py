#!/usr/bin/env python3
"""Read-only consistency check of prior runs and selected authenticated bodies."""
import datetime,hashlib,json,pathlib,stat
root=pathlib.Path(__file__).resolve().parent
original=root.parent/'original_preparation_family'/'original'
sha=lambda b:hashlib.sha256(b).hexdigest()
expected={
 'OBSTRUCTION.md':'dcd4ba441c5655526a20a2ddd474e6c4477fab2c74978b907125f8d797b41087',
 'verify.py':'6d8dea9de4cd15bd79f35e71f99799b36fcd805c793cc39633b92db3920f362c',
 'source_record.json':'411830d86ebe931cfe6597757aa0cd3a4dad863ead819489a0cb56ada7894e44',
 'turns.json':'f340ba8e1c5c2feffa540132654c3be65d7d66701ffa21f9f20235504746c7ab',
 'verification.json':'5091356715e82d3ebbf245b3ef792ef4d73f186233d17ad6be745ec8d6c58bb5'}
pins=[]
for name,digest in expected.items():
 p=original/name;body=p.read_bytes();assert sha(body)==digest
 pins.append({'path':str(p),'bytes':len(body),'sha256':digest,'observed_mode':oct(stat.S_IMODE(p.stat().st_mode))})
for name in ('OBSTRUCTION.md','verify.py'):
 assert (root/'reproduction'/name).read_bytes()==(original/name).read_bytes()
runs=[]
for label in ('original_checker','coordinate_controls'):
 prefix=root/'captures'/label
 prebody=prefix.with_suffix('.prelaunch.json').read_bytes();pre=json.loads(prebody)
 post=json.loads(prefix.with_suffix('.post.json').read_bytes())
 assert post['prelaunch_sha256']==sha(prebody)
 assert post['returncode']==0 and post['capture_pid']==pre['capture_pid']
 assert isinstance(post['child_pid'],int) and post['child_pid']>0
 assert datetime.datetime.fromisoformat(post['ended_utc'])>=datetime.datetime.fromisoformat(pre['prelaunch_utc'])
 assert pre['dependencies']=={'sympy':'1.14.0','mpmath':'1.3.0'}
 for source in pre['sources']:
  body=pathlib.Path(source['path']).read_bytes()
  assert len(body)==source['bytes'] and sha(body)==source['sha256']
 for stream in ('stdout','stderr'):
  body=prefix.with_suffix('.'+stream).read_bytes()
  assert len(body)==post[stream]['bytes'] and sha(body)==post[stream]['sha256']
 assert prefix.with_suffix('.stderr').read_bytes()==b''
 runs.append({'label':label,'child_pid':post['child_pid'],'returncode':0,'prelaunch_matches_current_sources':True,'full_streams_match_receipts':True})
assert (root/'captures/original_checker.stdout').read_bytes()==(original/'verification.json').read_bytes()
author=json.loads((root/'captures/original_checker.stdout').read_bytes())
assert author['assertions_passed']==61
controls=json.loads((root/'coordinate_results.json').read_bytes())
assert controls['assertions_passed']==78==sum(controls['counts'].values())
assert controls['source_sha256']==sha((root/'coordinate_controls.py').read_bytes())
assert (root/'coordinate_results.json').read_bytes()==(root/'captures/coordinate_controls.stdout').read_bytes()
turns=json.loads((original/'turns.json').read_bytes())
assert (turns['substantive_proof_attempts'],turns['budget'],turns['turns'][0]['outcome'])==(1,5,'unsolved')
auth_path=original.parent/'ORIGINAL_AUTHENTICATION.json';authbody=auth_path.read_bytes();auth=json.loads(authbody)
assert auth['head']=='1e762651b698c1fb519901bd924c5bd3717cc5ef' and auth['scientific_file_count']==17
for pin in pins:
 name=pathlib.Path(pin['path']).name
 matches=[v for v in auth['scientific_files'] if v['local_path']=='original/'+name]
 assert len(matches)==1 and matches[0]['sha256']==pin['sha256'] and matches[0]['bytes']==pin['bytes']
result={'checked_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'operator':'PR60 differential-form subagent /root/algebra_reproduction_audit',
 'selected_external_body_pins':pins,'original_authentication_dated_pin':{'path':str(auth_path),'bytes':len(authbody),'sha256':sha(authbody),'observed_mode':oct(stat.S_IMODE(auth_path.stat().st_mode))},
 'runs':runs,'author_assertions':61,'independent_assertions':78,
 'author_stdout_byte_identical':True,'author_budget':[1,5,'unsolved'],
 'ROOT_closure_or_math_acceptance_inferred':False}
print(json.dumps(result,indent=2))
