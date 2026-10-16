"""Extend root's93 actual-directory repair controls with the12 full-service cases.

The entire source of both root baseline and independent sealed-service program
is externally pinned before execution. All services and Git are fake; the
candidate05 transport context and synthetic terminal05 are explicit.
"""
import sys
if not sys.flags.isolated or sys.flags.optimize:
    raise RuntimeError('Use -I -B without optimization')
from pathlib import Path
import contextlib, hashlib, io, json

BASE = Path('/Users/alec/Documents/Math/draft_pr_claimed_solved_900_1000_20261012/audits/pr946_6000001/REVIEW05_CLOSURE_CONTROLS.py')
raw_base = BASE.read_bytes()
assert hashlib.sha256(raw_base).hexdigest() == '715e3c1b7d4e431a01aeb4728b76f3912e82bf2c9b01e48c453e524addac0988'
base = raw_base.decode()
ending = "output = Path(args.output).resolve()"
assert base.count(ending) == 1
base = base[:base.index(ending)]
# The repaired initial approval deliberately creates no ACCEPTANCE file. A
# subsequent fresh entry therefore raises FileNotFoundError, as well as the
# historical RuntimeError on a stale approval. Preserve the root82 baseline;
# disclose this narrow expected-exception adaptation for the new subject.
marker = 'late_namespace = {'
assert base.count(marker) == 1
base = base.replace(marker,
    'late = late.replace("except RuntimeError as ex:records.append", '
    '"except (RuntimeError, OSError) as ex:records.append")\n' + marker)
ns = {'__name__':'_root_full_closure93_', '__file__':str(BASE)}
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(base,str(BASE),'exec',dont_inherit=True,optimize=0),ns)
args, report = ns['args'], ns['report']
assert args.expect_defect is False and report['status'] == 'PASS'
assert report['root_control_count'] == 93
INPUT, scratch, manifest = ns['INPUT'], ns['scratch'], ns['manifest']
service = (INPUT/'service_boundaries.py').read_text()
replace = ns['replace']
service = replace(service, "O=Path(__file__).resolve().parent;R=Path('/Users/alec/Documents/Math')",
                  "O=Path(scratch_path);INPUT=Path(input_path);R=Path('/Users/alec/Documents/Math')")
service = replace(service, "raw=(P/'accept_pr946.py').read_bytes();assert hashlib.sha256(raw).hexdigest()=='62fa159687104c889195863303fa5642d877e52257bc9e4fb2bc97e89ea2b919'",
                  "raw=Path(args.core).read_bytes();assert hashlib.sha256(raw).hexdigest()==args.core_sha256")
service = service.replace("(O/'AUTHENTICATION_START.json')", "(INPUT/'AUTHENTICATION_START.json')")
service = replace(service,
    "N['review_check']=drift;call(lambda:N['accepted_review_check'](accepted,freeze,ctx));N['review_check']=actual_review",
    """N['review_check']=drift;error=None
 try:call(lambda:N['accepted_review_check'](accepted,freeze,ctx))
 except RuntimeError as caught:error=str(caught)
 finally:N['review_check']=actual_review
 assert fired[0] and error is not None,error""")
service = replace(service, "'defect_reproduced':True,'fresh_entry_error':str(ex)",
                  "'rejected_by_closing_guard':True,'closing_error':error,'fresh_entry_error':str(ex)")
service = service[:service.index("\n(O/'SERVICE_BOUNDARIES.json').write_text")]
sn = {'__name__':'_root_complete_fake_services_', '__file__':str(INPUT/'service_boundaries.py'),
      'args':args,'input_path':str(INPUT),'scratch_path':str(scratch)}
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(service,str(INPUT/'service_boundaries.py'),'exec',dont_inherit=True,optimize=0),sn)
assert len(sn['cases']) == 12
report['cases'].extend(sn['cases'])
report.update(root_control_count=len(report['cases']),
              root93_baseline_source_sha256=hashlib.sha256(raw_base).hexdigest(),
              full_positive_service_paths='Actual captured-kit stage/publish/inspect dispatch, tracker append/readback/dedup, native tree CAS/retry plus actual native_verify, final metadata/readback/completion/recovery; only services and Git transport fake.',
              root_fixture_context='Immutable candidate05 inventory/full histories with separately selected subject code; NEW entire independent review must also test actual eventual current06 context.',
              actual_external_mutations=0)
report['source_programs']['service_boundaries.py']=manifest['files']['service_boundaries.py']
assert report['root_control_count'] == 105
output = Path(args.output).resolve()
assert output.parent == ns['A'] and output.suffix == '.json'
output.write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({'status':'PASS','controls':105,'subject_core_sha256':args.core_sha256,
                  'actual_external_mutations':0}))
