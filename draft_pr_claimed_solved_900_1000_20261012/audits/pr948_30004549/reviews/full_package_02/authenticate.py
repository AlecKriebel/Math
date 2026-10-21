import pathlib,json,hashlib,subprocess,stat,tarfile,io,datetime,sys
R=pathlib.Path('/Users/alec/Documents/Math'); P=R/'draft_pr_claimed_solved_900_1000_20261012';A=P/'audits/pr948_30004549';D=A/'preprint';O=A/'reviews/full_package_02'
H='be4313efafa1af5962394e07d8a4debff2e94d92'; F='1bbfc6c554984f8f8a4a6c467c92ff6e5e87f22b2b79d2d9d91766bf0822e68c';M='a25e28435f84374bf6e6705c9e5bc91952236d9f5fc5dc48e05ad29d62956b23'
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def sha(b):return hashlib.sha256(b).hexdigest()
def need(v,s):
 if not v:raise RuntimeError(s)
def load(p):return json.loads(p.read_text())
def pin(p,rec):
 need(p.is_file() and not p.is_symlink(),str(p));b=p.read_bytes();need(len(b)==rec['bytes'] and sha(b)==rec['sha256'],'hash '+str(p));return rec
stage=sys.argv[1];started=now();f=load(D/'FREEZE.json');need(sha((D/'FREEZE.json').read_bytes())==F,'freeze')
need(f['revision_candidate']==2 and f['original_pr_head']==H and f['package_manifest_sha256']==M,'identity')
for k,v in f['files'].items():pin(D/k,v)
for k,v in f['evidence_files'].items():pin(R/k,v)
need(len(f['files'])==308 and len(f['evidence_files'])==440,'counts')
ops=A/'publication/workflow/OPERATIONS_INVENTORY.json';need(sha(ops.read_bytes())=='500866df6a5c92a38f133dbe7088da956bc52b54ade02b3fa258a07c3af4e002','ops')
inventory=load(ops);need(len(inventory['files'])==7,'ops count')
for k,v in inventory['files'].items():pin(R/k,v)
for k,v in f['future_helpers'].items():pin(P/k,v)
need(sha((A/'publication/workflow/MANIFEST.json').read_bytes())=='b77fac06fb3cbf3c04b0972d446828642a2b1caeefdaa2a33dc273b8f84cb7d2','workflow seal')
w=load(A/'publication/workflow/MANIFEST.json');need(set(w['files'])==set(w['explicit_public_allowlist']),'allowlist')
for k,v in w['files'].items():pin(A/'publication/workflow'/k,v)
need(len(w['files'])==357,'workflow count')
records=load(A/'ORIGINAL_FILE_RECORDS.json')['files'];need(len(records)==24,'original count')
archive=subprocess.check_output(['git','-c','tar.umask=0022','archive','--format=tar',H,*records],cwd=R)
tar=tarfile.open(fileobj=io.BytesIO(archive));members={x.name:x for x in tar.getmembers() if x.isfile()};need(set(members)==set(records),'archive closure')
originals={}
for k,v in records.items():
 line=subprocess.check_output(['git','ls-tree',H,'--',k],cwd=R,text=True).strip();mode,typ,blob,path=line.split(None,3);need(mode=='100644' and typ=='blob' and blob==v['git_blob'] and path==k,'tree '+k)
 b=subprocess.check_output(['git','cat-file','blob',blob],cwd=R);disk=A/'original'/k;db=disk.read_bytes();am=members[k];ab=tar.extractfile(am).read();need(stat.S_IMODE(disk.stat().st_mode)==0o644 and am.mode==0o644,'original modes '+k);need(b==db==ab and len(b)==v['bytes'] and sha(b)==v['sha256'],'original bytes '+k)
 originals[k]={'bytes':len(b),'sha256':sha(b),'git_blob':blob,'git_mode':'100644','disk_mode':'0644','archive_mode':'100644','disk_and_archive_match':True}
q=subprocess.check_output(['git','show',H+':unsolved_math_prioritization/QUEUE.md'],cwd=R,text=True);rows=[x for x in q.splitlines() if '30004549' in x];need(len(rows)==1 and rows[0].split('|')[8].strip()=='claimed_solved','literal queue')
if stage=='START':
 meta=json.loads(subprocess.check_output(['gh','api','repos/AlecKriebel/Math/pulls/948','--jq','{number,state,draft,head:{sha:.head.sha,ref:.head.ref},base:{ref:.base.ref,sha:.base.sha},updated_at,html_url}'],cwd=R,text=True));transport='REST'
else:
 query='query{repository(owner:\"AlecKriebel\",name:\"Math\"){pullRequest(number:948){number state isDraft headRefOid headRefName baseRefName baseRefOid baseRef{name target{oid}} updatedAt url}}}'
 reply=json.loads(subprocess.check_output(['gh','api','graphql','-f','query='+query],cwd=R,text=True));need(not reply.get('errors'),'GraphQL errors');node=reply['data']['repository']['pullRequest']
 meta={'number':node['number'],'state':node['state'].lower(),'draft':node['isDraft'],'head':{'sha':node['headRefOid'],'ref':node['headRefName']},'base':{'ref':node['baseRefName'],'sha':node['baseRefOid']},'updated_at':node['updatedAt'],'html_url':node['url'],'live_base_ref':node['baseRef']};transport='GraphQL_after_recorded_REST_rate_limit'
need(meta['number']==948 and meta['state']=='open' and meta['draft'] is True and meta['head']['sha']==H and meta['base']['ref']=='main','fresh meta')
obj={'status':'PASS','utc':now(),'original_pr_head':H,'freeze_sha256':F,'package_manifest_sha256':M,'future_helpers':f['future_helpers'],'candidate_files':f['files'],'originals':originals,'authentication_started_utc':started,'evidence_files_authenticated':f['evidence_files'],'operations_inventory_sha256':sha(ops.read_bytes()),'operations_files':inventory['files'],'workflow_manifest_sha256':sha((A/'publication/workflow/MANIFEST.json').read_bytes()),'workflow_files_authenticated':357,'fresh_pr_metadata':meta,'fresh_metadata_transport':transport,'immutable_queue_row':rows[0],'source_hash_limits':'Local private source anchor and historical evidence are hashed/read only; no private body is copied into this public review. SHA256 equality authenticates frozen bytes, not truth of claims.'}
(O/('AUTHENTICATION_'+stage+'.json')).write_text(json.dumps(obj,indent=2)+'\n');print(json.dumps({'status':'PASS','stage':stage,'utc':obj['utc'],'frozen':len(f['files']),'evidence':len(f['evidence_files']),'operations':7,'originals':len(originals),'workflow':357}))
