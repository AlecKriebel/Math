"""Own postmerge read-only authentication; never runs an operation entry point."""
import os,sys,hashlib,json,pathlib,sqlite3,types
R=pathlib.Path('/Users/alec/Documents/Math');P=R/'draft_pr_claimed_solved_900_1000_20261012';A=P/'audits/pr946_6000001';D=A/'preprint';W=A/'reviews/full_package_07'
os.environ.update(GIT_CONFIG_COUNT='1',GIT_CONFIG_KEY_0='gc.auto',GIT_CONFIG_VALUE_0='0',TMPDIR=str(W/'private/tmp'))
def need(x,m):
 if not x: raise RuntimeError(m)
def sha(x):return hashlib.sha256(x).hexdigest()
def pin(x):return {'bytes':len(x),'sha256':sha(x)}
core=(P/'accept_pr946.py').read_bytes();need(pin(core)=={'bytes':85902,'sha256':'8e1a0d7b3ca6e5d72e76415541b393fbfbe52e307368bc86b9e7982d5be27cd7'},'external core')
g={'__name__':'review07_captured_core','__file__':str(P/'accept_pr946.py')};exec(compile(core,str(P/'accept_pr946.py'),'exec',optimize=0),g)
inventory='f4742eca6ddd628ecac1e704fed772a17837d42d4d0fdef42c73d3cda3bed254';freeze_pin='9af8f2570af53b6a6658a7998ac08927829c8747be7c764a8d2c392dc6c6afe1'
context=g['capture_inventory'](inventory);f=g['freeze_check'](g['read_regular'](D/'FREEZE.json'),freeze_pin,context);g['disposition_check']();snapshot,originals=g['original_check']();built=g['archive_check'](f,originals)
need(len(f['files'])==223 and len(f['evidence_files'])==77,'223+77 closure');need(len(context['captured'])==7 and len(f['future_helpers'])==6,'dependency closure');need(built['zip_members']==220,'220 outer members')
row=g['claimed_row'](g['blob'](g['HEAD'],g['QUEUE']));need(sha(row.rstrip(b'\r\n'))=='11fbd85ea991520337b918a2caa719737acff2d202c796aa93e3343c61403895','original exact claimed row')
accepted=g['load'](A/'ACCEPTANCE.json');merged=g['merged_gate'](accepted,f);pr=merged['actual_PR_readback'];g['main_destination'](pr,merged=True);need(merged['merge_commit']=='918948421d00b1184a88ca07017134726b466adb','exact actual merge');need(sha(pr['body'].encode())==f['pr_description_sha256'],'original live body')
need(g['run'](['git','branch','--show-current']).strip()=='main','remain main')
con=sqlite3.connect('file:'+str(R/'unsolved_math_prioritization/cache/catalog.sqlite')+'?mode=ro',uri=True)
cache=con.execute('select payload,report from records where key=?',('6000001',)).fetchone();need(cache is not None,'actual records(key,payload,report)');p,r=map(json.loads,cache);con.close()
source={'statement_sha256':sha(p['statement'].encode()),'review_sha256':sha(json.dumps([p,r],sort_keys=True).encode()),'read_only':True,'schema':'records(key,payload,report)'}
need(source['statement_sha256']==g['STATEMENT'] and source['review_sha256']==g['REVIEW'],'raw cache identity')
operator=(A/'publication_operator.py').read_bytes();op=pin(operator);need(op=={'bytes':9163,'sha256':'4d219a1543a1c01ef3653ef48ade657db4dabc4c0fafe8cd245c0d13af86524e'},'external operator');need(operator==(A/'publication_operator_versions/operator01.py').read_bytes(),'preserved operator')
g['candidate_state_check'](f,freeze_pin,context);g['original_check']();g['archive_check'](f,originals)
reported_originals={k:{**v,'archive_mode':'100644','disk_and_archive_match':True} for k,v in originals.items()}
result={'status':'PASS','utc':g['utc_now'](),'original_pr_head':g['HEAD'],'freeze_sha256':freeze_pin,'package_manifest_sha256':f['package_manifest_sha256'],'future_helpers':f['future_helpers'],'candidate_files':f['files'],'evidence_files':f['evidence_files'],'payloads':built['payload_files'],'archive_members':built['zip_members'],'originals':reported_originals,'merged_gate':merged,'original_claimed_row_sha256_no_lf':sha(row.rstrip(b'\r\n')),'original_pr_body_sha256':sha(pr['body'].encode()),'source_cache':source,'dependency_inventory':context['inventory'],'inspected_publication_operator':op,'outer_optimization':sys.flags.optimize,'captured_core_optimization':0,'postmerge_scope_gate':True}
out=W/('AUTHENTICATION_'+(sys.argv[1] if len(sys.argv)>1 else 'START')+'.json');out.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'status':'PASS','receipt':str(out),'utc':result['utc'],'state':pr['state'],'originals':len(originals),'candidate_files':len(f['files']),'external_evidence':len(f['evidence_files'])}))
