"""Read-only whole07 review closure, source and decisive-capture verification."""
from pathlib import Path
import hashlib,json,stat,zipfile
ROOT=Path(__file__).resolve().parent
OPS=ROOT.parent/'operations07'
def need(x,m):
    if not x:raise RuntimeError(m)
def sha(b):return hashlib.sha256(b).hexdigest()
def checked_entries(base,manifest,excluded):
    pins=manifest['entries']
    actual={'.',*[p.relative_to(base).as_posix() for p in base.rglob('*') if p.relative_to(base).as_posix() not in excluded]}
    need(actual==set(pins),'Physical closure mismatch')
    files=directories=0
    for name,pin in pins.items():
        path=base if name=='.' else base/name
        s=path.lstat()
        need(not stat.S_ISLNK(s.st_mode),'Symlink')
        need(stat.S_IMODE(s.st_mode)==pin['mode'] and s.st_mtime_ns==pin['mtime_ns'],'Metadata changed: '+name)
        if pin['kind']=='file':
            b=path.read_bytes()
            need(len(b)==pin['bytes'] and sha(b)==pin['sha256'],'Bytes changed: '+name);files+=1
        else:
            need(pin['kind']=='directory' and stat.S_ISDIR(s.st_mode),'Entry kind');directories+=1
    return files,directories
def main():
    review=json.loads((ROOT/'MANIFEST.json').read_bytes())
    own=checked_entries(ROOT,review,{'MANIFEST.json'})
    raw=(OPS/'MANIFEST.json').read_bytes()
    need(sha(raw)=='8551344abd63c4edd9cb3dc22c815c1d69e4581f846b0f2db75f4dde0de1cc8a','Preparation seal changed')
    source=checked_entries(OPS,json.loads(raw),{'MANIFEST.json'})
    zpath=ROOT/'private/STATE_RACE_VIRTUAL_CAPTURE_BYTES.zip'
    with zipfile.ZipFile(zpath) as z:
        m=json.loads(z.read('MANIFEST.json'))
        need(len(z.namelist())==len(set(z.namelist())) and set(z.namelist())=={'MANIFEST.json',*['payload/'+k for k in m['content']]},'Virtual custody closure')
        for name,pin in m['content'].items():
            b=z.read('payload/'+name);need(len(b)==pin['bytes'] and sha(b)==pin['sha256']==name,'Virtual body changed')
        need(all(k in m['content'] for k in m['paths'].values()),'Missing virtual path body')
    result=json.loads((ROOT/'CONCURRENT_STATE_RACE_RESULT02.json').read_bytes())
    need(result['counterexample'] is True and result['stage_verified'] is True and result['concurrent_exact_bytes_preserved'] is False,'Counterexample result changed')
    need(result['concurrent_before']['id']==999 and result['after']['id']==777 and len(result['native_calls'])==4,'Counterexample mechanism changed')
    print(json.dumps({'status':'HOLD_PACKET_READBACK_PASS','review_files':own[0],'review_directories':own[1],'preparation_files':source[0],'preparation_directories':source[1],'decisive_capture_paths':len(m['paths']),'exact_unique_capture_bodies':len(m['content']),'provider_mutations':0,'publication_ready':False},sort_keys=True))
if __name__=='__main__':main()
