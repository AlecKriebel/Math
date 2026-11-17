"""One bounded passive legacy collector; no project imports or network."""
from pathlib import Path
from datetime import datetime, timezone
from html.parser import HTMLParser
import hashlib, io, json, os, re, stat, subprocess, sys, traceback, zipfile

M=Path('/Users/alec/Documents/Math');P=M/'research_website_catalogue_20261024'
W=Path('/Users/alec/Desktop/alec-dev/aleckriebel.com')
A=P/'verification/even-minkowski-legacy-sol-20261117';S=P/'papers/23203081/sources'
EDITORIAL=P/'verification/even-minkowski-editorial-sol-20261117'
ROW191=P/'papers/23204176/reviews/adversarial-sol'
CLEAR=P/'verification/root-clearance-23203081-20261117.json'
REVIEW=P/'papers/23203081/reviews/root-continuation-20261117/ROOT_REVIEW.md'
NATIVE='a4ce3c37dad209339e490d18dcced6c48cf912d2';RELEASE='731cccd1ff02693e9258351f3e902bd7fe6a2071'
PINS={'paper.pdf':(79097,'6192382c55a3ac50ee76ce2514579a330dda1da6d873a32944a03bef26ed3179'),
      'source-and-verification.zip':(123632,'fb1510e38281baffe92c176c34692e498725a61d221907435f77954bd6fc405c'),
      'README.md':(6229,'386d94cd217b609a1509bc6b3015bc583e3c7470d86a999fa6cbb5dcc930dac6')}
PATTERN=r'23203081|23203080|Minkowski|Brunn|log[-_ ]?BM'
before=None;failure=None;active='startup';commands=[]
def now():return datetime.now(timezone.utc).isoformat()
def sha(b):return hashlib.sha256(b).hexdigest()
def blob(b):return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
def save(name,x):(A/name).write_text(json.dumps(x,indent=2,ensure_ascii=True)+'\n')
def require(ok,label):
    global active
    active=label
    if not ok:raise AssertionError(label)
def meta(p):
    st=p.lstat()
    if not stat.S_ISREG(st.st_mode):raise ValueError('Not regular '+str(p))
    b=p.read_bytes();return {'bytes':len(b),'SHA256':sha(b),'mode':oct(stat.S_IMODE(st.st_mode)),'Git_blob_OID':blob(b)}
def snapshot(root):
    st=root.lstat();f={};d={};o={}
    if not stat.S_ISDIR(st.st_mode):raise ValueError('Not directory '+str(root))
    for p in sorted(root.rglob('*')):
        s=p.lstat();n=str(p.relative_to(root))
        if stat.S_ISREG(s.st_mode):f[n]=meta(p)
        elif stat.S_ISDIR(s.st_mode):d[n]=oct(stat.S_IMODE(s.st_mode))
        else:o[n]={'mode':oct(stat.S_IMODE(s.st_mode)),'target':os.readlink(p) if p.is_symlink() else None}
    return {'root':str(root),'root_mode':oct(stat.S_IMODE(st.st_mode)),'files':f,'directories':d,'other':o}
def native(root):
    gd=root/'.git';packed=gd/'packed-refs';lines=[x for x in packed.read_text().splitlines() if re.match(r'^[0-9a-f]{40} refs/heads/',x)]
    head=(gd/'HEAD').read_text().strip();ref=head.removeprefix('ref: ');loose=gd/ref
    resolved=loose.read_text().strip() if loose.is_file() else next(x.split()[0] for x in lines if x.split()[1]==ref)
    return {'HEAD':head,'resolved_local_HEAD':resolved,'files':{n:meta(gd/n) for n in ['HEAD','index','config']},
            'local_heads':snapshot(gd/'refs/heads'),'packed_local_head_lines':lines,'packed_refs_mode':oct(stat.S_IMODE(packed.stat().st_mode))}
def guard():return {'UTC':now(),'source':snapshot(S),'physical_native_docs':snapshot(M/'docs'),'M_native':native(M),'W_native':native(W),
                    'frozen_editorial':snapshot(EDITORIAL),'frozen_row191_INITIAL_hashes_only':snapshot(ROW191),
                    'identity_controls':{str(x):meta(x) for x in [CLEAR,REVIEW]},
                    'excluded_from_local_invariance':['remote-tracking refs','FETCH_HEAD','nonlocal packed-ref lines','Firebase metadata outside public']}
