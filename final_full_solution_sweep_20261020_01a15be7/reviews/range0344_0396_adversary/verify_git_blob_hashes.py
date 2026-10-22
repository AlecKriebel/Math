from pathlib import Path
import json,subprocess,hashlib,datetime
E=Path('/Users/alec/Documents/Math/final_full_solution_sweep_20261020_01a15be7');O=E/'reviews/range0344_0396_adversary'
rows=json.loads((O/'independent_classification_initial.json').read_text())['classifications'];files=[f for r in rows for f in r['changed_paths'] if f['head_git_blob']]
byoid={f['head_git_blob']:f for f in files};ids=list(byoid)
raw=subprocess.run(['git','cat-file','--batch'],input=('\n'.join(ids)+'\n').encode(),capture_output=True,check=True,cwd=E.parent).stdout
pos=0;checks=[]
for oid in ids:
 end=raw.index(b'\n',pos);parts=raw[pos:end].decode().split();assert parts[0]==oid and parts[1]=='blob';size=int(parts[2]);pos=end+1;data=raw[pos:pos+size];pos+=size;assert raw[pos:pos+1]==b'\n';pos+=1
 h=hashlib.sha1(b'blob '+str(size).encode()+b'\0'+data).hexdigest();s=hashlib.sha256(data).hexdigest();f=byoid[oid]
 checks.append({'git_blob':oid,'bytes':size,'git_object_hash_matches':h==oid,'sha256_matches_independent_snapshot':s==f['sha256'],'size_matches_independent_snapshot':size==f['bytes']})
assert pos==len(raw)
faults=[x for x in checks if not all(x[k] for k in ['git_object_hash_matches','sha256_matches_independent_snapshot','size_matches_independent_snapshot'])]
result={'checked_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'pr_count':len(rows),'changed_head_paths':len(files),'unique_blob_count':len(ids),'checks':checks,'faults':faults}
(O/'git_blob_hash_checks.json').write_text(json.dumps(result,indent=2)+'\n');print('raw Git-blob hashes',len(files),'paths',len(ids),'distinct blobs','faults',len(faults))
