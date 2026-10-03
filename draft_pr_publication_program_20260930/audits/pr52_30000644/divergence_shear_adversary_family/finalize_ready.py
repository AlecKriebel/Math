#!/usr/bin/env python3
"""Private preparer creates SOURCE handoff; never invokes ROOT close/read."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,stat,os

HERE=Path(__file__).resolve().parent
ORIGINAL=HERE.parent/'original_preparation_family'
def sha(b):return hashlib.sha256(b).hexdigest()
def utc():return datetime.now(timezone.utc).isoformat()
def row(p,relative=False,mode=None):
    b=p.read_bytes()
    return {'path':p.relative_to(HERE).as_posix() if relative else str(p),
            'bytes':len(b),'sha256':sha(b),
            'mode':mode or format(stat.S_IMODE(p.stat().st_mode),'04o')}
def put(name,v):
    (HERE/name).write_text(json.dumps(v,indent=2,sort_keys=True)+'\n')
assert not (HERE/'SELF_MANIFEST.json').exists()
assert not (HERE/'READY.json').exists()
auth=json.loads((ORIGINAL/'ORIGINAL_AUTHENTICATION.json').read_bytes())
assert auth['head']=='d40d2dae4cff2a5e5a1e12e9a2f8bc3987431c1a'
blob_rows=[]
paths=[]
for item in auth['primary_science_files']:
    p=Path(item['local_identity']['path'])
    body=p.read_bytes()
    got=hashlib.sha1(b'blob '+str(len(body)).encode()+b'\0'+body).hexdigest()
    assert got==item['git_blob_sha1']
    assert sha(body)==item['local_identity']['sha256']
    assert len(body)==item['local_identity']['bytes']
    paths.append(p)
    blob_rows.append({'path':str(p),'repository_path':item['repository_path'],
                      'git_blob_sha1':got,'git_mode':item['git_mode'],
                      'retrieval_recorded_mode_is_dated':item['local_identity']['mode']})
assert len(paths)==19
paths += [ORIGINAL/'ORIGINAL_AUTHENTICATION.json',ORIGINAL/'PRIMARY_SOURCE_SCOPE.md',
          ORIGINAL/'SOURCE_PRECISION_QUALIFICATIONS.md',ORIGINAL/'SELECTED_LITERAL_SOURCE.json',
          ORIGINAL/'primary_selected/owr2007-decisive-page.png',
          ORIGINAL/'primary_selected/acta-open-problems2007-decisive-page.png']
put('REFERENCE_BINDINGS.json',{'schema':'pr52-divergence-shear-full-references-v1',
    'utc':utc(),'original_head':auth['head'],'files':[row(p) for p in sorted(paths)],
    'original_git_blobs':sorted(blob_rows,key=lambda x:x['path']),
    'scope':'All bodies authenticated and read as bytes; this does not assign new mathematical authority to every historical checker or receipt.',
    'original_body_modes_dated':True,'ROOT_approval':False})
put('SOURCE_OBSERVATIONS.json',{'schema':'pr52-divergence-shear-primary-observations-v1',
    'utc_recorded':utc(),'fresh_web_primary_read':True,
    'primary_urls':['https://ems.press/content/serial-article-files/46087?nt=1',
                    'https://math.ac.vn/public/uploads/files/0702303.pdf'],
    'personally_viewed_selected_images':[
        {**row(ORIGINAL/'primary_selected/owr2007-decisive-page.png'),
         'printed_page':26,'observation':'Exact question, determinant-one definition, immediate affirmative credited answer; displayed sketch m=2,n=2.'},
        {**row(ORIGINAL/'primary_selected/acta-open-problems2007-decisive-page.png'),
         'printed_page':317,'observation':'Any ring containing Q; literal m,n >=1 and excluded other-ring cases. Web extraction misreads >= glyph.'}],
    'full_JPAA_article_personally_read':False,
    'whole_PDF_download_by_this_family':False,
    'credit_doi':'10.1016/j.jpaa.2006.09.013','recommended_status':'already_solved',
    'no_external_human_communication':True})
main=json.loads((HERE/'private_capture/CAPTURE.json').read_bytes())
edge=json.loads((HERE/'edge_capture/CAPTURE.json').read_bytes())
assert main['exit_code']==edge['exit_code']==0
assert (HERE/'private_capture/stderr.bin').read_bytes()==b''
assert (HERE/'edge_capture/stderr.bin').read_bytes()==b''
assert json.loads((HERE/'private_capture/stdout.bin').read_bytes())==json.loads((HERE/'RESULTS.json').read_bytes())
assert json.loads((HERE/'edge_capture/stdout.bin').read_bytes())==json.loads((HERE/'EDGE_RESULTS.json').read_bytes())
put('VERDICT.json',{'schema':'pr52-independent-divergence-shear-verdict-v1',
 'utc':utc(),'verdict':'PASS_EXACT_CREDITED_Q_ALGEBRA_THEOREM',
 'problem_id':30000644,'problem_number':'OWR-1452-008',
 'original_head':auth['head'],'recommended_status':'already_solved',
 'mandatory_mathematical_corrections':[],
 'unresolved_gap_within_exact_claim':None,'novelty':False,
 'claim':'Surjectivity for arbitrary commutative unital Q-algebras and all m,n >=1, from existing determinant-one polynomial automorphisms.',
 'proof':row(HERE/'INDEPENDENT_PROOF.md',True,'0444'),
 'report':row(HERE/'REPORT.md',True,'0444'),
 'independent_check_counts':[6672,9],'total_new_finite_assertions':6681,
 'actual_private_child_pids':[main['child_pid'],edge['child_pid']],
 'historical_checker_imported_or_rerun':False,
 'full_journal_proof_personally_read':False,'formal_proof_certification':False,
 'human_peer_review':False,'ROOT_approval':False,'native_acceptance':False,
 'paper_required_under_user_process':False,'Zenodo_publication_performed':False,
 'provenance_qualification':'Raw prior key absent; SQL non-NULL text {}; original prior_report JSON null. Existing operative qualification retained.',
 'accounting':'Zero substantive fresh search attempts, original 0/5; one credited known-theorem validation activity, no new original response count.'})
with (HERE/'RESEARCH_LOG.md').open('a') as f:
    f.write('\n- '+utc()+' — 100% complete toward this independent mathematical audit and SOURCE handoff. '
            'Universal all-ring reconstruction has no identified gap. Two real private runs pass 6,681 total exact assertions; '
            'complete streams were read. Both decisive source images were personally inspected, and the already_solved scope confirmed. '
            'Historical review was consulted only after the main independent derivation/checks. '
            'ROOT closure/readback and PR acceptance remain unperformed. No campaign discovery credit, native/Git/remote change, paper, DOI or human outreach.\n')
exclude={'INDEX.json','READY.json','SELF_MANIFEST.json'}
files=[p for p in sorted(HERE.rglob('*')) if p.is_file() and p.name not in exclude]
dirs=[HERE]+sorted(p for p in HERE.rglob('*') if p.is_dir())
put('INDEX.json',{'schema':'pr52-divergence-shear-source-index-v1','utc':utc(),
                 'files':[row(p,True,'0444') for p in files],
                 'directories':[{'path':'.' if p==HERE else p.relative_to(HERE).as_posix(),
                                 'mode':'0555'} for p in dirs],
                 'excludes':['INDEX.json','READY.json','SELF_MANIFEST.json'],
                 'scope':'Entire source-ready payload is listed; index and ready are bound by ROOT closure without circular self hashing.'})
put('READY.json',{'schema':'pr52-divergence-shear-source-ready-v1','utc':utc(),
                 'status':'SOURCE_READY_FOR_ROOT_CLOSURE','family':str(HERE),
                 'index':row(HERE/'INDEX.json',True,'0444'),
                 'payload_files_including_index_and_ready':len(files)+2,
                 'self_manifest_absent_at_source_ready':True,
                 'ROOT_execution_performed':False,'native_acceptance':False,
                 'recommended_status':'already_solved','new_assertions':6681,
                 'ROOT_steps':['Read all report/proof/code/full captures and closure source.',
                               'After preparer exit, execute close_family.py with actual external capture.',
                               'Separately execute read_closed_family.py with actual external capture.']})
for p in HERE.rglob('*'):
    if p.is_file():os.chmod(p,0o444)
for p in sorted(dirs,key=lambda p:len(p.parts),reverse=True):os.chmod(p,0o555)
from closure_common import inspect
inspection=inspect(False)
print(json.dumps({'status':'SOURCE_READY','ready':row(HERE/'READY.json',True),
                  'inspection':inspection,'ROOT_close_read_not_executed':True},indent=2,sort_keys=True))
