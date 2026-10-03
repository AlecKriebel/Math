"""Independent final read-only tree, metadata, ancestry and full-queue gate.

Does not mutate candidate files, Git/index/refs, remote or service state.
Only evidence below this script's dedicated audit directory is written.
"""
from pathlib import Path
import subprocess, hashlib, json, datetime

D=Path(__file__).resolve().parent
R=Path('/Users/alec/Documents/Math')
A=D.parent
HEAD='de6889b0ca34ceba9a08b85637272afe0b14af77'
BASE='e491808c3544ff44e8526d9b24857b5c9ca64208'
ORIGINAL='5da73632ab7a621de7b62edb5f70dfb8017e4a50'
PR379='3ef0b0f3fa8cdaf3561c0a38408bb29719ecac6d'
PREFIX='problems/30004322_arrangement_seshadri/'
QUEUE='unsolved_math_prioritization/QUEUE.md'

def sha(b): return hashlib.sha256(b).hexdigest()
def blob(b): return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
def git(*args): return subprocess.check_output(['git',*args],cwd=R)
def capture(args,label):
    p=subprocess.run(args,cwd=R,capture_output=True)
    (D/'streams'/f'{label}.stdout.txt').write_bytes(p.stdout)
    (D/'streams'/f'{label}.stderr.txt').write_bytes(p.stderr)
    assert p.returncode==0,(label,p.returncode,p.stderr.decode())
    return p.stdout
def ancestor(a,b):
    assert subprocess.run(['git','merge-base','--is-ancestor',a,b],cwd=R).returncode==0,(a,b)

assert git('rev-parse','main').decode().strip()==BASE
assert git('branch','--show-current').decode().strip()=='main'
raw=capture(['git','cat-file','-p',HEAD],'final_repaired_commit')
parents=[line.split()[1].decode() for line in raw.splitlines() if line.startswith(b'parent ')]
assert parents==[ORIGINAL,BASE]
tree=git('rev-parse',HEAD+'^{tree}').decode().strip()
assert tree=='c810b51c5d552bc0ce745ccfeddcf4e64074b85b'
ancestor(PR379,BASE); ancestor(BASE,HEAD); ancestor(ORIGINAL,HEAD)
assert git('merge-base',BASE,HEAD).decode().strip()==BASE

original_raw=(A/'snapshot_manifest.json').read_bytes()
repaired_raw=(A/'repaired_snapshot_manifest.json').read_bytes()
old=json.loads(original_raw);new=json.loads(repaired_raw)
assert old['head']==ORIGINAL
assert new['head']==HEAD and new['base']==BASE and new['original_frozen_head']==ORIGINAL
oldfiles={e['path']:e for e in old['files']}
newfiles={e['path']:e for e in new['files']}
assert len(oldfiles)==len(newfiles)==47 and oldfiles.keys()==newfiles.keys()
mathpaths={p for p in oldfiles if p.startswith(PREFIX)}
assert len(mathpaths)==46
records=[]; data={}
for path,e in newfiles.items():
    b=git('show',HEAD+':'+path)
    assert b==(A/'repaired_snapshot'/path).read_bytes()
    assert len(b)==e['bytes'] and sha(b)==e['sha256']
    data[path]=b
    if path in mathpaths:
        o=oldfiles[path]
        assert e==o
        assert b==git('show',ORIGINAL+':'+path)==(A/'snapshot'/path).read_bytes()
    records.append({'path':path,'bytes':len(b),'sha256':sha(b),'git_blob':blob(b),
                    'repaired_freeze_matches':True,'original_unchanged':path in mathpaths})
actualpaths=set(git('ls-tree','-r','--name-only',HEAD,'--',PREFIX).decode().splitlines())
assert actualpaths==mathpaths,'extra/missing packet files, including possible raw sources'
assert git('diff','--name-only',ORIGINAL,HEAD,'--',PREFIX)==b''
diff=capture(['git','diff','--name-status',BASE+'...'+HEAD],'final_pr_diff')
changes=[line.split('\t') for line in diff.decode().splitlines()]
assert len(changes)==47
assert {c[-1] for c in changes}==mathpaths|{QUEUE}
assert all(c[0]==('M' if c[-1]==QUEUE else 'A') for c in changes)

# Rebind every historical mathematical receipt directly to the repaired tree.
hist=[]
for i in range(1,5):
    m=json.loads(data[PREFIX+f'TURN_{i}_REMOTE_RECEIPT.json'])
    for e in m['files']:
        p=PREFIX+e['path'];b=data[p]
        assert len(b)==e['size'] and blob(b)==e['sha']
        assert b==git('show',m['head']+':'+p)
    ancestor(m['head'],HEAD)
    hist.append({'turn':i,'head':m['head'],'entries':len(m['files']),'all_match_repaired_and_historical_objects':True})
binding=json.loads(data[PREFIX+'review/REMOTE_BINDING.json'])
for e in binding['files']:
    p=PREFIX+e['path'];b=data[p]
    assert len(b)==e['bytes'] and sha(b)==e['sha256']
    assert blob(b)==e['expected_git_blob']==e['remote_git_blob']
    assert b==git('show',binding['commit']+':'+p)
