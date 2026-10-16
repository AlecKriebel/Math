"""Fresh reviewer controls; all hostile fixtures and targets are owned locally."""
from pathlib import Path
import hashlib, json, os, sys
from record_exec import run, digest, ROOT

A=ROOT.parent
D=A/'contingent_credited_note_v2'
S=D/'publicfiles/support'
base=ROOT/'independent_controls'
base.mkdir(exist_ok=False)
wrappers=['run_diagnostics.py','test_integrity.py','test_runner_custody.py']
results=[]

def require(value, why):
    if not value: raise RuntimeError(why)

def inventory(root):
    return {str(p.relative_to(root)):
        {'link':os.readlink(p)} if p.is_symlink() else {'sha256':digest(p.read_bytes()),'bytes':p.stat().st_size}
        for p in root.rglob('*') if p.is_file() or p.is_symlink()}

def fixture(case):
    package=case/'package'
    (package/'support/review').mkdir(parents=True)
    for name in wrappers+['safe_output.py']:
        (package/'support'/name).write_bytes((S/name).read_bytes())
    for name in ['README.md','LICENSE.txt','support/CANDIDATE.md']:
        (package/name).write_text('PRIVATE SYNTHETIC INPUT; DO NOT CHANGE\n')
    for name in ['check_integrity.py','support/verify.py','support/review/independent_checks.py']:
        (package/name).write_text('raise RuntimeError("Synthetic child reached")\n')
    return package

bootstrap='''import pathlib,runpy,sys
m=pathlib.Path(sys.argv[1]); script=sys.argv[2]
def observe(event,args):
 if event=="subprocess.Popen":
  with m.open("ab") as f: f.write(b"ATTEMPTED\\n")
sys.addaudithook(observe)
sys.path.insert(0,str(pathlib.Path(script).parent))
sys.argv=[script]+sys.argv[3:]
runpy.run_path(script,run_name="__main__")
'''
for optimized in [False,True]:
    for wrapper in wrappers:
        for kind in ['symlink_leaf','hardlink_leaf','existing_dir','existing_file','dangling_final',
                     'contained_ancestor','missing_parent','package_root','parent_then_contained']:
            label=wrapper[:-3]+'_'+kind+('_O' if optimized else '_normal')
            case=base/label
            package=fixture(case)
            out=case/'output'
            victim=package/('README.md' if wrapper==wrappers[0] else 'LICENSE.txt')
            if kind in ['symlink_leaf','hardlink_leaf','existing_dir']:
                out.mkdir()
                if kind!='existing_dir':
                    leaf=out/('author_normal.stdout.json' if wrapper==wrappers[0] else 'PROCESS_RECEIPTS.json')
                    if kind=='symlink_leaf':leaf.symlink_to(victim)
                    else:os.link(victim,leaf)
            elif kind=='existing_file':out.write_text('Existing output is a regular file\n')
            elif kind=='dangling_final':out.symlink_to(case/'absent_target')
            elif kind=='contained_ancestor':
                alias=case/'outside_named_alias';alias.symlink_to(package,target_is_directory=True)
                out=alias/'new_leaf'
            elif kind=='missing_parent':out=case/'missing_parent/new_leaf'
            elif kind=='package_root':out=package
            elif kind=='parent_then_contained':out=case/'package/support/../new_leaf'
            before=inventory(case)
            marker=case/'child_launches'
            script=package/'support'/wrapper
            args=['--output-dir',str(out)]
            if wrapper!=wrappers[0]:args+=['--archive',str(D/'pr97_support.zip')]
            argv=['/usr/bin/python3','-E','-B']+(['-O'] if optimized else [])+['-c',bootstrap,str(marker),str(script)]+args
            rc,stdout,stderr,receipt=run('independent_'+label,argv,ROOT,'synthetic output-boundary rejection',(script,package/'support/safe_output.py'))
            after=inventory(case)
            require(rc!=0 and not marker.exists() and before==after,'Custody violation '+label)
            results.append({'case':label,'kind':kind,'optimized':optimized,'wrapper':wrapper,'exit':rc,
                'no_child_launch':True,'input_and_output_unchanged':True,'inventory':before,
                'receipt':'actual_processes/independent_'+label+'/receipt.json'})

# Reuse the three independently successful real output directories; none may change.
for optimized in [False,True]:
    for wrapper,name in zip(wrappers,['diagnostics','integrity','custody']):
        prior=ROOT/(name+'_reproduction')
        label='actual_reuse_'+name+('_O' if optimized else '_normal')
        marker=base/(label+'.launch')
        script=S/wrapper
        before=inventory(prior)
        args=['--output-dir',str(prior)]
        if wrapper!=wrappers[0]:args+=['--archive',str(D/'pr97_support.zip')]
        argv=['/usr/bin/python3','-E','-B']+(['-O'] if optimized else [])+['-c',bootstrap,str(marker),str(script)]+args
        rc,stdout,stderr,receipt=run('independent_'+label,argv,ROOT,'actual completed-output reuse rejection',(script,S/'safe_output.py'))
        require(rc!=0 and b'fresh and non-existing' in stderr and not marker.exists() and before==inventory(prior),label)
        results.append({'case':label,'exit':rc,'no_child_launch':True,'input_and_output_unchanged':True,
            'receipt':'actual_processes/independent_'+label+'/receipt.json'})

