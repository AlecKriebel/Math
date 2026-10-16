#!/usr/bin/env python3
"""Read-only exact-plan/actual-commit verifier; all mutations are confined to own receipts."""
from pathlib import Path
import base64,datetime,gzip,hashlib,json,os,stat,subprocess,sys
T=Path(__file__).resolve().parents[1]
O=Path(__file__).resolve().parent
S=T/'merge-scope-review-scratch'
P=T/'preprint'
def need(ok,message):
    if not ok:raise ValueError(message)
def digest(body):return hashlib.sha256(body).hexdigest()
def git_oid(kind,body):return hashlib.sha1(kind.encode()+b' '+str(len(body)).encode()+b'\0'+body).hexdigest()
def api(path):
    need(not path.startswith('/') and all(part != '..' for part in path.split('/')),'safe API path')
    r=subprocess.run(['gh','api','repos/AlecKriebel/Math/'+path],capture_output=True,check=True)
    return json.loads(r.stdout)
def write_json(path,value):path.write_text(json.dumps(value,indent=2,sort_keys=True)+'\n')
def load_initial():
    d=json.loads((O/'INITIAL_SCOPE_POSITION.json').read_text())
    need(d['original_reviewed_candidate_head']=='34f21454986a28ca49f24999be3a0fd1b42755f8','frozen old head')
    return d
def check_sources(initial):
    sourcepath=T/'intake/ROOT_SOURCE_IDENTITY.json'
    need(digest(sourcepath.read_bytes())==initial['original_source_identity_sha256'],'immutable source identity')
    source=json.loads(sourcepath.read_text())
    for r in initial['original_files']:
        f=T/'intake/original'/r['path'];st=f.lstat()
        need(stat.S_ISREG(st.st_mode),'original regular file '+r['path'])
        b=f.read_bytes()
        need(len(b)==r['bytes'] and digest(b)==r['sha256'] and git_oid('blob',b)==r['git_blob'],'original bytes '+r['path'])
    need(digest((P/'PACKAGE_INVENTORY.json').read_bytes())==initial['package_inventory_sha256'],'frozen inventory')
    for r in initial['six_frozen_files']:
        b=(P/r['path']).read_bytes()
        need(len(b)==r['bytes'] and digest(b)==r['sha256'],'frozen release '+r['path'])
    mp=P/'source/MANIFEST.json'
    need(digest(mp.read_bytes())==initial['source_manifest_sha256'],'frozen source manifest')
    manifest=json.loads(mp.read_text());wanted={r['path'] for r in manifest['files']}|{'MANIFEST.json'}
    actual={str(f.relative_to(P/'source')) for f in (P/'source').rglob('*') if f.is_file() or f.is_symlink()}
    need(actual==wanted and len(actual)==213,'exact closed source213')
    for r in manifest['files']:
        f=P/'source'/r['path'];st=f.lstat();need(stat.S_ISREG(st.st_mode),'source regular file')
        b=f.read_bytes();need(len(b)==r['bytes'] and digest(b)==r['sha256'],'source bytes '+r['path'])
    return {'original_files':41,'source_files_including_manifest':213,'frozen_release_files':6,'source_identity_sha256':initial['original_source_identity_sha256'],'source_manifest_sha256':initial['source_manifest_sha256']}
class Merkle:
    def __init__(self,phase):self.cache={};self.phase=phase;self.receipts=[]
    def read(self,kind,sha):
        path=S/(kind+'_'+sha+'.json.gz')
        if path.exists():data=json.loads(gzip.decompress(path.read_bytes()))
        else:
            data=api('git/'+kind+'s/'+sha);path.write_bytes(gzip.compress(json.dumps(data,sort_keys=True).encode(),mtime=0))
        self.receipts.append({'kind':kind,'sha':sha,'scratch_receipt':path.name,'compressed_bytes':path.stat().st_size})
        return data
    def tree(self,sha):
        if sha in self.cache:return self.cache[sha]
        data=self.read('tree',sha)
        need(data['sha']==sha and data.get('truncated') is False,'nontruncated exact tree '+sha)
        entries=data['tree']
        need(len(entries)==len({e['path'] for e in entries}),'unique tree names')
        need(all('/' not in e['path'] and '\0' not in e['path'] for e in entries),'flat raw tree')
        entries={e['path']:{k:e[k] for k in ('path','mode','type','sha')} for e in entries}
        need(self.hash_tree(entries)==sha,'independent Git tree hash '+sha)
        self.cache[sha]=entries
        return entries
    def hash_tree(self,entries):
        body=b''
        for e in sorted(entries.values(),key=lambda e:e['path'].encode()+(b'/' if e['type']=='tree' else b'')):
            body+=e['mode'].lstrip('0').encode()+b' '+e['path'].encode()+b'\0'+bytes.fromhex(e['sha'])
        return git_oid('tree',body)
    def blob(self,sha):
        d=self.read('blob',sha);need(d['sha']==sha and d['encoding']=='base64','blob schema')
        b=base64.b64decode(d['content']);need(len(b)==d['size'] and git_oid('blob',b)==sha,'independent Git blob hash')
        return b
    def leaves(self,sha,prefix):
        result={}
        for name,e in self.tree(sha).items():
            p=prefix+name
            if e['type']=='tree':result.update(self.leaves(e['sha'],p+'/'))
            else:result[p]=(e['mode'],e['type'],e['sha'])
        return result
    def diff(self,a,b,prefix=''):
        ta=self.tree(a);tb=self.tree(b);result={}
        for name in sorted(set(ta)|set(tb)):
            x,y=ta.get(name),tb.get(name)
            if x==y:continue
            p=prefix+name
            if x and y and x['type']==y['type']=='tree':result.update(self.diff(x['sha'],y['sha'],p+'/'))
            else:
                left=self.leaves(x['sha'],p+'/') if x and x['type']=='tree' else ({p:(x['mode'],x['type'],x['sha'])} if x else {})
                right=self.leaves(y['sha'],p+'/') if y and y['type']=='tree' else ({p:(y['mode'],y['type'],y['sha'])} if y else {})
                for f in set(left)|set(right):
                    if left.get(f)!=right.get(f):result[f]={'before':left.get(f),'after':right.get(f)}
        return result
    def apply(self,sha,updates,prefix=''):
        entries=dict(self.tree(sha)) if sha else {}
        for name,value in updates.items():
            previous=entries.get(name);path=prefix+name
            if isinstance(value,dict):
                need(previous is None or previous['type']=='tree','tree type collision '+path)
                child=self.apply(previous['sha'] if previous else None,value,path+'/')
                entries[name]={'path':name,'mode':'040000','type':'tree','sha':child}
            else:
                need(path=='unsolved_math_prioritization/QUEUE.md' or previous is None or (previous['mode'],previous['type'],previous['sha'])==value,'differing source collision '+path)
                entries[name]={'path':name,'mode':value[0],'type':value[1],'sha':value[2]}
        sha=self.hash_tree(entries);self.cache[sha]=entries
        return sha
def trie_for(updates):
    trie={}
    for path,value in updates.items():
        t=trie;parts=path.split('/')
        for part in parts[:-1]:t=t.setdefault(part,{})
        t[parts[-1]]=value
    return trie
# Parent supplies the actual sealed plan and phase-specific checks; no implicit execution.
if __name__=='__main__':
    print(json.dumps({'result':'UTILITY_ONLY','message':'Use explicit phase driver with parent-supplied exact plan SHA; no final verdict inferred.'}))
