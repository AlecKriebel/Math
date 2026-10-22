#!/usr/bin/env python3
"""Independent bounded artifact reader; archived programs are never imported."""
from pathlib import Path
import datetime as dt,hashlib,json,zipfile,io,urllib.request,time,concurrent.futures,re,subprocess
H=Path(__file__).resolve().parent;P=H/'private';R=H.parents[1];C='39e8a7e1f675baa98d4907e7831edcbf2bf53767'
def sha(b):return hashlib.sha256(b).hexdigest()
def require(v,m):
 if not v:raise RuntimeError(m)
def load(p):return json.loads(p.read_text())
def dump(p,v):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(v,indent=2,ensure_ascii=False)+'\n')
def fetch(url):
 for i in range(4):
  try:
   req=urllib.request.Request(url,headers={'User-Agent':'bounded-independent-audit/1.0'})
   with urllib.request.urlopen(req,timeout=45) as f:return f.read(),{'url':url,'final_url':f.url,'status':f.status,'at':dt.datetime.now(dt.timezone.utc).isoformat()}
  except Exception:
   if i==3:raise
   time.sleep(.5)
def immutable(path,ref=C):
 q=P/'support'/path
 if q.exists():return q.read_bytes(),{'cached_immutable_ref':ref,'path':path}
 b,receipt=fetch('https://raw.githubusercontent.com/AlecKriebel/Math/'+ref+'/'+path)
 q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(b);return b,receipt
out={'at':dt.datetime.now(dt.timezone.utc).isoformat(),'checkpoint':C,'prs':[],'records':[],'packages':[]}
for n in range(1132,1141):
 v=load(P/f'pr{n}/CAPTURE.json');require(v['all_metadata_bound'] and v['live_equals_pinned_files'],f'PR{n}binding');require(not v['queue_files'],f'PR{n}QUEUE');require(all(x['equal'] for x in v['files']),f'PR{n}blobs');out['prs'].append({k:v[k] for k in ['number','head','base','body_sha256','state','merged','draft','file_count']})
for n in [23063072,23372668,23442649,23443039]:
 d=P/f'record{n}';v=load(d/'record_start.json');require(v['state']=='done' and v['submitted'] is True,f'record{n}state');rr={'record':n,'doi':v['doi'],'files':[]}
 for f in v['files']:
  b=(d/f['key']).read_bytes();require(len(b)==f['size'] and f['checksum']=='md5:'+hashlib.md5(b).hexdigest(),f'payload{n}/{f["key"]}')
  rr['files'].append({'name':f['key'],'bytes':len(b),'sha256':sha(b),'md5':f['checksum']})
 _,rr['doi_resolution']=fetch('https://doi.org/'+v['doi']);require(rr['doi_resolution']['final_url'].rstrip('/')==f'https://zenodo.org/records/{n}',f'DOI{n}')
 out['records'].append(rr)
