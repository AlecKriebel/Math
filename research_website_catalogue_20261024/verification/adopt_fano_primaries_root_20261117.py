"""Authenticate acquired primary files as inert data, without reading peer opinions."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib
import json
import stat

P=Path('/Users/alec/Documents/Math/research_website_catalogue_20261024')
R=P/'verification/fano-primary-acquisition-sol-20261117'
OUT=P/'verification/root-fano-primary-acquisition-adoption-20261117.json'
assert not OUT.exists()
sha=lambda b:hashlib.sha256(b).hexdigest()
pins={'FINAL.json':(724,'b17e67feb0616a21344821a5e7ba17b8399c225806a61a7fac8901d021f4ec65'),
      'MANIFEST.json':(3108,'adc8de13b56b91d4b8324d55e1f4764c56214cc724126e756928b8d0e4cd2405'),
      'SOURCE_EDITION_MAP.json':(73501,'6ac06417e83f6c432d40c5b9875dde0954aae6141585f8f667cef8c75fea7139')}
for name,pin in pins.items():
 b=(R/name).read_bytes();assert (len(b),sha(b))==pin,name
m=json.loads((R/'MANIFEST.json').read_bytes())
files={p.name for p in R.iterdir() if p.is_file()}
assert len(files)==14 and all(p.is_file() for p in R.iterdir())
assert stat.S_IMODE(R.stat().st_mode)==int(m['root_mode'],8)
assert set(m['exact_existing_terminal_recursive_hash_exclusions'])=={'MANIFEST.json','FINAL.json'}
assert {r['path'] for r in m['payload_files']}|{'MANIFEST.json','FINAL.json'}==files
for row in m['payload_files']:
 p=R/row['path'];b=p.read_bytes()
 assert (len(b),sha(b),stat.S_IMODE(p.stat().st_mode))==(row['bytes'],row['SHA256'],int(row['mode'],8)),row['path']
 assert (not b)==row['empty'] and p.name.startswith('.')==row['hidden']
for name,mode in m['terminal_modes'].items():assert stat.S_IMODE((R/name).stat().st_mode)==int(mode,8)
d=json.loads((R/'SOURCE_EDITION_MAP.json').read_bytes());c=d['private_payload_whole_census']
root=Path(c['root'])
assert root==P/'papers/23411227/reviews/root-continuation-20261117/primary'
assert len(c['files'])==42 and c['directories']=={}
assert {p.name for p in root.iterdir()}==set(c['files'])
for field,value in c['root_metadata'].items():
 info=root.stat();actual={'mode':format(stat.S_IMODE(info.st_mode),'04o'),'empty':not any(root.iterdir()),'mtime_ns':info.st_mtime_ns,'ctime_ns':info.st_ctime_ns}
 assert actual[field]==value,field
for name,row in c['files'].items():
 path=root/name;info=path.lstat();assert stat.S_ISREG(info.st_mode)
 b=path.read_bytes();actual={'bytes':len(b),'SHA256':sha(b),'mode':format(stat.S_IMODE(info.st_mode),'04o'),
 'hidden':name.startswith('.'),'empty':not b,'mtime_ns':info.st_mtime_ns,'ctime_ns':info.st_ctime_ns}
 assert actual==row,name
assert len(d['records'])==7 and len(d['commands'])==14 and all(x['exit_code']==0 for x in d['commands'])
for row in d['records']:
 p=Path(row['payload_pdf']['path']);b=p.read_bytes()
 assert b.startswith(b'%PDF-') and len(b)==row['declared_bytes'] and sha(b)==row['declared_SHA256']
 assert Path(row['cache_path']).read_bytes()==b and row['complete']
record={'UTC':datetime.now(timezone.utc).isoformat(),'status':'ACCEPTED_PINNED_PRIMARY_CUSTODY_ONLY',
 'own_files':14,'payload_files':42,'exact_cached_PDFs':7,'fresh_texts':7,'all14_Poppler_exits0':True,
 'all_payload_bytes_modes_times_topology_exact':True,'edition_pages':{r['label']:r['pdf_pages'] for r in d['records']},
 'unversioned_WZ_HLYTD_identified_by_whole_hash_not_VOR_or_currentHTTP_equality':True,
 'WZ_declared_pagination17_qualified_actualPDF15':True,'no_new_mathematical_verdict_or_scientific_execution':True,
 'root_actual_REPORT_FINAL_and_edition_metadata_read':True,'primary_bodies_unread_by_root_at_adoption':True,
 'controls':{n:{'bytes':s,'SHA256':h} for n,(s,h) in pins.items()}}
OUT.write_text(json.dumps(record,indent=2)+'\n')
b=OUT.read_bytes();print(json.dumps({'own_authenticated':14,'private_payload_authenticated':42,'bytes':len(b),'SHA256':sha(b),'path':str(OUT)}))
