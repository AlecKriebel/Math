"""Separate ROOT-only reader, saved but not run by the round-2 adversary.
Independently reads the fixed index and an existing ROOT closure; no imports
from the closure helper, control reruns, scientific review or publication.
"""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, os, stat, sys

BASE=Path(__file__).resolve().parent
CLOSE=BASE.parent/'ROOT_PREPRINT_ROUND2_ADJUDICATION_20261003.json'
DEST=BASE.parent/'ROOT_PREPRINT_ROUND2_READBACK_20261003.json'

def timestamp(): return datetime.now(timezone.utc).isoformat()
def file_record(path):
    metadata=os.lstat(path)
    if stat.S_IFMT(metadata.st_mode)!=stat.S_IFREG or metadata.st_nlink!=1: raise RuntimeError('File type/link discrepancy')
    data=Path(path).read_bytes()
    return dict(type='regular_file',nlink=metadata.st_nlink,full_mode_07777=f'{metadata.st_mode & 0o7777:04o}',
                bytes=len(data),sha256=hashlib.sha256(data).hexdigest())

def main():
    if sys.argv[1:]!=['--root-only-readback']: raise RuntimeError('Require --root-only-readback after ROOT closure')
    if DEST.exists() or DEST.is_symlink(): raise RuntimeError('Refusing existing readback')
    began=timestamp()
    source=json.loads((BASE/'SOURCE.json').read_bytes());ready=json.loads((BASE/'READY.json').read_bytes())
    closure=json.loads(CLOSE.read_bytes())
    if file_record(BASE/'SOURCE.json')!=ready['source']: raise RuntimeError('SOURCE anchor mismatch')
    if file_record(BASE/'SOURCE.json')['full_mode_07777']!='0444' or file_record(BASE/'READY.json')['full_mode_07777']!='0444': raise RuntimeError('Index permissions')
    present_files=[];present_dirs=['.']
    for current, dirs, files in os.walk(BASE,followlinks=False):
        for entry in dirs:
            q=Path(current)/entry
            if not stat.S_ISDIR(os.lstat(q).st_mode): raise RuntimeError('Unsupported directory entry')
            present_dirs.append(str(q.relative_to(BASE)))
        for entry in files:
            q=Path(current)/entry; file_record(q);present_files.append(str(q.relative_to(BASE)))
    if set(present_files)!=set(source['files'])|{'SOURCE.json','READY.json'} or set(present_dirs)!=set(source['directories']): raise RuntimeError('Owned packet topology')
    for entry,expected in source['files'].items():
        if file_record(BASE/entry)!=expected: raise RuntimeError('Owned body or complete mode changed: '+entry)
    for entry,expected in source['directories'].items():
        q=BASE if entry=='.' else BASE/entry
        if f'{os.lstat(q).st_mode & 0o7777:04o}'!=expected['full_mode_07777']: raise RuntimeError('Directory complete mode')
    for item in source['publication_artifacts']:
        if file_record(Path(item['path']))!=item['pin']: raise RuntimeError('Publication source body/mode changed')
    for item in source['capture_relationships']:
        captured=json.loads((BASE/item['capture']).read_bytes()); launched=json.loads((BASE/item['prelaunch']).read_bytes())
        if captured.get('actual_execution') is not True: raise RuntimeError('Not an actual capture')
        for field,value in launched.items():
            if captured.get(field)!=value: raise RuntimeError('Prelaunch field differs')
        for channel in ('stdout','stderr'):
            body=(BASE/item[channel]).read_bytes()
            if len(body)!=captured[channel]['bytes'] or hashlib.sha256(body).hexdigest()!=captured[channel]['sha256']: raise RuntimeError('Full stream discrepancy')
    pages=json.loads((BASE/'PDF_RENDER_CAPTURE.json').read_bytes())['pages']
    if set(pages)!={f'page-{i}.png' for i in range(1,7)}: raise RuntimeError('Six retained preview pages required')
    for page,expected in pages.items():
        data=(BASE/'pdf_review'/page).read_bytes()
        if len(data)!=expected['bytes'] or hashlib.sha256(data).hexdigest()!=expected['sha256']: raise RuntimeError('Preview pin')
    for label,filename in [('source','SOURCE.json'),('ready','READY.json'),('report','REPORT.md'),('verdict','VERDICT.json')]:
        if closure[label]!=file_record(BASE/filename): raise RuntimeError('Closure must bind exact delivered objects')
    if closure['new_scientific_review_credit']!=0 or closure['native_acceptance_or_publication_claimed'] or closure['ROOT_release_approval_claimed']: raise RuntimeError('Closure scope exceeded')
    record={'schema':'pr57-root-round2-independent-evidence-reader/v1','status':'ROOT_SEPARATE_ROUND2_READBACK_COMPLETE',
            'actual_reader_pid':os.getpid(),'start_utc':began,'end_utc':timestamp(),'closure':file_record(CLOSE),
            'source':file_record(BASE/'SOURCE.json'),'ready':file_record(BASE/'READY.json'),
            'owned_regular_file_count':len(present_files),'directory_count':len(present_dirs),
            'new_scientific_review_credit':0,'ROOT_release_approval_claimed':False,'native_acceptance_or_publication_claimed':False}
    with DEST.open('x') as target:json.dump(record,target,indent=2,sort_keys=True);target.write('\n')
    os.chmod(DEST,0o444)
    print(json.dumps(record,indent=2,sort_keys=True))

if __name__=='__main__':main()
