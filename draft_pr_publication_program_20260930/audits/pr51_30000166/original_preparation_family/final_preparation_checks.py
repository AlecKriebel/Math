"""Read only completed preparation evidence; no mathematical acceptance or native authority."""
import datetime
import hashlib
import json
from pathlib import Path

F=Path(__file__).resolve().parent
H='8006dd5f134ad0a2fa930e7278d3cb17945f4201'
B='c6975ca76f9f667f1250ba403d0e6da2aafe14d0'
CURRENT='final_preparation_checks'
checks=0


def check(condition,label):
    global checks
    assert condition,label
    checks+=1


def sha(b):return hashlib.sha256(b).hexdigest()


def pairs(ps):
    d={}
    for k,v in ps:
        assert k not in d,('duplicate JSON key',k)
        d[k]=v
    return d


def read(p):return json.loads(p.read_bytes(),object_pairs_hook=pairs)


def typed(a,b):
    check(type(a) is type(b),'recursive type')
    if isinstance(a,dict):
        check(a.keys()==b.keys(),'recursive keys')
        for k in a:typed(a[k],b[k])
    elif isinstance(a,list):
        check(len(a)==len(b),'recursive list length')
        for x,y in zip(a,b):typed(x,y)
    else:check(a==b,'recursive value')


def binding(q):
    p=Path(q['path']);b=p.read_bytes()
    check(p.is_relative_to(F),'capture identity remains in family')
    check(len(b)==q['bytes'] and sha(b)==q['sha256'],'capture body binding')


def capture(cap):
    p=read(cap/'PRELAUNCH.json');s=read(cap/'STARTED.json');c=read(cap/'COMPLETE.json')
    check(p['schema']=='pr51-private-command-prelaunch/v1','prelaunch schema')
    check(s['schema']=='pr51-private-command-started/v1','started schema')
    check(c['schema']=='pr51-private-command-completed/v1','completed schema')
    check(p['child_pid'] is None and p['completed'] is False,'prelaunch no invented child')
    check(type(p['wrapper_pid']) is int and type(s['child_pid']) is int,'literal actual PIDs')
    check(c['child_pid']==s['child_pid'] and c['completed'] is True,'actual completed PID')
    check(p['argv']==s['argv']==c['argv'] and p['cwd']==s['cwd']==c['cwd'],'literal argv/cwd')
    times=[datetime.datetime.fromisoformat(q['utc']) for q in (p,s,c)]
    check(times==sorted(times) and all(t.tzinfo is not None for t in times),'prelaunch/start/completion chronology')
    binding(p['operator'])
    check(Path(p['operator']['path'])==cap/'OPERATOR_PRELAUNCH.py','literal operator copy')
    for q in p['sources']:
        binding(q['saved'])
        check(q['saved']['sha256']==q['original']['sha256'] and q['saved']['bytes']==q['original']['bytes'],'prelaunch source literal copy')
        check(Path(q['saved']['path']).parent==cap,'source copy ownership')
    for k in ('prelaunch','started','stdout','stderr'):
        binding(c[k])
    check(c['exit_code']==(128 if cap.name=='original_object' else 0),'actual expected exit code')
    check(type(c['elapsed_seconds']) is float and c['elapsed_seconds']>=0,'actual elapsed duration')
    return {'name':cap.name,'child_pid':c['child_pid'],'utc_started':s['utc'],
            'utc_completed':c['utc'],'exit_code':c['exit_code'],
            'stdout_bytes':c['stdout']['bytes'],'stderr_bytes':c['stderr']['bytes']}


