#!/usr/bin/env python3
"""Read-only PR218 package/history audit; writes only beside this file."""
from pathlib import Path, PurePosixPath
from datetime import datetime, timezone
from collections import Counter
import difflib, hashlib, json, os, subprocess, sys, zipfile

O = Path(__file__).resolve().parent
A = O.parent
S = A / 'authenticated_sources_01'
P = S / 'existing_publication_audit/preprint'
H = P / 'history/before_review01_M1_fix_20261015'
checks = []
def check(name, result, **evidence):
    checks.append({'name': name, 'pass': bool(result), **evidence})
def sha(data): return hashlib.sha256(data).hexdigest()
def readj(path): return json.loads(path.read_text())
def pin(path, record, name):
    data = path.read_bytes()
    check(name, len(data) == record['bytes'] and sha(data) == record['sha256'],
          path=str(path.relative_to(A)), actual_bytes=len(data), actual_sha256=sha(data),
          expected_bytes=record['bytes'], expected_sha256=record['sha256'])
    return data

# Recompute every materialized source pin and native Git object ID without Git mutation.
pin(A/'ROOT_NATIVE_CUSTODY_ACCEPTANCE_01.json', {'bytes':7054,'sha256':'4b4deaed33b198a3e9814a46536108eed5c49cc26ff81975afd760b464d9e663'}, 'root_custody_acceptance_pin')
mp = S/'SOURCE_MATERIALIZATION_MANIFEST.json'
pin(mp, {'bytes':276014,'sha256':'16abd824d189596e2bb54101af72c2c1046a1f0d17a70ba130a019495226965d'}, 'materialization_manifest_pin')
m = readj(mp)
check('manifest_count', len(m['files']) == m['file_count'] == 391)
for r in m['files']:
    p = Path(r['path'])
    b = pin(p, r, 'materialized/'+str(p.relative_to(S)))
    native = hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
    check('native_blob/'+str(p.relative_to(S)), native == r['native_blob'], actual_git_blob=native)

# Both historical review seals, frozen submission objects and archive inventories.
for n, expected in [('fresh_review_01',14),('fresh_review_02',15)]:
    d=P/n; seal=readj(d/'SAFE_AUTHORED_MANIFEST.json')
    check(n+'/seal_count',len(seal['safe_authored_files'])==expected)
    for r in seal['safe_authored_files']: pin(d/r['path'],r,n+'/seal/'+r['path'])

zip_summary={}
for label,d in [('pre_M1',H),('final',P)]:
    frozen=readj(d/'FROZEN_INPUTS.json')
    for r in frozen['submission_files']: pin(d/r['path'],r,label+'/submission/'+r['path'])
    with zipfile.ZipFile(d/'output/cylinder_areas_verification.zip') as z:
        names=z.namelist(); records=frozen['archive_payload_manifest']
        check(label+'/safe_unique_names', len(names)==len(set(names)) and all(not PurePosixPath(n).is_absolute() and '..' not in PurePosixPath(n).parts and '\\' not in n for n in names))
        check(label+'/CRC',z.testzip() is None)
        check(label+'/inventory',set(names)=={r['path'] for r in records}|{'PACKAGE_FILES.json'} and len(names)==frozen['archive_members'])
        check(label+'/self_manifest_contents',readj(d/'FROZEN_INPUTS.json')['archive_payload_manifest']==json.loads(z.read('PACKAGE_FILES.json'))['files'])
        for r in records:
            b=z.read(r['path'])
            check(label+'/ZIP/'+r['path'],len(b)==r['bytes'] and sha(b)==r['sha256'])
        zip_summary[label]={'archive_members':len(names),'manifested_payloads':len(records),'names':names}
        if label=='final':
            for n in names:
                if n.startswith('current_source/'):
                    rel=n.removeprefix('current_source/')
                    check('ZIP_vs_reviewed_prepared_current/'+rel,z.read(n)==(P/'pr_update/30006020'/rel).read_bytes())
                if n.startswith('audits/root/'):
                    q=S/'existing_publication_audit/initial_review_20261015'/n.removeprefix('audits/root/')
                    check('ZIP_vs_current_root/'+q.name,z.read(n)==q.read_bytes())
            check('ZIP_source_metadata_match',z.read('cylinder_areas.tex')==(P/'cylinder_areas.tex').read_bytes() and z.read('metadata.json')==(P/'metadata.json').read_bytes())
            check('ZIP_no_full_third_party_PDF_text_HTML',not any(PurePosixPath(n).suffix.lower() in ('.pdf','.txt','.html','.htm') for n in names))
            for r in readj(P/'verification/PACKAGE_MANIFEST.json')['files']:
                check('ZIP_static_payload/'+r['path'],z.read('verification/'+r['path'])==(P/'verification'/r['path']).read_bytes())
            # Extract controlled exact bytes into this audit's directory only.
            extracted=O/'replay_package';extracted.mkdir(exist_ok=True)
            z.extractall(extracted)

