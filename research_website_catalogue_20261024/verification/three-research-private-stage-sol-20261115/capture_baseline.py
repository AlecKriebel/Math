#!/usr/bin/env python3
"""Explicit read-only website baseline/fence. Only this new packet is written.
No network, Git mutation, hooks, scientific imports, builds or outside writes.
Without an explicit mode this helper performs no live operation.
"""
from pathlib import Path
import datetime,hashlib,json,os,re,stat,struct,subprocess,sys
import xml.etree.ElementTree as ET
N=Path(__file__).absolute().parent
W=Path('/Users/alec/Desktop/alec-dev/aleckriebel.com')
SITE=['.firebaserc','firebase.json','.gitignore','README.md','deploy.sh','preview.sh']
GIT=['.git/HEAD','.git/refs/heads/master','.git/config']
CACHE={'research/index.html','research/sitemap.xml','research/research.css','research/five-outgoing-centers-alpha16/index.html'}
def need(ok,why):
    if not ok:raise ValueError(why)
def utc():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def pin(b):return {'bytes':len(b),'SHA256':hashlib.sha256(b).hexdigest()}
def read(p):
    need(p.is_relative_to(W) or p.is_relative_to(N),'bounded read scope');a=p.lstat();need(stat.S_ISREG(a.st_mode),'ordinary '+str(p));fd=os.open(p,os.O_RDONLY|os.O_NOFOLLOW)
    try:
        first=os.fstat(fd);need((a.st_dev,a.st_ino)==(first.st_dev,first.st_ino),'open identity');chunks=[]
        while True:
            b=os.read(fd,1048576)
            if not b:break
            chunks.append(b)
        last=os.fstat(fd);end=p.lstat();need((first.st_size,first.st_mtime_ns,first.st_ctime_ns)==(last.st_size,last.st_mtime_ns,last.st_ctime_ns),'stable held buffer');need((end.st_dev,end.st_ino)==(first.st_dev,first.st_ino),'path identity');b=b''.join(chunks);need(len(b)==first.st_size,'whole read');return b
    finally:os.close(fd)
def new(p,b):
    need(p.is_relative_to(N),'only owned writes');p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('xb') as f:need(f.write(b)==len(b),'complete exclusive write')
def encoded(v):return (json.dumps(v,ensure_ascii=False,indent=2)+'\n').encode()
def public(cache=False):
    files=[];dirs=[]
    def visit(d):
        before=d.lstat();need(stat.S_ISDIR(before.st_mode),'ordinary directory')
        for p in sorted(d.iterdir()):
            rel=p.relative_to(W/'public').as_posix();mode=p.lstat().st_mode
            if stat.S_ISDIR(mode):dirs.append(rel);visit(p)
            elif stat.S_ISREG(mode):
                b=read(p);row={'path':rel,**pin(b)};files.append(row)
                if cache and rel in CACHE:new(N/'raw/public'/rel,b)
            else:raise ValueError('public symlink/FIFO/special '+rel)
        after=d.lstat();need((before.st_dev,before.st_ino,before.st_mtime_ns,before.st_ctime_ns)==(after.st_dev,after.st_ino,after.st_mtime_ns,after.st_ctime_ns),'stable directory enumeration')
    visit(W/'public');return sorted(files,key=lambda r:r['path']),sorted(dirs)
def controls(cache=False):
    rows=[]
    for name in SITE+GIT:
        b=read(W/name);rows.append({'path':str(W/name),'relative_path':name,**pin(b),'role':'site_config' if name in SITE else 'Git_control'})
        if cache:new(N/'raw/controls'/name,b)
    return rows
