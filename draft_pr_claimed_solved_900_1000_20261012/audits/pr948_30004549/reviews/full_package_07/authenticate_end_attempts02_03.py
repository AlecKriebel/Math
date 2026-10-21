import sys,os,json,hashlib,pathlib,stat,zipfile,datetime
P=pathlib.Path('/Users/alec/Documents/Math/draft_pr_claimed_solved_900_1000_20261012'); A=P/'audits/pr948_30004549'; D=A/'preprint'; W=A/'publication/workflow'; R=A/'reviews/full_package_07'
PIN={'freeze':'1bbfc6c554984f8f8a4a6c467c92ff6e5e87f22b2b79d2d9d91766bf0822e68c','manifest':'a25e28435f84374bf6e6705c9e5bc91952236d9f5fc5dc48e05ad29d62956b23','pdf':'14063ce9fef470a6a3875dc429a1c3d34372d60cbd73eb7e22e77b46b1639f60'}
INV='500866df6a5c92a38f133dbe7088da956bc52b54ade02b3fa258a07c3af4e002'; SEALS=['348cf0e067b1a0532cb79172510c247ea3d079dcb315dab899143dc53dca0c66','98af806e47bdbe991ce01f710ea56f76d4c3081fcc2a2a3819362d55564229ea','24dec2ffbce33135e86fa7ef659374c594c54c6d1c2a7eb7f4e722cf21827465','5b91834665d27c0cb2ff7bbe9bd5296fcc133e825759c6e348d52d282fc62af2','4952eee8ff51c9d553121f66ccc907e4cc89eaa4b3bfbf36454e7a6e0ec9d15f','eeb67f2d7aedc0d1b2a2df4992d73847b75433328cba713d0ccb90e951fb0b81']
def utc():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def sh(b):return hashlib.sha256(b).hexdigest()
def save(n,d):
 raw=(json.dumps(d,indent=2,ensure_ascii=False,allow_nan=False)+'\n').encode(); p=R/n
 with p.open('wb') as f:f.write(raw);f.flush();os.fsync(f.fileno())
 assert p.read_bytes()==raw
 return d
s={'__file__':str(P/'accept_pr948.py'),'__name__':'review07_inert_ops'};raw=(P/'accept_pr948.py').read_bytes();assert sh(raw)=='3be81538c4e17e6b220208992a8d56422218f37773f84c8a690a4ab10a41d823';exec(compile(raw,str(P/'accept_pr948.py'),'exec',dont_inherit=True,optimize=0),s)
def payload_map(path,pin):
 raw=path.read_bytes();assert sh(raw)==pin
 # Access ONLY files and explicit allowlist; never expose substantive manifest fields.
 doc=json.loads(raw); files=doc['files']; allow=doc.get('explicit_public_allowlist')
 if allow is not None:assert len(allow)==len(set(allow)) and set(allow)==set(files)
 out={}
 for n,v in files.items():
  assert s['safe'](n); b=s['read_regular'](path.parent/n,pin=v);out[n]={'bytes':len(b),'sha256':sh(b)}
 return {'manifest_sha256':pin,'count':len(files),'payloads':out}
