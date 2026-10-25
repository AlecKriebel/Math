"""Acquire inspected K3P release assets, retaining large archives compressed."""
from pathlib import Path
from urllib.request import Request, urlopen
from datetime import datetime, timezone
from zipfile import ZipFile
import tarfile, hashlib, json, os, subprocess
folder=Path(__file__).resolve().parents[2]/'sources'
record=json.loads((folder/'record.json').read_text())
receipt={'record_id':str(record['id']), 'retrieved_utc':datetime.now(timezone.utc).isoformat(),'method':'Fresh public record; streamed all 14 published assets with checksum and size verification; large archives retained compressed.','files':[]}
inventories={}
for item in sorted(record['files'],key=lambda f:f['size']):
    name=item['key']; assert Path(name).name==name
    size=item['size']; assert size<100*1024*1024
    target=folder/name; alg,expected=item['checksum'].split(':',1)
    checksum=hashlib.new(alg); sha=hashlib.sha256(); count=0
    if target.exists():
        with target.open('rb') as src:
            while data:=src.read(1024*1024): checksum.update(data);sha.update(data);count+=len(data)
        valid=count==size and checksum.hexdigest()==expected
    else: valid=False
    url=item['links'].get('self') or item['links']['content']
    if not valid:
        checksum=hashlib.new(alg);sha=hashlib.sha256();count=0
        temp=target.with_name(name+'.download')
        subprocess.run(['curl','-fL','--silent','--show-error','--retry','2','--max-time','240',url,'-o',str(temp)],check=True)
        with temp.open('rb') as src:
            while data:=src.read(1024*1024):
                count+=len(data);assert count<=size
                checksum.update(data);sha.update(data)
        assert count==size and checksum.hexdigest()==expected,(name,count,checksum.hexdigest())
        os.replace(temp,target)
    receipt['files'].append({'name':name,'url':url,'bytes':count,'sha256':sha.hexdigest(),'zenodo_checksum':item['checksum']})
    (folder/'receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print('verified',name,count,sha.hexdigest(),flush=True)
    if name.endswith('.zip'):
        with ZipFile(target) as archive:
            infos=archive.infolist()
            inventories[name]={'members':len(infos),'expanded_bytes':sum(x.file_size for x in infos),'files':[{'name':x.filename,'bytes':x.file_size} for x in infos]}
            if 'Source_' in name:
                dest=folder/'published-source'/Path(name).stem
                assert sum(x.file_size for x in infos)<10*1024*1024
                for x in infos:
                    assert (dest/x.filename).resolve().is_relative_to(dest.resolve())
                    assert (x.external_attr>>16)&0o170000 != 0o120000
                archive.extractall(dest)
    elif name.endswith('.tar.gz'):
        with tarfile.open(target,'r:gz') as archive:
            infos=archive.getmembers()
            inventories[name]={'members':len(infos),'expanded_bytes':sum(x.size for x in infos),'files':[{'name':x.name,'bytes':x.size,'type':str(x.type)} for x in infos]}
    (folder/'archive_inventory.json').write_text(json.dumps(inventories,indent=2)+'\n')
receipt['complete']=len(receipt['files'])==len(record['files'])
receipt['completed_utc']=datetime.now(timezone.utc).isoformat()
(folder/'receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
print('COMPLETE',len(receipt['files']))
