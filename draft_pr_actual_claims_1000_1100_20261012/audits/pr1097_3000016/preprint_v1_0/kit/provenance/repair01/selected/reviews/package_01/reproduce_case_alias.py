#!/usr/bin/env python3
"""Disposable actual-filesystem falsification of case-alias protection."""
import sys
sys.dont_write_bytecode=True
import datetime,hashlib,json,os,shutil,subprocess,tempfile,zipfile
from pathlib import Path
R=Path(__file__).resolve().parent
P=R.parent.parent/'preprint_v1_0'

def need(q,m):
    if not q:raise ValueError(m)

def digest(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()

scratch=Path(tempfile.mkdtemp(prefix='review1097-case-alias-',dir='/private/tmp'))
rows=[]
try:
    clean=scratch/'clean';clean.mkdir()
    with zipfile.ZipFile(P/'pr1097_support_v1_0.zip') as z:z.extractall(clean)
    alias=scratch/'CLEAN'
    need(alias.is_dir() and os.path.samefile(alias,clean),'This control requires actual case-insensitive aliasing')
    baseline={p.relative_to(clean).as_posix():digest(p) for p in clean.rglob('*') if p.is_file()}
    for tag,flags in [('normal',['-B']),('optimized',['-O','-B'])]:
        for script,option,name in [('build_support.py','--out','case-alias-'+tag+'.zip'),('rebuild_pdf.py','--out-dir','case-pdf-'+tag)]:
            dest=alias/name
            argv=[sys.executable]+flags+['scripts/'+script,option,str(dest)]
            r=subprocess.run(argv,cwd=clean,capture_output=True)
            actual=clean/name
            rows.append({'mode':tag,'argv':argv,'exit_code':r.returncode,'stdout':r.stdout.decode(),'stderr':r.stderr.decode(),
                         'fresh_output_lexically_outside_kit':str(dest).startswith(str(alias)) and not str(dest).startswith(str(clean)+'/'),
                         'actual_output_created_inside_protected_kit':actual.exists(),
                         'same_existing_parent_inode':os.path.samefile(dest.parent,clean),
                         'output_is_directory':actual.is_dir(),
                         'created_file_hashes':({p.relative_to(clean).as_posix():digest(p) for p in actual.rglob('*') if p.is_file()} if actual.is_dir() else {name:digest(actual)} if actual.is_file() else {})})
            need(r.returncode==0 and actual.exists(),'The tested defect was not reproduced')
            if actual.is_dir():shutil.rmtree(actual)
            else:actual.unlink()
            need({p.relative_to(clean).as_posix():digest(p) for p in clean.rglob('*') if p.is_file()}==baseline,'Disposable clean tree did not restore exactly')
    (R/'CASE_ALIAS_FINDING.json').write_text(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'status':'REPRODUCED_ACTIONABLE_P3','candidate_or_original_modified':False,
        'cause':'fresh_output compares lexical pathlib containment; case-folding aliases share an existing parent inode but evade the KIT root comparison',
        'actual_filesystem_case_insensitive':True,'commands':rows,'temporary_outputs_removed':True},indent=2)+'\n')
finally:
    shutil.rmtree(scratch)
