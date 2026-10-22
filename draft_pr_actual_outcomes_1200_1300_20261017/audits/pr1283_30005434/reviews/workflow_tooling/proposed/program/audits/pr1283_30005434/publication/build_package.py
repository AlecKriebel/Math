#!/usr/bin/env python3
"""Build inspected eight-file edition/archive; never infer actual review PASS."""
from pathlib import Path
import datetime,hashlib,json,runpy,shutil,subprocess,sys,tempfile,zipfile
ROOT=Path(__file__).resolve().parent
PDF='Semibrace_Existence_Classification_Note_v1.0.pdf'
ZIP='Semibrace_Existence_Classification_Verification_v1.0.zip'
def binding(path):data=path.read_bytes();return {'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()}
def pdf_pages(path):
    result=subprocess.run(['pdfinfo',str(path)],check=True,capture_output=True,text=True)
    values=[line.split(':',1)[1].strip() for line in result.stdout.splitlines() if line.startswith('Pages:')]
    if len(values)!=1 or not values[0].isdigit():raise RuntimeError('Cannot independently read PDF page count')
    return int(values[0])
def document_bindings():
    context=runpy.run_path(str(ROOT/'prepare_package.py'))['load_context']()
    source=ROOT/'manuscript/main.tex';pdf=ROOT/'output/pdf/main.pdf';compiled=json.loads((ROOT/'COMPILE_RECEIPT.json').read_text());layout=json.loads((ROOT/'LAYOUT_VERIFICATION.json').read_text())
    source_sha=binding(source)['sha256'];pdf_sha=binding(pdf)['sha256'];pages=context['expected_pdf_pages']
    if compiled.get('returncode')!=0 or compiled.get('source_date_epoch')!=context['source_date_epoch'] or compiled.get('source_sha256')!=source_sha or compiled.get('pdf_sha256')!=pdf_sha or not compiled.get('at_utc'):raise RuntimeError('Current actual source/PDF compilation receipt missing/stale')
    if layout.get('status')!='pass' or layout.get('source_sha256')!=source_sha or layout.get('pdf_sha256')!=pdf_sha or layout.get('all_pages_visually_inspected') is not True or layout.get('page_indices_inspected')!=list(range(1,pages+1)) or layout.get('pages')!=pages or not layout.get('at_utc') or pdf_pages(pdf)!=pages:raise RuntimeError('Actual all-page visual inspection missing/stale')
    return {**context['document_bindings'],'current_context_sha256':binding(ROOT.parent/'CURRENT_PR1283_CONTEXT.json')['sha256'],**context['gate_bindings']}
def main():
    before=document_bindings()
    subprocess.run([sys.executable,'-B',str(ROOT/'prepare_package.py')],check=True,capture_output=True,text=True)
    package=ROOT/'verification';members=sorted(p for p in package.rglob('*') if p.is_file() and p!=package/'MANIFEST.json')
    if any(p.is_symlink() for p in package.rglob('*')):raise RuntimeError('Package symlink forbidden')
    manifest={'schema':'semibrace-existence-classification-verification-v1','version':'1.0','scope':'Explicit current context, immutable original eight files and authored proofs/reviews/receipts. No mathematical, priority or firstness acceptance is inferred from byte integrity.','files':[{'path':p.relative_to(package).as_posix(),**binding(p)} for p in members],'self_reference':'Root MANIFEST.json self-excluded; outside BUILD_RECEIPT and published artifact hashes are trust anchors.'}
    (package/'MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n');members.append(package/'MANIFEST.json')
    anchors={'manifest':binding(package/'MANIFEST.json')['sha256'],'context':before['current_context_sha256'],'snapshot':before['submitted_snapshot_sha256']}
    args=[arg for key,value in anchors.items() for arg in ['--expected-'+key+'-sha256',value]]
    run=subprocess.run([sys.executable,'-B',str(package/'verify.py'),*args],capture_output=True,text=True)
    if run.returncode:raise RuntimeError('Portable verifier rejected build: '+run.stderr)
    local=ROOT.parent/'reviews/workflow_tooling/_local';local.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='semibrace-existence-build-',dir=local) as folder:
        temporary_zip=Path(folder)/ZIP;temporary_pdf=Path(folder)/PDF
        with zipfile.ZipFile(temporary_zip,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as archive:
            for path in sorted(members):
                info=zipfile.ZipInfo(path.relative_to(package).as_posix(),date_time=(2026,10,17,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o644<<16;archive.writestr(info,path.read_bytes())
        with zipfile.ZipFile(temporary_zip) as archive:
            if len(archive.namelist())!=len(members) or set(archive.namelist())!={p.relative_to(package).as_posix() for p in members}:raise RuntimeError('Written ZIP inventory differs')
            for path in members:
                if archive.read(path.relative_to(package).as_posix())!=path.read_bytes():raise RuntimeError('Written ZIP bytes differ')
        shutil.copyfile(ROOT/'output/pdf/main.pdf',temporary_pdf)
        if document_bindings()!=before or binding(temporary_pdf)['sha256']!=before['pdf_sha256']:raise RuntimeError('Document/assurance drift during build')
        temporary_zip.replace(ROOT/ZIP);temporary_pdf.replace(ROOT/PDF)
    receipt={'at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'version':'1.0','document_bindings':before,'pdf':{'path':PDF,**binding(ROOT/PDF)},'verification_zip':{'path':ZIP,**binding(ROOT/ZIP)},'manifest_sha256':anchors['manifest'],'verification_anchors':anchors,'verification_run':json.loads(run.stdout),'archive_members':len(members),'current_edition_files':8,'original_submitted_files':8,'scope':'Built/copied artifacts only. Actual final whole-package reviews are required separately.'}
    (ROOT/'BUILD_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps(receipt,indent=2))
if __name__=='__main__':main()
