from pathlib import Path
import hashlib,json,subprocess,datetime
H=Path(__file__).resolve().parent;A=H.parent.parent;repo=Path('/Users/alec/Documents/Math')
def need(v,m):
 if not v:raise RuntimeError(m)
def bind(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
snap=json.loads((A/'SUBMITTED_SNAPSHOT.json').read_text());head=snap['head'];rows=[]
parents=subprocess.check_output(['git','-c','gc.auto=0','rev-list','--parents','-n','1',head],cwd=repo,text=True).split();need(parents==[head]+snap['parents'],'actual original parents')
for e in snap['files']:
 b=subprocess.check_output(['git','-c','gc.auto=0','show',head+':'+e['path']],cwd=repo);name=Path(e['path']).name;need(b==(A/'submitted'/name).read_bytes(),'actualgitbytes');need(bind(b)=={k:e[k] for k in ['bytes','sha256']},'snapshot binding');rows.append({'path':e['path'],'actual_original_git_blob_equal':True})
original={p.name:bind(p.read_bytes()) for p in (A/'submitted').iterdir()};current={p.name:bind(p.read_bytes()) for p in (A/'current_edition').iterdir()};correction=json.loads((A/'CURRENT_EDITION_CORRECTION.json').read_text());need(correction['original_files']==original and correction['current_files']==current,'both9maps');changed=sorted(n for n in original if original[n]!=current[n]);need(changed==sorted(e['path'] for e in correction['changes']) and len(changed)==6,'sixchanges');need(json.loads((A/'current_edition/ACCEPTANCE.json').read_text())['historical_20261011_acceptance']==json.loads((A/'submitted/ACCEPTANCE.json').read_text()),'historical acceptance literal object');cm=json.loads((A/'current_edition/EDITORIAL_CHANGE_MAP.json').read_text());need(cm['historical_20261011_editorial_map']==json.loads((A/'submitted/EDITORIAL_CHANGE_MAP.json').read_text()),'historical map literal object')
for n in cm['current_original_markdown']:need(cm['current_original_markdown'][n]==original[n] and cm['current_outputs'][n]==current[n],'changedmarkdownmaps')
spans=[]
for e in cm['current_byte_changes']:
 n=e['path'];o=(A/'submitted'/n).read_bytes();c=(A/'current_edition'/n).read_bytes();a,b=e['original_byte_range'];x,y=e['current_byte_range'];need(bind(o[a:b])==e['original_fragment'] and bind(c[x:y])==e['current_fragment'],'bytefragment');spans.append({'path':n,'original_byte_range':[a,b],'current_byte_range':[x,y],'fragments_verified':True})
for n in cm['current_original_markdown']:
 o=(A/'submitted'/n).read_bytes();c=(A/'current_edition'/n).read_bytes();oe=ce=0
 for e in [e for e in cm['current_byte_changes'] if e['path']==n]:
  a,b=e['original_byte_range'];x,y=e['current_byte_range'];need(o[oe:a]==c[ce:x],'unmappedchangedbytes');oe=b;ce=y
 need(o[oe:]==c[ce:],'unmappedtailchange')
result={'at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'actual_original_head':head,'actual_original_parents':parents[1:],'original_git_files':rows,'current9_and_original9_exact':True,'changed_files':changed,'historical_acceptance_and_map_nested_exact_objects':True,'current_change_map_exact_fragments_and_unchanged_regions':spans,'limits':'No authentication of unavailable older proof/audit/supplement bytes or original aggregate-check program/input bytes is inferred from the surviving acceptance/map/summary.'};(H/'EDITION_CHECKS.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'original_git_files':len(rows),'changed_files':changed,'verified_spans':len(spans)}))