helper='''import sys,os,json,pathlib
sys.path.insert(0,sys.argv[1])
from safe_output import write_new,Journal,fresh_output
b=pathlib.Path(sys.argv[2]); kind=sys.argv[3]; action=sys.argv[4]
victim=b/"victim"; victim.write_bytes(b"UNCHANGED")
leaf=b/"leaf";j=Journal(leaf)
if action=="update":j.save({"old":1});leaf.unlink()
if kind=="symlink":leaf.symlink_to(victim)
elif kind=="hardlink":os.link(victim,leaf)
else:leaf.write_bytes(b"EXISTING")
blocked=False
try:
 if action=="bytes":write_new(leaf,b"CORRUPTED")
 else:j.save({"new":2})
except FileExistsError:blocked=True
if victim.read_bytes()!=b"UNCHANGED":raise RuntimeError("Victim changed")
if action=="update":
 if blocked or leaf.is_symlink() or json.loads(leaf.read_text())!={"new":2}:raise RuntimeError("Bad replacement")
elif not blocked:raise RuntimeError("Initial alias write accepted")
if list(b.glob(".journal-*")):raise RuntimeError("Temporary residue")
print(json.dumps({"PASS":True,"victim_unchanged":True,"action":action,"kind":kind}))
'''
(base/'helper.py').write_text(helper)
for optimized in [False,True]:
    for kind in ['symlink','hardlink','plain']:
        for action in ['bytes','first_journal','update']:
            label='helper_'+kind+'_'+action+('_O' if optimized else '_normal')
            case=base/label;case.mkdir()
            argv=['/usr/bin/python3','-E','-B']+(['-O'] if optimized else [])+[str(base/'helper.py'),str(S),str(case),kind,action]
            rc,out,err,receipt=run('independent_'+label,argv,ROOT,'synthetic exclusive-first-write/atomic-update',(base/'helper.py',S/'safe_output.py'))
            require(rc==0 and json.loads(out)['PASS'],label)
            results.append({'case':label,'exit':rc,'victim_unchanged':True,'receipt':'actual_processes/independent_'+label+'/receipt.json'})

# Additional failure structures absent from the provided regression set.
for optimized in [False,True]:
    for kind,code,reason in [
        ('invalid_utf8','import sys;sys.stdout.buffer.write(b"\\xff")\n','Malformed child output'),
        ('scalar_json','print("3")\n','Child output lacks a PASS object'),
        ('failed_object','print(\'{"status":"FAIL"}\')\n','Child output lacks a PASS object')]:
        label='failure_'+kind+('_O' if optimized else '_normal')
        case=base/label;package=fixture(case)
        (package/'support/verify.py').write_text(code)
        script=package/'support/run_diagnostics.py'
        dest=case/'results'
        argv=['/usr/bin/python3','-E','-B']+(['-O'] if optimized else [])+[str(script),'--output-dir',str(dest)]
        rc,out,err,receipt=run('independent_'+label,argv,ROOT,'synthetic malformed/failed child custody',(script,package/'support/verify.py',package/'support/safe_output.py'))
        j=json.loads((dest/'PROCESS_RECEIPTS.json').read_bytes());last=j[-1]
        require(rc!=0 and last['accepted'] is False and last['rejection_reason']==reason,label)
        require(last['stdout_sha256']==digest((dest/'author_normal.stdout.json').read_bytes()),label+' stdout')
        require(last['stderr_sha256']==digest((dest/'author_normal.stderr.txt').read_bytes()),label+' stderr')
        require(last['pid']>0 and last['command'] and last['cwd'] and last['started_utc'] and last['finished_utc'],label+' fields')
        results.append({'case':label,'exit':rc,'failed_child_receipt':last,'raw_custody_preserved':True,
            'receipt':'actual_processes/independent_'+label+'/receipt.json'})

(base/'RESULT.json').write_text(json.dumps({'status':'PASS','controls':len(results),
    'output_rejections':54,'actual_completed_reuse':6,'helper_controls':18,'additional_failure_controls':6,
    'synthetic_roles_separate':True,'concurrent_hostile_replacement_tested':False,'results':results},indent=2)+'\n')
print(json.dumps({'status':'PASS','controls':len(results),'output_rejections':54,'actual_reuse':6,'helper':18,'additional_failures':6}))
