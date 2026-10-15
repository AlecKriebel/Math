#!/usr/bin/env python3
"""Rebuild the assigned archive using its authenticated current source tree."""
from pathlib import Path
import datetime,hashlib,json,os,shutil,subprocess,sys,zipfile
HERE=Path(__file__).resolve().parent
AUDIT=HERE.parents[1]
def main():
 target=HERE/'tmp/rebuild_audit';pub=target/'publication';pub.mkdir(parents=True)
 archive=AUDIT/'publication/bounded-region-fermions-source-verification-v1.0.zip'
 publication_roots={'note.tex','README.md','requirements.txt','verify_package.py','run_checked.py','copy_guard_challenge.py'}
 prefix='unsolved_math_prioritization/attempts/30006191/bounded_region_v2/'
 with zipfile.ZipFile(archive) as z:
  for name in z.namelist():
   if name=='PACKAGE_MANIFEST.json':continue
   if name.startswith('original_packet/'):
    dest=target/'original'/prefix/name.removeprefix('original_packet/')
    source=AUDIT/'original'/prefix/name.removeprefix('original_packet/')
   elif name=='note.pdf':dest=pub/'output/pdf/note.pdf';source=AUDIT/'publication/output/pdf/note.pdf'
   elif name in publication_roots:dest=pub/name;source=AUDIT/'publication'/name
   else:dest=target/name;source=AUDIT/name
   if source.read_bytes()!=z.read(name):raise RuntimeError('current source differs '+name)
   dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(source,dest)
 shutil.copyfile(AUDIT/'publication/build_package.py',pub/'build_package.py')
 env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',TMPDIR=str(HERE/'tmp'))
 p=subprocess.run([sys.executable,'-I','-B',str(pub/'build_package.py')],env=env,capture_output=True,text=True,timeout=60)
 if p.returncode:raise RuntimeError(p.stderr)
 result=json.loads(p.stdout)
 rebuilt=pub/archive.name
 if rebuilt.read_bytes()!=archive.read_bytes():raise RuntimeError('archive rebuild bytes differ')
 result.update(status='PASS',utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
   deterministic_archive_bytes_identical=True,build_input_current_source_bytes_independently_matched=True,
   original_candidate_untouched=True)
 (HERE/'ARCHIVE_REBUILD_RECEIPT.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':main()
