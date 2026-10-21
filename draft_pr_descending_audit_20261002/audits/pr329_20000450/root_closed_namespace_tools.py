"""Normalize existing external inventories without altering their dated records."""
from pathlib import Path
from root_submission_gate import A,load,pin,inventory

def octal(value):
    if isinstance(value,int):return f'{value:04o}'
    if value.startswith('0o'):return f'{int(value,8):04o}'
    return f'{int(value,8):04o}'

def verify_historical_namespaces():
    result={};external={};limits=[]
    for label,name in [('GEOMETRY','geometry'),('PRIMITIVITY','geometry_primitivity'),
        ('ARITHMETIC','arithmetic'),('DIVISION','division_polynomial'),
        ('PRIORITY','priority_audit'),('PREPRINT01','preprint_review_01')]:
        old=load(A/('ROOT_'+label+'_NAMESPACE_MANIFEST.json'))
        exclude=['.runtime'] if name=='geometry' else []
        actual=inventory(A/name,exclude)
        raw=old.get('files',old.get('payloads'))
        if isinstance(raw,dict):
            expected={n:dict(bytes=e['bytes'],sha256=e['sha256'],mode=octal(e['mode'])) for n,e in raw.items()}
        else:
            expected={}
            for e in raw:
                n=e['path']
                if label in {'GEOMETRY','PRIMITIVITY'}:
                    assert n.startswith(name+'/');n=n[len(name)+1:]
                mode=e.get('mode_decimal',e.get('mode'))
                expected[n]=dict(bytes=e['bytes'],sha256=e['sha256'],mode=octal(mode))
        assert actual['payloads']==expected,(name,'file body/mode/inventory changed')
        raw_dirs=old.get('directories',old.get('directory_modes'))
        if isinstance(raw_dirs,dict):dirs={n:octal(mode) for n,mode in raw_dirs.items()}
        else:
            dirs={}
            for row in raw_dirs:
                n=row['path'];assert n.startswith(name+'/');dirs[n[len(name)+1:]]=octal(row['mode'])
        root=old.get('root_mode',old.get('root_mode_decimal'))
        if root is not None:dirs['.']=octal(root)
        if '.' not in dirs:
            assert actual['directory_modes']['.']=='0755'
            dirs['.']='0755'
            limits.append(name+': historical inventory omitted the root directory mode; it is bound as0755 now, without claiming a prior native root-mode receipt.')
        assert actual['directory_modes']==dirs,(name,'directory inventory/mode changed')
        result[name]=dict(excluded_roots=exclude,inventory=actual,
            historical_external_manifest=pin(A/('ROOT_'+label+'_NAMESPACE_MANIFEST.json')))
        for e in old.get('external_pins',[]):
            p=Path(e['path']);expected=dict(bytes=e['bytes'],sha256=e['sha256'],mode=octal(e.get('mode_decimal',e.get('mode'))))
            assert pin(p)==expected
            if str(p) in external:assert external[str(p)]==expected
            external[str(p)]=expected
    return result,external,limits
