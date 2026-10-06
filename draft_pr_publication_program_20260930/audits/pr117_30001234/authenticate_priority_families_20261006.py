"""Authenticate sealed priority families and replay exact diagnostic controls."""
from pathlib import Path
import datetime, hashlib, json, os, subprocess
A=Path(__file__).resolve().parent
PY='/opt/homebrew/Cellar/python@3.14/3.14.6/Frameworks/Python.framework/Versions/3.14/bin/python3.14'
OUT=A/'ROOT_PRIORITY_FAMILY_AUTHENTICATION_20261006.json'
JOURNAL=A/'ROOT_PRIORITY_REPRODUCTION_PROCESS_JOURNAL_20261006.json'
events=[]
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def require(value,label):
    if not value:raise ValueError(label)
def sha(body):return hashlib.sha256(body).hexdigest()
def dump(path,data):path.write_text(json.dumps(data,indent=2,sort_keys=True)+'\n')
def pin(path):
    require(path.is_file() and not path.is_symlink(),'Regular sealed file required')
    body=path.read_bytes()
    return {'path':str(path.relative_to(A)),'bytes':len(body),'sha256':sha(body)}
families=[
 ('original_question_priority_adversary_20261006','1235924906c6fb09a18dcf1a324d06cbf42621c0c2c86758b8da0e2ce7f2d584',34,
 '762d4ba66ef866ebd8df4f4edf007b8f527c32bec96311b95d2e0bf7ae543f1b','priority_scope_checks.py',['--with-private-sources'],'--force-false',180,'guards'),
 ('determinantal_priority_adversary_20261006','851eae3623b022dc5b33003b410cc7431ef1d2a5126e826a382c1869840b1066',39,
 'd4b9bc3f1d389d7f2c838890bba56f908ef7f2785d89c319fb1a30e51d73d5f8','takagi_scope_checks.py',[],'--false-control',33,'explicit_exception_checks'),
 ('later_binomial_priority_adversary_20261006','f7832ca2499adef7307a9d84eecc435d32693571f7f231e5116d8f21ab4fae6e',26,
 '37f2f2017d8f878fcb2fd8692bf52f6af4b8518b8e6f811e391956f591b12c8f','priority_implication_controls.py',[],'--false-control',1210,'guard_count')]
require(not OUT.exists() and not JOURNAL.exists(),'Existing root actual run; inspect rather than repeat')
authenticated=[]
private_tokens={'private_sources','private_renders','private_backend','__pycache__'}
env={'PATH':'/usr/bin:/bin','LANG':'C','LC_ALL':'C','TZ':'UTC','__CF_USER_TEXT_ENCODING':'0x1F5:0x0:0x0'}
for name,manifest_hash,count,report_hash,code,extra,false_flag,checks,key in families:
    folder=A/name;manifest=folder/'OUTPUT_MANIFEST.json'
    require(sha(manifest.read_bytes())==manifest_hash,'Manifest hash changed: '+name)
    data=json.loads(manifest.read_text())
    members=data.get('members',data.get('files',data.get('public_members')))
    require(isinstance(members,list) and len(members)==count,'Manifest member count/schema: '+name)
    member_pins=[]
    for member in members:
        relative=member.get('path',member.get('relative_path'))
        require(relative and not Path(relative).is_absolute() and '..' not in Path(relative).parts,'Unsafe member path')
        require(not private_tokens.intersection(Path(relative).parts),'Private body in public manifest')
        current=pin(folder/relative)
        require(current['bytes']==member.get('bytes',member.get('byte_count')) and current['sha256']==member['sha256'],'Member changed: '+relative)
        member_pins.append(current)
    require(sha((folder/'REPORT.md').read_bytes())==report_hash,'Full report changed')
    results=[]
    for optimized in [False,True]:
        prefix=[PY,'-E','-S','-B','-P']+(['-O'] if optimized else [])
        for false in [False,True]:
            argv=prefix+[str(folder/code),*extra]+([false_flag] if false else [])
            start=now();child=subprocess.Popen(argv,cwd=folder,env=env,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
            out,err=child.communicate()
            event={'argv':argv,'PID':child.pid,'UTC_start':start,'UTC_end':now(),'exit_code':child.returncode,
              'stdout_bytes':len(out),'stdout_sha256':sha(out),'stdout':out.decode('utf-8','replace'),
              'stderr_bytes':len(err),'stderr_sha256':sha(err),'stderr':err.decode('utf-8','replace'),
              'optimized':optimized,'deliberate_false_control':false}
            events.append(event);dump(JOURNAL,{'schema':'pr117-root-priority-actual-process-journal/v1','actual_operator_PID':os.getpid(),'events':events})
            if false:
                require(child.returncode!=0 and b'ValueError' in err or child.returncode!=0 and b'ScopeFailure' in err,'False guard accepted')
            else:
                require(child.returncode==0,'Positive checker failed')
                result=json.loads(out);require(result[key]==checks,'Positive count changed')
                results.append({'PID':child.pid,'optimized':optimized,'checks':checks,'parsed_result':result})
    authenticated.append({'family':name,'manifest':pin(manifest),'report':pin(folder/'REPORT.md'),
      'result':pin(folder/'RESULT.json'),'member_count':count,'members':member_pins,'root_actual_replays':results,
      'root_read_full_report_result_and_effective_checker':True})
original=A/'original_head_authentication_20261006/original_attempt/CANDIDATE.md'
require(sha(original.read_bytes())=='1409e8ad35d34f3cc4a9bb14f7e42318c1dd1e0446ecba525c655fad8c978cdf','Original candidate changed')
receipt={'schema':'pr117-root-priority-family-authentication/v1','UTC':now(),'actual_operator_PID':os.getpid(),
 'authenticated_public_member_count':sum(x['member_count'] for x in authenticated),'families':authenticated,
 'actual_child_process_count':len(events),'positive_controls_normal_and_optimized_passed':True,
 'false_controls_normal_and_optimized_rejected':True,'same_exact_published_example_verified':True,
 'proposed_classification':'already_solved exact target','fresh_disposition_gate_pending':True,
 'publication_clearance':False,'math_valid':True,'new_central_proof_turns':0,'original_attempts':'1/5',
 'additive_triangle_citation_correction':'Sealed determinantal report equation(4) labels are OCR citation errors; current references use matrix p937, Remark4.3 p939, Example4.4 p940. Historical report preserved.',
 'goal_active':True,'program_completed':19,'published':11,'main_index_mutations':False}
dump(OUT,receipt)
print(json.dumps({k:v for k,v in receipt.items() if k!='families'},sort_keys=True))
