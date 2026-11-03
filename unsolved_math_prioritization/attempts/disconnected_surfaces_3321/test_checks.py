"""Reproducible semantic mutations and pre-read inventory rejection tests. No sockets."""
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).absolute().parent
spec = importlib.util.spec_from_file_location('frozen_verify', ROOT/'verify.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

def run():
    source = (ROOT/'check_lattice.py').read_text()
    mutations = {
        'change_vector_geometry': ('u,v=(1,2),(2,-1)', 'u,v=(1,2),(2,1)'),
        'remove_repeated_vector': ('X=[u,u,v]', 'X=[u,v]'),
        'replace_determinant_by_symmetric_form': ('x[0]*y[1]-x[1]*y[0]', 'x[0]*y[1]+x[1]*y[0]'),
        'drop_second_coordinate_in_row_norm': ('row[0]*x+row[1]*y', 'row[0]*x'),
        'admit_dependent_matrix_rows': ('abs(det(r,s))==1', 'abs(det(r,s))<=1'),
    }
    result = {'semantic_mutations':[], 'inventory_rejections':[], 'no_socket_creation':True}
    with tempfile.TemporaryDirectory() as temp:
        temp = Path(temp)
        for name,(old,new) in mutations.items():
            if source.count(old) != 1:
                raise RuntimeError('ambiguous mutation anchor')
            script = temp/(name+'.py')
            script.write_text(source.replace(old,new))
            for flags in ([],['-O']):
                p = subprocess.run([sys.executable,*flags,'-B',str(script)],capture_output=True,text=True,timeout=30)
                if p.returncode == 0 or 'RuntimeError' not in p.stderr:
                    raise RuntimeError('mutation was not killed: '+name)
                result['semantic_mutations'].append({'name':name,'mode':'optimized' if flags else 'normal','killed':True,'failure':p.stderr.strip().splitlines()[-1]})
        for kind in ('symlink','fifo','directory'):
            target=temp/kind
            target.mkdir()
            (target/'ordinary.txt').write_text('not read by inventory')
            entry=target/'unexpected'
            if kind=='symlink': entry.symlink_to(target/'ordinary.txt')
            elif kind=='fifo': os.mkfifo(entry)
            else: entry.mkdir()
            # Any attempted payload read fails independently of type detection.
            original=Path.read_bytes
            def forbidden_read(*args,**kwargs):
                raise AssertionError('inventory attempted payload read')
            Path.read_bytes=forbidden_read
            try:
                try: module.inventory(target)
                except RuntimeError as error:
                    result['inventory_rejections'].append({'kind':kind,'rejected_before_reads':True,'reason':'unexpected directory' if kind=='directory' else 'nonregular entry'})
                else: raise RuntimeError('unsafe inventory accepted')
            finally: Path.read_bytes=original
    result['status']='PASS'
    return result

if __name__=='__main__':
    print(json.dumps(run(),indent=2))