for n,pr in [(23442649,1135),(23443039,1136)]:
 d=P/f'record{n}';v=load(d/'record_start.json');zf=next(f['key'] for f in v['files'] if f['key'].endswith('.zip'));pdf=next(f['key'] for f in v['files'] if f['key'].endswith('.pdf'));z=zipfile.ZipFile(d/zf);names=z.namelist();payload={f.filename for f in z.infolist() if not f.is_dir()};require(len(names)==len(set(names)) and all(not p.startswith('/') and '..' not in Path(p).parts for p in names) and z.testzip() is None,f'ZIP{n}')
 manifest=json.loads(z.read('SOURCE_MANIFEST.json'));require(set(manifest)==payload-{'SOURCE_MANIFEST.json'},f'closedmanifest{n}')
 for path,pin in manifest.items():
  b=z.read(path);require(pin['bytes']==len(b) and pin['sha256']==sha(b),f'manifest{n}/{path}')
 meta=json.loads(z.read('zenodo-metadata.json'));dep=json.loads(z.read('zenodo-deposit.json'));require(dep['metadata']==meta,f'deposit{n}')
 comparisons=[]
 for k,value in meta.items():
  actual=v['metadata'].get(k)
  if k=='license':actual=v['metadata']['license']['id']
  if k=='upload_type':actual=v['metadata']['resource_type']['type']
  if k=='publication_type':actual=v['metadata']['resource_type']['subtype']
  eq=value==actual;normal=False
  if not eq and pr==1136 and k=='description':normal=value.replace('\u2019',"'")==actual
  require(eq or normal,f'nativefield{n}/{k}');comparisons.append({'field':k,'equal':eq,'documented_apostrophe_normalization':normal})
 hroot=P/f'pr{pr}/head';copies=[]
 for f in hroot.rglob('*'):
  if f.is_file():
   matches=[name for name in names if name.endswith('/inputs/'+f.name)]
   require(len(matches)==1 and z.read(matches[0])==f.read_bytes(),f'headcopy{pr}/{f.name}');copies.append({'path':str(f.relative_to(hroot)),'sha256':sha(f.read_bytes())})
 require(z.read('output/pdf/'+pdf)==(d/pdf).read_bytes(),f'embeddedpdf{n}')
 detail=load(P/f'pr{pr}/checkpoint/PR{pr}_PUBLICATION_COVERAGE_DETAILS.json');frozen=detail.get('six_frozen_assets',detail.get('all_six_release_assets'));ref=detail.get('immutable_review_commit',detail.get('postfreeze_commit'));reviewitems=detail.get('reviews',detail.get('two_clean_reviews'))
 audit=Path(f'draft_pr_actual_claims_1100_1200_20261017/audits/pr{pr}_'+('30000052' if pr==1135 else '2307037'));pub=audit/'publication';release={}
 for path,pin in frozen.items():
  b,rec=immutable(str(pub/path),ref);require(len(b)==pin['bytes'] and sha(b)==pin['sha256'],f'frozen{pr}/{path}');release[path]=b
 kit=zipfile.ZipFile(io.BytesIO(release['output/zenodo-upload-kit.zip']));kn=kit.namelist();expected=['README.md',zf,pdf,'zenodo-deposit.json','zenodo-metadata.json'];require(set(kn)==set(expected) and len(kn)==5,f'kitmembers{pr}')
 for path in [zf,pdf,'zenodo-metadata.json']:
  src=release['output/'+path] if path==zf else release['output/pdf/'+path] if path==pdf else release[path];require(kit.read(path)==src,f'kit{pr}/{path}')
 flat=json.loads(kit.read('zenodo-deposit.json'));require(flat['metadata']==meta and flat['files']==[{'path':pdf},{'path':zf}],f'flatdeposit{pr}')
 reviewresults=[]
 for rev in reviewitems:
  texts={}
  for name in ['REPORT.md','ARTIFACT_RECEIPT.json','START_PINS.json','END_PINS.json']:
   b,rec=immutable(str(audit/'reviews'/rev['round']/name),ref);texts[name]=b
  require(sha(texts['REPORT.md'])==rev['report_sha256'] and sha(texts['ARTIFACT_RECEIPT.json'])==rev['receipt_sha256'],f'reviewhash{pr}')
  start=json.loads(texts['START_PINS.json']);end=json.loads(texts['END_PINS.json']);receipt=json.loads(texts['ARTIFACT_RECEIPT.json'])
  def pins(value):
   if isinstance(value,list):return {x['path']:x for x in value}
   return value
  if pr==1135 and rev['round']=='package_04':sp=pins(start['files']);ep=pins(end['frozen_six_files'])
  elif pr==1135:sp=pins(start['frozen_six']);ep=pins(end['checks'])
  elif rev['round']=='package_01':sp=pins(start['files']);ep=pins(end['release'])
  else:sp=pins(start['files']);ep=pins(end['release_input_files'])
  for path,pin in frozen.items():
   for mapping in [sp,ep]:
    key=path if path in mapping else 'publication/'+path
    require(key in mapping and mapping[key]['sha256']==pin['sha256'] and mapping[key].get('bytes',mapping[key].get('size'))==pin['bytes'],f'structuredreleasepin{pr}/{path}')
  records=receipt.get('files',receipt.get('entries',receipt.get('authored_files')));records=pins(records)
  for name in ['REPORT.md','START_PINS.json','END_PINS.json']:
   require(name in records and records[name]['sha256']==sha(texts[name]),f'receiptbinding{pr}/{name}')
  reviewresults.append({'round':rev['round'],'report_sha256':sha(texts['REPORT.md']),'receipt_sha256':sha(texts['ARTIFACT_RECEIPT.json']),'all_six_hashes_in_both_pin_records':True})
 out['packages'].append({'pr':pr,'record':n,'zip_entries':len(names),'manifest_payloads':len(manifest),'closed_manifest':True,'native_metadata_fields':comparisons,'head_copies':copies,'embedded_pdf_equal':True,'portablekit_exact_five':True,'immutable_review_commit':ref,'reviews':reviewresults,'six_assets':frozen})
