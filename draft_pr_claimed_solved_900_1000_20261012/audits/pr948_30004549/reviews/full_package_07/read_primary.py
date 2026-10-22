from pathlib import Path
import json,hashlib,subprocess,os,datetime
R=Path(__file__).parent;A=R.parents[1]
sources=[('mfo','source_scope/private/mfo.pdf',[31]),('dlz','source_scope/private/dlz.pdf',[3,4,5]),('twzz','source_scope/private/twwzz-v3.pdf',[2]),('dlz08','classical_priority/private/dlz2008v1.pdf',[20]),('ht','recent_priority/private/ht-v3.pdf',[12,13,14]),('czi','recent_priority/private/czI-accepted.pdf',[24,25,26,27]),('czii','recent_priority/private/czII-accepted.pdf',[23,24]),('donaldson','mechanism_priority/private/donaldson.pdf',[1,2,3]),('bk','mechanism_priority/private/bande-kotschick.pdf',[4,5]),('s2026','recent_priority/private/s2026.pdf',[8,9,10]),('lu2020','classical_priority/private/lu2020journal.pdf',[13])]
rows=[]
for key,name,pages in sources:
 p=A/'reviews'/name;raw=p.read_bytes();texts=[]
 for page in pages:
  data=subprocess.run(['pdftotext','-f',str(page),'-l',str(page),'-layout',str(p),'-'],capture_output=True,check=True).stdout;texts.append(data)
 out=b'\n'.join(texts);target=R/'private_primary'/f'{key}.txt'
 with target.open('wb') as f:f.write(out);f.flush();os.fsync(f.fileno())
 assert target.read_bytes()==out;target.chmod(0o600)
 rows.append({'key':key,'source_relative_to_audit':'reviews/'+name,'source_sha256':hashlib.sha256(raw).hexdigest(),'pages_extracted':pages,'selected_text_sha256':hashlib.sha256(out).hexdigest(),'full_body_read':False,'public_body':False})
(R/'private_primary').chmod(0o700)
rec=(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'records':rows,'status':'EXTRACTION_AND_BODY_IDENTITY_ONLY_pending_personal_read'},indent=2)+'\n').encode()
with (R/'PRIMARY_INVENTORY.json').open('wb') as f:f.write(rec);f.flush();os.fsync(f.fileno())
assert (R/'PRIMARY_INVENTORY.json').read_bytes()==rec
