"""Confined final manifest/seal builder; does not write candidate or external state."""
from pathlib import Path
import datetime, hashlib, json, os, stat
D=Path(__file__).resolve().parent
A=D.parent
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
def require(ok,msg):
    if not ok: raise RuntimeError(msg)
def describe(p):
    b=p.read_bytes()
    return {'path':str(p),'size':len(b),'sha256':hashlib.sha256(b).hexdigest(),'mode_octal':oct(stat.S_IMODE(p.stat().st_mode))}
def write(name,obj):
    (D/name).write_text(json.dumps(obj,indent=2)+'\n')
require(not (D/'FINAL_REVIEW_SEAL.json').exists(),'final seal already exists; no overwrite')
inputs=json.loads((D/'CONSUMED_INPUTS.json').read_text())
by_path={}
for i in inputs:
    p=Path(i['path']);r=describe(p)
    require((r['size'],r['sha256'])==(i['size'],i['sha256']),'consumed input changed: '+str(p))
    by_path.setdefault(str(p),dict(r,consumptions=[]))['consumptions'].append({'utc':i['consumed_utc'],'mode':i['mode']})
baseline=json.loads((D/'CANDIDATE_BASELINE.json').read_text())
for i in baseline:
    r=describe(Path(i['path']))
    require((r['size'],r['sha256'])==(i['size'],i['sha256']),'candidate changed: '+i['path'])
native=[r for p,r in by_path.items() if p.startswith(str(A/'native_proposal_v1')+'/') or p.startswith(str(A/'original_submission')+'/')]
require(len(baseline)==23 and len(native)==71,'unexpected stability coverage')
first=describe(D/'FIRST_ASSESSMENT_SEAL.json')
require(first['sha256']=='18cb40546f1dabcdf8252e3ddda8fe36e866e6f328c91b47ac06f2b0bf7895bd','initial seal changed')
require(first['mode_octal']=='0o444','initial seal no longer read-only')
write('FINAL_CANDIDATE_STABILITY.json',{
    'utc':now,'status':'PASS_FROZEN_CANDIDATE_ALL_CONSUMED_INPUTS_AND_INITIAL_SEAL_BYTE_STABILITY',
    'initial_seal_sha256':first['sha256'],'initial_seal_mode_octal':first['mode_octal'],
    'frozen_candidate_paths_verified':len(baseline),'native_and_historical_paths_verified':len(native),
    'all_unique_consumed_input_paths_verified':len(by_path),'changed_paths':[],
    'candidate_baseline':baseline,'native_and_historical_paths':[{k:v for k,v in r.items() if k!='consumptions'} for r in native]})
res=json.loads((D/'RESULT.json').read_text());res['completed_utc']=now;res['final_consumed_input_paths_verified']=len(by_path)
res['input_output_manifest']='INPUT_OUTPUT_MANIFEST.json';res['public_output_whitelist']='PUBLIC_OUTPUT_WHITELIST.json';res['final_review_seal']='FINAL_REVIEW_SEAL.json'
write('RESULT.json',res)
with (D/'RESEARCH_LOG.md').open('a') as f:
    f.write('\n- '+now+': Final CRC/symlink and Ferudun v1 provider-file identity checks passed; exact native Sections 1–5 diff is only one trailing blank line. Final rehash verifies all 23 candidate/config paths, 71 native/historical paths and '+str(len(by_path))+' unique consumed inputs unchanged. Complete input/output manifest and explicit public whitelist sealed. Completion estimate: 100%; no scientific correction required and historical-priority limits retained.\n')
allowed=[
 'REVIEW.md','RESULT.json','FIRST_ASSESSMENT_SEAL.json','INDEPENDENT_DERIVATION.md',
 'independent_universal_check.py','independent.normal.json','independent.optimized.json',
 'PRIMARY_COMPARISON.md','independent_prior_deductions.py','prior.normal.json','prior.optimized.json',
 'PRIOR_DEDUCTION_RUNS.json','prior.ann_corrupt.normal.stderr.txt','prior.ann_corrupt.optimized.stderr.txt',
 'PACKAGE_REPRODUCTION_AND_INTEGRITY.json','package.normal.json','package.optimized.json',
 'package_controls.stdout.json','package_controls.stderr.txt','FINAL_ADDITIONAL_VALIDATION.json',
 'FINAL_CANDIDATE_STABILITY.json','FRESH_PROVIDER_OBSERVATIONS.json','FRESH_ORIGINAL_PROOF_COMPARISON.json',
 'RESEARCH_LOG.md','CANDIDATE_BASELINE.json','CONSUMED_INPUTS.json','audit_package.py','finalize_review.py',
 'INPUT_OUTPUT_MANIFEST.json','PUBLIC_OUTPUT_WHITELIST.json','FINAL_REVIEW_SEAL.json','FINAL_REVIEW_SEAL_SHA256.txt']
