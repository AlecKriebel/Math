"""Preserve the first candidate, repair authoring source in its native editor path,
and assemble revised supporting files. This is not publication authority.
"""
import datetime,difflib,hashlib,json,os,stat,zipfile
from pathlib import Path

R=Path('/Users/alec/Documents/Math');A=Path(__file__).resolve().parent
OLD=A/'preprint_package_v01';NEW=A/'preprint_package_v02'
ARCHIVE=A/'frozen_first_preprint_candidate'
PAYLOAD=['spectral_tensor_consistency.tex','README.md','SOURCE_EDITIONS.md','LICENSE.txt',
         'classical_regularization_application.md','independent_classical_derivation.md',
         'verify_package.py','CONTROL_CASES.json','EXPECTED_SCIENTIFIC_OUTPUTS.json',
         'record_metadata.json','PAYLOAD_PROVENANCE.json',
         'controls/author_turn1.py','controls/author_turn2.py',
         'controls/historical_independent.py','controls/empirical.py',
         'controls/spectral.py','controls/scope.py','controls/mechanism.py','controls/auxiliary.py']
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def sha(b):return hashlib.sha256(b).hexdigest()
def require(ok,m):
    if not ok:raise RuntimeError(m)
def pin(p):
    require(p.is_file() and not p.is_symlink(),'Regular file required')
    b=p.read_bytes();return {'path':str(p),'bytes':len(b),'sha256':sha(b),'mode':stat.S_IMODE(p.stat().st_mode)}
def load(p):return json.loads(p.read_bytes())
def write(p,x):
    with p.open('x') as f:f.write(json.dumps(x,indent=2,ensure_ascii=False)+'\n')
def replace_once(body,old,new):
    require(body.count(old)==1,'Exact repair target not unique');return body.replace(old,new,1)
