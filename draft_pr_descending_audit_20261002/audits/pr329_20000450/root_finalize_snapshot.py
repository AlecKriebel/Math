"""Independently authenticate the complete retained API capture and frozen files."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,base64,subprocess,stat
A=Path(__file__).resolve().parent;R=A.parents[2]
O=A/'root_capture_private/freeze_api_002';D=A/'root_capture_private/finalize_snapshot003';D.mkdir(exist_ok=False)
utc=lambda:datetime.now(timezone.utc).isoformat()
sha=lambda b:hashlib.sha256(b).hexdigest()
captures=[]
def run(args, required=True):
    st=utc();r=subprocess.run(args,cwd=R,capture_output=True);n=len(captures)
    j={'argv':args,'cwd':str(R),'started_utc':st,'ended_utc':utc(),'exit_code':r.returncode}
    for k,b in [('stdout',r.stdout),('stderr',r.stderr)]:
        (D/f'{n:03}.{k}.bin').write_bytes(b);j[k+'_bytes']=len(b);j[k+'_sha256']=sha(b)
    captures.append(j);(D/f'{n:03}.json').write_text(json.dumps(j,indent=2)+'\n')
    if required:assert r.returncode==0,(args,r.returncode)
    return r
def api(path):return json.loads(run(['gh','api','repos/AlecKriebel/Math/'+path]).stdout)
main=run(['git','rev-parse','HEAD']).stdout;index=run(['git','ls-files','-s','-z']).stdout
assert run(['git','branch','--show-current']).stdout.strip()==b'main'
old=json.loads((O/'003.stdout.bin').read_bytes());H=old['head']['sha']
assert H=='96395a4f506af6a6045e3cd59afcba2db6b7e2e7'
listed=json.loads((O/'004.stdout.bin').read_bytes());B=json.loads((O/'005.stdout.bin').read_bytes())['merge_base_commit']['sha']
commit=json.loads((O/'006.stdout.bin').read_bytes())
assert commit['sha']==H
trees={};blobs={};retained=[]
for receipt in sorted(O.glob('*.json')):
    j=json.loads(receipt.read_text());stem=receipt.stem
    for k in ['stdout','stderr']:
        b=(O/f'{stem}.{k}.bin').read_bytes();assert len(b)==j[k+'_bytes'] and sha(b)==j[k+'_sha256']
    assert j['exit_code']==0
    if j['argv'][0]=='gh':
        o=json.loads((O/f'{stem}.stdout.bin').read_bytes())
        if isinstance(o,dict) and 'tree' in o and isinstance(o['tree'],list):trees[o['sha']]=o
        if isinstance(o,dict) and o.get('encoding')=='base64' and 'content' in o:blobs[o['sha']]=o
    retained.append({'path':str(receipt.relative_to(A)),'bytes':receipt.stat().st_size,'sha256':sha(receipt.read_bytes())})
def entry(path):
    oid=commit['tree']['sha'];parts=path.split('/')
    for i,part in enumerate(parts):
        tree=trees[oid];assert not tree['truncated'] and tree['sha']==oid
        es=[e for e in tree['tree'] if e['path']==part];assert len(es)==1;e=es[0]
        if i==len(parts)-1:return e
        assert e['type']=='tree' and e['mode'] in {'40000','040000'};oid=e['sha']
prefix='unsolved_math_prioritization/attempts/20000450/';S=A/'snapshot';files=[]
for row in listed:
    p=row['filename'];assert p=='unsolved_math_prioritization/QUEUE.md' or p.startswith(prefix)
    assert row['status'] in {'modified','added'}
    e=entry(p);assert e['mode']=='100644' and e['type']=='blob' and e['sha']==row['sha']
    obj=blobs[e['sha']];raw=base64.b64decode(obj['content']);f=S/p
    assert len(raw)==obj['size']==e['size'] and raw==f.read_bytes()
    assert hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()==e['sha']
    assert stat.S_ISREG(f.lstat().st_mode) and stat.S_IMODE(f.stat().st_mode)==0o644
    files.append({'path':p,'bytes':len(raw),'sha256':sha(raw),'git_blob_sha':e['sha'],'mode':e['mode'],'API_object_disk_all_identical':True})
assert len(listed)==old['changed_files']==len(files)==22
assert {str(p.relative_to(S)) for p in S.rglob('*') if p.is_file()}=={e['path'] for e in files}
q=(S/'unsolved_math_prioritization/QUEUE.md').read_text()
rows=[(i+1,l) for i,l in enumerate(q.splitlines()) if len(l.split('|'))>11 and l.split('|')[2].strip().split(' / ')[0]=='20000450']
assert len(rows)==1
line,row=rows[0];assert row.split('|')[8].strip()=='claimed_solved' and row.split('|')[9].strip()=='1/5'
now=api('pulls/329');assert now['head']['sha']==H and now['state']=='open' and now['draft'] and now['base']['ref']=='main'
fresh=api('pulls/329/files?per_page=100')
assert {(e['filename'],e['sha'],e['status']) for e in fresh}=={(e['filename'],e['sha'],e['status']) for e in listed}
local=run(['git','cat-file','-e',H+'^{commit}'],required=False)
local_verified=False
if local.returncode==0:
    local_base=run(['git','merge-base',main.decode().strip(),H]).stdout.decode().strip();assert local_base==B
    paths=set(run(['git','diff','--name-only',B,H]).stdout.decode().splitlines());assert paths=={e['path'] for e in files}
    for e in files:
        assert run(['git','show',H+':'+e['path']]).stdout==(S/e['path']).read_bytes()
    local_verified=True
assert run(['git','rev-parse','HEAD']).stdout==main and run(['git','ls-files','-s','-z']).stdout==index
j={'utc':utc(),'status':'FROZEN_COMPLETE_API_GIT_OBJECT_DISK_SCOPE_VERIFIED','pr':329,'head':H,'base':B,'head_tree':commit['tree']['sha'],
   'target_prefix':prefix,'files':files,'all_files_count':22,'submitted_status':'claimed_solved','submitted_turns':'1/5','QUEUE_physical_line':line,
   'source_before_PR_analytic_reading':True,'root_no_PR_scientific_prose_or_inherited_verdict_read_yet':True,
   'native_API_capture_directory':str(O),'native_finalizer_capture_directory':str(D),'retained_native_receipts':retained,
   'main_and_entire_index_unchanged_during_finalizer':True,'local_Git_diff_and_all22_blobs_verified':local_verified,
   'no_Git_mutation':True,'program_sha256':sha(Path(__file__).read_bytes()),
   'historical_intake_errors':['freeze001 incorrectly assumed problems/ target prefix; stopped before writing snapshots',
       'freeze002 authenticated all22 files, then its row locator incorrectly expected a bare numeric-ID cell; stopped before declaration of completion. This independent finalizer parses ID/alias and fully rechecks retained objects/disk/live head.']}
(A/'snapshot_manifest.json').write_text(json.dumps(j,indent=2)+'\n')
with (A/'RESEARCH_LOG.md').open('a') as f:f.write('\n'+j['utc']+' — All22 candidate files independently authenticated against captured API objects/modes/disk and fresh live head/filelist. Two mechanical routing/row-format assertion failures retained and repaired; no proof or status acceptance inferred. Original1/5 preserved. Workflow10%, mathematical verification0%.\n')
print(json.dumps({k:v for k,v in j.items() if k not in {'files','retained_native_receipts'}},indent=2))
print(json.dumps([{'path':e['path'],'bytes':e['bytes']} for e in files],indent=2))
