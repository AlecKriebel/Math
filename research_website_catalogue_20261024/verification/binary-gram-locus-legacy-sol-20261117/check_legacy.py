"""Bounded passive legacy identity/custody checker. Writes only its fresh verification lane."""
import base64, datetime, hashlib, json, os, re, stat, subprocess, sys, time
from html.parser import HTMLParser
from pathlib import Path

M=Path('/Users/alec/Documents/Math')
P=M/'research_website_catalogue_20261024'
OWN=P/'verification/binary-gram-locus-legacy-sol-20261117'
SRC=P/'papers/23318851/sources'
PRIVATE=P/'verification/binary-gram-locus-editorial-sol-20261117'
RELEASE='674c6b9f9b296dd7a18dac4eec87b4ace840ccd5'
NATIVE='a4ce3c37dad209339e490d18dcced6c48cf912d2'
TREE_NATIVE='6ccfd5ab446400dc7fb3933dcc2e374cb415fa90'
TREE_RELEASE='e63ba1f227e5aa2f0e06fd6a52b36afa1531a4d0'
GIT=['/usr/bin/git','--no-optional-locks','-c','core.hooksPath=/dev/null','-c','core.fsmonitor=false','-C',str(M)]
assert sys.argv[1:] in (['intake'],['close'],['freeze'])
PHASE=sys.argv[1];calls=[]
def utc():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def rawjson(value):return (json.dumps(value,ensure_ascii=False,indent=2)+'\n').encode()
def save(name,value):
    with (OWN/name).open('xb') as f:f.write(rawjson(value))
def load(path):return json.loads(path.read_bytes())
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
    return {'root':str(root),'root_mode':dirs['.'],'files':files,'directories':{n:m for n,m in dirs.items() if n!='.'},'hidden_paths':sorted(n for n in paths if n!='.' and any(c.startswith('.') for c in n.split('/'))),'empty_files':sorted(n for n,p in files.items() if p['bytes']==0),'empty_directories':sorted(n for n in dirs if n!='.' and not any(x.startswith(n+'/') for x in paths))}
def run(argv,allowed=(0,)):
    number=len(calls);stem=f'{PHASE}-call-{number:03d}';start=utc();t=time.monotonic()
    r=subprocess.run(argv,capture_output=True)
    (OWN/(stem+'.stdout.bin')).write_bytes(r.stdout);(OWN/(stem+'.stderr.bin')).write_bytes(r.stderr)
    item={'argv':argv,'started_UTC':start,'finished_UTC':utc(),'elapsed_seconds':time.monotonic()-t,'exit':r.returncode,'stdout_bytes':len(r.stdout),'stderr_bytes':len(r.stderr),'stdout':stem+'.stdout.bin','stderr':stem+'.stderr.bin'}
    calls.append(item);save(stem+'.invocation.json',item)
    assert r.returncode in allowed,(argv,r.returncode,r.stderr.decode(errors='replace'))
    return r.stdout
def git(*args):return run(GIT+list(args))
def native_controls():
    refs=git('for-each-ref','--format=%(refname)%00%(objectname)','refs/heads').decode()
    rawrefs=census(M/'.git/refs/heads') if (M/'.git/refs/heads').exists() else {'exists':False}
    controls={n:pin(M/'.git'/n) for n in ('HEAD','index','config')}
    if (M/'.git/config.worktree').exists():controls['config.worktree']=pin(M/'.git/config.worktree')
    return {'HEAD_commit':git('rev-parse','HEAD').decode().strip(),'HEAD_raw_base64':base64.b64encode((M/'.git/HEAD').read_bytes()).decode(),'controls':controls,'logical_local_heads':refs,'physical_loose_local_heads':rawrefs}
def snapshot():
    result={'UTC':utc(),'native':native_controls(),'physical_docs':census(M/'docs'),'sources':census(SRC),'private_writer':census(PRIVATE),'identity_notes':{str(p.relative_to(P)):pin(p) for p in (P/'verification/root-clearance-23318851-20261117.json',P/'papers/23318851/reviews/root-continuation-20261117/ROOT_REVIEW.md')}}
    assert result['native']['HEAD_commit']==NATIVE
    assert git('rev-parse','HEAD:docs').decode().strip()==TREE_NATIVE
    assert git('rev-parse',RELEASE+':docs').decode().strip()==TREE_RELEASE
    result['observed_remote_tracking_main']=git('rev-parse','refs/remotes/origin/main').decode().strip()
    return result
