#!/usr/bin/env python3
"""Compact full-body source integrity checks; no mathematical acceptance."""
from pathlib import Path
import hashlib,json,os,stat
HERE=Path(__file__).resolve().parent
SELF='SELF_MANIFEST.json'
EXCLUDED={'INDEX.json','READY.json',SELF}
def sha(b):return hashlib.sha256(b).hexdigest()
def load(p):return json.loads(p.read_bytes())
def pin(p):
    s=p.lstat();assert stat.S_ISREG(s.st_mode) and not p.is_symlink()
    b=p.read_bytes();return {'path':str(p),'bytes':len(b),'sha256':sha(b),'mode':stat.S_IMODE(s.st_mode)}
def inventory(allow_self=False):
    files=[];dirs=[]
    for root,names,leaf in os.walk(HERE,followlinks=False):
        p=Path(root);assert not p.is_symlink();dirs.append({'path':str(p),'mode':stat.S_IMODE(p.lstat().st_mode)})
        for name in names:assert not (p/name).is_symlink()
        for name in leaf:
            q=p/name;assert not q.is_symlink()
            if name==SELF and q==HERE/SELF:
                assert allow_self,'SELF_MANIFEST must be absent before ROOT closure'
                continue
            files.append(pin(q))
    return sorted(files,key=lambda x:x['path']),sorted(dirs,key=lambda x:x['path'])