def main():
    need(sys.argv[1:] in [[],['capture'],['fence']],'finite explicit modes')
    if not sys.argv[1:]:
        print(json.dumps({'status':'EXPLICIT_CAPTURE_OR_FENCE_REQUIRED','live_reads':False,'writes':0,'network_requests':0}));return
    mode=sys.argv[1];need(not (N/'FINAL_SEAL.json').exists(),'immutable FINAL');need(not (N/('WEBSITE_BASELINE.json' if mode=='capture' else 'POST_FENCE.json')).exists(),'retain earlier attempt')
    receipts=[]
    def git(label,args):
        need(args[0] in ['rev-parse','symbolic-ref','ls-files','diff'],'read-only builtins only')
        argv=['git','--no-optional-locks','-c','core.fsmonitor=false','-c','core.hooksPath=/dev/null','-C',str(W),*args]
        r=subprocess.run(argv,capture_output=True,timeout=30);streams={}
        for key,b in [('stdout',r.stdout),('stderr',r.stderr)]:
            p=N/'raw'/(mode+'-'+label+'.'+key);new(p,b);streams[key]={'path':str(p),**pin(b)}
        receipts.append({'argv':argv,'exit_code':r.returncode,**streams});need(r.returncode==0,'read-only Git failed; retain failure/no retry');return r.stdout
    def state(label):
        need(git(label+'-top',['rev-parse','--show-toplevel']).decode().strip()==str(W),'exact website repository')
        need(git(label+'-branch',['symbolic-ref','HEAD']).strip()==b'refs/heads/master','actual master')
        refs=git(label+'-refs',['rev-parse','HEAD','refs/heads/master','HEAD^{tree}']).decode().splitlines();need(len(refs)==3 and refs[0]==refs[1],'actual HEAD/master identity')
        need(not os.path.lexists(W/'.git/index.lock'),'no active native index lock')
        raw=read(W/'.git/index');need(raw[:4]==b'DIRC' and hashlib.sha1(raw[:-20]).digest()==raw[-20:],'complete native index/checksum')
        return {'HEAD':refs[0],'master':refs[1],'tree':refs[2],'raw_index':pin(raw),'native_index_version':struct.unpack('>I',raw[4:8])[0],'native_index_records':struct.unpack('>I',raw[8:12])[0]},raw
    before,raw=state('before');stage=git('whole-stage',['ls-files','--stage','-z']);need(stage.endswith(b'\0') and stage.count(b'\0')==before['native_index_records'],'whole stage output/native header count')
    deletes=git('staged-deletions',['diff','--cached','--name-only','--diff-filter=D','-z','HEAD'])
    files,dirs=public(mode=='capture');ctl=controls(mode=='capture')
    if mode=='capture':new(N/'raw/shared-index.before',raw)
    index=read(W/'public/research/index.html');graphs=[json.loads(x) for x in re.findall(rb'<script type="application/ld\+json">\s*(.*?)\s*</script>',index,re.S)];collection=[g for g in graphs if type(g.get('mainEntity')) is dict and 'itemListElement' in g['mainEntity']];need(len(collection)==1,'one observed inventory ItemList');items=collection[0]['mainEntity'];need(items['numberOfItems']==len(items['itemListElement']),'actual inventory count');xml=read(W/'public/research/sitemap.xml');xmlcount=len(ET.fromstring(xml));counts=[len(files),len(items['itemListElement']),xmlcount]
    after,rawafter=state('after');filesafter,dirsafter=public();need(before==after and raw==rawafter and (files,dirs)==(filesafter,dirsafter) and ctl==controls(),'whole before/after fences stable')
    result={'UTC':utc(),'mode':mode,'website_root':str(W),'Git':before,'public_files':files,'public_directories':dirs,'site_and_Git_controls':ctl,'baseline_counts':counts,'raw_native_index_file':'raw/shared-index.before','all_native_index_records_retained_as_complete_opaque_original_buffer':True,'whole_stage_raw_output_retained':True,'raw_index_not_rebuilt_or_reordered':True,'staged_deletions_raw':pin(deletes),'actual_readonly_Git_receipts':receipts,'all_before_after_fences_unchanged':True,'network_requests':0,'programme_Git_read_or_frozen':False,'publication_authority':False,'canonical_url':None,'AA':None,'follow_up':None}
    if mode=='capture':
        result['root_hints_observed_matches']={'counts631_96_97':counts==[631,96,97],'HEAD_master2b78':before['HEAD']=='2b78e689e571e658daa859f29b97a61b9ec479ed','index5f9c':before['raw_index']['SHA256']=='5f9c24f576cca18c466163a9572120f118698ead90eca728199030ba346e8244','records58571':before['native_index_records']==58571}
        new(N/'WEBSITE_BASELINE.json',encoded(result))
    else:
        base=json.loads(read(N/'WEBSITE_BASELINE.json'));need(before==base['Git'] and files==base['public_files'] and dirs==base['public_directories'] and ctl==base['site_and_Git_controls'] and raw==read(N/'raw/shared-index.before'),'complete current baseline still exact');old=next(r for r in base['actual_readonly_Git_receipts'] if r['argv'][-3:]==['ls-files','--stage','-z']);need(stage==read(Path(old['stdout']['path'])),'all raw index stage records unchanged');new(N/'POST_FENCE.json',encoded(result))
    print(json.dumps({'status':'ACTUAL_READONLY_BASELINE_CAPTURED' if mode=='capture' else 'ACTUAL_READONLY_BASELINE_UNCHANGED','counts':counts,**before,'no_production_mutation':True},sort_keys=True))
if __name__=='__main__':main()
