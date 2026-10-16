import pathlib,json,hashlib,datetime,subprocess,os
os.environ.update(GIT_CONFIG_COUNT='1',GIT_CONFIG_KEY_0='gc.auto',GIT_CONFIG_VALUE_0='0')
R=pathlib.Path('/Users/alec/Documents/Math');P=R/'draft_pr_claimed_solved_900_1000_20261012';A=P/'audits/pr946_6000001';D=A/'preprint';W=A/'reviews/full_package_07'
def fp(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def need(x,m):
 if not x:raise RuntimeError(m)
records={};m=json.loads((D/'package/PACKAGE_MANIFEST.json').read_bytes())
for name,pin in m['family_manifests'].items():
 path=A/name;need(fp(path.read_bytes())['sha256']==pin,'family seal');j=json.loads(path.read_bytes());fs=next(j[k] for k in ['files','curated_files','public_files','payloads'] if k in j)
 if type(fs) is list:fs={x['path']:x for x in fs}
 for n,v in fs.items():b=(path.parent/n).read_bytes();need(len(b)==v['bytes'] and fp(b)['sha256']==v['sha256'],'family payload')
 records[name]={'sha256':pin,'payloads':len(fs)}
seals=['2f1a4ba73839b83280e9daba44fbe79e70b52a80761deded5314e0db99c7e834','e0361044f313b540f8a46b6a417a00a1777e22a33439e9a097aa0f9e7b54c3e6','28f08795caf265a412463b3b30880f29bcbc615eb84baf4b92010d1720326370','7fb99b465473a17ad54a363c4ee6f410023b3857343a5df2c356a705d50180d0','4d60602995d799a0850c4657b3401ad9c353460800f1fbd752c532b73b6963b2','1c75fc274754826a9d189a7e5e5ac206782deddd0a91dc75d0636d9aa787de71']
for i,pin in enumerate(seals,1):
 w=A/'reviews'/f'full_package_{i:02d}';need(fp((w/'MANIFEST.json').read_bytes())['sha256']==pin,'full seal');j=json.loads((w/'MANIFEST.json').read_bytes());need(set(j['files'])==set(j['explicit_public_allowlist']) and 'MANIFEST.json' not in j['files'],'closed allowlist')
 for n,v in j['files'].items():need(fp((w/n).read_bytes())==v,'prior full payload')
 base=D/'reviewed_candidates'/f'candidate{i:02d}' if i<=5 else D;f=json.loads((base/'FREEZE.json').read_bytes());need(len(f['files'])==223,'candidate count')
 for n,v in f['files'].items():need(fp((base/n).read_bytes())==v,'candidate payload')
 invpath=base/'OPERATIONS_INVENTORY.json' if i<=5 else A/'OPERATIONS_INVENTORY.json';need(fp(invpath.read_bytes())['sha256']==f['operations_inventory_sha256'],'historical inventory');inv=json.loads(invpath.read_bytes())
 for n,v in inv['files'].items():need(fp((base/'operations'/n if i<=5 else R/n).read_bytes())==v,'historical operation source')
 records[f'full_package_{i:02d}']={'sha256':pin,'payloads':len(j['files']),'candidate_files':223,'operation_sources':7,'current06_in_place':i==6}
pins=json.loads((A/'reviews/full_package_06/PRIMARY_SOURCE_PINS.json').read_bytes());actual=[]
for r in pins['actual_bodies_authenticated']+pins['additional_primary_bodies']:
 b=(A/r['private_path']).read_bytes();need(fp(b)=={'bytes':r['bytes'],'sha256':r['sha256']},'actual primary body pin');actual.append(r)
state=json.loads(subprocess.check_output(['git','show','7d3adb0e500b0414a49a449e7981d34ade329427:unsolved_math_prioritization/state.json'],cwd=R));hist=subprocess.check_output(['git','show','7d3adb0e500b0414a49a449e7981d34ade329427:unsolved_math_prioritization/history.jsonl'],cwd=R).decode();need('6000001' not in state and not any(str(json.loads(l).get('id'))=='6000001' for l in hist.splitlines() if l.strip()),'native history absent')
out={'status':'PASS','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'manifests':records,'all_eight_family_seals_and_v2_repair':True,'all_six_full_seals_and_complete_contexts':True,'original_native_history_absent':True,'original_declared_turns':'4/5','historical_total_unknown':True,'audit_adds':0};(W/'PRESERVATION_CHECKS.json').write_text(json.dumps(out,indent=2)+'\n');(W/'PRIMARY_SOURCE_PINS.json').write_text(json.dumps({'utc':out['utc'],'status':'PASS','actual_bodies_authenticated':actual,'raw_bodies_public':False},indent=2)+'\n');print(json.dumps({'status':'PASS','authenticated_manifests':len(records),'primary_bodies':len(actual)}))
