#!/usr/bin/env python3
"""Closed-inventory offline replay; trust an independently retained external pin."""
import argparse,hashlib,io,json,pathlib,re,subprocess,sys,tempfile,zipfile

def need(ok,message):
    if not ok:raise RuntimeError(message)
def digest(b):return hashlib.sha256(b).hexdigest()
def pairs(items):
    d={}
    for k,v in items:
        need(k not in d,'duplicate JSON key');d[k]=v
    return d
def obj(raw):return json.loads(raw,object_pairs_hook=pairs)
def safe(name):
    return isinstance(name,str) and bool(name) and '\\' not in name and not name.startswith('/') and all(x not in ('','.','..') for x in name.split('/'))
def verify_inventory(files,raw,pin,extra=()):
    need(digest(raw)==pin,'manifest pin mismatch')
    m=obj(raw);need(isinstance(m,dict) and set(m)=={'schema','files',*extra} and type(m['schema']) is int and m['schema']==1,'bad manifest schema')
    table=m['files'];need(isinstance(table,dict) and bool(table),'bad inventory')
    need(set(files)==set(table)|{'MANIFEST.json'},'inventory mismatch')
    for name,entry in table.items():
        need(safe(name) and name!='MANIFEST.json','unsafe inventory name')
        need(isinstance(entry,dict) and set(entry)=={'bytes','sha256'},'bad entry')
        need(type(entry['bytes']) is int and entry['bytes']>=0,'bad byte count')
        need(isinstance(entry['sha256'],str) and re.fullmatch('[0-9a-f]{64}',entry['sha256']),'bad digest')
        need(len(files[name])==entry['bytes'] and digest(files[name])==entry['sha256'],'content mismatch: '+name)
    return m

