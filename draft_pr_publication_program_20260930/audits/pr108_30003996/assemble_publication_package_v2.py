#!/usr/bin/env python3
"""Assemble immutable authored PR108 source, PDF and deterministic ZIP for review."""
from pathlib import Path, PurePosixPath
import argparse, datetime, hashlib, json, os, shutil, zipfile
A=Path(__file__).resolve().parent
S=A/'publication_package_v2'
D=A/'publication_ready_package_v2'
def require(c,m):
    if not c:raise RuntimeError(m)
def sha(b):return hashlib.sha256(b).hexdigest()
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def encode(x):return (json.dumps(x,indent=2,ensure_ascii=False)+'\n').encode()
def safe(q,root):
    require(q.is_file() and not q.is_symlink() and q.resolve().is_relative_to(root.resolve()),'nonregular/escaping input')
    for p in q.parents:
        require(not p.is_symlink(),'symlink ancestor')
def body(q,root):safe(q,root);return q.read_bytes()
def pin(q,root):
    b=body(q,root);return {'relative_path':str(q.relative_to(root)),'bytes':len(b),'sha256':sha(b)}
def source_inventory():
    seal=json.loads(body(S/'SEAL.json',S));mb=body(S/'SOURCE_PREPARATION_MANIFEST.json',S)
    require(len(mb)==seal['manifest_bytes'] and sha(mb)==seal['manifest_sha256']==args.source_manifest_sha,'source seal drift')
    m=json.loads(mb);require(m['PR']==108 and m['problem_id']==30003996 and len(m['files'])>=26,'source identity')
    paths=[]
    for row in m['files']:
        rel=row['relative_path'];require(str(PurePosixPath(rel))==rel and '..' not in PurePosixPath(rel).parts and not PurePosixPath(rel).is_absolute(),'source path')
        b=body(S/rel,S);require(len(b)==row['bytes'] and sha(b)==row['sha256'],'source pin drift')
        paths.append(rel)
    cs=body(S/'SHA256SUMS',S)
    require(len(cs)==seal['checksums_bytes'] and sha(cs)==seal['checksums_sha256'],'source checksums drift')
    paths+=['SOURCE_PREPARATION_MANIFEST.json','SHA256SUMS','SEAL.json']
    require(set(paths)=={str(p.relative_to(S)) for p in S.rglob('*') if p.is_file()},'unexpected source files')
    return paths,m