def command(label,argv,stdin=None,allowed=(0,)):
    env={k:v for k,v in os.environ.items() if not k.startswith('GIT_')};env.update(GIT_OPTIONAL_LOCKS='0',GIT_NO_REPLACE_OBJECTS='1')
    r=subprocess.run(argv,cwd=M,input=stdin,stdout=subprocess.PIPE,stderr=subprocess.PIPE,env=env)
    (A/(label+'.stdout.bin')).write_bytes(r.stdout);(A/(label+'.stderr.bin')).write_bytes(r.stderr)
    if stdin is not None:(A/(label+'.stdin.bin')).write_bytes(stdin)
    row={'label':label,'argv':argv,'exit':r.returncode,'stdout_bytes':len(r.stdout),'stdout_SHA256':sha(r.stdout),'stderr_bytes':len(r.stderr),'stderr_SHA256':sha(r.stderr)};commands.append(row)
    save('COMMANDS.json',commands)
    if r.returncode not in allowed:raise RuntimeError(json.dumps(row))
    return r.stdout
def git(label,args,stdin=None,allowed=(0,)):return command(label,['/usr/bin/git','--no-optional-locks','-C',str(M),*args],stdin,allowed)
def git_scope(label,commit,tree_expected):
    tree=git(label+'_tree',['rev-parse',commit+':docs']).decode().strip();require(tree==tree_expected,label+'_exact_docs_tree')
    raw=git(label+'_ls_tree',['ls-tree','-r','-l','-z',commit,'--','docs']);entries=[]
    for unit in raw.split(b'\0'):
        if not unit:continue
        h,p=unit.split(b'\t',1);mode,kind,oid,n=h.split();require(kind==b'blob' and mode in [b'100644',b'100755'],label+'_regular_blob_schema')
        entries.append({'path':p.decode(),'mode':mode.decode(),'Git_blob_OID':oid.decode(),'bytes':int(n)})
    require(len(entries)==254,label+'_254_leaf_inventory')
    ids=sorted({x['Git_blob_OID'] for x in entries});data=git(label+'_blob_batch',['cat-file','--batch'],''.join(x+'\n' for x in ids).encode())
    pos=0;bodies={}
    for oid in ids:
        end=data.index(b'\n',pos);h=data[pos:end].split();pos=end+1
        require(len(h)==3 and h[0].decode()==oid and h[1]==b'blob',label+'_batch_header')
        n=int(h[2]);b=data[pos:pos+n];pos+=n;require(data[pos:pos+1]==b'\n' and blob(b)==oid,label+'_batch_blob_identity');pos+=1;bodies[oid]=b
    require(pos==len(data),label+'_batch_consumed')
    for e in entries:e['SHA256']=sha(bodies[e['Git_blob_OID']])
    return {'commit':commit,'docs_tree':tree,'entries':entries,'bodies':{e['path']:bodies[e['Git_blob_OID']] for e in entries}}
class Page(HTMLParser):
    def __init__(self):super().__init__();self.title=False;self.title_data=[];self.links=[];self.meta=[];self.canonical=[]
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if tag=='title':self.title=True
        if tag=='meta':self.meta.append(a)
        if tag=='link' and 'canonical' in a.get('rel','').split():self.canonical.append(a.get('href'))
        if tag in ['a','link','object','embed','script']:self.links.append({'tag':tag,'attributes':a})
    def handle_endtag(self,tag):
        if tag=='title':self.title=False
    def handle_data(self,data):
        if self.title:self.title_data.append(data)

