#!/usr/bin/python3
import datetime,hashlib,importlib.util,json,pathlib
own=pathlib.Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('family_readonly_checks',own/'close_family.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
rows=m.captures()
assert len(rows)==11
v=json.loads((own/'VERDICT.json').read_bytes())
assert v['verdict']=='PASS_CREDITED_KNOWN_UNRESTRICTED_REFLECTION_CRITERION' and v['mandatory_mathematical_corrections']==[]
for name,count in [('hyperbolic_results.json',25),('distance_results.json',3)]:
    d=json.loads((own/name).read_bytes());assert d['passed']==count==len(d['checks']) and d['failed']==0 and all(v=='PASS' for v in d['checks'].values())
deleted=json.loads((own/'PRIMARY_DELETION.json').read_bytes());assert deleted['removed_file_count']==14 and deleted['directory_absent_after'] is True
assert not pathlib.Path(json.loads((own/'PRIMARY_IDENTITIES.json').read_bytes())['temporary_directory']).exists()
assert not (own/'SELF_MANIFEST.json').exists(),'Family closure must await ROOT after child exit'
assert not any(p.suffix.lower() in ['.pdf','.png','.jpg','.html','.sqlite','.db'] for p in own.rglob('*') if p.is_file())
read=json.loads((own/'CANDIDATE_READ_RECEIPT.json').read_bytes())
for f in read['files']:
    p=own.parent/'source_snapshot'/f['path'];assert p.stat().st_size==f['bytes'] and hashlib.sha256(p.read_bytes()).hexdigest()==f['sha256']
result={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'completed_captures_checked_before_this_final_launch_completed':len(rows),'captures':rows,'fresh_controls':28,'candidate_bytes_unchanged':True,'foreign_primary_directory_absent':True,'foreign_bodies_in_family':False,'family_manifest_absent_wait_ROOT':True,'scope':'This final command has an additional actual capture; ROOT closer independently verifies all completed capture records after child exit.'}
(own/'FINAL_ARTIFACT_RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'checked_completed_captures':len(rows),'fresh_controls':28,'all_verified':True,'closure':'WAIT_ROOT_AFTER_CHILD_EXIT'}))
