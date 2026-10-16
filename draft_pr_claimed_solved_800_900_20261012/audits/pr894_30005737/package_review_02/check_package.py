from pathlib import Path
import struct,zlib,hashlib,json,stat,datetime
R=Path(__file__).resolve().parent;A=R.parent;C=A/'package_assembly_01/candidate';V=C/'verification'
def sha(b):return hashlib.sha256(b).hexdigest()
def pin(b):return {'bytes':len(b),'sha256':sha(b)}
def load(p):return json.loads(p.read_bytes())
def parse_zip(raw,payloads,fixed=False):
 end=struct.unpack_from('<4s4H2IH',raw,len(raw)-22);assert end[:3]==(b'PK\x05\x06',0,0) and end[3]==end[4]==len(payloads) and end[7]==0
 pos=0;cd=end[6];assert cd+end[5]==len(raw)-22
 names=[];central_pos=cd;report=[]
 for name,want in sorted(payloads.items()):
  h=struct.unpack_from('<4s5H3I2H',raw,pos);assert h[0]==b'PK\x03\x04' and h[1:4]==(20,0,8) and h[-1]==0
  n=raw[pos+30:pos+30+h[9]];assert n==name.encode('ascii');assert h[8]==len(want)
  start=pos+30+len(n);comp=raw[start:start+h[7]];d=zlib.decompressobj(-15);b=d.decompress(comp);assert d.eof and not d.unused_data and not d.unconsumed_tail
  assert b==want and zlib.crc32(b)&0xffffffff==h[6]
  c=struct.unpack_from('<4s6H3I5H2I',raw,central_pos)
  assert c[:4]==(b'PK\x01\x02',788,20,0) and c[4:10]==(8,*h[4:9]) and c[10:15]==(len(n),0,0,0,0) and c[16]==pos
  assert raw[central_pos+46:central_pos+46+len(n)]==n
  mode=c[15]>>16;assert stat.S_ISREG(mode) and stat.S_IMODE(mode) in (0o444,0o644)
  if fixed:assert h[4:6]==(0,((2026-1980)<<9)|(10<<5)|16) and mode==0o100644
  report.append({'name':name,'crc32':h[6],'compressed_bytes':len(comp),'bytes':len(b),'offset':pos})
  pos=start+len(comp);central_pos+=46+len(n);names.append(name)
 assert pos==cd and central_pos==len(raw)-22
 return report

def raw_zip(payloads):
 out=bytearray();directory=bytearray();date=((2026-1980)<<9)|(10<<5)|16
 for name,b in sorted(payloads.items()):
  n=name.encode('ascii');encoder=zlib.compressobj(9,zlib.DEFLATED,-15);compressed=encoder.compress(b)+encoder.flush();crc=zlib.crc32(b)&0xffffffff;offset=len(out)
  out+=struct.pack('<4s5H3I2H',b'PK\x03\x04',20,0,8,0,date,crc,len(compressed),len(b),len(n),0)+n+compressed
  directory+=struct.pack('<4s6H3I5H2I',b'PK\x01\x02',788,20,0,8,0,date,crc,len(compressed),len(b),len(n),0,0,0,0,0o100644<<16,offset)+n
 cd=len(out);out+=directory;out+=struct.pack('<4s4H2IH',b'PK\x05\x06',0,0,len(payloads),len(payloads),len(directory),cd,0);return bytes(out)

m=load(A/'SOURCE_MANIFEST.json');originals=[]
for row in m['files']:
 b=(V/'source'/row['path']).read_bytes();assert pin(b)=={k:row[k] for k in ('bytes','sha256')};assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==row['git_blob'];assert b==(A/'source'/row['path']).read_bytes();originals.append({**row,'git_blob_verified':True,'source_byte_equal':True})
assert len(originals)==18 and sum(r['bytes'] for r in originals)==91564
man=load(V/'source/authored/MANIFEST.json');p={'MANIFEST.json':(V/'source/authored/MANIFEST.json').read_bytes()}
for r in man['files']:p[r['path']]=(V/'source/authored'/r['path']).read_bytes()
original_zip=parse_zip((V/'source/AUTHOR_CANDIDATE.zip').read_bytes(),p)
payloads={p.relative_to(V).as_posix():p.read_bytes() for p in V.rglob('*') if p.is_file()};assert len(payloads)==242
raw=(C/'post-lie-verification.zip').read_bytes();zip_rows=parse_zip(raw,payloads,True);rebuilt=raw_zip(payloads);assert rebuilt==raw
(R/'private_tmp/independent_raw_rebuild.zip').write_bytes(rebuilt)
idx=load(V/'package_index.json');assert len(idx['files'])==241;assert {r['path'] for r in idx['files']}==set(payloads)-{'package_index.json'}
for r in idx['files']:assert pin(payloads[r['path']])=={k:r[k] for k in ('bytes','sha256')}
outer=load(C/'CURRENT_PUBLICATION_MANIFEST.json');assert len(outer['files'])==252
allouter={p.relative_to(C).as_posix():p.read_bytes() for p in C.rglob('*') if p.is_file()};assert set(allouter)=={r['path'] for r in outer['files']}|{'CURRENT_PUBLICATION_MANIFEST.json'}
for r in outer['files']:assert pin(allouter[r['path']])=={k:r[k] for k in ('bytes','sha256')}
for n in ['portable.py','note.tex','metadata.json','zenodo-deposit.json']:assert (C/n).read_bytes()==(V/n).read_bytes()
mdata=load(C/'metadata.json');dep=load(C/'zenodo-deposit.json');assert len(mdata)==12 and dep['metadata']==mdata and dep['files']==[{'name':n,'path':n} for n in ['post-lie-note.pdf','post-lie-verification.zip']]
assert mdata['title']=='Post-Lie nonexistence with a semisimple target' and mdata['publication_date']=='2026-10-16' and mdata['license']=='cc-by-4.0' and mdata['creators']==[{'affiliation':'Independent researcher','name':'Kriebel, Alec','orcid':'0009-0001-9320-500X'}]
output={'timestamp_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'originals':originals,'original_archive':original_zip,'raw_zip':{'members':len(zip_rows),'pins':pin(raw),'exact_raw_struct_crc_zlib_rebuild':True,'implementation':'independent raw struct/CRC32/raw-DEFLATE writer; no zipfile import or subject helpers'},'outer_manifest_rows':252,'package_index_rows':241,'metadata_fields':sorted(mdata),'two_assets_exact':True,'all_four_outer_inner_copies_equal':True}
(R/'PACKAGE_CHECKS.json').write_text(json.dumps(output,indent=2)+'\n');print(json.dumps({k:v for k,v in output.items() if k not in ('originals','original_archive')},indent=2))
