from pathlib import Path,PurePosixPath
from datetime import datetime,timezone
import urllib.request,json,hashlib,zipfile,stat,subprocess
P=Path('/Users/alec/Documents/Math/research_website_catalogue_20261024/papers/23358014');S=P/'sources';R=P/'reviews/scope'
def now():return datetime.now(timezone.utc).isoformat()
def fetch(url):
 with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'IndependentResearchInventory/1.0'}),timeout=90) as f:return f.read(),f.geturl(),dict(f.headers)
def digest(b):return hashlib.sha256(b).hexdigest()
with (R/'RESEARCH_LOG.md').open('a') as f:f.write('# Intake and scope — 23358014\n\n## '+now()+' — 5%\n\nRead mandatory GOAL.md. Started fresh public acquisition against row 70 queue. Scope only: no helper execution or mathematical clearance. Preserve all prior sealed reviews and keep historical assessment bodies opaque.\n')
u='https://zenodo.org/api/records/23358014';b,res,h=fetch(u);(S/'record.json').write_bytes(b);record=json.loads(b)
expected={'critical_wave_growth.pdf':(88702,'aa742b791c3aa23961e786c94c47530a'),'critical_wave_verification.zip':(241890,'c46cf8f4d3c75cd3429f621afe8dc764')}
assert {x['key'] for x in record['files']}==set(expected)
assets=[]
for x in record['files']:
 name=x['key'];u=x['links']['self'];b,res,h=fetch(u);size,md5=expected[name]
 assert len(b)==size==x['size'] and hashlib.md5(b).hexdigest()==md5 and x['checksum']=='md5:'+md5
 if name.endswith('.pdf'):assert digest(b)=='a68d8d47dcf625f9ab8818924071200bff2b2280d67665e1e67dd7b83effe988'
 (S/name).write_bytes(b);assets.append({'name':name,'url':u,'resolved_url':res,'bytes':len(b),'md5':md5,'sha256':digest(b),'retrieved_utc':now()})
root=S/'published-source/critical_wave_verification';root.mkdir(parents=True,exist_ok=True);members=[];seen=set()
with zipfile.ZipFile(S/'critical_wave_verification.zip') as z:
 assert z.testzip() is None
 for i in z.infolist():
  path=PurePosixPath(i.filename);mode=i.external_attr>>16
  assert not path.is_absolute() and '..' not in path.parts and '\\' not in i.filename and not stat.S_ISLNK(mode) and i.filename not in seen
  seen.add(i.filename)
  assert not mode or stat.S_IFMT(mode) in (0,stat.S_IFDIR,stat.S_IFREG)
  q=root/path
  if i.is_dir():q.mkdir(parents=True,exist_ok=True);continue
  q.parent.mkdir(parents=True,exist_ok=True);b=z.read(i);q.write_bytes(b)
  members.append({'member':i.filename,'bytes':len(b),'sha256':digest(b),'crc32':f'{i.CRC:08x}','original_mode':oct(mode),'hidden':any(t.startswith('.') for t in path.parts),'reader_pdf':path.suffix.lower()=='.pdf','nested_archive':path.suffix.lower() in ['.zip','.gz','.tgz','.tar','.bz2','.xz']})
(S/'archive-inventory.json').write_text(json.dumps({'archive':'critical_wave_verification.zip','regular_members':members,'all_crc_pass':True},indent=2)+'\n')
receipt={'record_id':'23358014','record_url':'https://zenodo.org/api/records/23358014','record_sha256':digest((S/'record.json').read_bytes()),'verified_utc':now(),'title':record['metadata']['title'],'version':record['metadata'].get('version'),'publication_date':record['metadata']['publication_date'],'record_created':record['created'],'doi':record['doi'],'assets':assets,'regular_member_count':len(members),'scope':'Fresh API record/all public assets, queue/API size and MD5, independent SHA256, safe ZIP extraction and CRC/per-member mode/hidden/archive inventory; no helper execution.'}
(S/'receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
subprocess.run(['pdftotext','-layout',str(S/'critical_wave_growth.pdf'),str(R/'paper.txt')],check=True)
print(json.dumps(receipt,indent=2));print('MEMBERS');print('\n'.join(x['member'] for x in members))
