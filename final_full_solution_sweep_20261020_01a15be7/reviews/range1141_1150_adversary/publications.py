"""Download and independently authenticate existing published payloads, without execution."""
from capture import *
from sources import source
import urllib.request, zipfile, io

def get(url):
    with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'ResearchVerification/1.0'}),timeout=80) as r:
        return r.read(),r.url,r.status
def record(n,recid):
    d=PRIVATE/f'publication{n}'
    data,url,status=get(f'https://zenodo.org/api/records/{recid}')
    save(d/'record_initial.json',data); obj=json.loads(data)
    root=PRIVATE/'checkpoint'/HERE.parents[1].name
    expected=json.loads((root/f'PR{n}_PUBLICATION_VERIFICATION.json').read_text())
    coverage=json.loads((root/f'PR{n}_PUBLICATION_COVERAGE_DETAILS.json').read_text())
    assert obj['doi']==expected['doi'] and obj['submitted']
    files=[]
    for f in obj['files']:
        data,final,code=get(f['links']['self'])
        assert len(data)==f['size']
        assert f['checksum']=='md5:'+hashlib.md5(data).hexdigest()
        exp=next(e for e in expected['files'] if e['name']==f['key'])
        assert sha(data)==exp['sha256']
        r=save(d/f['key'],data);r.update(url=final,checksum=f['checksum'],status=code);files.append(r)
    data,final,code=get('https://doi.org/'+expected['doi'])
    save(d/'doi_destination.html',data)
    assert code==200 and final.rstrip('/')==f'https://zenodo.org/records/{recid}'
    zipname=next(f['key'] for f in obj['files'] if f['key'].endswith('.zip'))
    pdfname=next(f['key'] for f in obj['files'] if f['key'].endswith('.pdf'))
    with zipfile.ZipFile(d/zipname) as z:
        names=z.namelist()
        assert len(names)==len(set(names))==coverage['safe_closed_zip_members']
        assert z.testzip() is None
        for info in z.infolist():
            path=pathlib.PurePosixPath(info.filename)
            assert not path.is_absolute() and '..' not in path.parts
            assert ((info.external_attr>>16)&0o170000)!=0o120000
            save(d/'source'/info.filename,z.read(info.filename))
        manifest=json.loads(z.read('SOURCE_MANIFEST.json'))
        assert set(manifest)==set(names)-{'SOURCE_MANIFEST.json'}
        for name,pin in manifest.items():
            data=z.read(name)
            assert len(data)==pin['bytes'] and sha(data)==pin['sha256']
        pdfpath=next(s for s in names if s.startswith('output/pdf/') and s.endswith('.pdf'))
        assert z.read(pdfpath)==(d/pdfname).read_bytes()
        # Distributed archives may preserve the PR inventory beneath an audit inputs prefix.
        copies=[]
        for f in (PRIVATE/f'pr{n}'/'head').rglob('*'):
            if f.is_file():
                name=str(f.relative_to(PRIVATE/f'pr{n}'/'head'))
                matches=[s for s in names if pathlib.PurePosixPath(s).name==f.name and z.read(s)==f.read_bytes()]
                assert matches, name
                copies.append({'head_path':name,'archive_paths':matches})
        metadata=json.loads(z.read('zenodo-metadata.json'))
        deposit=json.loads(z.read('zenodo-deposit.json'))
        native=metadata.get('metadata',metadata)
        normalizations=[]
        for key,value in native.items():
            actual=obj['metadata'].get(key)
            if key in ['publication_type','upload_type'] and actual is None:
                subkey='subtype' if key=='publication_type' else 'type'
                assert obj['metadata']['resource_type'][subkey]==value
                normalizations.append({'field':key,'normalization':'resource_type.'+subkey})
                continue
            if key=='license' and isinstance(actual,dict) and actual=={'id':value}:
                normalizations.append({'field':'license','normalization':'scalar SPDX license to {id: scalar}'})
            else:
                assert actual==value,(key,actual,value)
        assert len(native)==coverage['native_metadata_fields']
    out={'pr':n,'record':recid,'captured':now(),'doi':expected['doi'],'doi_destination':final,'provider_state':{k:obj.get(k) for k in ['submitted','is_published','state','status']},'files':files,'safe_members':len(names),'manifest_payloads':len(manifest),'operative_head_copies':copies,'embedded_pdf_equal':True,'native_metadata_fields':len(native),'provider_normalizations':normalizations}
    save(d/'identity_initial.json',json.dumps(out,indent=2).encode())
    print(json.dumps(out,indent=2))
if __name__=='__main__':
    for n,r in [(1141,23443301),(1150,23444050)]:record(n,r)
