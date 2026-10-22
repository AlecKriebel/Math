"""Byte-exact virtual CAS for own fixture custody; never production CASE mutation."""
from pathlib import Path
import json,gzip,hashlib,base64,stat,os
O=Path(__file__).resolve().parent
def sha(b):return hashlib.sha256(b).hexdigest()
def jb(v):return(json.dumps(v,sort_keys=True,ensure_ascii=False,indent=2)+'\n').encode()
def restore(pack,e):
    memo={}
    def node(i):
        if i in memo:return memo[i]
        n=pack['nodes'][i];t=n[0]
        v={k:node(j)for k,j in n[1]}if t=='d'else[node(j)for j in n[1]]if t=='l'else float.fromhex(n[1])if t=='f'else n[1]
        memo[i]=v;return v
    v=node(e['node']);r=e['recipe']
    if r['encoding']=='bytes':b=base64.b64decode(v)
    else:
        kw=r['kwargs'];kw={**kw,'separators':tuple(kw['separators'])}if'separators'in kw else kw;b=(json.dumps(v,**kw)+r['suffix']).encode('utf-8')
    for unused in range(r['gzip_layers']):b=gzip.compress(b,mtime=0)
    assert sha(b)==e['exact_compressed_sha256']and len(b)==e['exact_compressed_bytes'];return b
PACKS={}
def exact_compressed(relative):
    p=O/relative
    if p.is_file():return p.read_bytes()
    idx=json.loads((O/'controls/CAS_PACK_INDEX.json').read_bytes());pin=idx['entries'][relative];name=pin['pack']
    if name not in PACKS:
        raw=(O/name).read_bytes();assert sha(raw)==idx['packs'][name]['sha256'];PACKS[name]=json.loads(gzip.decompress(raw))
    return restore(PACKS[name],PACKS[name]['entries'][relative])
def raw(relative):return gzip.decompress(exact_compressed(relative))
def present(relative):
    if(O/relative).is_file():return True
    p=O/'controls/CAS_PACK_INDEX.json';return p.is_file()and relative in json.loads(p.read_bytes())['entries']
def compact(selected=None):
    directory=O/'controls/custody_blobs';paths=selected if selected is not None else sorted(directory.glob('*.gz'),key=lambda p:p.stat().st_size)[:80];assert paths
    nodes=[];intern={}
    def node(v):
        t=type(v);n=['d',[[k,node(x)]for k,x in v.items()]]if t is dict else['l',[node(x)for x in v]]if t is list else['f',v.hex()]if t is float else['b',v]if t is bool else['i',v]if t is int else['n',None]if v is None else['s',v]
        k=json.dumps(n,ensure_ascii=False,separators=(',',':'))
        if k not in intern:intern[k]=len(nodes);nodes.append(n)
        return intern[k]
    entries={};sources={}
    candidates=[{'ensure_ascii':False,'sort_keys':True,'indent':2},{'ensure_ascii':False,'sort_keys':False,'indent':2},{'ensure_ascii':False,'sort_keys':True,'separators':[',',':']},{'ensure_ascii':False,'sort_keys':False,'separators':[',',':']},{'ensure_ascii':True,'sort_keys':False,'indent':2},{'ensure_ascii':False,'sort_keys':False}]
    for p in paths:
        original=p.read_bytes();b=original;layers=0
        while b.startswith(b'\x1f\x8b'):
            try:b=gzip.decompress(b);layers+=1
            except OSError:break
        recipe=None
        try:
            v=json.loads(b)
            for kw in candidates:
                actual={**kw,'separators':tuple(kw['separators'])}if'separators'in kw else kw
                for suffix in['','\n']:
                    if(json.dumps(v,**actual)+suffix).encode()==b:recipe={'encoding':'json','kwargs':kw,'suffix':suffix,'gzip_layers':layers};break
                if recipe:break
        except (ValueError,UnicodeError):pass
        if recipe is None:v=base64.b64encode(b).decode();recipe={'encoding':'bytes','gzip_layers':layers}
        s=p.lstat();relative=str(p.relative_to(O));entries[relative]={'node':node(v),'recipe':recipe,'exact_compressed_sha256':sha(original),'exact_compressed_bytes':len(original),'original_mode':stat.S_IMODE(s.st_mode),'original_mtime_ns':s.st_mtime_ns,'original_nlink':s.st_nlink};sources[relative]=original
    pack={'nodes':nodes,'entries':entries,'scope':'Exact recoverable own CAS compressed bytes and original file metadata; no original inode claim.'}
    for name,e in entries.items():assert restore(pack,e)==sources[name]
    idxpath=O/'controls/CAS_PACK_INDEX.json';index=json.loads(idxpath.read_bytes())if idxpath.exists()else{'entries':{},'packs':{}};name='controls/CAS_COMPACTION_PACK'+str(len(index['packs'])+1).zfill(2)+'.json.gz';compressed=gzip.compress(jb(pack),mtime=0);physical=sum(p.lstat().st_blocks*512 for p in[O,*O.rglob('*')]);assert physical+len(compressed)+65536<=10*1024*1024;assert os.statvfs(O).f_bavail*os.statvfs(O).f_frsize-len(compressed)>150*1024*1024
    p=O/name;p.write_bytes(compressed);read=json.loads(gzip.decompress(p.read_bytes()))
    for relative,e in read['entries'].items():assert restore(read,e)==sources[relative]
    index['packs'][name]={'sha256':sha(compressed),'bytes':len(compressed),'original_files':len(entries),'original_physical_bytes':sum(p.stat().st_blocks*512 for p in paths),'all_original_compressed_bytes_verified_before_own_unlink':True}
    for relative,e in entries.items():assert relative not in index['entries'];index['entries'][relative]={'pack':name,'compressed_sha256':e['exact_compressed_sha256']}
    idxpath.write_bytes(jb(index))
    for p in paths:p.unlink()
    print(json.dumps(index['packs'][name]))
if __name__=='__main__':compact()
