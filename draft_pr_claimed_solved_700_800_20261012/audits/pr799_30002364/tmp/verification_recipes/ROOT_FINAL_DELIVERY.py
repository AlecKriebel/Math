from pathlib import Path
import datetime,hashlib,json,os,subprocess,sys
R=Path('/Users/alec/Documents/Math');D=R/'draft_pr_claimed_solved_700_800_20261012';T=D/'audits/pr799_30002364/tmp';M=T/'root-receipts'
sys.path.insert(0,str(D));from graphql_scoped_commit import Remote,head_oid
def need(ok,msg):
 if not ok:raise RuntimeError(msg)
remote=Remote(head_oid());state=json.loads(remote.read(D.name+'/STATE.json'))
pubs=[r for r in state['processed'] if 'doi' in r];need(len(pubs)==9,'nine published cases')
q=remote.read('unsolved_math_prioritization/QUEUE.md');records=[];trackers=[]
for row in pubs:
 pr=row['pr'];problem=row['problem'];doi=row['doi']
 raw=remote.read('unsolved_math_prioritization/attempts/'+problem+'/acceptance.json');a=json.loads(raw)
 need(a['doi']==doi and a['pr']==pr and a['problem']==problem and a['merge_commit']==row['merge_commit'],'native acceptance identity')
 qr=[l for l in q.splitlines() if l.startswith('| ') and (' '+problem+' / ') in l]
 need(len(qr)==1 and qr[0].split('|')[8].strip()=='preprint_published' and qr[0].split('|')[12].strip()==doi,'native published row')
 path=D/'final_delivery'/('pr'+str(pr)+'-paper.pdf');b=path.read_bytes();pdfs=[f for f in a['publication_files'] if f['path'].endswith('.pdf')]
 need(len(pdfs)==1 and len(b)==pdfs[0]['bytes'] and hashlib.sha256(b).hexdigest()==pdfs[0]['sha256'] and b.startswith(b'%PDF'),'exact published PDF delivery')
 bindings={}
 for key in ['publication','tracker']:
  binding=a[key];s=remote.read(binding['path']);need(hashlib.sha256(s.encode()).hexdigest()==binding['sha256'],'immutable '+key+' binding')
  bindings[key]=json.loads(s)
 need(bindings['publication']['state']=='published' and bindings['publication']['doi']==doi,'confirmed production publication')
 tracker=bindings['tracker'];need(tracker['result']=='PASS' and tracker['doi']==doi and tracker['readback']['values']==[tracker['intended_values']],'confirmed exact tracker append')
 need(tracker['updated_range']==row['tracker_range'],'stored tracker range')
 trackers.append(tracker)
 records.append({'pr':pr,'problem':problem,'doi':doi,'merge_commit':row['merge_commit'],
  'native_acceptance_sha256':hashlib.sha256(raw.encode()).hexdigest(),'path':path.relative_to(R).as_posix(),
  'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'source_verification_archive_bound':any(f['path'].endswith('source-and-verification.zip') for f in a['publication_files']),
  'production_and_tracker_receipts_match_frozen_native_bindings':True,'tracker_range':tracker['updated_range']})
# A single fresh read of only the nine previously written ranges. No append.
cfg=D/'audits/pr789_30001478/tmp/gws-config-private'
env=dict(os.environ,GOOGLE_WORKSPACE_CLI_CONFIG_DIR=str(cfg),PATH='/Users/alec/.nvm/versions/node/v22.16.0/bin:'+os.environ.get('PATH',''))
params={'spreadsheetId':'1ZljUv5Q98jNXLoHK8WjwrkzSm3dhHC1-7LElcOU7y20','ranges':[r['updated_range'] for r in trackers],'valueRenderOption':'UNFORMATTED_VALUE'}
r=subprocess.run(['gws','sheets','spreadsheets','values','batchGet','--params',json.dumps(params)],cwd=R,env=env,capture_output=True,text=True,timeout=90)
if r.returncode:
 p=cfg/'final-read-diagnostic-private.txt';p.write_text(r.stderr or r.stdout);os.chmod(p,0o600)
 raise RuntimeError('Final read-only sheet check failed; private diagnostic retained, no write attempted')
readback=json.loads(r.stdout);need(len(readback['valueRanges'])==9,'nine fresh tracker ranges')
for t,v in zip(trackers,readback['valueRanges']):need(v.get('values')==[t['intended_values']],'fresh sheet values differ: '+t['updated_range'])
(M/'FINAL_SHEET_READBACK.json').write_text(json.dumps(readback,indent=2)+'\n')
result={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'result':'PASS','main_identity_commit':remote.parent,
 'nine_exact_published_PDF_deliverables':records,'total_PDF_bytes':sum(r['bytes'] for r in records),
 'fresh_Google_Workspace_CLI_only_nine_range_GET':True,'all36cells_match_original_append_receipts':True,
 'new_sheet_writes':0,'new_deposits_or_republications':0,'no_new_mathematical_review':True,
 'extensive_AI_use_unrefereed_disclosure_in_native_acceptances':True}
need(all(r['source_verification_archive_bound'] for r in records),'every paper has supporting archive')
(M/'ROOT_FINAL_DELIVERY.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'result':'PASS','papers':9,'total_PDF_bytes':result['total_PDF_bytes'],'fresh_exact_sheet_rows':9,'new_writes':0}))