def main():
    identity=read(F/'SNAPSHOT_IDENTITY.json');snap=F/'source_snapshot'
    check(identity['original_head']==H and identity['base']==B==identity['merge_base'],'fixed identity')
    check(identity['original_head_tree']=='a92db42bb58b7ca5bef852a548a77059dbf07276','head tree')
    files=identity['files'];names=[q['snapshot_relative_path'] for q in files]
    check(names==sorted(set(names)) and len(names)==15==identity['science_files_count'],'15 unique science files')
    check(names==sorted(p.relative_to(snap).as_posix() for p in snap.rglob('*') if p.is_file()),'complete literal archive')
    jsons=0;total=0
    for q in files:
        b=(snap/q['snapshot_relative_path']).read_bytes();total+=len(b)
        check(len(b)==q['bytes'] and sha(b)==q['sha256'],'snapshot SHA256/bytes')
        check(hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==q['git_blob_sha1'],'literal Git blob identity')
        check(q['git_mode']=='100644','original Git mode')
        if q['snapshot_relative_path'].endswith('.json'):read(snap/q['snapshot_relative_path']);jsons+=1
    check(total==53495==identity['science_bytes'] and jsons==8,'archive total and all original JSON')
    binding(identity['capture_diff'])
    diff=(F/'captures/pr_full_diff/STDOUT.bin').read_bytes()
    check(len(diff)==61415 and sha(diff)=='cd347fdfcf118cf10d59151d3a5c75e14edfab10add0ef2e93ef8525271aa951','complete diff pin')
    check(diff.count(b'diff --git ')==16==identity['changed_paths_count'],'full diff path count')
    compare=read(F/'captures/pr_compare/STDOUT.bin')
    check(compare['head_sha']==H and compare['base_sha']==B==compare['merge_base_sha'],'comparison identity')
    check(len(compare['files'])==16 and compare['total_commits']==3,'exact comparison counts')
    api={q['filename']:q for q in compare['files']}
    for q in files:
        a=api[q['repository_path']]
        check(a['sha']==q['git_blob_sha1'] and a['status']=='added' and a['deletions']==0,'all science added API identities')
    contents=read(F/'captures/science_directory_quoted/STDOUT.bin')+read(F/'captures/review_directory/STDOUT.bin')
    api_files={q['path']:q for q in contents if q['type']=='file'}
    check(set(api_files)=={q['repository_path'] for q in files},'complete contents directories')
    for q in files:
        a=api_files[q['repository_path']]
        check(a['sha']==q['git_blob_sha1'] and a['size']==q['bytes'],'contents size/blob')
    for name in ('pr_metadata','pr_metadata_final'):
        q=read(F/'captures'/name/'STDOUT.bin')
        check(q['headRefOid']==H and q['baseRefOid']==B and q['state']=='OPEN' and q['isDraft'] is True,'fresh read-only remote original')
    check((F/'captures/main_identity/STDOUT.bin').read_bytes()==b'main\n','main observation')
    provenance=read(snap/'provenance.json');summary=read(snap/'independent_review/review_summary.json')
    check(provenance['source_status_sha256']==sha((snap/'SOURCE_STATUS.md').read_bytes()),'original provenance SOURCE body')
    for key,path in (('source_status_sha256','SOURCE_STATUS.md'),('review_sha256','independent_review/REVIEW.md'),('independent_checker_sha256','independent_review/independent_checks.py'),('independent_results_sha256','independent_review/independent_results.json')):
        check(summary[key]==sha((snap/path).read_bytes()),'historical review metadata body pin')
    for cap_name,helper,result,private,n in (
        ('author_private_replay','verify.py','verification.json','private_replays/author/verify.py',2837),
        ('historical_independent_private_replay','independent_review/independent_checks.py','independent_review/independent_results.json','private_replays/historical_independent/independent_checks.py',35980)):
        check((F/private).read_bytes()==(snap/helper).read_bytes(),'unchanged helper bytes')
        out=(F/'captures'/cap_name/'STDOUT.bin').read_bytes();expected=(snap/result).read_bytes()
        check(out==expected,'literal complete replay stdout')
        typed(read(F/'captures'/cap_name/'STDOUT.bin'),read(snap/result))
        q=read(F/'captures'/cap_name/'STDOUT.bin')
        check(q['assertions']==n and q['status']=='PASS','actual replay assertions')
        check((F/'captures'/cap_name/'STDERR.bin').read_bytes()==b'','complete empty stderr')
    for key,name,original in (('30000166','selected_catalog_target','source_record.json'),('30000167','selected_catalog_duplicate','duplicate_source_record.json')):
        q=read(F/'captures'/name/'STDOUT.bin');source=read(snap/original)
        check(q['selected_count']==1 and q['parameters']==[key] and q['raw_row']['key']==key,'only selected catalog row')
        typed(q['parsed_payload'],source)
        typed(json.loads(q['raw_row']['payload'],object_pairs_hook=pairs),source)
        check('prior_report' not in source and 'prior_report' not in q['parsed_payload'],'literal prior_report absent')
        check(q['raw_row']['report']=='{}' and q['report_sql_null'] is False and q['parsed_report']=={},'SQL text{} versus absent/NULL')
    ledger=read(snap/'turns.json')
    check(type(ledger) is dict and ledger['substantive_proof_attempts']==0 and ledger['budget']==5 and len(ledger['events'])==2,'original one object ledger0/5')
    boundary=read(F/'SELECTED_NATIVE_BOUNDARY.json')
    check(boundary['parsed_rows']['30000166']['status']=='queued' and boundary['parsed_rows']['30000166']['turns']=='0/5','selected current queue')
    check(boundary['selected_literal_rows']['30000167']==[] and boundary['duplicate_queue_row_present'] is False,'duplicate queue absent')
    state=read(F/'PREPARATION_STATUS.json')
    check(state['fresh_independent_math_verdict'] is None and state['complete_imported_theorem_independently_certified'] is False,'no inherited mathematical acceptance')
    check(state['root_closure_performed'] is False and state['production_execution_approved'] is False and state['publication_approved'] is False,'no future authority')
    completed=[]
    for cap in sorted((F/'captures').iterdir()):
        if cap.name==CURRENT:continue
        if cap.name=='native_target_queue_locator':
            check(sorted(p.name for p in cap.iterdir())==['OPERATOR_PRELAUNCH.py','PRELAUNCH.json'],'honest original launch failure')
            binding(read(cap/'PRELAUNCH.json')['operator']);continue
        completed.append(capture(cap))
    check(not (F/'captures/science_directory').exists(),'shell failure did not create capture')
    print(json.dumps({'schema':'pr51-final-preparation-checks/v1',
        'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS_PREPARATION_EVIDENCE_ONLY',
        'checks_actual':checks,'archive_files':15,'archive_json_files':jsons,
        'archive_bytes':total,'completed_capture_count':len(completed),'completed_captures':completed,
        'retained_launch_failure_count':1,'retained_prelaunch_shell_failure_count':1,
        'current_check_capture_excluded_until_its_child_exit':CURRENT,
        'independent_mathematical_acceptance':None,'future_authority':False},indent=2))


if __name__=='__main__':main()
