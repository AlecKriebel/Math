import pathlib,hashlib,json,subprocess,datetime,stat,sys
R=pathlib.Path('/Users/alec/Documents/Math'); P=R/'draft_pr_claimed_solved_900_1000_20261012'; A=P/'audits/pr967_2616'; D=A/'reviews/closure_package_adversary_01'
H='b356dec5cb01e5f536b9cfeece56ad08844c03cb'
def sha(b):return hashlib.sha256(b).hexdigest()
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def capture(cmd):return subprocess.check_output(cmd,cwd=R)
def pin(p,h):
 b=p.read_bytes();assert sha(b)==h,(p,sha(b),h);return {'path':str(p.relative_to(R)),'bytes':len(b),'sha256':h,'status':'PASS'}
pins={A/'PRIORITY_DISPOSITION.json':'2d3e28bd446adc1707af8dc8b006c767ca2b09c9ca55658cf33b5717b58e8393',A/'CLOSURE_OPERATIONS_INVENTORY.json':'ad94d62072583e62092215bf919c974f237d52efb1f048e60bbee5724a370d0d',P/'close_pr967.py':'c6231a47758a6b037ed005883d39e374946e38bd9aec0c74eb33df3afe2d2a45',P/'finalize_pr967_and_gate_next.py':'47520f8f86889db8c5b85fc7000486773d2ca4e8601ad00531bad2fdce5143cb',A/'CLOSURE_COMMENT_DRAFT.md':'beb5578419962c14564c04d1cf6ff47979329788fb6391e0c0443606258241ef',A/'ROOT_FAMILY_AUTHENTICATIONS_NORMALIZED.json':'8b6446b4acc4c536375c2dcc3429d9f87e1151846db425a20dedf268b75f0ff6',A/'ORIGINAL_FILE_RECORDS.json':'610351fbb778f78ce53cda03ea715f38615abb5710690987c214f8093bda13ae',A/'closure_engineering_01/MANIFEST.json':'3ac3ea788e5ff27faf8943c0f2f5302bd1be1bc2e85cf3aaece79fe58e98a3d1'}
out={'started_utc':now(),'status':'PASS','pins':[pin(p,h) for p,h in pins.items()]}
metadata=json.loads(capture(['gh','api','repos/AlecKriebel/Math/pulls/967','--jq','{number,state,draft,head:.head.sha,base_ref:.base.ref,base:.base.sha,changed_files,merged_at}']))
assert metadata['number']==967 and metadata['head']==H and metadata['state']=='open' and metadata['draft'] and metadata['base_ref']=='main' and metadata['changed_files']==27 and metadata['merged_at'] is None
queue=capture(['git','show',H+':unsolved_math_prioritization/QUEUE.md']);rows=[r for r in queue.decode().splitlines() if len(r.split('|'))>8 and r.split('|')[2].strip()=='2616 / KOU-21.107']
assert len(rows)==1 and rows[0].split('|')[8].strip()=='claimed_solved'
out['fresh_metadata']=metadata;out['immutable_queue_status']='claimed_solved';out['immutable_queue_row_sha256']=sha((rows[0]+'\n').encode());out['branch']=capture(['git','branch','--show-current']).decode().strip();assert out['branch']=='main'
records=json.loads((A/'ORIGINAL_FILE_RECORDS.json').read_text())['files'];total=0
for rel,e in records.items():
 p=A/'original'/rel;b=p.read_bytes();assert len(b)==e['bytes'] and sha(b)==e['sha256'];assert stat.S_IMODE(p.stat().st_mode)==int(e['disk_mode'],8)
 v=capture(['git','ls-tree',H,'--',rel]).decode().split();assert v[0]==e['git_mode']=='100644' and v[2]==e['git_blob'];assert capture(['git','cat-file','blob',e['git_blob']])==b;total+=len(b)
assert len(records)==26 and total==147731
out['all26_original_bytes_and_modes_authenticated']=True;out['original_count']=26;out['original_total_bytes']=total
norm=json.loads((A/'ROOT_FAMILY_AUTHENTICATIONS_NORMALIZED.json').read_text());fr={}
def members(mpath,field):
 m=json.loads(mpath.read_text());allow=m[field];assert len(allow)==len(set(allow)) and set(allow)==set(m['files']) and 'MANIFEST.json' not in allow
 for rel,e in m['files'].items():
  assert not pathlib.PurePosixPath(rel).is_absolute() and '..' not in pathlib.PurePosixPath(rel).parts
  b=(mpath.parent/rel).read_bytes();assert len(b)==e['bytes'] and sha(b)==e['sha256'],rel
 return len(allow),sum(e['bytes'] for e in m['files'].values())
for name,e in norm['families'].items():
 mpath=R/e['manifest_path'];pin(mpath,e['manifest_sha256']);count,nbytes=members(mpath,e['manifest_allowlist_field']);assert count==e['file_count'] and nbytes==e['total_bytes']
 authp=R/e['root_authentication_path'];intakep=R/e['full_intake_path'];pin(authp,e['root_authentication_sha256']);pin(intakep,e['full_intake_sha256'])
 auth=json.loads(authp.read_text());entry=auth
 for selector in e['root_authentication_entry_path']:entry=entry[selector]
 assert entry[e['source_manifest_pin_field']]==e['manifest_sha256'] and entry[e['source_count_field']]==count and entry[e['source_bytes_field']]==nbytes and entry[e['source_all_members_field']] is True
 assert datetime.datetime.fromisoformat(e['root_authentication_utc'])<datetime.datetime.fromisoformat(e['full_intake_utc'])
 assert auth.get('utc',auth.get('authenticated_utc',auth.get('completed_utc')))==e['root_authentication_utc'],(name,auth.keys())
 intake=json.loads(intakep.read_text());assert intake.get('utc',intake.get('completed_utc'))==e['full_intake_utc'],name
 fr[name]={'count':count,'bytes':nbytes,'manifest_sha256':e['manifest_sha256'],'auth_utc':e['root_authentication_utc'],'intake_utc':e['full_intake_utc'],'status':'PASS'}
out['families']=fr;out['all_six_family_members_authenticated']=True
em=A/'closure_engineering_01/MANIFEST.json';c,n=members(em,'explicit_public_allowlist');assert (c,n)==(119,1616180);out['engineering_all_members']={'status':'PASS','count':c,'bytes':n}
out['both_entire_helpers_authenticated']=True;out['decision_sha256']=pins[A/'PRIORITY_DISPOSITION.json'];out['operations_inventory_sha256']=pins[A/'CLOSURE_OPERATIONS_INVENTORY.json'];out['closure_comment_sha256']=pins[A/'CLOSURE_COMMENT_DRAFT.md'];out['utc']=now()
(D/sys.argv[1]).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
