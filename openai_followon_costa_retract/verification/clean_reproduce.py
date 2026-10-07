#!/usr/bin/env python3
"""Verify the exact archive's contents and reproduce its checks in a fresh directory."""
from pathlib import Path
import argparse,datetime,hashlib,json,subprocess,tempfile,zipfile
ROOT=Path(__file__).resolve().parents[1]

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--python',required=True);ap.add_argument('--label',default='v1');a=ap.parse_args()
    dest=ROOT/'receipts'/('clean_reproduction_'+a.label);dest.mkdir(parents=True,exist_ok=True)
    archive=ROOT/'publication/upload-kit/source-and-verification.zip'
    record={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'archive_sha256':hashlib.sha256(archive.read_bytes()).hexdigest(),'runs':{}}
    with tempfile.TemporaryDirectory(dir=ROOT/'verification',prefix='clean-package-') as td:
        td=Path(td)
        with zipfile.ZipFile(archive) as z:
            assert z.testzip() is None
            assert all(not Path(n).is_absolute() and '..' not in Path(n).parts for n in z.namelist())
            z.extractall(td)
        inner=json.loads((td/'CONTENTS.json').read_text())
        for n,info in inner['files'].items():
            b=(td/n).read_bytes();assert len(b)==info['bytes'] and hashlib.sha256(b).hexdigest()==info['sha256'],n
        record['inner_manifest_files']=len(inner['files'])
        assert (td/'main.tex').read_bytes()==(ROOT/'manuscript/main.tex').read_bytes()
        for name,cmd in [('stabilization',[a.python,'check_stabilization.py']),('nonpolynomiality_identities',[a.python,'check_nonpolynomiality_certificates.py']),('paper_build',['tectonic','main.tex','--keep-logs'])]:
            p=subprocess.run(cmd,cwd=td,text=True,capture_output=True,timeout=60)
            (dest/(name+'.stdout')).write_text(p.stdout);(dest/(name+'.stderr')).write_text(p.stderr)
            record['runs'][name]={'exit':p.returncode};assert p.returncode==0,(name,p.stderr)
        log=(td/'main.log').read_text();assert 'Overfull' not in log
        assert 'undefined references' not in log.lower() and 'undefined citations' not in log.lower()
        for path in [td/'main.pdf',ROOT/'publication/upload-kit/paper.pdf']:
            subprocess.run(['pdftotext',str(path),str(dest/(('clean' if path.parent==td else 'deposit')+'.txt'))],check=True)
        assert (dest/'clean.txt').read_text()==(dest/'deposit.txt').read_text(),'PDF text changed in clean build'
        record['pdf_text_equal']=True
        record['clean_pdf_bytes']=(td/'main.pdf').stat().st_size
    record['status']='PASS'
    (dest/'receipt.json').write_text(json.dumps(record,indent=2)+'\n');print(json.dumps(record,indent=2))

if __name__=='__main__':main()