def validate_source_and_private(state):
    source=state['sources'];sf=load(SRC/'SOURCE_FINAL.json');sm=load(SRC/'SOURCE_MANIFEST.json')
    assert len(source['files'])==sf['regular_files']==95 and len(source['directories'])==sf['child_directories']==16
    assert source['files']['SOURCE_MANIFEST.json']=={'bytes':sf['manifest']['bytes'],'SHA256':sf['manifest']['SHA256'],'MD5':sf['manifest']['MD5'],'mode':sf['manifest']['mode']}
    expected_files={r['path']:{'bytes':r['bytes'],'SHA256':r['sha256'],'MD5':r['md5'],'mode':r['mode_octal']} for r in sm['entries'] if r['kind']=='file'}
    assert len(expected_files)==sm['file_count']==93
    assert expected_files=={n:p for n,p in source['files'].items() if n not in ('SOURCE_FINAL.json','SOURCE_MANIFEST.json')}
    assert {r['path']:r['mode_octal'] for r in sm['entries'] if r['kind']=='directory'}==dict(source['directories'],**{'.':source['root_mode']})
    private=state['private_writer'];ps=load(PRIVATE/'FINAL_SEAL.json');pm=load(PRIVATE/'FINAL_MANIFEST.json')
    assert len(private['files'])==ps['files']==21 and len(private['directories'])==ps['child_directories']==1
    assert private['files']['FINAL_MANIFEST.json']['SHA256']==ps['manifest_SHA256']
    assert private['files']['FINAL.json']['SHA256']==ps['FINAL_SHA256']
    for r in pm['entries']:
        if r['kind']=='file' and r['path'] not in ('FINAL_MANIFEST.json','FINAL_SEAL.json'):
            assert all(private['files'][r['path']][k]==r[k] for k in ('bytes','SHA256','mode'))
        if r['kind']=='directory':assert (private['root_mode'] if r['path']=='.' else private['directories'][r['path']])==r['mode']
class Text(HTMLParser):
    def __init__(self):super().__init__(convert_charrefs=True);self.skip=0;self.text=[];self.links=[]
    def handle_starttag(self,tag,attrs):
        if tag in ('script','style'):self.skip+=1
        if tag in ('p','div','li','h1','h2','h3','section','br','title'):self.text.append('\n')
        for k,v in attrs:
            if k in ('href','src') and v:self.links.append(v)
    def handle_endtag(self,tag):
        if tag in ('script','style'):self.skip-=1
        if tag in ('p','div','li','h1','h2','h3','section','title'):self.text.append('\n')
    def handle_data(self,data):
        if self.skip==0:self.text.append(data)
def tree_rows(commit,label):
    raw=git('ls-tree','-r','-t','-z','--full-tree',commit,'docs');rows=[]
    for item in raw.split(b'\0'):
        if not item:continue
        head,path=item.split(b'\t',1);mode,kind,oid=head.decode().split();name=path.decode()
        assert name=='docs' or name.startswith('docs/')
        rows.append({'path':name,'mode':mode,'type':kind,'OID':oid})
    assert len({r['path'] for r in rows})==len(rows)
    save(label+'-TREE.json',{'commit':commit,'docs_tree':TREE_NATIVE if label=='native' else TREE_RELEASE,'rows':rows})
    return rows