def init():
    paths,m=source_inventory();require(not D.exists(),'review package exists')
    qa=json.loads(body(A/'ROOT_PDF_UNCHANGED_V2_CONTINUITY_20261006.json',A))
    pdf=A/'publication_build_v1/root_dependent_spanning_trees.pdf'
    require(sha(body(S/'root_dependent_spanning_trees.tex',S))==qa['source_after_export']['sha256']=='a0e7e6158267fbf9ca4cafbd5ccb4cfa4ac79a1e0aea61282c9ee09d7e8d11d5','TeX drift')
    require(sha(body(pdf,A))==qa['PDF']['sha256'] and qa['all_actual_page_images_inspected_by_root'] and not qa['layout_concerns'],'PDF QA drift')
    require(json.loads(body(S/'intended_zenodo_metadata.json',S))['metadata']==json.loads(body(S/'zenodo-deposit.json',S))['metadata'],'source metadata mismatch')
    D.mkdir()
    for rel in paths:
        q=D/'source_preparation'/rel;q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(body(S/rel,S))
    (D/pdf.name).write_bytes(body(pdf,A))
    for name in ['intended_zenodo_metadata.json','zenodo-deposit.json']:(D/name).write_bytes(body(S/name,S))
    require(json.loads((D/'intended_zenodo_metadata.json').read_text())['metadata']==json.loads((D/'zenodo-deposit.json').read_text())['metadata'],'metadata mismatch')
    (D/'README.md').write_text("""# Aggregate root-dependent spanning-tree cost: review package
This package contains the four-page self-contained note and portable exact supporting files for Kaibel's Problem1. It proves NP-completeness for the all-root/full-orientation objective with costs in {0,1,2}, and the uniform positive shift gives {1,2,3}. One common undirected tree is used at every root.

The corrected V2 source-preparation snapshot is preserved unchanged in source_preparation/. Its correction ledger records the whole-package R1 input-validation repair, with V1 preserved separately in the repository. Its README, preparation seal and gates record their historical preparation state. They do not certify this assembled PDF/ZIP or replace subsequent whole-package review. The copied historical PROOF.md is a byte-bound B=n+1 preparation artifact with superseded status prose; the current note presents the same mechanism at B=2. Source_preparation/PRIORITY_PROVENANCE.md explains the dated priority audit and inaccessible originals. No earlier covering proof was located by 6 October 2026; absolute first discovery and continued openness are not asserted.

The PDF is root_dependent_spanning_trees.pdf. Its LaTeX source is source_preparation/root_dependent_spanning_trees.tex. Run the standard-library diagnostics with Python 3.10+:

    python3 source_preparation/run_checks.py --include-historical

This runs both normal and optimized Python, twelve mandatory intended failures, including malformed-input suffix controls, and four scratch-copy historical replays; it writes only removed temporary files by default. To retain a new receipt, add --output with an external scratch path. Directly executing copied historical scripts writes in their own folder, so use the runner to preserve this immutable snapshot.

PACKAGE_MANIFEST.json binds the logical authored payload and exact source identity. SHA256SUMS binds the payload files other than itself; the manifest and ZIP have external seal pins. The support ZIP contains this PDF and the entire logical package plus PACKAGE_MANIFEST.json; it excludes itself and contains no third-party PDF, source extract, screenshot, raw web response, credential or native-integration helper.

The identical intended metadata is in intended_zenodo_metadata.json and zenodo-deposit.json. The latter is for the repository's top-level Zenodo kit, selecting the adjacent PDF and support ZIP. The ZIP does not recursively contain itself; reusing its deposit file requires the original support ZIP adjacent to the extracted package. No DOI placeholder is asserted.

Extensive AI assistance in solving, drafting, source checks, code generation, reproduction and adversarial audits is disclosed in the manuscript and metadata. Automated review is not human refereeing; this is an unrefereed preprint without conventional human peer review. Original author effort 2/5 was authenticated from QUEUE/prose, no original structured ledger was supplied, and subsequent audits/package preparation add zero central proof-search turns.

Assembly is preparation for fresh whole-package review. Publication clearance and any later service actions are recorded separately in the repository, not inferred from this dated assembly snapshot. The offered license for authored artifacts is CC BY 4.0, as stated in source_preparation/LICENSE.md.
""")
    (A/'ROOT_PUBLICATION_SOURCE_ADOPTION_V2_20261006.json').write_bytes(encode({'UTC':now(),'actual_operator_PID':os.getpid(),'source_snapshot_SHA':sha(body(S/'SOURCE_PREPARATION_MANIFEST.json',S)),'source_files_authenticated_and_copied':len(paths),'TeX_SHA':m['paper_sha256'],'PDF_SHA':sha(body(pdf,A)),'whole_package_ready':False,'publication_clearance':False}))
    print(json.dumps({'phase':'init','logical_source_files':len(paths),'directory':str(D)}))
