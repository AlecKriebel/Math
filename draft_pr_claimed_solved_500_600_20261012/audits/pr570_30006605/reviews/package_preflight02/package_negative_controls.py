#!/usr/bin/env python3
"""Independent integrity fault controls plus explicitly mocked JSON comparison controls."""
from pathlib import Path
import json,subprocess,shutil,hashlib,os,sys,importlib.util,io,contextlib
from types import SimpleNamespace
HERE=Path(__file__).resolve().parent
CLEAN=HERE/'.cache/clean_replay/weighted_centers_verification'
WORK=HERE/'.cache/negative';WORK.mkdir(exist_ok=True)
ENV=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',TMPDIR=str(HERE/'.cache/tmp'))
results=[]
sha=lambda b:hashlib.sha256(b).hexdigest()
def copy(tag):
    dest=WORK/tag
    if dest.exists():shutil.rmtree(dest)
    shutil.copytree(CLEAN,dest);return dest

def reseal(dest):
    m=json.loads((dest/'MANIFEST.json').read_text())
    for n in m['files']:
        if (dest/n).is_file():
            b=(dest/n).read_bytes();m['files'][n]={'bytes':len(b),'sha256':sha(b)}
    (dest/'MANIFEST.json').write_text(json.dumps(m,indent=2)+'\n')

def rejected(tag,change,expected,seal=False):
    d=copy(tag);change(d)
    if seal:reseal(d)
    p=subprocess.run(['/usr/bin/sandbox-exec','-p','(version 1)(allow default)(deny network*)',sys.executable,str(d/'run_all.py')],cwd=d,env=ENV,capture_output=True,text=True)
    assert p.returncode!=0 and expected in p.stderr,(tag,p.stderr)
    results.append({'case':tag,'status':'REJECTED_AS_REQUIRED','expected_error':expected,'actual_stderr':p.stderr,'layer':'actual driver; no mocked subprocess'})

rejected('corrupt',lambda d:(d/'README.md').write_text('changed'),'Outer payload mismatch')
rejected('extra',lambda d:(d/'unregistered.md').write_text('extra'),'Outer payload inventory mismatch')
rejected('missing_nested_payload',lambda d:(d/'reviews/search01/REPORT.md').unlink(),'Outer payload inventory mismatch')
# Reseal the outer inventory after removing a nested file: inner ordinary SHA must still reject.
def erase_and_outer(d):
    p='reviews/oracle01/CONTROL_RESULTS.json';(d/p).unlink()
    m=json.loads((d/'MANIFEST.json').read_text());del m['files'][p];(d/'MANIFEST.json').write_text(json.dumps(m))
rejected('missing_nested_after_outer_reseal',erase_and_outer,'Nested hash mismatch or missing payload')
rejected('alter_nested_seal',lambda d:(d/'reviews/oracle01/SHA256SUMS').write_text('0'*64+'  controls.py\n'),'Nested hash mismatch or missing payload',True)
rejected('duplicate_nested_seal',lambda d:(d/'SEALS.json').write_text(json.dumps(json.loads((d/'SEALS.json').read_text())*2)),'Seal registry mismatch',True)

def ignored(d,wrong_job=False):
    jobs=json.loads((d/'JOBS.json').read_text())
    if wrong_job:jobs[0]['ignored_clock_fields']=['started_at_utc','completed_at_utc','elapsed_seconds']
    else:jobs[2]['ignored_clock_fields'].append('counts')
    (d/'JOBS.json').write_text(json.dumps(jobs))
# Test the comparison layer without burning the actual mathematical reruns again.
def comparison(tag,change_actual=None,change_jobs=None,expected=None):
    dest=copy(tag)
    if change_jobs:change_jobs(dest);reseal(dest)
    sys.path.insert(0,str(dest))
    spec=importlib.util.spec_from_file_location('review_driver_'+tag,dest/'run_all.py')
    mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
    jobs=json.loads((dest/'JOBS.json').read_text())
    wanted={j['script']:json.loads((dest/j['record']).read_text()) for j in jobs}
    actual_run=subprocess.run
    def fake(args,**kwargs):
        key=next(j['script'] for j in jobs if str(args[1]).endswith(j['script']))
        out=json.loads(json.dumps(wanted[key]))
        if change_actual:change_actual(key,out)
        return SimpleNamespace(returncode=0,stderr='',stdout=json.dumps(out))
    caught=None;stdout=io.StringIO()
    try:
        subprocess.run=fake
        with contextlib.redirect_stdout(stdout):mod.main()
    except Exception as ex:caught=str(ex)
    finally:subprocess.run=actual_run;sys.path.pop(0)
    if expected:assert caught and expected in caught,(tag,caught)
    else:assert caught is None,caught
    results.append({'case':tag,'status':'REJECTED_AS_REQUIRED' if expected else 'ACCEPTED_AS_REQUIRED','error':caught,'layer':'JSON-comparison unit control with explicitly mocked subprocess outputs; actual five programs separately replayed under OS network denial'})
comparison('complete_mock_baseline')
jobs_script='original/unsolved_math_prioritization/attempts/30006605/bundle/controls.py'
comparison('wrong_actual_math',lambda k,a:a.update({'unregistered_mathematical_value':1}) if k==jobs_script else None,expected='Complete mathematical JSON mismatch')
comparison('only_three_top_level_clocks',lambda k,a:a.update({'started_at_utc':'changed','completed_at_utc':'changed','elapsed_seconds':-1}) if k=='reviews/oracle01/controls.py' else None)
comparison('nested_clock_named_math',lambda k,a:a.update({'mathematics':{'started_at_utc':'changed'}}) if k=='reviews/oracle01/controls.py' else None,expected='Complete mathematical JSON mismatch')
comparison('extra_ignored_field',change_jobs=lambda d:ignored(d),expected='Unsupported replay normalization')
comparison('normalization_wrong_job',change_jobs=lambda d:ignored(d,True),expected='Unsupported replay normalization')
(HERE/'PACKAGE_NEGATIVE_RESULTS.json').write_text(json.dumps({'status':'PASS','cases':results},indent=2)+'\n')
print(json.dumps({'status':'PASS','negative_or_baseline_cases':len(results)}))
