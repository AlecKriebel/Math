"""Capture and externally authenticate all executable buffers before compilation."""
from pathlib import Path
import json,hashlib,types,sys,stat
ORDER=['ops_core','numeric','journal','authority','gates','providers','protocol','bridge']
NAMES={n+'.py'for n in ORDER}|{'bootstrap.py','entry.py'}
def sha(b):return hashlib.sha256(b).hexdigest()
def load_verified(expected):
    here=Path(__file__).resolve().parent;root=here.parent;raw=(here/'SOURCE_MANIFEST.json').read_bytes()
    if sha(raw)!=expected:raise RuntimeError('Caller-pinned source manifest mismatch')
    manifest=json.loads(raw)
    if type(manifest.get('module_compile_optimize'))is not int or manifest['module_compile_optimize']!=0:raise RuntimeError('Compile optimize0 required')
    if set(manifest['source_files'])!=NAMES:raise RuntimeError('Exact compiled source inventory required')
    def verify():
        if(here/'SOURCE_MANIFEST.json').read_bytes()!=raw:raise RuntimeError('Source manifest drift')
        if{p.name for p in here.glob('*.py')}!=NAMES:raise RuntimeError('Source namespace drift')
        buffers={}
        for base,entries in [(here,manifest['source_files']),(root,manifest['data_files'])]:
            for name,pin in entries.items():
                p=base/name;b=p.read_bytes()
                if p.is_symlink()or not p.is_file()or len(b)!=pin['bytes']or sha(b)!=pin['sha256']:raise RuntimeError('Source/data buffer drift '+name)
                buffers[name]=b
        shared=json.loads(buffers['SHARED_IMMUTABLE_INPUTS.json'])
        for name,pin in shared.items():
            p=Path(name);b=p.read_bytes();s=p.lstat()
            if p.is_symlink()or len(b)!=pin['bytes']or sha(b)!=pin['sha256']or stat.S_IMODE(s.st_mode)!=pin['mode']or s.st_mtime_ns!=pin['mtime_ns']or s.st_nlink!=pin['nlink']:raise RuntimeError('Immutable original scientific input drift '+name)
        closure=json.loads(buffers['CLOSED_PRIOR_INPUT.json']);prior=Path(closure['root']);seal=prior/'MANIFEST.json';sealed=seal.read_bytes()
        if sha(sealed)!=closure['manifest_sha256']:raise RuntimeError('Prior complete input seal drift')
        def item(p):
            s=p.lstat();v={'kind':'directory'if stat.S_ISDIR(s.st_mode)else'file'if stat.S_ISREG(s.st_mode)else'UNSUPPORTED','mode':stat.S_IMODE(s.st_mode),'mtime_ns':s.st_mtime_ns,'nlink':s.st_nlink}
            if v['kind']=='file':b=p.read_bytes();v.update(bytes=len(b),sha256=sha(b))
            return v
        sealed=json.loads(sealed);actual={'.'if p==prior else str(p.relative_to(prior)):item(p)for p in[prior,*sorted(prior.rglob('*'))]if p!=seal}
        if actual!=sealed['entries']or any(item(seal)[k]!=v for k,v in sealed['manifest_metadata'].items()):raise RuntimeError('Complete old01 namespace/bytes/mode/nsmtime/nlink drift')
        return buffers
    selected=verify();mods={};previous={}
    try:
        for name in ORDER:
            m=types.ModuleType(name);m.__file__=str(here/(name+'.py'));previous[name]=sys.modules.get(name);sys.modules[name]=m;mods[name]=m
            exec(compile(selected[name+'.py'],m.__file__,'exec',optimize=0),m.__dict__)
    finally:
        for name,old in previous.items():
            if old is None:sys.modules.pop(name,None)
            else:sys.modules[name]=old
    mods['protocol'].VERIFY_SOURCE_CLOSURE=verify;verify();return mods,verify
