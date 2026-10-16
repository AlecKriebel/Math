#!/usr/bin/env python3
"""Read-only checks of selected original pins and genuine own control capture."""
import hashlib,json,pathlib,stat
root=pathlib.Path(__file__).resolve().parent
pins=json.loads((root/'EXTERNAL_SOURCE_PINS.json').read_bytes())
checks=0
for item in pins['selected_external_files']:
 p=pathlib.Path(item['path']);s=p.lstat();b=p.read_bytes()
 assert stat.S_ISREG(s.st_mode) and not stat.S_ISLNK(s.st_mode)
 assert len(b)==item['bytes'] and hashlib.sha256(b).hexdigest()==item['sha256']
 checks+=1
account=json.loads(pathlib.Path(pins['accounting_path']).read_bytes())
assert account['head']=='b5a4829365f2a0bd5f42b7653c5cfacfa6b01d85'
assert len(account['git_scientific_modes'])==10 and all(v['git_mode']=='100644' for v in account['git_scientific_modes'])
assert account['prior_report']['upstream_value_absent'] is True
assert account['prior_report']['SQL_empty_object_is_missing_report_join_fallback'] is True
assert account['new_mathematical_attempts']==0 and account['new_mathematical_review_credit']==0
assert account['raw_problem_equals_original_source_record'] is True
original=pathlib.Path(pins['original_path'])
assert isinstance(json.loads((original/'prior_report.json').read_bytes()),dict)
assert json.loads(pathlib.Path(pins['raw_prior_path']).read_bytes()) is None
assert pathlib.Path(pins['SQL_path']).read_bytes()==b'{}'
assert not list(original.rglob('*.py'))
checks+=10
pre=(root/'captures/relation_controls.prelaunch.json').read_bytes()
post=json.loads((root/'captures/relation_controls.post.json').read_bytes())
assert hashlib.sha256(pre).hexdigest()==post['prelaunch_sha256'] and post['returncode']==0
for item in json.loads(pre)['sources']:
 b=pathlib.Path(item['path']).read_bytes()
 assert len(b)==item['bytes'] and hashlib.sha256(b).hexdigest()==item['sha256']
 checks+=1
for name in ('stdout','stderr'):
 b=(root/('captures/relation_controls.'+name)).read_bytes()
 assert len(b)==post[name]['bytes'] and hashlib.sha256(b).hexdigest()==post[name]['sha256']
 checks+=1
result=json.loads((root/'captures/relation_controls.stdout').read_bytes())
assert result['assertions_passed']==774 and sum(result['counts'].values())==774
assert result['source_sha256']==hashlib.sha256((root/'relation_controls.py').read_bytes()).hexdigest()
assert isinstance(post['child_pid'],int) and post['child_pid']==55556
checks+=4
print(json.dumps({'source_and_capture_check_groups':checks,'independent_control_assertions':774,'original_author_checker_present':False,'new_author_attempts':0,'raw_prior':'absent; selected null; SQL TEXT empty-object fallback; original dictionary placeholder','ROOT_authority_inferred':False},indent=2))
