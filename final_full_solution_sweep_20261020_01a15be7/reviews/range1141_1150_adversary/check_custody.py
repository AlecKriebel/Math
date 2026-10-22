"""Independent bounded custody checks. Read-only, including under -O and -OO.

Does not import or execute any archived program. Negative controls are in-memory.
"""
import copy, hashlib, io, json, pathlib, sys, zipfile, warnings

ROOT=pathlib.Path(sys.argv[1]).resolve()
def require(ok,reason):
    if not ok: raise ValueError(reason)
def digest(data): return hashlib.sha256(data).hexdigest()
def load(path): return json.loads((ROOT/path).read_text())
def valid_zip(data):
    with zipfile.ZipFile(io.BytesIO(data)) as z:
        names=z.namelist()
        require(len(names)==len(set(names)),'duplicate')
        for info in z.infolist():
            p=pathlib.PurePosixPath(info.filename)
            require(not p.is_absolute() and '..' not in p.parts,'unsafe-path')
            require((info.external_attr>>16)&0o170000 != 0o120000,'symlink')
        require(z.testzip() is None,'crc')
        m=json.loads(z.read('SOURCE_MANIFEST.json'))
        require(set(names)==set(m)|{'SOURCE_MANIFEST.json'},'membership')
        for name,pin in m.items():
            payload=z.read(name)
            require(len(payload)==pin['bytes'] and digest(payload)==pin['sha256'],'payload')
        return z.read(next(n for n in names if n.startswith('output/pdf/') and n.endswith('.pdf'))),len(names),len(m)
def alter_zip(data,kind):
    with zipfile.ZipFile(io.BytesIO(data)) as z:
        members=[(i,z.read(i.filename)) for i in z.infolist()]
    out=io.BytesIO()
    with warnings.catch_warnings():
        warnings.simplefilter('ignore',UserWarning)
        with zipfile.ZipFile(out,'w') as z:
            for i,payload in members:
                if i.filename=='README.md' and kind=='drop': continue
                if i.filename=='README.md' and kind=='payload':payload+=b'X'
                z.writestr(i,payload)
            if kind=='extra':z.writestr('unmanifested.txt',b'X')
            if kind=='duplicate':z.writestr(members[0][0],members[0][1])
            if kind=='unsafe':z.writestr('../escape.txt',b'X')
            if kind=='symlink':
                i=zipfile.ZipInfo('link');i.external_attr=0o120777<<16;z.writestr(i,b'/tmp/target')
    return out.getvalue()
def ledger(values,n,record,row):
    doi=f'https://doi.org/10.5281/zenodo.{record}'
    require(values[0]==['Original Problem','Solution Chat URL','DOI','Notes'],'columns')
    require(values[row-1][2]==doi,'row-doi')
    require(sum(str(c).count(doi) for r in values for c in r)==1,'doi-unique')
    require(f'/pull/{n}' in values[row-1][3],'row-pr')
    require(len(values[row-1])==4,'four-column-row')
def expect_failure(call,reason):
    try:call()
    except ValueError as e:
        require(str(e)==reason,'wrong-negative-diagnostic')
        return reason
    raise ValueError('negative-accepted')

result={'scope':'PR1141-1150 custody only; no universal proof or novelty claim','prs':[],'publications':[],'negative_controls':[]}
for n in range(1141,1151):
    cap=load(f'pr{n}/capture_receipt.json')
    pr=load(f'pr{n}/live_initial.json')
    disp=load(f'checkpoint/final_full_solution_sweep_20261020_01a15be7/PR{n}_DISPOSITION.json')
    cmp=load(f'pr{n}/comparison.json')
    require(cap['head']==disp['inventory_head_sha']==pr['head']['sha'],'head')
    require(cap['base']==disp['inventory_base_sha']==pr['base']['sha'],'base')
    require(cap['body_sha256']==disp['inventory_body_sha256']==digest((pr['body'] or '').encode()),'body')
    require(cap['changed_paths']==[f['filename'] for f in cmp['files']],'paths')
    require(not cap['queue_paths'],'queue')
    require(len(cap['payloads'])==len(cmp['files']),'complete-comparison')
    for f in cap['payloads']:
        b=(ROOT/pathlib.PurePosixPath(f['path']).relative_to('private')).read_bytes()
        require(len(b)==f['bytes'] and digest(b)==f['sha256'],'head-payload')
        require(hashlib.sha1(f'blob {len(b)}\0'.encode()+b).hexdigest()==f['git_blob_sha'],'git-blob')
    result['prs'].append({'pr':n,'files':len(cap['payloads']),'head':cap['head'],'body_sha256':cap['body_sha256'],'no_queue':True})
values=load('gws_initial.json')['values']
for n,record,row in [(1141,23443301,163),(1150,23444050,165)]:
    ledger(values,n,record,row)
    folder=ROOT/f'publication{n}'
    zfile=next(folder.glob('*.zip'));data=zfile.read_bytes()
    embedded,count,manifest=valid_zip(data)
    pdf=next(folder.glob('*.pdf')).read_bytes()
    require(embedded==pdf,'embedded-pdf')
    with zipfile.ZipFile(io.BytesIO(data)) as z:
        for f in (ROOT/f'pr{n}/head').rglob('*'):
            if f.is_file():
                require(any(pathlib.PurePosixPath(p).name==f.name and z.read(p)==f.read_bytes() for p in z.namelist()),'operative-edition')
    result['publications'].append({'pr':n,'members':count,'manifest_payloads':manifest,'source_sha256':digest(data),'pdf_sha256':digest(pdf),'ledger_row':row,'exact_operative_edition':True})
    for kind,diagnostic in [('payload','payload'),('drop','membership'),('extra','membership'),('duplicate','duplicate'),('unsafe','unsafe-path'),('symlink','symlink')]:
        result['negative_controls'].append({'pr':n,'mutation':kind,'rejected':expect_failure(lambda:valid_zip(alter_zip(data,kind)),diagnostic)})
    v=copy.deepcopy(values);v.append(copy.deepcopy(values[row-1]))
    result['negative_controls'].append({'pr':n,'mutation':'duplicate-doi-row','rejected':expect_failure(lambda:ledger(v,n,record,row),'doi-unique')})
print(json.dumps(result,sort_keys=True,indent=2))
