"""Optimization-safe, offline artifact/dependency verification; not a proof certificate."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import stat
import sys
import tempfile

ROOT=Path(__file__).resolve().parent
NAMES=frozenset(('ATTEMPT_REPORT.md','INDEPENDENT_REVIEW.md','SOURCE_VERIFICATION.json','SOURCE_MANIFEST.json','SOURCE_STATUS_GATE.md','SOURCE_METADATA.json','PROVENANCE.json','DEPENDENCY_AUDIT.json','README.md','verify_package.py','MANIFEST.json'))
BINDINGS={'ATTEMPT_REPORT.md':'a6d98f3033f8b7a39840ec4bc248a48b5bee7180e54607f9970336d1e023aa63','INDEPENDENT_REVIEW.md':'a82d483a606d595e3a197c738083f99cc80543a8a145051b6c2faf320f1b9fed'}
READ_EVENTS=[]
def require(ok,message):
    if not ok: raise RuntimeError(message)
def audit(event,args):
    if event.startswith('socket.'): raise RuntimeError('socket event denied')
    if event=='open': READ_EVENTS.append(str(args[0]))
def digest(data): return hashlib.sha256(data).hexdigest()
def inventory(root):
    require(stat.S_ISDIR(root.lstat().st_mode),'package root must be a real directory')
    actual=set()
    for p in root.iterdir():
        require(stat.S_ISREG(p.lstat().st_mode),'nonregular inventory entry: '+p.name)
        actual.add(p.name)
    require(actual==NAMES,'exact inventory mismatch')
def integrity(root=ROOT):
    inventory(root) # Deliberately before any content read, including the manifest.
    manifest=json.loads((root/'MANIFEST.json').read_text())
    require(set(manifest['files'])==NAMES-{'MANIFEST.json'},'manifest inventory mismatch')
    for name,entry in manifest['files'].items():
        data=(root/name).read_bytes()
        require({'bytes':len(data),'sha256':digest(data)}==entry,'hash mismatch: '+name)
    for name,expected in BINDINGS.items(): require(manifest['files'][name]['sha256']==expected,'review binding mismatch')
    source=json.loads((root/'SOURCE_MANIFEST.json').read_text())
    require(source['target_id']==11000162 and source['row']==1892 and source['attempts']==5,'source identity mismatch')
    require(source['disposition']=='PARTIAL_PROGRESS_NOT_SOLVED','source disposition mismatch')
    for entry in source['files']:
        require(manifest['files'][entry['name']]=={k:entry[k] for k in ('bytes','sha256')},'source manifest mismatch')
    prov=json.loads((root/'PROVENANCE.json').read_text())
    for name,entry in prov['inputs'].items():
        require(manifest['files'][name]=={k:entry[k] for k in ('bytes','sha256')},'provenance mismatch')
    verification=json.loads((root/'SOURCE_VERIFICATION.json').read_text())
    metadata=json.loads((root/'SOURCE_METADATA.json').read_text())
    public={entry['url']:entry for entry in metadata['sources']}
    for entry in verification['sources']:
        require(entry['metadata_match'] is True,'source verification failed')
        require(all(public[entry['url']][k]==entry[k] for k in ('bytes','sha256')),'public source metadata mismatch')
    return {'integrity':'PASS','payload_files':len(NAMES)-1,'target_id':11000162,'row':1892}
def dependency_replay(root=ROOT):
    d=json.loads((root/'DEPENDENCY_AUDIT.json').read_text())
    require(d['target_id']==11000162 and d['row']==1892,'dependency identity mismatch')
    require(d['attempts']==5 and [a['id'] for a in d['approaches']]==list(range(1,6)),'five approaches required')
    require(d['disposition']=='PARTIAL_PROGRESS_NOT_SOLVED','status inflation')
    require(d['thresholds']==[{'promise':'d >= 1','decision':'d = 1 versus d >= 2','total_algorithm_established':False},{'promise':'d >= 2','decision':'d = 2 versus d >= 3','total_algorithm_established':False}],'promise or totality inflation')
    require(d['certificate_kind']=='Analytic dependency audit, not a mathematical decision certificate','certificate scope inflation')
    require(d['worldwide_openness_claim'] is False and d['publication_performed'] is False and d['queue_edits_performed'] is False,'scope mismatch')
    require(all(a['accepted'] and a['missing'] for a in d['approaches']),'missing dependency qualifications')
    return {'analytic_dependency_audit':'PASS','mathematical_decision_certificate':False,'both_promised_problems':'NOT_SOLVED'}
def mutations():
    results=[]
    with tempfile.TemporaryDirectory(prefix='heegaard_mutations_') as tmp:
        parent=Path(tmp)
        for case in ('missing','extra','directory','symlink','fifo','content','manifest','status','threshold','certificate'):
            root=parent/case;shutil.copytree(ROOT,root)
            root.chmod(0o755)
            for item in root.iterdir(): item.chmod(0o644)
            target=root/'ATTEMPT_REPORT.md'
            structural=case in ('missing','extra','directory','symlink','fifo')
            if case=='missing': target.unlink()
            elif case=='extra': (root/'extra.txt').write_text('extra')
            elif case=='directory': (root/'extra').mkdir()
            elif case=='symlink': target.unlink(); target.symlink_to(ROOT/'ATTEMPT_REPORT.md')
            elif case=='fifo': target.unlink();os.mkfifo(target)
            elif case=='content': target.write_text(target.read_text()+'\nMutation\n')
            elif case=='manifest': (root/'MANIFEST.json').write_text('{}')
            else:
                p=root/'DEPENDENCY_AUDIT.json';d=json.loads(p.read_text())
                if case=='status': d['disposition']='SOLVED'
                elif case=='threshold': d['thresholds'][1]['total_algorithm_established']=True
                else: d['certificate_kind']='Mathematical decision certificate'
                p.write_text(json.dumps(d))
            before=len(READ_EVENTS)
            try:
                if case in ('status','threshold','certificate'): dependency_replay(root)
                else: integrity(root)
            except (RuntimeError,KeyError,ValueError): pass
            else: raise RuntimeError('mutation survived: '+case)
            if structural: require(len(READ_EVENTS)==before,'content read before structural rejection: '+case)
            results.append({'case':case,'rejected':True,'no_content_read':True if structural else None})
    import socket
    try: socket.socket()
    except RuntimeError as e: require(str(e)=='socket event denied','wrong socket rejection')
    else: raise RuntimeError('socket guard failed')
    return {'mutations':results,'socket_construction_denied':True,'scope':'Integrity and declared-dependency mutations, not mathematical counterexample tests.'}
def main():
    sys.dont_write_bytecode=True
    sys.addaudithook(audit)
    require(len(sys.argv)==2 and sys.argv[1] in ('--integrity','--replay','--mutations'),'choose --integrity, --replay, or --mutations')
    result=integrity()
    if sys.argv[1]=='--replay': result.update(dependency_replay())
    if sys.argv[1]=='--mutations': result.update(mutations())
    print(json.dumps(result,indent=2,sort_keys=True))
if __name__=='__main__': main()
