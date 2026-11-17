"""One passive identity/custody invocation; no imported project code or scientific execution."""
from pathlib import Path, PurePosixPath
from datetime import datetime, timezone
from html.parser import HTMLParser
import hashlib, io, json, os, re, stat, subprocess, sys, traceback, unicodedata, zipfile

P=Path('/Users/alec/Documents/Math/research_website_catalogue_20261024'); M=P.parent
A=P/'verification/pentagon-full-fifth-torsion-legacy-sol-20261117'
SRC=P/'papers/23137834/sources'; WRITER=P/'verification/pentagon-full-fifth-torsion-editorial-sol-20261117'
REVIEW=P/'papers/23137834/reviews/root-continuation-20261117/ROOT_REVIEW.md'
CLEAR=P/'verification/root-clearance-23137834-20261117.json'
NATIVE='a4ce3c37dad209339e490d18dcced6c48cf912d2'; RELEASED='bbfb7abf5c56e3f8d090e125784ff357138076fb'
TREES={NATIVE:'6ccfd5ab446400dc7fb3933dcc2e374cb415fa90',RELEASED:'e63ba1f227e5aa2f0e06fd6a52b36afa1531a4d0'}
ASSETS=[('pentagonal-torsion-note.pdf',92256,'0325be9bc4b754ad1d94baadf2f1b88af587e9443b9d242a2d7af7b2dda79420'),('pentagonal-torsion-verification.zip',206380,'e916946b6ffaaec2dae08b4a3622d19293d087ced789297ee38b86c671d76dab')]
TEXHASH='3338be58c5c6250a826f2a2af772db5a3838dad1d45c6c4a847c62cc00b4f9df'
GITLOG=[]; CACHE={}; OUTPUT=None; LAST_GIT_RAW=None
def utc():return datetime.now(timezone.utc).isoformat()
def require(v,s):
    if not v:raise RuntimeError(s)
def enc(v):return (json.dumps(v,ensure_ascii=False,indent=2)+'\n').encode()
def put(n,v):
    with (A/n).open('xb') as f:f.write(enc(v))
def dp(b):return {'bytes':len(b),'SHA256':hashlib.sha256(b).hexdigest(),'MD5':hashlib.md5(b).hexdigest()}
def pin(p):
    s=p.lstat();require(stat.S_ISREG(s.st_mode) and not p.is_symlink(),'real regular file '+str(p));b=p.read_bytes();t=p.lstat()
    require((s.st_dev,s.st_ino,s.st_mode,s.st_size,s.st_mtime_ns,s.st_ctime_ns)==(t.st_dev,t.st_ino,t.st_mode,t.st_size,t.st_mtime_ns,t.st_ctime_ns),'stable read '+str(p))
    return dp(b)|{'mode':oct(stat.S_IMODE(s.st_mode))}
def snap(root):
    if not os.path.lexists(root):return {'root':str(root),'absent':True}
    files={};dirs={};todo=[root]
    while todo:
        p=todo.pop();s=p.lstat();require(stat.S_ISDIR(s.st_mode) and not p.is_symlink(),'real directory');name=p.relative_to(root).as_posix();children=sorted(p.iterdir())
        dirs[name]={'mode':oct(stat.S_IMODE(s.st_mode)),'empty':not children}
        for c in children:
            t=c.lstat();require(not c.is_symlink(),'no symlink in guarded tree')
            if stat.S_ISDIR(t.st_mode):todo.append(c)
            else:files[c.relative_to(root).as_posix()]=pin(c)
        t=p.lstat();require((s.st_dev,s.st_ino,s.st_mode,s.st_mtime_ns,s.st_ctime_ns)==(t.st_dev,t.st_ino,t.st_mode,t.st_mtime_ns,t.st_ctime_ns),'stable directory read')
    return {'root':str(root),'files':files,'directories':dirs,'file_count':len(files),'child_directory_count':len(dirs)-1,'hidden_paths':sorted(n for n in set(files)|set(dirs) if n!='.' and any(x.startswith('.') for x in n.split('/'))),'empty_files':sorted(n for n,v in files.items() if v['bytes']==0),'empty_directories':sorted(n for n,v in dirs.items() if v['empty'])}
