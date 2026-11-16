"""Pure, read-only custody and exact native-index transformation. Stdlib only.
Default: authenticate this finite preparation and pinned original namespaces.
No project import, subprocess, network, science execution, or write occurs here.
"""
import hashlib
import json
import os
from pathlib import Path
import stat
import struct
import sys

N=Path(__file__).absolute().parent
P=N.parent.parent
W=Path('/Users/alec/Desktop/alec-dev/aleckriebel.com')
BASE='0880af3e389248dbcd098ac275a880d93e09ea99'
TREE='41a222e824f23b5efc0acd4f5a92ea50c4572cfa'
INDEX='35181f4046df6e197ba5c5c6e34c348b2b46783c0cc073a5b7f066692ba332b6'
PROTECTED='2a39a160e0c4a832d0afaa4159ef023f28b0ae0be03ee839d9926c370789b46c'
ROOT='408b6cb8660952c23e54f803d543eb82d3f226338371558871c76e59701cbc20'
INITIAL='143b8dcde67b8923122c3fe133814a552a154c3c0a9ca4ea822de743e74e59a5'
RUNTIME=P/'verification/supported-cycle-focal-production-runtime-sol-20261115'
INSTALL_AUTH=P/'verification/root-supported-cycle-focal-production-install-authority-20261115.json'
COMMIT_AUTH=P/'verification/root-supported-cycle-focal-production-commit-approval-20261115.json'
TERMINALS={'FINAL_SEAL.json','OWNED_MANIFEST.json'}
CHECKS=0

def need(ok,why):
    global CHECKS
    CHECKS+=1
    if not ok:raise ValueError(why)

def sha(b):return hashlib.sha256(b).hexdigest()
def descriptor(b):return {'bytes':len(b),'SHA256':sha(b)}
def encoded(x):return (json.dumps(x,indent=2,sort_keys=True)+'\n').encode()

def read(p):
    p=Path(p)
    need(p.is_absolute() and p.resolve()==p and stat.S_ISREG(p.lstat().st_mode),'ordinary real file '+str(p))
    return p.read_bytes()

def pinned(p,r):
    b=read(p);need(descriptor(b)=={k:r[k] for k in ('bytes','SHA256')},'whole body pin '+str(p));return b

def extent(root):
    root=Path(root);need(root.resolve()==root and stat.S_ISDIR(root.lstat().st_mode),'ordinary real directory '+str(root))
    files,dirs=[],[]
    def walk(d):
        with os.scandir(d) as entries:
            for e in entries:
                q=Path(e.path);r=q.relative_to(root).as_posix();m=q.lstat().st_mode
                if stat.S_ISDIR(m):dirs.append(r);walk(q)
                else:need(stat.S_ISREG(m),'reject all links and special entries '+str(q));files.append(r)
    walk(root);return sorted(files),sorted(dirs)

def sealed_reference(r):
    """Authenticate and parse the SAME held seal and manifest buffers."""
    root=Path(r['root']);sb=pinned(root/r['seal_name'],r['seal']);s=json.loads(sb)
    mb=pinned(root/r['manifest_name'],r['manifest']);m=json.loads(mb)
    if r['kind']=='old':binding=s['manifest']['SHA256']
    elif r['kind']=='old_audit':binding=s['MANIFEST_SHA256']
    elif r['kind']=='v2':binding=s['manifest_SHA256']
    else:binding=s['manifest']['SHA256']
    need(sha(mb)==binding,'seal binds exact parsed manifest buffer')
    rows=m.get('payloads')
    if rows is None:rows={x['path']:{k:x[k] for k in ('bytes','SHA256')} for x in m['files']}
    expected=sorted([*rows,r['seal_name'],r['manifest_name']])
    need(extent(root)==(expected,r['directories']),'closed ordinary files AND exact directories '+str(root))
    need(len(rows)==r['payload_files'],'literal payload count')
    for name,d in rows.items():pinned(root/name,d)
    return m

