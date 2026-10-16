from pathlib import Path
import json,sys,datetime
R=Path(__file__).resolve().parent;A=R.parents[1];D=A/'preprint';f=json.loads((D/'FREEZE.json').read_bytes());orig=json.loads((A/'ORIGINAL_FILE_RECORDS.json').read_bytes())['files'];boundary=sys.argv[1];rawpath=R/('AUTHENTICATION_'+boundary+'.json');a=json.loads(rawpath.read_bytes());keep=R/'private'/('AUTHENTICATION_'+boundary+'_mechanical.json');keep.write_bytes(rawpath.read_bytes())
p=json.loads((R/'private'/('PREFLIGHT_'+boundary+'.stdout.raw')).read_bytes());g=p['gate'];native=g['native'];pr=g['pr'];actual_originals={}
for name,want in orig.items():
 observed=a['original'][name]
 if not observed['match']:raise RuntimeError('actual original not matched')
 actual_originals[name]={**want,'archive_mode':'100644','disk_and_archive_match':True}
if not all(x['match'] for k in ['files','evidence_files','dependencies','original'] for x in a[k].values()):raise RuntimeError('authentication mismatch')
summary={'utc':p['utc'],'status':p['status'],'actual_main':g['parent'],'original_pr_head':p['original_pr_head'],'PR_state':pr['state'],'isDraft':pr['isDraft'],'baseRefName':pr['baseRefName'],'actual_live_base':pr['currentBaseRefOid'],'changed_paths_count':g['paths']['count'],'submitted_status':'claimed_solved','submitted_declared_turns':'1/5','source':g['source'],'native':native,'authority_equal':g['bracket']['authority_equal'],'Git_network_fetch_performed':p['Git_network_fetch_performed'],'service_mutations':p['service_mutations'],'acceptance_authority':False}
(R/('ACTUAL_'+boundary+'_PREFLIGHT_SUMMARY.json')).write_text(json.dumps(summary,indent=2)+'\n')
out={'status':'PASS','utc':p['utc'],'original_pr_head':f['original_pr_head'],'freeze_sha256':a['freeze']['sha256'],'package_manifest_sha256':f['package_manifest_sha256'],'future_helpers':f['future_helpers'],'candidate_files':{n:x['actual'] for n,x in a['files'].items()},'originals':actual_originals,'evidence_files':{n:x['actual'] for n,x in a['evidence_files'].items()},'operations_dependencies':{n:x['actual'] for n,x in a['dependencies'].items()},'operations_inventory':a['operations_inventory'],'core':a['core'],'observed_mechanical_utc':a['timestamp'],'fresh_live_gate':summary,'mechanical_matches':a['summary'],'private_raw_output_retained':True}
rawpath.write_text(json.dumps(out,indent=2)+'\n');print(boundary,'PASS',a['summary'])
