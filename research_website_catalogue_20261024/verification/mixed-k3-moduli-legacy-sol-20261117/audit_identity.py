"""One bounded passive identity census of physical docs and two existing Git snapshots."""
import base64, datetime, hashlib, json, os, re, stat, subprocess, time
from html.parser import HTMLParser
from pathlib import Path

M=Path('/Users/alec/Documents/Math')
P=M/'research_website_catalogue_20261024'
OWN=P/'verification/mixed-k3-moduli-legacy-sol-20261117'
SRC=P/'papers/23204176/sources'
WRITER=P/'verification/mixed-k3-moduli-editorial-sol-20261117'
NATIVE='a4ce3c37dad209339e490d18dcced6c48cf912d2'
RELEASED='15482acd0ef864af280a864758b2ac6aa24dfbe8'
TITLE='Rational Hodge classes on mixed products of K3 moduli spaces'
TARGETS={'paper.pdf':{'bytes':67264,'SHA256':'483a6edff90202ef4d31560049a32ce946dcd1c6a999ab5b1f25b66a8f326612'},'source-and-verification.zip':{'bytes':135014,'SHA256':'8f44cd5f9c447e40a97a07a3bcc62998accdb7aad4fce94b4020c5fe87f77ce0'}}
START=datetime.datetime.now(datetime.timezone.utc).isoformat()
clock=time.monotonic()
(OWN/'raw').mkdir()
(OWN/'candidates').mkdir()
calls=[]
env=dict(os.environ,GIT_OPTIONAL_LOCKS='0')
for k in ('GIT_DIR','GIT_WORK_TREE','GIT_INDEX_FILE','GIT_COMMON_DIR','GIT_OBJECT_DIRECTORY','GIT_ALTERNATE_OBJECT_DIRECTORIES'):env.pop(k,None)
GIT=['/usr/bin/git','--no-optional-locks','-c','core.hooksPath=/dev/null','-c','core.fsmonitor=false','-c','gc.auto=0']

def writej(name,data):
    with (OWN/name).open('x') as f:json.dump(data,f,ensure_ascii=False,indent=2);f.write('\n')
def rawfile(name,data):
    with (OWN/name).open('xb') as f:f.write(data)
def pin_bytes(raw,mode):return dict(bytes=len(raw),SHA256=hashlib.sha256(raw).hexdigest(),MD5=hashlib.md5(raw).hexdigest(),mode=mode)
def fileread(p):
    a=p.lstat()
    assert stat.S_ISREG(a.st_mode) and not p.is_symlink(),str(p)
    with p.open('rb') as f:
        b=os.fstat(f.fileno());assert (a.st_dev,a.st_ino)==(b.st_dev,b.st_ino)
        raw=f.read();z=os.fstat(f.fileno())
    end=p.lstat();fields=lambda s:(s.st_dev,s.st_ino,s.st_size,s.st_mode,s.st_mtime_ns,s.st_ctime_ns)
    assert fields(a)==fields(z)==fields(end) and len(raw)==z.st_size
    return pin_bytes(raw,oct(stat.S_IMODE(a.st_mode))),raw
def census(root):
    files,dirs={},{'.':oct(stat.S_IMODE(root.lstat().st_mode))}
    pending=[root]
    while pending:
        here=pending.pop();a=here.lstat()
        assert stat.S_ISDIR(a.st_mode) and not here.is_symlink()
        for p in sorted(here.iterdir()):
            rel=p.relative_to(root).as_posix();s=p.lstat();assert not p.is_symlink()
            if stat.S_ISDIR(s.st_mode):dirs[rel]=oct(stat.S_IMODE(s.st_mode));pending.append(p)
            else:files[rel]=fileread(p)[0]
        z=here.lstat();assert (a.st_dev,a.st_ino,a.st_mode,a.st_mtime_ns,a.st_ctime_ns)==(z.st_dev,z.st_ino,z.st_mode,z.st_mtime_ns,z.st_ctime_ns)
    return dict(root=str(root),root_mode=dirs['.'],files=files,directories={n:m for n,m in dirs.items() if n!='.'},hidden_paths=[n for n in sorted(set(files)|set(dirs)) if n!='.' and any(x.startswith('.') for x in n.split('/'))],empty_files=[n for n,x in sorted(files.items()) if x['bytes']==0],empty_directories=[n for n in sorted(dirs) if n!='.' and not any(q.startswith(n+'/') for q in set(files)|set(dirs))])
