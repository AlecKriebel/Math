import concurrent.futures, pathlib, subprocess, sys
F=pathlib.Path(__file__).resolve().parent
files=sorted((F/'private_sources').glob('hs-*.png'))
assert len(files)==56, len(files)
def work(p):
    label='ocr_'+p.stem
    argv=[sys.executable,'-E','-B',str(F/'run_native.py'),label,'/opt/homebrew/bin/tesseract',str(p),str(p.with_suffix('')),'--psm','3']
    r=subprocess.run(argv,stdout=subprocess.PIPE,stderr=subprocess.PIPE,cwd=F)
    assert r.returncode==0, (label,r.stdout,r.stderr)
    return label
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:
    labels=list(ex.map(work,files))
out=F/'private_sources'/'hansen1993_ocr.txt'
out.write_text('\n'.join('\n=== PDF PAGE '+str(i+1)+' ===\n'+p.with_suffix('.txt').read_text() for i,p in enumerate(files)))
print('Completed',len(labels),'actual retained OCR processes; combined text bytes',out.stat().st_size)
