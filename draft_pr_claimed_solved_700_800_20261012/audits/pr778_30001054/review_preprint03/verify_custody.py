"""Read-only exact review custody, excluding only the root MANIFEST.json."""
from pathlib import Path, PurePosixPath
import argparse, hashlib, json, os, re, stat


def need(ok, why):
    if not ok:
        raise ValueError(why)


def unique(pairs):
    result = {}
    for key, value in pairs:
        need(key not in result, 'duplicate JSON key')
        result[key] = value
    return result


def regular(p):
    need(stat.S_ISREG(p.lstat().st_mode), 'nonregular file: '+str(p))
    return p.read_bytes()


def identity(raw):
    return {'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}


def snapshot(root):
    need(stat.S_ISDIR(root.lstat().st_mode), 'root is not a plain directory')
    files = {}
    def walk(folder):
        entries = list(os.scandir(folder))
        need(bool(entries), 'empty directory: '+str(folder))
        for entry in entries:
            p = Path(entry.path)
            name = p.relative_to(root).as_posix()
            mode = entry.stat(follow_symlinks=False).st_mode
            if stat.S_ISDIR(mode):
                walk(p)
            else:
                need(stat.S_ISREG(mode), 'symlink/special: '+name)
                if name != 'MANIFEST.json':
                    files[name] = identity(regular(p))
    walk(root)
    return files


def verify(root, pin):
    need(re.fullmatch('[0-9a-f]{64}',pin) is not None, 'bad external digest')
    raw = regular(root/'MANIFEST.json')
    need(identity(raw)['sha256']==pin, 'external digest differs')
    manifest = json.loads(raw,object_pairs_hook=unique,
                          parse_constant=lambda x: (_ for _ in ()).throw(ValueError('nonfinite JSON')))
    need(type(manifest) is dict and set(manifest)=={'schema','files'}, 'manifest shape')
    need(manifest['schema']=='review-preprint03-exact-inventory-v1', 'schema')
    need(type(manifest['files']) is dict and len(manifest['files'])>0, 'file mapping')
    for name, row in manifest['files'].items():
        pp=PurePosixPath(name)
        need(name and name!='MANIFEST.json' and not pp.is_absolute()
             and str(pp)==name and all(x not in ('','.','..') for x in name.split('/'))
             and '\\' not in name, 'unsafe path')
        need(type(row) is dict and set(row)=={'bytes','sha256'}, 'record shape')
        need(type(row['bytes']) is int and row['bytes']>=0, 'record size')
        need(type(row['sha256']) is str and re.fullmatch('[0-9a-f]{64}',row['sha256']) is not None,
             'record digest')
    need(snapshot(root)==manifest['files'], 'file closure or bytes differ')
    return {'status':'PASS','files':len(manifest['files']),
            'manifest_sha256':pin,'mtime_independent':True,'hidden_included':True,
            'excluded_only':'MANIFEST.json','symlinks_special_empty_directories':False}


if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--root',type=Path,default=Path(__file__).absolute().parent)
    ap.add_argument('--manifest-sha256',required=True)
    args=ap.parse_args()
    print(json.dumps(verify(args.root.absolute(),args.manifest_sha256),sort_keys=True))
