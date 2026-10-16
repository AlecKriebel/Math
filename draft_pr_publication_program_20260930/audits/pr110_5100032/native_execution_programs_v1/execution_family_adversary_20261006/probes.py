"""Synthetic source probes only. Never calls worker/runner execute, services or native assess."""
import copy, hashlib, importlib.util, json, os, pathlib, signal, sys, textwrap, time, types
from unittest import mock
D=pathlib.Path(__file__).parent.parent
FAMILY={name:(D/name).read_bytes() for name in ['native_worker.py','native_runner.py','native_launcher.sh','protocol.py']}
R=pathlib.Path(__file__).parent/(('repaired_optimized_' if sys.flags.optimize else 'repaired_normal_')+str(os.getpid()))
R.mkdir(mode=0o700,exist_ok=False)
def module(name):
    m=types.ModuleType(name);m.__file__=str(D/(name+'.py'))
    exec(compile(FAMILY[name+'.py'],m.__file__,'exec'),m.__dict__);return m
w=module('native_worker');r=module('native_runner');p=module('protocol')
results=[]
def record(name,result,**more):results.append({'name':name,'result':result,**more})
def rejected(call):
    try:call()
    except (OSError,ValueError,KeyError,TypeError):return True
    return False
def spec(path,invocation,chain):
    return {'invocation_path':str(invocation),'resolved_absolute_path':str(path),'symlink_chain':chain,**w.pin(path.read_bytes()),'version':'synthetic'}
def linkrecord(path,target):return {'path':str(path),'target':target,'target_utf8_sha256':w.sha(target.encode())}
a=R/'symlink_dotdot';a.mkdir();(a/'real').mkdir();(a/'real/sub').mkdir()
(a/'tool').write_bytes(b'lexical collapse bytes');(a/'real/tool').write_bytes(b'kernel resolution bytes')
(a/'alias').symlink_to('real/sub');(a/'launch').symlink_to('alias/../tool')
actual=os.path.realpath(a/'launch')
true_spec=spec(a/'real/tool',a/'launch',[linkrecord(a/'launch','alias/../tool'),linkrecord(a/'alias','real/sub')])
false_spec=spec(a/'tool',a/'launch',[linkrecord(a/'launch','alias/../tool')])
record('kernel_valid_nested_symlink_dotdot_rejected',rejected(lambda:r.resolve_invocation(true_spec,w)),kernel_realpath=actual)
record('incorrect_lexical_path_accepted',not rejected(lambda:r.resolve_invocation(false_spec,w)),claimed_realpath=str(a/'tool'),kernel_realpath=actual)
a=R/'process_group';a.mkdir()
policy={'deadline_seconds':2,'stdout_cap':4096,'stderr_cap':4096,'retain_bytes':128,'max_processes':4,'term_grace_seconds':1,
 'allocation_cap':160*1024*1024,'file_count_cap':512,'headroom_bytes':32*1024*1024,'commit_reserve_bytes':8*1024*1024,'runtime_reserve_bytes':8*1024*1024}
code='import os,time; p=os.fork();\nif p==0:\n os.close(0);os.close(1);os.close(2);time.sleep(20);os._exit(0)\nprint(p,flush=True);os._exit(0)'
body,receipt=r.Processes(a,policy,w).run([os.path.realpath(sys.executable),'-E','-S','-B','-c',code],a,w.clean_environment(),fixture=True,allow_failure=True)
descendant=int(body.strip());alive=False
try:
    os.kill(descendant,0);alive=True
except ProcessLookupError:pass
finally:
    try:os.kill(descendant,signal.SIGKILL)
    except ProcessLookupError:pass
record('same_group_descendant_is_rejected',receipt['termination_reason']=='surviving_process_group',descendant_PID=descendant,direct_child_PID=receipt['PID'],exit_code=receipt['exit_code'],direct_child_reaped=receipt['reaped'],streams_drained=receipt['streams_fully_drained'],termination_reason=receipt['termination_reason'],group_absence_confirmed=receipt.get('process_group_absence_confirmed'),SIGKILL_attempted=receipt['SIGKILL_attempted'],descendant_PID_still_visible=alive,synthetic_descendant_cleanup='SIGKILL sent after observation if PID remains visible; PID visibility may include an unreapable descendant zombie')
a=R/'TERM_ignore_descendant';a.mkdir()
code='import os,signal,time;signal.signal(signal.SIGTERM,signal.SIG_IGN);p=os.fork();\nif p==0:\n os.close(0);os.close(1);os.close(2);time.sleep(20);os._exit(0)\nprint(p,flush=True);os._exit(0)'
body,receipt=r.Processes(a,policy,w).run([os.path.realpath(sys.executable),'-E','-S','-B','-c',code],a,w.clean_environment(),fixture=True,allow_failure=True)
descendant=int(body.strip())
try:os.kill(descendant,signal.SIGKILL)
except ProcessLookupError:pass
record('TERM_ignoring_same_group_descendant_KILL_and_reject',receipt['termination_reason']=='surviving_process_group' and receipt['SIGKILL_attempted'] and receipt['reaped'],receipt=receipt)
# Extract only the exact pure package-validation statements, never execute the runner.
source=FAMILY['native_runner.py'].decode();start=source.index("    package=packet['package'];");end=source.index('    transport=',start)
package_code=compile(textwrap.dedent(source[start:end]),str(D/'native_runner.py')+'#pure-package-guard','exec')
bodies={'manifest':b'{"complete":true}\n','proof':b'synthetic checked proof\n'}
bodies.update({'member_'+str(i):str(i).encode() for i in range(31)})
specs={name:{'path':name,**w.pin(body)} for name,body in bodies.items()}
package={'manifest':specs['manifest'],'effective_proof':specs['proof'],'logical_inventory':copy.deepcopy(specs),'transport_inventory_receipt':{'path':'unused','bytes':0,'sha256':'0'*64}}
def check_package(value,custom_bodies=None):
    data=bodies if custom_bodies is None else custom_bodies
    registry=[{'path':name,**w.pin(body)} for name,body in data.items()]
    inputs=p.Inputs(registry,data)
    exec(package_code,{'packet':{'package':value},'inputs':inputs,'need':r.need,'p':p})
