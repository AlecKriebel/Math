from pathlib import Path
import json,hashlib,datetime
P=Path(__file__).resolve().parent.parent
F=P/'publicfiles'
m=F/'PAYLOAD_MANIFEST.json'
d=json.loads(m.read_text())
for e in d['files']:
 p=F/e['file']; e['bytes']=p.stat().st_size; e['sha256']=hashlib.sha256(p.read_bytes()).hexdigest()
m.write_text(json.dumps(d,indent=2,sort_keys=True)+'\n')
with (P/'private_notes/RESEARCH_LOG.md').open('a') as f:
 f.write('\n'+datetime.datetime.now(datetime.timezone.utc).isoformat()+' - Initial assembled suite: 6 positive exits0 and 6 arithmetic false exits1; normal/-O streams agree. Export/render found one long preprint token extending a line on page1; wording shortened without content change. All five initial pages visually read. Fresh final rerun follows note-byte change. Preparation estimate70%; mathematics100%; historical priority unresolved.\n')