def heads():
    packed={}
    p=M/'.git/packed-refs'
    if p.exists():
        for line in p.read_text().splitlines():
            if line and not line.startswith(('#','^')):
                oid,name=line.split(' ',1)
                if name.startswith('refs/heads/'):packed[name]=oid
    loose=snap(M/'.git/refs/heads');logical=dict(packed)
    for name in loose.get('files',{}):logical['refs/heads/'+name]=(M/'.git/refs/heads'/name).read_text().strip()
    require(all(re.fullmatch('[0-9a-f]{40}',v) for v in logical.values()),'literal local branch OIDs')
    return {'loose':loose,'logical':logical}
def capture():return {'native_M':{'raw_controls':{n:pin(M/'.git'/n) for n in ('HEAD','index','config')},'local_heads':heads()},'docs':snap(M/'docs'),'source':snap(SRC),'writer':snap(WRITER),'specific_root':{str(p.relative_to(P)):pin(p) for p in (REVIEW,CLEAR)}}
def load(p):return json.loads(p.read_bytes())
def authenticate(b):
    n=b['native_M'];require((M/'.git/HEAD').read_bytes()==b'ref: refs/heads/main\n' and n['local_heads']['logical']['refs/heads/main']==NATIVE,'native raw HEAD/main')
    require(n['raw_controls']['index']['SHA256']=='91b10d938f7d737226662bbff3b07016dcc0e501376a045811ab4e930c6fbb11' and n['raw_controls']['index']['bytes']==25854746,'native full index pin')
    require(n['raw_controls']['config']['SHA256']=='2c083de0f0839443ce1ed062a8c1f2be83cbc30f838e5350e567a8153b7b3a47','native config pin')
    s=b['source'];sm=load(SRC/'SOURCE_MANIFEST.json');require((s['file_count'],s['child_directory_count'])==(97,7),'source97/7')
    require(s['files']['SOURCE_FINAL.json']['SHA256']=='14cbf430570b90574e7c28bba911e7fe2b868c164107591b1783694c30212f80' and s['files']['SOURCE_MANIFEST.json']['SHA256']=='7f2ec5e3f4d6fa358bc9dcc5af3ef5adb4ec3e3b2b8851ff831f8b4574dcd2ed','source external terminal pins')
    rows={r['path']:{k:r[k] for k in ('bytes','SHA256','mode')} for r in sm['files']};excluded=sm['root_controls_excluded_from_own_list']
    require(excluded==['SOURCE_MANIFEST.json','SOURCE_FINAL.json'] and len(rows)==len(sm['files']) and rows=={n:{k:r[k] for k in ('bytes','SHA256','mode')} for n,r in s['files'].items() if n not in excluded},'complete actual source payload schema')
    require({r['path']:r['mode'] for r in sm['directories']}=={n:r['mode'] for n,r in s['directories'].items() if n!='.'},'source directory modes')
    w=b['writer'];wm=load(WRITER/'FINAL_MANIFEST.json');require((w['file_count'],w['child_directory_count'])==(19,1),'writer19/1')
    require(w['files']['FINAL.json']['SHA256']=='0c6838af4b2acf9065b89587f8701b692be78caf974b67e6e5dbb06899a713aa' and w['files']['FINAL_MANIFEST.json']['SHA256']=='e31cdbc3460f63e135e075fbb21bff87e72ae5cbbedb71ce222b822f29645584','writer external terminal pins')
    ts=wm['terminal_pair'];require([r['path'] for r in ts]==['FINAL_MANIFEST.json','FINAL.json'] and all(r['recursive_hash_excluded'] for r in ts),'writer exact terminal schema')
    require(wm['payload_files']=={n:r for n,r in w['files'].items() if n not in ('FINAL_MANIFEST.json','FINAL.json')},'all whole writer payloads')
    require(wm['root_mode']==w['directories']['.']['mode'] and wm['directories']=={n:r['mode'] for n,r in w['directories'].items() if n!='.'},'whole writer directory modes')
    require(all(w['files'][r['path']]['bytes']==r['bytes'] and w['files'][r['path']]['mode']==r['mode'] for r in ts),'writer terminal bytes/modes')
    for p,size,sha in [(REVIEW,15716,'acd210977221457737949db0684d2c60c289fef197b6b4dcaa26d87c8aa99599'),(CLEAR,2546,'55ea79efc35b209694e5afd51edd42ffa6994cb6ca755e83c981494b7e291951')]:require((pin(p)['bytes'],pin(p)['SHA256'])==(size,sha),'fixed root identity')
    api=load(SRC/'record.response.body');require(api['id']==23137834 and api['metadata']['version']=='1.0' and api['metadata']['doi']=='10.5281/zenodo.23137834','native API identity')
    require([f['key'] for f in api['files']]==[x[0] for x in ASSETS],'native PDF then ZIP order')
    for f,(name,size,sha) in zip(api['files'],ASSETS):
        r=pin(SRC/'assets'/name);require(r['bytes']==size==f['size'] and r['SHA256']==sha and 'md5:'+r['MD5']==f['checksum'] and r==pin(WRITER/'private-page'/name),'whole source/writer/native asset')
    require(pin(SRC/'published-source/container-001/tree/manuscript.tex')['SHA256']==TEXHASH,'whole native TeX identity')
