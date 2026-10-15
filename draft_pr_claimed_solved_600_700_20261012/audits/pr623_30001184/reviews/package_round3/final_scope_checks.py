from pathlib import Path
import hashlib,json,sys,importlib.util,contextlib,io,tempfile,datetime
from unittest.mock import patch
R=Path(__file__).resolve().parent;A=R.parent.parent;P=A/'publication';EX=R/'tmp/extracted';sys.dont_write_bytecode=True
spec=importlib.util.spec_from_file_location('scope_read_only',A/'prepare_integration.py');p=importlib.util.module_from_spec(spec);spec.loader.exec_module(p)
D='10.5281/zenodo.99999999';META={'number':623,'state':'OPEN','baseRefName':'main','headRefName':p.BRANCH,'headRefOid':p.ORIGINAL,'isCrossRepository':False,'headRepositoryOwner':{'login':'AlecKriebel'}}
ROW='| 651 | 30001184 / OWR-3392-012 | title | .1 | 6 | 3 | 2009 | claimed_solved | 1/5 | | | |\n'
results={'python_optimization':sys.flags.optimize,'scope_controls':[]}
for label,status,turns in [('wrong_status','queued','1/5'),('wrong_turns','claimed_solved','0/5'),('excess_turns','claimed_solved','2/5')]:
 row=ROW.replace('claimed_solved',status).replace('1/5',turns).encode()
 with tempfile.TemporaryDirectory(dir=R/'tmp')as td:
  with patch.object(p,'local_state',return_value={}),patch.object(p,'PUSHED_RECEIPT',Path(td)/'absent'),patch.object(p,'pr_metadata',return_value=META),patch.object(p,'git',return_value=row),patch.object(p,'load_snapshot',side_effect=AssertionError('must not read native')),patch.object(p,'publication_inputs',side_effect=AssertionError('must not read payload')),patch.object(sys,'argv',['fixture','--doi',D]):
   try:p.main()
   except ValueError as err:rejected=str(err)=='live selected PR scope gate'
   else:rejected=False
 if not rejected:raise ValueError(label)
 results['scope_controls'].append({'case':label,'rejects_before_native_or_publication_reads':True})
for label,status,turns in [('main_already_claimed','claimed_solved','0/5'),('main_consumed_turn','queued','1/5')]:
 row=ROW.replace('claimed_solved',status).replace('1/5',turns).encode()
 try:p.patch_queue(row,D)
 except ValueError:rejected=True
 else:rejected=False
 if not rejected:raise ValueError(label)
 results['scope_controls'].append({'case':label,'rejected':True})
# metadata intent exact fields and two named uploads.
m=json.loads((P/'zenodo-deposit.json').read_text());md=m['metadata']
expected={'title':p.TITLE,'upload_type':'publication','publication_type':'preprint','publication_date':'2026-10-13','version':'1.0','access_right':'open','license':'cc-by-4.0','creators':[{'name':'Kriebel, Alec','affiliation':'Independent researcher','orcid':'0009-0001-9320-500X'}]}
if not all(md[k]==v for k,v in expected.items()):raise ValueError('metadata intent mismatch')
if m['files']!=[{'path':'gns_generation_counterexample.pdf'},{'path':'gns_verification.zip'}]:raise ValueError('upload names')
results['metadata_exact_intent']=expected;results['upload_names']=[e['path']for e in m['files']];results['ai_unrefereed_credit_scope_disclosed']=all(w in md['description']for w in ['Burgarth','Facchi','Hillier','Dive','Mintert','vom Ende','AI','unrefereed','first','kernel invariance'])
# ZIP distribution: exactly one PDF (paper), no raw third-party corpus or operational helpers/receipts.
files=[p for p in EX.rglob('*')if p.is_file()]
results['archive_file_count']=len(files);results['archive_pdf_names']=[p.relative_to(EX).as_posix()for p in files if p.suffix=='.pdf']
results['operational_helpers_distributed']=any(p.name in ['prepare_integration.py','record_tracker.py','check_repairs.py']for p in files)
results['raw_or_operation_receipts_distributed']=any('private' in p.relative_to(EX).as_posix()or p.name.startswith(('ZENODO_','TRACKER_','INTEGRATION_'))for p in files)
if results['operational_helpers_distributed']or results['raw_or_operation_receipts_distributed']or results['archive_pdf_names']!=['gns_generation_counterexample.pdf']:raise ValueError('distribution scope')
# Repair manifest's exact final hashes, plus original entry snapshots, all rechecked.
repair=json.loads((A/'PACKAGE_ROUND2_REPAIRS.json').read_text());pins=repair['new_inputs_sha256']
results['repair_pins']={n:{'expected':h,'actual':hashlib.sha256((A/n).read_bytes()).hexdigest()}for n,h in pins.items()}
if not all(d['expected']==d['actual']for d in results['repair_pins'].values()):raise ValueError('repair pin mismatch')
initial=json.loads((R/'INPUT_SHA256.json').read_text());final={n:{'size':(A/n).stat().st_size,'sha256':hashlib.sha256((A/n).read_bytes()).hexdigest()}for n in initial}
results['initial_snapshot_unchanged']=initial==final
if not results['initial_snapshot_unchanged']:raise ValueError('input changed while reviewed')
(R/'FINAL_INPUT_RECHECK.json').write_text(json.dumps({'checked_utc':datetime.datetime.now(datetime.UTC).isoformat(),'all_initial_inputs_unchanged':True,'final':final,'repair_pins_match':True},indent=2)+'\n')
results['result']='PASS';(R/('FINAL_SCOPE_CHECKS_O'+str(sys.flags.optimize)+'.json')).write_text(json.dumps(results,indent=2)+'\n');print(json.dumps({'result':'PASS','scope_controls':len(results['scope_controls']),'repair_pins_verified':len(pins),'input_unchanged':True}))
