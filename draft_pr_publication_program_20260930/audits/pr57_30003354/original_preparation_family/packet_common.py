#!/usr/bin/env python3
"""Compact full-byte SOURCE integrity; no mathematical or native acceptance."""
from pathlib import Path
import hashlib,json,os,stat
HERE=Path(__file__).resolve().parent;SELF='SELF_MANIFEST.json'
EXCLUDED={'INDEX.json','READY.json',SELF}
def sha(b):return hashlib.sha256(b).hexdigest()
def load(p):return json.loads(p.read_bytes())
def pin(p):
    s=p.lstat();assert stat.S_ISREG(s.st_mode) and not p.is_symlink()
    b=p.read_bytes();return {'path':str(p),'bytes':len(b),'sha256':sha(b),'mode':stat.S_IMODE(s.st_mode)}
def inventory(allow_self=False):
    files=[];dirs=[]
    for root,names,leaves in os.walk(HERE,followlinks=False):
        p=Path(root);assert not p.is_symlink();dirs.append({'path':str(p),'mode':stat.S_IMODE(p.lstat().st_mode)})
        for n in names:assert not(p/n).is_symlink()
        for n in leaves:
            q=p/n;assert not q.is_symlink()
            if q==HERE/SELF:
                assert allow_self,'SELF_MANIFEST must be absent before ROOT closure';continue
            files.append(pin(q))
    return sorted(files,key=lambda x:x['path']),sorted(dirs,key=lambda x:x['path'])
