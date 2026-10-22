from pathlib import Path
import json
H=Path(__file__).absolute().parent
R=H/'final_results'
def record(name):return json.loads((R/(name+'.json')).read_text())
def payload(name):return json.loads(record(name)['stdout'].splitlines()[-1])
records=[json.loads(p.read_text()) for p in R.glob('*.json')]
assert len(records)==79
assert all(not r['timeout'] for r in records)
assert payload('dispatcher_checked_regular')['accepted'] is True
for name in ('checked_writable','checked_symlink','checked_directory','checked_oversize','checked_dotdot','checked_fifo','checked_fifo_swap'):
 assert payload('dispatcher_'+name)['accepted'] is False,name
for name in ('bad_graph','bad_dispatcher_pin','bad_backend_pin','bad_source_pin','bad_gate_pin','bad_adoption_pin'):
 p=payload('dispatcher_'+name);assert p['events']==[] and p['exception'] is not None,name
for name in ('guard_relative','guard_outside','guard_kwargs'):
 p=payload('dispatcher_'+name);assert p['exception']['message']=='Unapproved backend import',name
 assert p['spec_restored'] and p['module_aliases_restored'],name
for phase in ('ready','merge','factual','completion'):
 for action in ('preflight','bind','prepare','verify','accept','sync','pointer'):
  name='dispatcher_route_'+phase+'_'+action;p=payload(name)
  assert p['spec_restored'] and p['module_aliases_restored'],name
  backend='c_compile' in p['events']
  if action=='preflight':
   assert not backend and (p['exception'] is None)==(phase=='ready'),name
  else:
   assert p['exception'] is None,name
   assert backend==(not(phase=='ready' and action=='bind')),name
   methods=[e for e in p['events'] if isinstance(e,list) and e[0]=='method']
   assert len(methods)==1 and methods[0][1:3]==['ready' if phase=='ready' else 'lifecycle',action],name
for name in ('constructor_failure','install_before_constructor','install_after_aliases','alias_read_failure','alias_restore_failure','close_failure','phase_exception'):
 p=payload('dispatcher_'+name)
 assert p['constructor_restored'] and p['spec_restored'] and p['module_aliases_restored'],name
 assert p['closed']==(0 if name=='install_before_constructor' else 1),name
 assert p['alias_original']==([True,True,False,True,True,True] if name=='alias_restore_failure' else [True]*6),name
 if name!='install_before_constructor':
  stats=[json.loads(line) for line in record('dispatcher_'+name)['stdout'].splitlines() if 'API_restore_attempt_count' in line][0]
  assert stats['API_restore_attempt_count']==6,name
for name in ('phase_exception_uncaught','chained_exception_uncaught'):
 r=record('dispatcher_'+name);assert r['exit']==1 and r['stderr']=='Root PR206 lifecycle failed: RuntimeError\n',name
 assert 'SYNTHETIC_CREDENTIAL_SENTINEL_206_AUDIT' not in r['stdout']+r['stderr'],name
 stats=json.loads(r['stdout']);assert stats['API_restore_attempt_count']==6,name
for name in ('create','reuse'):
 p=payload('installer_'+name)
 assert p['exception'] is None and p['mode']=='0o444' and p['lock_released_after_return'] and p['receipt_exists'] and p['attempt_preserved'],name
p=payload('installer_reuse');assert p['before_inode']==p['after_inode'] and p['mutations']==[]
for name in ('bad_protocol','bad_self_pin','bad_payload','bad_mode','symlink_lock','busy_lock','fifo_adoption','fifo_lock','fifo_swap_before_lock_open'):
 p=payload('installer_'+name);assert p['exception'] is not None and not p['receipt_exists'],name
p=payload('installer_existing_receipt');assert p['exception']['type']=='FileExistsError' and p['lock_released_after_return']
r=record('installer_error_uncaught');assert r['exit']==1 and r['stderr']=='Root PR206 installer failed: OSError\n'
for label in ('dispatcher','installer'):
 for kind in ('badint','unknown','missing'):
  r=record(label+'_'+kind);assert r['exit']==1 and r['stdout']=='' and r['stderr']=='Root PR206 '+('lifecycle' if label=='dispatcher' else 'installer')+' failed: RuntimeError\n'
  assert 'SECRET_206' not in r['stderr'],(label,kind)
 r=record(label+'_help');assert r['exit']==0 and r['stderr']=='' and 'usage:' in r['stdout']
 r=record(label+'_optimized');assert r['exit']==1 and 'required before dependen' in r['stderr']
print(json.dumps({'verified':True,'records':79,'remaining_mandatory_findings':0,'scope':'OWNED_SYNTHETIC_OFFLINE_ONLY'},sort_keys=True))