def gitrun(request):
    global LAST_GIT_RAW
    env={k:v for k,v in os.environ.items() if not k.startswith('GIT_')};env.update({'GIT_CONFIG_NOSYSTEM':'1','GIT_CONFIG_GLOBAL':'/dev/null','GIT_NO_LAZY_FETCH':'1','GIT_NO_REPLACE_OBJECTS':'1','GIT_TERMINAL_PROMPT':'0','GIT_ALLOW_PROTOCOL':'','GIT_OPTIONAL_LOCKS':'0'})
    argv=['/usr/bin/git','--no-optional-locks','--git-dir='+str(M/'.git'),'--work-tree='+str(M),'-c','protocol.allow=never','-c','core.hooksPath=/dev/null','-c','core.fsmonitor=false','-c','gc.auto=0','-c','maintenance.auto=false','cat-file','--batch']
    start=utc();r=subprocess.run(argv,input=request,stdout=subprocess.PIPE,stderr=subprocess.PIPE,env=env,cwd=M,check=False)
    LAST_GIT_RAW=(r.stdout,r.stderr)
    GITLOG.append({'argv':argv,'start_UTC':start,'end_UTC':utc(),'request':dp(request),'exit_code':r.returncode,'stdout':dp(r.stdout),'stderr':dp(r.stderr),'network_disabled':True})
    if r.returncode or r.stderr:
        (A/'FAILED_GIT.stdout.bin').write_bytes(r.stdout);(A/'FAILED_GIT.stderr.bin').write_bytes(r.stderr)
    require(r.returncode==0 and not r.stderr,'literal local cat-file result')
    return r.stdout
def fetch(oids):
    wanted=sorted(set(oids)-set(CACHE))
    if not wanted:return
    require(all(re.fullmatch('[0-9a-f]{40}',o) for o in wanted),'literal OIDs');raw=gitrun(''.join(o+'\n' for o in wanted).encode());at=0
    for oid in wanted:
        end=raw.index(b'\n',at);fields=raw[at:end].split();require(len(fields)==3 and fields[0].decode()==oid and fields[2].isdigit(),'complete object header');kind=fields[1];size=int(fields[2]);body=raw[end+1:end+1+size];at=end+1+size
        require(len(body)==size and raw[at:at+1]==b'\n' and hashlib.sha1(kind+b' '+str(size).encode()+b'\0'+body).hexdigest()==oid,'checksum-valid whole Git object');at+=1;CACHE[oid]=(kind,body)
    require(at==len(raw),'whole batch response consumed')
def tree(oid):
    fetch([oid]);kind,raw=CACHE[oid];require(kind==b'tree','tree object');rows=[];at=0;names=set()
    while at<len(raw):
        sep=raw.index(b' ',at);end=raw.index(b'\0',sep);name=raw[sep+1:end].decode();require(name not in names and name not in ('','.','..') and '/' not in name,'simple unique tree name');names.add(name);require(end+21<=len(raw),'whole tree record');rows.append((raw[at:sep].decode(),name,raw[end+1:end+21].hex()));at=end+21
    return rows