def seal():
    _,m=source_inventory()
    require(D.is_dir() and not (D/'PACKAGE_MANIFEST.json').exists(),'missing/already sealed')
    r=body(A/'ROOT_READY_PACKAGE_REPRODUCTION_V2_20261006.json',A)
    rr=json.loads(r);require(rr['all_pass'] and rr['intentional_controls_rejected']==12 and len(rr['historical_scratch_replays'])==4,'actual runner failed')
    require(rr['verification_reports'][0]['paper_sha256']==m['paper_sha256'],'runner paper binding')
    (D/'root_verified_reproduction.json').write_bytes(r)
    (D/'BUILD_PROVENANCE.json').write_bytes(encode({'UTC':now(),'actual_operator_PID':os.getpid(),'source_preparation_manifest_sha256':sha(body(S/'SOURCE_PREPARATION_MANIFEST.json',S)),'PDF_QA_receipt_sha256':sha(body(A/'ROOT_PDF_UNCHANGED_V2_CONTINUITY_20261006.json',A)),'source_adoption_receipt_sha256':sha(body(A/'ROOT_PUBLICATION_SOURCE_ADOPTION_V2_20261006.json',A)),'root_reproduction_execution_sha256':sha(body(A/'actual_operations/publication_ready_package_reproduction_v2/execution.json',A)),'PDF_pages_inspected':4,'native_compiler_success':True,'actual_exact_runner_success':True,'metadata_exact_matches_source_preparation':True,'fresh_whole_package_review_pending_at_assembly':True,'publication_clearance':False}))
    paths=sorted(p for p in D.rglob('*') if p.is_file())
    (D/'SHA256SUMS').write_text(''.join(sha(body(p,D))+'  '+str(p.relative_to(D))+'\n' for p in paths))
    paths.append(D/'SHA256SUMS');paths=sorted(paths)
    manifest={k:m[k] for k in ['PR','problem_id','original_head','review_hash','dataset_revision','imported_prior_report','author_orcid','effective_proof_sha256']}
    manifest.update({'schema':'pr108-publication-package-manifest/v1','UTC':now(),'actual_operator_PID':os.getpid(),'paper_sha256':m['paper_sha256'],'original_effort':'2/5; imported historical count, original structured ledger absent','new_central_proof_search_turns':0,'logical_payload_excludes_manifest_and_archive_self':True,'files':[pin(p,D) for p in paths]})
    (D/'PACKAGE_MANIFEST.json').write_bytes(encode(manifest));paths.append(D/'PACKAGE_MANIFEST.json')
    archive=D/'root_dependent_spanning_trees_support.zip'
    with zipfile.ZipFile(archive,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for p in sorted(paths):
            info=zipfile.ZipInfo(str(p.relative_to(D)),(2026,10,6,0,0,0));info.external_attr=0o100644<<16
            info.compress_type=zipfile.ZIP_DEFLATED;z.writestr(info,body(p,D))
    with zipfile.ZipFile(archive) as z:
        require(len(z.namelist())==len(paths) and len(set(z.namelist()))==len(paths),'archive members')
        for p in paths:require(z.read(str(p.relative_to(D)))==body(p,D),'archive body drift')
    (A/'ROOT_PUBLICATION_READY_PACKAGE_V2_SEAL_20261006.json').write_bytes(encode({'UTC':now(),'actual_operator_PID':os.getpid(),'package_manifest':pin(D/'PACKAGE_MANIFEST.json',D),'archive':pin(archive,D),'logical_payload_files':len(manifest['files']),'archive_members':len(paths),'archived_all_payload_bytes_match':True,'source_preparation_unchanged':True,'whole_package_review_ready':True,'whole_package_review_completed':False,'publication_clearance':False,'logical_payload_bytes':sum(p['bytes'] for p in manifest['files'])}))
    print(json.dumps({'phase':'seal','payload_files':len(manifest['files']),'archive_members':len(paths),'manifest_SHA':sha(body(D/'PACKAGE_MANIFEST.json',D)),'archive_bytes':archive.stat().st_size,'whole_package_review_completed':False}))
ap=argparse.ArgumentParser();ap.add_argument('phase',choices=['init','seal']);ap.add_argument('--source-manifest-sha',required=True);args=ap.parse_args()
require(len(args.source_manifest_sha)==64 and all(ch in '0123456789abcdef' for ch in args.source_manifest_sha),'explicit source manifest SHA256')
init() if args.phase=='init' else seal()

