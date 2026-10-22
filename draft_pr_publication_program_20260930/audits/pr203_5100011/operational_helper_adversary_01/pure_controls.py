from pathlib import Path
from collections import Counter
from datetime import datetime,timezone
import ast,hashlib,importlib.util,json
D=Path(__file__).resolve().parent;A=D.parent
# Only actual immutable original custody is read. No lifecycle constructor is invoked.
f=A/'native_publication_preparation_01/make_native.py';sp=importlib.util.spec_from_file_location('operational_audit_actual_custody',f);n=importlib.util.module_from_spec(sp);sp.loader.exec_module(n)
old=n.originals()
if len(old)!=18 or sum(map(len,old.values()))!=59989:raise RuntimeError('Original archive count/bytes')
changed={'README.md','SOURCES.md','MANIFEST.json','readiness.json','RESEARCH_LOG.md'}
if len(set(old)-changed)!=13 or 'PROOF.md' not in set(old)-changed:raise RuntimeError('13 native originals')
# Read-only AST shape/order evidence for pre-launch marker and baseline checks.
publish=A/'publication_operations_01/publish_exact.py';tracker=A/'publication_operations_01/update_tracker.py'
pt=ast.parse(publish.read_text());invoke=next(x for x in pt.body if isinstance(x,ast.FunctionDef) and x.name=='invoke')
marker_calls=[x.lineno for x in ast.walk(invoke) if isinstance(x,ast.Call) and isinstance(x.func,ast.Name) and x.func.id=='durable_json' and x.args and isinstance(x.args[0],ast.Name) and x.args[0].id=='marker']
launch=[x.lineno for x in ast.walk(invoke) if isinstance(x,ast.Call) and isinstance(x.func,ast.Attribute) and isinstance(x.func.value,ast.Name) and x.func.value.id=='subprocess' and x.func.attr=='run']
if len(marker_calls)!=1 or len(launch)!=1 or marker_calls[0]>=launch[0]:raise RuntimeError('Marker must precede mutation launch')
source=publish.read_text();required=['if marker.exists():raise RuntimeError','os.fsync(out.fileno())','os.fsync(fd)',"mode in ['stage','publish']"]
if not all(s in source for s in required):raise RuntimeError('Missing durable one-attempt guard')
ts=tracker.read_text();required=['original_rows=original_baseline(inflight,doi,row)',"'original_preappend_baseline'",'pin(p)!=ref[\'pin\']','Counter(original_rows)-Counter(ra)','os.fsync(out.fileno())','os.fsync(fd)']
if not all(s in ts for s in required):raise RuntimeError('Missing original recovery baseline enforcement')
# Explicit dummy-only counterexample; this is not scientific/tracker data and is never sent.
header=('DUMMY_HEADER','','','');foreign=('DUMMY_FOREIGN_ROW','','','');own=('DUMMY_NEW_ROW','','DUMMY-NOT-A-DOI','')
original=[header,foreign];recovery_before1=[header,own];recovery_before2=[header,own];after=[header,own]
old_accepts=not(Counter(recovery_before1)-Counter(after)) and not(Counter(recovery_before2)-Counter(after))
new_accepts=not(Counter(original)-Counter(after))
if not old_accepts or new_accepts:raise RuntimeError('Recovery deletion witness')
retained_after=[header,foreign,own]
if Counter(original)-Counter(retained_after):raise RuntimeError('Valid retention rejected')
# Compile/parse all helpers without execution or API/module loader invocation.
check=json.loads((A/'ROOT_PREPUBLICATION_OPERATIONAL_HELPER_CHECK_01.json').read_bytes())
pins={}
for rel in check['safe_files']:
 b=(A/rel).read_bytes();ast.parse(b.decode());pins[rel]={'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
report={'UTC':datetime.now(timezone.utc).isoformat(),'status':'PASS','actual_original_files':18,'actual_original_bytes':59989,'native_scientific_historical_unchanged_set_size':13,'original_PROOF_retained':True,'durable_marker_call_line':marker_calls[0],'child_launch_line':launch[0],'dummy_recovery_counterexample':{'old_fresh_only_predicate_accepts_deletion':old_accepts,'new_original_baseline_predicate_accepts_deletion':new_accepts,'valid_original_retention_accepted':True},'current_helper_pins':pins,'no_fake_scientific_artifact_or_publication_fact_created':True,'no_external_API_or_mutation_invoked':True}
(D/'PURE_CONTROLS_RECEIPT.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