def docs(commit,expected):
    fetch([commit]);kind,raw=CACHE[commit];require(kind==b'commit' and re.fullmatch(b'tree [0-9a-f]{40}',raw.split(b'\n')[0]),'commit identity');root=raw.split(b'\n')[0][5:].decode();require([x for x in tree(root) if x[1]=='docs']==[('40000','docs',expected)],'exact commit/docs tree binding')
    files={};dirs={};pending=[('.',expected)]
    while pending:
        fetch(o for n,o in pending);following=[]
        for prefix,oid in pending:
            dirs[prefix]={'Git_mode':'40000','OID':oid}
            for mode,name,child in tree(oid):
                path=name if prefix=='.' else prefix+'/'+name
                if mode=='40000':following.append((path,child))
                else:require(mode in ('100644','100755') and path not in files,'regular unique tree leaf');files[path]={'Git_mode':mode,'OID':child}
        pending=following
    fetch(r['OID'] for r in files.values())
    for r in files.values():
        kind,raw=CACHE[r['OID']];require(kind==b'blob','docs blob');r.update(dp(raw))
    return {'commit':commit,'docs_tree':expected,'files':files,'directories':dirs,'file_count':len(files),'child_directory_count':len(dirs)-1}
class HTML(HTMLParser):
    def __init__(self):super().__init__(convert_charrefs=True);self.parts=[];self.links=[];self.meta=[]
    def handle_data(self,s):self.parts.append(s)
    def handle_starttag(self,t,a):
        a=dict(a)
        if t=='meta':self.meta.append(a)
        for k in ('href','src'):
            if k in a:self.links.append(a[k])
def norm(s):return ''.join(c for c in unicodedata.normalize('NFKD',s).casefold() if c.isalnum())
STRONG=['23137834','regularpentagon','pentagonal','pentagonquintic','fifthtorsion','5torsion','mccallum','verdure']
BROAD=['pentagon','torsion','quintic','elliptic','tatenormal','genusone']
IDENTITIES={h:n for n,size,h in ASSETS}|{TEXHASH:'native manuscript.tex'}
def savehtml(raw):
    name='candidate-'+hashlib.sha256(raw).hexdigest()+'.html';p=A/'candidate-articles'/name
    if p.exists():require(p.read_bytes()==raw,'whole same candidate body')
    else:
        with p.open('xb') as f:f.write(raw)
    return 'candidate-articles/'+name
def scan(label,view,get):
    hits=[];members=[];matches=[];textual=[]
    def text(path,raw,archive=False):
        if PurePosixPath(path).suffix.casefold() not in ('.html','.htm','.md','.txt','.json','.xml','.tex','.bib','.cff'):return
        value=raw.decode('utf-8',errors='replace');fold=norm(value);strong=[s for s in STRONG if s in fold];broad=[s for s in BROAD if s in fold]
        if strong:textual.append({'path':path,'strong_terms':strong,'archive_member':archive,**dp(raw)})
        if PurePosixPath(path).suffix.casefold() in ('.html','.htm') and (strong or broad):
            p=HTML();p.feed(value);p.close();hits.append({'path':path,'strong_terms':strong,'broad_terms':broad,'archive_member':archive,'saved_whole_HTML':savehtml(raw),'links':p.links,'meta':p.meta,**dp(raw)})
    def check(path,raw):
        sha=hashlib.sha256(raw).hexdigest()
        if sha in IDENTITIES:matches.append({'path':path,'exact_identity':IDENTITIES[sha],**dp(raw)})
    def archive(path,raw,depth=0):
        require(depth<=8,'finite bounded nested archive depth')
        with zipfile.ZipFile(io.BytesIO(raw)) as z:
            names=set();total=0
            for m in z.infolist():
                duplicate=m.filename in names;names.add(m.filename);total+=m.file_size;require(total<=1073741824,'bounded one-GiB archive traversal')
                safe=not PurePosixPath(m.filename).is_absolute() and '..' not in PurePosixPath(m.filename).parts
                if m.is_dir():members.append({'container':path,'member':m.filename,'directory':True,'duplicate_name':duplicate,'external_attr':m.external_attr,'safe_relative_path':safe});continue
                b=z.read(m);require(len(b)==m.file_size,'complete archive member');full=path+'!'+m.filename;members.append({'container':path,'member':m.filename,'directory':False,'duplicate_name':duplicate,'external_attr':m.external_attr,'CRC32':m.CRC,'safe_relative_path':safe,**dp(b)});check(full,b);text(full,b,True)
                if b.startswith(b'PK\x03\x04'):archive(full,b,depth+1)
    for path,row in sorted(view['files'].items()):
        raw=get(path);require(all(dp(raw)[k]==row[k] for k in ('bytes','SHA256','MD5')),'complete view buffer '+path);check(path,raw);text(path,raw)
        if raw.startswith(b'PK\x03\x04'):archive(path,raw)
    return {'label':label,'file_count':view['file_count'],'child_directory_count':view['child_directory_count'],'HTML_count':sum(PurePosixPath(p).suffix.casefold() in ('.html','.htm') for p in view['files']),'whole_asset_or_source_matches':matches,'HTML_candidates':hits,'strong_text_candidates':textual,'archive_member_count':len(members),'all_archive_member_records':members}