def main():
    require(not __import__('sys').flags.optimize,'Optimization forbidden')
    gate=load(A/'ROOT_FIRST_PREPRINT_REVIEW_ADJUDICATION.json')
    require(gate['status']=='PASS_FIRST_WHOLE_PACKAGE_REVIEW_FOR_LISTED_GLOBAL_REPAIRS'
            and gate['ROOT_accepts_mathematics'] is True
            and gate['publication_clearance'] is False,'Actual first-review adjudication required')
    first_pin=pin(OLD/'FIRST_CANDIDATE_MANIFEST.json')
    require(first_pin['sha256']=='522fc23022c2975a0d43b66796bc2fa58d95eb4a59b892b835ea034ef78f5a73','First candidate manifest changed')
    candidate=load(OLD/'FIRST_CANDIDATE_MANIFEST.json');rows=candidate['files']
    require(len(rows)==23 and len({x['path'] for x in rows})==23,'First candidate literal scope differs')
    for row in rows:require(pin(Path(row['path']))==row,'First candidate input changed before archive')
    ARCHIVE.mkdir(exist_ok=False);archived=[]
    for row in rows:
        original=Path(row['path']);rel=original.relative_to(OLD);p=ARCHIVE/rel
        p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(original.read_bytes());p.chmod(row['mode'])
        copied=pin(p);require(all(copied[k]==row[k] for k in ('bytes','sha256','mode')),'First candidate archive differs')
        archived.append({'actual_original_input':row,'actual_byte_identical_archive':copied})
    (ARCHIVE/'FIRST_CANDIDATE_MANIFEST.json').write_bytes((OLD/'FIRST_CANDIDATE_MANIFEST.json').read_bytes())
    (ARCHIVE/'FIRST_CANDIDATE_MANIFEST.json').chmod(0o444)
    write(ARCHIVE/'ARCHIVE_MANIFEST.json',{'UTC':now(),'actual_PID':os.getpid(),'status':'FULL_LITERAL_FIRST_CANDIDATE_ARCHIVED_BEFORE_AUTHORING_REPAIR','original_manifest':first_pin,'actual_archived_manifest':pin(ARCHIVE/'FIRST_CANDIDATE_MANIFEST.json'),'literal_public_file_count':23,'files':archived,'noncircular_exclusion':['This archive manifest'],'reason':'Keep follow-up LaTeX edits in the same native editor file while preserving the whole actual first candidate independently and without retroactive path/body claims.'})
    (ARCHIVE/'ARCHIVE_MANIFEST.json').chmod(0o444)
    for p in sorted([x for x in ARCHIVE.rglob('*') if x.is_dir()],key=lambda x:len(x.parts),reverse=True):p.chmod(0o555)
    ARCHIVE.chmod(0o555)
    NEW.mkdir(exist_ok=False);(NEW/'controls').mkdir()
    for rel in PAYLOAD:
        if rel=='PAYLOAD_PROVENANCE.json':continue
        (NEW/rel).write_bytes((OLD/rel).read_bytes())
    author=OLD/'spectral_tensor_consistency.tex';old_author=pin(author)
    old_tex=author.read_text()
    anchor='\\end{proof}\n\nFor $N\\geq2$'
    paragraph=('\\end{proof}\n\n'
               'Set $K_h(x,z)=0$ for $z\\in\\partial D$. This is a Borel convention\n'
               'for every sample in $\\overline D$; under stationarity,\n'
               '$\\Prob(Y_i\\in\\partial D)=0$ for every $i$, so it changes no\n'
               'almost-sure conclusion.\n\nFor $N\\geq2$')
    new_tex=replace_once(old_tex,anchor,paragraph)
    author.chmod(0o644);author.write_text(new_tex)
    require(author.read_text()==new_tex,'Authoring source readback differs')
    (NEW/'spectral_tensor_consistency.tex').write_bytes(author.read_bytes())
    doc=NEW/'independent_classical_derivation.md';body=doc.read_text()
    body=replace_once(body,'The claim frozen in `CRITERIA.md` survives the attacks below.',
                      'The alternative consistency conclusion stated in the bundled classical_regularization_application.md survives the attacks below.')
    body=replace_once(body,'Choose 0<eta<s-d/2-2.','Choose 0<eta<min{1,s-d/2-2}.')
    doc.write_text(body)
    doc=NEW/'classical_regularization_application.md';body=doc.read_text()
    full_citation=('Bruce E. Hansen, "Uniform convergence rates for kernel estimation with dependent data," '
                   'Econometric Theory24(2008),726–748, DOI10.1017/S0266466608080304 '
                   '([author-hosted published paper](https://users.ssc.wisc.edu/~behansen/papers/et_08.pdf)), Theorem3')
    body=replace_once(body,'Bruce Hansen(2008), Theorem3',full_citation);doc.write_text(body)
    doc=NEW/'SOURCE_EDITIONS.md';body=doc.read_text()
    anchor='\n\nThe two independent priority families also investigated'
    row=('\n| Bruce E. Hansen, "Uniform convergence rates for kernel estimation with dependent data," '
         'Econometric Theory24(2008),726–748, DOI10.1017/S0266466608080304, '
         '[full author-hosted published paper](https://users.ssc.wisc.edu/~behansen/papers/et_08.pdf) '
         '| Assumptions1–3 and Theorem3 provide centered strong uniform kernel-average convergence '
         'for stationary mixing multivariate data with overlapping lag vectors. The supplementary '
         'application verifies the pair-density conditions at separated lags and handles the '
         'zero-extension boundary bias directly; this source does not prove tensor inversion or '
         'the main empirical spectral objective. |\n\nThe two independent priority families also investigated')
    body=replace_once(body,anchor,row);doc.write_text(body)
    doc=NEW/'README.md';body=doc.read_text()
    body=replace_once(body,'## License and candidate status','## License')
    body=replace_once(body,'This first package is being prepared for sequential fresh adversarial whole-package reviews. It is not a publication/merge clearance. The status statement will be updated after those reviews; the manuscript\'s unrefereed human-review status will remain explicit.',
                      'The manuscript and verification materials retain their explicit unrefereed status. Internal AI verification does not constitute human peer review or a formal theorem certificate.')
    doc.write_text(body)
    provenance=load(OLD/'PAYLOAD_PROVENANCE.json');provenance['UTC']=now();provenance['actual_preparer_PID']=os.getpid()
    provenance['first_candidate_archive']=pin(ARCHIVE/'ARCHIVE_MANIFEST.json')
    for entry in provenance['payload_sources']:
        if entry['package_path'] not in ('classical_regularization_application.md','independent_classical_derivation.md'):continue
        original=(R/entry['original_source']).read_text();public=(NEW/entry['package_path']).read_text()
        require(sha(original.encode())==entry['original_sha256'],'Frozen original proof source changed')
        entry['public_bytes']=len(public.encode());entry['public_sha256']=sha(public.encode())
        entry['wording_diff']=''.join(difflib.unified_diff(original.splitlines(keepends=True),public.splitlines(keepends=True),fromfile=entry['original_source'],tofile=entry['package_path']))
        if entry['package_path']=='independent_classical_derivation.md':
            entry.pop('mathematical_content_unchanged',None)
            entry['mathematical_conclusion_unchanged']=True
            entry['proof_precision_clarification']='The conventional Holder exponent range 0<eta<1 is explicit; the strict Sobolev assumption already provides such an exponent.'
    write(NEW/'PAYLOAD_PROVENANCE.json',provenance)
    rows=[{'path':rel,'bytes':(NEW/rel).stat().st_size,'sha256':sha((NEW/rel).read_bytes()),'ZIP_mode':0o100644} for rel in sorted(PAYLOAD)]
    write(NEW/'MANIFEST.json',{'schema':'spectral-tensor-supplement/v1','payload':rows,'exclusions':load(OLD/'MANIFEST.json')['exclusions'],'finite_controls_not_theorem_certificate':True})
    with zipfile.ZipFile(NEW/'spectral_tensor_verification.zip','x',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for rel in sorted(PAYLOAD+['MANIFEST.json']):
            info=zipfile.ZipInfo('spectral-tensor-consistency/'+rel,date_time=(2026,10,5,0,0,0));info.create_system=3;info.external_attr=0o100644<<16;info.compress_type=zipfile.ZIP_DEFLATED
            z.writestr(info,(NEW/rel).read_bytes(),compress_type=zipfile.ZIP_DEFLATED,compresslevel=9)
    with zipfile.ZipFile(NEW/'spectral_tensor_verification.zip') as z:
        require(len(z.infolist())==20 and z.testzip() is None,'Revised ZIP invalid')
        for rel in PAYLOAD+['MANIFEST.json']:require(z.read('spectral-tensor-consistency/'+rel)==(NEW/rel).read_bytes(),'Revised ZIP body differs')
    write(NEW/'zenodo-deposit.json',{'metadata':load(NEW/'record_metadata.json'),'files':[{'path':'spectral_tensor_consistency.pdf'},{'path':'spectral_tensor_verification.zip'}]})
    require((NEW/'record_metadata.json').read_bytes()==(OLD/'record_metadata.json').read_bytes(),'Intended metadata changed')
    current_author=pin(author)
    reconciliation={'UTC':now(),'actual_PID':os.getpid(),'authoring_path_kept_in_same_native_editor':str(author),'old_first_candidate_author':old_author,'actual_full_original_archive':pin(ARCHIVE/'ARCHIVE_MANIFEST.json'),'current_authoring_source':current_author,'new_candidate_source':pin(NEW/'spectral_tensor_consistency.tex'),'original_PR_snapshot_and_first_PDF_ZIP_unchanged':True,'qualification':'The old first-candidate manifest is a historical epoch. Its one authoring .tex path now contains the repaired source, explicitly reconciled with the complete byte-identical archived first candidate. No unchanged-current-body claim is made for that authoring path.','exact_TeX_diff':''.join(difflib.unified_diff(old_tex.splitlines(keepends=True),new_tex.splitlines(keepends=True),fromfile='first-candidate.tex',tofile='repaired-authoring-source.tex'))}
    write(OLD/'AUTHORING_PATH_RECONCILIATION_02.json',reconciliation)
    write(NEW/'GLOBAL_REPAIR_RECEIPT.json',{'UTC':now(),'actual_PID':os.getpid(),'status':'REVISED_SUPPORTING_PACKAGE_ASSEMBLED_PENDING_NATIVE_COMPILE_EXPORT_REPLAY_SECOND_REVIEW','first_review_adjudication':pin(A/'ROOT_FIRST_PREPRINT_REVIEW_ADJUDICATION.json'),'first_candidate_full_archive':pin(ARCHIVE/'ARCHIVE_MANIFEST.json'),'authoring_path_reconciliation':pin(OLD/'AUTHORING_PATH_RECONCILIATION_02.json'),'repairs':['Borel zero extension of sample kernel on boundary; stationary probability-zero convention explicit','Unbundled CRITERIA reference replaced with bundled exact conclusion','Explicit conventional Holder exponent range','Full Hansen2008 citation and source-edition credit','Preparation-only README status replaced by truthful permanent unrefereed review disclosure'],'unchanged_metadata':True,'unchanged_all8_control_sources_and_expected_scientific_outputs':True,'publication_clearance':False,'recorder_source':pin(Path(__file__).resolve()),'estimates_percent':{'math':100,'bounded_priority':100,'publication_workflow':55}})
    (NEW/'RESEARCH_LOG.md').write_text('# PR302 revised preprint package\n\n'+now()+'. Four reviewer/ROOT precision and presentation cleanups are applied globally in a new complete supplement. The entire actual first candidate is preserved before reusing the native editor authoring path. The almost-sure theorem, eight control bodies and exact metadata are unchanged; the conventional Holder range and boundary-data definition are now explicit. Compile/export/all-page visual QA, revised archive replay and the second fresh whole-package review remain. Checkpoint estimate: math100%; bounded priority100%; publication workflow55%. No publication, tracker, Git/index, native integration or writer authority is asserted.\n')
    print(json.dumps({'status':'REVISED_PACKAGE_PREPARED_NOT_PUBLISHED','actual_PID':os.getpid(),'new_package':str(NEW),'new_source':pin(NEW/'spectral_tensor_consistency.tex'),'new_ZIP':pin(NEW/'spectral_tensor_verification.zip')},indent=2))
if __name__=='__main__':main()
