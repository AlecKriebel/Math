"""Fresh physical fixtures; all mutations remain under this review's RAM folder."""
from pathlib import Path
from tempfile import TemporaryDirectory
import hashlib, json, os, shutil, stat, subprocess, sys, time

ROOT = Path(__file__).resolve().parent.parent
WORK = ROOT/'preprint/tmp/review03-work'
SOURCE = WORK/'extracted'
PDF = ROOT/'preprint/output/pdf/paper.pdf'
PINS = json.loads((ROOT/'PREPRINT_REVIEW_INPUTS_03.json').read_text())['six']
ENV = os.environ.copy()
ENV.update(TMPDIR=str(WORK), PYTHONDONTWRITEBYTECODE='1')
for key in ('PYTHONPATH','PYTHONHOME','PYTHONOPTIMIZE'):
    ENV.pop(key, None)


def need(ok, message):
    if not ok:
        raise RuntimeError(message)


def digest(b):
    return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}


def scan(root):
    rows = {}
    if not root.exists():
        return rows
    def walk(p):
        for x in sorted(p.iterdir()):
            s=x.lstat();n=x.relative_to(root).as_posix()
            if stat.S_ISLNK(s.st_mode):
                rows[n]=('link',os.readlink(x))
            elif stat.S_ISDIR(s.st_mode):
                rows[n]=('dir',);walk(x)
            elif stat.S_ISREG(s.st_mode):
                rows[n]=('file',s.st_ino,s.st_nlink,digest(x.read_bytes()))
            else:
                rows[n]=('special',s.st_mode)
    walk(root)
    return rows


def run(py,opt,script,args):
    return subprocess.run([py,'-E','-s','-B']+(['-O'] if opt else [])+
                          [str(script)]+list(map(str,args)),env=ENV,cwd='/',
                          capture_output=True,timeout=120)


def main():
    rows=[]
    baseline=scan(SOURCE)
    pdf_before=PDF.read_bytes()
    runtimes=['/opt/homebrew/bin/python3',
              '/Users/alec/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3']
    for py in runtimes:
        for opt in (False,True):
            mode=Path(py).parents[1].name+('-O' if opt else '-normal')
            version=subprocess.run([py,'--version'],capture_output=True,text=True).stdout.strip()
            with TemporaryDirectory(dir=WORK,prefix='physical-positive-') as tmp:
                t=Path(tmp);src=t/'relocated source with spaces';shutil.copytree(SOURCE,src)
                for p in src.rglob('*'):
                    if p.is_file():os.utime(p,(1000000000,1000000000))
                before=scan(src)
                r=run(py,opt,src/'verify_bundle.py',['--integrity-only','--pdf',PDF])
                need(r.returncode==0,'relocated source integrity '+r.stderr.decode())
                out=t/'rebuilt with spaces'
                r=run(py,opt,src/'build_package.py',['--pdf',PDF,'--output-dir',out])
                need(r.returncode==0,'portable rebuild '+r.stderr.decode())
                got={n:digest((out/n).read_bytes()) for n in PINS}
                need(got==PINS,'portable same-six mismatch')
                need(scan(src)==before,'portable build changed input')
                rows.append(dict(runtime=version,optimized=opt,case='relocated_changed_mtimes_same_six_rebuild',
                                 status='PASS',six=got))
            for case in ('changed_tex','missing_tex','hidden_extra','empty_directory','source_symlink',
                         'source_fifo','wrong_pdf'):
                with TemporaryDirectory(dir=WORK,prefix='physical-source-') as tmp:
                    t=Path(tmp);src=t/'source';shutil.copytree(SOURCE,src);pdf=PDF
                    if case=='changed_tex':(src/'paper.tex').write_bytes(b'changed')
                    elif case=='missing_tex':(src/'paper.tex').unlink()
                    elif case=='hidden_extra':(src/'.hidden').write_bytes(b'extra')
                    elif case=='empty_directory':(src/'empty').mkdir()
                    elif case=='source_symlink':
                        (src/'paper.tex').unlink();(src/'paper.tex').symlink_to(SOURCE/'paper.tex')
                    elif case=='source_fifo':os.mkfifo(src/'pipe')
                    elif case=='wrong_pdf':pdf=t/'wrong.pdf';pdf.write_bytes(b'%PDF-wrong')
                    before=scan(t)
                    r=run(py,opt,src/'verify_bundle.py',['--integrity-only','--pdf',pdf])
                    need(r.returncode!=0,'accepted source negative '+case)
                    need(scan(t)==before,'source rejection changed fixture '+case)
                    rows.append(dict(runtime=version,optimized=opt,case=case,status='REJECTED',
                                     stderr=r.stderr.decode(errors='replace')[-1000:],preserved=True))
            for case in ('output_inside_input','ancestor_symlink','destination_symlink','output_fifo',
                         'output_directory','output_hardlink_to_pdf','output_hardlink_to_source',
                         'inventory_hardlink_to_pdf','file_parent'):
                with TemporaryDirectory(dir=WORK,prefix='physical-output-') as tmp:
                    t=Path(tmp);src=t/'source';shutil.copytree(SOURCE,src)
                    out=t/'outputs';out.mkdir();pdf=t/'input.pdf';pdf.write_bytes(pdf_before)
                    # A sentinel output must survive every rejected build.
                    (out/'zenodo-metadata.json').write_bytes(b'preserve existing output\n')
                    if case=='output_inside_input':out=src/'new-output'
                    elif case=='ancestor_symlink':
                        link=t/'linked-parent';link.symlink_to(out,target_is_directory=True);out=link/'nested'
                    elif case=='destination_symlink':(out/'paper.tex').symlink_to(src/'paper.tex')
                    elif case=='output_fifo':os.mkfifo(out/'source-and-verification.zip')
                    elif case=='output_directory':(out/'paper.tex').mkdir()
                    elif case=='output_hardlink_to_pdf':os.link(pdf,out/'paper.tex')
                    elif case=='output_hardlink_to_source':os.link(src/'paper.tex',out/'paper.tex')
                    elif case=='inventory_hardlink_to_pdf':os.link(pdf,out/'PACKAGE_INVENTORY.json')
                    elif case=='file_parent':(out/'output').write_bytes(b'parent is file')
                    before=scan(t)
                    r=run(py,opt,src/'build_package.py',['--pdf',pdf,'--output-dir',out])
                    need(r.returncode!=0,'accepted output negative '+case)
                    need(scan(t)==before,'build rejection changed input/output '+case)
                    rows.append(dict(runtime=version,optimized=opt,case=case,status='REJECTED',
                                     stderr=r.stderr.decode(errors='replace')[-1000:],preserved=True))
            print(version,opt,'physical controls complete',flush=True)
    need(scan(SOURCE)==baseline and PDF.read_bytes()==pdf_before,'frozen source/PDF changed')
    receipt={'status':'PASS','runs':rows,'count':len(rows),
             'positive_rebuilds':4,'negative_fixtures':64,
             'source_and_supplied_pdf_preserved':True,'scratch':'owned RAM fixtures, removed'}
    (ROOT/'review_preprint03/PHYSICAL_AND_REBUILD_RESULTS.json').write_text(json.dumps(receipt,indent=2)+'\n')


if __name__=='__main__':
    main()