def inputs():
    ib=read(N/'INITIAL_SEAL.json');need(sha(ib)==INITIAL,'immutable source-only initial')
    initial=json.loads(ib);ob=pinned(N/'INPUT_ORACLE.json',initial['INPUT_ORACLE']);o=json.loads(ob)
    pinned(N/'INITIAL_EXPECTATIONS.json',initial['INITIAL_EXPECTATIONS'])
    root=json.loads(pinned(Path(o['root_adoption']['path']),o['root_adoption']))
    need(o['root_adoption']['SHA256']==ROOT and root['root_complete_current_code_and_output_adopted'] is True,'actual separate stage/copy adoption')
    need(root['production_installation_authorized'] is False,'stage receipt grants no production authority')
    for r in o['closed_reference_packets']:sealed_reference(r)
    for r in o['frozen_original_files']:pinned(Path(r['path']),r)
    for ns in o['closed_original_namespaces']:need(extent(Path(ns['path']))==(ns['files'],ns['directories']),'whole original namespace '+ns['path'])
    paths=[r['path'] for r in o['exact10']]
    need(paths==sorted(set(paths)) and len(paths)==10,'exact unique ordered10')
    need(sum(r['action']=='add' for r in o['exact10'])==8 and {r['path'] for r in o['exact10'] if r['action']=='replace'}=={'research/index.html','research/sitemap.xml'},'eight article-root leaves/two aggregates')
    for r in o['exact10']:pinned(Path(r['source']),r)
    return o

def oracle(o):
    return {'public/'+r['path']:hashlib.sha1(b'blob '+str(r['bytes']).encode()+b'\0'+pinned(Path(r['source']),r)).hexdigest() for r in o['exact10']}

