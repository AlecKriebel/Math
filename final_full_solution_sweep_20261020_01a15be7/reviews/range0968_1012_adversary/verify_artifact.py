#!/usr/bin/env python3
"""Read-only offline seal verifier. Never imports evidence or invokes commands."""
from pathlib import Path,PurePosixPath
import argparse,hashlib,json,os,re,stat,sys
ROOT=Path(__file__).resolve().parent

def require(test,message):
    if not test:
        raise ValueError(message)

def strict_object(pairs):
    out={}
    for key,value in pairs:
        require(key not in out,'duplicate JSON key')
        out[key]=value
    return out

def nonfinite(value):
    raise ValueError('nonfinite JSON constant')

def document(path):
    return json.loads(path.read_text(encoding='utf-8'),object_pairs_hook=strict_object,parse_constant=nonfinite)

def sha(data):
    return hashlib.sha256(data).hexdigest()

def safe_path(value):
    require(type(value) is str and value and '\\' not in value and '\x00' not in value,'unsafe path')
    p=PurePosixPath(value)
    require(not p.is_absolute() and all(x not in ('','.','..') for x in value.split('/')),'unsafe path')
    require(str(p)==value,'noncanonical path')
    return value

def regular(path):
    require(not path.is_symlink(),'symlink rejected')
    require(stat.S_ISREG(path.lstat().st_mode),'nonregular file rejected')

def check_seal(folder,name):
    path=folder/name; seal=folder/(name.replace('.json','.sha256'))
    regular(path);regular(seal)
    expected=(sha(path.read_bytes())+'  '+name+'\n').encode()
    require(seal.read_bytes()==expected,'manifest digest mismatch')
    return document(path)

def verify_entries(folder,entries):
    require(type(entries) is list,'entries must be list')
    names=[]
    for row in entries:
        require(type(row) is dict and set(row)=={'path','bytes','sha256'},'invalid entry schema')
        name=safe_path(row['path']); names.append(name)
        require(type(row['bytes']) is int and row['bytes']>=0,'invalid byte count')
        require(type(row['sha256']) is str and re.fullmatch('[0-9a-f]{64}',row['sha256']) is not None,'invalid content digest')
        f=folder/name
        for part in [f,*f.parents]:
            if part==folder:break
            require(not part.is_symlink(),'symlink rejected')
        regular(f);b=f.read_bytes()
        require(len(b)==row['bytes'] and sha(b)==row['sha256'],'file content mismatch: '+name)
    require(len(names)==len(set(names)),'duplicate manifest path')
    require(names==sorted(names),'manifest entries not sorted')
    return set(names)

def tree_contents(folder):
    files=set();directories=set()
    require(not folder.is_symlink() and folder.is_dir(),'invalid evidence directory')
    for base,dirs,names in os.walk(folder,followlinks=False):
        for name in dirs:
            f=Path(base)/name; require(not f.is_symlink(),'symlink rejected')
            require(stat.S_ISDIR(f.lstat().st_mode),'nonregular directory')
            directories.add(str(f.relative_to(folder)))
        for name in names:
            f=Path(base)/name;regular(f);files.add(str(f.relative_to(folder)))
    return files,directories

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--private',action='store_true',help='also verify locally retained private evidence')
    args=parser.parse_args()
    require(not Path(__file__).is_symlink(),'verifier symlink rejected')
    m=check_seal(ROOT,'OUTPUT_MANIFEST.json')
    require(type(m) is dict and set(m)=={'schema','created_utc','scope','files','private_manifest_sha256'},'invalid public manifest schema')
    require(type(m['schema']) is int and m['schema']==1,'invalid schema version')
    require(type(m['created_utc']) is str and type(m['scope']) is str,'invalid public metadata')
    require(type(m['private_manifest_sha256']) is str and re.fullmatch('[0-9a-f]{64}',m['private_manifest_sha256']) is not None,'invalid private seal anchor')
    names=verify_entries(ROOT,m['files'])
    require(all('/' not in n for n in names),'public paths must be top-level')
    observed={x.name for x in ROOT.iterdir()}
    allowed=names|{'OUTPUT_MANIFEST.json','OUTPUT_MANIFEST.sha256'}
    if 'private' in observed:
        require(not (ROOT/'private').is_symlink() and (ROOT/'private').is_dir(),'invalid private directory')
        allowed.add('private')
    require(observed==allowed,'public inventory not closed')
    private_count=None
    if args.private:
        folder=ROOT/'private'
        require(folder.is_dir() and not folder.is_symlink(),'private evidence unavailable')
        p=check_seal(folder,'PRIVATE_MANIFEST.json')
        require(sha((folder/'PRIVATE_MANIFEST.json').read_bytes())==m['private_manifest_sha256'],'private seal differs from public anchor')
        require(type(p) is dict and set(p)=={'schema','files','directories'},'invalid private manifest schema')
        require(type(p['schema']) is int and p['schema']==1,'invalid private schema version')
        pnames=verify_entries(folder,p['files'])
        require(type(p['directories']) is list and all(type(x) is str for x in p['directories']),'invalid directory inventory')
        directories=[safe_path(x) for x in p['directories']]
        require(directories==sorted(set(directories)),'duplicate/unsorted directory inventory')
        found_files,found_dirs=tree_contents(folder)
        require(found_files==pnames|{'PRIVATE_MANIFEST.json','PRIVATE_MANIFEST.sha256'},'private inventory not closed')
        require(found_dirs==set(directories),'private directory inventory not closed')
        private_count=len(pnames)
    print(json.dumps({'status':'PASS','public_payload_files':len(names),'private_payload_files':private_count,'scope':'offline bytes and closed inventories only; no mathematics, authorship, provider state or global completeness certificate'},sort_keys=True))

if __name__=='__main__':
    try:
        main()
    except Exception as error:
        print(json.dumps({'status':'FAIL','reason':str(error)},sort_keys=True))
        sys.exit(1)
