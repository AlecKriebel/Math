"""Shared read-only source loader for frozen/proposed/canonical controls."""
import hashlib,json,sys,types
from pathlib import Path
HERE=Path(__file__).resolve().parent
AUDIT=HERE.parent
FROZEN=HERE/'pre_review02_binding'
NAMES=['ops_binding','prepublication_check','publication_live_gates','repository_integration','verify_published_files','publication_lifecycle','record_publication_ledger']

def implementation(kind='proposed'):
    bindings={e['path']:e for e in json.loads((HERE/'INPUT_PRESERVATION.json').read_text())['files']}
    for name in NAMES:
        path=(FROZEN/(name+'.py') if kind=='frozen' else HERE/'proposed_helpers'/(name+'.py') if kind=='proposed' else AUDIT/(name+'.py'))
        body=path.read_bytes()
        if kind=='frozen' and hashlib.sha256(body).hexdigest()!=bindings[name+'.py']['sha256']:raise RuntimeError('Frozen helper binding differs')
        module=types.ModuleType(name);module.__file__=str(AUDIT/(name+'.py'));sys.modules[name]=module
        exec(compile(body,str(path),'exec'),module.__dict__)
    return tuple(sys.modules[n] for n in NAMES)
