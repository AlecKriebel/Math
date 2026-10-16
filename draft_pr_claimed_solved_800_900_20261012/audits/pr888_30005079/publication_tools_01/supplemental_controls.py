"""Additional current-layout and before-replay controls, using private fixtures."""
from pathlib import Path
from types import SimpleNamespace
import datetime,importlib.util,json,tempfile

HERE=Path(__file__).absolute().parent
spec=importlib.util.spec_from_file_location('portable',HERE/'portable.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
results=[]

def rejected(label,call):
    try: call()
    except (ValueError,OSError) as exc: results.append({'control':label,'status':'REJECTED_AS_REQUIRED','reason':str(exc)})
    else: raise RuntimeError('accepted control: '+label)

def main():
    fixture=HERE/'private_tmp/fixture'; current=HERE/'private_tmp/current'
    original={p.relative_to(current).as_posix():p.read_bytes() for p in current.rglob('*') if p.is_file()}
    def mutate(label,name,raw):
        blobs=dict(original);blobs[name]=raw
        index=m.strict_json(blobs['CURRENT_PUBLICATION_MANIFEST.json'])
        for row in index['files']: row.update(m.pin_bytes(blobs[row['path']]))
        indexraw=(json.dumps(index,indent=2,sort_keys=True)+'\n').encode();blobs['CURRENT_PUBLICATION_MANIFEST.json']=indexraw
        with tempfile.TemporaryDirectory(prefix='current-control-',dir=HERE/'private_tmp') as td:
            root=Path(td)/'packet';m.materialize(root,blobs)
            rejected(label,lambda:m.current_inputs(root,m.sha(indexraw)))
    mutate('actual_outer_inner_TeX_copy_drift','note.tex',b'Changed outer TeX.\n')
    meta=m.strict_json(original['metadata.json']);meta['description']='Changed outer description.'
    mutate('actual_outer_inner_metadata_copy_drift','metadata.json',json.dumps(meta).encode())
    mutate('actual_outer_inner_deposit_copy_drift','zenodo-deposit.json',original['zenodo-deposit.json']+b' ')
    mutate('actual_outer_inner_tool_copy_drift','portable.py',original['portable.py']+b'\n')
    mutate('current_actual_PDF_header_rejection','rank-two-fano-note.pdf',b'not a PDF')
    mutate('current_ZIP_trailer_rejection','rank-two-fano-verification.zip',original['rank-two-fano-verification.zip']+b'x')
    layout=m.strict_json(original['CURRENT_PUBLICATION.json']);layout['portable_prefix']='changed'
    mutate('current_layout_prefix_drift','CURRENT_PUBLICATION.json',json.dumps(layout).encode())
    blobs={p.relative_to(fixture).as_posix():p.read_bytes() for p in fixture.rglob('*') if p.is_file()}
    saved_verify=m.verify_result;saved_temp=m.tempfile.TemporaryDirectory
    def forbidden(*args,**kwargs): raise AssertionError('ARCHIVAL_REPLAY_OR_TEMP_CREATION_OCCURRED')
    m.verify_result=forbidden;m.tempfile.TemporaryDirectory=forbidden
    try:
        for label,out in [('nested_output_rejected_before_replay_and_temp',fixture/'source/checks/rank-two-fano-verification.zip'),('existing_output_rejected_before_replay_and_temp',HERE/'private_tmp/build/rank-two-fano-verification.zip')]:
            args=SimpleNamespace(root=fixture,output=out,dependency_dir=None,primary_dir=None)
            rejected(label,lambda args=args:m.build_output(blobs,m.sha(blobs['package_index.json']),args))
    finally: m.verify_result=saved_verify;m.tempfile.TemporaryDirectory=saved_temp
    # An actual symlinked output parent must fail before any output creation.
    with tempfile.TemporaryDirectory(prefix='output-symlink-control-',dir=HERE/'private_tmp') as td:
        root=Path(td);(root/'target').mkdir();(root/'alias').symlink_to(root/'target',target_is_directory=True)
        rejected('symlink_output_parent',lambda:m.output_preflight(fixture,blobs,root/'alias/rank-two-fano-verification.zip'))
    # This instrumentation establishes order, complementing the real complete
    # three-corpus authentication recorded in SOURCE_ONLY_RECEIPT.json.
    pins=[];saved_stream=m.stream_pin;saved_read=m.read_regular
    def pin(path,size,digest): pins.append((size,digest))
    def read(*args,**kwargs):
        if len(pins)!=3: raise AssertionError('TARGET_READ_BEFORE_ALL_THREE_PIN_CALLS')
        raise ValueError('ALL_THREE_COMPLETE_PIN_CALLS_PRECEDE_FIRST_PARSE_OR_EXTRACTION')
    m.stream_pin=pin;m.read_regular=read
    try: rejected('source_only_all_three_pins_before_first_record_read',lambda:m.source_only([Path('a'),Path('b'),Path('c')]))
    finally: m.stream_pin=saved_stream;m.read_regular=saved_read
    receipt={'timestamp_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'completion_estimate_percent':90,'actual_subprocess_count':0,'scope':'In-process current-layout and ordering controls; final parent paper PDF is not validated by these fixtures.','results':results}
    (HERE/'SUPPLEMENTAL_CONTROL_RECEIPT.json').write_text(json.dumps(receipt,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'PASS','controls':len(results)}))

if __name__=='__main__': main()