f1=readj(P/'fresh_review_01/REVIEW_FINDINGS.json');f2=readj(P/'fresh_review_02/REVIEW_FINDINGS.json')
check('review01_old_three_pins',all(f1[key]==sha((H/name).read_bytes()) for key,name in [('reviewed_manuscript_sha256','cylinder_areas.tex'),('reviewed_pdf_sha256','output/pdf/cylinder_areas.pdf'),('reviewed_archive_sha256','output/cylinder_areas_verification.zip')]))
check('review01_remains_nonclean',f1['status']=='REPAIR_REQUIRED_PRECISION' and len(f1['issues'])==1 and f1['issues'][0]['id']=='M1' and not f1['provider_release_clearance'])
check('review02_final_frozen_pin',f2['frozen_input_sha256']==sha((P/'FROZEN_INPUTS.json').read_bytes()))
for r in f2['submission_files']:pin(P/r['path'],r,'review02_bound_final/'+r['path'])
for num in ['01','02']:
    r=readj(P/f'ROOT_REVIEW{num}_ACCEPTANCE.json')
    check('root_review'+num+'/report_pin',r['report_sha256']==sha((P/f'fresh_review_{num}/REPORT.md').read_bytes()))
check('root_review01_not_promoted',not readj(P/'ROOT_REVIEW01_ACCEPTANCE.json')['clean_review'] and not readj(P/'ROOT_REVIEW01_ACCEPTANCE.json')['release_cleared'])
check('root_M1_required_new_review',readj(P/'ROOT_M1_GLOBAL_REPAIR_ACCEPTANCE.json')['new_second_manuscript_review_required'] and not readj(P/'ROOT_M1_GLOBAL_REPAIR_ACCEPTANCE.json')['release_cleared'])
check('review02_no_findings',not f2['mandatory_findings'] and not f2['optional_findings'])
check('review02_claimed_input_pin_receipt',readj(P/'fresh_review_02/INPUT_PIN_RECEIPT.json')['frozen_sha256']==sha((P/'FROZEN_INPUTS.json').read_bytes()))
for n in ['PRIOR_REPAIR_VERIFICATION.json','CUSTODY_RECEIPT.json']:
    r=readj(P/'fresh_review_02'/n)
    check('review02_existing_receipt/'+n,all(x['pass'] for x in r['checks']),recorded_check_count=len(r['checks']))

# Reconstruct the substantive repair rather than accepting a pass label.
before=(H/'cylinder_areas.tex').read_text().splitlines()
after=(P/'cylinder_areas.tex').read_text().splitlines()
changes=[(tag,i,j,k,l) for tag,i,j,k,l in difflib.SequenceMatcher(None,before,after).get_opcodes() if tag!='equal']
check('M1_manuscript_only_one_paragraph_changed',changes==[('replace',64,65,64,65)],opcodes=changes)
check('M1_final_explicit_finite_event',all(t in after[64] for t in [r'Z_1,\ldots,Z_n',r'\sum_{j=1}^n jZ_j=n',r'C_j=0',r'e^{-\sum_{j=1}^n a_j}h_n>0']))
for n in ['metadata.json','deposit.json']:
    check('M1_unchanged_metadata/'+n,(P/n).read_bytes()==(H/n).read_bytes())
for d in [S/'current_attempt',S/'Main_attempt',S/'existing_publication_audit/publication/native_current_source',P/'pr_update/30006020']:
    cm=readj(d/'CURRENT_SOURCE_MANIFEST.json')
    for r in cm['current_files']:pin(d/r['path'],r,'current_manifest/'+str(d.relative_to(S))+'/'+r['path'])
    check('original22_count/'+str(d.relative_to(S)),len(cm['original_submission_files'])==22)
    for r in cm['original_submission_files']:
        pin(d/'history/original_submission_20261001'/r['path'],r,'historical_manifest/'+str(d.relative_to(S))+'/'+r['path'])
        check('actual_original22/'+str(d.relative_to(S))+'/'+r['path'],(d/'history/original_submission_20261001'/r['path']).read_bytes()==(S/'original_attempt'/r['path']).read_bytes())
    current=(d/'CANDIDATE.md').read_text();orig=(S/'original_attempt/CANDIDATE.md').read_text()
    check('core3_to9/'+str(d.relative_to(S)),current[current.index('## 3.'):current.index('## 10.')]==orig[orig.index('## 3.'):orig.index('## 10.')])
for role in ['Main_attempt','existing_publication_audit/publication/native_current_source']:
    d=S/role
    files=[p.relative_to(S/'current_attempt') for p in (S/'current_attempt').rglob('*') if p.is_file()]
    check('native_current_copy/'+role,len(files)==30 and all((S/'current_attempt'/n).read_bytes()==(d/n).read_bytes() for n in files))
for n in ['CANDIDATE.md','FINAL_DISPOSITION.md','README.md']:
    t=(S/'current_attempt'/n).read_text()
    check('M1_current_finite/'+n,'finite' in t and ('vector' in t or '1,…,n' in t))
