import pathlib,json,hashlib,subprocess,datetime,sqlite3
R=pathlib.Path('/Users/alec/Documents/Math');A=R/'draft_pr_claimed_solved_900_1000_20261012/audits/pr946_6000001';D=A/'preprint';O=A/'reviews/full_package_04'
def need(c,m):
 if not c:raise RuntimeError(m)
def fp(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
records={}
m=json.loads((D/'package/PACKAGE_MANIFEST.json').read_bytes())
for w,pin in m['family_manifests'].items():
 path=A/w;raw=path.read_bytes();need(fp(raw)['sha256']==pin,w);j=json.loads(raw);fs=next(j[k] for k in ['files','curated_files','public_files','payloads'] if k in j)
 if type(fs) is list:fs={x['path']:x for x in fs}
 for k,v in fs.items():
  b=(path.parent/k).read_bytes();need(len(b)==v['bytes'] and fp(b)['sha256']==v['sha256'],w+'/'+k)
 records[w]={'manifest_sha256':pin,'payloads':len(fs)}
for i,pin in [(1,'2f1a4ba73839b83280e9daba44fbe79e70b52a80761deded5314e0db99c7e834'),(2,'e0361044f313b540f8a46b6a417a00a1777e22a33439e9a097aa0f9e7b54c3e6'),(3,'28f08795caf265a412463b3b30880f29bcbc615eb84baf4b92010d1720326370')]:
 path=A/'reviews'/f'full_package_{i:02d}'/'MANIFEST.json';raw=path.read_bytes();need(fp(raw)['sha256']==pin,'oldseal');j=json.loads(raw)
 for k,v in j['files'].items():need(fp((path.parent/k).read_bytes())==v,'oldpayload')
 old=D/'reviewed_candidates'/f'candidate{i:02d}';f=json.loads((old/'FREEZE.json').read_bytes())
 for k,v in f['files'].items():need(fp((old/k).read_bytes())==v,'oldcandidate')
 inv=json.loads((old/'OPERATIONS_INVENTORY.json').read_bytes());need(fp((old/'OPERATIONS_INVENTORY.json').read_bytes())['sha256']==f['operations_inventory_sha256'],'oldinventory')
 for k,v in inv['files'].items():need(fp((old/'operations'/k).read_bytes())==v,'oldsource')
 records[f'full_package_{i:02d}']={'manifest_sha256':pin,'payloads':len(j['files']),'historical_files':len(f['files']),'historical_operation_sources':len(inv['files'])}
db=sqlite3.connect('file:'+str((R/'unsolved_math_prioritization/cache/catalog.sqlite').resolve())+'?mode=ro',uri=True);x=db.execute('select payload,report from records where key=?',('6000001',)).fetchone();p,r=map(json.loads,x);statement=hashlib.sha256(p['statement'].encode()).hexdigest();review=hashlib.sha256(json.dumps([p,r],sort_keys=True).encode()).hexdigest();need(statement=='04707260f4ed2585125f1da57279c9cf1da447cd99a9010d463e5be43dc945cd' and review=='f8584e1f273da5d42d94704da74c51cf5aa9f0100b44e2bc9b2096c45eabf4fb','rawcache')
head='7d3adb0e500b0414a49a449e7981d34ade329427'
state=json.loads(subprocess.check_output(['git','show',head+':unsolved_math_prioritization/state.json'],cwd=R));history=subprocess.check_output(['git','show',head+':unsolved_math_prioritization/history.jsonl'],cwd=R).decode();hits=[j for l in history.splitlines() if l.strip() for j in [json.loads(l)] if str(j.get('id'))=='6000001'];need('6000001' not in state and hits==[],'native unknown')
print(json.dumps({'status':'PASS','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'preserved_manifests':records,'raw_source_statement_hash':statement,'raw_source_review_hash':review,'complete_selected_prior_report_read':True,'native_target_state_absent':True,'native_target_history_events':0,'original_declared_turns':'4/5','native_history_not_fabricated':True,'new_proof_search_turns':0},indent=2))

