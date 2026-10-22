#!/usr/bin/env python3
"""Authenticate a frozen local-obstruction packet before isolated replay."""
import argparse,hashlib,io,json,os,shutil,stat,subprocess,sys,tempfile,zipfile
from pathlib import Path,PurePosixPath

MANIFEST_SHA256='f51701ffee330f80efab5ffdc48892d7f2b3201ac0c8a2e4bc41d29bb0486808'
PINS={'EMPTY_MONOCHROMATIC_3081_AUTHOR_SAFE_FREEZE.zip': (15603, '0edf7b3e9c4b7cfc72c0f194cc9a62da4ecf6d946b63e7d1b74e6c4afda41fd1'), 'EMPTY_MONOCHROMATIC_3081_AUTHOR_EXTERNAL_MANIFEST.json': (1917, '5d974f4db3baa61297b08dfb753550956951b6c983b5cefe937ec6cc8efec885'), 'EMPTY_MONOCHROMATIC_3081_INDEPENDENT_AUDIT_SAFE.zip': (40991, '415841917e90f9bfd6e3c9bee406595ccdd68a1a25853ab99b7b5b25a4e0b821'), 'EMPTY_MONOCHROMATIC_3081_INDEPENDENT_AUDIT_EXTERNAL_MANIFEST.json': (2270, '3db65bb07ec78d3059685f53289364a86a185960d98f7c19b70c7039bb877eb2'), 'EMPTY_MONOCHROMATIC_3081_INDEPENDENT_AUDIT_RECEIPT.json': (7066, '46d659f1e01b3d5a34b6b849445225d4e108a357f2674f109a15396d694b05d3')}
AZ='EMPTY_MONOCHROMATIC_3081_AUTHOR_SAFE_FREEZE.zip'
AM='EMPTY_MONOCHROMATIC_3081_AUTHOR_EXTERNAL_MANIFEST.json'
IZ='EMPTY_MONOCHROMATIC_3081_INDEPENDENT_AUDIT_SAFE.zip'
IM='EMPTY_MONOCHROMATIC_3081_INDEPENDENT_AUDIT_EXTERNAL_MANIFEST.json'

def need(ok,message):
    if not ok:raise ValueError(message)
def sha(b):return hashlib.sha256(b).hexdigest()
def dig(b):return {'bytes':len(b),'sha256':sha(b)}
def unique(pairs):
    out={}
    for k,v in pairs:
        need(k not in out,'duplicate JSON key');out[k]=v
    return out
def parse(b):return json.loads(b,object_pairs_hook=unique)
def read(p):
    need(stat.S_ISREG(p.lstat().st_mode),'nonregular file');return p.read_bytes()
def authenticate(root):
    need(stat.S_ISDIR(root.lstat().st_mode),'nonordinary root')
    raw=read(root/'PUBLICATION_MANIFEST.json');need(sha(raw)==MANIFEST_SHA256,'publication manifest pin mismatch')
    m=parse(raw)
    need((m['problem_id'],m['problem_number'],m['rank'],m['status'],m['substantive_approaches'],m['approach_ceiling'],m['repair_required'])==(3081,'OPG-2435',926,'unsolved',2,5,False),'publication scope')
    expected=set(m['files'])|{'PUBLICATION_MANIFEST.json','verify_publication.py'};dirs=set()
    for name in expected:
        p=PurePosixPath(name);need(not p.is_absolute() and '..' not in p.parts and '\\' not in name and str(p)==name,'unsafe path')
        dirs.update(str(x) for x in p.parents if str(x)!='.')
    found=set()
    for base,subdirs,names in os.walk(root,followlinks=False):
        for name in subdirs:
            p=Path(base)/name;need(stat.S_ISDIR(p.lstat().st_mode) and p.relative_to(root).as_posix() in dirs,'unexpected/nonordinary directory')
        for name in names:
            p=Path(base)/name;need(stat.S_ISREG(p.lstat().st_mode),'nonregular member');found.add(p.relative_to(root).as_posix())
    need(found==expected,'exact file allowlist mismatch')
    buffers={'PUBLICATION_MANIFEST.json':raw,'verify_publication.py':read(root/'verify_publication.py')}
    need(buffers['verify_publication.py']==read(Path(__file__)),'wrapper copy mismatch')
    for name,pin in m['files'].items():
        b=read(root/name);need(dig(b)==pin,'file pin mismatch: '+name);buffers[name]=b
    for name,pin in PINS.items():
        b=buffers['releases/'+name];need((len(b),sha(b))==pin,'frozen release pin mismatch')
    return buffers
