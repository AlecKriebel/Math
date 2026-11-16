"""New bounded root-authorized read-only drift fence. Writes only owned receipts.
Imports only the newly read V2 custody helper; never imports or runs old code.
"""
import sys
sys.dont_write_bytecode=True
from datetime import datetime,timezone
import json
import os
from pathlib import Path
import stat
import subprocess
import re
import xml.etree.ElementTree as ET
import verify_v2 as V

N=V.N;W=Path('/Users/alec/Desktop/alec-dev/aleckriebel.com')
BASE='0880af3e389248dbcd098ac275a880d93e09ea99'

def ordinary(p):
    V.need(p.resolve()==p and stat.S_ISREG(p.lstat().st_mode),'ordinary exact live allowlisted path')
    return p.read_bytes()

def new(p,b):
    V.need(p.is_relative_to(N),'owned receipt only')
    with p.open('xb') as f:V.need(f.write(b)==len(b),'whole receipt write')

def main():
    V.need(sys.argv[1:] in [['pre'],['post']],'explicit finite guard phase')
    phase=sys.argv[1];name=phase.upper()+'_GUARD.json'
    V.need(not (N/'FINAL_SEAL.json').exists() and not (N/name).exists(),'one pre-FINAL guard per phase')
    inputs,baseline,source_rows=V.references()
    auth=V.P/'verification/root-supported-cycle-focal-corrective-private-v2-authorization-20261115.json'
    V.need(V.digest(ordinary(auth))==V.AUTH,'actual current root authorization matches frozen copy')
    if phase=='pre':(N/'private').mkdir()
    receipts=[]
    def git(*args):
        V.need(args[0] in {'rev-parse','symbolic-ref','remote','ls-remote','ls-files','diff'},'read-only Git allowlist')
        env={k:v for k,v in os.environ.items() if not k.startswith('GIT_')};env['GIT_OPTIONAL_LOCKS']='0'
        r=subprocess.run(['git','-c','core.fsmonitor=false','-c','core.hooksPath=/dev/null',*args],cwd=W,env=env,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=30)
        rec={'ordinal':len(receipts)+1,'operation':args[0],'arguments':[a if not(a.startswith('http') or a.startswith('git@')) else '<bound explicit push URL>' for a in args],'exit':r.returncode}
        for stream,b in [('stdout',r.stdout),('stderr',r.stderr)]:
            if len(b)>4096 and args[0]=='ls-files':
                old=next(x for x in baseline['actual_readonly_Git_receipts'] if x['operation']=='ls-files')
                p=V.OLD/old[stream];V.need(V.read(p)==b,'whole fresh stream equals retained authenticated original buffer')
                binding={'path':str(p),'by_reference_whole_actual_bytes_equal':True}
            else:
                p=N/'private'/('%s-git-%02d.%s'%(phase,len(receipts)+1,stream));new(p,b);binding={'path':str(p),'by_reference_whole_actual_bytes_equal':False}
            rec[stream]={**binding,'bytes':len(b),'SHA256':V.digest(b)}
        receipts.append(rec)
        V.need(r.returncode==0,'actual read-only Git failure; no retry')
        return r.stdout
    def state():
        V.need(git('rev-parse','--show-toplevel').decode().strip()==str(W),'exact website repository')
        V.need(git('symbolic-ref','HEAD').strip()==b'refs/heads/master','actual master')
        values=git('rev-parse','HEAD','refs/heads/master','HEAD^{tree}').decode().splitlines()
        V.need(values==[BASE,BASE,baseline['Git']['tree']],'actual0880master/tree')
        urls=git('remote','get-url','--push','--all','origin').splitlines();V.need(len(urls)==1 and V.digest(urls[0])==baseline['Git']['origin_push_URL_SHA256'],'same explicit push destination')
        advertisement=git('ls-remote','--refs',urls[0].decode(),'refs/heads/master')
        V.need(advertisement.decode()==baseline['Git']['actual_remote_advertisement'],'actual remote0880 advertisement')
        raw=ordinary(W/'.git/index');V.need(V.digest(raw)=='35181f4046df6e197ba5c5c6e34c348b2b46783c0cc073a5b7f066692ba332b6' and raw==V.read(V.OLD/baseline['full_raw_index']),'all raw native index bytes remain exact')
        V.need(not os.path.lexists(W/'.git/index.lock'),'no actual index lock')
        return {'HEAD':values[0],'master':values[1],'tree':values[2],'index_SHA256':V.digest(raw),'remote_advertisement':advertisement.decode()}
    before=state()
    fresh_index=git('ls-files','--stage','-z')
    oldls=next(x for x in baseline['actual_readonly_Git_receipts'] if x['operation']=='ls-files')
    V.need(fresh_index==V.read(V.OLD/oldls['stdout']),'all actual stage tuples unchanged')
    deletions=git('diff','--cached','--name-only','--diff-filter=D','-z',BASE)
    V.need(deletions==b'','actual staged deletions zero; records are protected records')
    files,dirs=V.extent(W/'public');V.need(files==baseline['public_namespace'] and dirs==baseline['public_directories'] and len(files)==623,'all actual623 ordinary paths/directories')
    observations=[]
    for r in baseline['files']:
        b=ordinary(Path(r['path']));V.need(b==V.pin(V.OLD/r['blob'],r),'whole actual public/config/control bytes versus pinned baseline')
        observations.append({'path':r['path'],'bytes':len(b),'SHA256':V.digest(b),'role':r['role']})
    current_index=ordinary(W/'public/research/index.html');g=json.loads(re.findall(rb'<script type="application/ld\+json">\s*(.*?)\s*</script>',current_index,re.S)[0])
    V.need(g['mainEntity']['numberOfItems']==len(g['mainEntity']['itemListElement'])==94 and len(ET.fromstring(ordinary(W/'public/research/sitemap.xml')))==95,'fresh actual94index95XML')
    for r in inputs['files']:V.need(ordinary(Path(r['path']))==V.pin(V.OLD/r['blob'],r),'all819 actual source/editorial/fact/root buffers')
    for ns in inputs['complete_original_namespaces']:V.close(Path(ns['path']),ns['files'],ns['directories'])
    protected={}
    for rid in ['23578142','23306203']:
        e=V.P/'papers'/rid/'reviews/editorial';p=json.loads(V.cached(source_rows,e/'PROTECTED_INPUTS.json'))
        V.need(len(p['core_files'])==18,'qualified17original plus405b helper')
        for r in p['files']:
            b=ordinary(Path(r['path']));V.need(len(b)==r['bytes'] and V.digest(b)==r['SHA256'],'complete original source/science/core byte fence')
            protected[r['path']]={k:r[k] for k in ('bytes','SHA256')}
    after=state();V.need(before==after,'start/end actual refs/index/remote fence')
    result={'UTC':datetime.now(timezone.utc).isoformat(),'status':'ALL_ACTUAL_READONLY_FENCES_UNCHANGED','phase':phase,'root_corrective_authorization_SHA256':V.AUTH,'baseline_counts':[623,94,95],'proposed_counts':[631,96,97],**after,
      'all623_configs_controls_whole_observations':observations,'source_context_files':819,'protected_source_science_core_whole_bindings':protected,
      'native_index_records':58563,'protected_raw_records':58561,'raw_protected_fingerprint':baseline['native_index']['protected_native_raw_records_SHA256'],
      'raw_index_reuse_proof':'fresh whole bytes identical to original pinned complete raw buffer; no parse/rebuild or duplicate cache',
      'actual_staged_deletions':0,'actual_Git_receipts':receipts,'programme_Git_controls_read_or_frozen':False,'current_native_context_only':'94verified106science102finalized; old92unchanged','production_mutation':False}
    new(N/name,(json.dumps(result,indent=2)+'\n').encode())
    print(json.dumps({'status':result['status'],'phase':phase,'actual_counts':[623,94,95],'whole_public_configs_controls':len(observations),'source_context_files':819,'protected_unique_source_science_core_files':len(protected),'native_index_records':58563,'protected_raw_records':58561,'actual_readonly_Git_operations':len(receipts),'production_mutation':False},sort_keys=True))

if __name__=='__main__':main()
