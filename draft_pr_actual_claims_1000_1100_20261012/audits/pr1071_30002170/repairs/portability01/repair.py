"""Bounded WHOLE03-P3-01 repair. Atomic writes; no Git or remote actions."""
import hashlib, json, os, sys, zipfile
sys.dont_write_bytecode = True
from datetime import datetime, timezone
from pathlib import Path
D = Path(__file__).resolve().parent
A = D.parents[1]
P = A / 'NEWpreprint_v1_0'
ZIP = 'PR1071_preprint_v1_0_support.zip'
CHANGED = ['README.md', 'SUPPLEMENT.md', 'scripts/check.py', 'scripts/verify_package.py',
           'INPUT_COPY_MAP.json', 'PACKAGE_MANIFEST.json', ZIP, ZIP+'.sha256', 'UPLOAD_BINDINGS.json']
def now(): return datetime.now(timezone.utc).isoformat()
def need(ok, msg):
    if not ok: raise RuntimeError(msg)
def read(p): return json.loads(p.read_text())
def atomic(p, b):
    p.parent.mkdir(parents=True, exist_ok=True)
    temp = p.with_name(p.name+'.portability01-tmp')
    need(not temp.exists(), 'Temporary path exists')
    temp.write_bytes(b if isinstance(b, bytes) else b.encode())
    os.replace(temp, p)
def write(p, obj): atomic(p, json.dumps(obj, indent=2)+'\n')
def pin(p, name):
    b=p.read_bytes(); return {'path':str(name), 'bytes':len(b), 'sha256':hashlib.sha256(b).hexdigest()}
def log(msg, percent):
    with (D/'RESEARCH_LOG.md').open('a') as f: f.write('\n'+now()+' — '+str(percent)+'%: '+msg+'\n')

def before():
    need(not (D/'BEFORE_PINS.json').exists(), 'Before capture exists')
    initial = {r['path']:r for r in read(D/'BASELINE_INPUT_PINS.json')['rows']}
    for r in initial.values(): need(pin(A/r['path'], r['path'])==r, 'Input changed since entry '+r['path'])
    rows=[]
    for name in CHANGED:
        dst=D/'before/NEWpreprint_v1_0'/name
        atomic(dst, (P/name).read_bytes())
        rows.append({'original_path':'NEWpreprint_v1_0/'+name, 'before_snapshot':str(dst.relative_to(A)), **pin(dst, name)})
    write(D/'BEFORE_PINS.json', {'utc':now(), 'rows':rows})
    log('All 763 entry inputs rehashed unchanged; exact before bytes captured for nine necessary interfaces, including old ZIP. Contract selected: complete recursive schema/type/exact comparison, explicit finite derived-float policies, exact sample inputs, residual and positivity guards. Tested runtime claim will be limited to installed CPython3.11.8/3.14.6 binary64.', 15)

