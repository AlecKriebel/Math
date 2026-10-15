#!/usr/bin/env python3
"""Independent sealed-R5 archive, exact-input, source-blob and rebuild checks."""
from pathlib import Path, PurePosixPath
import hashlib, io, json, stat, subprocess, zipfile, shutil
HERE=Path(__file__).resolve().parent
BASE=HERE.parent
EXTRACTED=HERE/'verification_extracted'
checks=[]
def need(t,s):
    if not t: raise RuntimeError(s)
def h(raw):return hashlib.sha256(raw).hexdigest()
def record(s,**kw): checks.append(dict(check=s,passed=True,**kw))
def archive(raw,label):
    with zipfile.ZipFile(io.BytesIO(raw)) as z:
        names=z.namelist();need(len(names)==len(set(names)),label+' duplicates')
        need(not z.comment,label+' comment')
        data={}
        for i in z.infolist():
            n=i.filename;parts=n.split('/');m=i.external_attr>>16
            need(not PurePosixPath(n).is_absolute() and all(v not in ('','.','..') for v in parts) and '\\' not in n and ':' not in n and not any(ord(c)<32 for c in n),label+' path '+n)
            need(i.create_system==3 and stat.S_ISREG(m) and not m&0o111 and not i.flag_bits&1,label+' mode '+n)
            data[n]=z.read(i)
            need(len(data[n])==i.file_size,label+' size '+n)
            if n.endswith(('.md','.json','.py','.tex')):data[n].decode('utf-8')
            if n.endswith('.json'):json.loads(data[n])
    record('archive structural safety',archive=label,members=len(data))
    return data

def manifest(data,n,label,closed=True):
    m=json.loads(data[n]);rows=m.get('files',m.get('inventory'));need(isinstance(rows,list),label+' rows')
    prefix=n.rsplit('/',1)[0]+'/' if '/' in n else ''
    rows_paths=[prefix+r['path'] for r in rows]
    need(len(rows_paths)==len(set(rows_paths)),label+' duplicate manifest paths')
    if closed:need(set(rows_paths)=={a for a in data if a.startswith(prefix)}-{n},label+' inventory closure')
    for r,name in zip(rows,rows_paths):
        need(name in data,label+' missing '+name);raw=data[name]
        need(len(raw)==r['bytes'] and h(raw)==r['sha256'],label+' hash/size '+name)
        if 'git_blob_sha' in r:
            need(hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()==r['git_blob_sha'],label+' git hash '+name)
    record('manifest identities and closure',archive=label,manifest=n,members=len(rows))
    return m

raw=(BASE/'preprint/verification.zip').read_bytes();d=archive(raw,'verification.zip')
for n in d:
    if n.rsplit('/',1)[-1] in ('MANIFEST.json','PUBLIC_AUDIT_MANIFEST.json'):manifest(d,n,'verification.zip')
for key,folder in [('AUTHOR','author'),('INDEPENDENT_AUDIT','independent_audit'),('SECOND_ADVERSARIAL_REVIEW','second_review')]:
    e=json.loads(d['source/FUNCTION_THEORY_2307042_'+key+'_EXTERNAL_MANIFEST.json']);a=d['source/'+e['archive']]
    need(h(a)==e['archive_sha256'] and len(a)==e['archive_bytes'],key+' external archive pin')
    inner=archive(a,e['archive']);need(set(inner)=={r['path'] for r in e['inventory']},key+' external closure')
    for r in e['inventory']:need(h(inner[r['path']])==r['sha256'] and len(inner[r['path']])==r['bytes'],key+' external member pin')
    for n in inner:
        if n.rsplit('/',1)[-1]=='MANIFEST.json':manifest(inner,n,e['archive'])
    need(inner=={n.removeprefix('source/'+folder+'/'):v for n,v in d.items() if n.startswith('source/'+folder+'/')},key+' expanded bytes differ')
    record('nested archive matches expanded tree',kind=key)

