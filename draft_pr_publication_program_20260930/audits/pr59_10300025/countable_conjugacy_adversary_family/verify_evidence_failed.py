#!/usr/bin/env python3
"""Final read-only mathematical evidence checks; record dated external pins."""
import datetime,hashlib,json,os,pathlib,stat
root=pathlib.Path(__file__).resolve().parent
source=root.parent/'original_preparation_family'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
records=[]
for p in (root/'captures').glob('*.prelaunch.json'):
    pre=json.loads(p.read_bytes());post=json.loads(p.with_name(p.name.replace('.prelaunch.json','.post.json')).read_bytes())
    assert post['prelaunch_sha256']==sha(p) and post['returncode']==0
    for desc in pre['sources']:
        f=pathlib.Path(desc['path']);assert f.stat().st_size==desc['bytes'] and sha(f)==desc['sha256']
    assert set(pre['environment'])=={'PATH','LANG','LC_ALL','PYTHONHASHSEED','PYTHONDONTWRITEBYTECODE','PYTHONIOENCODING'}
    for stream in ('stdout','stderr'):
        f=p.with_name(p.name.replace('.prelaunch.json','.'+stream))
        assert f.stat().st_size==post[stream]['bytes'] and sha(f)==post[stream]['sha256']
    records.append({'capture':p.name.removesuffix('.prelaunch.json'),'child_pid':post['child_pid'],
                    'capture_pid':post['capture_pid'],'prelaunch_utc':pre['prelaunch_utc'],
                    'ended_utc':post['ended_utc'],'source_sha256':pre['sources'][1]['sha256']})
assert len(records)==5
author=json.loads((root/'reproduction/verification.json').read_bytes());assert author['assertions_passed']==6665
assert (root/'reproduction/verification.json').read_bytes()==(source/'original/verification.json').read_bytes()
results=[json.loads((root/n).read_bytes()) for n in ('controls_results.json','additional_controls_results.json','boundary_controls_results.json')]
assert sum(results[0]['counts'].values())==45547
assert results[1]['assertions_passed']==results[2]['assertions_passed']==15
assert len(results[0]['interval_certificates'])==208
index=json.loads((source/'SCIENCE_INDEX.json').read_bytes());assert len(index)==23
for name,d in index.items():
    p=source/'original'/name;assert p.stat().st_size==d['bytes'] and sha(p)==d['sha256']
    assert stat.S_ISREG(p.lstat().st_mode) and p.stat().st_mode&0o7777==0o444
external=[]
for n in ('INDEX.json','READY.json','SCIENCE_INDEX.json','ORIGINAL_AUTHENTICATION.json','SOURCE_ACCOUNTING.json'):
    p=source/n;external.append({'path':str(p),'bytes':p.stat().st_size,'sha256':sha(p),'mode_07777':oct(p.stat().st_mode&0o7777)})
manifest=source/'ROOT_MANIFEST.json'
if manifest.exists():
    m=json.loads(manifest.read_bytes());external.append({'path':str(manifest),'bytes':manifest.stat().st_size,
              'sha256':sha(manifest),'operator':m['operator'],'closed_pid':m['pid'],'closed_utc':m['utc']})
out={'operator':'PR59 mathematical subagent','pid':os.getpid(),'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
     'captures_verified':records,'author_assertions_reproduced':6665,'independent_assertions_passed':45577,
     'complete_finite_interval_certificates':208,'original_science_bodies_readonly_hash_verified':23,
     'external_source_pins':external,'external_SOURCE_ROOT_manifest_present':manifest.exists(),
     'limits':'Dated external pins, no original SOURCE or ROOT custody credit; no original budget change.'}
(root/'evidence_readback.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