def parse_index(raw,targets):
    """Conservative native v2 parser; retain each complete unmodified record."""
    need(len(raw)>=32 and raw[:4]==b'DIRC' and hashlib.sha1(raw[:-20]).digest()==raw[-20:],'native index header/checksum')
    version,count=struct.unpack('>II',raw[4:12]);need(version==2,'native index version2 only')
    end=len(raw)-20;pos=12;entries=[]
    for _ in range(count):
        start=pos;need(pos+62<=end,'complete native record header');flags=struct.unpack('>H',raw[pos+60:pos+62])[0]
        need(flags&0xf000==0,'native stage0/no extended/assume-valid flags')
        stop=raw.find(b'\0',pos+62,end);need(stop>=0,'native path terminator');name=raw[pos+62:stop]
        need(name and flags&0xfff==min(len(name),0xfff),'literal native path length')
        pos=start+((stop-start+1+7)//8)*8;need(pos<=end and not any(raw[stop:pos]),'native zero padding')
        mode=struct.unpack('>I',raw[start+24:start+28])[0];need(mode in (0o100644,0o100755,0o120000,0o160000),'native supported mode')
        entries.append((name,raw[start:pos],mode,raw[start+40:start+60].hex()))
    names=[x[0] for x in entries];need(names==sorted(set(names)),'native complete unique byte ordering')
    extensions=[]
    while pos<end:
        need(pos+8<=end,'complete extension header');kind=raw[pos:pos+4];size=struct.unpack('>I',raw[pos+4:pos+8])[0]
        need(kind==b'TREE' and not extensions and pos+8+size<=end,'only one known optional TREE extension')
        extensions.append((kind.decode(),size,sha(raw[pos+8:pos+8+size])));pos+=8+size
    need(pos==end,'exact native index extent')
    protected=[(n,b) for n,b,_,_ in entries if n not in targets]
    fingerprint=sha(b'\0'.join(n+b'\t'+b.hex().encode() for n,b in protected)+b'\0')
    return {'version':version,'count':count,'entries':entries,'protected':protected,'fingerprint':fingerprint,'extensions':extensions}

def splice(raw,oids):
    """Replace only ten eligible records. No Git command, stat refresh or rebuild."""
    targets={p.encode() for p in oids};old=parse_index(raw,targets)
    need(sha(raw)==INDEX and old['count']==58563 and len(old['protected'])==58561 and old['fingerprint']==PROTECTED,'actual held original raw index contract')
    need(len(targets)==10 and sum(n in targets for n,_,_,_ in old['entries'])==2,'eight new/two existing native records')
    records={n:b for n,b,_,_ in old['entries'] if n not in targets}
    for p,oid in oids.items():
        name=p.encode();need(len(oid)==40 and bytes.fromhex(oid).hex()==oid,'exact lowercase blob OID')
        record=struct.pack('>10I',0,0,0,0,0,0,0o100644,0,0,0)+bytes.fromhex(oid)+struct.pack('>H',min(len(name),0xfff))+name+b'\0'
        records[name]=record+b'\0'*((-len(record))%8)
    # TREE caches the obsolete path/blob graph; omit precisely this optional cache.
    body=b'DIRC'+struct.pack('>II',old['version'],len(records))+b''.join(records[n] for n in sorted(records))
    result=body+hashlib.sha1(body).digest();new=parse_index(result,targets)
    need(new['count']==58571 and new['protected']==old['protected'] and new['fingerprint']==PROTECTED and not new['extensions'],'all58561 protected records byte-identical; only TREE invalidated')
    actual={n.decode():(mode,oid) for n,_,mode,oid in new['entries'] if n in targets}
    need(actual=={p:(0o100644,oid) for p,oid in oids.items()},'all ten exact replacement records')
    return result

def preparation_seal():
    sb=read(N/'FINAL_SEAL.json');s=json.loads(sb);mb=pinned(N/'OWNED_MANIFEST.json',s['manifest']);m=json.loads(mb)
    need(extent(N)==(sorted([*m['files'],*TERMINALS]),m['directories']),'finite preparation namespace; only two exact root terminals')
    for name,d in m['files'].items():pinned(N/name,d)
    need(s['production_installation_authorized'] is False and s['publication_authorized'] is False,'preparation is not production authority')
    return sha(sb)

def authority(a,expected,prep,contract):
    need(a.get('schema')=='root-supported-cycle-focal-install-v1' and a.get('authority')=='root' and a.get('template_not_root_receipt') is False,'actual root installation receipt, not a template')
    need(a.get('production_installation_authorized') is True and a.get('current_mechanism_fully_adopted') is True and a.get('independent_mechanism_audit_adopted') is True,'future distinct root mechanism/audit/installation authority')
    need(a.get('root_stage_adoption_SHA256')==ROOT and a.get('preparation_seal_SHA256')==prep and a.get('runtime_contract_SHA256')==contract,'whole stage/preparation/runtime bindings')
    need(a.get('parent')==BASE and a.get('raw_index_SHA256')==INDEX and a.get('protected_raw_SHA256')==PROTECTED and a.get('runtime_root')==str(RUNTIME),'fixed actual baseline/native index/runtime')
    need(a.get('gitpaths')==sorted(expected) and a.get('expected_blob_OIDs')==expected,'exact ten candidate blob bindings')
    audit=a.get('independent_mechanism_audit_SHA256');need(isinstance(audit,str) and len(audit)==64 and bytes.fromhex(audit).hex()==audit,'actual separately adopted audit pin')

def runtime(root,contract,prep,expected):
    """Pure durable-state closure. Does NOT verify current website/refs/remote."""
    stateb=read(root/'STATE.json');s=json.loads(stateb);phase=s['phase'];need(phase in contract['phases'],'finite durable phase')
    names=contract['phases'][phase]['files'];need(extent(root)==(sorted([*names,'STATE.json']),[]),'exact runtime ordinary files and zero directories')
    need(s['preparation_seal_SHA256']==prep and s['runtime_contract_SHA256']==sha(encoded(contract)) and set(s['files'])==set(names),'state/preparation/contract/exact names')
    buffers={n:pinned(root/n,d) for n,d in s['files'].items()}
    auth=json.loads(buffers['ROOT_AUTHORITY.json']);authority(auth,expected,prep,s['runtime_contract_SHA256'])
    need(s['root_authority_SHA256']==sha(buffers['ROOT_AUTHORITY.json']),'held root authority binding')
    pre=json.loads(buffers['PRE_INSTALL.json']);need(pre['parent']==BASE and pre['index_SHA256']==INDEX and pre['gitpaths']==sorted(expected),'pre-install exact baseline')
    need(isinstance(json.loads(buffers['GIT_LOG.json']),list),'whole actual command log array')
    if phase!='INSTALL_STARTED':
        p=json.loads(buffers['PENDING_COMMIT.json']);need(p['parent']==BASE and p['gitpaths']==sorted(expected) and p['blob_OIDs']==expected and p['protected_raw_SHA256']==PROTECTED and p['root_authority_SHA256']==s['root_authority_SHA256'],'pending exact parent/paths/blob/protected/authority bindings')
        need(p['commit_index_SHA256']==sha(buffers['commit.index']) and p['approved_index_SHA256']==sha(buffers['shared-index.approved']),'actual temp and approved raw buffer bindings')
        approved=parse_index(buffers['shared-index.approved'],{x.encode() for x in expected})
        need(approved['fingerprint']==PROTECTED and approved['count']==58571,'approved native raw index preservation')
        need({n.decode():(m,oid) for n,_,m,oid in approved['entries'] if n.decode() in expected}=={n:(0o100644,oid) for n,oid in expected.items()},'approved exact ten records')
        need(all(len(p[k])==40 and bytes.fromhex(p[k]).hex()==p[k] for k in ('commit','tree')),'pending immutable object identities')
    if phase=='PUBLISHED':
        approval=json.loads(buffers['ROOT_COMMIT_APPROVAL.json']);commit_authority(approval,p,sha(buffers['PENDING_COMMIT.json']),sha(buffers['ROOT_AUTHORITY.json']),prep)
        pub=json.loads(buffers['PUBLICATION.json']);need(pub['commit']==p['commit'] and pub['tree']==p['tree'] and pub['index_SHA256']==p['approved_index_SHA256'] and pub['protected_raw_SHA256']==PROTECTED and pub['remote_advertised_master']==p['commit'],'whole final object/index/remote receipt binding')
        before=json.loads(buffers['PRE_PUBLICATION.json']);need(before['parent']==BASE and before['commit']==p['commit'] and before['index_SHA256']==INDEX,'pre-publication old/new binding')
        need(s['root_commit_approval_SHA256']==sha(buffers['ROOT_COMMIT_APPROVAL.json']),'commit approval whole bytes binding')
    return {'phase':phase,'files':len(names)+1,'live_state_reverified':False}

def commit_authority(a,p,pending_sha,install_sha,prep):
    need(a.get('schema')=='root-supported-cycle-focal-commit-v1' and a.get('authority')=='root' and a.get('template_not_root_receipt') is False and a.get('publication_authorized') is True,'separate actual root commit approval')
    need(a.get('preparation_seal_SHA256')==prep and a.get('root_install_authority_SHA256')==install_sha and a.get('pending_commit_receipt_SHA256')==pending_sha,'whole authority/pending receipt bindings')
    for k in ('parent','commit','tree','gitpaths','approved_index_SHA256','protected_raw_SHA256'):need(a.get(k)==p[k],'exact approved '+k)

def main():
    need(not sys.argv[1:],'default pure custody only; runtime is an explicit future caller interface')
    o=inputs();oids=oracle(o);raw=read(Path(o['raw_index_reference']));newraw=splice(raw,oids)
    go=json.loads(read(N/'READONLY_GO_REFERENCE.json'));gb=pinned(Path(go['path']),go);need(sha(gb)=='9e7a4a9274d45fe9699fdb9720f3c7b9991d4b704aac44b2de77c97444fae26a','actual root reviewed read-only capture GO')
    code=json.loads(read(N/'CURRENT_CODE_PINS.json'))
    for name,d in code.items():pinned(N/name,d)
    need(json.loads(gb)['capture_helper_SHA256']==code['capture_readonly.py']['SHA256'],'root read exact current capture body')
    template=json.loads(read(N/'ROOT_INSTALL_AUTHORITY_TEMPLATE.json'));need(template['production_installation_authorized'] is False and template['current_mechanism_fully_adopted'] is False and template['template_not_root_receipt'] is True,'current root install template disabled')
    commit=json.loads(read(N/'ROOT_COMMIT_APPROVAL_TEMPLATE.json'));need(commit['publication_authorized'] is False and commit['template_not_root_receipt'] is True,'current commit template disabled')
    contract=json.loads(read(N/'RUNTIME_CONTRACT.json'));need(encoded(contract)==read(N/'RUNTIME_CONTRACT.json') and contract['runtime_root']==str(RUNTIME) and all(v['directories']==[] for v in contract['phases'].values()),'canonical finite external runtime contract')
    for phase in ('PRE','POST'):
        g=json.loads(read(N/(phase+'_GUARD.json')));need(g['status']=='PASS_FRESH_EXACT10_READONLY_DRIFT_FENCE' and g['Git']['index_SHA256']==INDEX and g['baseline_counts']==[623,94,95] and g['production_mutation'] is False,'actual reviewed '+phase+' baseline')
        for r in g['actual_Git_receipts']:
            need(r['actual_exit']==0 and r['timed_out'] is False,'literal successful read-only Git receipt')
            for stream in ('stdout','stderr'):pinned(Path(r[stream]['path']),r[stream])
    sealed=(N/'FINAL_SEAL.json').exists()
    if sealed:preparation_seal()
    print(json.dumps({'status':'PASS_PURE_EXACT10_PREPARATION_CUSTODY','sealed':sealed,'checks':CHECKS,'original_files':len(o['frozen_original_files']),'original_namespaces':len(o['closed_original_namespaces']),'candidate_buffers':len(oids),'protected_raw_records':58561,'approved_raw_index_SHA256':sha(newraw),'originals_read_by_reference':True,'runtime_read':False,'production_executed':False},sort_keys=True))

if __name__=='__main__':main()
