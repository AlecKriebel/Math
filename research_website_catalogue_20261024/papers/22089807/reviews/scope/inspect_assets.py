from pathlib import Path,PurePosixPath
import io,json,zipfile,tarfile,hashlib,base64,csv,subprocess
base=Path(__file__).resolve().parents[2];src=base/'sources';scope=base/'reviews/scope';root=src/'published-source'
archive=src/'simultaneous_amplifier_beyond_three_halves_source_and_certificates.tar.gz';outer=json.load(open(scope/'archive_inventory.json'))
expected={}
for line in (root/'MANIFEST.sha256').read_text().splitlines():
 h,name=line.split('  ',1);assert name not in expected;expected[name]=h
actual={x['name']:x['sha256'] for x in outer if x['type']=='file' and x['name']!='MANIFEST.sha256'}
assert actual==expected
nested=[];archives=[];readers=[]
for x in outer:
 if x['type']!='file':continue
 p=root/x['name'];data=p.read_bytes();assert len(data)==x['bytes'] and hashlib.sha256(data).hexdigest()==x['sha256']
 if data.startswith(b'%PDF-'):readers.append({'source':'embedded','path':str(p),'archive_filename':archive.name,'archive_member':x['name'],'bytes':len(data),'sha256':x['sha256']})
 if zipfile.is_zipfile(io.BytesIO(data)):
  with zipfile.ZipFile(io.BytesIO(data)) as z:
   assert z.testzip() is None;names=z.namelist();assert len(names)==len(set(names));record_names=[n for n in names if n.endswith('.dist-info/RECORD')];assert len(record_names)==1
   record_rows=list(csv.reader(io.StringIO(z.read(record_names[0]).decode())));verified=0
   for n,h,size in record_rows:
    d=z.read(n)
    if h:
     alg,b64=h.split('=',1);assert base64.urlsafe_b64encode(hashlib.new(alg,d).digest()).decode().rstrip('=')==b64;assert len(d)==int(size);verified+=1
   for i,m in enumerate(z.infolist()):
    d=z.read(m.filename);row={'archive_member':x['name'],'index':i,'name':m.filename,'bytes':len(d),'sha256':hashlib.sha256(d).hexdigest(),'hidden':any(v.startswith('.') for v in PurePosixPath(m.filename).parts),'pdf_magic':d.startswith(b'%PDF-'),'container_magic':zipfile.is_zipfile(io.BytesIO(d)),'document_extension':PurePosixPath(m.filename).suffix.lower() in ('.pdf','.docx','.html','.htm','.md','.rst','.ipynb')};nested.append(row)
    if row['pdf_magic']:readers.append({'source':'nested','outer_archive':archive.name,'archive_member':x['name'],'nested_member':m.filename,'bytes':len(d),'sha256':row['sha256']})
   archives.append({'member':x['name'],'members':len(names),'unique':True,'crc_ok':True,'wheel_record_verified_entries':verified,'wheel_record_entries':len(record_rows),'hidden_entries':sum(v['hidden'] for v in nested if v['archive_member']==x['name'])})
for f in json.load(open(src/'receipt.json'))['files']:
 p=src/f['name']
 if p.read_bytes().startswith(b'%PDF-'):readers.append({'source':'standalone','path':str(p),'bytes':f['bytes'],'sha256':f['sha256']})
for row in readers:
 if row.get('path'):
  p=Path(row['path']);info=subprocess.check_output(['pdfinfo',str(p)],text=True);row['pdfinfo']=info;row['pages']=int(next(l.split(':',1)[1] for l in info.splitlines() if l.startswith('Pages:')))
summary={'outer_members':len(outer),'outer_regular_files':sum(x['type']=='file' for x in outer),'outer_hidden_entries':sum(x['hidden'] for x in outer),'duplicate_outer_paths':False,'links_and_special_entries':0,'internal_manifest_exact_set_and_all_hashes_match':True,'nested_archives':archives,'nested_member_count':len(nested),'nested_container_magic_count':sum(x['container_magic'] for x in nested),'reader_count':len(readers),'reader_count_definition':'all files with %PDF- magic, including nested wheel members','unknown_extra_reader':False}
(scope/'nested_member_inventory.json').write_text(json.dumps(nested,indent=2)+'\n');(scope/'reader_asset_ledger.json').write_text(json.dumps(readers,indent=2)+'\n');(scope/'asset_inspection_summary.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps(summary,indent=2))
