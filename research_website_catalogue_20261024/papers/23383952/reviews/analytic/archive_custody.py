"""Hash/CRC-read every original occurrence without extraction or opinion reading."""
from pathlib import Path,PurePosixPath
from io import BytesIO
import datetime,hashlib,json,stat,zipfile
O=Path(__file__).resolve().parent;B=O.parents[1];S=B/'sources'
inventory=json.loads((S/'archive-members.json').read_text());table={(r['container'],r['original_member_name']):r for r in inventory['members']};containers={r['container']:r for r in inventory['archive_containers']};seen=[];cseen=[];total=0;directories=0
def need(x,tag):
 if not x:raise ValueError(tag)
def walk(name,data):
 global total,directories
 row=containers[name];need(row['kind']=='zip' and row['bytes']==len(data) and row['sha256']==hashlib.sha256(data).hexdigest(),'container identity');cseen.append(name)
 with zipfile.ZipFile(BytesIO(data)) as z:
  names=set()
  for i in z.infolist():
   p=PurePosixPath(i.filename);mode=i.external_attr>>16
   need(not p.is_absolute() and '..' not in p.parts and '\\' not in i.filename and i.filename not in names and not i.flag_bits&1,'safe unique unencrypted path');names.add(i.filename)
   if i.is_dir():directories+=1;continue
   need(stat.S_IFMT(mode) in (0,stat.S_IFREG),'regular body')
   b=z.read(i);key=(name,i.filename);r=table[key];actual=Path(r['extracted_path'])
   need(actual.resolve().is_relative_to(S.resolve()) and r['safe_regular_body'] is True,'existing contained extraction')
   need(r['bytes']==len(b)==i.file_size and r['sha256']==hashlib.sha256(b).hexdigest() and r['CRC32']==f'{i.CRC:08x}' and actual.read_bytes()==b,'actual full CRC/hash/existing identity')
   seen.append(key);total+=len(b)
   nested=name+'::'+i.filename
   if nested in containers:walk(nested,b)
   else:need(not zipfile.is_zipfile(BytesIO(b)),'no unrecorded ZIP')
walk('weighted-yamabe-heat-trace-verification.zip',(S/'weighted-yamabe-heat-trace-verification.zip').read_bytes())
need(set(seen)==set(table) and len(seen)==len(table)==142 and set(cseen)==set(containers) and len(cseen)==4 and total==928042,'complete142_occurrences_four_containers')
receipt={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS','regular_occurrences':len(seen),'containers':len(cseen),'nested_containers':3,'expanded_bytes_all_depths':total,'directory_entries':directories,'all_CRC_hash_and_existing_bytes_equal':True,'all_support_opinion_prose_semantically_read':False,'extractions_repacked_or_source_programs_executed':False}
(O/'RECURSIVE_CUSTODY.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps(receipt))