def authenticate(label):
 began=utc(); context=s['capture_inventory'](INV)
 freeze=s['freeze_check'](s['read_regular'](D/'FREEZE.json'),PIN['freeze'],context,base=D)
 assert len(freeze['files'])==308 and len(freeze['evidence_files'])==440 and len(freeze['future_helpers'])==6
 workflow=payload_map(W/'MANIFEST.json','b77fac06fb3cbf3c04b0972d446828642a2b1caeefdaa2a33dc273b8f84cb7d2');assert workflow['count']==357
 assert sh((W/'CONTRACT.json').read_bytes())=='0ccccc9cc49cadf489248f2a56d275625a033289ec5361212e35b6d9b9052827'
 hist=D/'reviewed_candidates/candidate01';pres=payload_map(hist/'PRESERVATION.json','dfb4a95b998f4b200ba8755fefe104126383667ee6ea927d338d144d396a2535');assert pres['count']==353
 oldraw=(hist/'FREEZE.json').read_bytes();old=s['freeze_check'](oldraw,sh(oldraw),context,base=hist,historical=True)
 assert len(old['files'])==262 and len(old['evidence_files'])==82
 private=hist/'evidence';assert stat.S_IMODE(private.stat().st_mode)==0o700
 private_modes={n:oct(stat.S_IMODE((private/n).stat().st_mode)) for n in old['evidence_files']};assert set(private_modes.values())=={'0o600'}
 priors={f'{i:02d}':payload_map(A/f'reviews/full_package_{i:02d}/MANIFEST.json',pin) for i,pin in enumerate(SEALS,1)}
 originals=s['original_check'](); names=[]
 with zipfile.ZipFile(D/s['ZIP']) as z:
  infos=z.infolist();assert len(infos)==258
  for n,v in originals.items():
   matches=[x for x in infos if x.filename=='original/'+n]
   assert len(matches)==1,(n,'archive original path')
   i=matches[0];assert i.create_system==3 and stat.S_IFMT(i.external_attr>>16)==stat.S_IFREG and stat.S_IMODE(i.external_attr>>16)==0o644
   assert z.read(i)==s['blob'](s['HEAD'],n)==(A/'original'/n).read_bytes()
   v.update(archive_mode='100644',disk_and_archive_match=True);names.append(i.filename)
 pr=s['pr_view']();s['main_destination'](pr);assert pr['isDraft'] is True
 assert sh(pr['body'].encode())==freeze['pr_description_sha256']
 row=s['claimed_row'](s['blob'](s['HEAD'],s['QUEUE'])).decode()
 remote={n:s['run'](['gh','api','--method','GET','repos/AlecKriebel/Math/contents/'+n,'-H','Accept: application/vnd.github.raw+json','-f','ref='+pr['currentBaseRefOid']],raw=True) for n in [s['STATE'],s['HISTORY']]}
 state=json.loads(remote[s['STATE']]);events=[json.loads(x) for x in remote[s['HISTORY']].splitlines() if x.strip()];target=[e for e in events if str(e.get('id'))==s['KEY']]
 assert s['KEY'] not in state and not target
 native={'state_sha256':sh(remote[s['STATE']]),'history_sha256':sh(remote[s['HISTORY']]),'target_state_absent':True,'target_history_entries':0,'historical_native_turn_count':'UNKNOWN','new_author_proof_responses':0,'method':'read-only GitHub raw contents at actual currentBaseRefOid'}
 after_pr=s['pr_view']();s['main_destination'](after_pr)
 if after_pr!=pr:
  save('ACTUAL_PR_METADATA_BRACKET_DIFFERENCE_'+label+'.json',{'utc':utc(),'before':pr,'after':after_pr,'differences':{k:{'before':pr.get(k),'after':after_pr.get(k)} for k in set(pr)|set(after_pr) if pr.get(k)!=after_pr.get(k)}})
  raise RuntimeError('actual PR/live metadata drifted across native read; rerun authentication')
 details={'began_utc':began,'completed_utc':utc(),'operations_inventory_sha256':INV,'seven_operations':context['inventory']['files'],'workflow':workflow,'historical_preservation':pres,'historical_freeze':{'sha256':sh(oldraw),'files':len(old['files']),'evidence':len(old['evidence_files']),'operations':7,'private_root_mode':'0700','private_files_mode':'0600'},'prior_mechanical_payload_maps':priors,'current_external_evidence_count':len(freeze['evidence_files']),'actual_pr':pr,'immutable_head_gate_row':row,'native_accounting':native,'original_archive_paths':names}
 save('AUTHENTICATION_'+label+'_DETAILS.json',details)
 receipt={'status':'PASS','utc':utc(),'original_pr_head':s['HEAD'],'freeze_sha256':PIN['freeze'],'package_manifest_sha256':PIN['manifest'],'future_helpers':freeze['future_helpers'],'candidate_files':freeze['files'],'originals':originals}
 save('AUTHENTICATION_'+label+'.json',receipt); s['review_authentication'](json.loads((R/('AUTHENTICATION_'+label+'.json')).read_bytes()),PIN,freeze,s['original_check']())
 print(json.dumps({'label':label,'utc':receipt['utc'],'status':receipt['status'],'operations':7,'frozen':308,'evidence':440,'future_helpers':6,'workflow':357,'preserved':353,'originals':24,'prior_payload_counts':{k:v['count'] for k,v in priors.items()},'pr':{k:pr[k] for k in ['state','isDraft','headRefOid','baseRefName','baseRefOid','currentBaseRefOid']}}))
 return receipt
if __name__=='__main__':
 label=sys.argv[1]
 if label=='START' and not (R/'SESSION_START.json').exists():
  save('SESSION_START.json',{'started_utc':utc(),'reviewer_agent_id':'/root/pr948_full_package_07','mechanical_pre_math_scope':'No prior substantive verdict, result, theorem, issue or argument read before own initial attack. Earlier tool showed only manifest key names/types and first payload fingerprint. No blindness claim.'})
 authenticate(label)
