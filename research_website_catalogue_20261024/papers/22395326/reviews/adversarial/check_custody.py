"""Bind every frozen source object and archive member, plus previous owned packets."""
from pathlib import Path, PurePosixPath
from datetime import datetime, timezone
import hashlib,json,stat,zipfile,zlib
D=Path(__file__).resolve().parent;P=D.parents[3];S=P/'papers/22395326/sources'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def req(c,m):
    if not c:raise RuntimeError(m)
def bind(p):return {'path':str(p),'bytes':p.stat().st_size,'sha256':sha(p)}
manifest=S/'SOURCE_READY_MANIFEST.json';data=json.loads(manifest.read_text());original=[]
for row in data['files']:
    path=S/row['path'];got=bind(path);req((got['bytes'],got['sha256'])==(row['bytes'],row['sha256']),str(path));original.append(got)
req(len(original)==133,'133 frozen bindings')
members=[]
for archive in sorted(S.glob('*.zip')):
    with zipfile.ZipFile(archive) as z:
        seen=set()
        for info in z.infolist():
            p=PurePosixPath(info.filename)
            req(not p.is_absolute() and '..' not in p.parts and '\\' not in info.filename,'unsafe path')
            if info.is_dir():continue
            req(info.filename not in seen,'duplicate member');seen.add(info.filename)
            mode=(info.external_attr>>16)&0xffff
            req(not stat.S_ISLNK(mode),'symlink')
            blob=z.read(info);req(len(blob)==info.file_size and (zlib.crc32(blob)&0xffffffff)==info.CRC,'CRC')
            expanded=S/'published-source'/archive.name/info.filename
            h=hashlib.sha256(blob).hexdigest();req(expanded.is_file() and sha(expanded)==h,'expanded member drift')
            members.append({'archive':archive.name,'member':info.filename,'bytes':len(blob),'crc32':f'{info.CRC:08x}','sha256':h,'expanded_path':str(expanded)})
req(len(members)==118,'118 archive members')
readyseal=S/'SOURCE_READY_SEAL.json'
receipts={'utc':datetime.now(timezone.utc).isoformat(),'source_ready_manifest':bind(manifest),'source_ready_seal':bind(readyseal),'source_objects':original,'archive_member_occurrences':members,'all_133_bindings_and_118_members_match':True,'expanded_member_total_bytes':sum(r['bytes'] for r in members),'no_original_write':True}
(D/'ORIGINAL_BINDINGS.json').write_text(json.dumps(receipts,indent=2)+'\n')
previous=[P/'papers'/r/'reviews/adversarial' for r in ['23074543','23442760','23395703','23333353','23416806','23441617','23576280','23331258','23217863']]+[P/'verification/cfh-independent-code-audit-sol-20261025']
pres=[];total=0
for folder in previous:
    m=folder/'FINAL_MANIFEST.json';seal=folder/'FINAL_SEAL.json';md=json.loads(m.read_text());sd=json.loads(seal.read_text())
    req(sd['manifest_sha256']==sha(m),'previous manifest seal')
    entries=md['files'];entries=[dict(v,path=k) for k,v in entries.items()] if isinstance(entries,dict) else entries
    owned=[]
    for row in entries:
        path=folder/row['path'];b=bind(path);req(b['sha256']==row['sha256'] and b['bytes']==row['bytes'],'previous packet drift');owned.append(b)
    total+=len(owned);pres.append({'folder':str(folder),'manifest':bind(m),'seal':bind(seal),'owned_bindings':owned})
req(total==147,'147 prior owned files')
(D/'PREVIOUS_PACKET_PRESERVATION.json').write_text(json.dumps({'utc':datetime.now(timezone.utc).isoformat(),'packets':pres,'owned_file_count':total,'all_match':True},indent=2)+'\n')
print(json.dumps({'source_bindings':len(original),'archive_members':len(members),'prior_packets':len(pres),'prior_owned_files':total,'all_match':True}))
