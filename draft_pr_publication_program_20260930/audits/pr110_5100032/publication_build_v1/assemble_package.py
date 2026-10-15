#!/usr/bin/env python3
"""Assemble and authenticate a fixed publication candidate; no service actions."""
from pathlib import Path, PurePosixPath
from datetime import datetime, timezone
import hashlib, json, os, shutil, stat, sys, zipfile

B=Path(__file__).resolve().parent; A=B.parent
S=A/'publication_package_v1'; D=A/'publication_ready_v1'
def require(ok,msg):
    if not ok: raise RuntimeError(msg)
def now(): return datetime.now(timezone.utc).isoformat()
def pin(p, rel=None):
    b=p.read_bytes(); return {'path':rel or p.name,'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def read(p): return json.loads(p.read_text())
def write(p,value): p.write_text(json.dumps(value,indent=2,sort_keys=True)+'\n')
def main():
    start=now(); require(not D.exists(),'Candidate directory must be fresh')
    m=read(S/'source_payload_manifest.json')
    require(pin(S/'source_payload_manifest.json')['sha256']=='003e11228b5b3cd7ffb6b20712fae42574c38d8f52a7f3bc9dafc3a4d40604b8','External source manifest pin')
    for e in m['files']: require(pin(S/e['path'])==e,'Source changed before assembly')
    require(read(B/'ROOT_SOURCE_AUTHENTICATION.json')['source_unchanged_after_root_replay'],'Root source authentication')
    compiler=read(A/'actual_operations/publication_pdf_compile_v1_20261006/execution.json')
    require(compiler['exit_code']==0 and compiler['stderr']['bytes']==0,'Actual compiler failed')
    info=(A/'actual_operations/publication_pdf_info_v1_20261006/stdout.bin').read_text()
    require('Pages:           4' in info,'Expected four-page export')
    log=(B/'focal_antipedal_sum.log').read_text()
    require('Undefined control sequence' not in log and 'Overfull' not in log and 'undefined references' not in log,'Compiler warning/error requires repair')
    D.mkdir()
    for p in S.iterdir(): shutil.copyfile(p,D/p.name)
    shutil.copyfile(B/'focal_antipedal_sum.pdf',D/'focal_antipedal_sum.pdf')
    Q=D/'root_reproduction'; Q.mkdir()
    for n in ('root_verification_normal.json','root_verification_optimized.json','root_execution_envelope.json',
              'ROOT_SOURCE_AUTHENTICATION.json','root_replay_stdout.json','root_replay_stderr.bin'):
        shutil.copyfile(B/n,Q/n)
    T=D/'build'; T.mkdir()
    for n in ('BUILTIN_COMPILER_DIAGNOSTICS.json','focal_antipedal_sum.log'):
        shutil.copyfile(B/n,T/n)
    shutil.copyfile(A/'actual_operations/publication_pdf_compile_v1_20261006/execution.json',T/'compiler_execution.json')
    shutil.copyfile(A/'actual_operations/publication_pdf_compile_v1_20261006/stdout.bin',T/'compiler_stdout.txt')
    shutil.copyfile(A/'actual_operations/publication_pdf_info_v1_20261006/stdout.bin',T/'pdfinfo.txt')
    pdf=pin(D/'focal_antipedal_sum.pdf')
    provenance={'schema':'pr110-publication-build-provenance/v1','actual_assembler_PID':os.getpid(),
        'UTC':now(),'source':pin(D/'focal_antipedal_sum.tex'),'PDF':pdf,'PDF_page_count':4,
        'built_in_compiler_success':True,'export_compiler':compiler,
        'visual_review':{'reviewer':'root','scope':'Every one of four rendered PDF pages inspected in full',
            'result':'No clipping, overlaps, missing glyphs or broken references seen',
            'render_execution':read(A/'actual_operations/publication_pdf_render_v1_20261006/execution.json'),
            'render_page_pins':[pin(B/('page-'+str(i)+'.png')) for i in range(1,5)]},
        'authored_source_bytes_preserved':True,'whole_package_reviews_pending':True,
        'meaning':'Fixed candidate for review. A later external gate records independent reviews and publication authorization.'}
    write(T/'build_provenance.json',provenance)
    (D/'PACKAGE_README.md').write_text('''# Publication candidate: focal antipedal sum invariant

Alec Kriebel, version 1.0, 6 October 2026. Original work licensed CC BY 4.0.

This package contains the self-contained four-page research note, its LaTeX source,
the portable standard-library exact verifier, original authored-source custody
receipts, and a separate root reproduction plus actual PDF build provenance.
The adjacent deposit manifest names the PDF and support ZIP. The support ZIP also
contains the same PDF bytes for convenient offline review.

Read `README.md` for the theorem, assumptions, attribution, exact controls and
commands. Extract the ZIP or use a scratch copy before running
`python3 run_verification.py`, since that runner writes fresh receipts. Python
3.10 or newer is sufficient; no packages or network are needed. Compilation of
the standalone source requires ordinary LaTeX with the listed packages, or
Tectonic; the PDF here was exported by Tectonic after a successful built-in
compiler check. Source-relative manuscript binding is portable.

`source_payload_manifest.json` and `source_seal_receipt.json` preserve the earlier
source-only preparation checkpoint exactly. Their statements about compilation
and review pending refer to that earlier checkpoint. `seal_source_payload.py`
is for the author's original source-only custody environment, not this enlarged
release; it is unnecessary to run the mathematical verifier. The source receipts
and separate root reproduction describe real completed runs, not future promises.
`build/build_provenance.json` records the exported PDF and all four rendered pages.

`PACKAGE_MANIFEST.json` covers every payload member except itself, `SHA256SUMS`
and the ZIP. `SHA256SUMS` adds the manifest. The external candidate seal binds
all of those files and the ZIP; independent whole-package reviews and the final
publication gate are retained separately in the repository audit folder. Such
later review receipts do not change the fixed manuscript or archive bytes.

The primary-source audit is bounded as stated in the manuscript and
`source_audit_summary.md`. Observation credit belongs to Reznik, Garcia and
Koiller; classical mechanisms are explicitly credited. No absolute-first claim
or assertion that the problem stayed open throughout every later publication is
made. AI tools were used extensively; this is unrefereed and has not undergone
conventional human peer review. Third-party source bodies and credentials are
not redistributed.
''')
    files=sorted(p for p in D.rglob('*') if p.is_file())
    entries=[pin(p,p.relative_to(D).as_posix()) for p in files]
    manifest={'schema':'pr110-fixed-publication-payload-manifest/v1','UTC':now(),'actual_assembler_PID':os.getpid(),
      'files':entries,'excluded':['PACKAGE_MANIFEST.json','SHA256SUMS','focal_antipedal_sum_support.zip'],
      'source_manifest':pin(D/'source_payload_manifest.json'),'state':'fixed candidate for independent whole-package review'}
    write(D/'PACKAGE_MANIFEST.json',manifest)
    summed=entries+[pin(D/'PACKAGE_MANIFEST.json')]
    (D/'SHA256SUMS').write_text(''.join(e['sha256']+'  '+e['path']+'\n' for e in sorted(summed,key=lambda x:x['path'])))
    members=sorted(p for p in D.rglob('*') if p.is_file())
    zpath=D/'focal_antipedal_sum_support.zip'
    with zipfile.ZipFile(zpath,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for p in members:
            rel=p.relative_to(D).as_posix(); info=zipfile.ZipInfo(rel,date_time=(2026,10,6,0,0,0))
            info.external_attr=(stat.S_IFREG|0o644)<<16; info.compress_type=zipfile.ZIP_DEFLATED
            z.writestr(info,p.read_bytes(),compress_type=zipfile.ZIP_DEFLATED,compresslevel=9)
    with zipfile.ZipFile(zpath) as z:
        require(z.testzip() is None,'Archive CRC integrity')
        require(z.namelist()==[p.relative_to(D).as_posix() for p in members],'Exact archive member set/order')
        for name in z.namelist():
            parts=PurePosixPath(name); require(not parts.is_absolute() and '..' not in parts.parts,'Archive path scope')
            require(z.read(name)==(D/name).read_bytes(),'Archive full byte mismatch: '+name)
    for e in m['files']: require(pin(S/e['path'])==e and pin(D/e['path'])==e,'Authored source changed after assembly')
    allfiles=sorted(p for p in D.rglob('*') if p.is_file())
    seal={'schema':'pr110-fixed-publication-candidate-seal/v1','UTC_start':start,'UTC_end':now(),'actual_assembler_PID':os.getpid(),
      'package_directory':str(D),'files':[pin(p,p.relative_to(D).as_posix()) for p in allfiles],
      'payload_manifest':pin(D/'PACKAGE_MANIFEST.json'),'PDF':pdf,'ZIP':pin(zpath),
      'full_ZIP_members_checked':len(members),'whole_package_reviews_pending':True,'publication_ready':False,
      'workflow_completion_percent':45}
    write(A/'publication_ready_v1_SEAL.json',seal)
    print(json.dumps({'status':'fixed_candidate_assembled','PDF':pdf,'ZIP':pin(zpath),'package_files':len(allfiles),
      'archive_members_checked':len(members),'seal':pin(A/'publication_ready_v1_SEAL.json'),'publication_ready':False},indent=2))
if __name__=='__main__':main()