# External archive formats deliberately are not forced into the local packaging schema.
z=zipfile.ZipFile(P/'record23063072/OWR-14298580-008-source.zip');names=z.namelist();require(len(names)==99 and sum(not f.is_dir() for f in z.infolist())==92 and z.testzip() is None,'externalzip')
a=z.read('reproducibility/claimant/outputs/certificate_Sigma_30_47_83.txt');b=z.read('reproducibility/verifier/certificate_Sigma_30_47_83.txt');require(a==b,'external certificates');out['external_format']={'entries':99,'payloads':92,'complete_internal_manifest':False,'embedded_pdf':False,'two_certificate_copies_equal':True,'certificate_sha256':sha(a)}
# Bind the historical guarded append and independent review acceptance without executing them.
audit='final_full_solution_sweep_20261020_01a15be7/audits/pr1132_30005952';values={}
for name in ['LEDGER_RECONCILIATION_PLAN.json','ROOT_LEDGER_REVIEW_ACCEPTANCE.json','reconcile_external_ledger.py','LEDGER_RECONCILIATION_INTENT.json','LEDGER_RECONCILIATION_RESPONSE.json','LEDGER_PUBLICATION_VERIFICATION.json']:
 b,_=immutable(audit+'/'+name);values[name]=b
acc=json.loads(values['ROOT_LEDGER_REVIEW_ACCEPTANCE.json']);plan=json.loads(values['LEDGER_RECONCILIATION_PLAN.json']);require(sha(values['LEDGER_RECONCILIATION_PLAN.json'])==acc['plan_sha256'] and sha(values['reconcile_external_ledger.py'])==acc['helper_sha256'],'adoption')
for pin in acc['review_pins']:
 b,_=immutable(audit+'/'+pin['path']);require(sha(b)==pin['sha256'],'independentreviewpin')
rows=load(P/'ledger_start.json')['values'];require(rows[180]==plan['proposed_row'],'fresh row181 exactplan');out['reconciliation']={'review_acceptance_before_append':acc['at']<json.loads(values['LEDGER_RECONCILIATION_INTENT.json'])['at']<json.loads(values['LEDGER_PUBLICATION_VERIFICATION.json'])['at'],'adopted_helper_hash':acc['helper_sha256'],'adopted_plan_hash':acc['plan_sha256'],'independent_review_pins':len(acc['review_pins']),'fresh_row181_equals_plan':True}
# Broad semantic leads: known target IDs, source aliases, primary URLs, names and theorem vocabulary.
patterns={1132:r'30005952|14298580.?008|23063072|Alfieri|Binns|strong.{0,3}geography|Heegaard',1133:r'30006113|30004905|30006114|2609.04414|strong.{0,5}density|feedback.{0,5}vertex|Fiorini',1134:r'30005752|14298157.?001|2609.37452|quantum.{0,5}greedy|Qiyue',1135:r'30000052|723.?005|23442649|23372668|random.{0,15}lattice|Novak|Hinrichs|45858',1136:r'2307037|022.?7037|23443039|Baernstein|squared.{0,5}pole|fixed.{0,5}area|7\.37',1137:r'30000515|1276.?008|Godeaux|bicanonical|46059',1138:r'2302066|022.?2066|Hinkkanen|2\.66|growth.{0,10}hierarchy|omega.{0,5}1.{0,10}entire',1139:r'30000374|1116.?002|Camerlo|ordinal.{0,8}color|46028',1140:r'30002450|12732.?002|2008.10168|two.{0,4}puncture|twice.{0,4}puncture|Geuenich|Miranda.Olvera'}
out['ledger']={'rows':len(rows),'headers':rows[0],'leads':{str(pr):[i for i,row in enumerate(rows,1) if re.search(pat,' '.join(map(str,row)),re.I)] for pr,pat in patterns.items()},'all_primary_doi_unique_for_targets':all(sum(len(r)>2 and str(n) in r[2] for r in rows)==1 for n in [23063072,23442649,23443039])}
dump(H/'CHECKS.json',out);print(json.dumps({'status':'PASS','prs':len(out['prs']),'files':sum(x['file_count'] for x in out['prs']),'records':len(out['records']),'packages':out['packages'],'ledger':out['ledger'],'reconciliation':out['reconciliation']},indent=2))