def apply_exact_patch(originals,raw):
    lines=raw.decode().splitlines(keepends=True);i=0;outputs={}
    while i<len(lines):
        need(lines[i].startswith('--- a/'),'bad patch old header');name=lines[i][6:].strip();i+=1
        need(name in originals and name not in outputs,'unexpected patch target')
        need(lines[i]=='+++ b/'+name+'\n','bad patch new header');i+=1
        old=originals[name].decode().splitlines(keepends=True);out=[];pos=0
        while i<len(lines) and lines[i].startswith('@@ '):
            h=re.fullmatch(r'@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@\n',lines[i]);need(h is not None,'bad hunk')
            start=int(h[1])-1;oc=int(h[2] or '1');nc=int(h[4] or '1');i+=1
            need(start>=pos,'overlapping patch');out+=old[pos:start];pos=start;consumed=added=0
            need(len(out)==int(h[3])-1,'wrong new hunk position')
            while i<len(lines) and not lines[i].startswith(('@@ ','--- a/')):
                line=lines[i];i+=1;need(line[0] in ' +-','unsupported patch line')
                if line[0] in ' -':need(pos<len(old) and old[pos]==line[1:],'patch context mismatch');pos+=1;consumed+=1
                if line[0] in ' +':out.append(line[1:]);added+=1
            need(consumed==oc and added==nc,'patch hunk counts mismatch')
        out+=old[pos:];outputs[name]=''.join(out).encode()
    need(set(outputs)=={'PROOF.md','verify_packet.py'},'patch targets mismatch')
    return outputs

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--manifest-sha256',required=True);args=parser.parse_args()
    need(re.fullmatch('[0-9a-f]{64}',args.manifest_sha256),'bad external pin')
    root=pathlib.Path(__file__).resolve().parent
    entries=list(root.rglob('*'));need(all(not x.is_symlink() and (x.is_file() or x.is_dir()) for x in entries),'nonregular or symlink member')
    files={x.relative_to(root).as_posix():x.read_bytes() for x in entries if x.is_file()}
    need('MANIFEST.json' in files,'manifest absent')
    manifest=verify_inventory(files,files['MANIFEST.json'],args.manifest_sha256)
    dirs={x.relative_to(root).as_posix() for x in entries if x.is_dir()};expected_dirs={p.as_posix() for n in files for p in pathlib.PurePosixPath(n).parents if p.as_posix()!='.'}
    need(dirs==expected_dirs,'unlisted directory')
    author_pin='82b3c843525fb245d0fc1a7fb6eaa472ef8589439cd230275687b910a222f0c9'
    audit_pin='e8f2ee62b8996714ef7823903333813dc3a84e36f064bd00b486c621a831db6e'
    prov=obj(files['PROVENANCE.json']);accepted_pin=prov['accepted_manifest_sha256']
    subsets={}
    for folder,pin,extra in [('authored',author_pin,()),('independent_audit',audit_pin,('original_author_manifest_sha256',)),('accepted',accepted_pin,())]:
        sub={n[len(folder)+1:]:b for n,b in files.items() if n.startswith(folder+'/')};subsets[folder]=sub
        verify_inventory(sub,sub['MANIFEST.json'],pin,extra)
    need(obj(subsets['independent_audit']['MANIFEST.json'])['original_author_manifest_sha256']==author_pin,'audit original binding')
    for archive,pin,size,folder,prefix in [('AUTHOR_FREEZE.zip','64d3d4a8562911b3a2853fb3823ab8e52f1a795c663b3a97207f356aac4a2cd1',27913,'authored','author/'),('INDEPENDENT_AUDIT_FREEZE.zip','79e540e3e3420e261a2515553d276ba967c7076e217fe6541bb211d3ef4c8700',32780,'independent_audit','independent_audit/')]:
        b=files[archive];need(len(b)==size and digest(b)==pin,'archive original pin')
        with zipfile.ZipFile(io.BytesIO(b)) as z:
            names=z.namelist();need(len(names)==len(set(names)) and set(names)=={prefix+n for n in subsets[folder]},'archive inventory')
            for n in names:need(z.read(n)==subsets[folder][n[len(prefix):]],'archive member mismatch')
    patched=apply_exact_patch(subsets['authored'],files['independent_audit/CORRECTIONS.patch'])
    need(patched['PROOF.md']==files['accepted/PROOF.md']==files['independent_audit/PROOF.corrected.md'],'corrected proof mismatch')
    need(patched['verify_packet.py']==files['accepted/verify_packet.py']==files['independent_audit/verify_packet.hardened.py'],'hardened checker mismatch')
    delta=sorted(n for n in subsets['authored'] if subsets['authored'][n]!=subsets['accepted'][n]);need(delta==prov['accepted_changes_from_authored'],'accepted delta mismatch')
    with tempfile.TemporaryDirectory(prefix='quantum-knot-publication-') as td:
        temp=pathlib.Path(td)
        for n,b in files.items():
            dest=temp/n;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(b)
        def run(script,optimized=False,args=()):
            command=[sys.executable,'-I','-S','-B']+(['-O'] if optimized else [])+[str(temp/script),*args]
            r=subprocess.run(command,cwd=td,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=180)
            need(r.returncode==0,'replay failure: '+script+' '+r.stderr.decode(errors='replace'));return r.stdout
        for mode in (False,True):
            for folder,pin in [('authored',author_pin),('accepted',accepted_pin)]:
                run(folder+'/verify_packet.py',mode,('--manifest-sha256',pin))
            need(run('independent_audit/independent_checks.py',mode)==files['independent_audit/INDEPENDENT_RESULTS.json'],'independent diagnostics mismatch')
        need(run('authored/test_integrity.py')==files['authored/INTEGRITY_CONTROLS.json'],'original integrity result mismatch')
        need(run('independent_audit/test_hardened_schema.py')==files['independent_audit/HARDENED_SCHEMA_RESULTS.json'],'schema results mismatch')
    print(json.dumps({'status':'pass','author_checks':4043,'independent_checks':7421,'original_rejections':18,'hardened_schema_rejections':10,'exact_patch_applied':True,'immutable_archives':2,'files_verified':len(manifest['files']),'scope':'Integrity and finite diagnostic replay only; mathematical acceptance and limits are in the audit.'},sort_keys=True))
if __name__=='__main__':main()
