from pathlib import Path
import json,hashlib,base64,datetime as dt
N=Path('/Users/alec/Documents/Math/draft_pr_descending_audit_20261002/audits/pr263_30000170/initial_review_20261011/integration_preparation')
E=N/'actual_author_execution';P=json.loads((N/'exact_native_candidate_v02/PREPARATION.json').read_text());blobs=[]
for i,z in enumerate(P['selected_full_body_manifest'],1):
 f=E/'full_blob_readbacks'/(str(i).zfill(3)+'_'+z['git_blob']+'.json');x=json.loads(f.read_text());b=base64.b64decode(x['content'])
 assert x['sha']==z['git_blob'] and x['encoding']=='base64' and x['size']==len(b)==z['bytes']
 assert hashlib.sha256(b).hexdigest()==z['sha256'] and hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==z['git_blob']
 assert b==Path(z['source']).read_bytes()
 blobs.append({'path':z['path'],'bytes':len(b),'sha256':z['sha256'],'git_blob':z['git_blob'],'provider_response':str(f),'full_body_exact':True})
V=json.loads((N.parent/'native_integration_adversarial_review/EXACT_PREPARATION_AUDIT.json').read_text())
anc=sorted(z['directory'] for z in V['rewritten_ancestors']);assert len(anc)==24;trees=[]
files=sorted((E/'nonrecursive_tree_readbacks').glob('*.json'));assert len(files)==24
for path,f in zip(anc,files):
 x=json.loads(f.read_text());oid=x['sha'];assert not x.get('truncated',False);items=x['tree'];assert all('/' not in z['path'] for z in items)
 body=b''.join(z['mode'].lstrip('0').encode()+b' '+z['path'].encode()+b'\0'+bytes.fromhex(z['sha']) for z in sorted(items,key=lambda z:z['path'].encode()+(b'/' if z['type']=='tree' else b'')))
 assert hashlib.sha1(b'tree '+str(len(body)).encode()+b'\0'+body).hexdigest()==oid
 expected=next(z for z in V['rewritten_ancestors'] if z['directory']==path);assert oid==expected['after']
 trees.append({'path':path,'git_tree':oid,'actual_nonrecursive_entries':len(items),'raw_bytes':len(body),'raw_sha256':hashlib.sha256(body).hexdigest(),'full_raw_exact':True})
C=json.loads((E/'FULL_COMMIT_READBACK.json').read_text());CP=json.loads((N/'exact_native_candidate_v02/COMMIT_PAYLOAD.json').read_text());raw=(E/'ACTUAL_REMOTE_COMMIT.raw').read_bytes()
assert raw==(N.parent/'native_integration_adversarial_review/INDEPENDENT_COMMIT.raw').read_bytes()
assert hashlib.sha1(b'commit '+str(len(raw)).encode()+b'\0'+raw).hexdigest()==P['commit']
assert C['sha']==P['commit'] and C['tree']['sha']==P['tree'] and [z['sha'] for z in C['parents']]==P['ordered_parents']
assert C['message']+'\n'==CP['message'];assert all(C[k][f]==CP[k][f] for k in ['author','committer'] for f in ['name','email','date'])
R={'schema':'pr263-actual-provider-created-objects-full-readback-v1','UTC':dt.datetime.now(dt.timezone.utc).isoformat(),'commit':P['commit'],'tree':P['tree'],'ordered_parents':P['ordered_parents'],'all133_selected_full_provider_blob_bodies_exact':True,'actual_blob_GET_count':133,'selected_bodies':blobs,'all24_edited_ancestor_raw_provider_trees_exact':True,'actual_tree_GET_count':24,'edited_ancestor_trees':trees,'actual_remote_raw_commit326_bytes_exact_to_independent':True,'REST_metadata_exact_except_final_message_newline_omitted_by_API':True,'raw_remote_readback_resolves_API_newline_omission':True,'provider_ref_mutations':0,'primary_local_Git_mutations':0}
F=E/'ROOT_ACTUAL_PROVIDER_OBJECT_READBACK_ACCEPTANCE.json';F.write_text(json.dumps(R,indent=2)+'\n')
print(json.dumps({'UTC':R['UTC'],'actual_full_blob_reads':len(blobs),'actual_full_raw_tree_reads':len(trees),'actual_remote_raw_commit_bytes':len(raw),'commit':R['commit'],'tree':R['tree'],'acceptance_bytes':len(F.read_bytes()),'acceptance_sha256':hashlib.sha256(F.read_bytes()).hexdigest(),'provider_ref_mutations':0},indent=2))
