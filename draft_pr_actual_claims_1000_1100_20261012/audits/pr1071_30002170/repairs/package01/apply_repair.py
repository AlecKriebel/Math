from pathlib import Path
import json,hashlib,shutil,datetime,difflib
r=Path('/Users/alec/Documents/Math/draft_pr_actual_claims_1000_1100_20261012/audits/pr1071_30002170');p=r/'NEWpreprint_v1_0';e=r/'repairs/package01'
def write(n,s): (p/n).write_text(s)
write('scripts/package_paths.py','''"""Static filesystem policy for frozen members and fresh external outputs.

Outputs must not exist (including dangling symlinks). Their parent must be an
existing real directory outside the package, with no symlink ancestors. A new
output directory is empty before any copy, log or trusted subprocess write.
This is a static local preflight, not a concurrent filesystem race guarantee.
"""
import os, stat
from pathlib import Path, PurePosixPath
ROOT = Path(__file__).resolve().parents[1]
def require(ok, message):
    if not ok:
        raise RuntimeError(message)
def safe_path(root, name):
    require(isinstance(name, str) and bool(name), 'Invalid member name.')
    parts = name.split('/')
    require(not PurePosixPath(name).is_absolute() and all(x not in ('', '.', '..') for x in parts) and '\\\\' not in name, 'Unsafe member name: ' + name)
    base = Path(root).resolve()
    current = base
    for i, part in enumerate(parts):
        current = current / part
        require(not current.is_symlink(), 'Symlink member/ancestor: ' + name)
        require(current.exists(), 'Missing member/ancestor: ' + name)
        mode = current.stat().st_mode
        require(stat.S_ISREG(mode) if i == len(parts)-1 else stat.S_ISDIR(mode), 'Nonregular member or nondirectory ancestor: ' + name)
    require(current.resolve().is_relative_to(base), 'Escaping member: ' + name)
    return current

def fresh_output(path, root=ROOT):
    """Return a preflighted absent file/directory; no mkdir or write occurs."""
    target = Path(os.path.abspath(os.fspath(path)))
    require(not target.exists() and not target.is_symlink(), 'Output must be new; existing files/directories, symlinks and hardlinks are rejected: ' + str(target))
    parent = target.parent
    require(parent.exists() and parent.is_dir(), 'Output parent must already exist: ' + str(parent))
    for ancestor in (parent, *parent.parents):
        require(not ancestor.is_symlink(), 'Symlink output ancestor: ' + str(ancestor))
        require(ancestor.is_dir(), 'Output ancestor is not a directory: ' + str(ancestor))
    require(not target.is_relative_to(Path(root).resolve()) and not target.resolve().is_relative_to(Path(root).resolve()), 'Output must be outside all frozen package descendants.')
    return target
''')
v=(p/'scripts/verify_package.py').read_text();v=v.replace('import argparse,hashlib,json,zipfile','import argparse,hashlib,json,zipfile,sys\nsys.dont_write_bytecode=True');a=v.index('def safe_path(');b=v.index('def verify(',a);v=v[:a]+'''from package_paths import safe_path

def validate_citation(root, metadata):
    text=safe_path(root,'CITATION.txt').read_text(encoding='utf-8')
    lines=text.splitlines()
    require(len(lines)==11 and lines[0]=='Scholarly citation (plain UTF-8; not CFF)', 'Citation format drift.')
    values={}
    for line in lines[1:]:
        require(': ' in line, 'Malformed citation field.')
        key,value=line.split(': ',1)
        require(key not in values and value, 'Duplicate/empty citation field.')
        values[key]=value
    expected={'Author':'Alec Kriebel','Title':metadata['title'],'Kind':'Unrefereed research note (preprint)','Version':'1.0','Date':'2026-10-14','Affiliation':'Independent Researcher','ORCID':'https://orcid.org/'+metadata['creators'][0]['orcid'],'License':'CC BY 4.0','Attribution':'Attributed witness proof; historical and method priority, full novelty, and worldwide current-open status UNKNOWN.','Review':'Extensive AI assistance; no human peer review or formal certification.'}
    require(values==expected, 'Scholarly citation fields differ from reviewed paper/metadata.')
    require(not (root/'CITATION.cff').exists() and not (root/'CITATION.cff').is_symlink(), 'Invalid historical CFF must not be an active root citation.')
    return values
''' + v[b:]
v=v.replace("manifest=json.loads((root/'PACKAGE_MANIFEST.json').read_text());members=manifest['members']", "root=Path(root).resolve()\n    manifest=json.loads(safe_path(root,'PACKAGE_MANIFEST.json').read_text());members=manifest['members']")
v=v.replace("metadata=json.loads((root/'metadata.json').read_text())", "metadata=json.loads(safe_path(root,'metadata.json').read_text())")
v=v.replace("json.loads((root/'metadata_wrapped.json').read_text())", "json.loads(safe_path(root,'metadata_wrapped.json').read_text())").replace("json.loads((root/'deposit.json').read_text())", "json.loads(safe_path(root,'deposit.json').read_text())").replace("json.loads((root/'STATUS.json').read_text())", "json.loads(safe_path(root,'STATUS.json').read_text())").replace("json.loads((root/'INPUT_COPY_MAP.json').read_text())", "json.loads(safe_path(root,'INPUT_COPY_MAP.json').read_text())")
v=v.replace("for r in json.loads(safe_path(root,'INPUT_COPY_MAP.json').read_text())['copies']:", "validate_citation(root,metadata)\n    current=json.loads(safe_path(root,'CURRENT_STATUS.json').read_text())\n    require(current['state']=='PENDING_NEW_WHOLE_02' and current['fresh_whole_package_reviews_completed']==1 and current['minimum_fresh_reviews_required']==2, 'Current review state drift.')\n    require(current['publication_ready'] is False and current['issues_resolved'] is False and current['published'] is False and current['services_held_at_pr']==1032, 'Premature current promotion.')\n    for r in json.loads(safe_path(root,'INPUT_COPY_MAP.json').read_text())['copies']:")
v=v.replace("if selected.exists():", "if selected.exists() or selected.is_symlink():\n        require(selected.is_file() and not selected.is_symlink(),'Present bindings must be a regular nonsymlink file.')")
v=v.replace("b=json.loads(selected.read_text());pdf=root/b['pdf']['filename'];require(pdf.is_file()", "b=json.loads(selected.read_text());pdf=safe_path(root,b['pdf']['filename']);require(pdf.is_file()")
v=v.replace("require(ap.is_file(),'Present bindings require a readable archive.')", "require(ap.is_file() and not ap.is_symlink(),'Present bindings require a regular nonsymlink archive.')")
write('scripts/verify_package.py',v)
b=(p/'scripts/build_archive.py').read_text();b=b.replace('from verify_package import ROOT,verify','from verify_package import ROOT,verify\nfrom package_paths import fresh_output,safe_path');b=b.replace("verify(bindings=ROOT/'__absent_binding__')","output=fresh_output(a.out)\nverify(bindings=ROOT/'__absent_binding__')");b=b.replace("manifest=json.loads((ROOT/'PACKAGE_MANIFEST.json').read_text())","manifest=json.loads(safe_path(ROOT,'PACKAGE_MANIFEST.json').read_text())");start=b.index('if a.out.resolve()');end=b.index('with zipfile.ZipFile',start);b=b[:start]+b[end:];b=b.replace("zipfile.ZipFile(a.out,'w'","zipfile.ZipFile(output,'w'").replace("(ROOT/name).read_bytes()","safe_path(ROOT,name).read_bytes()");write('scripts/build_archive.py',b)
c=(p/'scripts/check.py').read_text();c=c.replace('from pathlib import Path','sys.dont_write_bytecode=True\nfrom pathlib import Path\nfrom package_paths import fresh_output,safe_path');c=c.replace('out.mkdir(parents=True,exist_ok=True)','out=fresh_output(out,root)\n    out.mkdir()');c=c.replace("json.loads((root/'INPUT_COPY_MAP.json').read_text())","json.loads(safe_path(root,'INPUT_COPY_MAP.json').read_text())").replace("src=root/row['package_copy']","src=safe_path(root,row['package_copy'])");c=c.replace("subprocess.run([sys.executable,*flags,str(checker)],capture_output=True,text=True)","subprocess.run([sys.executable,*flags,str(checker)],capture_output=True,text=True,cwd=dest)")
c=c.replace("require(args.out.resolve()!=root,'Use an output directory separate from frozen package contents.');run(args.out.resolve())", "run(args.out)");c=c.replace("with tempfile.TemporaryDirectory(prefix='pr1071-finite-') as d:run(Path(d))", "with tempfile.TemporaryDirectory(prefix='pr1071-finite-',dir=Path(tempfile.gettempdir()).resolve()) as d:run(Path(d)/'result')");write('scripts/check.py',c)
d=(p/'scripts/build_pdf.py').read_text().replace('import argparse, os, shutil, subprocess','import argparse, os, shutil, subprocess, sys\nsys.dont_write_bytecode=True').replace('from pathlib import Path','from pathlib import Path\nfrom package_paths import fresh_output,safe_path');d=d.replace('dest=a.out.resolve()', 'dest=fresh_output(a.out,root)');d=d.replace("if dest==root:raise SystemExit('Use a separate output directory.')\ndest.mkdir(parents=True,exist_ok=True)","dest.mkdir()");d=d.replace("shutil.copyfile(root/'paper.tex',source)","shutil.copyfile(safe_path(root,'paper.tex'),source)");d=d.replace('env=env,text=True,capture_output=True)', 'env=env,text=True,capture_output=True,cwd=dest)');write('scripts/build_pdf.py',d)
write('CITATION.txt', '''Scholarly citation (plain UTF-8; not CFF)
Author: Alec Kriebel
Title: A localized Gaussian-witness lower bound for fractional iterated area on uniform grids
Kind: Unrefereed research note (preprint)
Version: 1.0
Date: 2026-10-14
Affiliation: Independent Researcher
ORCID: https://orcid.org/0009-0001-9320-500X
License: CC BY 4.0
Attribution: Attributed witness proof; historical and method priority, full novelty, and worldwide current-open status UNKNOWN.
Review: Extensive AI assistance; no human peer review or formal certification.
''')
(p/'CITATION.cff').unlink()
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
write('CURRENT_STATUS.json',json.dumps({'utc':now,'state':'PENDING_NEW_WHOLE_02','pr':1071,'fresh_whole_package_reviews_completed':1,'minimum_fresh_reviews_required':2,'publication_ready':False,'issues_resolved':False,'published':False,'services_held_at_pr':1032,'meaning':'Bounded repair addresses three whole01 P3 findings. Original STATUS/FINAL_VERIFICATION/preparation pins remain dated historical stages; a new complete whole02 review is required.'},indent=2)+'\n')
read=(p/'README.md').read_text();read=read.replace('STATUS.json records the dated preparation state. This frozen version awaits at least two fresh whole-package reviews;','STATUS.json retains the dated original preparation state. CURRENT_STATUS.json records the repaired package: one fresh whole review completed, three P3 findings repaired, and a NEW complete whole02 review required;')
read=read.replace('Generated outputs are deliberately outside the extracted frozen package.','Generated outputs must be new and outside every descendant of the extracted frozen package. Their parent must already exist and have no symlink ancestors. Existing output files/directories are rejected, including symlinks, dangling links and hardlink aliases. Use a new directory/file for every run. This static local preflight covers the entire new checker/compiler directory, including subprocess files, logs and receipts; it does not promise safety under concurrent filesystem changes.')
read+= '''\n## Repaired support interfaces and citation\n\nCITATION.txt is a validated plain UTF-8 scholarly citation of the research note; the mathematical paper is not classified as software or a dataset. The invalid original CFF (root `type: unpublished`, outside CFF 1.2.0's software/dataset enum) is preserved exactly as history/preparation01/CITATION.cff.invalid.txt and is not an active citation file. The official schema is https://raw.githubusercontent.com/citation-file-format/citation-file-format/1.2.0/schema.json . The verifier parses the plain fields and requires their exact agreement with the reviewed author/title/ORCID/version/date and attribution.\n\nEvery manifest/member file is required to be present, regular, nonsymlink and reached only through real directory ancestors inside the package, including the self-hash-excluded manifest BEFORE JSON parsing. The default absent-binding path and strict present/required binding checks remain available. The original preparation's pin manifest and dated reports remain unchanged. history/preparation01/ resolves exact before bytes of changed outputs; WHOLE01_COPY_EXCLUSIONS.json names individually omitted raw streams/private/generated files. These historical artifacts retain their earlier meanings and are superseded by CURRENT_STATUS.json for current workflow status.\n'''
write('README.md',read)
s=(p/'SUPPLEMENT.md').read_text();s+='''\nBounded package repair (14 October 2026 UTC): CURRENT_STATUS.json records one completed fresh whole review and the requirement for a NEW whole02 review. The original preparation status and hash records remain unchanged history. All generating commands require absent output names outside the package, existing real parent directories, and no symlink ancestors; all generated child files therefore start in a new empty external directory. The original checker itself is unchanged. This is a static local-filesystem rule, without concurrent race claims. The bootstrap manifest and all ordinary members share regular/nonsymlink/ancestry checks before parsing or writing. CITATION.txt supplies the current plain scholarly citation, with explicit parser checks; the original invalid root-enum CFF is historical text only. The analytic paper, PDF and all three bibliographic metadata objects are unchanged.\n''';write('SUPPLEMENT.md',s)
# Append exact safe whole01 custody; omit only individually recorded raw/private products.
cp=json.loads((e/'before/INPUT_COPY_MAP.json').read_text());added=[];excluded=[]
rev=r/'reviews/package_01';pins=json.loads((rev/'OUTPUT_PINS.json').read_text())['files']
for rec in pins:
 n=rec['path'];q=rev/n
 if q.suffix=='.txt' or n in ['paper.log.txt']:
  excluded.append({'path':'reviews/package_01/'+n,'bytes':q.stat().st_size,'sha256':hashlib.sha256(q.read_bytes()).hexdigest(),'reason':'Generated compiler/checker raw stream, log or extracted text; excluded individually, not needed for authored finding/evidence.'});continue
 dest='custody/reviews/package_01/'+n;d=p/dest;d.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(q,d);added.append({'original_path':'reviews/package_01/'+n,'package_copy':dest,'bytes':q.stat().st_size,'sha256':hashlib.sha256(q.read_bytes()).hexdigest(),'byte_exact':True})
