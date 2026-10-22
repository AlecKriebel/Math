#!/usr/bin/env python3
"""Measure real full-corpus source-only ordering and archival non-access."""
from pathlib import Path
import contextlib
import datetime
import hashlib
import io
import json
import runpy
import sys

HERE=Path(__file__).resolve().parent
AUDIT=HERE.parent
REPOSITORY=HERE.parents[3]
TOOL=AUDIT/'publication_tools_02/portable.py'
PIN='09e4932f66c15916891245a1fb3d6a7052cb5619710d94e0e2305fb7a7612aa6'


def main():
    assert hashlib.sha256(TOOL.read_bytes()).hexdigest()==PIN
    api=runpy.run_path(str(TOOL),run_name='source_only_independent_probe')
    namespace=api['main'].__globals__
    events=[]
    archival_opens=[]
    subprocesses=[]
    source_root=str((AUDIT/'source').resolve())+'/'
    def audit(name,values):
        if name=='subprocess.Popen':
            subprocesses.append(name)
        if name=='open' and isinstance(values[0],(str,bytes)):
            path=Path(values[0]).absolute()
            if str(path).startswith(source_root):
                archival_opens.append(path.name)
    sys.addaudithook(audit)
    original_stream=namespace['stream_pin']
    original_read=namespace['read_regular']
    def streamed(path,*values):
        result=original_stream(path,*values)
        events.append({'event':'whole_pin_completed','name':path.name})
        return result
    def read(path,*values,**kwargs):
        events.append({'event':'read_for_parse','name':path.name})
        return original_read(path,*values,**kwargs)
    def forbidden(*unused,**unused_kw):
        raise AssertionError('Archival helper reached during source-only')
    namespace['stream_pin']=streamed
    namespace['read_regular']=read
    namespace['original_inputs']=forbidden
    namespace['replay']=forbidden
    sys.argv=[str(TOOL),'source-only','--catalog',str(REPOSITORY/'unsolved_math_prioritization/catalog.json'),
              '--problems',str(REPOSITORY/'unsolved_math_prioritization/cache/problems.json'),
              '--reports',str(REPOSITORY/'unsolved_math_prioritization/cache/research_results.json')]
    output=io.StringIO()
    with contextlib.redirect_stdout(output):
        api['isolated']()
        api['main']()
    result=json.loads(output.getvalue())
    names=['catalog.json','problems.json','research_results.json']
    assert events[:3]==[{'event':'whole_pin_completed','name':n} for n in names]
    assert events[3:]==[{'event':'read_for_parse','name':n} for n in names]
    assert not archival_opens and not subprocesses
    receipt={'timestamp_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
             'tool_sha256':PIN,'scope':'Real source-only CLI dispatcher with observational wrappers; complete existing corpora read only.',
             'completion_estimate_percent':60,'source_result':result,'observed_order':events,
             'archival_file_open_events':len(archival_opens),'subprocess_popen_events':len(subprocesses),
             'archival_helpers_forbidden_by_probe':True,
             'corpus_bodies_copied':False,'primary_sources':'NOT_RUN: required BGT filename not present; no source body copied or renamed.'}
    destination=HERE/'SOURCE_ONLY_RECEIPT.json'
    assert not destination.exists()
    destination.write_text(json.dumps(receipt,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':result['status'],'whole_pins_before_first_parse':True,
                      'archival_file_open_events':len(archival_opens),'subprocess_popen_events':len(subprocesses)}))


if __name__=='__main__': main()
