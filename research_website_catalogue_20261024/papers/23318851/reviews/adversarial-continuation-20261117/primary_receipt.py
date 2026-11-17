"""Passive primary-file byte receipt; no imported code or mathematical execution."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
P=Path('/Users/alec/Documents/Math/research_website_catalogue_20261024')
A=P/'papers/23318851/reviews/adversarial-continuation-20261117'
N=P/'papers/23318851/sources/archives/02-gram_locus_support.zip.extracted'
names={'Seigal2018':'Seigal2018.pdf','HSS2003':'HSSv2.pdf','Bravyi2003/2004':'Bravyiv1.pdf',
    'Sinn2011':'Sinnv1.pdf','DSL2017published':'DSLpublished.pdf','OWR20/2017':'OWR2017.pdf'}
source=json.loads((N/'SOURCE_LOCATORS.json').read_text())
rows=[]
for r in source['sources']:
    if r['source'] not in names:continue
    p=A/'primary'/names[r['source']];b=p.read_bytes();h=hashlib.sha256(b).hexdigest()
    assert h==r['SHA256'],r['source']
    rows.append({'source':r['source'],'path':str(p.relative_to(A)),'URL':r['URL'],
        'bytes':len(b),'SHA256':h,'matches_declared_source_pin':True,
        'equivalent_fetch_argv':['curl','--fail','--location','--silent','--show-error',r['URL'],'-o',str(p)],
        'fetch_exit':0,'fetch_stdout_stderr':'no diagnostics observed',
        'timing_limit':'Exact per-fetch UTC not separately captured; successful literal commands/exits are in tool transcript'})
assert len(rows)==6
out={'UTC':datetime.now(timezone.utc).isoformat(),'primary_files':rows,
    'actual_read_scope':'EXPOSURE_AND_PRIMARY_LEDGER.md','source_locator_read_scope_claims_adopted':False,
    'native_route':'NATIVE_RUN.json','additional_scientific_execution':0}
assert not (A/'PRIMARY_RECEIPT.json').exists()
(A/'PRIMARY_RECEIPT.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'primary_files':len(rows),'all_declared_pins_exact':True}))
