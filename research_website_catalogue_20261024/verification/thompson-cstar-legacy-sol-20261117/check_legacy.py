"""Fresh passive Thompson-note identity audit; writes only its new verification lane."""
import base64, datetime, hashlib, json, stat, subprocess, sys, time
from html.parser import HTMLParser
from pathlib import Path
M=Path('/Users/alec/Documents/Math');P=M/'research_website_catalogue_20261024'
OWN=P/'verification/thompson-cstar-legacy-sol-20261117'
SRC=P/'papers/23204212/sources';WRITER=P/'verification/thompson-cstar-editorial-sol-20261117'
NATIVE='a4ce3c37dad209339e490d18dcced6c48cf912d2';RELEASE='2d020358e466323f2f188ee84aa2ff1a535bed8c'
NTREE='6ccfd5ab446400dc7fb3933dcc2e374cb415fa90';RTREE='e63ba1f227e5aa2f0e06fd6a52b36afa1531a4d0'
GIT=['/usr/bin/git','--no-optional-locks','-c','core.hooksPath=/dev/null','-c','core.fsmonitor=false','-C',str(M)]
assert sys.argv[1:] in (['intake'],['close'],['freeze'])
phase=sys.argv[1];calls=[]
def utc():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def encoded(x):return (json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode()
def save(name,x):
    with (OWN/name).open('xb') as f:f.write(encoded(x))
def load(p):return json.loads(p.read_bytes())
def pin(p):
    a=p.lstat();assert stat.S_ISREG(a.st_mode) and not p.is_symlink()
    raw=p.read_bytes();b=p.lstat();key=lambda s:(s.st_dev,s.st_ino,s.st_mode,s.st_size,s.st_mtime_ns,s.st_ctime_ns)
    assert key(a)==key(b) and len(raw)==a.st_size
    return {'bytes':len(raw),'SHA256':hashlib.sha256(raw).hexdigest(),'MD5':hashlib.md5(raw).hexdigest(),'mode':oct(stat.S_IMODE(a.st_mode))}
def census(root):
    assert root.is_dir() and not root.is_symlink()
    files={};dirs={'.':oct(stat.S_IMODE(root.lstat().st_mode))};todo=[root]
    while todo:
        here=todo.pop();a=here.lstat()
        for p in sorted(here.iterdir()):
            n=p.relative_to(root).as_posix();s=p.lstat();assert not p.is_symlink()
            if stat.S_ISDIR(s.st_mode):dirs[n]=oct(stat.S_IMODE(s.st_mode));todo.append(p)
            else:files[n]=pin(p)
        b=here.lstat();assert (a.st_dev,a.st_ino,a.st_mode,a.st_mtime_ns,a.st_ctime_ns)==(b.st_dev,b.st_ino,b.st_mode,b.st_mtime_ns,b.st_ctime_ns)
    paths=set(files)|set(dirs)
    return {'root':str(root),'root_mode':dirs['.'],'files':files,'directories':{n:m for n,m in dirs.items() if n!='.'},'hidden_paths':sorted(n for n in paths if n!='.' and any(s.startswith('.') for s in n.split('/'))),'empty_files':sorted(n for n,p in files.items() if p['bytes']==0),'empty_directories':sorted(n for n in dirs if n!='.' and not any(x.startswith(n+'/') for x in paths))}
def run(argv,allowed=(0,)):
    stem=f'{phase}-call-{len(calls):03d}';start=utc();t=time.monotonic();r=subprocess.run(argv,capture_output=True)
    (OWN/(stem+'.stdout.bin')).write_bytes(r.stdout);(OWN/(stem+'.stderr.bin')).write_bytes(r.stderr)
    item={'argv':argv,'started_UTC':start,'finished_UTC':utc(),'elapsed_seconds':time.monotonic()-t,'exit':r.returncode,'stdout_bytes':len(r.stdout),'stderr_bytes':len(r.stderr),'stdout':stem+'.stdout.bin','stderr':stem+'.stderr.bin'}
    calls.append(item);save(stem+'.invocation.json',item)
    assert r.returncode in allowed,(argv,r.returncode,r.stderr.decode(errors='replace'))
    return r.stdout
def git(*args):return run(GIT+list(args))
def snapshot():
    logical=git('for-each-ref','--format=%(refname)%00%(objectname)','refs/heads').decode()
    native={'HEAD_commit':git('rev-parse','HEAD').decode().strip(),'HEAD_raw_base64':base64.b64encode((M/'.git/HEAD').read_bytes()).decode(),'controls':{n:pin(M/'.git'/n) for n in ('HEAD','index','config')},'logical_local_heads':logical,'loose_local_heads':census(M/'.git/refs/heads') if (M/'.git/refs/heads').exists() else {'exists':False}}
    if (M/'.git/config.worktree').exists():native['controls']['config.worktree']=pin(M/'.git/config.worktree')
    assert native['HEAD_commit']==NATIVE
    assert git('rev-parse','HEAD:docs').decode().strip()==NTREE and git('rev-parse',RELEASE+':docs').decode().strip()==RTREE
    return {'UTC':utc(),'native':native,'physical_docs':census(M/'docs'),'sources':census(SRC),'writer':census(WRITER),'identity_notes':{str(p.relative_to(P)):pin(p) for p in (P/'verification/root-clearance-23204212-20261117.json',P/'papers/23204212/reviews/root-continuation-20261117/ROOT_REVIEW.md')},'observed_local_remote_tracking_main':git('rev-parse','refs/remotes/origin/main').decode().strip()}
def validate(s):
    source=s['sources'];sf=load(SRC/'SOURCE_FINAL.json');sm=load(SRC/'SOURCE_MANIFEST.json')
    assert len(source['files'])==sf['regular_files']==55 and len(source['directories'])==sf['child_directories']==14
    assert source['files']['SOURCE_FINAL.json']['SHA256']=='b68fbb425b7d910a2508c46ff311491a1c797568dcf39d3c7deb0a0545e1afd5'
    assert source['files']['SOURCE_MANIFEST.json']['SHA256']==sf['manifest']['SHA256']=='afa64c126da0aabc4a44ec242553e5b2354540eb1b0b60e55ab7b1a9855a09be'
    expected={r['path']:{'bytes':r['bytes'],'SHA256':r['sha256'],'MD5':r['md5'],'mode':r['mode_octal']} for r in sm['entries'] if r['kind']=='file'}
    assert len(expected)==sm['file_count']==53 and expected=={n:p for n,p in source['files'].items() if n not in ('SOURCE_FINAL.json','SOURCE_MANIFEST.json')}
    assert {r['path']:r['mode_octal'] for r in sm['entries'] if r['kind']=='directory'}==dict(source['directories'],**{'.':source['root_mode']})
    w=s['writer'];wm=load(WRITER/'MANIFEST.json');ws=load(WRITER/'SEAL.json')
    assert len(w['files'])==wm['file_count']==ws['file_count']==27 and len(w['directories'])==wm['child_directory_count']==1
    assert w['files']['MANIFEST.json']['SHA256']==ws['manifest_sha256']=='4c5cb453d5fec1544e0b6556b5d858c059657f24dd547b161358f40e14314a55'
    assert w['files']['FINAL.json']['SHA256']==ws['FINAL_sha256']=='36c84f224773aa954a4e59a3152b2089e60c95710e88a12231931c646b1e8557'
    for r in wm['entries']:
        if r['kind']=='file' and r['path'] not in ('MANIFEST.json','SEAL.json'):
            v=w['files'][r['path']];assert (v['bytes'],v['SHA256'],v['mode'])==(r['bytes'],r['sha256'],r['mode_octal'])
        elif r['kind']=='directory':assert (w['root_mode'] if r['path']=='.' else w['directories'][r['path']])==r['mode_octal']
    model=load(WRITER/'MODEL.json')
    for name,digest in model['input_pins'].items():
        if name.startswith(str(P)) and name in (str(P/'verification/root-clearance-23204212-20261117.json'),str(P/'papers/23204212/reviews/root-continuation-20261117/ROOT_REVIEW.md')):assert s['identity_notes'][str(Path(name).relative_to(P))]['SHA256']==digest
class ArticleText(HTMLParser):
    def __init__(self):super().__init__(convert_charrefs=True);self.skip=0;self.text=[];self.links=[]
    def handle_starttag(self,tag,attrs):
        if tag in ('script','style'):self.skip+=1
        if tag in ('title','h1','h2','h3','p','div','li','section','br'):self.text.append('\n')
        self.links.extend(v for k,v in attrs if k in ('href','src') and v)
    def handle_endtag(self,tag):
        if tag in ('script','style'):self.skip-=1
        if tag in ('title','h1','h2','h3','p','div','li','section'):self.text.append('\n')
    def handle_data(self,data):
        if not self.skip:self.text.append(data)
def tree(commit,label):
    raw=git('ls-tree','-r','-t','-z','--full-tree',commit,'docs');rows=[]
    for part in raw.split(b'\0'):
        if not part:continue
        h,n=part.split(b'\t',1);mode,kind,oid=h.decode().split();path=n.decode();assert path=='docs' or path.startswith('docs/')
        rows.append({'path':path,'mode':mode,'type':kind,'OID':oid})
    assert len({r['path'] for r in rows})==len(rows);save(label+'-TREE.json',{'commit':commit,'docs_tree':NTREE if label=='native' else RTREE,'rows':rows});return rows
if phase=='intake':
    s=snapshot();validate(s);save('GUARD_BEFORE.json',s);model=load(WRITER/'MODEL.json');assets=[]
    for a in model['native_assets_in_original_order']:
        name=a['native_filename'];p=SRC/'zenodo-files'/name;raw=p.read_bytes();v=pin(p)
        assert v['bytes']==a['bytes'] and v['SHA256']==a['sha256'] and v['MD5']==a['md5'] and pin(WRITER/'private-page'/name)==v
        assets.append({'ordinal':a['ordinal'],'native_filename':name,'identity':v,'Git_blob_OID':hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()})
    pattern=r'Thompson|non.?amenab|23204212|thompson-cstar|commensurat|Le Boudec|Matte Bon';candidates=[];spaces={};(OWN/'candidates').mkdir()
    for label,commit in (('physical',None),('native',NATIVE),('released',RELEASE)):
        rows=None if commit is None else tree(commit,label)
        if commit is None:
            raw=run(['/Applications/ChatGPT.app/Contents/Resources/codex-cli/codex-path/rg','-l','-0','-i','--hidden','--no-ignore','--glob','*.html','--glob','*.htm','-e',pattern,str(M/'docs')],allowed=(0,1))
            paths=[Path(n.decode()).relative_to(M).as_posix() for n in raw.split(b'\0') if n]
            count=sum(n.lower().endswith(('.html','.htm')) for n in s['physical_docs']['files'])
            matches=[{'asset':a['native_filename'],'path':'docs/'+n} for n,p in s['physical_docs']['files'].items() for a in assets if p['bytes']==a['identity']['bytes'] and p['SHA256']==a['identity']['SHA256']]
        else:
            raw=run(GIT+['grep','-l','-z','-i','-I','-E','-e',pattern,commit,'--',':(glob)docs/**/*.html',':(glob)docs/**/*.htm'],allowed=(0,1))
            paths=[n.decode().removeprefix(commit+':') for n in raw.split(b'\0') if n];assert all(n.startswith('docs/') for n in paths)
            count=sum(r['type']=='blob' and r['path'].lower().endswith(('.html','.htm')) for r in rows)
            matches=[{'asset':a['native_filename'],'path':r['path'],'OID':r['OID']} for r in rows if r['type']=='blob' for a in assets if r['OID']==a['Git_blob_OID']]
            for match in matches:
                b=git('cat-file','blob',match['OID']);a=next(a for a in assets if a['native_filename']==match['asset']);assert len(b)==a['identity']['bytes'] and hashlib.sha256(b).hexdigest()==a['identity']['SHA256']
        assert len(paths)==len(set(paths));spaces[label]={'commit':commit,'HTML_files':count,'blob_leaves':len(s['physical_docs']['files']) if rows is None else sum(r['type']=='blob' for r in rows),'candidate_paths':sorted(paths),'exact_whole_asset_matches':matches}
        for name in sorted(paths):
            b=(M/name).read_bytes() if commit is None else git('show',commit+':'+name);text=b.decode('utf-8');number=f'{len(candidates)+1:03d}';h='candidates/'+number+'.html';t='candidates/'+number+'.txt';(OWN/h).write_bytes(b)
            parser=ArticleText();parser.feed(text);parser.close();(OWN/t).write_text(''.join(parser.text)+'\n',encoding='utf-8')
            strong=[v for v in (model['title'],model['doi'],'23204212','thompson-cstar-verification','thompson-cstar-source') if v.casefold() in text.casefold()]
            candidates.append({'namespace':label,'path':name,'bytes':len(b),'SHA256':hashlib.sha256(b).hexdigest(),'HTML':h,'full_visible_text':t,'all_links':parser.links,'strong_identity_tokens':strong})
    diff=git('diff','--no-ext-diff','--no-textconv','--raw','--no-abbrev',NATIVE,RELEASE,'--','docs').decode()
    save('IDENTITY_SEARCH.json',{'UTC':utc(),'title':model['title'],'DOI':model['doi'],'native_assets':assets,'pattern':pattern,'namespaces':spaces,'candidates':candidates,'native_released_raw_diff':diff,'bounds':'Only current physical docs and these two exact Git docs trees; no live/remote refresh/global-history inference.'});save('INTAKE_CALLS.json',calls)
    print(json.dumps({'status':'INTAKE_COMPLETE','namespaces':spaces,'candidate_copies':len(candidates),'unique_candidate_HTMLs':len({r['SHA256'] for r in candidates}),'physical_docs_files_childdirs':[len(s['physical_docs']['files']),len(s['physical_docs']['directories'])]}))
elif phase=='close':
    s=snapshot();validate(s);save('GUARD_AFTER.json',s);before=load(OWN/'GUARD_BEFORE.json')
    for key in ('native','physical_docs','sources','writer','identity_notes'):assert s[key]==before[key],key
    save('CLOSING_CALLS.json',calls);save('CUSTODY_RESULT.json',{'UTC':utc(),'status':'EXACT_PROTECTED_NAMESPACES','sources':[55,14],'writer':[27,1],'physical_docs':[len(s['physical_docs']['files']),len(s['physical_docs']['directories'])],'all_bytes_modes_hidden_empty_topology_exact':True,'remote_tracking_before':before['observed_local_remote_tracking_main'],'remote_tracking_after':s['observed_local_remote_tracking_main'],'remote_tracking_outside_exact_guard':True});print('Complete protected namespaces exact; no W access or native Git mutation.')
else:
    assert load(OWN/'CUSTODY_RESULT.json')['status']=='EXACT_PROTECTED_NAMESPACES';names=('FINAL_MANIFEST.json','FINAL.json')
    for n in names:
        with (OWN/n).open('xb'):pass
    c=census(OWN);files={n:p for n,p in c['files'].items() if n not in names};modes={n:c['files'][n]['mode'] for n in names};now=utc()
    manifest={'schema':'finite-legacy-correspondence-whole-namespace-v1','UTC':now,'root':str(OWN),'root_mode':c['root_mode'],'file_count':len(files)+2,'child_directory_count':len(c['directories']),'payload_files':files,'directories':c['directories'],'hidden_paths':c['hidden_paths'],'empty_files':sorted(n for n,p in files.items() if p['bytes']==0),'empty_directories':c['empty_directories'],'terminal_pair':[{'path':n,'bytes':0,'mode':modes[n],'recursive_hash_excluded':True} for n in names]}
    final={'schema':'bounded-Thompson-legacy-FINAL-v1','UTC':now,'record':'23204212','status':'FROZEN_COMPLETE','completion_percent':100,'file_count':len(files)+2,'child_directory_count':len(c['directories']),'manifest':{'bytes':0,'SHA256':'0'*64,'mode':modes[names[0]]},'own_bytes':0,'own_mode':modes[names[1]],'report':files['REPORT.md'],'custody':files['CUSTODY_RESULT.json'],'identity_search':files['IDENTITY_SEARCH.json'],'canonical':None,'redirect':None,'publication_authority':False,'scientific_execution_or_network_or_W_access':False,'exact_terminal_hash_exclusions':list(names),'self_hash_delivered_externally':True}
    for unused in range(20):
        lengths=(len(encoded(manifest)),len(encoded(final)))
        for row in manifest['terminal_pair']:row['bytes']=lengths[names.index(row['path'])]
        final['manifest']['bytes']=lengths[0];final['own_bytes']=lengths[1]
        if lengths==(len(encoded(manifest)),len(encoded(final))):break
    else:raise AssertionError('terminal length fixed point')
    mb=encoded(manifest);final['manifest']['SHA256']=hashlib.sha256(mb).hexdigest();fb=encoded(final);assert lengths==(len(mb),len(fb))
    (OWN/names[0]).write_bytes(mb);(OWN/names[1]).write_bytes(fb);end=census(OWN)
    assert {n:p for n,p in end['files'].items() if n not in names}==files and end['directories']==c['directories'] and end['root_mode']==c['root_mode']
    assert end['files'][names[0]]['SHA256']==final['manifest']['SHA256'] and all(end['files'][n]['bytes']==r['bytes'] and end['files'][n]['mode']==r['mode'] for n,r in zip(names,manifest['terminal_pair']))
    print(json.dumps({'status':'FROZEN_COMPLETE','file_count':len(files)+2,'child_directory_count':len(c['directories']),'FINAL_MANIFEST':pin(OWN/names[0]),'FINAL':pin(OWN/names[1]),'REPORT':pin(OWN/'REPORT.md'),'finished_UTC':utc()}))
