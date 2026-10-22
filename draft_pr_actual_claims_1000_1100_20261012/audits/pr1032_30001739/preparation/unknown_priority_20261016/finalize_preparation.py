#!/usr/bin/env python3
"""Freeze only this new preparation after checkable local QA; no services or Git."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import importlib.util
import io
import json
import stat
import subprocess
import sys
import warnings
import zipfile

P = Path(__file__).resolve().parent
B = P.parents[1]
O = B/'preprint_v1_0'
K = O/'kit'
REPO = B.parents[2]

def h(d): return hashlib.sha256(d).hexdigest()
def row(f,root):
    d=f.read_bytes()
    return {'path':f.relative_to(root).as_posix(),'bytes':len(d),'sha256':h(d)}
def put(f,x): f.write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n')
def load_module(name,path):
    spec=importlib.util.spec_from_file_location(name,path)
    module=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module
def require(c,m):
    if not c: raise RuntimeError(m)

def main():
    require(not (O/'PREPARATION_SEAL.json').exists() and not (P/'PREPARATION_SEAL.json').exists(),'output already sealed')
    now=datetime.now(timezone.utc).isoformat()
    # Same final PDF/source bytes, viewed in all nine raster pages before this command.
    require((O/'paper.pdf').read_bytes()==(K/'paper.pdf').read_bytes(),'PDF copy')
    require((O/'paper.tex').read_bytes()==(K/'paper.tex').read_bytes(),'source copy')
    names=sorted([p.relative_to(K).as_posix() for p in K.rglob('*') if p.is_file()]+['ALLOWLIST.json','MANIFEST.json'])
    require(len(names)==len(set(names)),'unexpected existing inventories')
    put(K/'ALLOWLIST.json',{'schema':1,'files':names,'selection_policy':'Explicit authored-only list. No raw third-party source material, fixtures, recursively copied audit tree, or nested archives.'})
    members=[row(K/name,K) for name in names if name!='MANIFEST.json']
    put(K/'MANIFEST.json',{'schema':1,'algorithm':'sha256','self_hash_excluded':True,'files':members,
        'scope':'content identities and exact allowlist; not a digital signature, theorem proof, or exhaustive original audit archive'})
    archive=O/'pr1032_supportkit_v1.0.zip'
    builder=load_module('archive_build',K/'scripts/build_archive.py')
    builder.build(K,archive)
    second=P/'deterministic_rebuild.zip'
    builder.build(K,second)
    require(archive.read_bytes()==second.read_bytes(),'archive deterministic rebuild')
    verifier=load_module('verify_prepared',K/'scripts/verify_kit.py')
    runs=[]
    for flags in ([],['-O'],['-OO']):
        cmd=[sys.executable,'-I','-B',*flags,str(K/'scripts/verify_kit.py'),'--archive',str(archive)]
        proc=subprocess.run(cmd,capture_output=True,timeout=60)
        require(proc.returncode==0 and not proc.stderr,'whole verifier failed '+repr(proc.stderr))
        result=json.loads(proc.stdout)
        runs.append({'utc':datetime.now(timezone.utc).isoformat(),'command':cmd,'exit':proc.returncode,'stdout_bytes':len(proc.stdout),'stdout_sha256':h(proc.stdout),'stderr_bytes':len(proc.stderr),'result':result})
    put(P/'WHOLE_KIT_RUNS.json',runs)
    # Hostile ZIP variants are created only in memory; no original or released file is touched.
    with zipfile.ZipFile(archive) as z:
        baseline=[(i.filename,z.read(i),i.external_attr) for i in z.infolist()]
    def fixture(items):
        output=io.BytesIO()
        with warnings.catch_warnings():
            warnings.simplefilter('ignore',UserWarning)
            with zipfile.ZipFile(output,'w') as z:
                for name,data,attrs in items:
                    i=zipfile.ZipInfo(name,(2026,10,16,0,0,0));i.create_system=3
                    i.external_attr=attrs;i.compress_type=zipfile.ZIP_STORED
                    z.writestr(i,data)
        output.seek(0);return output
    mutate={
      'changed_pdf_bytes':[(n,(d+b'x') if n=='paper.pdf' else d,a) for n,d,a in baseline],
      'missing_paper':[r for r in baseline if r[0]!='paper.tex'],
      'unlisted_extra':baseline+[('extra.txt',b'x',(stat.S_IFREG|0o644)<<16)],
      'traversal_member':baseline+[('../escape.txt',b'x',(stat.S_IFREG|0o644)<<16)],
      'duplicate_member':baseline+[baseline[0]],
      'symlink_member':[(n,d,(stat.S_IFLNK|0o777)<<16 if n=='paper.pdf' else a) for n,d,a in baseline]}
    controls=[]
    for name,items in mutate.items():
        try:
            verifier.validate_archive(fixture(items))
        except RuntimeError as exc:
            controls.append({'fixture':name,'rejected':True,'reason':str(exc)})
        else:raise RuntimeError('hostile ZIP accepted: '+name)
    put(P/'ARCHIVE_NEGATIVE_CONTROLS.json',controls)
    native=B/'publication/zenodo-deposit.json'
    upload=load_module('native_zenodo_readonly',REPO/'zenodo_deposit_tool/zenodo.py')
    m1,f1=upload.load_manifest(native)
    m2,f2=upload.load_manifest(O/'zenodo-deposit.json')
    require(m1==m2==json.loads((O/'.zenodo.json').read_text())==json.loads((K/'.zenodo.json').read_text()),'bibliographic metadata mismatch')
    ident=lambda files:[{'name':f['name'],'path':str(f['path']),'bytes':f['size'],'sha256':f['sha256']} for f in files]
    require(ident(f1)==ident(f2),'native manifest resolves different released objects')
    require('doi' not in m1 and 'prereserve_doi' not in m1,'invented DOI')
    put(P/'NATIVE_METADATA_READONLY_CHECK.json',{'utc':datetime.now(timezone.utc).isoformat(),'native_load_manifest':'PASS; imported parser only, no service/secret/state operations','metadata_equal':True,'same_exact_bibliographic_objects_and_files':True,'files':ident(f1)})
    binding={'schema':1,'publication_ready':False,'metadata_sha256':h((O/'.zenodo.json').read_bytes()),
             'native_metadata':row(native,B),'files':[row(O/'paper.pdf',O),row(archive,O)],
             'note':'Both native repository and preprint deposit manifests parse with the native uploader and resolve to these identical files; no external deposit or DOI exists by this check.'}
    put(O/'DEPOSIT_BINDING.json',binding)
    original=json.loads((P/'ORIGINAL_INPUT_PINS.json').read_text())
    for r in original['files']:
        require(row(B/r['path'],B)==r,'ORIGINAL INPUT DRIFT: '+r['path'])
    known={r['path'] for r in original['files']}
    later=[row(p,B) for p in sorted(B.rglob('*')) if p.is_file() and not p.is_relative_to(P) and not p.is_relative_to(O) and p.relative_to(B).as_posix() not in known]
    require({r['path'] for r in later}<={'ROOT_UNKNOWN_PRIORITY_USER_DIRECTION_20261016.json','publication/zenodo-deposit.json'},'unexpected outside addition')
    put(P/'ORIGINAL_INPUT_RECHECK.json',{'utc':datetime.now(timezone.utc).isoformat(),'status':'PASS','unchanged_original_files':len(known),'original_bytes':sum(r['bytes'] for r in original['files']),'authorized_later_additions':later,'deleted_or_changed_originals':[]})
    render=[row(p,P) for p in sorted((P/'renders').glob('page-*.png'))]
    require(len(render)==9,'PDF page count')
    log=(P/'paper.log').read_text()
    require('Overfull' not in log and 'undefined' not in log.lower(),'PDF overflow or unresolved reference')
    put(P/'PDF_QA.json',{'utc':datetime.now(timezone.utc).isoformat(),'paper':row(O/'paper.pdf',O),'pages':9,'engine':'Tectonic 0.16.9','compile_exit':0,'overfull_boxes':0,'undefined_references':0,'remaining_warning':'one Underfull hbox in LM reference; visually acceptable line spacing',
        'actual_visual_inspection':'All nine final 1200px raster pages were individually opened with view_image and inspected before sealing. No clipping, overlap, missing glyphs, unreadable equations or tables, or page-number defects found.','renders':render})
    with (P/'RESEARCH_LOG.md').open('a') as stream:
        stream.write(f'\n- {now}: Paper assembled from all original proof/audit reports, fresh analytic and Langlands reports/derivations, root deductions and priority source comparisons. No third-party full bodies newly inspected. Hand-entered Hall Y lists initially differed from full graphs; corrected before packaging, then actual fifteen-row TeX table checked under normal/-O/-OO. Preparation 70%; readiness false.\n')
        stream.write(f'- {now}: Final nine-page PDF compiled and all nine pages actually viewed. Initial overfull prose line corrected; one harmless underfull reference remains. Initial helper searches using unmatched zsh globs exited1 and a broad file search reported a pre-existing missing path elsewhere; neither supplied mathematical evidence. All mathematical and final build/kit/metadata checks succeeded. Preparation 90%; readiness false.\n')
        stream.write(f'- {datetime.now(timezone.utc).isoformat()}: All287original files rechecked byte-exact; authorized later root user-direction record and newly absent-before native manifest separately inventoried. Fifteen direct finite runs and three whole-verifier modes (45 additional finite executions) pass; six hostile ZIP variants rejected; deterministic archive rebuilt byte-for-byte; native uploader parser resolves identical metadata and release files without network. Preparation100%; research mathematical baseline accepted in scoped conditional sense, historical priority/overlap UNKNOWN; publication readinessfalse pending root adoption and minimumTWO fresh independent COMPLETE whole-paper/package adversarial reviews. No Git/index/branch/QUEUE/PR/service action, outreach, further agents, or deletion of pre-existing artifacts. Final outputs are frozen by the following seals.\n')
    shutil_log=(P/'RESEARCH_LOG.md').read_text()
    (O/'RESEARCH_LOG.md').write_text(shutil_log)
    summary={'utc':datetime.now(timezone.utc).isoformat(),'preparation_completion_percent':100,'publication_ready':False,
      'head_oid':original['head_oid'],'original_files_unchanged':len(known),'original_bytes':sum(r['bytes'] for r in original['files']),
      'paper':row(O/'paper.pdf',O),'paper_pages':9,'archive':row(archive,O),'archive_members':len(names),
      'selected_historical_authored_records':13,'byte_exact_checkers':3,'finite_programs':5,'direct_finite_runs':15,
      'whole_verifier_modes':3,'additional_finite_executions':45,'hostile_zip_rejections':len(controls),
      'deterministic_archive_rebuild':True,'native_metadata_parser_same_objects':True,
      'priority_Luo_Zha':'UNKNOWN','new_primary_source_body_inspection':False,
      'pending':['root adoption of exact sealed outputs','minimum TWO fresh independent COMPLETE whole-paper-and-package adversarial reviews; preparation is not a review','resolution of every actionable issue before promotion; later repairs use new revision, preserve seals'],
      'excluded_claims':['first or worldwide novel','source Luo-Zha inspected or irrelevant','general kernel-generation disproof','finite code computes Hom','historical environmental harness replay','formal proof assistant or human peer review','actual publication/deposit/DOI']}
    put(P/'FINAL_PREPARATION_REPORT.json',summary)
    report=f'''# PR1032 / problem30001739 preparation report

Prepared a complete attributed nine-page mathematical note and lean verification kit at accepted head `{original['head_oid']}`. Exact field: F=Q3, E/F unramified quadratic; quotient of D_E[4,6] x D_E[2,5] x D_E[3,3] x D_E[1,4] x D_E[0,2], degree15. The written proof establishes tau invariance, noninduction as an entire object, and zero periods for every Hermitian stabilizer using the explicit published FLO/JPSS/LM interfaces. It distinguishes the reducible standard module from its quotient and states the exact historical OWR k=1, FLO6.12 and unrestricted local unitary Jacquet consequences.

The source credit section names all material antecedents (FLO, JPSS, LM, GMM, MOS, BP, Lu-Matringe, Matringe-Offen[-Yang], Sharma) and Luo-Zha's documented kernel-generation claim. All exact/transformed parameter, mechanism and period-consequence overlap with Luo-Zha DOI10.1007/s11464-025-0256-0 is UNKNOWN. The full body was not inspected. No novelty/first/current-open claim or separate kernel-generation disproof is made. The human policy is to leave this unknown and proceed; historical pending-priority records are retained unchanged as dated history, superseded only as workflow. This preparation newly read the authored mathematical/source-comparison records, not the third-party source bodies.

Deliverables: `paper.tex`, `paper.pdf`, `pr1032_supportkit_v1.0.zip`, `kit/`, `.zenodo.json`, `CITATION.bib`, `zenodo-deposit.json`, `DEPOSIT_BINDING.json`, `STATUS.json`, and this report. Native `publication/zenodo-deposit.json` was absent and was newly written with the same bibliographic metadata and exact same PDF/archive objects; the repository's native parser was run read-only. No DOI, external service mutation or deposit is asserted.

The archive has {len(names)} explicit allowlisted members, including13historical authored reports/models/root records and3byte-exact stdlib diagnostic copies. SOURCE_CREDITS/COPY_MAP/OMISSIONS provide semantic scope, identities and precise omissions. It excludes raw source bodies/extracts/images/API responses, runtime fixtures, archives and recursive audit custody. All287original files ({sum(r['bytes'] for r in original['files'])}bytes) were preserved byte-exact and rechecked. Later authorized root direction and newly written native metadata are separately accounted for.

Verification:15direct finite runs (5programs x normal/-O/-OO), then3whole-verifier modes with45further finite executions; full deterministic output identities agree. Scalar checks cover40germs,30order conditions and exact units; noninduction checks all15partitions in both directions, Hall vs injection decisions, positive calibration and6hostile graph mutations; the actual paper Hall table is also checked. Six hostile ZIP variants are rejected. Archive rebuild is byte-identical. These checks are finite corroboration, not Hom computations, source-theorem reproving, historical fixture replay or priority evidence.

PDF:9pages, compiled with Tectonic, every final rendered page actually viewed individually. No overflow or undefined references; one underfull bibliography line has acceptable spacing. Initial hand-transcribed auxiliary Y lists and overfull prose were corrected before final checks. Nonblocking helper-search failures are recorded honestly in the research log. Original sealed files, archives and source evidence were never rewritten or deleted. No Git/index/branch/QUEUE/PR/service action, outreach or further subagents occurred.

Extensive AI use, unrefereed status, absence of external human peer review, author ORCID0009-0001-9320-500X, and CC BY4.0 authored-content license are disclosed throughout. Preparation is100%complete. **Publication readiness is FALSE** until root adoption and minimumTWO fresh independent COMPLETE whole-paper/package adversarial reviews. This preparation is not one of those reviews. Any later correction must preserve these sealed bytes and use a new revision.

Paper SHA256 `{summary['paper']['sha256']}`, {summary['paper']['bytes']}bytes.
Archive SHA256 `{summary['archive']['sha256']}`, {summary['archive']['bytes']}bytes.
Detailed local receipts live under `preparation/unknown_priority_20261016/`; final seal inventories identify this exact state.
'''
    (O/'PREPARATION_REPORT.md').write_text(report)
    # No further writes to the preprint after this seal.
    preprint_rows=[row(p,O) for p in sorted(O.rglob('*')) if p.is_file()]
    put(O/'PREPARATION_SEAL.json',{'schema':1,'utc':datetime.now(timezone.utc).isoformat(),'scope':'all new preprint files, excluding this self-referential seal only; plus native manifest identity','files':preprint_rows,'native_manifest':row(native,B),'publication_ready':False,'pending':summary['pending']})
    # No further writes to the preparation directory after this seal.
    prep_rows=[row(p,P) for p in sorted(P.rglob('*')) if p.is_file()]
    put(P/'PREPARATION_SEAL.json',{'schema':1,'utc':datetime.now(timezone.utc).isoformat(),'scope':'all owned preparation files, excluding this seal; preprint seal externally pinned','files':prep_rows,'preprint_seal':row(O/'PREPARATION_SEAL.json',O),'publication_ready':False})
    print(json.dumps(summary,indent=2))

if __name__=='__main__':main()