def git(*args,data=None,keep=True):
    argv=GIT+list(args);r=subprocess.run(argv,cwd=M,env=env,input=data,capture_output=True,check=False)
    ident='raw/git-'+str(len(calls)).zfill(2)
    rawfile(ident+'.stderr.bin',r.stderr)
    if keep:rawfile(ident+'.stdout.bin',r.stdout)
    calls.append(dict(argv=argv,cwd=str(M),exit_code=r.returncode,stdout_bytes=len(r.stdout),stdout_SHA256=hashlib.sha256(r.stdout).hexdigest(),stderr_bytes=len(r.stderr),stderr_SHA256=hashlib.sha256(r.stderr).hexdigest(),stdout_file=ident+'.stdout.bin' if keep else None,stderr_file=ident+'.stderr.bin',input_bytes=len(data) if data else 0,input_SHA256=hashlib.sha256(data).hexdigest() if data else None))
    assert r.returncode==0,r.stderr.decode(errors='replace')
    return r.stdout
def refs():
    return git('rev-parse','HEAD','refs/heads/main','refs/remotes/origin/main').decode().splitlines()
def native_guard():
    native_files={}
    for n in ('HEAD','index','config','config.worktree'):
        q=Path(git('rev-parse','--git-path',n).decode().strip());q=q if q.is_absolute() else M/q
        native_files[n]=dict(path=str(q),exists=q.exists())
        if q.exists():
            value,raw=fileread(q);native_files[n].update(value)
            if n=='HEAD':native_files[n]['raw_base64']=base64.b64encode(raw).decode()
    q=Path(git('rev-parse','--git-path','refs/heads').decode().strip());q=q if q.is_absolute() else M/q
    return dict(files=native_files,HEAD=git('rev-parse','HEAD').decode().strip(),branch=git('branch','--show-current').decode().strip(),logical_local_heads=git('for-each-ref','--format=%(refname)%00%(objectname)%00%(objecttype)','refs/heads').decode(),loose_local_heads=census(q))
def trees(ref):
    result={}
    for row in git('ls-tree','-r','-t','-z','--full-tree',ref,'--','docs').split(b'\0'):
        if row:
            head,path=row.split(b'\t',1);mode,kind,oid=head.decode().split();name=path.decode()
            assert name not in result
            result[name]=dict(mode=mode,type=kind,OID=oid)
    return result
def delta(a,b):
    return [dict(path=n,before=a.get(n),after=b.get(n)) for n in sorted(set(a)|set(b)) if a.get(n)!=b.get(n)]

refs_before=refs()
assert refs_before==[NATIVE,NATIVE,RELEASED]
before=dict(native_M=native_guard(),physical_docs=census(M/'docs'),sources=census(SRC),writer=census(WRITER))
assert before['native_M']['HEAD']==NATIVE and before['native_M']['branch']=='main'
assert len(before['sources']['files'])==43 and len(before['sources']['directories'])==7
assert len(before['writer']['files'])==28 and len(before['writer']['directories'])==1
for name,digest in {'SOURCE_MANIFEST.json':'53be96c6f47deccccc173286d10bdf46b50df4f237c985f42f2da8a69d8c8ffb','SOURCE_FINAL.json':'f7bc05f4e7d56f0fbad45d77bdb4992d9fd92de8d976bdc5ff3b446f7dbfe9c8'}.items():assert before['sources']['files'][name]['SHA256']==digest
for name,digest in {'MANIFEST.json':'1aa3d7271c59f80db746b41005b605d2e68ec448cdf3125b3b282ae7e6acb171','FINAL.json':'245fcc03a3105d4a3a093821bd79e995d13225246a5e0f96b7a6c3e322a814b8'}.items():assert before['writer']['files'][name]['SHA256']==digest
writej('GUARDS_BEFORE.json',before)
source_api=json.loads((SRC/'native-metadata/record-api.json').read_bytes())
assert source_api['id']==23204176 and source_api['metadata']['title']==TITLE
assert [x['key'] for x in source_api['files']]==list(TARGETS)
for n,v in TARGETS.items():
    actual=before['sources']['files']['zenodo-files/'+n]
    assert all(actual[k]==x for k,x in v.items())
    assert actual==before['writer']['files']['assets/'+n]