whitelist={'utc':now,'policy':'Explicit per-file whitelist; every other R2 file is private by default. Whitelisting is eligibility, not an instruction or authorization to publish.',
 'allowed_relative_paths':allowed,
 'explicit_exclusions':['scratch/**','tmp/**','PRIMARY_HISTORY_OBSERVATIONS.json','raw third-party/provider source bodies','third-party PDF/text/HTML bodies','rendered candidate pages and extracted PDF text','all files not explicitly allowed'],
 'rationale':'Public entries contain this review, independent deductions/code, reproduction diagnostics, chronology observations, and size/hash provenance only. No third-party source-body redistribution or private credentials is permitted. Input manifests name and hash sources without redistributing bodies.'}
write('PUBLIC_OUTPUT_WHITELIST.json',whitelist)
excluded={'INPUT_OUTPUT_MANIFEST.json','FINAL_REVIEW_SEAL.json','FINAL_REVIEW_SEAL_SHA256.txt'}
outputs=[]
for p in sorted(D.rglob('*')):
    if p.is_file() and str(p.relative_to(D)) not in excluded:
        r=describe(p);r['relative_path']=str(p.relative_to(D));r['public_output_eligible']=r['relative_path'] in allowed
        r['classification']='OWN_PUBLIC_REVIEW_ARTIFACT' if r['public_output_eligible'] else 'PRIVATE_SCRATCH_OR_SOURCE_DERIVED_OUTPUT'
        outputs.append(r)
manifest={'utc':now,'input_consumption_records':len(inputs),'unique_input_paths':len(by_path),
 'inputs':list(by_path.values()),'outputs':outputs,
 'output_self_reference_exclusions':sorted(excluded),
 'self_reference_resolution':'This manifest cannot include its own final digest; FINAL_REVIEW_SEAL.json pins this manifest and whitelist and the principal review outputs. The seal digest is recorded separately. No circular/self-referential hash claim is made.',
 'private_outputs_must_not_be_redistributed':True,
 'temporary_scope_exception':'The first supplied-control replay wrote automatically cleaned system temporary mutant files outside R2. This is disclosed in REVIEW/RESULT/log; no surviving files there are claimed as inventoried. The complete replay was rerun with TMPDIR confined to R2/scratch/tmp.'}
write('INPUT_OUTPUT_MANIFEST.json',manifest)
# Rehash the output list once before sealing so no stale output hash passes.
for r in outputs:
    fresh=describe(Path(r['path']))
    require((fresh['size'],fresh['sha256'])==(r['size'],r['sha256']),'output changed before seal: '+r['path'])
seal_paths=['REVIEW.md','RESULT.json','INPUT_OUTPUT_MANIFEST.json','PUBLIC_OUTPUT_WHITELIST.json','FINAL_CANDIDATE_STABILITY.json','FIRST_ASSESSMENT_SEAL.json']
seal={'utc':now,'status':'FINAL_INDEPENDENT_REVIEW_SEALED','scientific_verdict':res['scientific_verdict'],
 'substantive_findings':[],'seal_first_requirement_satisfied':True,'scope_deviation_disclosed':True,
 'principal_outputs':[describe(D/n) for n in seal_paths],
 'frozen_candidate_principal_bytes':[i for i in baseline if Path(i['path']).name in ['property_s_counterexample.pdf','property_s_support.zip','property_s_counterexample.tex','metadata.json','MANIFEST.json']],
 'all_output_hashes_recorded_except_explicit_self_references':True,'review_completion_percent':100,
 'publication_performed':False,'historical_priority_first_exclusive_and_independence_certified':False}
data=(json.dumps(seal,indent=2)+'\n').encode()
fd=os.open(D/'FINAL_REVIEW_SEAL.json',os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o444)
with os.fdopen(fd,'wb') as f:f.write(data)
sha=hashlib.sha256(data).hexdigest()
fd=os.open(D/'FINAL_REVIEW_SEAL_SHA256.txt',os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o444)
with os.fdopen(fd,'w') as f:f.write(sha+'  FINAL_REVIEW_SEAL.json\n')
print(json.dumps({'utc':now,'status':'FINAL_SEAL_CREATED','seal_sha256':sha,'input_records':len(inputs),'unique_inputs':len(by_path),'inventoried_outputs':len(outputs),'principal_outputs':seal['principal_outputs']},indent=2))
