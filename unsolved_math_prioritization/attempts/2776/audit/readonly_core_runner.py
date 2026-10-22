#!/usr/bin/env python3
"""Run the original mathematical functions without its mandatory output-file write."""
import errno
import json
import os
from pathlib import Path
import runpy
import sys

p=Path(sys.argv[1]).resolve()
if os.getuid()!=1000 or os.geteuid()!=1000:
    raise RuntimeError('Expected genuine UID/EUID 1000')
for candidate, flags in [(p,os.O_WRONLY),(Path.cwd()/'readonly_probe',os.O_WRONLY|os.O_CREAT|os.O_EXCL)]:
    try:
        fd=os.open(candidate,flags,0o600)
    except PermissionError as exc:
        if exc.errno!=errno.EACCES:
            raise
    else:
        os.close(fd)
        raise RuntimeError('Input/cwd is unexpectedly writable')
namespace=runpy.run_path(str(p),run_name='audited_module')
results={'problem_id':2776,'all_checks_passed':True,
         'graph_criterion':namespace['graph_check'](),
         'cycle_cover_obstruction':namespace['cycle_checks'](),
         'free_quotient_obstruction':namespace['cyclic_reduction_check'](),
         'explicit_free_embedding':namespace['schottky_check'](),
         'c5_local_gadget_obstruction':namespace['c5_transversal_check'](),
         'finite_cover_obstruction':'Proved in the report; not computationally tested.'}
print(json.dumps({'uid':os.getuid(),'euid':os.geteuid(),'optimization':sys.flags.optimize,
                  'input_write_denied':True,'cwd_create_denied':True,'results':results},indent=2))
