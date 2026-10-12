#!/usr/bin/env python3
"""Local-only read/replay custody; writes exclusively under this audit directory."""
import datetime, hashlib, json, os, pathlib, shutil, subprocess, sys, zipfile

HERE = pathlib.Path(__file__).resolve().parent
PACKAGE = HERE.parent / 'publication_package_v1'

def utc():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()

def sha(body):
    return hashlib.sha256(body).hexdigest()

def inventory(root):
    return [{'path': str(p.relative_to(root)), 'bytes': p.stat().st_size,
             'sha256': sha(p.read_bytes())} for p in sorted(root.rglob('*')) if p.is_file()]

def write(path, value):
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + '\n')

def execute(label, argv, cwd=None):
    directory = HERE / 'execution' / label
    directory.mkdir(parents=True, exist_ok=False)
    rec = {'label': label, 'argv': argv, 'cwd': str(cwd or HERE),
           'declared_utc': utc(), 'driver_pid': os.getpid(),
           'driver_sha256': sha(pathlib.Path(__file__).read_bytes())}
    proc = subprocess.Popen(argv, cwd=cwd or HERE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    rec.update(pid=proc.pid, spawn_observed_utc=utc())
    out, err = proc.communicate()
    (directory/'stdout.bin').write_bytes(out)
    (directory/'stderr.bin').write_bytes(err)
    rec.update(completed_utc=utc(), exit_code=proc.returncode,
               stdout_bytes=len(out), stderr_bytes=len(err),
               stdout_sha256=sha(out), stderr_sha256=sha(err))
    write(directory/'record.json', rec)
    print(json.dumps({'label':label,'pid':proc.pid,'exit':proc.returncode,
                      'stdout_sha256':sha(out),'stderr_sha256':sha(err)}), flush=True)
    return rec

def prepare():
    before = {'observed_utc':utc(), 'immutable_science_head':'5cc1602c05d79502defb07cec7027963149494d2',
              'package':str(PACKAGE), 'files':inventory(PACKAGE)}
    write(HERE/'PACKAGE_BEFORE.json', before)
    shutil.copytree(PACKAGE, HERE/'disposable_package')
    with zipfile.ZipFile(PACKAGE/'blaschke-bloch-verification-v1.zip') as archive:
        names=archive.namelist()
        rows=[]
        issues=[]
        for info in archive.infolist():
            path=pathlib.PurePosixPath(info.filename)
            body=archive.read(info.filename)
            local=PACKAGE / info.filename
            equal=local.is_file() and local.read_bytes()==body
            rows.append({'path':info.filename,'bytes':len(body),'sha256':sha(body),
                         'equal_to_current_local_member':equal})
            if path.is_absolute() or '..' in path.parts or not equal:
                issues.append(info.filename)
        write(HERE/'ARCHIVE_CHECK.json',{'observed_utc':utc(),'member_count':len(names),
               'duplicates':len(names)-len(set(names)), 'issues':issues,'members':rows})
    (HERE/'rendered').mkdir()
    execute('manifest_initial',[sys.executable,'-E','-B','manifest.py','--verify'],HERE/'disposable_package')
    execute('replay_current',[sys.executable,'-E','-B','run_verification.py'],HERE/'disposable_package')
    execute('reject_optimized',[sys.executable,'-O','-E','-B','run_verification.py'],HERE/'disposable_package')
    execute('pdfinfo',['/opt/homebrew/bin/pdfinfo',str(PACKAGE/'note.pdf')])
    execute('render_pdf',['/opt/homebrew/bin/pdftoppm','-r','110','-png',str(PACKAGE/'note.pdf'),str(HERE/'rendered'/'page')])
    execute('extract_pdf',['/opt/homebrew/bin/pdftotext','-layout',str(PACKAGE/'note.pdf'),str(HERE/'note_pdf_extracted.txt')])
    write(HERE/'PACKAGE_AFTER_PREPARE.json',{'observed_utc':utc(),'unchanged':inventory(PACKAGE)==before['files'],'files':inventory(PACKAGE)})

if __name__=='__main__':
    prepare()
