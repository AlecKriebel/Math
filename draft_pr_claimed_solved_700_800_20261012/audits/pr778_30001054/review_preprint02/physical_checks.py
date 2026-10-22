"""Independent physical source/output guards and same-six relocation rebuilds.

Usage: python -B physical_checks.py source-dir supplied-pdf pin-json scratch-dir
All mutations are made in disposable copies beneath the given scratch directory.
"""
from pathlib import Path
import hashlib,json,os,shutil,stat,subprocess,sys,tempfile,datetime

source,pdf,pins_path,scratch=map(Path,sys.argv[1:])
pins=json.loads(pins_path.read_text())['six']
runtimes=['/opt/homebrew/bin/python3','/Users/alec/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3']

def need(condition,message):
    if not condition:raise RuntimeError(message)

def snap(root):
    out={}
    if not root.exists():return out
    for p in sorted(root.rglob('*')):
        m=p.lstat().st_mode;n=p.relative_to(root).as_posix()
        if stat.S_ISREG(m):out[n]=['file',len(p.read_bytes()),hashlib.sha256(p.read_bytes()).hexdigest()]
        elif stat.S_ISLNK(m):out[n]=['symlink',os.readlink(p)]
        elif stat.S_ISDIR(m):out[n]=['directory']
        elif stat.S_ISFIFO(m):out[n]=['fifo']
        else:out[n]=['special',stat.S_IFMT(m)]
    return out

before=snap(source);pdf_before=pdf.read_bytes();rows=[]

def invoke(py,opt,script,args):
    cmd=[py,'-B']+(['-O'] if opt else [])+[str(script)]+list(map(str,args))
    p=subprocess.run(cmd,cwd='/',capture_output=True,timeout=180)
    return {'command':cmd,'returncode':p.returncode,'stdout_sha256':hashlib.sha256(p.stdout).hexdigest(),'stderr':p.stderr.decode()}

for py in runtimes:
    for opt in [False,True]:
        with tempfile.TemporaryDirectory(prefix='review02-relocation-',dir=scratch) as td:
            base=Path(td);moved=base/'relocated closed source with spaces';shutil.copytree(source,moved)
            for p in moved.rglob('*'):
                if p.is_file():os.utime(p,(1000000000,1000000000))
            q=invoke(py,opt,moved/'verify_bundle.py',['--integrity-only','--pdf',pdf])
            need(q['returncode']==0,'relocated integrity: '+q['stderr']);rows.append({'case':'relocation_changed_mtimes','runtime':py,'optimized':opt,**q})
            q=invoke(py,opt,moved/'build_package.py',['--pdf',pdf,'--output-dir',base/'rebuilt'])
            need(q['returncode']==0,'rebuild: '+q['stderr'])
            exact={n:{'bytes':len((base/'rebuilt'/n).read_bytes()),'sha256':hashlib.sha256((base/'rebuilt'/n).read_bytes()).hexdigest()} for n in pins}
            need(exact==pins,'six rebuilt bytes differ')
            need(snap(moved)==before,'relocation rebuild altered source')
            rows.append({'case':'same_six_rebuild','runtime':py,'optimized':opt,'six':exact,**q})
        for case in ['hidden_extra','missing','altered','symlink','fifo','empty_directory']:
            with tempfile.TemporaryDirectory(prefix='review02-source-negative-',dir=scratch) as td:
                moved=Path(td)/'source';shutil.copytree(source,moved)
                p=moved/'paper.tex'
                if case=='hidden_extra':(moved/'.unexpected').write_text('extra\n')
                elif case=='missing':p.unlink()
                elif case=='altered':p.write_bytes(p.read_bytes()+b'\nchanged\n')
                elif case=='symlink':p.unlink();p.symlink_to(moved/'README.md')
                elif case=='fifo':os.mkfifo(moved/'unexpected.fifo')
                elif case=='empty_directory':(moved/'unexpected-empty').mkdir()
                mutated=snap(moved)
                q=invoke(py,opt,moved/'verify_bundle.py',['--integrity-only','--pdf',pdf])
                need(q['returncode']!=0,'source corruption accepted: '+case)
                need('ValueError:' in q['stderr'],'not a source-guard rejection: '+case)
                need(snap(moved)==mutated,'reject altered input: '+case)
                rows.append({'case':'source_'+case,'runtime':py,'optimized':opt,**q})
        cases=['inside_source','ancestor_symlink','nested_ancestor_symlink','tex_destination_symlink','pdf_destination_symlink','inventory_destination_symlink','fifo_destination','directory_destination','pdf_hardlink','source_hardlink','ordinary_output_hardlink','source_zip_symlink']
        for case in cases:
            with tempfile.TemporaryDirectory(prefix='review02-output-negative-',dir=scratch) as td:
                base=Path(td);moved=base/'source';shutil.copytree(source,moved);out=base/'out';out.mkdir()
                if case=='inside_source':out=moved/'inside'
                elif case=='ancestor_symlink':(base/'real').mkdir();out=base/'linked'/'child';(base/'linked').symlink_to(base/'real',target_is_directory=True)
                elif case=='nested_ancestor_symlink':(base/'real').mkdir();(out/'output').symlink_to(base/'real',target_is_directory=True)
                elif case.endswith('destination_symlink'):
                    target={'tex_destination_symlink':'paper.tex','pdf_destination_symlink':'output/pdf/paper.pdf','inventory_destination_symlink':'PACKAGE_INVENTORY.json'}[case]
                    p=out/target;p.parent.mkdir(parents=True,exist_ok=True);p.symlink_to(pdf)
                elif case=='source_zip_symlink':(out/'source-and-verification.zip').symlink_to(pdf)
                elif case=='fifo_destination':os.mkfifo(out/'source-and-verification.zip')
                elif case=='directory_destination':(out/'source-and-verification.zip').mkdir()
                elif case=='pdf_hardlink':p=out/'output/pdf/paper.pdf';p.parent.mkdir(parents=True);os.link(pdf,p)
                elif case=='source_hardlink':os.link(moved/'paper.tex',out/'paper.tex')
                elif case=='ordinary_output_hardlink':(base/'unrelated').write_text('preserve\n');os.link(base/'unrelated',out/'paper.tex')
                initial=snap(base)
                q=invoke(py,opt,moved/'build_package.py',['--pdf',pdf,'--output-dir',out])
                need(q['returncode']!=0,'output guard accepted: '+case)
                need('ValueError:' in q['stderr'],'not a builder-guard rejection: '+case)
                need(snap(base)==initial,'builder wrote before failed batch preflight: '+case)
                rows.append({'case':'output_'+case,'runtime':py,'optimized':opt,**q})
need(snap(source)==before and pdf.read_bytes()==pdf_before,'review changed supplied inputs')
print(json.dumps({'status':'PASS','at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'physical_source_negatives':24,'physical_output_negatives':48,'relocation_positives':4,'same_six_rebuilds':4,'closed_input_and_pdf_unchanged':True,'checks':rows},indent=2))