selection=json.loads(d['preprint/supplement_selection.json']);public=['note.tex','README.md','build_package.py','zenodo-metadata.json','supplement_selection.json']
expected={'preprint/'+n for n in public}|{i.get('archive_path',i['path']) for i in selection}|{'MANIFEST.json'}
need(set(d)==expected,'selection inventory differs')
for n in public:need(d['preprint/'+n]==(BASE/'preprint'/n).read_bytes(),'public exact input '+n)
for i in selection:need(d[i.get('archive_path',i['path'])]==(BASE/i['path']).read_bytes(),'selected source '+i['path'])
record('outer exact closed selection',members=len(d))

source=json.loads(d['SOURCE_MANIFEST.json']);need(source['head']=='5820e9784dbcfeda0acabaa435cb38cf6a4576df' and source['pr']==810,'source pin')
for r in source['files']:
    src=d['source/'+r['snapshot_path']];need(len(src)==r['bytes'] and h(src)==r['sha256'],'source snapshot hash '+r['snapshot_path'])
    got=subprocess.run(['git','show',source['head']+':'+r['source_path']],capture_output=True,check=True).stdout
    need(got==src,'original immutable source git blob '+r['source_path'])
record('all original source manifest blobs verified against Git object',members=len(source['files']))

kit=archive((BASE/'preprint/zenodo-upload-kit.zip').read_bytes(),'zenodo-upload-kit.zip')
need(set(kit)=={'annular-martin-kernel-note.pdf','annular-martin-kernel-verification.zip','zenodo-metadata.json','zenodo-deposit.json'},'kit closure')
need(kit['annular-martin-kernel-verification.zip']==raw,'kit supplement bytes')
need(kit['annular-martin-kernel-note.pdf']==(BASE/'preprint/output/pdf/note.pdf').read_bytes(),'kit PDF bytes')
need(kit['zenodo-metadata.json']==d['preprint/zenodo-metadata.json'],'kit metadata bytes')
meta=json.loads(kit['zenodo-metadata.json']);dep=json.loads((BASE/'preprint/zenodo-deposit.json').read_bytes());kdep=json.loads(kit['zenodo-deposit.json']);need(dep['metadata']==meta==kdep['metadata'],'metadata equality')
need(dep['files']==[{'path':'output/pdf/note.pdf','name':'annular-martin-kernel-note.pdf'},{'path':'verification.zip','name':'annular-martin-kernel-verification.zip'}],'deposit file schema')
need(kdep['files']==[{'path':'annular-martin-kernel-note.pdf'},{'path':'annular-martin-kernel-verification.zip'}],'kit deposit file schema')
need(meta['creators'][0]['orcid']=='0009-0001-9320-500X' and meta['license']=='cc-by-4.0' and meta['publication_type']=='preprint','metadata core')
record('exact kit and metadata equality')

clean=HERE/'tmp/clean_rebuild';clean.mkdir(parents=True,exist_ok=True)
for n,v in d.items():
    p=clean/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(v)
out=clean/'preprint/output/pdf';out.mkdir(parents=True,exist_ok=True)
# The builder takes a prebuilt PDF. First test exact kit assembly with the sealed PDF.
shutil.copyfile(BASE/'preprint/output/pdf/note.pdf',out/'note.pdf')
r=subprocess.run(['python3','build_package.py'],cwd=clean/'preprint',capture_output=True,text=True,check=True)
for n in ['verification.zip','zenodo-deposit.json','zenodo-upload-kit.zip']:
    need((clean/'preprint'/n).read_bytes()==(BASE/'preprint'/n).read_bytes(),'clean exact build '+n)
record('clean extracted archive assembly byte-identical',stdout=r.stdout.strip())
# Independent compilation source equality, page count/text is checked separately.
need((HERE/'tmp/compiled/note.tex').read_bytes()==d['preprint/note.tex'],'isolated compile source')
record('isolated compilation consumed sealed source')
(HERE/'ARCHIVE_AUDIT_RESULT.json').write_text(json.dumps({'all_passed':True,'checks':checks},indent=2)+'\n')
print(json.dumps({'all_passed':True,'checks':len(checks),'source_blobs':len(source['files']),'verification_members':len(d)},indent=2))
