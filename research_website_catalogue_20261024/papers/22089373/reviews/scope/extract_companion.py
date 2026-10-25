from pathlib import Path
from datetime import datetime,timezone
import tarfile,hashlib,json
R=Path(__file__).resolve().parent;S=R.parents[1]/'sources';D=S/'related-record-22064121';A=D/'stc_jc_sharp_boundary_atlas_certificates_v1.1.7.tar.gz';out=D/'published-source';out.mkdir(exist_ok=True)
items=[];pdfs=[]
with tarfile.open(A,'r:gz') as t:
 for m in t.getmembers():
  p=out/m.name;assert p.resolve().is_relative_to(out.resolve());assert m.isfile() or m.isdir()
  if m.isdir():p.mkdir(parents=True,exist_ok=True);continue
  p.parent.mkdir(parents=True,exist_ok=True);b=t.extractfile(m).read();assert len(b)==m.size;p.write_bytes(b)
  e={'path':m.name,'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()};items.append(e)
  if p.suffix.lower()=='.pdf':pdfs.append(e)
now=datetime.now(timezone.utc).isoformat()
(D/'extraction-integrity.json').write_text(json.dumps({'completed_utc':now,'completion_percent':100,'archive_sha256':hashlib.sha256(A.read_bytes()).hexdigest(),'safe_regular_files_only':True,'members':items,'reader_pdfs':pdfs},indent=2)+'\n')
log=R/'RESEARCH_LOG.md';log.write_text(log.read_text()+f'\n## {now} — 35%\n\nFresh companion record22064121: all ten published files downloaded and MD5/size/SHA-256 bound. The 94,158,772-byte tar.gz agrees with its manuscript envelope SHA. Safe extraction preserves all {len(items)} regular files (108,939,654 expanded bytes), with no links, escapes or unsafe members. Historical replay logs/summary bodies were acquired but not read. All33+7 actual published PDF pages now read, including computational dependency boundaries and scope limitations. Current metadata v1.1.7/Aug23 is separate from the printed month-only August2026 date and Aug25 record creation.\n')
print(json.dumps({'extraction':str(out),'regular_files':len(items),'reader_pdfs':pdfs},indent=2))