if PHASE=='intake':
    state=snapshot();validate_source_and_private(state);save('GUARD_BEFORE.json',state)
    model=load(PRIVATE/'MODEL.json');assets=[]
    for a in model['native_assets_in_original_order']:
        name=a['native_filename'];p=SRC/'zenodo-files'/name;raw=p.read_bytes();identity=pin(p)
        assert identity['SHA256']==a['SHA256'] and identity['bytes']==a['bytes'] and pin(PRIVATE/'private-page'/name)==identity
        assets.append({'native_filename':name,'identity':identity,'Git_blob_OID':hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()})
    patterns=[r'\bGram\b|\btensors?\b|\bSeigal\b|23318851|30003480|gram_locus']
    q=r'(^|[^[:alnum:]_])(Gram|tensors?|Seigal)([^[:alnum:]_]|$)|23318851|30003480|gram_locus'
    candidates=[];namespaces={};(OWN/'candidates').mkdir()
    for label,commit in (('physical',None),('native',NATIVE),('released',RELEASE)):
        rows=None if commit is None else tree_rows(commit,label)
        if commit is None:
            result=run(['/Applications/ChatGPT.app/Contents/Resources/codex-cli/codex-path/rg','-l','-0','-i','--hidden','--no-ignore','--glob','*.html','--glob','*.htm','-e',patterns[0],str(M/'docs')],allowed=(0,1))
            paths=[Path(n.decode()).relative_to(M).as_posix() for n in result.split(b'\0') if n]
            htmlcount=sum(n.lower().endswith(('.html','.htm')) for n in state['physical_docs']['files'])
            matches=[{'asset':a['native_filename'],'path':'docs/'+n} for n,v in state['physical_docs']['files'].items() for a in assets if v['bytes']==a['identity']['bytes'] and v['SHA256']==a['identity']['SHA256']]
        else:
            result=run(GIT+['grep','-l','-z','-i','-I','-E','-e',q,commit,'--',':(glob)docs/**/*.html',':(glob)docs/**/*.htm'],allowed=(0,1))
            paths=[n.decode().removeprefix(commit+':') for n in result.split(b'\0') if n]
            assert all(n.startswith('docs/') for n in paths)
            htmlcount=sum(r['type']=='blob' and r['path'].lower().endswith(('.html','.htm')) for r in rows)
            matches=[{'asset':a['native_filename'],'path':r['path'],'OID':r['OID']} for r in rows if r['type']=='blob' for a in assets if r['OID']==a['Git_blob_OID']]
            for match in matches:
                raw=git('cat-file','blob',match['OID']);a=next(a for a in assets if a['native_filename']==match['asset'])
                assert len(raw)==a['identity']['bytes'] and hashlib.sha256(raw).hexdigest()==a['identity']['SHA256']
        assert len(paths)==len(set(paths));namespaces[label]={'commit':commit,'html_files':htmlcount,'candidate_paths':sorted(paths),'exact_whole_asset_matches':matches}
        for name in sorted(paths):
            raw=(M/name).read_bytes() if commit is None else git('show',commit+':'+name)
            digest=hashlib.sha256(raw).hexdigest();ident=f'{len(candidates)+1:03d}';htmlname='candidates/'+ident+'.html';textname='candidates/'+ident+'.txt'
            (OWN/htmlname).write_bytes(raw);parser=Text();parser.feed(raw.decode('utf-8'));parser.close()
            (OWN/textname).write_text(''.join(parser.text)+'\n',encoding='utf-8')
            strong=[token for token in (model['title'],model['DOI'],'23318851','gram_locus_note','gram_locus_support','30003480') if token.casefold() in raw.decode('utf-8').casefold()]
            candidates.append({'namespace':label,'path':name,'bytes':len(raw),'SHA256':digest,'saved_HTML':htmlname,'full_visible_text':textname,'all_links':parser.links,'strong_identity_tokens':strong})
    save('IDENTITY_SEARCH.json',{'UTC':utc(),'target_title':model['title'],'DOI':model['DOI'],'native_assets':assets,'physical_rg_pattern':patterns[0],'Git_ERE_pattern':q,'namespaces':namespaces,'candidates':candidates,'scope':'Only actual present physical docs and two exact fixed Git docs trees. No network/global-history/live absence determination.'})
    save('INTAKE_CALLS.json',calls);print(json.dumps({'status':'INTAKE_COMPLETE','physical_docs_files':len(state['physical_docs']['files']),'physical_docs_childdirs':len(state['physical_docs']['directories']),'namespaces':namespaces,'candidate_copies':len(candidates),'unique_candidate_bytes':len({c['SHA256'] for c in candidates})}))