def validate_content():
    checks=0
    auth=load(HERE/'ORIGINAL_AUTHENTICATION.json')
    assert auth['original_head']=='28c6ce952d6027fb995bbd2d79a8c9647cc8b844';checks+=1
    assert auth['actual_merge_base_oid']==load(HERE/'captures/actual_merge_base/stdout.bin')['merge_base_commit']['sha'];checks+=1
    assert len(auth['original_science_files'])==19 and auth['complete_diff_file_count']==20;checks+=1
    expected=set()
    for row in auth['original_science_files']:
        p=HERE/'original'/row['relative_path'];b=p.read_bytes();expected.add(p)
        assert str(p)==row['local_path'] and len(b)==row['bytes'] and sha(b)==row['sha256'];checks+=1
        assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==row['git_blob_sha1'];checks+=1
        assert row['git_mode']=='100644';checks+=1
    assert {p for p in (HERE/'original').rglob('*') if p.is_file()}==expected;checks+=1
    diff=(HERE/'FULL_PR_DIFF.patch').read_bytes()
    assert len(diff)==auth['full_diff']['bytes'] and sha(diff)==auth['full_diff']['sha256'];checks+=1
    assert diff.count(b'\ndiff --git ')+int(diff.startswith(b'diff --git '))==20;checks+=1
    assert auth['original_queue_diff'].encode() in diff;checks+=1
    for name in ['root_tree','tree_unsolved_math_prioritization','tree_attempts','tree_30002061','review_tree']:
        tree=load(HERE/'captures'/name/'stdout.bin');assert not tree['truncated']
        body=b''.join(i['mode'].lstrip('0').encode()+b' '+i['path'].encode()+b'\0'+bytes.fromhex(i['sha'])
             for i in sorted(tree['tree'],key=lambda i:(i['path']+('/' if i['type']=='tree' else '')).encode()))
        assert hashlib.sha1(b'tree '+str(len(body)).encode()+b'\0'+body).hexdigest()==tree['sha'];checks+=1
    account=load(HERE/'SOURCE_ACCOUNTING.json')
    assert account['raw_report_key_present'] is False and account['raw_report_interpretation']=='ABSENT; no raw value';checks+=1
    assert account['SQL_selected_row']['report_literal']=='{}' and account['SQL_selected_row']['report_is_SQL_NULL'] is False;checks+=1
    assert account['archived_prior_report_literal']=='null\n';checks+=1
    assert account['native_state_key_present'] is False and '| queued | 0/5 |' in account['native_queue_literal'];checks+=1
    assert account['original_draft_proposes']=={'Status':'unsolved','Turns':'1/5','substantive_routes_used':1};checks+=1
    assert account['new_response_or_route_increment'] is False;checks+=1
    assert json.loads(account['SQL_selected_row']['payload_literal'])==load(HERE/'original/source_record.json');checks+=1
    for d in sorted((HERE/'captures').iterdir()):
        if not d.is_dir() or not (d/'CAPTURE.json').exists():continue
        c=load(d/'CAPTURE.json')
        assert c['child_pid']>0 and c['operator_pid']>0 and c['utc_start']<=c['utc_end'];checks+=1
        assert c['operator_unchanged_after'] is True and c['sources_unchanged_after'] is True;checks+=1
        assert isinstance(c['argv'],list) and c['argv'] and c['ROOT_approval'] is False;checks+=1
        assert c['native_Git_ref_or_remote_mutation'] is False;checks+=1
        for key in ['stdout','stderr']:
            b=(d/(key+'.bin')).read_bytes();assert {'bytes':len(b),'sha256':sha(b)}==c[key];checks+=1
        b=(d/'operator_prelaunch.py').read_bytes();assert {'bytes':len(b),'sha256':sha(b)}==c['operator'];checks+=1
        for src in c['sources']:
            p=Path(src['original']);saved=Path(src['saved']);assert p.is_relative_to(HERE) and saved.is_relative_to(HERE)
            b=p.read_bytes();assert b==saved.read_bytes() and len(b)==src['bytes'] and sha(b)==src['sha256'];checks+=1
        assert c['exit_code']==(128 if d.name=='local_original_object' else 0);checks+=1
    reproduced=load(HERE/'REPRODUCTION.json');assert reproduced['new_math_verdict'] is None and reproduced['ROOT_acceptance'] is False;checks+=1
    for job in reproduced['jobs']:
        c=load(Path(job['capture']));assert c['child_pid']==job['child_pid'] and c['exit_code']==0 and len(c['sources'])==2;checks+=1
        for rec in job['receipts']:
            a=Path(rec['private']['path']);b=Path(rec['exact_original_reference']['path']);assert a.read_bytes()==b.read_bytes();checks+=1
    v=load(HERE/'original/verification.json');old=load(HERE/'original/review/submitted_verification.json')
    assert v['passed']==4200 and v['failed']==0 and len(v['cases'])==27 and v['glued_region_cases']==6;checks+=1
    assert {k for k in set(v)|set(old) if v.get(k)!=old.get(k)}=={'partial_sha256'};checks+=1
    ind=load(HERE/'original/review/independent_results.json')
    assert ind['passed']==59718 and ind['failed']==0 and ind['disk_target_cases']==ind['gluing_cases']==387 and ind['interval_cases']==30;checks+=1
    return checks
def validate_ready(allow_self=False):
    files,dirs=inventory(allow_self);index=load(HERE/'INDEX.json');ready=load(HERE/'READY.json')
    assert sha((HERE/'INDEX.json').read_bytes())==ready['index_sha256']
    payload=[r for r in files if Path(r['path']).name not in EXCLUDED or Path(r['path']).parent!=HERE]
    assert payload==index['files'] and dirs==index['directories']
    assert len(payload)==ready['payload_file_count'] and sum(r['bytes'] for r in payload)==ready['payload_total_bytes']
    assert len(files)==ready['complete_prepared_file_count']<=220 and sum(r['bytes'] for r in files)<=1500000
    assert all(r['mode']==0o444 for r in files) and all(r['mode']==0o755 for r in dirs)
    assert ready['source_preparation_completion_percent']==100 and ready['ROOT_personal_read_attestation'] is False
    assert ready['new_mathematical_verdict'] is None and ready['native_acceptance_authority'] is False
    for row in index['immutable_external_references']:
        assert pin(Path(row['path']))==row
    for key,name in [('common_source_sha256','packet_common.py'),('closer_source_sha256','ROOT_close_source.py'),('reader_source_sha256','ROOT_read_closed_source.py')]:
        assert ready[key]==sha((HERE/name).read_bytes())
    return files,dirs,validate_content()
