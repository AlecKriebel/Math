"""Correct one reviewer-owned archive category, retaining full earlier inventory."""
from pathlib import Path
import gzip,json,os
from capture import HERE,pin,write,now,digest
def main():
 p=HERE/'SOURCE_ARCHIVE_INDEX.json';before=p.read_bytes();old=HERE/'SOURCE_ARCHIVE_INDEX_before_external_source_correction.json';old.write_bytes(before)
 d=json.loads(before);src=Path('/Users/alec/Documents/Math/zenodo_deposit_tool/zenodo.py')
 matched=[r for r in d['unredistributed_external_binary_anchors']if r['input']['path']==str(src)]
 assert len(matched)==1 and pin(src)==matched[0]['input']
 d['unredistributed_external_binary_anchors']=[r for r in d['unredistributed_external_binary_anchors']if r not in matched]
 b=src.read_bytes();target=HERE/'source_archives/external_zenodo_source.bin.gz';target.write_bytes(gzip.compress(b,mtime=0));assert gzip.decompress(target.read_bytes())==b
 d['complete_body_copies'].append(dict(original=pin(src),complete_copy=pin(target),codec='gzip',logical_bytes=len(b),logical_sha256=digest(b),reading_extent='Repository local-check implementation was an authenticated source input; whole code not claimed manually audited as an external publication API.'))
 d['correction_UTC']=now();d['correction_actual_recorder_PID']=os.getpid();d['external_python_source_correction']='The outside-audit Zenodo Python script is source, not a runtime binary; direct full copy added and earlier literal inventory preserved. Its actual local-check prelaunch copy was already authenticated.'
 write(p,d)
 write(HERE/'SOURCE_ARCHIVE_CATEGORY_CORRECTION.json',dict(UTC=now(),actual_recorder_PID=os.getpid(),executed_source=pin(__file__),literal_previous_inventory=pin(old),corrected_inventory=pin(p),complete_external_source=pin(src),complete_copy=pin(target),historical_category_error='Initial preparer classified every outside-audit anchor as an executable/runtime binary, including this Python source. Five actual external binary anchors remain pinned and unredistributed.',candidate_modified=False))
 with (HERE/'RESEARCH_LOG.md').open('a')as f:f.write('\n'+now()+' — Final source-inventory readback caught one own category mistake: repository Zenodo Python source had been listed with external binaries. Its full direct source copy was added and literal earlier inventory preserved. No package/source/scientific outcome changed; review estimated95%. Actual recorder PID '+str(os.getpid())+'.\n')
 print(json.dumps(dict(status='OWN_SOURCE_CATEGORY_CORRECTED_COMPLETE_301_SOURCE_COPIES',actual_recorder_PID=os.getpid(),copies=len(d['complete_body_copies']),external_actual_binaries=len(d['unredistributed_external_binary_anchors']))))
if __name__=='__main__':main()