try:
    before=guard();save('GUARDS_BEFORE.json',before)
    require(meta(CLEAR)['SHA256']=='008042d4a6d50c8bd0bfdc979db9afeff5c808091aaa2c8be5b4ec25c9dd6ada','scientific_identity_clearance_pin')
    require(meta(REVIEW)['SHA256']=='527f2415f022d84d4344175c3abaedb8057c8006b4f6a184830bdd2eebfce848','root_review_identity_pin')
    require(before['M_native']['resolved_local_HEAD']==NATIVE and before['M_native']['files']['index']['SHA256']=='91b10d938f7d737226662bbff3b07016dcc0e501376a045811ab4e930c6fbb11','native_main_and_index_identity')
    source=before['source'];require(len(source['files'])==51 and len(source['directories'])==12 and not source['other'],'complete_51_file_12_directory_source')
    sm=json.loads((S/'SOURCE_MANIFEST.json').read_text());expected={x['path']:x for x in sm['entries']}
    actual={'.':{'path':'.','kind':'directory','mode_octal':source['root_mode'],'empty':not(source['files'] or source['directories'])}}
    for n,v in source['files'].items():actual[n]={'path':n,'kind':'file','mode_octal':v['mode'],'bytes':v['bytes'],'sha256':v['SHA256'],'md5':hashlib.md5((S/n).read_bytes()).hexdigest()}
    for n,v in source['directories'].items():actual[n]={'path':n,'kind':'directory','mode_octal':v,'empty':not any((S/n).iterdir())}
    actual={k:v for k,v in actual.items() if k not in sm['excluded_control_files']}
    require(actual==expected,'complete_source_manifest_paths_bytes_modes_hashes_topology')
    native_assets={}
    for n,(length,h) in PINS.items():
        v=meta(S/'zenodo-files'/n);require(v['bytes']==length and v['SHA256']==h,'native_asset_pin_'+n);native_assets[n]=v
    record=json.loads((S/'native-metadata/record-api.json').read_text())
    require('version' not in record['metadata'] and [x['key'] for x in record['files']]==list(PINS),'API_version_absence_and_PDF_ZIP_README_order')
    save('NATIVE_IDENTITY.json',{'record':record,'assets':native_assets,'root_review':meta(REVIEW),'clearance':meta(CLEAR),'proposed_target':'https://aleckriebel.com/research/even-minkowski-uniqueness/','target_live_verified':False})
    command('physical_rg_files',['rg','--files','--hidden','--no-ignore',str(M/'docs')])
    command('physical_rg_keywords',['rg','--hidden','--no-ignore','-n','-i','-e',PATTERN,str(M/'docs')],allowed=(0,1))
    command('physical_rg_native_SHA256',['rg','--hidden','--no-ignore','-n','-F',*sum([['-e',h] for _,h in PINS.values()],[]),str(M/'docs')],allowed=(0,1))
    scopes={'native_HEAD':git_scope('native_HEAD',NATIVE,'6ccfd5ab446400dc7fb3933dcc2e374cb415fa90'),
            'scoped_release':git_scope('scoped_release',RELEASE,'e63ba1f227e5aa2f0e06fd6a52b36afa1531a4d0')}
    for label,scope in scopes.items():
        git(label+'_grep_keywords',['grep','-I','-n','-i','-E','-e',PATTERN,scope['commit'],'--','docs'],allowed=(0,1))
        git(label+'_grep_native_SHA256',['grep','-I','-n','-F',*sum([['-e',h] for _,h in PINS.values()],[]),scope['commit'],'--','docs'],allowed=(0,1))
    delta=git('native_vs_released_docs_delta',['diff','--name-status',NATIVE,RELEASE,'--','docs']).decode().splitlines()
    require(len(delta)==13 and all(x.startswith('M\t') for x in delta),'intentional_13_modified_paths_between_snapshots')
    physical={'entries':[{'path':'docs/'+n,**v} for n,v in before['physical_native_docs']['files'].items()],
              'bodies':{'docs/'+n:(M/'docs'/n).read_bytes() for n in before['physical_native_docs']['files']},'commit':None,'docs_tree':None}
    scopes['physical_native']=physical
    candidates=[];inventories={};matches={};wrapper=[]
    sizes={n for n,_ in PINS.values()};target_hashes={v['SHA256']:n for n,v in native_assets.items()}
    def zip_scan(label,data,depth=0):
        row={'archive':label,'depth':depth,'outer_bytes':len(data),'outer_SHA256':sha(data),'members':[],'native_matches':[],'nested_exclusions':[]}
        with zipfile.ZipFile(io.BytesIO(data)) as z:
            for info in z.infolist():
                m={'name':info.filename,'bytes':info.file_size,'compressed_bytes':info.compress_size,'CRC32':format(info.CRC,'08x'),'directory':info.is_dir()}
                if not info.is_dir() and info.file_size in sizes:
                    b=z.read(info);m.update(SHA256=sha(b),Git_blob_OID=blob(b))
                    if sha(b) in target_hashes:row['native_matches'].append({'member':info.filename,'native_asset':target_hashes[sha(b)],'SHA256':sha(b)})
                if not info.is_dir() and info.filename.lower().endswith('.zip'):
                    if depth==0 and info.file_size<=8*1024*1024:zip_scan(label+'!'+info.filename,z.read(info),1)
                    else:row['nested_exclusions'].append({'member':info.filename,'reason':'Bound: one nested level, at most 8 MiB'})
                row['members'].append(m)
        wrapper.append(row)
    for label,scope in scopes.items():
        inventories[label]={'commit':scope['commit'],'docs_tree':scope['docs_tree'],'entries':scope['entries']}
        found=[]
        for e in scope['entries']:
            for name,v in native_assets.items():
                by_sha=e['SHA256']==v['SHA256'];by_blob=e['Git_blob_OID']==v['Git_blob_OID'];require(by_sha==by_blob,'SHA256_BLOB_correspondence_agrees')
                if by_sha:found.append({'path':e['path'],'native_asset':name,'SHA256':e['SHA256'],'Git_blob_OID':e['Git_blob_OID']})
        matches[label]=found
        for path,data in scope['bodies'].items():
            if path.lower().endswith('.zip'):zip_scan(label+':'+path,data)
            if not path.lower().endswith('.html'):continue
            text=data.decode('utf-8');reason=[]
            if re.search(PATTERN,text,re.I):reason.append('keyword_or_record_in_actual_full_HTML')
            if re.search(r'minkowski|brunn|log[-_ ]?bm',path,re.I):reason.append('route_name')
            if any(x['path'].rsplit('/',1)[0]==path.rsplit('/',1)[0] for x in found):reason.append('same_directory_as_exact_native_asset')
            if not reason:continue
            page=Page();page.feed(text);dest=A/'candidate-HTML'/label/path;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(data)
            candidates.append({'scope':label,'path':path,'reason':reason,'bytes':len(data),'SHA256':sha(data),'title':''.join(page.title_data),
                               'canonical':page.canonical,'meta':page.meta,'linked_assets_and_scripts':page.links,'saved_path':str(dest.relative_to(A)),
                               'full_body_personally_read_after_collection':False})
    routes=['docs/papers/even-minkowski-uniqueness/index.html','docs/papers/log-minkowski/index.html','docs/papers/log-brunn-minkowski/index.html','docs/research/even-minkowski-uniqueness/index.html']
    save('COMPLETE_LEAF_INVENTORIES.json',inventories);save('NATIVE_ASSET_CORRESPONDENCE.json',{'native_assets':native_assets,'all_scopes_exact_outer_matches':matches})
    save('WRAPPER_CORRESPONDENCE.json',{'bounds':'All current outer .zip files across the three exact scopes; every member metadata row; target-size members hashed regardless of name; one nested ZIP level <=8 MiB; no extraction or execution.','archives':wrapper,'native_member_matches':sum(len(x['native_matches']) for x in wrapper),'exclusions':sum(len(x['nested_exclusions']) for x in wrapper)})
    save('CANDIDATE_HTML.json',candidates)
    save('COLLECTION.json',{'UTC':now(),'status':'COLLECTED_FOR_PERSONAL_CORRESPONDENCE_REVIEW','source_identity':record['metadata']['title'],'native_API_version_absent':True,
         'scope_counts':{k:len(v['entries']) for k,v in scopes.items()},'snapshot_delta':delta,'keyword_candidates':len(candidates),
         'exact_outer_asset_match_counts':{k:len(v) for k,v in matches.items()},'wrapper_native_matches':sum(len(x['native_matches']) for x in wrapper),
         'wrapper_exclusions':sum(len(x['nested_exclusions']) for x in wrapper),'specific_routes':[{**{'path':p},**{k:any(e['path']==p for e in v['entries']) for k,v in scopes.items()}} for p in routes],
         'legacy_source_url':None,'verified_redirect_target':None,'proposed_target':'https://aleckriebel.com/research/even-minkowski-uniqueness/','target_live_verified':False,'global_historical_absence_asserted':False,
         'collector_attempts':1,'helper_source_import_AST_compile_test_execution':0,'network_or_protected_mutation':False,'row191_findings_disclosed':False})
except BaseException as ex:
    failure={'UTC':now(),'criterion':active,'exception':repr(ex),'traceback':traceback.format_exc()};save('FIRST_FAILURE.json',failure);sys.stderr.write(failure['traceback'])
finally:
    after=guard();save('GUARDS_AFTER.json',after);unchanged=before is not None and {k:v for k,v in before.items() if k!='UTC'}=={k:v for k,v in after.items() if k!='UTC'}
    if not unchanged and failure is None:
        failure={'UTC':now(),'criterion':'complete_protected_guards','exception':'Protected scope changed','traceback':''};save('FIRST_FAILURE.json',failure);sys.stderr.write(failure['exception']+'\n')
    save('ATTEMPT_RESULT.json',{'UTC':now(),'status':'FIRST_FAILURE_STOP' if failure else 'COLLECTION_COMPLETE','first_failure':failure,'complete_protected_guards_unchanged':unchanged,'attempts':1,'retries':0})
    print(json.dumps({'status':'FIRST_FAILURE_STOP' if failure else 'COLLECTION_COMPLETE','guards_unchanged':unchanged,'first_failure':failure['criterion'] if failure else None}))
sys.exit(1 if failure else 0)
