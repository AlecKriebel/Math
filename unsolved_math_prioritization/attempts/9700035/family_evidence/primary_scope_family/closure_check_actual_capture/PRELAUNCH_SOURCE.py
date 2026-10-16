#!/usr/bin/env python3
"""Read-only final input/capture checks; never imports submitted helpers."""
import datetime, hashlib, json, pathlib, re

B=pathlib.Path(__file__).resolve().parent
A=B.parent
R=A.parents[2]

def sha(data):
    return hashlib.sha256(data).hexdigest()

def pairs(items):
    out={}
    for key,value in items:
        if key in out:
            raise ValueError('Duplicate JSON key: '+key)
        out[key]=value
    return out

def read(p):
    return json.loads(p.read_bytes(),object_pairs_hook=pairs)

def file_rows(folder,exclude_self=True,excluded_roots=()):
    rows=[]
    for p in sorted(folder.rglob('*')):
        assert not p.is_symlink(), str(p)
        if p.is_dir():
            continue
        assert p.is_file(),str(p)
        q=p.relative_to(folder).as_posix()
        if (exclude_self and q=='FIRST_PARTY_MANIFEST.json') or q.split('/')[0] in excluded_roots:
            continue
        data=p.read_bytes()
        rows.append({'path':q,'size':len(data),'sha256':sha(data)})
    return rows

def strict_rows(rows):
    names=[]
    for row in rows:
        assert type(row) is dict and set(row)=={'path','size','sha256'}
        p=row['path'];assert type(p) is str and p and not p.startswith('/')
        assert '\\' not in p and all(x not in ('','.', '..') for x in p.split('/'))
        assert pathlib.PurePosixPath(p).as_posix()==p
        assert type(row['size']) is int and row['size']>=0
        assert type(row['sha256']) is str and re.fullmatch('[0-9a-f]{64}',row['sha256'])
        names.append(p)
    assert names==sorted(names) and len(names)==len(set(names))

def main():
    assert R==pathlib.Path('/Users/alec/Documents/Math')
    snapshot=(A/'snapshot_manifest.json').read_bytes()
    assert sha(snapshot)=='feef9bf6433c165296d3cdea883ceb74440048e17ff87f03ef636a99338cb3e6'
    original=read(A/'snapshot_manifest.json');assert len(original['files'])==16
    for row in original['files']:
        data=(A/'source_snapshot'/row['path']).read_bytes()
        assert type(row['size']) is int and len(data)==row['size'] and sha(data)==row['sha256']
    old=[]
    for suffix,pin,count in [
        ('pr40_2814/primary_scope_family','adaa4da7629209ddba020851c54e4a2098147983c26acb7f2dbbfc159dda5d42',97),
        ('pr39_9500008/current_preparation_static_adversary_family','51a9d901e4a64a28b6d53e7a14a329151e7806ecfd05c99c8f7da3803cc36f23',8),
        ('pr40_2814/root_audit_SQL_qualification_family','fc5bb1b6f6d967defcf007f4caa95fafd0b3a074a79f5090fe59d714470c98c2',5)]:
        folder=A.parent/suffix;data=(folder/'FIRST_PARTY_MANIFEST.json').read_bytes();assert sha(data)==pin
        m=read(folder/'FIRST_PARTY_MANIFEST.json');assert len(m['files'])==count;strict_rows(m['files'])
        excluded=m.get('excluded_root_directories',[])
        assert file_rows(folder,excluded_roots=excluded)==m['files']
        old.append({'path':suffix,'manifest_sha256':pin,'members_unchanged':count})
    captures=[]
    for folder,sourcepin,checks in [
        ('data_audit_actual_capture','338849247b77a782f7515eca9408936cfa159db1ee561ff75be743b4e2b3c106',None),
        ('finite_controls_actual_capture','ffc1a3337f2ec4a5c5005f2f4083f9c3c37940b4342c5bd28697e72d1fb08b6f',1307),
        ('finite_controls_actual_capture_v2','6b66fa75e72f2f6760d5d5099e026d0d9af41a8df7fdb57685c7de35958cfaa7',1326)]:
        d=B/folder;c=read(d/'CAPTURE.json');s=(d/'PRELAUNCH_SOURCE.py').read_bytes()
        assert c['source_sha256']==sourcepin==sha(s)
        assert type(c['source_size']) is int and c['source_size']==len(s)
        assert c['actual_execution'] is True and c['completed'] is True and c['status']=='PASS'
        assert type(c['exit_code']) is int and c['exit_code']==0
        for channel in ('stdout','stderr'):
            row=c[channel];data=(d/row['path']).read_bytes()
            assert type(row['size']) is int and len(data)==row['size'] and sha(data)==row['sha256']
        if checks is not None:
            result=read(d/'RESULT.json');assert type(result['passed']) is int and result['passed']==checks==len(result['checks'])
            assert type(result['failed']) is int and result['failed']==0
        captures.append({'path':folder,'actual_source_sha256':sourcepin,'exit_code':0,'finite_checks':checks})
    result=read(B/'RESULT.json')
    for key,value in [('original_substantive_attempts',2),('substantive_attempt_limit',5),('new_substantive_attempts',0),('audit_attempts_added',0),('review_completion_estimate_percent',100)]:
        assert type(result[key]) is int and result[key]==value
    for key in ['historical_actual_model_verified','historical_actual_reasoning_verified','current_actual_model_verified','current_actual_reasoning_verified','own_execution_prelaunch_version_record','current_full_target_completion_certificate']:
        assert key in result and result[key] is None
    for key in ['original_helpers_imported','original_helpers_executed','full_original_resolution_claimed','novel_result_claimed','paper_or_DOI_warranted','native_or_canonical_writes','Git_or_remote_writes','external_human_contact']:
        assert key in result and result[key] is False
    assert result['mandatory_submitted_PROOF_repairs']==[] and result['submitted_PROOF_math_defect_found'] is False
    assert result['status']=='PASS_QUALIFIED_UNSOLVED_PARTIAL'
    assert (B/'.gitignore').read_bytes()==b'/foreign_primary_cache/\n'
    foreign=read(B/'FOREIGN_CACHE_MANIFEST.json');strict_rows(foreign['files'])
    assert file_rows(B/'foreign_primary_cache',exclude_self=False)==foreign['files']
    parsed=[]
    for p in B.rglob('*.json'):
        if p.relative_to(B).parts[0]=='foreign_primary_cache':
            continue
        read(p);parsed.append(p.relative_to(B).as_posix())
    print(json.dumps({'schema':1,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS_READONLY_PRECLOSURE_BINDINGS','snapshot_original16_unchanged':True,'old_closed_families_unchanged':old,'actual_own_capture_contracts_checked':captures,'strict_required_int_bool_present_null_checks_passed':True,'preclosure_owned_JSON_all_parsed_no_duplicate_keys':sorted(parsed),'foreign_exact_files':len(foreign['files']),'foreign_cache_separate_not_first_party':True,'proposal_helper_import_or_execution':False,'shared_native_Git_remote_writes':False,'new_substantive_attempts':0,'audit_attempts_added':0,'scope':'Read-only preclosure bindings check. Final manifest is constructed and independently checked after this actual capture; no future packet or original helper verdict certified.'},indent=2))

if __name__=='__main__':
    main()
