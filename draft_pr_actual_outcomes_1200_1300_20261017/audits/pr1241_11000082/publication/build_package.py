#!/usr/bin/env python3
"""Freeze authored sources, receipts and an inspected compiled PDF."""
from pathlib import Path
import hashlib,json,shutil,subprocess,sys,tempfile,zipfile
ROOT=Path(__file__).resolve().parent
PACKAGE=ROOT/'verification'
def expected_pdf_pages():
    context=json.loads((ROOT.parent/'CURRENT_PR1241_CONTEXT.json').read_text())
    pages=context.get('expected_pdf_pages')
    if type(pages) is not int or pages<1:raise RuntimeError('Set expected_pdf_pages from the actually compiled and rendered current PDF')
    return pages

def pdf_pages(path):
    run=subprocess.run(['pdfinfo',str(path)],capture_output=True,text=True,check=True)
    values=[line.split(':',1)[1].strip() for line in run.stdout.splitlines() if line.startswith('Pages:')]
    if len(values)!=1 or not values[0].isdigit():raise RuntimeError('Cannot independently read PDF page count')
    return int(values[0])
def binding(p):
    b=p.read_bytes();return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def document_bindings():
    """Refuse stale source/PDF or absent compile/visual-QA evidence."""
    source=ROOT/'manuscript/main.tex';pdf=ROOT/'output/pdf/main.pdf'
    compiled=json.loads((ROOT/'COMPILE_RECEIPT.json').read_text());layout=json.loads((ROOT/'LAYOUT_VERIFICATION.json').read_text())
    source_sha=binding(source)['sha256'];pdf_sha=binding(pdf)['sha256']
    if compiled.get('source_date_epoch')!='1792267200':raise RuntimeError('Current compilation must record the chosen reproducible build stamp')
    if compiled.get('returncode')!=0 or compiled.get('source_sha256')!=source_sha or compiled.get('pdf_sha256')!=pdf_sha:raise RuntimeError('Current source/PDF compilation binding missing or stale')
    if layout.get('status')!='pass' or layout.get('source_sha256')!=source_sha or layout.get('pdf_sha256')!=pdf_sha or not layout.get('all_pages_visually_inspected') or layout.get('page_indices_inspected')!=list(range(1,layout.get('pages',0)+1)) or layout.get('pages')!=expected_pdf_pages() or pdf_pages(pdf)!=expected_pdf_pages():raise RuntimeError('Current source/PDF all-page layout binding missing or stale')
    return {'source_sha256':source_sha,'pdf_sha256':pdf_sha,'compile_receipt_sha256':binding(ROOT/'COMPILE_RECEIPT.json')['sha256'],'layout_receipt_sha256':binding(ROOT/'LAYOUT_VERIFICATION.json')['sha256'],'current_context_sha256':binding(ROOT.parent/'CURRENT_PR1241_CONTEXT.json')['sha256'],'priority_adjudication_sha256':binding(ROOT.parent/'PRIORITY_ADJUDICATION.json')['sha256']}

def main():
    document_before=document_bindings()
    subprocess.run([sys.executable,'-B',str(ROOT/'prepare_package.py')],check=True,capture_output=True,text=True)
    members=sorted(p for p in PACKAGE.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p!=PACKAGE/'MANIFEST.json')
    manifest={'schema':'johnson-filtration-multiplicity-verification-v1','version':'1.0','scope':'Attributed alternative convex-core proof of unbounded ambient-conjugacy dilatation multiplicity in each fixed finite Johnson term; Ferudun DOI10.5281/zenodo.23301731 explicitly credited; no firstness/new existence/new mechanism/current-openness claim.','files':[{'path':p.relative_to(PACKAGE).as_posix(),**binding(p)} for p in members],'self_reference':'Root MANIFEST.json excluded from own list; every other member including nested immutable manifests is bound. External BUILD_RECEIPT binds manifest and ZIP.'}
    (PACKAGE/'MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n');members.append(PACKAGE/'MANIFEST.json')
    run=subprocess.run([sys.executable,'-B',str(PACKAGE/'verify.py')],check=True,capture_output=True,text=True)
    archive=ROOT/'Johnson_Filtration_Multiplicity_Verification_v1.0.zip';pdf=ROOT/'Johnson_Filtration_Multiplicity_Note_v1.0.pdf'
    local=ROOT.parent/'_local';local.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='publication-build-',dir=local) as folder:
        temporary_zip=Path(folder)/archive.name;temporary_pdf=Path(folder)/pdf.name
        with zipfile.ZipFile(temporary_zip,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as out:
            for p in sorted(members):
                info=zipfile.ZipInfo(p.relative_to(PACKAGE).as_posix(),date_time=(2026,10,17,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o644<<16;out.writestr(info,p.read_bytes())
        with zipfile.ZipFile(temporary_zip) as final:
            if set(final.namelist())!={p.relative_to(PACKAGE).as_posix() for p in members} or len(final.namelist())!=len(members) or json.loads(final.read('MANIFEST.json'))!=manifest:raise RuntimeError('Written ZIP inventory/manifest changed')
            for e in manifest['files']:
                data=final.read(e['path'])
                if len(data)!=e['bytes'] or hashlib.sha256(data).hexdigest()!=e['sha256']:raise RuntimeError('Written ZIP bytes differ at '+e['path'])
        shutil.copyfile(ROOT/'output/pdf/main.pdf',temporary_pdf)
        if document_bindings()!=document_before or binding(temporary_pdf)['sha256']!=document_before['pdf_sha256']:raise RuntimeError('Document/QA evidence changed during package build')
        temporary_zip.replace(archive);temporary_pdf.replace(pdf)
    receipt={'version':'1.0','document_bindings':document_before,'pdf':{'path':pdf.name,**binding(pdf)},'verification_zip':{'path':archive.name,**binding(archive)},'manifest_sha256':binding(PACKAGE/'MANIFEST.json')['sha256'],'manuscript_source_sha256':binding(ROOT/'manuscript/main.tex')['sha256'],'verification_run':json.loads(run.stdout),'archive_members':len(members),'release_artifacts':'Built in ignored temporary directory; written ZIP member bytes and final source/PDF/QA state checked before replacing release files.'}
    (ROOT/'BUILD_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps(receipt,indent=2))
if __name__=='__main__':main()
