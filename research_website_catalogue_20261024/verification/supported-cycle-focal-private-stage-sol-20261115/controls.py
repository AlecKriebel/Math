"""New finite namespace fixtures only; no renderer, source/science or old fault campaign."""
import sys
sys.dont_write_bytecode = True
import ast
import json
import os
from pathlib import Path
import stat
import tempfile

O = Path(__file__).resolve().parent


def denied(action):
    try:
        action()
    except RuntimeError:
        return
    raise RuntimeError('expected namespace rejection missing')


def main():
    if (O / 'FINAL_SEAL.json').exists():
        raise RuntimeError('Immutable FINAL: controls may run only before sealing')
    tree = ast.parse((O / 'verify_stage.py').read_bytes())
    definitions = [n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in {'need','extent','closed_namespace'}]
    environment = {'Path':Path,'os':os,'stat':stat,'CHECKS':0}
    exec(compile(ast.Module(body=definitions,type_ignores=[]),'<current-own-namespace-definitions>','exec'),environment)
    check = environment['closed_namespace']
    with tempfile.TemporaryDirectory(prefix='finite-namespace-',dir=O / 'private') as directory:
        root = Path(directory); (root / 'inputs').mkdir()
        for name in ['payload','OWNED_MANIFEST.json','FINAL_SEAL.json']:
            (root / name).write_bytes(b'owned fixture bytes; no actual receipt')
        action = lambda: check(root,['payload'],['inputs'],['OWNED_MANIFEST.json','FINAL_SEAL.json'])
        action()
        (root / 'extra-empty').mkdir(); denied(action); (root / 'extra-empty').rmdir()
        os.mkfifo(root / 'fifo'); denied(action); (root / 'fifo').unlink()
        (root / 'link').symlink_to(root / 'payload'); denied(action); (root / 'link').unlink()
        (root / 'inputs/FINAL_SEAL.json').write_bytes(b'nested basename is not excluded')
        denied(action); (root / 'inputs/FINAL_SEAL.json').unlink()
        (root / 'run-state').mkdir(); denied(action)
        (root / 'run-state/anonymous').write_bytes(b'no future subtree exception'); denied(action)
        (root / 'run-state/anonymous').unlink(); (root / 'run-state').rmdir()
        action()
    print(json.dumps({'status':'PASS_NEW_FINITE_NAMESPACE_CONTROLS','declared_empty_inputs_preserved':True,
                      'only_exact_root_terminals_excluded':True,
                      'rejected':['unlisted-empty-directory','FIFO','symlink','nested-terminal-basename',
                                  'future-empty-run-state','anonymous-future-run-state-payload'],
                      'future_runtime_namespace_exemption':False,'old_fault_science_renderer_campaigns_executed':False,
                      'writes_only_owned_temporary_child':True},indent=2))

if __name__ == '__main__':
    main()
