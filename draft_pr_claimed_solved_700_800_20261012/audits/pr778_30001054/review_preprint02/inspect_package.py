"""Read every distribution member and validate bytes, forms, and bindings."""
from pathlib import Path,PurePosixPath
import ast,hashlib,io,json,re,stat,sys,zipfile

base=Path(sys.argv[1]);pins=json.loads(Path(sys.argv[2]).read_text())['six']
def need(c,m):
    if not c:raise ValueError(m)
def identity(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def unique(pairs):
    d={}
    for k,v in pairs:need(k not in d,'duplicateJSONkey');d[k]=v
    return d
def json_read(b):
    def bad(x):raise ValueError('nonfiniteJSON')
    return json.loads(b.decode(),object_pairs_hook=unique,parse_constant=bad)
for n,pin in pins.items():need(identity((base/n).read_bytes())==pin,'six:'+n)
with zipfile.ZipFile(base/'source-and-verification.zip') as z:
    infos=z.infolist();need(len(infos)==123,'membercount');names=[x.filename for x in infos]
    need(names==sorted(set(names)),'namesorder/duplicate')
    source={};rows=[]
    for i in infos:
        n=i.filename
        need(n==str(PurePosixPath(n)) and not n.startswith('/') and '\\' not in n and all(p not in ('','.','..') for p in n.split('/')),'path')
        need(i.external_attr>>16==0o100644 and i.date_time==(2026,10,16,0,0,0) and i.compress_type==zipfile.ZIP_DEFLATED,'zipform')
        b=z.read(i);source[n]=b
        kind='nestedZIP' if n.endswith('.zip') else 'utf8text'
        if kind!='nestedZIP':b.decode()
        if n.endswith('.json'):json_read(b);kind='JSON'
        if n.endswith('.py'):ast.parse(b.decode());kind='Python'
        rows.append({'path':n,**identity(b),'kind':kind})
manifest=json_read(source['MANIFEST.json'])
expected={x['path']:{k:x[k] for k in ('bytes','sha256')} for x in manifest['files']}
need(set(expected)==set(source)-{'MANIFEST.json'},'closednames')
for n,x in expected.items():need(identity(source[n])==x,'closedbytes:'+n)
need(source['paper.tex']==(base/'paper.tex').read_bytes(),'tex')
bindings=json_read(source['PREPRINT_BINDINGS.json'])
need(bindings['paper.tex']==pins['paper.tex'] and bindings['paper.pdf']==pins['output/pdf/paper.pdf'],'paperbindings')
snapshot=json_read(source['audit/SNAPSHOT.json']);need(len(snapshot['files'])==32,'original32')
original=[]
for x in snapshot['files']:
    name='audit/original/'+x['path'];need(identity(source[name])=={k:x[k] for k in ('bytes','sha256')},'originalbytes');original.append(name)
need({n for n in source if n.startswith('audit/original/')}==set(original),'originalclosure')
nested=[]
for n,b in source.items():
    if n.endswith('.zip'):
        with zipfile.ZipFile(io.BytesIO(b)) as z:
            folder='review' if 'FRESH' in n else 'audit';prefix=n.rsplit('/archives/',1)[0]+'/'+folder+'/'
            entries=z.infolist();need(len(entries)==(7 if folder=='review' else 14),'nestedcount')
            need(len(set(x.filename for x in entries))==len(entries),'nestedduplicate')
            for i in entries:need(z.read(i)==source[prefix+i.filename],'nestedbytes')
            nested.append({'name':n,'members':[{'path':i.filename,**identity(z.read(i))} for i in entries]})
with zipfile.ZipFile(base/'zenodo-upload-kit.zip') as z:
    kit={i.filename:z.read(i) for i in z.infolist()}
    need(set(kit)=={'README.md','paper.pdf','source-and-verification.zip','zenodo-deposit.json','zenodo-metadata.json'} and len(z.infolist())==5,'kitmembers')
need(kit['paper.pdf']==(base/'output/pdf/paper.pdf').read_bytes(),'kitpdf')
need(kit['source-and-verification.zip']==(base/'source-and-verification.zip').read_bytes(),'kitsource')
metadata=json_read((base/'zenodo-metadata.json').read_bytes())
need(metadata==json_read(source['zenodo-metadata.json'])==json_read(kit['zenodo-metadata.json']),'metadataequal')
for d in [json_read((base/'zenodo-deposit.json').read_bytes()),json_read(kit['zenodo-deposit.json'])]:need(d['metadata']==metadata['metadata'],'depositmetadata')
need(json_read((base/'zenodo-deposit.json').read_bytes())['files']==[{'path':'output/pdf/paper.pdf','name':'paper.pdf'},{'path':'source-and-verification.zip','name':'source-and-verification.zip'}],'depositmapping')
need(json_read(kit['zenodo-deposit.json'])['files']==[{'path':'paper.pdf'},{'path':'source-and-verification.zip'}],'kitmapping')
m=metadata['metadata'];need(m['creators']==[{'name':'Kriebel, Alec','affiliation':'Independent researcher','orcid':'0009-0001-9320-500X'}],'creator')
need(m['license']=='cc-by-4.0' and m['publication_type']=='preprint' and m['version']=='1.0' and m['publication_date']=='2026-10-16','metadatavalues')
need('unrefereed' in m['description'] and 'AI tools were used extensively' in m['description'] and 'firstness' in m['description'],'disclosures')
need(not any(n.lower().endswith(('.pdf','.pem','.key','.env')) for n in source),'unexpectedbody/secretfile')
need(not any(re.search(r'(?<![A-Za-z0-9_])(?:sk-proj-|ghp_)[A-Za-z0-9_-]{20,}',b.decode(errors='ignore')) for b in source.values()),'credentialpattern')
print(json.dumps({'status':'PASS','all_six_unchanged':True,'members':rows,'original_files':original,'nested':nested,'metadata':metadata,'kit_members':sorted(kit),'content_screen':'All123 read; allUTF8/JSON/Python parse; no third-partyPDF/fullpaper-body file or credential token discovered. Historical source excerpts/citations are retained as authored analysis, not licensed as third-party bodies.','scope':'Structural/identity/content-screen checks support but do not replace semantic reading of paper, operative qualifications, source comparison and actual algorithms.'},indent=2))