for d,n in [(P/'verification','CLAIM_AND_EVIDENCE_MAP.md'),(S/'existing_publication_audit/initial_review_20261015','ROOT_ASSEMBLY_PRIMARY_COMPARISON.md')]:
    t=(d/n).read_text();check('M1_current_finite/'+n,all(w in t for w in ['finite','Z_1','positive probability']) if n.startswith('ROOT_') else all(w in t for w in ['finite','Z_1','h_n>0']))
# Native post-publication candidate differs only by administrative preamble before section 1.
current=(S/'current_attempt/CANDIDATE.md').read_text();prep=(P/'pr_update/30006020/CANDIDATE.md').read_text()
check('native_vs_reviewed_candidate_below_section1',current[current.index('## 1.'):]==prep[prep.index('## 1.'):])
check('native_vs_reviewed_source_audit',(S/'current_attempt/SOURCE_AUDIT.md').read_bytes()==(P/'pr_update/30006020/SOURCE_AUDIT.md').read_bytes())

# Cross-package metadata and externally observed administrative state (no network calls).
metadata=readj(P/'metadata.json');deposit=readj(P/'deposit.json');public=readj(A/'root_external_metadata_observation_02/ACTUAL_ZENODO_METADATA_STDOUT.json')
check('deposit_metadata_identical',metadata==deposit['metadata'])
check('actual_metadata_production_done',public['environment']=='production' and public['state']=='done' and public['submitted'] is True and public['doi']=='10.5281/zenodo.23387774')
check('actual_metadata_all_requested_fields_identical',all(public['metadata'].get(k)==v for k,v in metadata.items()))
for r in public['files']:
    p=P/('output/pdf/cylinder_areas.pdf' if r['name']=='cylinder_areas.pdf' else 'output/cylinder_areas_verification.zip')
    b=p.read_bytes();check('actual_metadata_file/'+r['name'],len(b)==r['size'] and hashlib.md5(b).hexdigest()==r['md5'],actual_sha256=sha(b))
receipt=readj(S/'current_attempt/PUBLICATION_RECEIPT.json')
check('native_publication_receipt_metadata',receipt['publication']['metadata']==metadata)
check('native_publication_receipt_final_clearance',readj(S/'current_attempt/FINAL_ACCEPTANCE.json')['manuscript_reviews']==readj(P/'FINAL_CLEARANCE.json'))
tracker=readj(A/'root_tracker_observation_01/ROOT_TRACKER_OBSERVATION_01.json')
raw=readj(A/'root_tracker_observation_01/PRIVATE_ACTUAL_SHEET_STDOUT.json')
rows=raw.get('values',[]);matched=[(i+1,row) for i,row in enumerate(rows) if any('10.5281/zenodo.23387774' in str(c) for c in row)]
check('tracker_exactly_one_observed_row99',len(matched)==1 and matched[0][0]==99 and matched[0][1]==receipt['tracker']['values'],matches=matched)
check('tracker_observation_matches_raw',tracker['match_count']==1 and tracker['matching_rows'][0]['cells']==matched[0][1] and tracker['matching_rows'][0]['row_index']==99)
queue=(A/'root_current_status_custody_01/PRIVATE_CURRENT_HEAD_QUEUE.md').read_text()
qlines=[(i+1,l) for i,l in enumerate(queue.splitlines()) if '30006020' in l]
check('current_queue_one_row_consistent',len(qlines)==1 and 'claimed_solved | 1/5' in qlines[0][1] and '10.5281/zenodo.23387774' in qlines[0][1],lines=qlines)

# Reproduce from exact extracted final ZIP using only its standard-library runner.
env={k:v for k,v in os.environ.items() if not k.startswith('PYTHON')}
run=subprocess.run([sys.executable,'-I',str(O/'replay_package/verification/run_checks.py'),'--receipt',str(O/'ACTUAL_EXTRACTED_REPLAY.json')],capture_output=True,text=True,env=env,timeout=120)
(O/'ACTUAL_EXTRACTED_REPLAY_STDOUT.txt').write_text(run.stdout)
(O/'ACTUAL_EXTRACTED_REPLAY_STDERR.txt').write_text(run.stderr)
check('actual_extracted_runner_returncode',run.returncode==0,returncode=run.returncode)
if (O/'ACTUAL_EXTRACTED_REPLAY.json').exists():
    replay=readj(O/'ACTUAL_EXTRACTED_REPLAY.json')
    check('actual_extracted_runner_status',replay['status']=='PASS' and replay['counted_exact_assertions_excluding_dvv']==7100 and replay['dvv_rational_composition_cases']==123 and replay['sealed_payload_files_verified']==16)

result={'schema':'pr218-independent-package-history-checks-v1','UTC':datetime.now(timezone.utc).isoformat(),'scope':'PACKAGE_AND_RECORDED_HISTORY_ONLY_NOT_THEOREM_OR_OVERALL_ACCEPTANCE','check_count':len(checks),'failed_checks':[x for x in checks if not x['pass']],'all_pass':all(x['pass'] for x in checks),'zip_summary':{k:{n:v for n,v in d.items() if n!='names'} for k,d in zip_summary.items()},'checks':checks}
(O/'PACKAGE_HISTORY_CHECKS.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
print(json.dumps({k:v for k,v in result.items() if k not in ['checks']},indent=2))
