#!/usr/bin/env python3
"""Finite own-only namespace fixtures; no project import, science or subprocess."""
import ast
import hashlib
import json
import os
from pathlib import Path
import stat

E=Path(__file__).absolute().parent

def main():
    if (E/'FINAL_SEAL.json').exists():
        raise ValueError('sealed: no fixture execution authority')
    tree=ast.parse((E/'verify_editorial.py').read_text())
    names={'need','read','pin','scan','close_namespace'}
    nodes=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in names]
    if {n.name for n in nodes}!=names:
        raise ValueError('missing actual closure functions')
    env={'hashlib':hashlib,'os':os,'Path':Path,'stat':stat,'checks':0}
    exec(compile(ast.Module(body=nodes,type_ignores=[]),'actual-owned-closure-functions','exec'),env)
    base=E/('namespace-fixture-work' if __debug__ else 'namespace-fixture-work-optimized')
    base.mkdir()
    root=base/'fixture';root.mkdir()
    (root/'ordinary').write_bytes(b'bound complete ordinary body\n')
    (root/'declared-empty').mkdir()
    expected=env['scan'](root)
    env['close_namespace'](root,expected)
    rejected=[]
    def reject(label):
        try:env['close_namespace'](root,expected)
        except ValueError:rejected.append(label)
        else:raise ValueError('fixture escaped: '+label)
    (root/'unlisted-empty').mkdir();reject('unlisted empty directory');(root/'unlisted-empty').rmdir()
    (root/'future-run-state').mkdir();reject('anonymous future subtree');(root/'future-run-state').rmdir()
    os.mkfifo(root/'pipe');reject('FIFO before any body read');(root/'pipe').unlink()
    (root/'link').symlink_to('ordinary');reject('symlink file');(root/'link').unlink()
    (root/'dir-link').symlink_to('declared-empty',target_is_directory=True);reject('symlink directory');(root/'dir-link').unlink()
    (root/'ordinary').write_bytes(b'changed body\n');reject('whole body changed');(root/'ordinary').write_bytes(b'bound complete ordinary body\n')
    (root/'declared-empty').rmdir();reject('missing declared empty directory');(root/'declared-empty').mkdir()
    (root/'FINAL_SEAL.json').mkdir();reject('terminal spelling does not exempt directory');(root/'FINAL_SEAL.json').rmdir()
    env['close_namespace'](root,expected)
    (root/'ordinary').unlink();(root/'declared-empty').rmdir();root.rmdir()
    if list(base.iterdir()) or len(rejected)!=8:
        raise ValueError('fixture cleanup or count')
    print(json.dumps({'status':'OWN_NAMESPACE_CONTROLS_PASSED','mode':'ordinary' if __debug__ else 'optimized-O',
      'actual_extracted_functions':sorted(names),'function_source_SHA256':hashlib.sha256(ast.unparse(ast.Module(body=nodes,type_ignores=[])).encode()).hexdigest(),
      'legitimate_declared_empty_accepted':True,'rejections':rejected,'ordinary_roundtrip_revalidated':True,
      'all_created_specials_links_and_child_paths_removed':True,'retained_empty_finite_root':base.name,
      'no_source_or_scientific_execution':True},sort_keys=True))

if __name__=='__main__':
    main()
