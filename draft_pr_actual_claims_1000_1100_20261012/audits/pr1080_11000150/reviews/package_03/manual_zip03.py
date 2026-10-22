import struct,hashlib,json,zlib,io
from pathlib import Path
H=Path(__file__).resolve().parent;P=H.parents[1]/'preprint_v1_0';K=P/'verification_kit'
names=json.loads((K/'ALLOWLIST.json').read_text())['members']
out=io.BytesIO();central=[];date=((2026-1980)<<9)|(10<<5)|14
for name in names:
    encoded=('verification_kit/'+name).encode('ascii');data=(K/name).read_bytes();crc=zlib.crc32(data);size=len(data);offset=out.tell()
    out.write(struct.pack('<IHHHHHIIIHH',0x04034b50,20,0,0,0,date,crc,size,size,len(encoded),0));out.write(encoded);out.write(data)
    central.append(struct.pack('<IHHHHHHIIIHHHHHII',0x02014b50,(3<<8)|20,20,0,0,0,date,crc,size,size,len(encoded),0,0,0,0,0o100644<<16,offset)+encoded)
start=out.tell()
for record in central:out.write(record)
csize=out.tell()-start
out.write(struct.pack('<IHHHHIIH',0x06054b50,0,0,len(names),len(names),csize,start,0))
body=out.getvalue();actual=(P/'verification_kit.zip').read_bytes()
if body!=actual:raise RuntimeError('Independent manually constructed ZIP differs')
result={'status':'PASS','method':'Independent struct-packed local and central ZIP headers, payload CRCs, EOCD; no candidate builder or zipfile writer','members':len(names),'bytes':len(body),'sha256':hashlib.sha256(body).hexdigest(),'all_bytes_equal':True}
(H/'MANUAL_ZIP_RECONSTRUCTION.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result))