record('valid33_package_membership_passes',not rejected(lambda:check_package(package)))
for role in ['manifest','effective_proof']:
    bad=copy.deepcopy(package);key='manifest' if role=='manifest' else 'proof';bad['logical_inventory'][key]=specs['member_0']
    record('missing_inventory_'+role+'_rejected',rejected(lambda:check_package(bad)))
bad=copy.deepcopy(package);bad['logical_inventory'].pop('member_0');record('32_member_package_rejected',rejected(lambda:check_package(bad)))
bad=copy.deepcopy(package);bad['unexpected']=True;record('extra_package_field_rejected',rejected(lambda:check_package(bad)))
for role,body in [('proof',b''),('manifest',b'{}')]:
    data={**bodies,role:body};bad=copy.deepcopy(package);new={'path':role,**w.pin(body)};bad['logical_inventory'][role]=new;bad['effective_proof' if role=='proof' else 'manifest']=new
    record('empty_'+role+'_rejected',rejected(lambda:check_package(bad,data)))
a=R/'guards';a.mkdir();(a/'leaf').write_bytes(b'x');(a/'symlink').symlink_to('leaf')
record('leaf_symlink_rejected',rejected(lambda:w.read_file(a/'symlink',16)))
os.link(a/'leaf',a/'hard');record('hardlink_rejected',rejected(lambda:w.read_file(a/'leaf',16)));(a/'hard').unlink()
record('collision_rejected',rejected(lambda:w.atomic_write(a,'leaf',b'new',16)))
record('stale_preimage_rejected',rejected(lambda:w.atomic_write(a,'leaf',b'new',16,replace=True,expected=w.pin(b'wrong'))))
record('boolean_CPU_rejected',rejected(lambda:w.limits_policy({'cpu_seconds':True,'file_size_bytes':4096,'open_files':32,'memory_advisory_bytes':134217728,'hard_memory_claimed':False})))
record('duplicate_JSON_rejected',rejected(lambda:r.loads(b'{"x":1,"x":2}')))
a=R/'stdlib_shadow';a.mkdir();(a/'json.py').write_text('SYNTHETIC_SHADOW="local shadow imported"\n')
(a/'tiny.py').write_text('import json;print(getattr(json,"SYNTHETIC_SHADOW","safe stdlib"))\n')
runner=r.Processes(a,policy,w)
out,receipt=runner.run([os.path.realpath(sys.executable),'-E','-S','-B',str(a/'tiny.py')],a,w.clean_environment(),fixture=True)
record('E_S_B_allow_script_directory_stdlib_shadow',out==b'local shadow imported\n',receipt=receipt)
out,receipt=runner.run([os.path.realpath(sys.executable),'-E','-S','-B','-P',str(a/'tiny.py')],a,w.clean_environment(),fixture=True)
record('P_prevents_script_directory_stdlib_shadow',out==b'safe stdlib\n',receipt=receipt)
a=R/'actual_safe_startup_guard';a.mkdir()
runner=r.Processes(a,{**policy,'retain_bytes':4096},w)
for role in ['native_runner','native_worker']:
    argument='--config' if role=='native_runner' else '--control'
    out,receipt=runner.run([os.path.realpath(sys.executable),'-E','-S','-B',str(D/(role+'.py')),argument,str(a/'missing.json')],a,w.clean_environment(),fixture=True,allow_failure=True)
    record(role+'_rejects_missing_P_before_imports',receipt['exit_code']!=0 and b'-P' in (a/receipt['streams']['stderr']['retained_path']).read_bytes(),receipt=receipt)
a=R/'EPERM_receipt';a.mkdir()
runner=r.Processes(a,policy,w)
real_killpg=r.os.killpg
def signal_permission(pgid,sig):
    if sig==0:raise PermissionError(1,'synthetic EPERM group probe')
    return real_killpg(pgid,sig)
