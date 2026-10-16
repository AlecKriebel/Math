"""Publish sealed second helper findings at65%; no actual release or PR write."""
from pathlib import Path
import ast,hashlib,json
D=Path(__file__).resolve().parent;p=D/'publish_progress_65.py'
prior=json.loads((D/'PROGRESS_65_CHECKPOINT_RECEIPT.json').read_text())
rel=p.relative_to(D.parents[2].parent).as_posix()
pin=next(x for x in prior['owned_files'] if x['path']==rel)
assert hashlib.sha256(p.read_bytes()).hexdigest()==pin['sha256']
tree=ast.parse(p.read_text());assert isinstance(tree.body[-1],ast.Expr)
tree.body=[n for n in tree.body[:-1] if not(isinstance(n,ast.Assert) and 'PROGRESS_65_CHECKPOINT_RECEIPT' in ast.unparse(n))]
ns={'__file__':str(p)};exec(compile(tree,str(p)+'[definitions-only]','exec'),ns);source=ns['source']
assert not (D/'PROGRESS_65_REVIEW02_CHECKPOINT_RECEIPT.json').exists()
extra="""folder=D.parent/'release_helpers_adversary_02'
seal=folder/'AUTHORED_MANIFEST.json';m=json.loads(seal.read_text());paths.append(seal)
assert hashlib.sha256(seal.read_bytes()).hexdigest()=='0e0096a38f01f0353b28375cd712d1cffb3af92adb0d3d5f51af0360f9a48b9c'
for row in m['files']:
    q=folder/row['path'];raw=q.read_bytes()
    assert q.resolve().is_relative_to(folder.resolve()) and not q.is_symlink()
    assert len(raw)==row['bytes'] and hashlib.sha256(raw).hexdigest()==row['sha256']
    paths.append(q)
for name in ['root_reproduction_10_binding_actual_compatibility','root_reproduction_11_native_final06','root_reproduction_12_helper02_findings']:
    paths += [q for q in (D/name).iterdir() if q.is_file() and (q.name.startswith('ROOT') or q.suffix=='.py' or q.name=='OWN_TERMINAL_FIXTURE_HARDLINK_PLAN.json.gz')]
"""
changes=[
("OUT=D/'PROGRESS_65_CHECKPOINT_RECEIPT.json'","OUT=D/'PROGRESS_65_REVIEW02_CHECKPOINT_RECEIPT.json'"),
("prior=json.loads((D/'PROGRESS_55_CHECKPOINT_RECEIPT.json').read_text())","prior=json.loads((D/'PROGRESS_65_CHECKPOINT_RECEIPT.json').read_text())"),
("assert prior['commit']=='4d58dd0557c1108ac6ea24395deb28cf560d9303'","assert prior['commit']=='32838f8ddbc822c8e29776cbe712f466ed52410d'"),
("strftime('progress65_%Y%m%dT%H%M%S%fZ')","strftime('progress65review02_%Y%m%dT%H%M%S%fZ')"),
("paths += [OLD/'FINAL_COMPLETION_CHECKPOINT_PUBLICATION_RECEIPT.json'",extra+"paths += [OLD/'FINAL_COMPLETION_CHECKPOINT_PUBLICATION_RECEIPT.json'"),
("assert len(entries)<1500","assert len(entries)<1700"),
("Checkpoint PR209 at65%: two scientific package reviews accepted; final clean controls reproduced; source repairs pending","Checkpoint PR209 at65%: sealed second release audit, three reproduced findings; repairs active, publication held"),
]
for old,new in changes:
    assert source.count(old)==1,old;source=source.replace(old,new)
source=source.replace("strftime('progress65review02_%Y%m%dT%H%M%S%fZ')","strftime('progress65review02retry03_%Y%m%dT%H%M%S%fZ')")
read_retry="""raw_api=api
def api(method,path,payload=None):
    for attempt in range(3):
        try:return raw_api(method,path,payload)
        except RuntimeError:
            last=(T/f'{seq:03d}-stderr.txt').read_text(errors='replace')
            if method!='GET' or attempt==2 or not any(s in last for s in ['TLS handshake timeout','context deadline exceeded','connection reset by peer']):raise
            print('Retained transient failed native GET; bounded read-only retry',flush=True)
current_claim()
parent="""
assert source.count("current_claim()\nparent=")==1
source=source.replace("current_claim()\nparent=",read_retry)

source=source.replace("def api(method,path,payload=None):","def api(method,path,payload=None,request_source=None):")
source=source.replace("return raw_api(method,path,payload)","return raw_api(method,path,payload,request_source=request_source)")
needle="        if len(request_bytes)>262144:"
replacement="""        if request_source is not None:
            source_body=request_source.read_bytes()
            assert method=='POST' and path=='git/blobs' and payload['encoding']=='base64'
            assert base64.b64decode(payload['content'])==source_body
            encoded=payload['content'].encode();assert request_bytes.count(encoded)==1
            prefix,suffix=request_bytes.split(encoded)
            recipe=dict(schema='lossless-native-blob-request-v1',method=method,path=path,
                request_bytes=len(request_bytes),request_sha256=hashlib.sha256(request_bytes).hexdigest(),
                source=request_source.relative_to(ROOT).as_posix(),source_bytes=len(source_body),
                source_sha256=hashlib.sha256(source_body).hexdigest(),
                prefix_b64=base64.b64encode(prefix).decode(),suffix_b64=base64.b64encode(suffix).decode())
            q=T/f'{seq:03d}-request-lossless-recipe.json'
            with q.open('x') as handle:
                handle.write(json.dumps(recipe,indent=2)+'\\n');handle.flush();os.fsync(handle.fileno())
            saved=json.loads(q.read_bytes());body=(ROOT/saved['source']).read_bytes()
            rebuilt=base64.b64decode(saved['prefix_b64'])+base64.b64encode(body)+base64.b64decode(saved['suffix_b64'])
            assert rebuilt==request_bytes and hashlib.sha256(rebuilt).hexdigest()==saved['request_sha256']
        elif len(request_bytes)>262144:"""
assert source.count(needle)==1
source=source.replace(needle,replacement)
old="api('POST','git/blobs',dict(content=base64.b64encode(raw).decode(),encoding='base64'))"
assert source.count(old)==1
source=source.replace(old,"api('POST','git/blobs',dict(content=base64.b64encode(raw).decode(),encoding='base64'),request_source=q)")

exec(compile(source,str(D/'publish_progress_65_review02_retry03.py')+'[pinned-template]','exec'),{'__file__':str(D/'publish_progress_65_review02_retry03.py'),'__name__':'__main__'})