root_input_pins={}
for n,digest in {'verification/root-clearance-23204176-20261117.json':'ea5472784dffe99ee849d40700541b9453466b2f3edf064a3a02fe091e7f55cd','papers/23204176/reviews/root-continuation-20261117/ROOT_REVIEW.md':'726d07488144fb2a7e4cbc0351c235a4a422a42346e71410000833596c2f6b94'}.items():
    root_input_pins[n]=fileread(P/n)[0];assert root_input_pins[n]['SHA256']==digest
snapshots={'native':trees(NATIVE),'released':trees(RELEASED)}
assert snapshots['native']['docs']['OID']=='6ccfd5ab446400dc7fb3933dcc2e374cb415fa90'
assert snapshots['released']['docs']['OID']=='e63ba1f227e5aa2f0e06fd6a52b36afa1531a4d0'
oids=sorted({v['OID'] for rows in snapshots.values() for v in rows.values() if v['type']=='blob'})
batch=('\n'.join(oids)+'\n').encode();raw=git('cat-file','--batch',data=batch,keep=False)
objects={};cursor=0
for expected in oids:
    end=raw.index(b'\n',cursor);oid,kind,size=raw[cursor:end].decode().split();size=int(size);cursor=end+1
    assert oid==expected and kind=='blob'
    body=raw[cursor:cursor+size];assert len(body)==size and raw[cursor+size:cursor+size+1]==b'\n';cursor+=size+1
    assert hashlib.sha1(b'blob '+str(size).encode()+b'\0'+body).hexdigest()==oid
    objects[oid]=body
assert cursor==len(raw)
del raw

class Page(HTMLParser):
    def __init__(self):super().__init__(convert_charrefs=True);self.text=[];self.links=[];self.meta={};self.title=[];self.intitle=False
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if tag=='a':self.links.append(a.get('href',''))
        if tag=='meta' and 'name' in a:self.meta[a['name']]=a.get('content','')
        if tag=='title':self.intitle=True
    def handle_endtag(self,tag):
        if tag=='title':self.intitle=False
    def handle_data(self,data):
        self.text.append(data)
        if self.intitle:self.title.append(data)
exact_patterns={'record_id':re.compile('23204176'),'DOI':re.compile(r'10\.5281/zenodo\.23204176',re.I),'exact_title':re.compile(r'rational\s+hodge\s+classes\s+on\s+mixed\s+products\s+of\s+k3\s+moduli\s+spaces',re.I),'proposed_slug':re.compile('mixed-k3-moduli-hodge-classes',re.I)}
related=re.compile(r'\bk3\b|k3p|hodge|\bmoduli\b|bülles|bulles|arapura',re.I)
views={}
all_candidates=[]
def inspect_view(label,files):
    records={};matches={k:[] for k in exact_patterns};assets={n:[] for n in TARGETS};candidates=[]
    for path,(mode,body) in sorted(files.items()):
        value=pin_bytes(body,mode);records[path]=value
        for name,target in TARGETS.items():
            if value['bytes']==target['bytes'] and value['SHA256']==target['SHA256']:assets[name].append(path)
        try:text=body.decode('utf-8')
        except UnicodeDecodeError:continue
        page=None
        if path.lower().endswith(('.html','.htm')):
            page=Page();page.feed(text);page.close();normalized=' '.join(page.text)
        else:normalized=text
        hits=[name for name,pattern in exact_patterns.items() if pattern.search(path) or pattern.search(text) or pattern.search(normalized)]
        for name in hits:matches[name].append(path)
        if page and (hits or related.search(path) or related.search(normalized)):
            saved='candidates/'+label+'-'+str(len(candidates)).zfill(2)+'.html';rawfile(saved,body)
            candidates.append(dict(path=path,saved_file=saved,title=''.join(page.title),citation_title=page.meta.get('citation_title'),exact_identity_hits=hits,asset_and_source_links=page.links,whole_article_SHA256=value['SHA256'],whole_article_bytes=value['bytes']))
    value=dict(whole_files=len(files),all_whole_file_identities=records,exact_search_matches=matches,whole_target_asset_matches=assets,candidates=candidates)
    views[label]=value;all_candidates.extend(dict(view=label,**x) for x in candidates)
physical={}
for n,value in before['physical_docs']['files'].items():
    pin,body=fileread(M/'docs'/n);assert pin==value;physical['docs/'+n]=(value['mode'],body)