def diff(x,y):
    a=x['files'];b=y['files'];common=set(a)&set(b)
    return {'only_first_files':sorted(set(a)-set(b)),'only_second_files':sorted(set(b)-set(a)),'common_content_differences':{n:{'first':a[n],'second':b[n]} for n in sorted(common) if any(a[n][k]!=b[n][k] for k in ('bytes','SHA256','MD5'))},'common_permission_or_Git_mode_differences':{n:{'first':a[n].get('mode',a[n].get('Git_mode')),'second':b[n].get('mode',b[n].get('Git_mode'))} for n in sorted(common) if (int(a[n].get('mode',a[n].get('Git_mode')),8)&0o777)!=(int(b[n].get('mode',b[n].get('Git_mode')),8)&0o777)},'only_first_directories':sorted(set(x['directories'])-set(y['directories'])),'only_second_directories':sorted(set(y['directories'])-set(x['directories'])),'directory_modes_and_git_tree_OIDs_retained_in_full_view_maps':True}
def seal(result):
    names=('MANIFEST.json','FINAL.json')
    for n in names:
        with (A/n).open('xb'):pass
    s=snap(A);payload={n:r for n,r in s['files'].items() if n not in names}
    manifest={'schema':'finite-pentagon-legacy-whole-namespace-v1','UTC':utc(),'root':str(A),'root_mode':s['directories']['.']['mode'],'file_count':len(s['files']),'child_directory_count':s['child_directory_count'],'payload_files':payload,'directories':s['directories'],'hidden_paths':s['hidden_paths'],'empty_files':sorted(n for n,r in payload.items() if r['bytes']==0),'empty_directories':s['empty_directories'],'terminal_pair':[{'path':n,'bytes':0,'mode':s['files'][n]['mode'],'recursive_hash_excluded':True} for n in names]}
    final={'schema':'pentagon-legacy-finite-FINAL-v1','UTC':utc(),'record':'23137834','row':170,'status':'FROZEN_BOUNDED_IDENTITY_EVIDENCE_FOR_ROOT_REVIEW','completion_percent_assigned_legacy_task':100,'reported_disposition':result,'whole_fixed_guard_before_after_exact':True,'file_count':len(s['files']),'child_directory_count':s['child_directory_count'],'manifest':{'bytes':0,'SHA256':'0'*64},'own_bytes':0,'canonical':None,'redirect':None,'AA':None,'follow_up':None,'publication_or_live_certificate':False,'scientific_executions':0,'saved_reader_invocations':1,'unexpected_errors':0,'terminal_self_hash_exclusions':list(names),'external_terminal_pins_required':True,'stop':True}
    for step in range(20):
        lengths=(len(enc(manifest)),len(enc(final)))
        for i,r in enumerate(manifest['terminal_pair']):r['bytes']=lengths[i]
        final['manifest']['bytes']=lengths[0];final['own_bytes']=lengths[1]
        if lengths==(len(enc(manifest)),len(enc(final))):break
    else:raise RuntimeError('terminal length fixed point')
    mb=enc(manifest);final['manifest']['SHA256']=hashlib.sha256(mb).hexdigest();fb=enc(final);require(lengths==(len(mb),len(fb)),'final terminal lengths');(A/names[0]).write_bytes(mb);(A/names[1]).write_bytes(fb);e=snap(A)
    require({n:r for n,r in e['files'].items() if n not in names}==payload and e['directories']==s['directories'],'whole namespace quiescent seal')
    print(json.dumps({'status':final['status'],'file_count':len(s['files']),'child_directory_count':s['child_directory_count'],'MANIFEST':pin(A/names[0]),'FINAL':pin(A/names[1]),'completed_UTC':utc()}),flush=True)
