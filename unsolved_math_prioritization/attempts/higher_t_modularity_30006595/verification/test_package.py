"""Exact mathematical mutation controls and inventory negative tests, without asserts."""
import ast,hashlib,json,os,pathlib,stat,subprocess,sys,tempfile
from unittest.mock import patch
from inventory import snapshot,kind
ROOT=pathlib.Path(__file__).resolve().parents[1]
SOURCE=(ROOT/'authored/check_fixed_alphabet.py').read_text()
def need(value,message):
    if not value:raise RuntimeError(message)
def run(source,opt):
    p=subprocess.run([sys.executable,'-B']+(['-O'] if opt else [])+['-c',source],capture_output=True,text=True,timeout=120)
    return {'returncode':p.returncode,'stdout':p.stdout,'stderr':p.stderr}
need(not any(isinstance(n,ast.Assert) for n in ast.walk(ast.parse(SOURCE))),'Residual assert')
original=(ROOT/'verification/original_check_fixed_alphabet.py.txt').read_bytes()
provenance=json.loads((ROOT/'verification/assert_provenance.json').read_text())
need(hashlib.sha256(original).hexdigest()==provenance['original_sha256'],'Original provenance hash mismatch')
need(hashlib.sha256(SOURCE.encode()).hexdigest()==provenance['hardened_sha256'],'Hardened provenance hash mismatch')
original_tree=ast.parse(original)
all_asserts=[n for n in ast.walk(original_tree) if isinstance(n,ast.Assert)]
need(len(all_asserts)==provenance['original_assert_count']==len(provenance['asserts']),'Whole-module assert census mismatch')
need([{'line':n.lineno,'end_line':n.end_lineno,'expression':ast.unparse(n.test)} for n in all_asserts]==provenance['asserts'],'Assert provenance expression mismatch')
class Harden(ast.NodeTransformer):
    def visit_Assert(self,node):
        return ast.If(test=ast.UnaryOp(op=ast.Not(),operand=node.test),body=[ast.Raise(exc=ast.Call(func=ast.Name(id='RuntimeError',ctx=ast.Load()),args=[ast.Constant(value='Exact check failed: '+ast.unparse(node.test))],keywords=[]),cause=None)],orelse=[])
need(ast.dump(ast.fix_missing_locations(Harden().visit(original_tree)),include_attributes=False)==ast.dump(ast.parse(SOURCE),include_attributes=False),'Non-assert mathematical AST changed')

mutations=[('gauge_sign','I2(mul(f, U[-1])), -1','I2(mul(f, U[-1])), 1'),('kernel_normalization','{1: 8, 2: -8, 4: 8}, 1, 16','{1: 8, 2: -8, 4: 8}, 1, 8'),('double_primitive','a[n] / n ** 2','a[n] / n'),('eta_substitution','{1: 24, 2: -48, 4: 24}, 1, 64','{1: 24, 2: -48, 4: 24}, 1, 32'),('parameter_sign','B[k] * j * j -','B[k] * j * j +'),('eisenstein_coefficient','if not f == scale(add(add(scale(E4(1), 1), scale(E4(2), -17))','if not f == scale(add(add(scale(E4(1), 1), scale(E4(2), -16))')]
report={'normal':run(SOURCE,False),'optimized':run(SOURCE,True),'mathematical_mutations':[],'inventory_tests':[]}
for mode in ['normal','optimized']:
    need(report[mode]['returncode']==0,'Baseline failed '+mode)
need(report['normal']['stdout']==report['optimized']['stdout'],'Optimized output mismatch')
for name,old,new in mutations:
    need(SOURCE.count(old)==1,'Mutation target not unique: '+name)
    altered=SOURCE.replace(old,new)
    modes={str(opt):run(altered,opt) for opt in [False,True]}
    for outcome in modes.values():
        need(outcome['returncode']!=0 and 'RuntimeError: Exact check failed:' in outcome['stderr'],'Mutation escaped: '+name)
    report['mathematical_mutations'].append({'name':name,'old':old,'new':new,'runs':modes})
for label,mode in [('symlink',stat.S_IFLNK),('fifo',stat.S_IFIFO),('socket_mode_synthetic',stat.S_IFSOCK),('character_device',stat.S_IFCHR),('block_device',stat.S_IFBLK)]:
    try:kind(mode|0o600)
    except ValueError:report['inventory_tests'].append({'test':label,'status':'REJECTED','method':'synthetic stat mode; no special object created'})
    else:raise RuntimeError('Special mode accepted')
with tempfile.TemporaryDirectory() as d:
    p=pathlib.Path(d);(p/'a.txt').write_text('ordinary');(p/'nested').mkdir()
    baseline=snapshot(p)
    (p/'nested/socket_mode_only').write_text('not a socket')
    original_stat=os.stat
    def synthetic_socket(path,*args,**kwargs):
        value=original_stat(path,*args,**kwargs)
        if path=='socket_mode_only':
            fields=list(value);fields[0]=stat.S_IFSOCK|0o600
            return os.stat_result(fields)
        return value
    with patch('os.stat',side_effect=synthetic_socket),patch('os.read',side_effect=RuntimeError('Read before synthetic socket rejection')):
        try:snapshot(p)
        except ValueError:report['inventory_tests'].append({'test':'nested_socket_mode_synthetic','status':'REJECTED_BEFORE_READ','method':'mocked stat for ordinary file; no socket created'})
        else:raise RuntimeError('Synthetic nested socket accepted')
    (p/'nested/socket_mode_only').unlink()

    for label,create in [('nested_symlink',lambda:os.symlink('../a.txt',p/'nested/bad')),('nested_fifo',lambda:os.mkfifo(p/'nested/bad'))]:
        create()
        try:
            with patch('os.read',side_effect=RuntimeError('Content read before complete type gate')):
                try:snapshot(p)
                except ValueError:report['inventory_tests'].append({'test':label,'status':'REJECTED_BEFORE_READ'})
                else:raise RuntimeError('Bad entry accepted')
        finally:(p/'nested/bad').unlink()
    (p/'empty').mkdir();need(snapshot(p)!=baseline,'Empty directory not inventoried');(p/'empty').rmdir()
    (p/'extra').write_text('extra');need(snapshot(p)!=baseline,'Extra file not detected');(p/'extra').unlink()
    (p/'a.txt').write_text('tampered');need(snapshot(p)!=baseline,'Changed bytes not detected')
    report['inventory_tests'].append({'test':'empty_directory_extra_file_changed_bytes','status':'DETECTED'})
report['status']='PASS'
print(json.dumps(report,indent=2))
