"""Reproduce the inspected original deposit only in byte-identical quarantine."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,os,resource,shutil,subprocess,sys

HERE=Path(__file__).resolve().parent
SOURCE=HERE.parent.parent/'sources'/'support'
QUARANTINE=HERE/'quarantine'
QUARANTINE.mkdir(exist_ok=True)
COPY=QUARANTINE/'support'
assert not COPY.exists(), 'Use a fresh quarantine; do not overwrite prior runs.'
manifest=json.loads((SOURCE/'SUPPORT_MANIFEST.json').read_bytes())['files']
inventory={}
json_summaries={}
for path in sorted(SOURCE.rglob('*')):
    if path.is_file():
        rel=path.relative_to(SOURCE).as_posix();data=path.read_bytes()
        inventory[rel]={'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),
                        'mode':path.stat().st_mode&0o777}
        if rel!='SUPPORT_MANIFEST.json':assert inventory[rel]==manifest[rel],rel
        if rel.endswith('.json'):
            value=json.loads(data)
            json_summaries[rel]={'type':type(value).__name__,'entries':len(value),
                                 'keys':sorted(value) if isinstance(value,dict) else None}
assert set(inventory)==set(manifest)|{'SUPPORT_MANIFEST.json'}
shutil.copytree(SOURCE,COPY,copy_function=shutil.copy2)
for rel,pin in inventory.items():
    data=(COPY/rel).read_bytes()
    assert hashlib.sha256(data).hexdigest()==pin['sha256']
    assert (COPY/rel).stat().st_mode&0o777==pin['mode']

runtime=HERE.parents[3]/'tmp'/'shared-math-runtime'/'bin'/'python'
assert runtime.is_file(),str(runtime)
output=QUARANTINE/'actual-run'
command=[sys.executable,'-I','-B',str(COPY/'verification'/'run_diagnostics.py'),
         '--stdlib-python',sys.executable,'--library-python',str(runtime),
         '--output-directory',str(output)]
def limits():
    resource.setrlimit(resource.RLIMIT_CPU,(500,500))
    resource.setrlimit(resource.RLIMIT_FSIZE,(16*1024*1024,16*1024*1024))
    resource.setrlimit(resource.RLIMIT_NOFILE,(128,128))
started=datetime.now(timezone.utc).isoformat()
env={'PATH':'/usr/bin:/bin','PYTHONDONTWRITEBYTECODE':'1','PYTHONNOUSERSITE':'1'}
process=subprocess.run(command,cwd=QUARANTINE,env=env,capture_output=True,
                       timeout=600,preexec_fn=limits)
(QUARANTINE/'runner.stdout').write_bytes(process.stdout)
(QUARANTINE/'runner.stderr').write_bytes(process.stderr)
assert process.returncode==0,(process.returncode,process.stderr.decode())
assert not process.stderr
result=json.loads((output/'RESULT.json').read_bytes())
journal=json.loads((output/'CHILD_JOURNAL.json').read_bytes())
assert result['verdict']=='PASS_PORTABLE_DIAGNOSTIC_REPRODUCTION'
assert result['child_process_count']==22
assert result['all_children_reaped'] and result['all_process_groups_absent']
assert result['all_child_returncodes_zero'] and result['sources_full_body_mode_unchanged']
for rel,pin in inventory.items():
    assert hashlib.sha256((SOURCE/rel).read_bytes()).hexdigest()==pin['sha256']
    assert hashlib.sha256((COPY/rel).read_bytes()).hexdigest()==pin['sha256']
report={'started_utc':started,'finished_utc':datetime.now(timezone.utc).isoformat(),
         'support_member_count':len(inventory),'support_internal_manifest_all_match':True,
         'all_json_fully_parsed':len(json_summaries),'json_summaries':json_summaries,
         'inventory':inventory,'quarantine':str(QUARANTINE),'command':command,
         'returncode':process.returncode,'stderr_empty':not process.stderr,
         'stdout_sha256':hashlib.sha256(process.stdout).hexdigest(),
         'runner_result':result,'actual_child_journal':journal,
         'original_and_quarantine_input_bytes_unchanged':True,
         'deposited_scripts_read_before_execution':True,
         'network_or_out_of_quarantine_writes_initiated':False,
         'scientific_role':'Supporting diagnostics only, not a Brownian proof or certified quadrature.'}
(HERE/'support-reproduction.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({'status':'PASS','support_members':len(inventory),
                  'children':22,'all_reaped':True,'all_source_bytes_unchanged':True,
                  'roles':result['role_results']},indent=2))