GUARD = '''# Explicit binary64 diagnostic tolerances; these are acceptance envelopes,
# not interval error bounds or a proof of cross-runtime numerical accuracy.
COVARIANCE_ABS_TOL = 2.0**-49  # eight binary64 epsilons; max observed drift is one
DERIVED_REL_TOL = 2.0**-47     # 32 binary64 epsilons for libm-derived positive values
def float_policy(path):
    if path == ('L1_fthird_numeric',):return (DERIVED_REL_TOL,0.0,'derived_relative')
    if len(path)==3 and type(path[1]) is int:
        if path[0]=='finite_covariance_identity_float_cross_checks' and path[2] in ('direct','grouped','difference'):
            return (0.0,COVARIANCE_ABS_TOL,'covariance_absolute')
        if path[0]=='constant_float_checks' and path[2] in ('D_H','Pbar_f','Pbar_g','c_H'):
            return (DERIVED_REL_TOL,0.0,'derived_relative')
    return (0.0,0.0,'exact_float')  # H sample inputs and any other float stay exact
def result_guard(result,expected):
    require(sys.float_info.radix==2 and sys.float_info.mant_dig==53 and sys.float_info.max_exp==1024,'Diagnostic requires IEEE754 binary64 floats.')
    require(type(result) is dict and type(expected) is dict,'Result roots must be objects.')
    coverage={'exact_nonfloat_leaves':0,'exact_float':0,'derived_relative':0,'covariance_absolute':0}
    def compare(value,baseline,path):
        label='/'.join(map(str,path)) or '<root>'
        require(type(value) is type(baseline),'Result type differs: '+label)
        if type(baseline) is dict:
            require(value.keys()==baseline.keys(),'Result field set differs: '+label)
            for key in baseline:compare(value[key],baseline[key],path+(key,))
        elif type(baseline) is list:
            require(len(value)==len(baseline),'Result list length differs: '+label)
            for i,(v,b) in enumerate(zip(value,baseline)):compare(v,b,path+(i,))
        elif type(baseline) is float:
            require(math.isfinite(value) and math.isfinite(baseline),'Nonfinite float: '+label)
            rel,absolute,policy=float_policy(path)
            require(abs(value-baseline)<=max(absolute,rel*max(abs(value),abs(baseline))),'Floating diagnostic differs: '+label)
            coverage[policy]+=1
        else:
            require(value==baseline,'Exact result differs: '+label)
            coverage['exact_nonfloat_leaves']+=1
    # Only the top-level UTC is excluded; every other container, key and leaf
    # is visited. Rational identities, normalization, text and integers are exact.
    compare(canonical(result),canonical(expected),())
    require(result['exact_area_pairing']=='4/45045','Area pairing changed.')
    require(result['L1_f']=='1/128' and result['L1_g']=='1/630','Polynomial L1 norms changed.')
    require(result['L1_gthird']=='113/196','Third-derivative norm changed.')
    require(all(x==['0','0'] for x in result['endpoint_traces_phi_derivatives_0_to_3'].values()),'Endpoint traces changed.')
    require(result['L1_fthird_numeric']>0,'Finite norm positivity check failed.')
    for row in result['constant_float_checks']:
        require(0<row['H']<1 and all(row[k]>0 for k in ('D_H','Pbar_f','Pbar_g','c_H')),'Finite constant positivity check failed.')
    for row in result['finite_covariance_identity_float_cross_checks']:
        require(row['direct']>0 and row['grouped']>0,'Finite covariance positivity check failed.')
        require(row['difference']==row['direct']-row['grouped'],'Stored covariance residual is inconsistent.')
        require(abs(row['difference'])<=COVARIANCE_ABS_TOL,'Direct/grouped covariance identity diagnostic failed.')
    return coverage
'''