def validate_content():
    checks=0;auth=load(HERE/'ORIGINAL_AUTHENTICATION.json')
    assert auth['original_head']=='4ecc453d6f9ec2e64cdb2d4b41c018fffbe85b29';checks+=1
    compare=load(HERE/'captures/actual_merge_base/stdout.bin')
    assert auth['actual_merge_base_oid']==compare['merge_base_commit']['sha']==auth['github_base_oid']=='c6975ca76f9f667f1250ba403d0e6da2aafe14d0';checks+=1
    assert auth['github_base_equals_actual_merge_base'] is True;checks+=1
    assert len(auth['original_science_files'])==17 and auth['complete_diff_file_count']==18;checks+=1
    trees={}
    for row in auth['authenticated_trees']:
        path=row['path'];name='root_tree' if not path else 'tree_'+Path(path).name
        tree=load(HERE/'captures'/name/'stdout.bin');assert not tree['truncated'];checks+=1
        body=b''.join(i['mode'].lstrip('0').encode()+b' '+i['path'].encode()+b'\0'+bytes.fromhex(i['sha'])
          for i in sorted(tree['tree'],key=lambda i:(i['path']+('/' if i['type']=='tree' else '')).encode()))
        assert hashlib.sha1(b'tree '+str(len(body)).encode()+b'\0'+body).hexdigest()==tree['sha']==row['sha'];checks+=1
        assert row['entry_count']==len(tree['tree']) and row['full_binary_tree_hash_authenticated'] is True;checks+=1
        trees[path]=tree
    assert len(trees)==6;checks+=1
    for path,tree in trees.items():
        if not path:continue
        parent=str(Path(path).parent);parent='' if parent=='.' else parent
        rows=[r for r in trees[parent]['tree'] if r['path']==Path(path).name]
        assert len(rows)==1 and rows[0]['type']=='tree' and rows[0]['sha']==tree['sha'];checks+=1
    commit=load(HERE/'captures/head_commit/stdout.bin')
    assert commit['sha']==auth['original_head'] and commit['tree']['sha']==auth['root_tree']==trees['']['sha'];checks+=1
    changed=load(HERE/'captures/changed_files/stdout.bin');assert len(changed)==18;checks+=1
    expected=set()
    for row in auth['original_science_files']:
        p=HERE/'original'/row['relative_path'];b=p.read_bytes();expected.add(p)
        assert str(p)==row['local_path'] and len(b)==row['bytes'] and sha(b)==row['sha256'];checks+=1
        assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==row['git_blob_sha1'];checks+=1
        assert row['git_mode']=='100644';checks+=1
        parent=str(Path(row['repository_path']).parent);leaf=Path(row['repository_path']).name
        matches=[r for r in trees[parent]['tree'] if r['path']==leaf]
        assert len(matches)==1 and matches[0]['sha']==row['git_blob_sha1'] and matches[0]['mode']==row['git_mode'];checks+=1
        matches=[r for r in changed if r['filename']==row['repository_path']]
        assert len(matches)==1 and matches[0]['sha']==row['git_blob_sha1'] and matches[0]['status']=='added';checks+=1
    assert {p for p in (HERE/'original').rglob('*') if p.is_file()}==expected;checks+=1
    q=[r for r in changed if r['filename']=='unsolved_math_prioritization/QUEUE.md']
    assert len(q)==1 and q[0]['sha']==auth['original_queue_destination_blob_sha1'];checks+=1
    qtree=[r for r in trees['unsolved_math_prioritization']['tree'] if r['path']=='QUEUE.md']
    assert len(qtree)==1 and qtree[0]['sha']==q[0]['sha'];checks+=1
    diff=(HERE/'FULL_PR_DIFF.patch').read_bytes()
    assert len(diff)==auth['full_diff']['bytes']==85518 and sha(diff)==auth['full_diff']['sha256'];checks+=1
    assert diff==(HERE/'captures/full_original_diff/stdout.bin').read_bytes();checks+=1
    assert diff.count(b'\ndiff --git ')+int(diff.startswith(b'diff --git '))==18;checks+=1
    assert auth['original_queue_diff'].encode() in diff;checks+=1
    meta=load(HERE/'captures/current_pr_metadata/stdout.bin');api=load(HERE/'captures/api_pr_metadata/stdout.bin')
    assert meta['headRefOid']==api['head']['sha']==auth['original_head'];checks+=1
    assert meta['baseRefOid']==api['base']['sha']==auth['github_base_oid'];checks+=1
    assert meta['state']=='OPEN' and meta['isDraft'] is True and api['state']=='open' and api['draft'] is True;checks+=1
    assert (HERE/'captures/current_branch/stdout.bin').read_bytes()==b'main\n';checks+=1
    a=load(HERE/'SOURCE_ACCOUNTING.json');source=load(HERE/'original/source_record.json')
    assert a['raw_report_key_present'] is False and a['raw_report_interpretation']=='ABSENT; no raw value';checks+=1
    assert a['SQL_selected_row']['report_is_SQL_NULL'] is False and a['SQL_selected_row']['report_literal']=='{}';checks+=1
    assert a['archived_wrapper_upstream_report_field_present'] is False and 'upstream_report' not in source;checks+=1
    assert a['archived_separate_prior_report_file_present'] is False;checks+=1
    assert json.loads(a['SQL_selected_row']['payload_literal'])==source and a['original_problem_typed_equal_to_raw_and_SQL'] is True;checks+=1
    assert a['native_state_key_present'] is False and '| queued | 0/5 |' in a['native_queue_literal'];checks+=1
    assert a['original_draft_proposes']=={'Status':'claimed_solved','Turns':'1/5'};checks+=1
    assert a['original_status_file_present'] is False and a['original_status_literal_from_status_file'] is None and not(HERE/'original/status.json').exists();checks+=1
    assert a['original_turns_used']==1 and a['original_turn_limit']==5 and a['original_turn_log_entry_count']==1;checks+=1
    assert a['new_response_or_route_increment'] is False and a['native_mutation'] is False;checks+=1
    before=load(HERE/'SOURCE_ACCOUNTING_FAILED_ATTEMPT.json')
    for k in ['raw_report_key_present','SQL_selected_row','original_draft_proposes','original_turns_used','original_turn_limit']:
        assert before[k]==a[k];checks+=1
    assert b"KeyError: 'original_status_literal'" in (HERE/'captures/source_accounting/stderr.bin').read_bytes();checks+=1
    for d in sorted((HERE/'captures').iterdir()):
        if not d.is_dir() or not(d/'CAPTURE.json').exists():continue
        c=load(d/'CAPTURE.json');assert c['child_pid']>0 and c['operator_pid']>0 and c['utc_start']<=c['utc_end'];checks+=1
        assert c['operator_unchanged_after'] is True and c['sources_unchanged_after'] is True;checks+=1
        assert isinstance(c['argv'],list) and c['argv'] and c['ROOT_approval'] is False and c['native_Git_ref_or_remote_mutation'] is False;checks+=1
        for key in ['stdout','stderr']:
            b=(d/(key+'.bin')).read_bytes();assert {'bytes':len(b),'sha256':sha(b)}==c[key];checks+=1
        b=(d/'operator_prelaunch.py').read_bytes();assert {'bytes':len(b),'sha256':sha(b)}==c['operator'] and b==(HERE/'capture_command.py').read_bytes();checks+=1
        for r in c['sources']:
            original=Path(r['original']);saved=Path(r['saved']);assert original.is_relative_to(HERE) and saved.is_relative_to(HERE)
            b=original.read_bytes();assert b==saved.read_bytes() and len(b)==r['bytes'] and sha(b)==r['sha256'];checks+=1
        assert c['exit_code']==({'local_original_object':128,'source_accounting':1}.get(d.name,0));checks+=1
    rep=load(HERE/'REPRODUCTION.json');assert rep['new_math_verdict'] is None and rep['ROOT_acceptance'] is False;checks+=1
    assert rep['separate_archived_author_replay_process_claimed'] is False and len(rep['jobs'])==2;checks+=1
    for row in rep['frozen_author_replay_body_comparison']:
        assert Path(row['current']['path']).read_bytes()==Path(row['archived_author_replay']['path']).read_bytes();checks+=1
    for job in rep['jobs']:
        c=load(Path(job['capture']));assert c['child_pid']==job['child_pid'] and c['exit_code']==0;checks+=1
        assert len(c['sources'])==(2 if job['name']=='author_current' else 1);checks+=1
        b=Path(job['private_stdout_receipt']['path']).read_bytes()
        assert b==Path(job['exact_original_reference']['path']).read_bytes()==(Path(job['capture']).parent/'stdout.bin').read_bytes();checks+=1
    v=load(HERE/'original/verification.json');ind=load(HERE/'original/independent_review/independent_results.json')
    assert v['status']=='PASS' and v['assertions']==90 and len(v['checks'])==90 and v['sympy_version']=='1.14.0';checks+=1
    assert ind['status']=='PASS' and ind['exact_assertions']==136 and sum(ind['categories'].values())==136 and ind['categories']['scaled_profile_diagnostic']==98;checks+=1
    proof=(HERE/'original/CANDIDATE.md').read_bytes();provenance=load(HERE/'original/provenance.json');review=load(HERE/'original/independent_review/review_summary.json')
    assert sha(proof)==v['candidate_sha256']==provenance['candidate_sha256']==review['artifact_sha256']=='7f358fb1aaa73dc3cfd06c798c10f6afed65ee430b622b84b90f0554dd440e62';checks+=1
    assert b'pending separate adversarial review' in proof and b'Priority is unconfirmed' in proof;checks+=1
    assert sha((HERE/'original/verify.py').read_bytes())==review['submitted_verifier_sha256']=='dad7fc79034bb61fb869a81582cae21ebade0a49474f9c590cc145586dd8a04c';checks+=1
    assert sha((HERE/'original/independent_review/REVIEW.md').read_bytes())==review['report_sha256'];checks+=1
    turns=load(HERE/'original/turns.json');assert turns['substantive_proof_attempts']==1 and turns['budget']==5 and len(turns['turns'])==1;checks+=1
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
    assert index['immutable_external_references']==[]
    for key,name in [('common_source_sha256','packet_common.py'),('closer_source_sha256','ROOT_close_source.py'),('reader_source_sha256','ROOT_read_closed_source.py')]:
        assert ready[key]==sha((HERE/name).read_bytes())
    return files,dirs,validate_content()
