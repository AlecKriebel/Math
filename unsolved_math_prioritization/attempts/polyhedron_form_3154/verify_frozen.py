#!/usr/bin/env python3
"""Offline, fail-closed verification. Receipt is outside the frozen directory."""
import sys

def deny_network(event,args):
    if event.startswith('socket.'):
        raise RuntimeError('Socket operation forbidden: '+event)
sys.addaudithook(deny_network)
import ast,contextlib,hashlib,io,json,os,stat,tempfile
from pathlib import Path

ALLOWED={'ACCEPTANCE.md','CLT_PROOF_AUDIT.md','independent_clt_review.md','check_constants.py','check_results.json','verification_manifest.json','SOURCE_STATUS_GATE.md','dataset_verification.json','public_sources.json','AST_PROVENANCE.json','README.md','verify_frozen.py','FREEZE_MANIFEST.json'}
def require(ok,message):
    if not ok: raise RuntimeError(message)
def inventory(root,expected):
    require(stat.S_ISDIR(os.lstat(root).st_mode),'Root must be a real directory')
    found=set()
    def walk(folder):
        with os.scandir(folder) as entries:
            for entry in entries:
                path=Path(entry.path); mode=entry.stat(follow_symlinks=False).st_mode
                require(stat.S_ISDIR(mode) or stat.S_ISREG(mode),'Rejected nonregular entry: '+str(path))
                rel=str(path.relative_to(root))
                require(rel in expected,'Unexpected inventory entry: '+rel)
                if stat.S_ISDIR(mode):walk(path)
                else:found.add(rel)
    walk(root)
    require(found==expected,'Missing inventory entries')
    return found

def read_regular(path):
    fd=os.open(path,os.O_RDONLY|os.O_NOFOLLOW|os.O_NONBLOCK)
    try:
        require(stat.S_ISREG(os.fstat(fd).st_mode),'Nonregular read refused')
        with os.fdopen(fd,'rb',closefd=False) as stream:return stream.read()
    finally:os.close(fd)
def digest(data):return hashlib.sha256(data).hexdigest()
class Harden(ast.NodeTransformer):
    def visit_Assert(self,node):
        return ast.copy_location(ast.If(test=ast.UnaryOp(op=ast.Not(),operand=node.test),body=[ast.Raise(exc=ast.Call(func=ast.Name(id='RuntimeError',ctx=ast.Load()),args=[ast.Constant(value='Mathematical assertion failed')],keywords=[]),cause=None)],orelse=[]),node)
def execute(src):
    tree=ast.fix_missing_locations(Harden().visit(ast.parse(src)))
    require(not any(isinstance(n,ast.Assert) for n in ast.walk(tree)),'Unhardened assertion')
    with tempfile.TemporaryDirectory(prefix='polyhedron_replay_') as tmp:
        filename=str(Path(tmp)/'check_constants.py')
        namespace={'__file__':filename,'__name__':'__main__'}
        with contextlib.redirect_stdout(io.StringIO()):exec(compile(tree,filename,'exec'),namespace)
        result=json.loads(read_regular(Path(tmp)/'check_results.json'))
        return result

def main():
    require(len(sys.argv)==2,'Usage: python [-O] verify_frozen.py EXTERNAL_RECEIPT.json')
    root=Path(os.path.abspath(os.path.dirname(__file__)))
    inventory(root,ALLOWED) # No payload file is opened before full recursive inventory passes.
    receipt_path=Path(os.path.abspath(sys.argv[1]))
    require(root not in receipt_path.parents,'Receipt must remain external')
    receipt=json.loads(read_regular(receipt_path))
    require(set(receipt['files'])==ALLOWED,'Receipt inventory mismatch')
    for name,item in receipt['files'].items():
        data=read_regular(root/name)
        require(len(data)==item['bytes'] and digest(data)==item['sha256'],'Frozen byte mismatch: '+name)
    manifest=json.loads(read_regular(root/'FREEZE_MANIFEST.json'))
    require(set(manifest['files'])==ALLOWED-{'FREEZE_MANIFEST.json'},'Manifest inventory mismatch')
    for name,item in manifest['files'].items():
        data=read_regular(root/name)
        require(len(data)==item['bytes'] and digest(data)==item['sha256'],'Manifest mismatch: '+name)
    source=read_regular(root/'check_constants.py').decode()
    provenance=json.loads(read_regular(root/'AST_PROVENANCE.json'))
    require(digest(source.encode())==provenance['sha256'],'Source provenance mismatch')
    require(digest(ast.dump(ast.parse(source),include_attributes=False).encode())==provenance['whole_module_ast_sha256'],'Whole module AST mismatch')
    expected=json.loads(read_regular(root/'check_results.json'))
    require(execute(source)==expected,'Full replay differs from original saved results')
    controls={}
    mutations={
      'wrong_curvature':('(3*a-1)*s.log(3*a-1)','(4*a-1)*s.log(3*a-1)'),
      'wrong_unrooting_normalizer':('486*math.sqrt(math.pi)','243*math.sqrt(math.pi)'),
      'wrong_variance_scale':('fourth/(e/32)**2','fourth/(e/16)**2'),
      'missing_binomial_shift':('logchoose(2*i,j+3)','logchoose(2*i,j)'),
    }
    for name,(before,after) in mutations.items():
        require(source.count(before)==1,'Mutation target not unique')
        altered=source.replace(before,after)
        require(digest(ast.dump(ast.parse(altered),include_attributes=False).encode())!=provenance['whole_module_ast_sha256'],'AST mutation escaped')
        # Deliberately bypass provenance here to independently exercise mathematical checks.
        try:detected=execute(altered)!=expected
        except RuntimeError:detected=True
        require(detected,'Mathematical negative control escaped: '+name)
        controls[name]='REJECTED by mathematical assertion or full result mismatch; AST provenance also rejects'
    for kind in ('symlink','fifo','nested_directory','extra_regular'):
        with tempfile.TemporaryDirectory(prefix='poly_inventory_') as tmp:
            fixture=Path(tmp)
            target=fixture/'bad'
            if kind=='symlink':target.symlink_to('/does/not/exist')
            elif kind=='fifo':os.mkfifo(target)
            elif kind=='nested_directory':target.mkdir()
            else:target.write_text('unexpected')
            try:inventory(fixture,set())
            except RuntimeError:controls[kind]='REJECTED before payload reads'
            else:raise RuntimeError('Inventory negative control escaped: '+kind)
    print(json.dumps({'status':'PASS','optimization':sys.flags.optimize,'disposition':'already_solved','turns':1,'full_replay':'all symbolic, rational parity, and eight proxy cases match','controls':controls,'network':'socket operations prohibited by audit hook; no socket probes performed','proof_boundary':'authored audit plus independent review; classical theorems are inputs, preprint not journal-certified'},indent=2))
if __name__=='__main__':main()
