#!/usr/bin/env python3
"""Verify exact publication membership, immutable archives, replay, and optional queue bytes."""
from pathlib import Path,PurePosixPath
import argparse,hashlib,json,os,stat,subprocess,sys,zipfile

def require(ok,message):
    if not ok:raise RuntimeError(message)

def identity(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}

def safe(name):
    p=PurePosixPath(name)
    require(bool(name) and not p.is_absolute() and '..' not in p.parts and str(p)==name,'Unsafe path')
    return name

def inventory(root):return {p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file() or p.is_symlink()}

def run(script,optimized=False):
    args=[sys.executable,'-I','-B']+(['-O'] if optimized else [])+[str(script)]
    result=subprocess.run(args,cwd=script.parent,check=True,capture_output=True,text=True)
    return json.loads(result.stdout)

def verify(root):
    require(root.is_dir(),'Missing packet root')
    require(not any(p.is_symlink() for p in root.rglob('*')),'Symlink in payload')
    m=json.loads((root/'PUBLICATION_MANIFEST.json').read_text());files=m['files']
    names=[safe(f['path']) for f in files]
    require(len(names)==len(set(names)),'Duplicate manifest path')
    require(inventory(root)==set(names)|{'PUBLICATION_MANIFEST.json'},'Recursive inventory mismatch')
    for f in files:require(identity((root/f['path']).read_bytes())=={k:f[k] for k in ('bytes','sha256')},'File bytes/hash mismatch: '+f['path'])
    provenance=json.loads((root/'PUBLICATION_PROVENANCE.json').read_text());count=0
    for a in provenance['archives']:
        path=root/safe(a['path']);dest=root/safe(a['extracted_directory'])
        require(identity(path.read_bytes())=={k:a[k] for k in ('bytes','sha256')},'Archive identity mismatch')
        with zipfile.ZipFile(path) as z:
            names=z.namelist()
            require(len(names)==len(set(names))==a['member_count'],'Archive member count mismatch')
            require(z.testzip() is None,'Archive CRC mismatch')
            require(set(names)==inventory(dest),'Archive/extracted inventory mismatch')
            for info in z.infolist():
                require(not info.is_dir() and not stat.S_ISLNK(info.external_attr>>16),'Unsafe ZIP member')
                name=safe(info.filename)
                require(z.read(name)==(dest/name).read_bytes(),'Archive member bytes mismatch')
            count+=len(names)
    names=inventory(root/'author')
    require(names==inventory(root/'audit/author_freeze'),'Frozen author inventory mismatch')
    for n in names:require((root/'author'/n).read_bytes()==(root/'audit/author_freeze'/n).read_bytes(),'Frozen author copy changed')
    return {'status':'PASS','payload_files':len(files)+1,'archive_members_byte_verified':count,'author_snapshot_identical':True}

def replay(root,optimized=False):
    expected_author=json.loads((root/'author/CHECK_RESULTS.json').read_text())
    expected_audit=json.loads((root/'audit/INDEPENDENT_CHECK_RESULTS.json').read_text())
    require(run(root/'author/checks.py',optimized)==expected_author,'Author exact results mismatch')
    require(run(root/'audit/independent_checks.py',optimized)==expected_audit,'Independent exact results mismatch')
    author=run(root/'author/verify_packet.py',optimized)
    audit=run(root/'audit/verify_audit.py',optimized)
    require(author['packet']=='PASS' and author['finite_checks']==22185,'Author replay failure')
    require(audit['audit_packet']=='PASS' and audit['author_assertions']==22185 and audit['independent_assertions']==40249,'Audit replay failure')
    return {'status':'PASS','author_assertions':22185,'independent_assertions':40249,'symbolic_polynomial_identities':5,'exact_result_json_matches':True,'optimized_python':optimized,'scope':'Finite algebraic controls; not a proof of the unrestricted analytic PDE conjecture.'}

def verify_queue(root,base_path,updated_path):
    d=json.loads((root/'QUEUE_DELTA.json').read_text());base=base_path.read_bytes();updated=updated_path.read_bytes()
    require(identity(base)==d['base'] and identity(updated)==d['updated'],'Queue identity mismatch')
    x=base.splitlines(keepends=True);y=updated.splitlines(keepends=True)
    require(len(x)==len(y),'Queue line count mismatch')
    hits=[i for i,l in enumerate(x) if b'| 30005995 / OWR-14298587-010 |' in l]
    require(len(hits)==1,'Queue target not unique');i=hits[0]
    require(i+1==d['row_line_1_based'],'Queue position mismatch')
    require(x[:i]==y[:i] and x[i+1:]==y[i+1:],'Unrelated queue bytes changed')
    before=x[i].split(b'|');after=y[i].split(b'|')
    require(len(before)==len(after),'Queue cell count mismatch')
    require([j for j in range(len(before)) if before[j]!=after[j]]==[8,9],'Unexpected changed queue cells')
    require(before[1].strip()==after[1].strip()==b'803','Queue rank mismatch')
    require(before[8]==b' queued ' and before[9]==b' 0/5 ' and after[8]==b' unsolved ' and after[9]==b' 5/5 ','Queue disposition mismatch')
    return {'status':'PASS','changed_cells':['Status','Turns'],'all_other_bytes_preserved':True,'stale_header_preserved':True,'findings_unchanged':True}

def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--replay',action='store_true');parser.add_argument('--optimized-replay',action='store_true');parser.add_argument('--queue-base',type=Path);parser.add_argument('--queue-updated',type=Path);args=parser.parse_args()
    require(bool(args.queue_base)==bool(args.queue_updated),'Both queue files are required')
    root=Path(__file__).resolve().parent;result=verify(root)
    result['queue']=verify_queue(root,args.queue_base,args.queue_updated) if args.queue_base else {'status':'NOT_RUN','reason':'Optional queue snapshots not supplied'}
    result['normal_replay']=replay(root) if args.replay else {'status':'NOT_RUN'}
    result['optimized_replay']=replay(root,True) if args.optimized_replay else {'status':'NOT_RUN'}
    print(json.dumps(result,indent=2,sort_keys=True))

if __name__=='__main__':main()