def archives(buffers):
    out=[]
    for label,az,am,count in [('original',AZ,AM,10),('audit',IZ,IM,12)]:
        raw=buffers['releases/'+az];m=parse(buffers['releases/'+am]);need(m['archive']==dict(name=az,**dig(raw)),'archive metadata')
        rows=m['members'];names=[r['name'] for r in rows];need(len(names)==len(set(names))==count,'external membership')
        with zipfile.ZipFile(io.BytesIO(raw)) as z:
            need(len(z.namelist())==len(set(z.namelist()))==count and set(z.namelist())==set(names),'archive membership')
            for row in rows:
                name=row['name'];need(name not in ('','.','..') and '/' not in name and '\\' not in name,'archive path')
                info=z.getinfo(name);need(stat.S_ISREG(info.external_attr>>16) and not info.flag_bits&1,'archive mode')
                b=z.read(info);need(dig(b)=={k:row[k] for k in ('bytes','sha256')} and b==buffers[label+'/'+name],'archive or expanded member mismatch')
            internal=parse(z.read('MANIFEST.json'))['files'];need(len(internal)==count-1 and len({r['name'] for r in internal})==count-1,'internal inventory')
            need({r['name'] for r in internal}|{'MANIFEST.json'}==set(names),'internal member set')
            for row in internal:need(dig(z.read(row['name']))=={k:row[k] for k in ('bytes','sha256')},'internal member mismatch')
        out.append({'label':label,'members':count,'exact_match':True})
    for name in (AZ,AM):need(buffers['audit/'+name]==buffers['releases/'+name],'nested original mismatch')
    a=parse(buffers['audit/ACCEPTANCE.json'])
    need((a['problem_id'],a['problem_number'],a['rank'],a['status'],a['substantive_approaches'],a['approach_ceiling'])==(3081,'OPG-2435',926,'ACCEPT_UNCHANGED_AUTHOR_PACKET',2,5),'acceptance identity')
    need(a['mathematical_outcome']=='Unsolved: local proof-shortcut obstructions only','acceptance scope')
    for key in ('new_asymptotic_bound','asymptotic_counterexample','repair_required'):need(a[key] is False,'acceptance overclaim')
    need((a['actual_replay_cases'],a['expected_successes'],a['expected_failures'])==(38,6,32),'acceptance counts')
    for field,name in [('accepted_author_archive',AZ),('accepted_author_external_manifest',AM)]:need(a[field]==dict(name=name,bytes=PINS[name][0],sha256=PINS[name][1]),'acceptance exact pin')
    return out
def run(script,args,optimized,cwd):
    cmd=[sys.executable,'-I','-B']+(['-O'] if optimized else [])+[str(script),*map(str,args)]
    p=subprocess.run(cmd,cwd=cwd,capture_output=True,text=True,timeout=240,env={'PATH':os.environ.get('PATH','/usr/bin:/bin'),'HOME':str(cwd/'unrelated home'),'PYTHONPATH':str(cwd/'hostile pythonpath')})
    need(p.returncode==0,'replay failed: '+p.stderr);out=parse(p.stdout);need(out['status']=='PASS','replay nonPASS')
    return out,sha(p.stdout.encode())
def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--root',type=Path,default=Path(__file__).absolute().parent);p.add_argument('--integrity-only',action='store_true');p.add_argument('--corpus-dir',type=Path);p.add_argument('--source-dir',type=Path);a=p.parse_args()
    need(bool(a.corpus_dir)==bool(a.source_dir),'supply both full-input directories');need(not(a.integrity_only and a.corpus_dir),'integrity-only cannot claim input replay')
    buffers=authenticate(a.root.absolute());ar=archives(buffers)
    result={'status':'PASS','problem_id':3081,'mathematical_status':'unsolved','substantive_approaches':2,'approach_ceiling':5,'new_asymptotic_result':False,'formal_proof_check':False,'files_authenticated':len(buffers),'archives':ar,'full_input_replay':bool(a.corpus_dir),'mode':'integrity-only' if a.integrity_only else 'replay','replays':[]}
    with tempfile.TemporaryDirectory(prefix='triangles publication relocated α ') as tmp:
        work=Path(tmp);packet=work/'authenticated packet'
        for name,b in buffers.items():
            dest=packet/name;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(b)
        args=[]
        if a.corpus_dir:
            cd=work/'private corpus inputs';sd=work/'private source inputs';cd.mkdir();sd.mkdir()
            for name in ('catalog.json','problems.json','research_results.json'):shutil.copyfile(a.corpus_dir/name,cd/name)
            for row in parse(buffers['original/SOURCE_VERIFICATION.json'])['retrievals']:
                if row.get('status')==200:shutil.copyfile(a.source_dir/row['filename'],sd/row['filename'])
            args=['--corpus-dir',cd,'--source-dir',sd]
        if not a.integrity_only:
            hashes=[]
            for optimized in (False,True):
                independent,ih=run(packet/'audit/independent_check.py',args,optimized,work)
                need(independent['geometry']['E0']==0 and independent['geometry']['E1']==8 and len(independent['family'])==30,'geometry replay result')
                need(independent['corpora']['requested']==bool(args) and independent['sources']['requested']==bool(args),'input replay request')
                if args:need(independent==parse(buffers['audit/INDEPENDENT_NORMAL.json']),'frozen full independent output mismatch')
                replay,rh=run(packet/'audit/replay_author.py',args,optimized,work)
                expected=(38,6,32) if args else (32,4,28)
                need((replay['case_count'],sum(x['expected_pass'] for x in replay['cases']),sum(not x['expected_pass'] for x in replay['cases']))==expected,'author replay case counts')
                need(replay['private_corpora_relocated']==bool(args) and replay['private_sources_relocated']==bool(args),'relocated input claims')
                result['replays'].append({'optimized':optimized,'isolated':True,'relocated':True,'independent_stdout_sha256':ih,'author_replay_stdout_sha256':rh,'case_count':expected[0],'expected_successes':expected[1],'expected_failures':expected[2],'E0':0,'E1':8,'family_k_max':30})
                hashes.append(ih)
            need(hashes[0]==hashes[1],'independent normal/optimized output mismatch')
    print(json.dumps(result,indent=2,sort_keys=True))
if __name__=='__main__':
    try:main()
    except Exception as e:
        print('FAIL: '+str(e),file=sys.stderr);sys.exit(1)