def main():
    global OUTPUT
    require(Path(__file__).resolve()==A/'read_legacy_once.py' and not (A/'BEFORE.json').exists(),'one fresh saved invocation')
    (A/'candidate-articles').mkdir();OUTPUT=(A/'DATA.stdout.txt').open('x');(A/'DATA.stderr.txt').touch(exist_ok=False)
    start=utc();put('INVOCATION.json',{'argv':[sys.executable,str(Path(__file__).resolve())],'start_UTC':start,'native_Git_read_only':True,'network_disabled_for_Git':True,'source_or_helper_execution':False})
    before=capture();put('BEFORE.json',{'UTC':start,'snapshot':before});authenticate(before);require((before['docs']['file_count'],before['docs']['child_directory_count'])==(257,50),'complete physical docs257/50')
    views={'physical':before['docs']};observations=[scan('physical Math/docs',views['physical'],lambda p:(M/'docs'/p).read_bytes())]
    for label,commit in [('native',NATIVE),('released',RELEASED)]:
        views[label]=docs(commit,TREES[commit]);observations.append(scan(label+' commit '+commit,views[label],lambda p,v=views[label]:CACHE[v['files'][p]['OID']][1]))
    native_zip=(SRC/'assets'/ASSETS[1][0]).read_bytes();sourcezip={'files':{ASSETS[1][0]:dp(native_zip)},'file_count':1,'child_directory_count':0};nativearchive=scan('original native verification ZIP',sourcezip,lambda p:native_zip)
    put('EVIDENCE.json',{'schema':'bounded-pentagon-three-view-identity-evidence-v1','UTC':utc(),'root_supplied_released_snapshot_not_live_remote_check':RELEASED,'views':views,'observations':observations,'native_archive_inventory':nativearchive,'native_assets_original_order':[{'name':n,'bytes':b,'SHA256':h} for n,b,h in ASSETS],'Git_read_log':GITLOG})
    put('VIEW_DIFFERENCES.json',{'physical_vs_native':diff(views['physical'],views['native']),'physical_vs_released':diff(views['physical'],views['released']),'native_vs_released':diff(views['native'],views['released'])})
    message=json.dumps({'phase':'READY_FOR_PERSONAL_WHOLE_CANDIDATE_READ','UTC':utc(),'view_counts':[(x['label'],x['file_count'],x['child_directory_count'],x['HTML_count'],len(x['HTML_candidates']),len(x['whole_asset_or_source_matches'])) for x in observations],'candidate_files':len(list((A/'candidate-articles').iterdir()))})
    OUTPUT.write(message+'\n');OUTPUT.flush();print(message,flush=True)
    command=input('Personal reading/report complete: enter SEAL once to close fixed guards and freeze.\n')
    require(command=='SEAL' and (A/'REPORT.md').is_file() and (A/'DISPOSITION.json').is_file(),'personal report and exact close command')
    result=load(A/'DISPOSITION.json');after=capture();require(after==before,'whole native/docs/source/writer/root guard before-after exact');put('AFTER.json',{'UTC':utc(),'snapshot':after});put('RESULTS.json',{'schema':'bounded-pentagon-legacy-passive-custody-result-v1','start_UTC':start,'end_UTC':utc(),'whole_guard_before_after_exact':True,'disposition':result,'saved_reader_invocations':1,'unexpected_errors':0,'source_and_science_executions':0,'W_Gitmutation_network_Sheet_UI_redirect_deploy_outreach':False})
    OUTPUT.write(json.dumps({'phase':'WHOLE_FIXED_GUARDS_EXACT','end_UTC':utc(),'status':'READY_TO_FREEZE'})+'\n');OUTPUT.close();seal(result)
if __name__=='__main__':
    try:main()
    except BaseException:
        literal=traceback.format_exc();(A/'DATA.stderr.txt').write_text(literal)
        if LAST_GIT_RAW is not None:
            (A/'LAST_GIT.stdout.bin').write_bytes(LAST_GIT_RAW[0]);(A/'LAST_GIT.stderr.bin').write_bytes(LAST_GIT_RAW[1])
        if OUTPUT is not None and not OUTPUT.closed:OUTPUT.close()
        put('FAILURE.json',{'UTC':utc(),'literal_traceback':literal,'Git_read_log':GITLOG,'automatic_retry':False,'stop':True});sys.stderr.write(literal);raise SystemExit(1)