for n in ['OUTPUT_PINS.json','SEAL.json']:
 q=rev/n;dest='custody/reviews/package_01/'+n;d=p/dest;d.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(q,d);added.append({'original_path':'reviews/package_01/'+n,'package_copy':dest,'bytes':q.stat().st_size,'sha256':hashlib.sha256(q.read_bytes()).hexdigest(),'byte_exact':True})
n='ROOT_WHOLE_PACKAGE_REVIEW_01.json';q=r/n;dest='custody/'+n;shutil.copyfile(q,p/dest);added.append({'original_path':n,'package_copy':dest,'bytes':q.stat().st_size,'sha256':hashlib.sha256(q.read_bytes()).hexdigest(),'byte_exact':True})
write('WHOLE01_COPY_EXCLUSIONS.json',json.dumps({'utc':now,'scope':'Individual exclusions from whole01 terminal OUTPUT_PINS; safe authored findings/reports/results/code copied unchanged.','records':excluded},indent=2)+'\n')
# Exact changed-preparation history; map sources to snapshots for historical current locators.
for q in sorted((e/'before').rglob('*')):
 if not q.is_file() or q.suffix=='.zip' or q.name.endswith('.sha256'):continue
 n=q.relative_to(e/'before').as_posix();dest='history/preparation01/'+('CITATION.cff.invalid.txt' if n=='CITATION.cff' else n);d=p/dest;d.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(q,d);added.append({'original_path':'NEWpreprint_v1_0/'+n,'source_snapshot':'repairs/package01/before/'+n,'package_copy':dest,'bytes':q.stat().st_size,'sha256':hashlib.sha256(q.read_bytes()).hexdigest(),'byte_exact':True,'meaning':'Exact before-repair historical bytes; historical invalid CFF retained as text only.'})
