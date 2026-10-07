"""Demonstrate the documented cwd boundary without performing recursive copying."""
from pathlib import Path
import json,runpy,sys,os
from unittest.mock import patch
project=Path(__file__).resolve().parents[1]
root=project/'publication/zenodo-upload-kit/source-and-verification'
observed={}
def intercept(src,dst,*args,**kwargs):
    src=Path(src).resolve();dst=Path(dst).resolve()
    observed.update(source=str(src),destination=str(dst),destination_inside_source=dst.is_relative_to(src))
    raise RuntimeError('COPY_INTERCEPTED_BEFORE_DISK_RECURSION')
old=os.getcwd();old_argv=sys.argv[:]
try:
    os.chdir(root);sys.argv=[str(root/'reproduce.py'),'--output','reproduction-receipt.json']
    with patch('shutil.copytree',intercept):
        try:runpy.run_path(str(root/'reproduce.py'),run_name='__main__')
        except RuntimeError as e:assert str(e)=='COPY_INTERCEPTED_BEFORE_DISK_RECURSION'
finally:
    os.chdir(old);sys.argv=old_argv
assert observed['destination_inside_source']
(project/'reviews/reproducer_boundary_v2.json').write_text(json.dumps({'bug_confirmed':True,'safe_interception':observed,'original_payload_unmodified':True},indent=2)+'\n')
print('Documented cwd boundary bug confirmed safely; no recursive copy performed.')