with mock.patch.object(r.os,'killpg',signal_permission):
    out,receipt=runner.run([os.path.realpath(sys.executable),'-E','-S','-B','-P','-c','print("small synthetic process")'],a,w.clean_environment(),fixture=True,allow_failure=True)
record('EPERM_retains_truthful_failure_receipt',receipt['operator_intervention_required'] is True and receipt['process_group_absence_confirmed'] is False and 'PGID_probe_permission_denied' in receipt['cleanup_errors'] and receipt['termination_reason'] is not None and (a/'PROCESS_JOURNAL.json').exists(),receipt=receipt)
a=R/'post_spawn_setup_failure';a.mkdir();runner=r.Processes(a,policy,w)
children=[];real_popen=r.subprocess.Popen
def capture_popen(*args,**kwargs):
    child=real_popen(*args,**kwargs);children.append(child);return child
error=None
try:
    with mock.patch.object(r.subprocess,'Popen',capture_popen),mock.patch.object(r.os,'set_blocking',side_effect=ValueError('synthetic post-spawn setup failure')):
        runner.run([os.path.realpath(sys.executable),'-E','-S','-B','-P','-c','import time;time.sleep(20)'],a,w.clean_environment(),fixture=True,allow_failure=True)
except BaseException as caught:error=type(caught).__name__
managed_reaped=bool(children) and children[0].poll() is not None
for child in children:
    if child.poll() is None:
        try:os.killpg(child.pid,signal.SIGKILL)
        except ProcessLookupError:pass
        child.wait(timeout=3)
record('post_spawn_setup_failure_managed_and_receipted',managed_reaped and (a/'PROCESS_JOURNAL.json').exists(),exception_type=error,direct_child_PID=None if not children else children[0].pid,managed_reaped_before_manual_cleanup=managed_reaped,launch_journal_present=(a/'PROCESS_LAUNCHES.json').exists(),result_journal_present=(a/'PROCESS_JOURNAL.json').exists(),manual_SIGKILL_cleanup_needed=not managed_reaped)
a=R/'child_mask_and_launch';a.mkdir();runner=r.Processes(a,policy,w)
out,receipt=runner.run([os.path.realpath(sys.executable),'-E','-S','-B','-P','-c','import json,signal;print(json.dumps(sorted(int(x) for x in signal.pthread_sigmask(signal.SIG_BLOCK,set()))))'],a,w.clean_environment(),fixture=True)
mask=json.loads(out);launch=w.loads((a/'PROCESS_LAUNCHES.json').read_bytes())['launches'][0]
record('child_TERM_INT_masks_unblocked',int(signal.SIGTERM) not in mask and int(signal.SIGINT) not in mask,actual_child_mask=mask,receipt=receipt)
record('launch_journal_binds_real_PID_argv_environment',launch['PID']==receipt['PID'] and launch['argv']==receipt['argv'] and launch['environment_sha256']==receipt['environment_sha256'] and launch['state']=='launched_not_yet_reaped')
# Fresh present configuration checks only, without retaining bodies or using credentials.
gitconfig=w.read_file(r.C/'.git/config',128*1024)
config=r.configparser.RawConfigParser();config.read_string(gitconfig.decode())
git_allowed=all(not section.lower().startswith(('include','alias','url ','filter ','diff ','credential')) and
 all(key.lower() not in ['sshcommand','pager','editor','proxy','promisor','partialclonefilter'] for key in config[section]) for section in config.sections())
record('genuine_current_Git_configuration_policy_passes',git_allowed,pin=w.pin(gitconfig),body_retained=False)
ghconfig=pathlib.Path('/Users/alec/.config/gh/config.yml')
ghbody=w.read_file(ghconfig,128*1024);record('genuine_current_GH_configuration_policy_passes',not rejected(lambda:r.validate_gh_configuration_lines(ghbody.decode())),pin=w.pin(ghbody),body_retained=False)
envelope={'schema':'pr110-program-adversarial-synthetic-probes/v1','UTC':w.now(),'operator_PID':os.getpid(),'optimization':sys.flags.optimize,
 'synthetic_fixture_only':True,'actual_native_assess_calls':0,'actual_service_calls':0,'Git_mutations':0,'native_export_calls':0,
 'program_pins':{name:w.pin(body) for name,body in FAMILY.items()},'family_unchanged_during_probes':all((D/name).read_bytes()==body for name,body in FAMILY.items()),'results':results}
envelope['expected_observations']={row['name']:row['name'] not in ['kernel_valid_nested_symlink_dotdot_rejected','incorrect_lexical_path_accepted'] for row in results}
envelope['expected_observations_met']=all(row['result'] is envelope['expected_observations'][row['name']] for row in results)
(R/'RESULT.json').write_bytes(w.canonical(envelope));print(json.dumps(envelope,sort_keys=True))
w.need(envelope['family_unchanged_during_probes'] and envelope['expected_observations_met'],'Family changed or unexpected synthetic observation')
