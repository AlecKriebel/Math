"""Optional exact PR205 custody runner. Root reviews source and manifest first.
python3 -B run_intake205_with_tree_cache.py --root-reviewed MODE GEN execute
The accepted adapter caches only authenticated immutable nonrecursive trees.
"""
from pathlib import Path
import hashlib,importlib.util,json,sys
if sys.flags.optimize or not sys.dont_write_bytecode:raise RuntimeError('Ordinary Python -B required')
D=Path(__file__).resolve().parent;A=D.parent;AUDITS=A.parent;OLD=AUDITS/'pr204_5100012';T=OLD/'immutable_tree_transport_01'
OWN={'freeze_original205.py','checkpoint_intake205.py','run_intake205_with_tree_cache.py','offline_intake_guards.py','CHECKPOINT_CONTRACT.md','CUSTODY_RECHECK.json','ORIGINAL_DECLARED_SOURCE_HASHES.json','BASELINE_AUTHORITY.json','INTAKE10_PREPARATION_CONTRACT.json','OFFLINE_INTAKE_GUARDS.json','RESEARCH_LOG.md'}
def require(ok,msg):
    if not ok:raise RuntimeError(msg)
def pin(raw):return {'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}
def checked(path,expected,readonly=True):
    require(path.is_file() and not path.is_symlink() and (not readonly or path.stat().st_mode&0o777==0o444),'Regular readonly source '+str(path));raw=path.read_bytes();require(pin(raw)==expected,'Reviewed source pin '+str(path));return raw
def load_module(name,path):
    spec=importlib.util.spec_from_file_location(name,path);value=importlib.util.module_from_spec(spec);spec.loader.exec_module(value);return value
def validate_sources():
    own=json.loads((D/'SAFE_AUTHORED_MANIFEST.json').read_bytes());require(set(own['files'])==OWN,'Exact custody205 helper allowlist')
    for name,x in own['files'].items():checked(D/name,x)
    checked(OLD/'ROOT_IMMUTABLE_TREE_TRANSPORT_ACCEPTANCE_01.json',{'bytes':891,'sha256':'e8ec04013dee6df99c35df0b05e4b9da088402c54c782b65f4ec2d7587bc3992'})
    tm=json.loads(checked(T/'SAFE_AUTHORED_MANIFEST.json',{'bytes':2982,'sha256':'64efffc6de309930dc8e80f1ef4c8bdcf6fed5a654947f444ad6aa4ebc568f53'}))
    for name,x in tm['files'].items():require(Path(name).name==name,'Transport basename');checked(T/name,x)
    graph=json.loads(checked(T/'CALL_GRAPH_AND_SOURCE_PINS.json',tm['files']['CALL_GRAPH_AND_SOURCE_PINS.json']))
    for entry in graph['six_modules']:checked(AUDITS/entry['source'],entry['pin'],readonly=False)
    for name,x in graph['additional_source_pins'].items():checked(AUDITS/name,x,readonly=False)
    checked(T/'tree_transport.py',{'bytes':10532,'sha256':'65db9937fa474626fb833357bec447830e24c4d14f0362b98e0fd3d0a4f7e0b9'})
def main():
    require(len(sys.argv)==5 and sys.argv[1]=='--root-reviewed' and sys.argv[4]=='execute','Explicit Root review/phase/generation/execute required')
    mode,gen=sys.argv[2:4];require(mode in ('prepare','verify','accept','sync'),'Custody205 phase required');validate_sources()
    helper=load_module('Root_reviewed_PR205_custody10',D/'checkpoint_intake205.py');helper.inputs();helper.baseline()
    adapter=load_module('Root_accepted_immutable_tree_transport_PR205',T/'tree_transport.py');core=helper.v;original_load=core.load;restorers=[];caches=[]
    def cached_load():
        values=original_load();cache,restore=adapter.install_loaded(values[0],values[1]);caches.append(cache);restorers.append(restore);return values
    core.load=cached_load
    try:
        if mode=='sync':helper.sync(gen)
        else:helper.run(mode,gen)
    finally:
        core.load=original_load;summaries=[dict(x.stats) for x in caches]
        for restore in reversed(restorers):restore()
        if summaries:print(json.dumps({'Root_accepted_immutable_tree_transport_stats':summaries,'mutable_requests_uncached_no_retry':True}))
if __name__=='__main__':main()
