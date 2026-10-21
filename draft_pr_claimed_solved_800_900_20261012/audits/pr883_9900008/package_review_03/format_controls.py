#!/usr/bin/env python3
"""Small independent format fixtures for already authenticated/read current helpers.
No input mutations or file extraction. Exact reviewed modules loaded in isolation.
"""
from pathlib import Path
import hashlib,io,json,runpy,stat,struct,sys,zipfile,zlib
H=Path(__file__).resolve().parent
R=H.parent/'replay/revision_r2'
P=R/'preprint/verification_package'
PINS={'build_verification.py':'2b0521d74a49360cbdd6d48427cb02763b586f3a5196766ec16f6ddc2fa41f2c','check_originals.py':'e4fb73b16db72ed4387c08c38662a1ad9f836f9b0ecd2ff91778347deb74829b','verify_package.py':'e80ce30e89547c52d63c44237a554f0b3bf1ae1959783bbbba1f3f1703e9f7f8','verify_current_publication.py':'3fc89372bae6cc3ed2f6a8d4f93d890e94e9fd635b712223853630d26f034672'}
def need(c,s):
 if not c:raise RuntimeError(s)
def build(data,compressed):
 name=b'x.bin';crc=zlib.crc32(data);mode=(stat.S_IFREG|0o644)<<16;date=(46<<9)|(10<<5)|15
 local=struct.pack('<4s5H3I2H',b'PK\x03\x04',20,0,8,0,date,crc,len(compressed),len(data),len(name),0)+name+compressed
 central=struct.pack('<4s6H3I5H2I',b'PK\x01\x02',(3<<8)|20,20,0,8,0,date,crc,len(compressed),len(data),len(name),0,0,0,0,mode,0)+name
 end=struct.pack('<4s4H2IH',b'PK\x05\x06',0,0,1,1,len(central),len(local),0)
 return local+central+end
def compress(b):
 c=zlib.compressobj(9,zlib.DEFLATED,-15);return c.compress(b)+c.flush()
payload=b'check\r\n\x00\xff';plain=compress(payload)
cases=[('valid',payload,plain,True),('reconciled_suffix',payload,plain+b'\x00',False),('second_empty_stream',payload,plain+compress(b''),False),('truncated_empty',b'',compress(b'')[:-1],False)]
rows=[]
for name,pin in PINS.items():
 path=P/name;need(hashlib.sha256(path.read_bytes()).hexdigest()==pin,'startup pin changed')
 module=runpy.run_path(str(path),run_name='_independent_review_helper_')
 for label,data,comp,expected in cases:
  raw=build(data,comp)
  if label in ('reconciled_suffix','second_empty_stream'):
   with zipfile.ZipFile(io.BytesIO(raw)) as z:need(z.read('x.bin')==data,'fixture must remain byte-correct through ordinary zipfile')
  reason=None
  try:module['zip_payloads'](raw,{'x.bin':data},generated=True);accepted=True
  except (ValueError,zlib.error) as e:accepted=False;reason=str(e)
  need(accepted is expected,'unexpected current helper decision')
  rows.append({'module':name,'case':label,'expected_accept':expected,'actual_accept':accepted,'reason':reason,'archive_bytes':len(raw),'archive_sha256':hashlib.sha256(raw).hexdigest()})
print(json.dumps({'status':'PASS','decisions':len(rows),'valid_accepts':4,'rejections':12,'rows':rows,'scope':'Small ordinary artifact-format controls; not an exhaustive parser/security review.'},indent=2,sort_keys=True))
