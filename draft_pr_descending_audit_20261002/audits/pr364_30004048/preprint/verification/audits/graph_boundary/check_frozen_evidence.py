#!/usr/bin/env python3
"""Writing acquisition driver with read-only Git/source/replay operations.

No branch/ref/index/worktree/network mutations. Raw command streams are gzipped
losslessly in own private folder. This writes acquisitions and is NOT a standalone
read-only closure verifier. Do not launch it after closing this audit namespace.
Private absence is reported, never converted to a successful check.
"""
import argparse, datetime, gzip, hashlib, json, pathlib, subprocess

parser=argparse.ArgumentParser()
parser.add_argument('--audit',type=pathlib.Path,required=True)
parser.add_argument('--repo',type=pathlib.Path,required=True)
parser.add_argument('--capture-name',default='frozen_evidence_capture')
parser.add_argument('--require-private',action='store_true')
args=parser.parse_args()
A=args.audit.resolve();repo=args.repo.resolve()
own=A/'graph_boundary_review';target=A/'snapshot/unsolved_math_prioritization/attempts/30004048'
prefix='unsolved_math_prioritization/attempts/30004048'
head='0d07b06537aded3e76f5a71908f3546df574a691';base='efd29c05204703acca9a0860812f54b94fae54b1'
if pathlib.Path(args.capture_name).name!=args.capture_name:raise ValueError('capture-name must be a basename')
capture=own/'private'/args.capture_name
capture.mkdir(parents=True,exist_ok=False)
receipts=[]
def h(data):return hashlib.sha256(data).hexdigest()
def blob_id(data):return hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
def git(argv):
    start=datetime.datetime.now(datetime.timezone.utc).isoformat()
    result=subprocess.run(['git']+argv,cwd=repo,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    stem=f'{len(receipts):03d}'
    for label,data in [('stdout',result.stdout),('stderr',result.stderr)]:
        with gzip.GzipFile(filename=str(capture/f'{stem}_{label}.bin.gz'),mode='wb',mtime=0) as out:out.write(data)
    receipt={'argv':['git']+argv,'cwd':str(repo),'start_utc':start,'end_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'exit_code':result.returncode,'stdout_bytes':len(result.stdout),'stderr_bytes':len(result.stderr),'stdout_sha256':h(result.stdout),'stderr_sha256':h(result.stderr),'logical_stream_sha256':h(b'STDOUT\0'+result.stdout+b'STDERR\0'+result.stderr),'private_capture_stem':stem}
    receipts.append(receipt)
    (capture/f'{stem}_receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
    if result.returncode:raise RuntimeError(receipt)
    return result.stdout

raw=git(['diff','--raw','--no-abbrev','-z',base,head]).split(b'\0')
assert raw[-1]==b'';raw=raw[:-1];assert len(raw)%2==0
scope=[]
for metadata,pathbytes in zip(raw[::2],raw[1::2]):
    oldmode,newmode,oldsha,newsha,status=metadata.decode().lstrip(':').split()
    path=pathbytes.decode();assert status in ('A','M');assert newmode=='100644'
    frozen=(A/'snapshot'/path).read_bytes();actual=git(['cat-file','blob',head+':'+path])
    assert actual==frozen and blob_id(actual)==newsha
    scope.append({'path':path,'status':status,'old_mode':oldmode,'head_mode':newmode,'old_blob':oldsha,'head_blob':newsha,'bytes':len(actual),'sha256':h(actual)})
assert len(scope)==42
snapshots={str(f.relative_to(A/'snapshot')) for f in (A/'snapshot').rglob('*') if f.is_file()}
assert snapshots=={entry['path'] for entry in scope}
targetfiles=sorted(p for p in target.rglob('*') if p.is_file());assert len(targetfiles)==41

nested=[]
for manifest in sorted(target.rglob('*.json')):
    obj=json.loads(manifest.read_text())
    if isinstance(obj,dict):
        for entry in obj.get('files',[]):
            if 'path' not in entry or 'sha256' not in entry:continue
            child=manifest.parent/entry['path'];data=child.read_bytes()
            assert len(data)==entry['bytes'] and h(data)==entry['sha256']
            nested.append({'manifest':str(manifest.relative_to(target)),'path':entry['path'],'sha256':h(data),'bytes':len(data)})
assert len(nested)==135
historical_names={'SOURCE_GATE_MANIFEST.json','TURN_1_MANIFEST.json','TURN_2_MANIFEST.json','TURN_3_MANIFEST.json','FINAL_AUTHOR_MANIFEST.json'}
assert sum(entry['manifest'] in historical_names for entry in nested)==88
publication=json.loads((target/'PUBLICATION_MANIFEST.json').read_text())
assert {entry['path'] for entry in publication['files']}|{'PUBLICATION_MANIFEST.json'}=={str(p.relative_to(target)) for p in targetfiles}
remote=json.loads((target/'review/REMOTE_BINDING.json').read_text())
assert len(remote['files'])==30
for entry in remote['files']:
    data=(target/entry['name']).read_bytes()
    actual=git(['cat-file','blob',remote['commit']+':'+prefix+'/'+entry['name']])
    assert actual==data and blob_id(data)==entry['sha'] and len(data)==entry['size']
disposition=json.loads((target/'DISPOSITION.json').read_text())
assert disposition['author_manifest']==h((target/'FINAL_AUTHOR_MANIFEST.json').read_bytes())
assert disposition['review_manifest']==h((target/'review/REVIEW_MANIFEST.json').read_bytes())
assert json.loads((target/'review/REVIEW_MANIFEST.json').read_text())['author_manifest_sha256']==disposition['author_manifest']

history=[]
expected=['1ac8406f5a698e6fc2767d5f4b6e2f44cc327747','ae93eeeeb6a4d8945a59bcacdebdac2a1335517c','067266518aca8b427edd926a68a311e538ad45dd']
for i,commit in enumerate(expected,1):
    introduced=git(['log','--diff-filter=A','--format=%H',head,'--',prefix+f'/TURN_{i}.md']).decode().splitlines()
    assert introduced==[commit]
    state=json.loads(git(['cat-file','blob',commit+':'+prefix+f'/CURRENT_STATE_T{i}.json']))
    assert state['author_turns']==i
    history.append({'turn':i,'first_introduction_commit':commit,'turn_state':state['author_turns']})
    # Bind each historical manifest entry directly to its checkpoint Git blob.
    mf=target/f'TURN_{i}_MANIFEST.json';obj=json.loads(mf.read_text())
    for entry in obj['files']:
        assert git(['cat-file','blob',commit+':'+prefix+'/'+entry['path']])==(target/entry['path']).read_bytes()

queue=next(e for e in scope if e['path']=='unsolved_math_prioritization/QUEUE.md')
oldqueue=git(['cat-file','blob',base+':'+queue['path']]);newqueue=(A/'snapshot'/queue['path']).read_bytes()
assert blob_id(oldqueue)==queue['old_blob']
queuepatch=git(['diff','--no-ext-diff','--unified=3',base,head,'--',queue['path']]).decode()
queue_info={'old_bytes':len(oldqueue),'head_bytes':len(newqueue),'same_first_line':oldqueue.splitlines()[0]==newqueue.splitlines()[0],'old_first_line':oldqueue.splitlines()[0].decode(),'head_first_line':newqueue.splitlines()[0].decode(),'patch':queuepatch}

sources=[]
source_mf=json.loads((target/'SOURCE_MANIFEST.json').read_text())
for entry in source_mf['sources']:
    p=own/'private/sources'/entry['file']
    receipt={'file':entry['file'],'url':entry['url'],'expected_bytes':entry['bytes'],'expected_sha256':entry['sha256'],'private_available':p.is_file()}
    if p.is_file():
        data=p.read_bytes();assert len(data)==entry['bytes'] and h(data)==entry['sha256'];receipt['status']='BYTES_AND_HASH_MATCH'
    else:receipt['status']='NOT_CHECKED_PRIVATE_ABSENT'
    sources.append(receipt)
addition=json.loads((target/'SOURCE_ADDITION_T3.json').read_text())
assert next(e['sha256'] for e in source_mf['sources'] if e['file']==addition['primary_file'])==addition['primary_sha256']

replay_specs=[(f'04{i}_replay_turn{i}',f'TURN_{i}_CHECKS.json') for i in (1,2,3)]+[('044_replay_original_review','review/INDEPENDENT_CHECKS.json')]
replays=[]
for name,expected_file in replay_specs:
    d=own/'private/commands'/name
    receipt={'name':name,'expected_file':expected_file,'private_available':d.is_dir()}
    if d.is_dir():
        out=(d/'stdout.bin').read_bytes();err=(d/'stderr.bin').read_bytes();command=json.loads((d/'receipt.json').read_text())
        assert command['exit_code']==0 and not err and out==(target/expected_file).read_bytes()
        assert h(out)==command['stdout_sha256'] and h(err)==command['stderr_sha256']
        assert h(b'STDOUT\0'+out+b'STDERR\0'+err)==command['logical_stream_sha256']
        receipt.update(status='WHOLE_STDOUT_BYTE_EXACT',stdout_sha256=h(out),logical_stream_sha256=command['logical_stream_sha256'],exact_assertions=json.loads(out).get('assertions',json.loads(out).get('exact_assertions')))
    else:receipt['status']='NOT_CHECKED_PRIVATE_ABSENT'
    replays.append(receipt)
copy=own/'private/replay';copy_status='NOT_CHECKED_PRIVATE_ABSENT'
if copy.is_dir():
    copied={str(p.relative_to(copy)) for p in copy.rglob('*') if p.is_file()}
    assert copied=={str(p.relative_to(target)) for p in targetfiles}
    for original in targetfiles:assert original.read_bytes()==(copy/original.relative_to(target)).read_bytes()
    copy_status='ALL41_SOURCES_BYTE_IDENTICAL'
if args.require_private:
    assert all(e['private_available'] for e in sources+replays) and copy_status=='ALL41_SOURCES_BYTE_IDENTICAL'

print(json.dumps({'status':'PASS_PUBLIC_GIT_BINDINGS','private_checks_complete':all(e['private_available'] for e in sources+replays) and copy_status=='ALL41_SOURCES_BYTE_IDENTICAL','scope':scope,'target_files':41,'actual_paths':42,'nested_entries':135,'historical_author_nested_entries':88,'author_remote_bindings':30,'historical_turns':history,'queue':queue_info,'sources':sources,'replays':replays,'replay_copy':copy_status,'git_commands':receipts,'limitations':['Catalogue JSONL/imported records and prior-search raw data are not in the41-target packet; no independent certificate of their negative historical claims.','Three source pins are checked against newly fetched original primary PDFs; raw PDFs/text/renders stay private.','No exact psi values, invariant minima, ordering, novelty or universal negative-literature claim is inferred.','Private absence suppresses source/replay verification; it never becomes PASS for that private check.']},indent=2,sort_keys=True))
