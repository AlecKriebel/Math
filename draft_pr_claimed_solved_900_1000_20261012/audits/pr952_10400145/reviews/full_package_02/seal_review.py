"""Seal only the deliberately listed public own artifacts; never recurse."""
import datetime,hashlib,json,pathlib
R=pathlib.Path(__file__).resolve().parent
names=[
'RESULT.json','FULL_AUDIT.md','RESEARCH_LOG.md','AUTHENTICATION_START.json','AUTHENTICATION_END.json','COLD_REPLAY.json','INITIAL_ATTACK.md','PRIOR_ASSESSMENT_INTAKE.json',
'REVIEW_NOTES.md','START_TIME.txt','ACTUAL_START_PREFLIGHT_SUMMARY.json','ACTUAL_END_PREFLIGHT_SUMMARY.json','SEALED_INTAKE_AUTHENTICATION.json','PUBLIC_COPY_CLOSURE.json','ORIGINAL_REVIEW_COVERAGE.json','SOURCE_RETRIEVALS.json','HISTORICAL_VALIDATION.json','HARNESS_ADAPTATIONS.json','SUITE_REPLAY_SUMMARY.json','OPTIMIZED_CORE_REPLAY.json','WRAPPER_DIFFS.json','INHERITED_DISPOSITIONS_VERIFIED.json','PRIOR_ISSUES_VERIFIED.json','RECORD_SCHEMA_VALIDATION.json','EARLY_AUTHENTICATION_ERROR.json','LEGACY_REPLAY.json','END_ATTEMPT01_FAILURE.json',
'authenticate.py','authenticate_attempt01_preserved.py','authenticate_seals.py','cold_replay.py','replay_suites.py','optimized_core_replay.py','independent_operations_probe.py','independent_boundaries_probe.py','independent_math.py','probe_finalization_recovery.py','probe_finalization_positive.py','write_dispositions.py','seal_review.py',
'HOSTILE_POSITIVE.stdout.raw','HOSTILE_POSITIVE.stderr.raw','ORIGINAL_MUTATIONS.launch.json','ORIGINAL_MUTATIONS.stdout.raw','ORIGINAL_MUTATIONS.stderr.raw',
'authentication_start_attempt02.stdout.raw','authentication_start_attempt02.stderr.raw','start_preflight_launch.json','end_preflight_launch.json',
'END_ATTEMPT01_end_preflight_launch.json','END_ATTEMPT01_end_preflight.stdout.raw','END_ATTEMPT01_end_preflight.stderr.raw','END_ATTEMPT02_AUTHENTICATION_END.json','END_ATTEMPT02_end_preflight_launch.json']
for mode in ['normal','O','OO','env2']:
 for suffix in ['launch.json','stdout.raw','stderr.raw']:names.append(f'COLD_{mode}.{suffix}')
for group in ['INDEPENDENT_OPS','INDEPENDENT_MATH','BOUNDARIES','FINALIZATION_RECOVERY','FINALIZATION_POSITIVE']:
 for mode in ['normal','O','OO']:
  for suffix in ['launch.json','stdout.raw','stderr.raw']:names.append(f'{group}_{mode}.{suffix}')
for group,labels in [('SUITE',['operations','source_gate','native_recovery','profile','observations']),('OPTCORE',['operations','source_gate','native_recovery'])]:
 for label in labels:
  for mode in ['normal','O','OO']:
   for suffix in ['launch.json','stdout.raw','stderr.raw']:names.append(f'{group}_{label}_{mode}.{suffix}')
for mode in ['normal','O','OO']:
 for suffix in ['stdout.raw','stderr.raw']:names.append(f'LEGACY_{mode}.{suffix}')
for family in ['algebra_falsifier_01','quantum_bridge_01']:
 for suffix in ['launch.json','stdout.raw','stderr.raw']:names.append(f'{family}.{suffix}')
for i in [1,2,3]:
 for suffix in ['launch.json','stdout.raw','stderr.raw']:names.append(f'authentication_end_attempt{i:02d}.{suffix}')
if len(names)!=len(set(names)):raise RuntimeError('duplicate intended public artifact')
mandatory={'RESULT.json','FULL_AUDIT.md','RESEARCH_LOG.md','AUTHENTICATION_START.json','AUTHENTICATION_END.json','COLD_REPLAY.json','INITIAL_ATTACK.md','PRIOR_ASSESSMENT_INTAKE.json'}
files={}
for name in sorted(names):
 if pathlib.PurePosixPath(name).name!=name or name.startswith('private_'):raise RuntimeError('not explicit flat public artifact')
 p=R/name
 if p.is_symlink() or not p.is_file():raise RuntimeError('missing/linked public artifact '+name)
 b=p.read_bytes()
 if name in mandatory and not b.strip():raise RuntimeError('empty mandatory artifact')
 files[name]={'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
result=json.loads((R/'RESULT.json').read_bytes())
if result['clean_for_preprint'] is not False or result['required_issues'][0]['id']!='R952-FULL02-OPS-01':raise RuntimeError('incorrect adverse result')
doc={'schema':'pr952-whole-package-review-seal-v1','utc':datetime.datetime.now(datetime.timezone.utc).isoformat().replace('+00:00','Z'),'reviewer_agent_id':'/root/pr952_full_package_02','pr':952,'problem_id':'10400145','candidate_revision':3,'original_pr_head':'989a532ae1d50894190d010a0a02ba8c3d71ee05','files':files,'explicit_public_allowlist':list(files),'private_bodies_extracts_images_fixtures_excluded':True,'clean_review_credit':False,'review_outcome':'COMPLETE_ADVERSE_WHOLE_CURRENT_PACKAGE_REVIEW','scope':'Deliberately selected reviewer-authored code/reasoning/receipt/hash metadata only. Successful raw preflight source/PR bodies, primary PDFs/extracts/images, compiled/authentication captured bodies, copied engineering sources, scratch fixtures and caches are excluded. All actual raw failures are retained locally; the first local setup traceback is honestly disclosed as tool-transcript retention rather than initially redirected capture.'}
p=R/'MANIFEST.json'
if p.exists():raise RuntimeError('never overwrite sealed review manifest')
p.write_text(json.dumps(doc,indent=2)+'\n');print(json.dumps({'manifest_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'sealed_public_payloads':len(files),'verdict':doc['review_outcome'],'required_finding':'R952-FULL02-OPS-01'},sort_keys=True))
