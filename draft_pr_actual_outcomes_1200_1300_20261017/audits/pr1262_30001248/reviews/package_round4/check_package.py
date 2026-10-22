#!/usr/bin/env python3
"""Independent archive, history, edition, and outside-anchor checks."""
import hashlib,html,json,os,pathlib,subprocess,sys,zipfile
H=pathlib.Path(__file__).resolve().parent;A=H.parent.parent;P=A/'publication'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def need(c,m):
    if not c:raise ValueError(m)
def save(n,j):(H/n).write_text(json.dumps(j,indent=2)+'\n')
def binding(p):return dict(bytes=p.stat().st_size,sha256=sha(p))
b=json.loads((P/'BUILD_RECEIPT.json').read_text());c=json.loads((A/'CURRENT_PR1262_CONTEXT.json').read_text())
need(sha(A/'CURRENT_PR1262_CONTEXT.json')=='aebb00ec598c1e459e15a2006bafba9711d1bb6cf6bb91dccd7b2502d01476eb','context')
for k in ('pdf','verification_zip'):need(binding(P/b[k]['path'])=={q:b[k][q] for q in ('bytes','sha256')},k)
root=H/'_local'/'extracted';root.mkdir(parents=True,exist_ok=True)
with zipfile.ZipFile(P/b['verification_zip']['path']) as z:
    names=z.namelist();need(len(names)==203 and len(set(names))==203,'203 unique members')
    for n in names:
        rel=pathlib.PurePosixPath(n);need(not rel.is_absolute() and '..' not in rel.parts and str(rel)==n,'safe lexical zip')
        need(z.read(n)==(P/'verification'/n).read_bytes(),'actual tree identical '+n)
    z.extractall(root)
m=json.loads((root/'MANIFEST.json').read_text());need(len(m['files'])==202,'202 nonself root records')
need(sha(root/'MANIFEST.json')==b['verification_anchors']['manifest'],'outside manifest anchor')
allnames={'MANIFEST.json'}
for e in m['files']:
    need(e['path'] not in allnames,'duplicate root member');allnames.add(e['path']);need(binding(root/e['path'])=={k:e[k] for k in ('bytes','sha256')},e['path'])
need(set(names)==allnames,'closed archive inventory')
registries=[]
for reg in c['authored_freezes']:
    q=root/reg['path'];need(sha(q)==reg['sha256'],'registry anchor');obj=json.loads(q.read_text());entries=obj[reg['entries_key']];seen=set()
    for e in entries:
        n=e[reg['path_key']];need(n not in seen,'duplicate family member');seen.add(n)
        need(not pathlib.PurePosixPath(n).is_absolute() and '..' not in pathlib.PurePosixPath(n).parts,'relative selected key')
        need(binding(root/reg['base']/n)==dict(bytes=e[reg['size_key']],sha256=e['sha256']),'family member')
    registries.append(dict(path=reg['path'],entries=len(entries),selected_schema=[reg[k] for k in ('entries_key','path_key','size_key')]))
need(len(registries)==14,'14 explicit registries');need(registries[3]['selected_schema']==['entries','relative_path','bytes'],'Fourier exact selected schema')
wrappers=[]
for n in ('ACCEPTANCE.json','SOURCES.json','VERIFICATION.json'):
    old=json.loads((A/'submitted'/n).read_text());new=json.loads((A/'current_edition'/n).read_text());need(new['historical_submitted_record_20261011']==old,'v3 historical parsed record exact '+n)
    wrappers.append(n)
hist=A/'release_history/pre_html_escape_20261017';baseline=json.loads((A/'DRAFT_REPAIR_BASELINE.json').read_text())
for n,entry in baseline['history'].items():need(binding(hist/n)==entry,'old release history '+n)
old=json.loads((hist/'zenodo-deposit.json').read_text());new=json.loads((P/'zenodo-deposit.json').read_text());need(set(new['metadata'])==set(old['metadata']) and len(new['metadata'])==11,'11 metadata')
need(all(new['metadata'][k]==old['metadata'][k] for k in new['metadata'] if k!='description'),'only description changes')
need(html.unescape(new['metadata']['description'])==html.unescape(old['metadata']['description']),'unescaped content identical')
need(new['metadata']['description']==old['metadata']['description'].replace('n>=3','n&gt;=3').replace('n>=4','n&gt;=4'),'exact entity change only')
need(new['metadata']==c['metadata'],'metadata current context exact')
need(not (P/'FINAL_REVIEW_GATE.json').exists(),'actual new final gate absent during review')
need(not (P/'PUBLICATION_RECEIPT.json').exists() and not (P/'PUBLISH_INTENT.json').exists(),'no actual local publication claims')
save('PACKAGE_AUTHENTICATION.json',dict(status='PASS',archive_members=203,root_nonself_members=202,nested_registries=registries,structured_wrappers_exact=wrappers,history_all_baseline_entries_exact=True,metadata_11_fields_exact=True,metadata_html_only_two_entities=True,actual_new_final_gate_absent=True,portable_anchors=b['verification_anchors']))
env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',TMPDIR=str(H/'_local'))
args=[a for k,v in b['verification_anchors'].items() for a in ['--expected-'+k+'-sha256',v]]
for label,flags in [('normal',[]),('O',['-O']),('OO',['-OO'])]:
    run=subprocess.run([sys.executable,'-B',*flags,str(root/'verify.py'),*args],env=env,capture_output=True,text=True)
    (H/('PORTABLE_'+label+'.json')).write_text(run.stdout);(H/'_local'/('portable_'+label+'.stderr')).write_text(run.stderr)
    need(run.returncode==0,'portable replay '+label+' '+run.stderr)
print('PASS archive authentication and extracted verifier normal/-O/-OO')
