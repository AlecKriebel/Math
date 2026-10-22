#!/usr/bin/env python3
"""Freeze the current inspected PDF and portable verification contents."""
from pathlib import Path
import hashlib,json,shutil,subprocess,sys,zipfile
ROOT=Path(__file__).resolve().parent
PACKAGE=ROOT/'verification'
def binding(p):
    data=p.read_bytes();return {'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()}
def main():
    subprocess.run([sys.executable,'-B',str(ROOT/'prepare_package.py')],check=True,capture_output=True,text=True)
    run=subprocess.run([sys.executable,'-B',str(PACKAGE/'verify.py')],check=True,capture_output=True,text=True)
    shutil.copyfile(PACKAGE/'results.json',PACKAGE/'expected_results.json')
    members=sorted(p for p in PACKAGE.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.name not in {'MANIFEST.json','results.json'})
    # Nested manifests and results belong to immutable independent histories.
    members += sorted(p for p in PACKAGE.rglob('*') if p.is_file() and p.name in {'MANIFEST.json','results.json'} and p.parent!=PACKAGE)
    manifest={'schema':'tree-five-list-verification-archive-v1','version':'1.0','scope':'Explicit historical tree-equality counterexample. No historical firstness, minimality or current-openness claim.','files':[{'path':p.relative_to(PACKAGE).as_posix(),**binding(p)} for p in sorted(members)],'self_reference':'Root MANIFEST.json binds every other archive member and excludes itself; external BUILD_RECEIPT.json binds the manifest and archive. Root results.json is a replay output and is not archived.'}
    (PACKAGE/'MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n');members.append(PACKAGE/'MANIFEST.json')
    archive=ROOT/'Tree_Five_List_Verification_v1.0.zip'
    with zipfile.ZipFile(archive,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as out:
        for p in sorted(members):
            info=zipfile.ZipInfo(p.relative_to(PACKAGE).as_posix(),date_time=(2026,10,17,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o644<<16
            out.writestr(info,p.read_bytes())
    pdf=ROOT/'Tree_Five_List_Note_v1.0.pdf';shutil.copyfile(ROOT/'output/pdf/main.pdf',pdf)
    receipt={'version':'1.0','pdf':{'path':pdf.name,**binding(pdf)},'verification_zip':{'path':archive.name,**binding(archive)},'manifest_sha256':binding(PACKAGE/'MANIFEST.json')['sha256'],'manuscript_source_sha256':binding(ROOT/'manuscript/main.tex')['sha256'],'verification_run':json.loads(run.stdout),'archive_members':len(members)}
    (ROOT/'BUILD_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps(receipt,indent=2))
if __name__=='__main__':main()
