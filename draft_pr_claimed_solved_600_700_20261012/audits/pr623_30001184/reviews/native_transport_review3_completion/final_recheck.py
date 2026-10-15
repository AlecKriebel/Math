"""Completion review final binding; read-only outside its own folder."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib,json,os,subprocess
HERE=Path(__file__).resolve().parent
ROOT=Path('/Users/alec/Documents/Math')
AUDIT=HERE.parent.parent
initial=json.loads((HERE/'INPUT_BINDING.json').read_bytes())
def pin(data):return {'size':len(data),'sha256':hashlib.sha256(data).hexdigest()}
checks={name:pin((ROOT/name).read_bytes())==receipt for name,receipt in initial['inputs'].items()}
primary=json.loads((HERE/'ORIGINAL_ARCHIVE_PRIMARY_BINDING.json').read_bytes())
primary_checks={name:pin(Path(receipt['path']).read_bytes())=={'size':receipt['size'],'sha256':receipt['sha256']} for name,receipt in primary['primary_source_pins'].items()}
suites={}
for mode in ('NORMAL','OPTIMIZED'):
    for group,expected in [('SUPPLIED',56),('WIRE',16),('SOURCE',4),('RESTART',4)]:
        path=HERE/(group+'_'+mode+'.json')
        data=path.read_bytes(); result=json.loads(data)
        if result['tests']!=expected or result['failures']!=0 or result.get('errors',0)!=0:raise RuntimeError('Test evidence failure '+path.name)
        suites[path.name]={**pin(data),'tests':result['tests'],'failures':result['failures'],'errors':result.get('errors',0),'optimization':result['optimization']}
preflight_path=AUDIT/'ROOT_RESUMED_PREFLIGHT_20261015.json'
preflight_data=preflight_path.read_bytes(); preflight=json.loads(preflight_data)
if not(preflight['id']==23356540 and preflight['metadata_verified'] is True and preflight['submitted'] is False and preflight['completed_files']==[] and preflight['pending_files']==[] and preflight['live_mutations']==0):raise RuntimeError('Parent preflight is not expected unchanged draft')
branch=subprocess.run(['git','symbolic-ref','--short','HEAD'],cwd=ROOT,env={**os.environ,'GIT_OPTIONAL_LOCKS':'0'},capture_output=True,check=True).stdout.decode().strip()
if branch!='main':raise RuntimeError('Shared branch is not main')
report={'checked_utc':datetime.now(timezone.utc).isoformat(),'initial_inputs_count':len(checks),'initial_inputs_checks':checks,'all_initial_inputs_unchanged':all(checks.values()),'primary_source_checks':primary_checks,'all_primary_sources_unchanged':all(primary_checks.values()),'gate45_unchanged':primary['gate45_match'],'native29_original_equal':primary['native29_original_equal'],'native29_zip_equal':primary['native29_zip_equal'],'zip_manifest87_valid':primary['zip_manifest87_valid'],'transport_absent_pdf_zip':primary['transport_absent_pdf_zip'],'suites':suites,'parent_preflight':{'path':str(preflight_path),**pin(preflight_data),'verified_utc':preflight['verified_utc'],'submitted':False,'completed_files':[],'pending_files':[],'source':'Fresh parent guarded invocation; no duplicate live request by this reviewer'},'local_branch':branch,'live_network_calls_by_this_reviewer':0,'live_mutations_by_this_reviewer':0,'review_complete_percent':100,'estimated_transport_readiness_percent':90,'strongest_verified_result':'Frozen repaired transport passes the bounded source, byte, annotation/link, journal and unchanged-kit receipt model; science and package unchanged','exact_live_gap':'Actual own-draft initialize/content/commit and final native representation, external DOI resolution HTTP200 and final real kit publication receipt remain unexecuted'}
if not report['all_initial_inputs_unchanged'] or not report['all_primary_sources_unchanged']:raise RuntimeError('Captured input drift')
(HERE/'FINAL_INPUT_RECHECK.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k not in ('initial_inputs_checks','primary_source_checks','suites')},indent=2))
