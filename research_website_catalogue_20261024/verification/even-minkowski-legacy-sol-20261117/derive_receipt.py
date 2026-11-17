"""Analyze only already collected evidence; no protected paths or commands."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json
A=Path('/Users/alec/Documents/Math/research_website_catalogue_20261024/verification/even-minkowski-legacy-sol-20261117')
def load(n):return json.loads((A/n).read_text())
def sha(b):return hashlib.sha256(b).hexdigest()
def save(n,x):(A/n).write_text(json.dumps(x,indent=2)+'\n')
inventories=load('COMPLETE_LEAF_INVENTORIES.json');wrapper=load('WRAPPER_CORRESPONDENCE.json')
maps={k:{x['path']:x for x in v['entries']} for k,v in inventories.items()}
native=maps['native_HEAD'];physical=maps['physical_native']
physical_delta=[]
for p in sorted(set(native)|set(physical)):
    if p not in native:physical_delta.append({'path':p,'kind':'physical_only'})
    elif p not in physical:physical_delta.append({'path':p,'kind':'native_HEAD_only'})
    elif native[p]['SHA256']!=physical[p]['SHA256']:physical_delta.append({'path':p,'kind':'different_actual_bytes'})
archive_counts={}
for scope in inventories:
    rows=[r for r in wrapper['archives'] if r['archive'].startswith(scope+':')]
    archive_counts[scope]={'outer_archives':sum(r['depth']==0 for r in rows),'nested_archives':sum(r['depth']==1 for r in rows),
        'member_metadata_rows':sum(len(r['members']) for r in rows),'target_size_members_hashed':sum('SHA256' in m for r in rows for m in r['members']),
        'native_member_matches':sum(len(r['native_matches']) for r in rows),'nested_exclusions':sum(len(r['nested_exclusions']) for r in rows)}
path='docs/papers/knudson-gradient-path/index.html';extracted={};associated=[]
for scope in ['native_HEAD','scoped_release']:
    data=(A/(scope+'_blob_batch.stdout.bin')).read_bytes();pos=0;wanted=maps[scope][path]['Git_blob_OID'];body=None
    while pos<len(data):
        end=data.index(b'\n',pos);oid,kind,n=data[pos:end].split();pos=end+1;n=int(n);b=data[pos:pos+n];pos+=n
        assert data[pos:pos+1]==b'\n';pos+=1
        if oid.decode()==wanted:body=b
    assert pos==len(data) and body is not None and sha(body)==maps[scope][path]['SHA256']
    dest=A/'associated-keyword-page'/scope/'index.html';dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(body);extracted[scope]=body
    associated.append({'scope':scope,'path':path,'saved_path':str(dest.relative_to(A)),**maps[scope][path]})
body=extracted['native_HEAD'];assert sha(body)==physical[path]['SHA256']
associated.append({'scope':'physical_native','path':path,'same_actual_bytes_as':'native_HEAD','saved_path':'associated-keyword-page/native_HEAD/index.html',**physical[path]})
receipt={'UTC':datetime.now(timezone.utc).isoformat(),'input_scope':'Already collected files in this owned lane only; no protected re-read or new Git/search command.',
    'physical_vs_native_HEAD_byte_delta':physical_delta,'archive_counts':archive_counts,
    'scope_HTML_counts':{k:sum(p.endswith('.html') for p in v) for k,v in maps.items()},
    'associated_incidental_keyword_pages':associated,
    'keyword_hit_literal':'H. Edelsbrunner, D. Letscher, and A. Zomorodian,',
    'keyword_hit_path':'docs/papers/knudson-gradient-path/paper.tex:149',
    'candidate_HTML_by_target_keywords':load('CANDIDATE_HTML.json'),
    'derived_data_attempts':1,'collector_reruns':0}
save('DERIVED_EVIDENCE_RECEIPT.json',receipt)
print(json.dumps({'archive_counts':archive_counts,'scope_HTML_counts':receipt['scope_HTML_counts'],'physical_delta':physical_delta},indent=2))