def mutate():
    need((D/'BEFORE_PINS.json').exists(), 'Capture before bytes first')
    need(not (P/'PORTABILITY_REPAIR_STATUS.json').exists(), 'Already repaired')
    for r in read(D/'BEFORE_PINS.json')['rows']:
        need((A/r['original_path']).read_bytes()==(A/r['before_snapshot']).read_bytes(),'Changed after before capture')
    stamp=now()
    source=(P/'scripts/check.py').read_text().replace('import argparse,hashlib,json,shutil,subprocess,sys,tempfile','import argparse,hashlib,json,math,shutil,subprocess,sys,tempfile')
    source=source.replace('"""Replay byte-exact original finite checker; use explicit guards under -O."""','"""Replay original bytes with exact identities and finite floating diagnostics."""')
    start=source.index('def result_guard(');end=source.index('def expect_rejection(',start)
    source=source[:start]+GUARD+source[end:]
    source=source.replace('    modes=[]','    modes=[];normal_result=None')
    source=source.replace("result=json.loads((dest/'FINITE_CHECKS.json').read_text());result_guard(result,expected)","result=json.loads((dest/'FINITE_CHECKS.json').read_text());coverage=result_guard(result,expected)\n        if normal_result is None:normal_result=canonical(result)\n        else:require(canonical(result)==normal_result,'Same-runtime normal/optimized results differ.')")
    source=source.replace("'full_mathematics_equal_utc_only_difference':True", "'complete_non_utc_field_contract_pass':True,'comparison_coverage':coverage")
    source=source.replace("'guard_implementation':'Explicit RuntimeError guards remain active under python -O. Original checker assertions are active only in normal mode; optimized execution is accepted only after full result comparison by explicit guards.'", "'same_runtime_normal_optimized_non_utc_exact_equal':True,'float_contract':{'covariance_absolute_tolerance':COVARIANCE_ABS_TOL,'derived_relative_tolerance':DERIVED_REL_TOL,'all_other_values':'exact, with finite guards for all floats','ignored_field':'top-level utc only'},'guard_implementation':'Explicit RuntimeError guards remain active under python -O. Original checker assertions are active only in normal mode; optimized execution is accepted only after complete explicit schema/exact/toleranced result validation and same-runtime normal/optimized equality.'")
    atomic(P/'scripts/check.py',source)
    anchor="    for r in json.loads(safe_path(root,'INPUT_COPY_MAP.json').read_text())['copies']:\n"
    verifier=(P/'scripts/verify_package.py').read_text();need(verifier.count(anchor)==1,'Verifier anchor')
    added='''    portability=json.loads(safe_path(root,'PORTABILITY_REPAIR_STATUS.json').read_text())
    require(portability['state']=='PENDING_NEW_COMPLETE_WHOLE04_AFTER_PORTABILITY_REPAIR' and portability['pr']==1071 and portability['head']=='fc37aa5169a0fe6adae0a254c9ee6c1531a2911f', 'Current portability identity/state drift.')
    require(portability['fresh_whole_package_reviews_completed']==3 and portability['minimum_fresh_reviews_required']==2 and portability['new_complete_whole_review_required']==4 and portability['new_complete_whole_review_completed'] is False, 'New complete whole04 requirement/accounting drift.')
    require(portability['latest_complete_review_findings']=={'P0':0,'P1':0,'P2':0,'P3':1} and portability['bounded_repair_findings_fixed']==['WHOLE03-P3-01'], 'Whole03/portability finding accounting drift.')
    require(portability['root_repair_adoption_required'] is True and portability['root_terminal_adoption_required'] is True, 'Portability root adoption requirements drift.')
    require(portability['publication_ready'] is False and portability['issues_resolved'] is False and portability['published'] is False and portability['services_held_after_pr']==1032, 'Portability repair cannot confer readiness or bypass ordered hold.')
    require(portability['source_evidence']=='PORTABILITY_SOURCE_EVIDENCE.json', 'Missing portability finding provenance.')
    evidence=json.loads(safe_path(root,portability['source_evidence']).read_text())
    require(evidence['finding']=='WHOLE03-P3-01' and evidence['kind']=='SAFE_AUTHORED_FINDING_AND_ROOT_EVIDENCE_WITH_EXACT_CUSTODY', 'Portability evidence scope drift.')
    latest=json.loads(safe_path(root,'custody/reviews/package_03/VERDICT.json').read_text())
    require(latest['review_round']==3 and latest['whole_reviews_completed']==3 and latest['finding_counts']=={'P0':0,'P1':0,'P2':0,'P3':1} and len(latest['findings'])==1 and latest['findings'][0]['id']=='WHOLE03-P3-01', 'Complete whole03 finding/accounting drift.')
    root03=json.loads(safe_path(root,'custody/ROOT_WHOLE_PACKAGE_REVIEW_03.json').read_text())
    require(root03['status']=='ADOPT_COMPLETE_WHOLE03_ONE_P3_PENDING_BOUNDED_PORTABILITY_REPAIR_AND_NEW_COMPLETE_WHOLE04' and root03['whole_reviews_completed']==3 and root03['minimum_whole_reviews']==2 and root03['findings']=={'P0':0,'P1':0,'P2':0,'P3':1}, 'Root whole03 adoption missing.')
    require(root03['output_pins_sha256']==sha(safe_path(root,'custody/reviews/package_03/OUTPUT_PINS.json')), 'Root whole03 output seal binding drift.')
'''
    atomic(P/'scripts/verify_package.py',verifier.replace(anchor,added+anchor))
    status={'utc':stamp,'state':'PENDING_NEW_COMPLETE_WHOLE04_AFTER_PORTABILITY_REPAIR','pr':1071,'head':'fc37aa5169a0fe6adae0a254c9ee6c1531a2911f','fresh_whole_package_reviews_completed':3,'minimum_fresh_reviews_required':2,'latest_complete_review_findings':{'P0':0,'P1':0,'P2':0,'P3':1},'bounded_repair_findings_fixed':['WHOLE03-P3-01'],'new_complete_whole_review_required':4,'new_complete_whole_review_completed':False,'root_repair_adoption_required':True,'root_terminal_adoption_required':True,'publication_ready':False,'issues_resolved':False,'published':False,'services_held_after_pr':1032,'source_evidence':'PORTABILITY_SOURCE_EVIDENCE.json','meaning':'Three full reviews completed, minimum two. Whole03 found one new support P3; bounded repair is applied, pending root repair adoption then a NEW COMPLETE whole04 and root terminal adoption. This repair is neither whole04 nor readiness authority. All older status/counters/seals retain exact dated meanings. Mathematical acceptance and UNKNOWN priority/novelty/current-open qualifications are unchanged.'}
    write(P/'PORTABILITY_REPAIR_STATUS.json',status)
    notes='''# Finite-checker portability contract

WHOLE03-P3-01 is the full-result exact-equality failure on installed CPython3.11.8: 26 covariance floating leaves differ from the frozen baseline, with maximum absolute drift 2.220446049250313e-16. Exact identities and normalization agree. The observation is consistent with Python3.12's documented float-sum change; this repair does not claim that change is a complete causal explanation.

The standard-library interfaces are validated on installed CPython3.11.8 and CPython3.14.6 with IEEE754 binary64. Other runtime versions/platforms are unvalidated; the former blanket Python3.9+ compatibility claim is withdrawn. No source/runtime or expected-result substitution occurs. The historical program and baseline remain byte-exact.

scripts/check.py visits every non-utc field recursively. Object key sets, list lengths, types, exact strings/rationals, integer indices, normalization, prose and sample H inputs agree exactly. Every float in actual and baseline must be finite. Derived covariance direct/grouped/difference values use only COVARIANCE_ABS_TOL=2^-49=1.7763568394002505e-15 (eight binary64 epsilons). The numeric radical norm and positive D_H/Pbar_f/Pbar_g/c_H outputs use only DERIVED_REL_TOL=2^-47=7.105427357601002e-15 (32 epsilons), with zero absolute tolerance; acceptance is abs(actual-baseline)<=relative*max(abs(actual),abs(baseline)). All other floats are exact. No leaf is silently discarded; only the top-level utc is ignored. Every constant/norm/covariance value required positive is independently checked positive, the stored covariance difference equals direct-grouped exactly, and its absolute value must be <=2^-49.

The covariance envelope is eight times the observed maximum drift and below one tenth of the original program's 2e-14 absolute identity check. The relative envelope is a small explicit margin for elementary/libm rounding, tested at all frozen samples on the two named runtimes; it is not a proved error bound for other libm/platforms or arbitrary H,m. Both are deliberately finite approximate diagnostic acceptance policies, not interval enclosures, certificates of numerical accuracy, or universal proofs. The unchanged analytic theorem supplies the universal claim. Gross float perturbations, nonfinite values, missing/extra fields, type changes and exact identity/normalization changes reject. Mutations within the named tolerance may be accepted by design.

The original normal execution keeps its assertions active. Its optimized execution disables those assertions; it is accepted only after the wrapper's unconditional schema/exact/toleranced comparison. Within the same runtime, normal and optimized non-utc JSON must additionally agree exactly. Source guards still reject removed conjugation and journal-version boundaries; exact pairing-to-zero and nonpositive constants remain faults. No optimized historical assertion validation is claimed.

PORTABILITY_REPAIR_STATUS.json now governs workflow: three full reviews completed (minimum two), whole03 one P3, bounded repair applied, root repair adoption and then a NEW COMPLETE whole04 plus root terminal adoption required. Readiness/issues-resolved/published are false and services remain held after PR1032. Earlier CASE repair/status, terminal and ROOT records are exact dated history. Mathematical, priority, citation, native metadata and PDF/source qualifications are unchanged. This bounded task performs no actual PDF compile/render or PDF marker, external contact, Git/index/branch or service action.
'''
    atomic(P/'PORTABILITY_REPAIR_NOTES.md',stamp+'\n\n'+notes)
    sources=['reviews/package_03/REPORT.md','reviews/package_03/VERDICT.json','reviews/package_03/OUTPUT_PINS.json','reviews/package_03/SEAL.json','ROOT_WHOLE_PACKAGE_REVIEW_03.json']
    evidence={'utc':stamp,'kind':'SAFE_AUTHORED_FINDING_AND_ROOT_EVIDENCE_WITH_EXACT_CUSTODY','finding':'WHOLE03-P3-01','sources':[pin(A/n,n) for n in sources],'scope':'Complete safe authored whole03 report/verdict/output inventory/seal and root adoption copied exactly. Other execution/source/runtime bodies are omitted individually, not claimed newly replayed. This bounded repair is not complete whole04.','observed_maximum_float_drift':2.220446049250313e-16,'original_exact_identity_claims_unchanged':True,'new_complete_whole_review_required':4}
    write(P/'PORTABILITY_SOURCE_EVIDENCE.json',evidence)
    old=read(P/'INPUT_COPY_MAP.json');need(len(old['copies'])==128,'Original128 rows')
    copies=list(old['copies']);added_names=[]
    def copy(original, destination, snapshot=None):
        src=A/(snapshot or original);dst=P/destination;need(not dst.exists(),'Existing custody destination')
        atomic(dst,src.read_bytes());r={'original_path':original,'package_copy':destination,'bytes':src.stat().st_size,'sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'byte_exact':True,'meaning':'Exact authored evidence/history before portability repair; dated workflow claims retain their historical scope.'}
        if snapshot:r['source_snapshot']=snapshot
        copies.append(r);added_names.append(destination)
    for r in read(D/'BEFORE_PINS.json')['rows']:
        name=r['path']
        if name not in (ZIP,ZIP+'.sha256'):copy(r['original_path'],'history/pre_portability01/'+name,r['before_snapshot'])
    for n in sources:copy(n,'custody/'+n)
    write(P/'INPUT_COPY_MAP.json',{**old,'scope':old['scope']+'; WHOLE03-P3-01 before-interface and safe full authored whole03/root evidence appended after the original128 exact ordered rows.','copies':copies})
    exclusions=[]
    for p in sorted((A/'reviews/package_03').rglob('*')):
        if p.is_file() and not p.is_symlink() and str(p.relative_to(A)) not in sources:
            exclusions.append({**pin(p,p.relative_to(A)),'reason':'Unselected whole03 evidence/program/raw execution history retained exactly locally, not redistributed or claimed replayed here.'})
    for n in (ZIP,ZIP+'.sha256'):
        p=D/'before/NEWpreprint_v1_0'/n
        exclusions.append({**pin(p,p.relative_to(A)),'reason':'Exact previous archive/sidecar retained locally only; old ZIP excluded from distribution.'})
    write(P/'PORTABILITY_COPY_EXCLUSIONS.json',{'utc':stamp,'records':exclusions,'meaning':'Individual omissions preserve prior custody without packaging growing raw command streams, source text/pixels, runtime binaries or old ZIPs. All previous omission ledgers stay exact.'})
    rm=(P/'README.md').read_text()
    rm=rm.replace('CASE_ALIAS_REPAIR_STATUS.json now governs current workflow: the new CASE-1071 P3 support defect is bounded-repaired, but a NEW complete whole03 review and root repair/terminal adoption are required.', 'CASE_ALIAS_REPAIR_STATUS.json preserves the dated case repair stage. PORTABILITY_REPAIR_STATUS.json now governs current workflow: three complete whole reviews (minimum two), whole03 one new P3 support finding, bounded portability repair applied, root repair adoption then a NEW COMPLETE whole04 and root terminal adoption required.')
    rm=rm.replace('Python 3.9+ standard library is sufficient for integrity, archive building and finite-checker replay.', 'The standard-library integrity, archive-building and finite-checker commands are validated on installed CPython 3.11.8 and 3.14.6 with IEEE754 binary64 floats. Other runtime versions/platforms are unvalidated; no blanket Python 3.9+ support claim remains.')
    rm=rm.replace('The checker uses an unchanged isolated copy of the original standard-library program and compares all result mathematics with the frozen original, ignoring only utc.', 'The checker uses an unchanged isolated copy of the original standard-library program and checks every non-utc container, type and field against the frozen baseline. Exact identities/normalization and sample inputs stay exact; only derived floats use the explicit finite tolerances in PORTABILITY_REPAIR_NOTES.md (covariance absolute 2^-49; other derived values relative 2^-47). Nonfinite values reject; covariance residual consistency and positivity are checked. Same-runtime normal/optimized non-utc JSON must also agree exactly. Original assertions run only in normal mode; the optimized pass relies on the explicit wrapper contract.')
    rm=rm.replace('and currently by CASE_ALIAS_REPAIR_STATUS.json for workflow accounting.', 'then by CASE_ALIAS_REPAIR_STATUS.json, and currently by PORTABILITY_REPAIR_STATUS.json for workflow accounting.')
    start=rm.index('## Current support hold and review accounting')
    rm=rm[:start]+'''## Current support hold and review accounting

Three NEW complete whole reviews are complete (minimum two). Whole03 independently retained the mathematics and case repair, and found WHOLE03-P3-01: exact floating replay failed on installed3.11.8. That support finding is now bounded-repaired using the complete finite comparison contract in PORTABILITY_REPAIR_NOTES.md; root repair adoption then a NEW COMPLETE whole04 and root terminal adoption are required. This task is not that full review or readiness authority. Readiness/issues-resolved/published remain false and services held after PR1032. Earlier CASE status, all dated terminal/ROOT seals and counters remain exact history. See PORTABILITY_REPAIR_STATUS.json and PORTABILITY_SOURCE_EVIDENCE.json.

The external native uploader input remains publication/zenodo-deposit.json in the audit tree; its unchanged metadata equals the three unchanged bibliographic objects and it selects the unchanged paper.pdf and same-named current support ZIP. Included deposit.json remains a historical metadata wrapper. The first128 exact copy-map rows remain unchanged and ordered; seven exact before-interface snapshots and five safe complete authored whole03/root records are appended. Individual omissions retain old ZIPs and raw evidence locally. The analytic theorem, source/PDF, citation, source-version boundaries and UNKNOWN priority/novelty/current-open qualifications are unchanged.
'''
    atomic(P/'README.md',rm)
    supp=(P/'SUPPLEMENT.md').read_text()
    supp=supp.replace('The adapter only changes output location through the copy path.', 'The historical source is unchanged; the wrapper isolates its output location and validates the complete result contract.')
    supp=supp.replace('explicit wrapper guards compare every mathematical field with the original baseline, excluding only utc, and test deliberate Fourier/source/pairing failures.', 'explicit wrapper guards compare every non-utc container/type/field under the exact identities and finite derived-float contract in PORTABILITY_REPAIR_NOTES.md, reject nonfinite values, test deliberate Fourier/source/pairing failures, and require same-runtime normal/optimized non-utc JSON to agree exactly. Exact baseline equality across runtimes is not claimed.')
    supp=supp.replace('At least two fresh whole-package reviews were required; both are now completed and the latest has zero actionable findings. Publication readiness and issues-resolved flags remain false pending root terminal integrity adoption.', 'The original two-review completion and former terminal gate are dated history in the unchanged status records. The current portability gate requires root repair adoption, then a NEW COMPLETE whole04 and root terminal adoption; three complete reviews have finished, with one new P3 in whole03. Publication readiness and issues-resolved remain false.')
    supp=supp.replace('TERMINAL_STATUS.json and FINAL_ACCEPTANCE.md govern current workflow accounting.', 'TERMINAL_STATUS.json and FINAL_ACCEPTANCE.md governed workflow accounting at that dated stage; the final portability paragraph below gives the current gate.')
    supp += '\nCurrent portability repair ('+stamp+'): three NEW complete whole reviews have completed (minimum two). Whole03 found one new P3 support finding, WHOLE03-P3-01, after retaining the mathematical/case controls. The bounded portability repair uses complete schema/type/field coverage, exact rational/normalization/sample values, finite-only derived-float tolerances (covariance absolute2^-49, numeric norm and constant outputs relative2^-47), residual consistency and positive-value checks. CPython3.11.8 and3.14.6 binary64 are the validated runtimes; others are unvalidated. These are finite approximate diagnostics, not interval/universal certificates. PORTABILITY_REPAIR_STATUS.json supersedes earlier workflow claims: root repair adoption then NEW COMPLETE whole04 and root terminal adoption required, readiness/issues-resolved/published false, services held after PR1032. Every older status/counter/seal remains exact dated history. No theorem/proof/source/PDF/bibliographic/native/citation or historical checker/baseline change, new compile/render/PDF marker, historical omitted-program replay or priority clearance is asserted.\n'
    atomic(P/'SUPPLEMENT.md',supp)
    manifest=read(P/'PACKAGE_MANIFEST.json');names={r['path'] for r in manifest['members']}
    names.update(added_names+['PORTABILITY_REPAIR_STATUS.json','PORTABILITY_REPAIR_NOTES.md','PORTABILITY_SOURCE_EVIDENCE.json','PORTABILITY_COPY_EXCLUSIONS.json'])
    manifest['policy']+='; complete finite portability contract, separate whole04/root hold, exact pre-portability history and original128 ordered copies preserved.'
    manifest['members']=[pin(P/n,n) for n in sorted(names)];write(P/'PACKAGE_MANIFEST.json',manifest)
    temp=P/(ZIP+'.portability01-tmp');need(not temp.exists(),'Temporary ZIP exists')
    with zipfile.ZipFile(temp,'w',compression=zipfile.ZIP_STORED,allowZip64=False) as z:
        for name in sorted(names|{'PACKAGE_MANIFEST.json'}):
            i=zipfile.ZipInfo(name,date_time=(2026,10,14,0,0,0));i.create_system=3;i.external_attr=0o100644<<16;i.compress_type=zipfile.ZIP_STORED
            z.writestr(i,(P/name).read_bytes())
    os.replace(temp,P/ZIP)
    archive=pin(P/ZIP,ZIP);atomic(P/(ZIP+'.sha256'),archive['sha256']+'  '+ZIP+'\n')
    binding=read(P/'UPLOAD_BINDINGS.json');binding['archive']['bytes']=archive['bytes'];binding['archive']['sha256']=archive['sha256'];binding['manifest_sha256']=pin(P/'PACKAGE_MANIFEST.json','')['sha256'];write(P/'UPLOAD_BINDINGS.json',binding)
    write(D/'BUILD_SUMMARY.json',{'utc':now(),'archive':archive,'members':len(names)+1,'copy_rows':len(copies),'original128_ordered_rows_unchanged':copies[:128]==old['copies'],'new_custody_copies':added_names,'individual_omissions':len(exclusions)})
    log('Atomic bounded code/prose/status/custody/manifest/binding repair applied. Original inputs/history remain retained, archive rebuilt closed. No new validation outcomes are claimed yet.',45)
    print(json.dumps(read(D/'BUILD_SUMMARY.json'),indent=2))
if __name__=='__main__': {'before':before,'mutate':mutate}[sys.argv[1]]()
