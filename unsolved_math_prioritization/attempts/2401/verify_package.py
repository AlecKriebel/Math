#!/usr/bin/env python3
"""Fail-closed local verification. Finite evidence, never a continuum proof."""
import ast
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parent

def require(ok, message):
    if not ok:
        raise RuntimeError(message)

def digest(b):
    return {'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()}

def inventory(root):
    # lstat BEFORE reading or recursing: FIFOs cannot block this inventory.
    require(stat.S_ISDIR(root.lstat().st_mode), 'root is not a real directory')
    files, dirs = {}, []
    def visit(directory):
        for path in sorted(directory.iterdir()):
            mode = path.lstat().st_mode
            rel = path.relative_to(root).as_posix()
            if stat.S_ISREG(mode):
                files[rel] = digest(path.read_bytes())
            elif stat.S_ISDIR(mode):
                dirs.append(rel)
                visit(path)
            else:
                raise RuntimeError('nonregular entry rejected: ' + rel)
    visit(root)
    return {'files': files, 'directories': dirs}

def run(path, optimized=False):
    cmd = [sys.executable, '-B'] + (['-O'] if optimized else []) + [str(path)]
    return subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=60)

def reconstruct(original):
    records=[]
    class Harden(ast.NodeTransformer):
        def visit_Assert(self, node):
            require(node.msg is None, 'unexpected assert message')
            i=len(records)+1
            new=ast.If(test=ast.UnaryOp(op=ast.Not(),operand=node.test),body=[ast.Raise(exc=ast.Call(func=ast.Name(id='AssertionError',ctx=ast.Load()),args=[ast.Constant(value='check_%02d failed'%i)],keywords=[]),cause=None)],orelse=[])
            records.append({'id':i,'original_line':node.lineno,'original_source':ast.get_source_segment(original,node),'original_ast':ast.dump(node,include_attributes=False),'replacement_ast':ast.dump(new,include_attributes=False)})
            return ast.copy_location(new,node)
    return ast.fix_missing_locations(Harden().visit(ast.parse(original))), records

def main():
    actual=inventory(ROOT)
    expected=json.loads((ROOT/'MANIFEST.json').read_text())
    actual['files'].pop('MANIFEST.json')
    require(actual == expected['inventory'], 'recursive inventory mismatch')
    original=(ROOT/'original_exact_checks.py').read_text()
    hardened=(ROOT/'exact_checks.py').read_text()
    rebuilt, records=reconstruct(original)
    provenance=json.loads((ROOT/'AST_PROVENANCE.json').read_text())
    require(provenance['checks']==records, 'assert provenance mismatch')
    require(ast.dump(rebuilt,include_attributes=False)==ast.dump(ast.parse(hardened),include_attributes=False),'whole-module AST mismatch')
    require(not any(isinstance(n,ast.Assert) for n in ast.walk(ast.parse(hardened))), 'assert survives hardening')
    require(provenance['original_sha256']==digest(original.encode())['sha256'],'original provenance hash')
    require(provenance['hardened_sha256']==digest(hardened.encode())['sha256'],'hardened provenance hash')
    saved=(ROOT/'exact_checks_result.json').read_bytes()
    runs=[]
    for name in ['original_exact_checks.py','exact_checks.py']:
        for optimized in [False,True]:
            result=run(ROOT/name,optimized)
            require(result.returncode==0 and result.stderr==b'' and result.stdout==saved,'complete output reproduction failed')
            runs.append({'file':name,'optimized':optimized,'stdout':digest(result.stdout),'stderr_bytes':0,'exit_code':0})
    controls=[]
    with tempfile.TemporaryDirectory(prefix='ep949-') as temporary:
        temp=Path(temporary)
        # Each mathematical predicate must fail under normal AND -O execution.
        for record in records:
            mutant=ast.parse(hardened)
            target='check_%02d failed'%record['id']
            changed=0
            for node in ast.walk(mutant):
                if isinstance(node,ast.If) and len(node.body)==1 and isinstance(node.body[0],ast.Raise):
                    if ast.literal_eval(node.body[0].exc.args[0])==target:
                        node.test=ast.Constant(value=True); changed+=1
            require(changed==1,'mutation target is not unique')
            path=temp/'mutant.py'; path.write_text(ast.unparse(ast.fix_missing_locations(mutant)))
            for optimized in [False,True]:
                result=run(path,optimized)
                require(result.returncode!=0 and target.encode() in result.stderr and result.stdout==b'','mathematical predicate deletion not detected')
            controls.append({'check_id':record['id'],'forced_false_predicate_detected_normal_and_optimized':True})
        # Specific mathematical regressions, not only forced-failure predicates.
        regressions={
            'omit_sumset_diagonals': ('return {a+b for a in A for b in B}', 'return {a+b for a in A for b in B if a != b}'),
            'omit_witness_sumset': ('return not (S&A or S&sumset(A))', 'return not (S&A)'),
            'omit_reflection_translation': ('A={x-s for x in C}', 'A={x for x in C}'),
            'weaken_reflection_bound': ('assert max(cores.values())==3', 'assert max(cores.values())==2'),
        }
        for label,(old,new) in regressions.items():
            require(original.count(old)==1,'mutation source missing')
            tree,_=reconstruct(original.replace(old,new))
            path=temp/'mutant.py'; path.write_text(ast.unparse(tree))
            for optimized in [False,True]:
                result=run(path,optimized)
                require(result.returncode!=0 and b'AssertionError' in result.stderr,'mathematical regression not detected: '+label)
            controls.append({'regression':label,'detected_normal_and_optimized':True})
        # Nested inventory attacks: regular extras, symlink, directory symlink,
        # FIFO, Unix socket, and unexpected empty directory.
        for kind in ['symlink','directory_symlink','fifo']:
            root=temp/kind; (root/'nested').mkdir(parents=True)
            target=root/'nested'/'attack'
            if kind=='symlink': target.symlink_to(ROOT/'PROOF_REPORT.md')
            elif kind=='directory_symlink': target.symlink_to(ROOT,target_is_directory=True)
            elif kind=='fifo': os.mkfifo(target)
            try:
                inventory(root)
            except RuntimeError as exc:
                require('nonregular entry rejected' in str(exc),'wrong rejection')
            else:
                raise RuntimeError('inventory accepted '+kind)
            controls.append({'inventory_attack':kind,'rejected_before_read':True})
        # Creation of a Unix socket is denied in this environment. Synthetic
        # mode checks cover default rejection, without claiming real fixtures.
        for kind,mode in [('socket',stat.S_IFSOCK),('block_device',stat.S_IFBLK),('character_device',stat.S_IFCHR)]:
            require(not stat.S_ISREG(mode) and not stat.S_ISDIR(mode), 'special mode misclassified')
            controls.append({'inventory_mode':kind,'synthetic_default_rejection':True,'real_fixture_created':False})
        root=temp/'regular_extra'; root.mkdir(); baseline=inventory(root)
        (root/'nested').mkdir(); require(inventory(root)!=baseline,'empty directory undetected')
        (root/'nested'/'extra').write_text('extra'); require(inventory(root)!=baseline,'extra file undetected')
        controls.append({'inventory_attack':'extra_regular_file_and_empty_directory','detected':True})
    result={'disposition':'NOT SOLVED','all_passed':True,'whole_module_ast_equivalence':True,'asserts_hardened':len(records),'complete_output_runs':runs,'negative_controls':controls,'inventory':actual,'limits':'Finite checks and artifact integrity only; no continuum proof, novelty or live source-status certificate.'}
    print(json.dumps(result,indent=2,sort_keys=True))

if __name__=='__main__':
    main()
