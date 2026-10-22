import pathlib,json,hashlib,subprocess,stat,datetime,sys
W=pathlib.Path('/Users/alec/Documents/Math'); P=W/'draft_pr_claimed_solved_900_1000_20261012';A=P/'audits/pr967_2616';R=A/'reviews/closure_package_adversary_02'
pins={'PRIORITY_DISPOSITION.json':'1c783ed45d2b15500ec4ebf83f071373ea1e49cd342ec1f8a3cbfbf102c86160','CLOSURE_OPERATIONS_INVENTORY.json':'1aec2d70a27a8ef251c8478932d1cd578c0a259e075fec591edc345c19d8745a','CLOSURE_COMMENT_DRAFT.md':'beb5578419962c14564c04d1cf6ff47979329788fb6391e0c0443606258241ef','ROOT_TRUSTED_CLOSURE_LAUNCHER.py':'69fc93f82639e7c01d570115bb0bd92873966e81cbe93822a5fabdbe4c62757e','ROOT_FAMILY_AUTHENTICATIONS_NORMALIZED.json':'8b6446b4acc4c536375c2dcc3429d9f87e1151846db425a20dedf268b75f0ff6','ORIGINAL_FILE_RECORDS.json':'610351fbb778f78ce53cda03ea715f38615abb5710690987c214f8093bda13ae','closure_engineering_01/MANIFEST.json':'3ac3ea788e5ff27faf8943c0f2f5302bd1be1bc2e85cf3aaece79fe58e98a3d1','closure_engineering_02/MANIFEST.json':'a8f2fb89e18275b8c948beefaf2d4c9c4f21c0ba8f08e7ced7d1e39a83ba418f','reviews/closure_package_adversary_01/MANIFEST.json':'6c659f3aa01ad6c0d440229c4dfeae6cf7dcc991f13e23318e06a8f527b03476','supplemental/verify_robust.py':'05ad68c46fa8ffa56a002786d5178dfaae558f671208b36912ee45711a99c07e'}
records={}
def check(path,expected):
 b=path.read_bytes();h=hashlib.sha256(b).hexdigest()
 if h!=expected['sha256'] or ('bytes'in expected and len(b)!=expected['bytes']): raise RuntimeError('authentication failed '+str(path))
 records[str(path.relative_to(W))]={'sha256':h,'bytes':len(b)}
 return b
for n,h in pins.items():check(A/n,{'sha256':h})
def members(mp,field):
 m=json.loads(mp.read_bytes()); fs=m['files'];ls=m[field]
 if len(ls)!=len(set(ls)) or set(ls)!=set(fs):raise RuntimeError('allowlist mismatch '+str(mp))
 for n,v in fs.items():check(mp.parent/n,v)
 return {'members':len(fs),'bytes':sum(v['bytes'] for v in fs.values())}
seals={}
for n in ['closure_engineering_01','closure_engineering_02','reviews/closure_package_adversary_01']:
 seals[n]=members(A/n/'MANIFEST.json','explicit_public_allowlist')
fams=json.loads((A/'ROOT_FAMILY_AUTHENTICATIONS_NORMALIZED.json').read_bytes())['families']
for n,f in fams.items():
 mp=W/f['manifest_path'];check(mp,{'sha256':f['manifest_sha256']});seals[n]=members(mp,f['manifest_allowlist_field'])
 for k in ['root_authentication','full_intake']:check(W/f[k+'_path'],{'sha256':f[k+'_sha256']})
 source=json.loads((W/f['root_authentication_path']).read_bytes())
 for k in f['root_authentication_entry_path']:source=source[k]
 if source[f['source_manifest_pin_field']]!=f['manifest_sha256'] or source[f['source_count_field']]!=f['file_count'] or source[f['source_bytes_field']]!=f['total_bytes'] or source[f['source_all_members_field']] is not True:raise RuntimeError('normalization source mismatch '+n)
 if f['root_authentication_utc']>=f['full_intake_utc']:raise RuntimeError('intake chronology')
d=json.loads((A/'PRIORITY_DISPOSITION.json').read_bytes())
for n,v in d['evidence_files'].items():check(W/n,v)
inv=json.loads((A/'CLOSURE_OPERATIONS_INVENTORY.json').read_bytes())
if len(inv['files'])!=2:raise RuntimeError('helper inventory')
for n,v in inv['files'].items():check(W/n,v)
orig=json.loads((A/'ORIGINAL_FILE_RECORDS.json').read_bytes())
if len(orig['files'])!=26:raise RuntimeError('original count')
for n,v in orig['files'].items():
 path=A/'original'/n;b=check(path,v)
 if format(stat.S_IMODE(path.stat().st_mode),'04o')!=v['disk_mode']:raise RuntimeError('disk mode')
 gb=subprocess.check_output(['git','cat-file','blob',orig['head']+':'+n],cwd=W)
 if gb!=b:raise RuntimeError('Git/disk bytes')
 gm=subprocess.check_output(['git','ls-tree',orig['head'],'--',n],cwd=W).decode().split()[0]
 if gm!=v['git_mode'] or hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()!=v['git_blob']:raise RuntimeError('git mode/blob')
if sum(v['bytes']for v in orig['files'].values())!=147731:raise RuntimeError('original total')
result={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS','decision_sha256':pins['PRIORITY_DISPOSITION.json'],'operations_inventory_sha256':pins['CLOSURE_OPERATIONS_INVENTORY.json'],'closure_comment_sha256':pins['CLOSURE_COMMENT_DRAFT.md'],'trusted_launcher_sha256':pins['ROOT_TRUSTED_CLOSURE_LAUNCHER.py'],'all26_original_bytes_and_modes_authenticated':True,'all_six_family_members_authenticated':True,'both_entire_helpers_authenticated':True,'root_evidence_files':len(d['evidence_files']),'seals':seals,'fingerprints':records}
name='AUTHENTICATION_'+('END' if len(sys.argv)>1 and sys.argv[1]=='end' else 'START')+'.json';(R/name).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items()if k!='fingerprints'},indent=2))
