"""Fresh-main checkpoint of prepared PR209 scientific package and genuine ZIP replays."""
from pathlib import Path
import ast,hashlib,json
D=Path(__file__).resolve().parent
# Reconstruct the already inspected 35% publisher without executing any of it.
p=D/'publish_progress_35.py';tree=ast.parse(p.read_text());assert isinstance(tree.body[-1],ast.Expr) and isinstance(tree.body[-2],ast.Assert)
tree.body=tree.body[:-2];ns={'__file__':str(p)};exec(compile(tree,str(p)+'[definition-only]','exec'),ns);source=ns['source']
assert not (D/'PROGRESS_45_CHECKPOINT_RECEIPT.json').exists()
extra="""B=D.parent/'preprint'
obj=json.loads((B/'SOURCE_MANIFEST.json').read_text())
for row in obj['files']:
    p=B/row['path'];raw=p.read_bytes()
    assert len(raw)==row['bytes'] and hashlib.sha256(raw).hexdigest()==row['sha256']
    paths.append(p)
paths += [B/n for n in ['SOURCE_MANIFEST.json','PACKAGE_MANIFEST.json','deposit.json','k303b-source-verification.zip']]
R=D/'root_reproduction_04_portable_zip_01/executed'
paths.append(R/'REPRODUCTION.json')
for folder in R.iterdir():
    if folder.is_dir():
        for p in folder.rglob('*'):
            if p.is_file() and 'inputs' not in p.relative_to(folder).parts:
                paths.append(p)
"""
readback="""run=subprocess.run([GH,'api',BASE+'git/blobs/'+hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\\0'+raw).hexdigest()],capture_output=True,timeout=90)
    assert run.returncode==0
    obj=json.loads(run.stdout)
    assert obj['sha']==hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\\0'+raw).hexdigest()
    assert obj.get('encoding')=='base64' and base64.b64decode(obj['content'])==raw"""
start=source.index("    run=subprocess.run([GH,'api',BASE+'contents/'+rel+'?ref='+new]")
end=source.index("    return dict(path=rel",start)
source=source[:start]+'    '+readback+ '\n'+source[end:]
changes=[
("OUT=D/'PROGRESS_35_CHECKPOINT_RECEIPT.json'","OUT=D/'PROGRESS_45_CHECKPOINT_RECEIPT.json'"),
("prior=json.loads((D/'PROGRESS_25_CHECKPOINT_RECEIPT.json').read_text())","prior=json.loads((D/'PROGRESS_35_CHECKPOINT_RECEIPT.json').read_text())"),
("assert prior['commit']=='80ca3a950e762ee4a10fbaaa19ebecd06399bba1'","assert prior['commit']=='f9862f73ca1589941876b0c2ebad0782ffbb4894'"),
("assert state['completion_percent']==35 and state['preprint_preparation_cleared'] is True","assert state['completion_percent']==45 and state['preprint_preparation_cleared'] is True"),
("strftime('progress35_%Y%m%dT%H%M%S%fZ')","strftime('progress45_%Y%m%dT%H%M%S%fZ')"),
("paths += [OLD/'FINAL_COMPLETION_CHECKPOINT_PUBLICATION_RECEIPT.json'",extra+"paths += [OLD/'FINAL_COMPLETION_CHECKPOINT_PUBLICATION_RECEIPT.json'"),
("assert len(entries)<250","assert len(entries)<600"),
("Checkpoint PR209 at35%: qualified priority audit, exact contemporary and classical credit, writing clearance","Checkpoint PR209 at45%: credited five-page note and verified portable package, first whole-package review active"),
("case_completion_percent=35","case_completion_percent=45"),
]
for old,new in changes:
 assert source.count(old)==1,old;source=source.replace(old,new)
exec(compile(source,str(D/'publish_progress_45.py')+'[pinned-template]','exec'),{'__file__':str(D/'publish_progress_45.py'),'__name__':'__main__'})
