"""Authenticate this flat authored review using externally supplied manifest and checker pins."""
from pathlib import Path,PurePosixPath
import argparse,hashlib,json,os,stat,subprocess,sys
sys.dont_write_bytecode=True

def need(ok,message):
    if not ok:raise ValueError(message)

def sha(raw):return hashlib.sha256(raw).hexdigest()

def identity(raw):return {'bytes':len(raw),'sha256':sha(raw)}

def unique(pairs):
    out={}
    for k,v in pairs:
        need(k not in out,'Duplicate JSON key');out[k]=v
    return out

def parse(raw):
    return json.loads(raw,object_pairs_hook=unique,parse_constant=lambda x:(_ for _ in ()).throw(ValueError('Nonfinite JSON')))

def pin(value):return isinstance(value,str)and len(value)==64 and all(x in'0123456789abcdef'for x in value)

def regular(path):
    need(stat.S_ISREG(path.lstat().st_mode),'Nonregular input')
    fd=os.open(path,os.O_RDONLY|os.O_NOFOLLOW|os.O_NONBLOCK)
    with os.fdopen(fd,'rb')as f:
        need(stat.S_ISREG(os.fstat(f.fileno()).st_mode),'Nonregular descriptor');return f.read()

def inventory(root):
    need(root.is_dir()and not root.is_symlink(),'Packet directory required')
    result={}
    for p in root.iterdir():
        need(p.name not in result and not p.is_symlink(),'Duplicate or symlink member')
        result[p.name]=regular(p)
    return result

def relative(root,name):
    need(isinstance(name,str)and name and'\\'not in name and not PurePosixPath(name).is_absolute()and all(x not in('','.','..')for x in name.split('/')),'Unsafe relative input')
    p=root
    need(root.is_dir()and not root.is_symlink(),'External root directory required')
    for part in name.split('/'):
        p=p/part;need(not p.is_symlink(),'External symlink')
    return p

def verify(args):
    need(pin(args.expected_manifest_sha256)and pin(args.expected_checker_sha256),'External pins required')
    root=args.packet.absolute()
    need(Path(__file__).absolute()==root/'custody_check.py','Run the checker from the selected packet')
    need(sha(regular(root/'custody_check.py'))==args.expected_checker_sha256,'External checker pin differs')
    files=inventory(root);raw=files['MANIFEST.json']
    need(sha(raw)==args.expected_manifest_sha256,'External manifest pin differs')
    manifest=parse(raw);need(manifest['schema']=='pr788-whole-review02/v1','Manifest schema')
    expected={}
    for row in manifest['files']:
        name=row['path'];need(isinstance(name,str)and name and'/'not in name and'\\'not in name and name not in('.','..','MANIFEST.json')and name not in expected,'Invalid/repeated manifest member')
        need(set(row)=={'path','bytes','sha256'}and type(row['bytes'])is int and row['bytes']>=0 and pin(row['sha256']),'Invalid member identity')
        expected[name]={k:row[k]for k in('bytes','sha256')}
    need(set(files)==set(expected)|{'MANIFEST.json'},'Closed packet inventory differs')
    for n,r in expected.items():need(identity(files[n])==r,'Packet bytes differ: '+n)
    bound=0;external=0;replays=[]
    if args.preprint_root:
        b=parse(files['INPUT_BINDINGS.json']);p=args.preprint_root.absolute()
        for row in b['preprint_inputs']:
            need(identity(regular(relative(p,row['path'])))=={k:row[k]for k in('bytes','sha256')},'Bound preprint input differs: '+row['path']);bound+=1
        actual=set();directories=set()
        for item in(p/'source').rglob('*'):
            need(not item.is_symlink(),'External source symlink')
            n=item.relative_to(p/'source').as_posix()
            if item.is_dir():directories.add(n)
            else:actual.add(n)
        listed={x['path'][7:]for x in b['preprint_inputs']if x['path'].startswith('source/')}
        need(actual==listed,'External source closure differs')
        need(directories=={q.as_posix()for n in actual for q in Path(n).parents if q.as_posix()!='.'},'External source empty directory')
    if args.primary_root:
        ledger=parse(files['SOURCE_READ_LEDGER.json']);p=args.primary_root.absolute()
        for row in ledger['local_custody']:
            need(identity(regular(relative(p,row['path'])))=={k:row[k]for k in('bytes','sha256')},'Primary evidence differs: '+row['path']);external+=1
    if args.replay:
        for opt in(False,True):
            r=subprocess.run([sys.executable,'-I','-B']+(['-O']if opt else[])+[str(root/'independent_diagnostics.py')],cwd='/',capture_output=True,text=True,timeout=60)
            need(r.returncode==0 and not r.stderr and parse(r.stdout)==parse(files['DIAGNOSTIC_RESULTS.json']),'Diagnostic replay differs')
            replays.append({'optimized':opt,'result':'PASS','stdout_sha256':sha(r.stdout.encode())})
    need(inventory(root)==files,'Packet changed during check')
    return {'result':'PASS','manifest_sha256':args.expected_manifest_sha256,'checker_sha256':args.expected_checker_sha256,'authored_files_including_manifest':len(files),'preprint_inputs_rehashed':bound,'primary_evidence_files_rehashed':external,'finite_replays':replays,'scope':'Custody and exact finite diagnostics only; no formal topology, novel-result or priority certification. Optional primary custody covers only the listed fresh evidence, never the lost historical 76-file bank.'}

def main():
    a=argparse.ArgumentParser(description=__doc__);a.add_argument('--packet',type=Path,required=True);a.add_argument('--expected-manifest-sha256',required=True);a.add_argument('--expected-checker-sha256',required=True);a.add_argument('--preprint-root',type=Path);a.add_argument('--primary-root',type=Path);a.add_argument('--replay',action='store_true');args=a.parse_args()
    try:r=verify(args)
    except Exception as e:print(json.dumps({'result':'FAIL','error':str(e)},sort_keys=True));return 1
    print(json.dumps(r,indent=2,sort_keys=True));return 0

if __name__=='__main__':sys.exit(main())
