"""One acquisition of each primary PDF and deterministic reading extraction."""
import datetime, hashlib, json, subprocess, time
from pathlib import Path
if not __debug__:
    raise RuntimeError('Assertions must be enabled')
OWN=Path('/Users/alec/Documents/Math/research_website_catalogue_20261024/papers/23318851/reviews/followup-ghz11-adversarial-sol')
rows=[]
sources=[('seigal2018','https://seigal.github.io/seigal2018gram.pdf',None),('ferudun','https://zenodo.org/api/records/23111048/files/OWR-15428-003-paper.pdf/content','a99172938f203f5a494c2191a73072299857ce8d3adfa6867831ca737c471cbb')]
def run(name,argv):
    started=datetime.datetime.now(datetime.timezone.utc).isoformat();tick=time.monotonic()
    with (OWN/'primary'/(name+'.stdout')).open('xb') as out,(OWN/'primary'/(name+'.stderr')).open('xb') as err:
        r=subprocess.run(argv,stdout=out,stderr=err,check=False)
    rows.append(dict(name=name,argv=argv,UTC=started,seconds=time.monotonic()-tick,exit_code=r.returncode))
    (OWN/'ACQUISITION_EXECUTIONS.json').write_text(json.dumps(rows,indent=2)+'\n')
    assert r.returncode==0,(name,r.returncode)
identities=[]
for name,url,expected in sources:
    pdf=OWN/'primary'/(name+'.pdf')
    run(name+'-fetch',['/usr/bin/curl','--fail-with-body','--location','--max-time','60','--dump-header',str(OWN/'primary'/(name+'.headers')), '--output',str(pdf),url])
    raw=pdf.read_bytes();sha=hashlib.sha256(raw).hexdigest()
    assert raw.startswith(b'%PDF-') and (expected is None or sha==expected)
    identities.append(dict(name=name,URL=url,bytes=len(raw),SHA256=sha,asserted_expected_SHA256=expected,expected_hash_matches=sha==expected if expected else None))
    (OWN/'PRIMARY_IDENTITIES.json').write_text(json.dumps(identities,indent=2)+'\n')
    run(name+'-pdfinfo',['/opt/homebrew/bin/pdfinfo',str(pdf)])
    run(name+'-extract',['/opt/homebrew/bin/pdftotext','-layout',str(pdf),str(OWN/'primary'/(name+'.txt'))])
print(json.dumps(dict(status='ACQUIRED_PRIMARY_PDFS_AND_READING_TEXT',sources=identities,commands=len(rows),all_exit_zero=True)))
