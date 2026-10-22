"""Optional Root-reviewed runner; not executed by adapter author.
Usage: python3 -B run_with_tree_cache.py --root-reviewed HELPER MODE GENERATION execute
Only prepare/verify/accept/sync of the explicit existing PR204 helper are allowed.
"""
from pathlib import Path
import importlib.util,json,sys
if sys.flags.optimize or not sys.dont_write_bytecode:raise RuntimeError('Ordinary Python -B required')
from tree_transport import install_loaded,require
D=Path(__file__).resolve().parent;A=D.parent
def main():
    require(len(sys.argv)==6 and sys.argv[1]=='--root-reviewed','Root review required: --root-reviewed HELPER MODE GENERATION')
    f=Path(sys.argv[2]);mode=sys.argv[3];gen=sys.argv[4]
    # A final explicit token prevents accidental execution of a pasted partial command.
    require(sys.argv[5]=='execute' and mode in ['prepare','verify','accept','sync'],'Explicit reviewed phase/execute token required')
    allowed={A/'science_checkpoint_01/checkpoint_math204.py',A/'priority_checkpoint_01/checkpoint_priority204.py',A/'package_checkpoint_01/checkpoint_package204.py'}
    require(f.is_absolute() and f in allowed and f.is_file() and not f.is_symlink() and f.stat().st_mode&0o777==0o444,'Explicit sealed existing PR204 helper path required')
    spec=importlib.util.spec_from_file_location('Root_reviewed_checkpoint_with_optional_tree_cache',f);helper=importlib.util.module_from_spec(spec);spec.loader.exec_module(helper)
    core=helper.v;original_load=core.load;restorers=[];caches=[]
    def cached_load():
        values=original_load();cache,restore=install_loaded(values[0],values[1]);caches.append(cache);restorers.append(restore);return values
    core.load=cached_load
    try:
        if mode=='sync':helper.sync(gen)
        else:helper.run(mode,gen)
    finally:
        core.load=original_load
        summaries=[dict(x.stats) for x in caches]
        for restore in reversed(restorers):restore()
        if summaries:print(json.dumps({'immutable_tree_cache_transport_stats':summaries,'no_mutable_response_cached':True}))
if __name__=='__main__':main()
