from pathlib import Path
from urllib.request import Request,urlopen
from concurrent.futures import ThreadPoolExecutor
import json,struct,hashlib,zlib,datetime,subprocess
base=Path(__file__).resolve().parent;cache=base/'reading-cache'
now=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat()
def get(url,a,b):
 with urlopen(Request(url,headers={'Range':f'bytes={a}-{b}','User-Agent':'Research catalogue verification'}),timeout=60) as r:
  assert r.status==206 and r.headers.get('Content-Range','').startswith(f'bytes {a}-{b}/');d=r.read(b-a+2);assert len(d)==b-a+1;return d
wanted={21753405:('universal_simultaneous_amplification/output/pdf/no_universal_death_birth_amplifier.pdf','universal_simultaneous_amplification/paper/main.tex'),21850042:('paper_lower_threshold/output/pdf/simultaneous_amplification_below_three_halves.pdf',),21852072:('paper_hybrid_threshold/output/pdf/simultaneous_amplification_beyond_three_halves.pdf',)}
rows=json.load(open(base/'prior_archive_interface_ledger.json'))
for row in rows:
 rid=row['record_id'];members=json.load(open(cache/f'{rid}-central.json'));out=[]
 for end in wanted[rid]:
  hits=[m for m in members if m['name'].endswith(end)];assert len(hits)==1;m=hits[0];head=get(row['url'],m['local_offset'],m['local_offset']+29);h=struct.unpack('<4s5H3L2H',head);assert h[0]==b'PK\x03\x04';a=m['local_offset']+30+h[-2]+h[-1];raw=get(row['url'],a,a+m['compressed_bytes']-1);data=zlib.decompress(raw,-15) if m['method']==8 else raw;assert len(data)==m['bytes'] and zlib.crc32(data)==m['crc32'];p=cache/f'{rid}-{Path(m["name"]).name}';p.write_bytes(data)
  out.append({'archive_member':m['name'],'local_cache_path':str(p),'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),'zip_crc32_match':True,'compressed_bytes':m['compressed_bytes'],'retrieved_utc':now()})
  if p.suffix=='.pdf':subprocess.run(['pdftotext','-layout',str(p),str(p.with_suffix('.txt'))],check=True)
 row['selected_interfaces']=out
(base/'prior_archive_interface_ledger.json').write_text(json.dumps(rows,indent=2)+'\n')
items=[('svoboda2024si','https://journals.plos.org/ploscompbiol/article/file?id=10.1371/journal.pcbi.1012008.s001&type=supplementary'),('brewster2026','https://drops.dagstuhl.de/storage/00lipics/lipics-vol362-itcs2026/LIPIcs.ITCS.2026.29/LIPIcs.ITCS.2026.29.pdf')]
rows=json.load(open(base/'primary_acquisition_ledger.json'))
for name,url in items:
 try:
  with urlopen(Request(url,headers={'User-Agent':'Research catalogue verification'}),timeout=60) as r:data=r.read();typ=r.headers.get('Content-Type');final=r.url
  assert data.startswith(b'%PDF');p=cache/(name+'.pdf');p.write_bytes(data);subprocess.run(['pdftotext','-layout',str(p),str(p.with_suffix('.txt'))],check=True)
  rows.append({'id':name,'url':url,'resolved_url':final,'retrieved_utc':now(),'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),'local_cache_path':str(p),'content_type':typ,'status':'acquired'})
 except Exception as e:rows.append({'id':name,'url':url,'status':'failed','error':str(e),'retrieved_utc':now()})
(base/'primary_acquisition_ledger.json').write_text(json.dumps(rows,indent=2)+'\n')
print(json.dumps(rows[-2:],indent=2));print('Prior interfaces acquired')