cp['copies']+=added;cp['scope']+='; append unchanged safe whole01 outputs/root adoption and exact changed-preparation history. source_snapshot resolves prior locator before bytes.';write('INPUT_COPY_MAP.json',json.dumps(cp,indent=2)+'\n')
# Original 92 output-pin manifest stays untouched; ensure every changed old pin resolves to saved before bytes.
old=json.loads((p/'INPUT_OUTPUT_PINS.json').read_text())['records'];res=[]
for z in old:
 q=p/z['path'];matching=q.is_file() and hashlib.sha256(q.read_bytes()).hexdigest()==z['sha256']
 before=e/'before'/z['path']
 if not matching:
  if not before.is_file():raise RuntimeError('Missing before for '+z['path'])
  if hashlib.sha256(before.read_bytes()).hexdigest()!=z['sha256']:raise RuntimeError('Before mismatch '+z['path'])
 res.append(dict(z,current_unchanged=matching,before_bytes_path_relative_to_audit=None if matching else before.relative_to(r).as_posix()))
(e/'PREPARATION_92_PIN_RESOLUTION.json').write_text(json.dumps({'utc':now,'records':res},indent=2)+'\n')
(e/'CFF_PRIMARY_EVIDENCE.json').write_text(json.dumps({'utc':now,'official_source':'https://raw.githubusercontent.com/citation-file-format/citation-file-format/1.2.0/schema.json','local_schema':'reviews/package_01/private/cff_schema_1_2_0.json','schema_sha256':hashlib.sha256((rev/'private/cff_schema_1_2_0.json').read_bytes()).hexdigest(),'root_enum':json.loads((rev/'private/cff_schema_1_2_0.json').read_text())['properties']['type']['enum'],'old_root_type':'unpublished','repair':'Plain UTF-8 scholarly citation; no CFF schema assertion for plain text; exact fields parsed and checked.'},indent=2)+'\n')
print(json.dumps({'copies':len(cp['copies']),'added':len(added),'exclusions':len(excluded)}))
