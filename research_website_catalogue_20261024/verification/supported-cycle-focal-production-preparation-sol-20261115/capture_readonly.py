"""Finite PRE/POST read-only website/source drift guard; no production operation.
Self-contained stdlib body for root reading before any fresh website/Git access.
Writes only new receipts in this preparation. Never imports old/project code.
"""
from datetime import datetime,timezone
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import subprocess
import sys
import xml.etree.ElementTree as ET

N=Path(__file__).absolute().parent
P=N.parent.parent
W=Path('/Users/alec/Desktop/alec-dev/aleckriebel.com')
BASE='0880af3e389248dbcd098ac275a880d93e09ea99'
INDEX='35181f4046df6e197ba5c5c6e34c348b2b46783c0cc073a5b7f066692ba332b6'
ROOT='408b6cb8660952c23e54f803d543eb82d3f226338371558871c76e59701cbc20'
INITIAL='143b8dcde67b8923122c3fe133814a552a154c3c0a9ca4ea822de743e74e59a5'

def need(ok,why):
    if not ok:raise ValueError(why)

def sha(b):return hashlib.sha256(b).hexdigest()

def read(p):
    need(p.resolve()==p and stat.S_ISREG(p.lstat().st_mode),'ordinary no-link input '+str(p));return p.read_bytes()

def extent(root):
    need(root.resolve()==root and stat.S_ISDIR(root.lstat().st_mode),'ordinary real root')
    fs,ds=[],[]
    def walk(d):
        for e in os.scandir(d):
            q=Path(e.path);r=q.relative_to(root).as_posix();m=q.lstat().st_mode
            if stat.S_ISDIR(m):ds.append(r);walk(q)
            else:need(stat.S_ISREG(m),'reject namespace link/special');fs.append(r)
    walk(root);return sorted(fs),sorted(ds)

def pin(p,r):
    b=read(p);need(len(b)==r['bytes'] and sha(b)==r['SHA256'],'whole reference pin '+str(p));return b

def new(p,b):
    need(p.is_relative_to(N),'owned receipt only')
    with p.open('xb') as f:need(f.write(b)==len(b),'complete owned receipt')

