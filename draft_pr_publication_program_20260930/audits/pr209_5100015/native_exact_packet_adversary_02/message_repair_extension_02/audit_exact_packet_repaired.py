"""Independent exact PR209 merge95 packet audit. Native GETs only.

No Root acceptance is made or synthesized. Inert model/core functions are used
only after independent source pin checks; direct canonical serialization and
byte/path/scope validation provide a distinct cross-check. No CLI/executor run.
"""
import argparse
import base64
import copy
import datetime
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import stat
import subprocess
import types

OWN=Path(__file__).absolute().parent
A=OWN.parents[1]
B=A/'native_integration_preparation_01'
C=A.parents[2]
R=Path('/Users/alec/Documents/Math')
GH='/opt/homebrew/Cellar/gh/2.85.0/bin/gh'
RECORDS=[]

def need(ok,message):
    if not ok:raise AssertionError(message)
def pin(raw):return {'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}
def native(kind,raw):return hashlib.sha1(kind.encode()+b' '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
def encoded(value):return (json.dumps(value,sort_keys=True,indent=2,allow_nan=False)+'\n').encode()
def safe(path):
    need(type(path) is str and path and not PurePosixPath(path).is_absolute() and '\\' not in path
         and all(x not in ('','.','..') for x in path.split('/')),'relative path')
    need(all(ord(ch)>=32 and ord(ch)!=127 for ch in path),'control-free path')
    return path
def load(name):
    path=B/name;module=types.ModuleType('independent_'+name.replace('.','_'));module.__file__=str(path)
    exec(compile(path.read_bytes(),str(path),'exec'),module.__dict__);return module
def tree_hash(entries):
    # Kept separate from production C.tree_hash.
    raw=b''
    for name,(mode,kind,oid) in sorted(entries.items(),key=lambda item:item[0].encode()+(b'/' if item[1][1]=='tree' else b'')):
        raw += str(int(mode)).encode()+b' '+name.encode()+b'\0'+bytes.fromhex(oid)
    return native('tree',raw)

parser=argparse.ArgumentParser()
parser.add_argument('--manifest',required=True)
parser.add_argument('--bytes',type=int,required=True)
parser.add_argument('--sha256',required=True)
args=parser.parse_args()
manifest_path=B/safe(args.manifest)
manifest_raw=manifest_path.read_bytes()
manifest_pin={'bytes':args.bytes,'sha256':args.sha256}
need(pin(manifest_raw)==manifest_pin,'externally supplied exact manifest pin')
need(stat.S_IMODE(manifest_path.stat().st_mode)==0o444,'manifest frozen readonly')
m=json.loads(manifest_raw)
H=load('native209_model.py');T=load('native_trees_readonly.py')
need(m['phase']=='merge95' and m['PR']==209 and m['problem_id']=='5100015','phase and case')
for field,name in [('helper_pin','native209_model.py'),('executor_pin','native209_future_executor.py'),('core_pin','native_trees_readonly.py')]:
    need(pin((B/name).read_bytes())==m[field],'current execution source binding '+field)
need(m['expected_parent']=='a687f7f4b7c374c6f29feb99b5d0e017833244e8','accepted MAIN anchor')
need(m['expected_parent_tree']=='e0b726bb0019b5835601b7317f6913fa3334528a','accepted MAIN tree')
need(m['facts']==H.phase_facts('merge95'),'facts95')

FILES={};PRE={};SOURCE_IDENTITIES={}
for row in m['files']:
    p=safe(row['path']);source=B/safe(row['source'])
    need(p not in FILES,'unique native leaf')
    need(source.resolve()==source and source.is_relative_to(B),'canonical owned source')
    initial=source.stat();body=source.read_bytes();after=source.stat()
    need(initial.st_ino==after.st_ino and initial.st_mtime_ns==after.st_mtime_ns,'source stable during read')
    need(stat.S_ISREG(initial.st_mode) and stat.S_IMODE(initial.st_mode)==0o444,'readonly regular source')
    need(pin(body)=={k:row[k] for k in ('bytes','sha256')} and native('blob',body)==row['git_blob'],'full selected SHA256 and native identity')
    need('/_private/' not in '/'+p and '/journal' not in p.lower(),'private/journal excluded')
    need(not p.endswith('TRACKER_GET_STDOUT.json') and 'private_render_' not in p,'whole tracker and render cache excluded')
    FILES[p]=body
    PRE[p]=None if row['preimage'] is None else (row['preimage']['mode'],row['preimage']['type'],row['preimage']['sha'])
    SOURCE_IDENTITIES[p]={'source':row['source'],'pin':pin(body),'native':native('blob',body)}
need(len(FILES)==m['total_files']<=600 and sum(map(len,FILES.values()))==m['total_bytes']<=8_000_000,'exact bounded selected totals')
need(len(FILES)>=60,'full packet')

allowed_extra={H.QUEUE,*H.VIEWS[2:],*H.LATE_ROOT_ALLOWLIST}
need(all(p.startswith(H.ATTEMPT) or p.startswith(H.CASE) or p in allowed_extra for p in FILES),'strict native path scope')
source_manifest_path=H.CASE+'native_integration_preparation_01/SOURCE_MANIFEST.json'
need(source_manifest_path in FILES and FILES[source_manifest_path]==(B/'SOURCE_MANIFEST.json').read_bytes(),'exact current source manifest selected')
source_manifest=json.loads(FILES[source_manifest_path])
for row in source_manifest['source_files']:
    native_path=H.CASE+'native_integration_preparation_01/'+row['path']
    need(native_path in FILES and pin(FILES[native_path])=={k:row[k] for k in ('bytes','sha256')},'explicit complete source archive')
    need(not any(part.startswith(('packet','ROOT_')) for part in PurePosixPath(row['path']).parts),'source closure excludes operational packet/gates/journals')

original=json.loads((B/'ORIGINAL_NATIVE_REFERENCE.json').read_bytes())
revised=json.loads((B/'REVISED_NATIVE_REFERENCE.json').read_bytes())
own={row['path']:row for row in revised['leaves']}
need(len(own)==54 and {p for p in FILES if p.startswith(H.ATTEMPT)}==set(own),'exact own54')
for p,row in own.items():need(native('blob',FILES[p])==row['git_object'],'own54 native exact')
need(sum(len(FILES[p]) for p in own)==205547,'own54 byte total')
for row in original['leaves']:
    archive=H.ATTEMPT+'history/original_submission_20261016/'+row['path'][len(H.ATTEMPT):]
    need(native('blob',FILES[archive])==row['git_object'],'original23 exact archive')
need(len(original['leaves'])==23,'original23 complete')

snapshot=json.loads((A/'root_native_snapshot_01/READONLY_SNAPSHOT.json').read_bytes())
known={row['path']:row for row in snapshot['entries']}
for p,preimage in PRE.items():
    if p in known:
        expected=known[p]['tuple'];expected=tuple(expected) if expected is not None else None
    elif p.startswith(H.CASE) or p.startswith(H.ATTEMPT):expected=None
    else:raise AssertionError('No authenticated native preimage scope for '+p)
    need(preimage==expected,'exact Root snapshot preimage '+p)

for row in m['local_views']:
    p=row['path'];need(p in H.VIEWS,'local exact view')
    actual=C/p
    actual_body=actual.read_bytes() if actual.exists() else None
    need((pin(actual_body) if actual_body is not None else None)==row['preimage'],'current actual local preimage')
    if row['source'] is not None:
        need((B/row['source']).read_bytes()==actual_body,'sealed preimage copy')
    if p in (H.VIEWS[1],H.VIEWS[4]) and actual_body is not None:
        need(FILES[p].startswith(actual_body),'append-only actual local research log')
for p in (H.VIEWS[0],H.VIEWS[2]):H.matches(json.loads(FILES[p]),H.phase_facts('merge95'),'JSON exact phase facts')
for p in (H.VIEWS[1],H.VIEWS[3],H.VIEWS[4]):H.markdown_current(FILES[p],'merge95',p in (H.VIEWS[1],H.VIEWS[4]))
baseline=json.loads((B/'BASELINE_MEMBERSHIP.json').read_bytes())
progress=json.loads(FILES[H.VIEWS[2]])
need(progress['fully_completed_eligible_PRs']==baseline['fully_completed_eligible_PRs'],'same50 completed membership')
need(progress['published_PRs']==baseline['published_PRs']+[209],'exact35 publication adoption membership')
need(progress['dated_eligible_total']==99,'dated denominator99')
need(progress['active_publication_DOI']=='10.5281/zenodo.23413614','existing DOI, no new deposit')
need(progress['active_tracker_range']=="'Math Puzzles'!A121:D121",'existing exact tracker row')
H.queue_change((A/'root_native_snapshot_01/bodies'/H.QUEUE).read_bytes(),FILES[H.QUEUE],'merge95')
for p,wanted in H.LATE_ROOT_ALLOWLIST.items():need(p in FILES and pin(FILES[p])==wanted,'two exact permitted late Root artifacts')

reference_reused=json.loads((B/'EXISTING_SHARED_BODY_IDENTITIES.json').read_bytes())['files']
need(m['reused_blobs']==reference_reused and len(reference_reused)==228,'228 exact unchanged shared closure')
reused_bytes=0
for row in reference_reused:
    need(row['path'] not in FILES,'shared reused body never recopied or overwritten')
    body=(R/row['path']).read_bytes()
    need(pin(body)=={k:row[k] for k in ('bytes','sha256')} and native('blob',body)==row['git_blob'],'local entire228 SHA256/native closure')
    reused_bytes+=len(body)
need(reused_bytes==5435888,'reused228 bytes')

# Fresh, narrowly bounded immutable immediate-tree GETs supply the conditional
# native scope calculation. They do not authenticate a future candidate.
GETS=[];CACHE={};REUSED_IMMUTABLE=[]
prior_stopped=OWN.parent/'candidate_addendum_01'
prior_seal=json.loads((prior_stopped/'STOPPED_SEAL.json').read_bytes())
prior_name='metadata/git_commits_a687f7f4b7c374c6f29feb99b5d0e017833244e8.json'
prior_row=next(row for row in prior_seal['files'] if row['path']==prior_name)
prior_raw=(prior_stopped/prior_name).read_bytes()
need(pin(prior_raw)=={k:prior_row[k] for k in ('bytes','sha256')},'previous actual immutable parent metadata unchanged')
CACHE['git/commits/'+m['expected_parent']]=json.loads(prior_raw)
REUSED_IMMUTABLE.append({'path':'git/commits/'+m['expected_parent'],'source':'candidate_addendum_01/'+prior_name,**pin(prior_raw)})
def get(method,path):
    need(method=='GET' and (path in ('git/ref/heads/main','pulls/209') or re.fullmatch(r'git/(commits|trees)/[0-9a-f]{40}',path)),'GET-only constrained route')
    if path.startswith('git/') and path not in ('git/ref/heads/main',) and path in CACHE:return copy.deepcopy(CACHE[path])
    need(len(GETS)<10,'at most10 fresh read-only requests')
    result=subprocess.run([GH,'api','--method','GET','repos/AlecKriebel/Math/'+path],stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=45)
    need(len(result.stdout)<4_000_000 and len(result.stderr)<65536,'bounded immediate-tree response')
    need(result.returncode==0,'read-only native GET success')
    value=json.loads(result.stdout)
    GETS.append({'path':path,'stdout':pin(result.stdout),'stderr':pin(result.stderr),'exit':result.returncode})
    if path.startswith(('git/commits/','git/trees/')):CACHE[path]=copy.deepcopy(value)
    return value

need(get('GET','git/ref/heads/main')['object']['sha']==m['expected_parent'],'fresh actual MAIN before conditional calculation')
commit=get('GET','git/commits/'+m['expected_parent'])
need(commit['sha']==m['expected_parent'] and commit['tree']['sha']==m['expected_parent_tree'],'fresh actual parent/tree')
pr=get('GET','pulls/209')
need(pr['head']['sha']==H.PREPARED and pr['base']['ref']=='main' and pr['draft'] is False and pr['state']=='open' and pr['merged'] is False,'fresh exact ready open PR')
need(pr['title']==snapshot['PR_title'] and pin((pr['body'] or '').encode())==snapshot['PR_body_pin'],'reviewed PR title/body unchanged')

trees=T.NativeTrees(get)
# Prior independent review authenticated the shared tuple under this exact
# immutable native parent. Reuse that sealed observation instead of reopening
# two unchanged shared ancestors; current MAIN remains the identical commit.
prior_assessment_raw=(OWN.parent/'EXACT_PACKET_ASSESSMENT.json').read_bytes()
need(pin(prior_assessment_raw)=={'bytes':56821,'sha256':'d96d6f4ee04b89a325ab4e9ca7ae87543806447df447b7a2af3a771291dfc559'},'previous independent shared tuple observation pin')
prior_assessment=json.loads(prior_assessment_raw)
need(prior_assessment['actual_main_lease_observed']==m['expected_parent'] and prior_assessment['opaque_shared_tree_preserved']==H.SHARED_TREE,'unchanged immutable shared tuple observation')
REUSED_IMMUTABLE.append({'role':'shared_tuple_under_identical_immutable_parent','source':'EXACT_PACKET_ASSESSMENT.json',**pin(prior_assessment_raw)})
modeled,changed,dirs=H.expected(T,trees,m['expected_parent_tree'],FILES,PRE)

# Independently overlay immediate native entries. Every unselected native
# tuple remains literally unchanged. No whole repository traversal occurs.
trie={}
for p,body in FILES.items():
    node=trie;parts=p.split('/')
    for component in parts[:-1]:node=node.setdefault(component,{})
    need(parts[-1] not in node,'independent leaf uniqueness')
    node[parts[-1]]=body
independent_changed=set();independent_dirs=set()
def rebuild(oid,node,prefix):
    old=dict(trees.get(oid,0)) if oid is not None else {}
    result=dict(old)
    for name,value in node.items():
        path=prefix+name;before=old.get(name)
        if isinstance(value,bytes):
            need(before==PRE[path],'independent fresh native leaf preimage')
            after=('100644','blob',native('blob',value))
            if after!=before:independent_changed.add(path)
            result[name]=after
        else:
            need(before is None or before[:2]==('040000','tree'),'independent ancestor tree type')
            if before is None:independent_dirs.add(path)
            result[name]=('040000','tree',rebuild(before[2] if before else None,value,path+'/'))
    return tree_hash(result)
independent_root=rebuild(m['expected_parent_tree'],trie,'')
need(independent_root==modeled and independent_changed==changed and independent_dirs==dirs,'distinct canonical tree rebuild and scope equality')
need(changed==set(FILES),'every selected leaf add/change exactly, no deletions')
request,modeled_commit=H.commit_request(m,modeled,[m['expected_parent'],H.PREPARED])
need(get('GET','git/ref/heads/main')['object']['sha']==m['expected_parent'],'actual MAIN stable at end of read-only audit')
need(pin(manifest_path.read_bytes())==manifest_pin,'manifest stable after full audit')

result={'schema':'pr209-native-exact-packet-independent-review-v1',
 'evidence_scope':'CONDITIONAL_EXACT_PACKET_REVIEW_NOT_ROOT_AUTHORITY',
 'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'PR':209,'phase':'merge95',
 'verdict':'PASS_CONDITIONAL_EXACT_PACKET','mandatory_findings':[],'optional_findings':[],
 'accepted':False,'Root_acceptance_granted':False,
 'manifest_name':args.manifest,'manifest_pin':manifest_pin,
 'helper_pin':m['helper_pin'],'executor_pin':m['executor_pin'],'core_pin':m['core_pin'],
 'source_manifest_pin':pin((B/'SOURCE_MANIFEST.json').read_bytes()),
 'selected_files':len(FILES),'selected_bytes':sum(map(len,FILES.values())),
 'own_attempt_files':54,'own_attempt_bytes':205547,'original_archive_files':23,
 'existing_reused_files':228,'existing_reused_bytes':reused_bytes,
 'all_selected_SHA256_and_native_bytes_checked':True,'all_local228_shared_SHA256_native_bytes_checked':True,
 'all_selected_native_preimages_independently_checked':True,'all_local_five_preimages_checked':True,
 'exact_five_phase_facts_and_append_history_checked':True,'exact_single_own_QUEUE_row_checked':True,
 'strict_selected_scope_checked':True,'opaque_shared_tree_preserved':H.SHARED_TREE,
 'conditional_tree':modeled,'conditional_commit':modeled_commit,'conditional_parents':[m['expected_parent'],H.PREPARED],
 'conditional_changed_leaves':sorted(changed),'conditional_added_directories':sorted(dirs),'conditional_deleted_directories':[],
 'distinct_canonical_serializer_agrees':True,'actual_read_only_native_GETs':GETS,
 'prior_immutable_observations_reused':REUSED_IMMUTABLE,'actual_GET_cap':10,
 'actual_native_entries_authenticated':trees.inspected,
 'actual_main_lease_observed':m['expected_parent'],'actual_ready_PR_title_body_unchanged':True,
 'native_objects_created':False,'refs_updated':False,'Root_gates_created':False,
 'production_CLI_invoked':False,'publication_or_tracker_action':False,'local_five_modified':False,
 'limitations':['Conditional packet and source assessment only; this does not establish a future native candidate, CAS, PR merge, local synchronization or terminal completion.',
 'Fresh bounded native tree observations establish preimage scope; unchanged228 native full bodies must still be independently fetched by actual candidate/readback verification.',
 'Other reviewer and Root scientific/publication clearances are separately supplied and confer no execution authority here.']}
(OWN/'EXACT_PACKET_ASSESSMENT.json').write_bytes(encoded(result))
(OWN/'EXACT_PACKET_BODY_INVENTORY.json').write_bytes(encoded({'manifest_pin':manifest_pin,'files':SOURCE_IDENTITIES}))
print(json.dumps({k:v for k,v in result.items() if k not in ('conditional_changed_leaves','conditional_added_directories','actual_read_only_native_GETs','limitations')},sort_keys=True))