elif PHASE=='close':
    state=snapshot();validate_source_and_private(state);save('GUARD_AFTER.json',state);before=load(OWN/'GUARD_BEFORE.json')
    for k in ('native','physical_docs','sources','private_writer','identity_notes'):assert state[k]==before[k],k
    save('CLOSING_CALLS.json',calls);save('CUSTODY_RESULT.json',{'UTC':utc(),'status':'EXACT_PROTECTED_NAMESPACES','source_files_childdirs':[len(state['sources']['files']),len(state['sources']['directories'])],'private_files_childdirs':[len(state['private_writer']['files']),len(state['private_writer']['directories'])],'physical_docs_files_childdirs':[len(state['physical_docs']['files']),len(state['physical_docs']['directories'])],'remote_tracking_before':before['observed_remote_tracking_main'],'remote_tracking_after':state['observed_remote_tracking_main'],'remote_tracking_is_observation_not_protected_boundary':True,'whole_bytes_modes_hidden_empty_topology_exact':True})
    print('Closing custody passed: native HEAD/index/config/local-heads, complete physical docs, sources, private writer and identity-note files exact.')
else:
    assert load(OWN/'CUSTODY_RESULT.json')['status']=='EXACT_PROTECTED_NAMESPACES'
    names=('FINAL_MANIFEST.json','FINAL.json')
    for name in names:
        with (OWN/name).open('xb'):pass
    c=census(OWN);files={n:v for n,v in c['files'].items() if n not in names};started=utc();modes={n:c['files'][n]['mode'] for n in names}
    manifest={'schema':'finite-legacy-audit-complete-namespace-v1','UTC':started,'root':str(OWN),'root_mode':c['root_mode'],'file_count':len(files)+2,'child_directory_count':len(c['directories']),'payload_files':files,'directories':c['directories'],'hidden_paths':c['hidden_paths'],'empty_files':sorted(n for n,v in files.items() if v['bytes']==0),'empty_directories':c['empty_directories'],'terminal_pair':[{'path':n,'bytes':0,'mode':modes[n],'self_recursive_hash_excluded':True} for n in names]}
    final={'schema':'bounded-legacy-correspondence-final-v1','UTC':started,'status':'FROZEN_COMPLETE','completion_percent':100,'record':'23318851','manifest':{'bytes':0,'SHA256':'0'*64,'mode':modes[names[0]]},'own_terminal_bytes':0,'own_terminal_mode':modes[names[1]],'file_count':len(files)+2,'child_directory_count':len(c['directories']),'report':files['REPORT.md'],'custody':files['CUSTODY_RESULT.json'],'identity_search':files['IDENTITY_SEARCH.json'],'canonical':None,'redirect':None,'publication_authority':False,'only_terminal_hash_exclusions':list(names),'native_W_access_or_network_or_science_execution':False,'seal_hash_external':True}
    for unused in range(20):
        lengths=(len(rawjson(manifest)),len(rawjson(final)))
        for row in manifest['terminal_pair']:row['bytes']=lengths[names.index(row['path'])]
        final['manifest']['bytes']=lengths[0];final['own_terminal_bytes']=lengths[1]
        if lengths==(len(rawjson(manifest)),len(rawjson(final))):break
    else:raise AssertionError('terminal length fixed point')
    mraw=rawjson(manifest);final['manifest']['SHA256']=hashlib.sha256(mraw).hexdigest();fraw=rawjson(final)
    assert lengths==(len(mraw),len(fraw))
    (OWN/names[0]).write_bytes(mraw);(OWN/names[1]).write_bytes(fraw)
    after=census(OWN);assert {n:v for n,v in after['files'].items() if n not in names}==files and after['directories']==c['directories'] and after['root_mode']==c['root_mode']
    assert after['files'][names[0]]['SHA256']==final['manifest']['SHA256']
    assert all(after['files'][n]['bytes']==row['bytes'] and after['files'][n]['mode']==row['mode'] for n,row in zip(names,manifest['terminal_pair']))
    print(json.dumps({'status':'FROZEN_COMPLETE','file_count':len(files)+2,'child_directory_count':len(c['directories']),'FINAL_MANIFEST':pin(OWN/names[0]),'FINAL':pin(OWN/names[1]),'report':pin(OWN/'REPORT.md'),'finished_UTC':utc()}))