def main():
    need(sys.argv[1:] in [['pre'],['post']],'finite explicit read-only phase');phase=sys.argv[1]
    need(not (N/'FINAL_SEAL.json').exists() and not (N/(phase.upper()+'_GUARD.json')).exists(),'one pre-FINAL capture per phase')
    ib=read(N/'INITIAL_SEAL.json');need(sha(ib)==INITIAL,'fixed source-only initial');initial=json.loads(ib)
    ob=pin(N/'INPUT_ORACLE.json',initial['INPUT_ORACLE']);oracle=json.loads(ob)
    rb=pin(Path(oracle['root_adoption']['path']),oracle['root_adoption']);need(sha(rb)==ROOT,'actual new root408b receipt');root=json.loads(rb)
    need(root['root_complete_current_code_and_output_adopted'] is True and root['separate_bounded_production_mechanism_preparation_authorized'] is True and root['production_installation_authorized'] is False,'root grants preparation only')
    # All above reads are source-only. Fresh website access starts below this gate.
    ref=next(r for r in oracle['closed_reference_packets'] if r['kind']=='old');oldroot=Path(ref['root'])
    sb=pin(oldroot/ref['seal_name'],ref['seal']);oldseal=json.loads(sb)
    mb=pin(oldroot/ref['manifest_name'],ref['manifest']);need(sha(mb)==oldseal['manifest']['SHA256'],'same-buffer held baseline manifest');oldmanifest=json.loads(mb)
    baseline_path=Path(oracle['old_baseline_reference']);need(baseline_path==oldroot/'WEBSITE_BASELINE.json','fixed old baseline location')
    baseline=json.loads(pin(baseline_path,oldmanifest['payloads']['WEBSITE_BASELINE.json']))
    raw_reference=Path(oracle['raw_index_reference']);need(raw_reference==oldroot/'private/shared-index.before' and sha(pin(raw_reference,oldmanifest['payloads']['private/shared-index.before']))==INDEX,'held whole index reference')
    if phase=='pre':(N/'private').mkdir()
    receipts=[]
    def git(*args):
        need(args[0] in {'rev-parse','symbolic-ref','remote','ls-remote','ls-files','diff'},'read-only Git allowlist')
        env={k:v for k,v in os.environ.items() if not k.startswith('GIT_')};env['GIT_OPTIONAL_LOCKS']='0'
        command=['git','-c','core.fsmonitor=false','-c','core.hooksPath=/dev/null',*args]
        try:
            r=subprocess.run(command,cwd=W,env=env,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=30)
            output,error,code,timedout=r.stdout,r.stderr,r.returncode,False
        except subprocess.TimeoutExpired as exc:
            output,error,code,timedout=exc.output or b'',exc.stderr or b'',None,True
        rec={'ordinal':len(receipts)+1,'operation':args[0],'arguments':[a if not(a.startswith('http') or a.startswith('git@')) else '<bound explicit push destination>' for a in args],'actual_exit':code,'timed_out':timedout}
        for name,b in [('stdout',output),('stderr',error)]:
            old=next((x for x in baseline['actual_readonly_Git_receipts'] if x['operation']==args[0]),None)
            alias=oldroot/old[name] if old and args[0]=='ls-files' else None
            if len(b)>4096 and alias is not None and pin(alias,oldmanifest['payloads'][alias.relative_to(oldroot).as_posix()])==b:
                destination=alias;byref=True
            else:
                destination=N/'private'/('%s-git-%02d.%s'%(phase,len(receipts)+1,name));new(destination,b);byref=False
            rec[name]={'path':str(destination),'bytes':len(b),'SHA256':sha(b),'whole_actual_bytes_retained_by_reference':byref}
        receipts.append(rec)
        if code!=0 or timedout:
            new(N/(phase.upper()+'_FAILED_GIT.json'),(json.dumps(receipts,indent=2)+'\n').encode())
            raise ValueError('read-only Git failed; full actual streams retained; no retry')
        return output
    def state():
        need(git('rev-parse','--show-toplevel').decode().strip()==str(W),'exact website repository')
        need(git('symbolic-ref','HEAD').strip()==b'refs/heads/master','existing master branch')
        values=git('rev-parse','HEAD','refs/heads/master','HEAD^{tree}').decode().splitlines()
        need(values==[BASE,BASE,'41a222e824f23b5efc0acd4f5a92ea50c4572cfa'],'actual0880master/tree')
        urls=git('remote','get-url','--push','--all','origin').splitlines();need(len(urls)==1 and sha(urls[0])==baseline['Git']['origin_push_URL_SHA256'],'one exact actual push destination')
        remote=git('ls-remote','--refs',urls[0].decode(),'refs/heads/master');need(remote.split()==[BASE.encode(),b'refs/heads/master'],'actual remote advertised oldSHA')
        raw=read(W/'.git/index');need(sha(raw)==INDEX and raw==read(raw_reference),'every fresh native raw index byte equals held reference')
        need(not os.path.lexists(W/'.git/index.lock'),'no shared index lock')
        controls={n:sha(read(W/'.git'/n)) for n in ('HEAD','refs/heads/master','config')}
        return {'HEAD':BASE,'master':BASE,'tree':values[2],'index_SHA256':sha(raw),'index_mode':stat.S_IMODE((W/'.git/index').lstat().st_mode),'remote_advertisement':remote.decode(),'push_URL_SHA256':sha(urls[0]),'controls_SHA256':controls}
    before=state()
    actual=git('ls-files','--stage','-z');oldls=next(x for x in baseline['actual_readonly_Git_receipts'] if x['operation']=='ls-files')
    need(actual==read(oldroot/oldls['stdout']),'whole native stage tuples remain exact')
    deletions=git('diff','--cached','--name-only','--diff-filter=D','-z',BASE);need(deletions==b'','zero actual staged deletions; raw records are protected records')
    need(extent(W/'public')==(baseline['public_namespace'],baseline['public_directories']) and len(baseline['public_namespace'])==623,'whole exact623 public namespace')
    observed=[]
    for r in baseline['files']:
        b=read(Path(r['path']));need(b==pin(oldroot/r['blob'],r),'all public/config/control bodies unchanged')
        observed.append({k:r[k] for k in ('path','bytes','SHA256','role')})
    graph=json.loads(re.findall(rb'<script type="application/ld\+json">\s*(.*?)\s*</script>',read(W/'public/research/index.html'),re.S)[0])['mainEntity']
    need(graph['numberOfItems']==len(graph['itemListElement'])==94 and len(ET.fromstring(read(W/'public/research/sitemap.xml')))==95,'fresh94index95XML')
    for r in oracle['frozen_original_files']:pin(Path(r['path']),r)
    for ns in oracle['closed_original_namespaces']:need(extent(Path(ns['path']))==(ns['files'],ns['directories']),'complete source/editorial/science/root extent')
    for r in oracle['exact10']:
        pin(Path(r['source']),r)
        if r['action']=='add':need(not os.path.lexists(W/'public'/r['path']),'all eight exact new leaves absent')
    after=state();need(before==after,'complete start/end Git/index/control/remote guard')
    value={'UTC':datetime.now(timezone.utc).isoformat(),'status':'PASS_FRESH_EXACT10_READONLY_DRIFT_FENCE','phase':phase,'root_adoption_SHA256':ROOT,'INPUT_ORACLE_SHA256':sha(ob),'Git':after,'baseline_counts':[623,94,95],'proposed_counts':[631,96,97],'public_configs_controls':observed,'raw_index_reference':str(raw_reference),'complete_raw_records':58563,'protected_raw_records':58561,'protected_raw_SHA256':baseline['native_index']['protected_native_raw_records_SHA256'],'actual_staged_deletions':0,'actual_original_files':len(oracle['frozen_original_files']),'actual_closed_original_namespaces':len(oracle['closed_original_namespaces']),'actual_Git_receipts':receipts,'programme_HEAD_sharedindex_refs_read_or_frozen':False,'current_native_context_only':107,'production_mutation':False}
    new(N/(phase.upper()+'_GUARD.json'),(json.dumps(value,indent=2)+'\n').encode())
    print(json.dumps({'status':value['status'],'phase':phase,'actual_counts':[623,94,95],'public_configs_controls':len(observed),'original_files':len(oracle['frozen_original_files']),'closed_original_namespaces':len(oracle['closed_original_namespaces']),'actual_readonly_Git_commands':len(receipts),'protected_raw_records':58561,'production_mutation':False},sort_keys=True))

if __name__=='__main__':main()
