"""Pure source controls; stdout only, no actual capture/finalize or filesystem writes."""
import sys
if not (sys.flags.ignore_environment and sys.flags.no_site and sys.dont_write_bytecode and sys.flags.safe_path and not sys.flags.optimize):raise RuntimeError('Use Python3.11 -E -S -B -P')
import types,ast,json,hashlib
from pathlib import Path
HERE=Path(__file__).absolute().parent
SOURCE=(HERE/'capture_logical_packet.py').read_text()
EXPECTED_SOURCE={"bytes":42168,"sha256":"313a9fdfeb37407f94a5950ab91120e52850b85acb178d1f7a83e5bef8851a3b"}
if {'bytes':len(SOURCE.encode()),'sha256':hashlib.sha256(SOURCE.encode()).hexdigest()}!=EXPECTED_SOURCE:raise RuntimeError('Exact tested capture source required')
cap=types.ModuleType('source_only_capture_controls');cap.__file__=str(HERE/'capture_logical_packet.py')
exec(compile(SOURCE,cap.__file__,'exec'),cap.__dict__)
ENGINE=cap.ENGINE

def run_controls():
 import copy,base64,calendar
 h,e,c=cap.helpers();results=[]
 def yes(name,fn):
  value=fn();cap.need(value is not False,name);results.append({'name':name,'result':'PASS'})
 def no(name,fn):
  try:fn()
  except (RuntimeError,KeyError,ValueError,TypeError,IndexError,FileNotFoundError):results.append({'name':name,'result':'EXPECTED_REFUSAL'});return
  raise RuntimeError('Unexpected acceptance: '+name)
 yes('new module helpers inert exact frozen model/core',lambda:h.CURRENT=='7f17eef77c52b2d9b2ec3ad0803c016267fa6496' and h.CORE_PIN['sha256']=='c71575a580c43fea8d302c978e0b6c340a16474779ffeb4671e77b967cf6e2ce')
 old=(ENGINE.parent.parent/'pr218_30006020/logical_capture_source_preparation_02/capture_logical_packet.py').read_text()
 oldtree=ast.parse(old);newtree=ast.parse(SOURCE)
 for name in ('need','pin','enc','read_regular','load','file_ref','merge_prefix','GET'):
  get=lambda tree:next(n for n in tree.body if isinstance(n,(ast.FunctionDef,ast.ClassDef)) and n.name==name)
  yes('exact inherited AST '+name,lambda name=name,get=get:ast.dump(get(oldtree),include_attributes=False)==ast.dump(get(newtree),include_attributes=False))
 yes('log prefix local extends native',lambda:cap.merge_prefix(b'abc_more',b'abc')==b'abc_more')
 yes('log prefix native extends local',lambda:cap.merge_prefix(b'abc',b'abc_more')==b'abc_more')
 yes('absent/native log prefix',lambda:cap.merge_prefix(None,b'abc')==b'abc')
 no('divergent log prefixes',lambda:cap.merge_prefix(b'left',b'right'))
 own=b'|239|30001321 / OWR-4081-005|a|b|c|d|e|claimed_solved|3/5|f|g|h|\n'
 before=b'foreign bytes\n'+own.replace(b'claimed_solved|3/5',b'queued|0/5')+b'trailing foreign\n'
 after,pre,post=cap.queue_postimage(h,before,own,'merge95')
 yes('95 wholeQUEUE only exact own row changes',lambda:after==b'foreign bytes\n'+own+b'trailing foreign\n')
 yes('100 wholeQUEUE no rewrite',lambda:cap.queue_postimage(h,after,None,'completion100')[0]==after)
 no('100 supplied row refused',lambda:cap.queue_postimage(h,after,own,'completion100'))
 no('false1/5 row refused',lambda:cap.queue_postimage(h,before,own.replace(b'3/5',b'1/5'),'merge95'))
 no('multiple post rows refused',lambda:cap.queue_postimage(h,before,own+own,'merge95'))
 for prefix in (b' ',b'  ',b'\t'):
  no('indented duplicate ownrow '+str(prefix),lambda prefix=prefix:cap.queue_postimage(h,before+prefix+own,own,'merge95'))
 # Canonical source body reader over prior owned synthetic bytes only.
 existing=ENGINE/'_synthetic_controls_04/publication.json';existing_raw=existing.read_bytes()
 rr={'origin':str(existing),**h.pin(existing_raw),'git_blob':h.native('blob',existing_raw)}
 yes('selected source body full nativeSHA256/SHA1',lambda:cap.selected_bodies(h,{h.CASE+'synthetic_metadata.json':rr})[h.CASE+'synthetic_metadata.json']==existing_raw)
 no('selected source nativeOID mismatch',lambda:cap.selected_bodies(h,{h.CASE+'synthetic_metadata.json':{**rr,'git_blob':'0'*40}}))
 no('selected source length mismatch',lambda:cap.selected_bodies(h,{h.CASE+'synthetic_metadata.json':{**rr,'bytes':rr['bytes']+1}}))
 # Strict finite source/target metadata; no math bodies are read.
 def row(path,p,oid):
  return {'path':path,'origin':str(ENGINE/'BASELINE_MEMBERSHIP.json'),**p,'git_blob':oid,
   'observed_source_mode':292,'role':'SYNTHETIC_METADATA_CONTROL','selection_basis':'No source body read by this test'}
 base=[]
 for path,p in cap.required_carry(h).items():base.append(row(path,p,'1'*40))
 for path,r in h.original_archives().items():base.append(row(path,{k:r[k] for k in ('bytes','sha256')},r['native_blob']))
 scientific=[row(r['repository_path'],{k:r[k] for k in ('bytes','sha256')},r['native_blob']) for r in h.submitted_inventory()]
 def plan(rows):return {'schema':'pr239-root-positive-public-selection-v1','PR':239,'operational_authority':False,'files':rows,'total_files':len(rows),'total_bytes':sum(r['bytes'] for r in rows)}
 p95=plan(base+scientific);p100=plan(base)
 yes('95 includes24carry32archive32attempt',lambda:len(cap.selection(h,p95,'merge95'))==88)
 yes('100 only carry/archive no science',lambda:len(cap.selection(h,p100,'completion100'))==56)
 for key,value in [('PR',239.0),('operational_authority',True),('total_files',88.0),('schema','pr218-root-positive-public-selection-v1')]:
  no('strict selection header '+key,lambda key=key,value=value:cap.selection(h,{**p95,key:value},'merge95'))
 no('extra selection header',lambda:cap.selection(h,{**p95,'extra':True},'merge95'))
 no('missing original32',lambda:cap.selection(h,plan((base+scientific)[:-1]),'merge95'))
 no('missing carry',lambda:cap.selection(h,plan((base+scientific)[1:]),'merge95'))
 no('duplicate selected target',lambda:cap.selection(h,plan(base+scientific+[base[0]]),'merge95'))
 for suffix in ('_private/raw.json','ROOT_COMPLETE239_READ_X/receipt.json','nested/ROOT_COMPLETE218_WORK_X/a.json','packet/a.json','paper.pdf','source.zip'):
  no('selected private/binary '+suffix,lambda suffix=suffix:cap.selection(h,plan(base+scientific+[row(h.CASE+suffix,{'bytes':1,'sha256':'a'*64},'2'*40)]),'merge95'))
 no('science100 refused',lambda:cap.selection(h,p95,'completion100'))
 modebad=copy.deepcopy(p95);modebad['files'][0]['observed_source_mode']='0444'
 no('selection string mode refused',lambda:cap.selection(h,modebad,'merge95'))
 # Signed canonical raw reconstruction retains final empty gpgsig continuation.
 root='2'*40;parent='1'*40
 payload='tree '+root+'\nparent '+parent+'\nauthor Test <test@example.invalid> 0 +0000\ncommitter Test <test@example.invalid> 0 +0000\n\nsynthetic\n'
 signature='-----BEGIN PGP SIGNATURE-----\nSYNTHETIC\n-----END PGP SIGNATURE-----\n'
 head,body=payload.encode().split(b'\n\n',1);raw=head+b'\ngpgsig '+b'\n '.join(signature.encode().split(b'\n'))+b'\n\n'+body
 j={'sha':cap.native('commit',raw),'tree':{'sha':root},'parents':[{'sha':parent}], 'verification':{'payload':payload,'signature':signature}}
 yes('signed trailingLF raw identity',lambda:cap.raw_commit(j)==raw)
 wrong=copy.deepcopy(j);wrong['verification']['signature']=signature.rstrip('\n')
 no('signed lost final empty line refused',lambda:cap.raw_commit(wrong))
 no('signed wrong metadata root refused',lambda:cap.raw_commit({**j,'tree':{'sha':'3'*40}}))
 unsigned_header='tree '+root+'\nparent '+parent+'\nauthor Test <test@example.invalid> 0 +0000\ncommitter Test <test@example.invalid> 0 +0000\n\n'
 uraw=(unsigned_header+'synthetic\n').encode()
 uj={'sha':cap.native('commit',uraw),'tree':{'sha':root},'parents':[{'sha':parent}],'verification':{'reason':'unsigned','payload':None,'signature':None},
  'author':{'name':'Test','email':'test@example.invalid','date':'1970-01-01T00:00:00Z'},'committer':{'name':'Test','email':'test@example.invalid','date':'1970-01-01T00:00:00Z'},'message':'synthetic'}
 yes('unsigned exact nativeOID recovers oneLF',lambda:cap.raw_commit(uj)==uraw)
 no('unknown signed encoding refused',lambda:cap.raw_commit({**uj,'verification':{'reason':'unknown','payload':None,'signature':None}}))
 # Actual frozen publication validator over prior owned explicitly synthetic receipts.
 fixtures=ENGINE/'_synthetic_controls_04'
 def reference(name):
  p=fixtures/(name+'.json');raw=p.read_bytes();return {'path':str(p),**h.pin(raw)}
 evidence={'publication':reference('publication'),'tracker':reference('tracker')}
 native_views={p:None for p in h.VIEWS};local=dict(native_views)
 baseline=cap.enc({**h.baseline_facts('merge95'),**h.source_baseline(),'dated_eligible_total':99})
 native_views[h.VIEWS[2]]=local[h.VIEWS[2]]=baseline
 native_views[h.VIEWS[4]]=b'program historical\n';local[h.VIEWS[4]]=b'program historical\nlocal review addition\n'
 local[h.VIEWS[1]]=b'case historical reviews\n'
 v95=cap.postimages(h,evidence,'merge95',native_views,local,'2026-10-18T03:00:00Z')
 yes('95 proposals conservative55/39 noadvance',lambda:h.decode(v95[h.VIEWS[2]])['published_count']==39 and h.decode(v95[h.VIEWS[0]])['completed'] is False)
 yes('95 both log prefixes preserved',lambda:v95[h.VIEWS[4]].startswith(native_views[h.VIEWS[4]]) and v95[h.VIEWS[4]].startswith(local[h.VIEWS[4]]))
 n95={p:v95[p] for p in h.VIEWS};l95=dict(n95)
 v100=cap.postimages(h,evidence,'completion100',n95,l95,'2026-10-18T03:01:00Z')
 yes('100 proposal56/40 only239',lambda:h.decode(v100[h.VIEWS[2]])['fully_completed_eligible_PRs']==h.source_baseline()['fully_completed_eligible_PRs']+[239] and h.decode(v100[h.VIEWS[2]])['published_count']==40)
 yes('100 proposal remains conditional/noactualadvance',lambda:h.decode(v100[h.VIEWS[0]])['conditional_proposal_only'] is True and h.decode(v100[h.VIEWS[0]])['advance_to_next_PR_authorized_now'] is False)
 yes('95→100 exact log prefix and latest marker',lambda:all(v100[p].startswith(v95[p]) for p in (h.VIEWS[1],h.VIEWS[4])))
 for phase,n,l in [('merge95',n95,l95),('completion100',native_views,local)]:
  no('wrong historical markers '+phase,lambda phase=phase,n=n,l=l:cap.postimages(h,evidence,phase,n,l,'2026-10-18T03:01:00Z'))
 badn=dict(native_views);badn[h.VIEWS[2]]=cap.enc({**h.baseline_facts('merge95'),**h.source_baseline(),'fully_completed_count':56,'dated_eligible_total':99})
 no('intervening progress refused',lambda:cap.postimages(h,evidence,'merge95',badn,local,'2026-10-18T03:00:00Z'))
 badl=dict(local);badl[h.VIEWS[4]]=b'divergent global history'
 no('divergent actual local/native logs refused',lambda:cap.postimages(h,evidence,'merge95',native_views,badl,'2026-10-18T03:00:00Z'))
 # Authenticated offline native tree replay + exact frozen expected rebuild.
 objects={}
 def tree(flat):
  trie={}
  for path,item in flat.items():
   node=trie;parts=path.split('/')
   for part in parts[:-1]:node=node.setdefault(part,{})
   node[parts[-1]]=item
  def walk(node):
   values={}
   for name,item in node.items():values[name]=('040000','tree',walk(item)) if type(item) is dict else item
   oid=c.tree_hash([(name,*item) for name,item in values.items()]);objects[oid]=values;return oid
  return walk(trie)
 oldleaf=('100644','blob',cap.native('blob',b'old proof\n'))
 flat={h.ATTEMPT+'/old.txt':oldleaf,'foreign-dir':('040000','tree','f'*40),'foreign-mode':('100755','blob','e'*40)}
 root=tree(flat);ts=cap.authenticated_tree_replay(h,c,objects)
 payload={h.ATTEMPT+'/new/proof.txt':b'new proof\n'};pre={p:ts.lookup(root,p) for p in payload}
 projected=cap.projected_attempt(h,c,ts,root,payload,pre)
 expectedroot=tree({h.ATTEMPT+'/old.txt':oldleaf,h.ATTEMPT+'/new/proof.txt':('100644','blob',cap.native('blob',b'new proof\n'))})
 projected_ts=cap.authenticated_tree_replay(h,c,objects)
 yes('project own tree through frozen expected',lambda:projected==projected_ts.lookup(expectedroot,h.ATTEMPT))
 yes('foreign tree not descended',lambda:'f'*40 not in ts.cache)
 yes('opaque own tree100 unchanged',lambda:cap.projected_attempt(h,c,ts,root,{}, {})==ts.lookup(root,h.ATTEMPT))

 # F01: start a separate observer whose opaque attempt envelope does not exist.
 opaque_oid='a'*40
 opaque_root=tree({h.ATTEMPT:('040000','tree',opaque_oid),'foreign-mode':('100755','blob','e'*40)})
 opaque_ts=cap.authenticated_tree_replay(h,c,copy.deepcopy(objects))
 yes('fresh opaque tuple lookup without own envelope',lambda:opaque_ts.lookup(opaque_root,h.ATTEMPT)==('040000','tree',opaque_oid))
 prior_cache=set(opaque_ts.cache);prior_inspected=opaque_ts.inspected
 yes('F01 empty overlay returns untouched opaque node',lambda:cap.projected_attempt(h,c,opaque_ts,opaque_root,{}, {})==('040000','tree',opaque_oid))
 yes('F01 no child GET/replay access',lambda:opaque_oid not in objects and opaque_oid not in opaque_ts.cache and set(opaque_ts.cache)==prior_cache and opaque_ts.inspected==prior_inspected)
 absent_root=tree({'foreign-mode':('100755','blob','e'*40)})
 absent_ts=cap.authenticated_tree_replay(h,c,copy.deepcopy(objects))
 yes('F01 empty/absent boundary preserves absence',lambda:cap.projected_attempt(h,c,absent_ts,absent_root,{}, {}) is None)
 # F02: use the actual accepted-carry map, never the broad preliminary selector.
 extra=h.OLD_CASE+'extra_public_metadata.json';summary=b'owned synthetic public metadata\n';extra_payload={extra:summary}
 no('F02 prior target outside actual carry refused',lambda:cap.final_target_admissibility(h,extra_payload,{},[],'completion100'))
 yes('F02 exact explicitly carry-listed extra accepted',lambda:cap.final_target_admissibility(h,extra_payload,{extra:h.pin(summary)},[],'completion100'))
 no('F02 carry body mismatch refused',lambda:cap.final_target_admissibility(h,extra_payload,{extra:h.pin(b'different')},[],'completion100'))
 yes('F02 own public target accepted',lambda:cap.final_target_admissibility(h,{h.CASE+'report.json':summary},{},[],'completion100'))
 science_path=h.ATTEMPT+'/new_note.txt';science=[{'path':science_path,**h.pin(summary)}]
 no('F02 unlisted science refused95',lambda:cap.final_target_admissibility(h,{science_path:summary},{},[],'merge95'))
 yes('F02 individually listed science accepted95',lambda:cap.final_target_admissibility(h,{science_path:summary},{},science,'merge95'))
 no('F02 science forbidden100',lambda:cap.final_target_admissibility(h,{science_path:summary},{},science,'completion100'))
 no('F02 private current-case target refused',lambda:cap.final_target_admissibility(h,{h.CASE+'_private/a.json':summary},{},[],'completion100'))

 # Replace tuple explicitly; no actual provider/cache is patched.
 bad=copy.deepcopy(objects);bad[root]['foreign-mode']=('100755','blob','d'*40)
 no('corrupt replay native hash refused',lambda:cap.authenticated_tree_replay(h,c,bad).lookup(root,h.ATTEMPT))
 no('offline missing tree refused',lambda:cap.authenticated_tree_replay(h,c,{}).lookup(root,h.ATTEMPT))
 no('wrong native preimage in projection refused',lambda:cap.projected_attempt(h,c,ts,root,{h.ATTEMPT+'/old.txt':b'changed'}, {h.ATTEMPT+'/old.txt':None}))
 yes('frozen production sources unchanged',lambda:cap.file_ref(ENGINE/'SOURCE_MANIFEST.json',cap.ENGINE_MANIFEST_PIN)[0]['sha256']==cap.ENGINE_MANIFEST_PIN['sha256'])
 # Structural boundaries of high-level actions; no action is executed.
 funcs={n.name:n for n in newtree.body if isinstance(n,(ast.FunctionDef,ast.ClassDef))}
 finalize_text=ast.get_source_segment(SOURCE,funcs['finalize']);capture_text=ast.get_source_segment(SOURCE,funcs['capture'])
 yes('F02 final target check precedes stage write',lambda:finalize_text.index('final_target_admissibility(')<finalize_text.index('out=Output('))
 yes('finalize has no transport construction',lambda:not any(x in finalize_text for x in ('e.API(','GET(','Seed(','Runtime(','WriterLock(')))
 yes('capture never creates Root accepted receipts',lambda:"'accepted':True" not in capture_text and "'evidence_scope':'ACTUAL_ROOT_RECEIPT'" not in capture_text)
 yes('finalize does not create logical acceptance',lambda:"'pr239-root-completion-logical-packet-acceptance-v1'" not in finalize_text)
 yes('guard manifest variable not shadowed by QUEUE row',lambda:'own_raw' in ast.get_source_segment(SOURCE,funcs['source_guard']) and 'own_before' in capture_text)
 return {'schema':'pr239-logical-capture-pure-controls-v1','source_preparation_percent':100,'passed':len(results),'results':results,
  'scope':'OWNED_PURE_FUNCTIONS_AND_AST_ONLY_NO_CAPTURE_OR_FINALIZE_ACTION','no_filesystem_writes':True,
  'source_pin':cap.pin(SOURCE.encode()),'no_API_Seed_Runtime_original_lock_current_five_native_or_provider_effects':True,
  'limits':['No capture/finalize/source_guard/Output high-level action was executed.','Inherited GET receipt/cache accounting is full-AST-identical to accepted218; no real transport was constructed.','Publication receipts read by postimage controls are prior own labelled synthetic fixtures, not actual Root event authority.']}

if __name__=='__main__':print(json.dumps(run_controls(),sort_keys=True,indent=2))