inspect_view('physical',physical)
for label,rows in snapshots.items():
    inspect_view(label,{n:(v['mode'],objects[v['OID']]) for n,v in rows.items() if v['type']=='blob'})
physical_keys=set(views['physical']['all_whole_file_identities'])
differences={}
for label in ('native','released'):
    current=views['physical']['all_whole_file_identities'];other=views[label]['all_whole_file_identities']
    differences['physical_vs_'+label]=[dict(path=n,physical=current.get(n),snapshot=other.get(n)) for n in sorted(set(current)|set(other)) if n not in current or n not in other or any(current[n][k]!=other[n][k] for k in ('bytes','SHA256','MD5')) or ('100755' if current[n]['mode'] in ('0o755','0o775') else '100644')!=other[n]['mode']]
differences['native_vs_released_all_tree_entries']=delta(snapshots['native'],snapshots['released'])
writej('SNAPSHOTS_AND_DIFFERENCES.json',dict(native_commit=NATIVE,released_commit=RELEASED,root_supplied_released_commit_not_network_verified=True,snapshots=snapshots,differences=differences))
writej('SEARCH_AND_ASSET_IDENTITIES.json',dict(schema='bounded-three-view-legacy-identity-search-v1',UTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),record_id='23204176',title=TITLE,native_asset_order=source_api['files'],target_whole_assets=TARGETS,exact_patterns={k:v.pattern for k,v in exact_patterns.items()},candidate_keyword_pattern=related.pattern,views=views,scope='All actual physical docs files and all blob leaves of the two exact existing Git docs trees; no global history, network or live absence claim'))
writej('CANDIDATE_READING_LIST.json',dict(candidates=all_candidates,personal_whole_article_read_required_before_final=True))
after=dict(native_M=native_guard(),physical_docs=census(M/'docs'),sources=census(SRC),writer=census(WRITER))
writej('GUARDS_AFTER.json',after)
assert before==after
assert root_input_pins=={n:fileread(P/n)[0] for n in root_input_pins}
refs_after=refs()
writej('AUDIT_RESULT.json',dict(schema='bounded-legacy-identity-audit-result-v1',started_UTC=START,finished_UTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),elapsed_seconds=time.monotonic()-clock,record_id='23204176',native_commit=NATIVE,released_commit=RELEASED,refs_before=refs_before,refs_after=refs_after,refs_after_observed_without_network=True,root_inputs=root_input_pins,all_native_M_docs_source_writer_guards_exact=True,physical_files=len(physical_keys),native_files=views['native']['whole_files'],released_files=views['released']['whole_files'],unique_Git_blob_objects=len(oids),all_Git_blob_bodies_authenticated_against_OID=True,Git_blob_batch_stdout_hashed_not_saved_as_a_large_duplicate_cache=True,all_exact_search_counts={label:{k:len(v) for k,v in row['exact_search_matches'].items()} for label,row in views.items()},all_whole_target_asset_match_counts={label:{k:len(v) for k,v in row['whole_target_asset_matches'].items()} for label,row in views.items()},candidate_count=len(all_candidates),no_W_access=True,no_network_or_Git_or_source_or_writer_mutations=True,no_scientific_code_import_or_execution=True,canonical_url=None,redirect_target=None,proposed_slug_not_live_verified='mixed-k3-moduli-hodge-classes',scope='Bounded correspondence identity only, not scientific adjudication or global historical/live absence',Git_calls=calls))
with (OWN/'RESEARCH_LOG.md').open('a') as f:f.write('\n'+datetime.datetime.now(datetime.timezone.utc).isoformat()+' — One saved passive audit completed; complete native M controls/docs/source/writer before-after guards equal. Three views and every whole target asset compared; candidate articles retained for complete personal reading. Completion80%; no W access or network.\n')
print(json.dumps(dict(status='PASSIVE_AUDIT_COMPLETE_PENDING_PERSONAL_CANDIDATE_READ',files={k:v['whole_files'] for k,v in views.items()},candidate_count=len(all_candidates),exact_counts={k:{n:len(x) for n,x in v['exact_search_matches'].items()} for k,v in views.items()},asset_counts={k:{n:len(x) for n,x in v['whole_target_asset_matches'].items()} for k,v in views.items()},guards_exact=True,no_W_access=True)))
