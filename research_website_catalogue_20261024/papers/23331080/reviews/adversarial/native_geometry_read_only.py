#!/usr/bin/env python3
"""Execute only the native geometry math program with its sole output in RAM."""
from pathlib import Path
import contextlib, io, json, sys
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent
program=HERE/'cache/replay/geometry/verify_independent.py'
target=program.with_name('verification_results.json')
raw=program.read_text(); writes=[]; captured=io.StringIO()
original=Path.write_text
def memory_write(path,data,*args,**kwargs):
    if path.resolve()!=target.resolve():raise RuntimeError('unexpected native write intent '+str(path))
    writes.append({'target_name':path.name,'content':data})
    return len(data)
try:
    Path.write_text=memory_write
    with contextlib.redirect_stdout(captured):
        exec(compile(raw,str(program),'exec'),{'__name__':'__main__','__file__':str(program)})
finally:
    Path.write_text=original
if len(writes)!=1:raise RuntimeError('expected exactly one native mathematical output intent')
if program.read_text()!=raw:raise RuntimeError('native program changed')
if writes[0]['content']!=target.read_text():raise RuntimeError('memory-only replay differs from retained actual isolated output')
print(json.dumps({'assessment':'NATIVE_GEOMETRY_MATHEMATICS_REPLAYED_WITH_ONLY_OUTPUT_CAPTURED_IN_MEMORY',
 'literal_stdout':captured.getvalue(),'captured_write_intents':writes,
 'actual_files_written':0,'native_program_bytes_modified':False},indent=2,sort_keys=True))
