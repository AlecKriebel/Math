"""New readiness-only optional Root-reviewed runner; old runner is unchanged.
python3 -B run_ready_with_tree_cache.py --root-reviewed MODE GENERATION execute
"""
from pathlib import Path
import hashlib,importlib.util,json,sys
if sys.flags.optimize or not sys.dont_write_bytecode:raise RuntimeError('Ordinary Python -B required')
D=Path(__file__).resolve().parent;A=D.parent;AUDITS=A.parent;T=A/'immutable_tree_transport_01'
def require(ok,msg):
    if not ok:raise RuntimeError(msg)
def pin(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def checked(f,x,readonly=True):
    require(f.is_file() and not f.is_symlink() and (not readonly or f.stat().st_mode&0o777==0o444) and pin(f.read_bytes())==x,'Reviewed source pin/readonly mismatch '+str(f));return f.read_bytes()
def load_module(name,f):
    s=importlib.util.spec_from_file_location(name,f);x=importlib.util.module_from_spec(s);s.loader.exec_module(x);return x
def validate_sources():
    own=json.loads((D/'SAFE_AUTHORED_MANIFEST.json').read_bytes())
    require(set(own['files'])=={'checkpoint_ready204.py','run_ready_with_tree_cache.py','CHECKPOINT_CONTRACT.md','RESEARCH_LOG.md'},'Readiness-only helper manifest')
    for name,x in own['files'].items():checked(D/name,x)
    checked(A/'ROOT_IMMUTABLE_TREE_TRANSPORT_ACCEPTANCE_01.json',{'bytes':891,'sha256':'e8ec04013dee6df99c35df0b05e4b9da088402c54c782b65f4ec2d7587bc3992'})
    tm=json.loads(checked(T/'SAFE_AUTHORED_MANIFEST.json',{'bytes':2982,'sha256':'64efffc6de309930dc8e80f1ef4c8bdcf6fed5a654947f444ad6aa4ebc568f53'}))
    for name,x in tm['files'].items():require(Path(name).name==name,'Reviewed transport manifest path');checked(T/name,x)
    graph=json.loads(checked(T/'CALL_GRAPH_AND_SOURCE_PINS.json',tm['files']['CALL_GRAPH_AND_SOURCE_PINS.json']))
    for entry in graph['six_modules']:checked(AUDITS/entry['source'],entry['pin'],readonly=False)
    for name,x in graph['additional_source_pins'].items():checked(AUDITS/name,x,readonly=False)
    checked(T/'tree_transport.py',{'bytes':10532,'sha256':'65db9937fa474626fb833357bec447830e24c4d14f0362b98e0fd3d0a4f7e0b9'})
def main():
    require(len(sys.argv)==5 and sys.argv[1]=='--root-reviewed' and sys.argv[4]=='execute','Explicit Root review/phase/generation/execute required')
    mode,gen=sys.argv[2:4];require(mode in ['prepare','verify','accept','sync','pointer'],'Readiness-only reviewed phase required');validate_sources()
    helper=load_module('Root_reviewed_ready204_checkpoint',D/'checkpoint_ready204.py');adapter=load_module('Root_accepted_immutable_tree_transport_for_ready204',T/'tree_transport.py')
    core=helper.v;original_load=core.load;restorers=[];caches=[]
    def cached_load():
        values=original_load();cache,restore=adapter.install_loaded(values[0],values[1]);caches.append(cache);restorers.append(restore);return values
    core.load=cached_load
    try:
        if mode=='sync':helper.sync(gen)
        elif mode=='pointer':helper.pointer(gen)
        else:helper.run(mode,gen)
    finally:
        core.load=original_load;summaries=[dict(x.stats) for x in caches]
        for restore in reversed(restorers):restore()
        if summaries:print(json.dumps({'Root_accepted_immutable_tree_transport_stats':summaries,'mutable_requests_uncached_no_retry':True}))
if __name__=='__main__':main()