ancestor(binding['commit'],HEAD)
manifestcounts={}
for name in [f'TURN_{i}_MANIFEST.json' for i in range(1,6)]+['FINAL_AUTHOR_MANIFEST.json']:
    m=json.loads(data[PREFIX+name])
    for e in m['files']:
        b=data[PREFIX+e['path']]
        assert len(b)==e['bytes'] and sha(b)==e['sha256']
    if 'previous_manifest_sha256' in m:
        prev=f'TURN_{int(name.split('_')[1])-1}_MANIFEST.json'
        assert sha(data[PREFIX+prev])==m['previous_manifest_sha256']
    manifestcounts[name]=len(m['files'])
assert sum(manifestcounts.values())==62
rm=json.loads(data[PREFIX+'review/REVIEW_MANIFEST.json'])
for e in rm['files']:
    b=data[PREFIX+'review/'+e['path']]
    assert len(b)==e['bytes'] and sha(b)==e['sha256']

qb=git('show',BASE+':'+QUEUE); qh=data[QUEUE]
def locate(b):
    hits=[(i,line) for i,line in enumerate(b.splitlines(keepends=True),1)
          if line.startswith(b'|') and b'30004322 / OWR-17296-003' in line]
    assert len(hits)==1
    i,row=hits[0];cells=row.split(b'|');assert len(cells)==14
    return i,row,cells
ib,rb,cb=locate(qb);ih,rh,ch=locate(qh)
assert ib==ih==413 and cb[1].strip()==ch[1].strip()==b'402'
assert cb[8].strip()==b'queued' and cb[9].strip()==b'0/5'
assert ch[8].strip()==b'unsolved' and ch[9].strip()==b'5/5'
assert [i for i,(a,b) in enumerate(zip(cb,ch)) if a!=b]==[8,9]
assert qb.replace(rb,rh)==qh
assert len(qb.splitlines())==len(qh.splitlines())
assert all(a==b for i,(a,b) in enumerate(zip(qb.splitlines(keepends=True),qh.splitlines(keepends=True)),1) if i!=413)
assert (D/'streams/repaired_queue_main.txt').read_bytes()==qb
assert (D/'streams/repaired_queue_head.txt').read_bytes()==qh

state=json.loads(data[PREFIX+'STATE_T5.json'])
scope=json.loads(data[PREFIX+'PUBLICATION_SCOPE.json'])
assert state=={'problem_id':30004322,'author_turns':5,'status':'original unresolved','author_search_stopped':True}
assert scope['problem_id']==30004322 and scope['status']=='unsolved' and scope['author_turns']==5
assert scope['author_commit']==binding['commit'] and scope['author_files_preserved']==36 and scope['review_files_preserved']==8
assert scope['review_verdict']=='PASS_SCOPED_ORIGINAL_UNSOLVED_5_OF_5'
assert scope['novelty_certified'] is False and scope['raw_sources_included'] is False
assert scope['source_publication_date']=='2020-11-19'

# Read-only service readback establishes the currently advertised PR head/base.
jq='{number,state,draft,title,head_sha:.head.sha,head_ref:.head.ref,base_sha:.base.sha,base_ref:.base.ref,changed_files,html_url,merged,merge_commit_sha}'
api_raw=capture(['gh','api','repos/AlecKriebel/Math/pulls/378','--jq',jq],'final_github_pr_metadata')
api=json.loads(api_raw)
assert api['number']==378 and api['state']=='open' and api['merged'] is False
assert api['head_sha']==HEAD and api['base_sha']==BASE and api['base_ref']=='main'
assert api['changed_files']==47 and 'unsolved (5/5)' in api['title']
assert api['draft'] is True
assert git('rev-parse','main').decode().strip()==BASE,'moving-main race'
result={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS_SCOPED_FINAL_REPAIRED_PACKAGE',
 'original_head':ORIGINAL,'repaired_head':HEAD,'actual_main':BASE,'actual_379_merge':PR379,
 'tree':tree,'parents':parents,'merge_base':BASE,'all_ancestry_checks_pass':True,
 'original_snapshot_manifest_sha256':sha(original_raw),'repaired_snapshot_manifest_sha256':sha(repaired_raw),
 'repaired_freeze_bindings':records,'math_files_identical_original_repaired_freeze_and_git':46,
 'pr_diff_paths':47,'packet_file_count':46,'raw_source_files_in_packet':0,
 'historical_receipts_bound_to_repaired_head':hist,'old_author_freeze_entries_bound_to_repaired_head':len(binding['files']),
 'author_manifest_entries_bound_to_repaired_head':manifestcounts,'old_review_manifest_entries':len(rm['files']),
 'queue':{'physical_line':413,'displayed_rank':402,'changed_pipe_cells':[8,9],
          'before_row':rb.decode(),'after_row':rh.decode(),'all_other_queue_bytes_identical':True,
          'all_prior_queue_outcomes_preserved':True,'base_bytes':len(qb),'head_bytes':len(qh),
          'base_sha256':sha(qb),'head_sha256':sha(qh)},
 'current_packet_state':state,'current_publication_scope':scope,'live_github_metadata':api,
 'original_conjecture_status':'unsolved','author_turns':'5/5','mandatory_math_repairs':[],
 'remaining_audit_gates':[],'remaining_mathematical_gap':'arbitrary realizable complex line arrangements outside proved subclasses/certified range',
 'mutations':'own audit evidence files only; no candidate/index/Git/remote/service/paper/DOI mutation',
 'scope_completion_percent':100,'original_problem_resolution_percent':0}
print(json.dumps(result,sort_keys=True,indent=2))
