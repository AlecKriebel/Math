"""Verify the actual PR18 append and a fresh full-table uniqueness readback."""
from pathlib import Path
import datetime as dt
import hashlib
import importlib.util
import json
import os
import shutil

own=Path(__file__).resolve().parent
a18=own.parent
program=a18.parents[1]
repo=program.parent
source=program/'infrastructure/append_publication.py'
spec=importlib.util.spec_from_file_location('pr18_tracker',source)
module=importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
capture=program/'audits/pr45_9900007/root_pr18_tracker_authorized_append_and_readback_actual_capture'
result=json.loads((capture/'stdout.bin').read_bytes())
if result['state']!='appended_verified' or result['append_performed'] is not True:
    raise RuntimeError('Actual append/readback has not passed')
attempt=Path(result['receipt_dir'])
private=a18/'publication/tracker_private'
if attempt.parent!=private:
    raise RuntimeError('Unexpected recovery receipt root')
request=json.loads((attempt/'request.json').read_bytes())
response=json.loads((attempt/'response.json').read_bytes())
readback=json.loads((attempt/'readback.json').read_bytes())
intent=json.loads((a18/'publication/INTENDED_TRACKER_ROW.json').read_bytes())
expected=intent['intended_values'].copy()
expected[2]='https://doi.org/'+expected[2]
if request['body']['values']!=[expected] or readback['values']!=[expected] or result['range']!="'Math Puzzles'!A14:D14":
    raise RuntimeError('Actual four-cell row differs from prepared intent or actual observed range')
stamp=dt.datetime.now(dt.timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
post=private/('post-readback-'+stamp)
module.durable_mkdir(post)
gws=shutil.which('gws')
if not gws:
    raise RuntimeError('Google Workspace CLI missing')
title=module.resolve_tab(gws,post)
rows=module.read_table(gws,post,title,'full-table-postappend')
match=module.duplicate_row(rows,set(request['problem_keys']),request['doi_key'])
if match!=(14,expected):
    raise RuntimeError('Fresh table does not contain exactly one correct PR18 row at the observed range')
sha=lambda body:hashlib.sha256(body).hexdigest()
record={'schema':'pr18-actual-tracker-verification/v1','UTC':dt.datetime.now(dt.timezone.utc).isoformat(),
    'actual_author_pid':os.getpid(),'spreadsheet_id':module.SPREADSHEET_ID,'sheet_id':module.SHEET_ID,
    'resolved_tab':title,'range':result['range'],'DOI':request['doi_key'],
    'append_performed':True,'append_response_exactly_one_row_four_cells':True,
    'actual_row':expected,'independent_readback_exact':True,
    'fresh_full_table_exactly_one_matching_problem_DOI_row':True,
    'headers_matched_live':module.HEADERS,'private_full_table_receipts':post.relative_to(repo).as_posix(),
    'authorized_append_receipts':attempt.relative_to(repo).as_posix(),
    'request_sha256':sha((attempt/'request.json').read_bytes()),
    'append_response_sha256':sha((attempt/'response.json').read_bytes()),
    'independent_readback_sha256':sha((attempt/'readback.json').read_bytes()),
    'actual_parent_capture_sha256':sha((capture/'CAPTURE.json').read_bytes()),
    'helper_source_sha256':sha(source.read_bytes()),'new_central_attempts':0,'PR18_workflow_percent':100}
for src,dest in [('request.json','TRACKER_REQUEST.json'),('response.json','TRACKER_APPEND_RESPONSE.json'),('readback.json','TRACKER_READBACK.json')]:
    path=a18/'publication'/dest
    if path.exists():
        raise RuntimeError('Do not replace existing public own-row receipts')
    path.write_bytes((attempt/src).read_bytes())
path=a18/'publication/TRACKER_VERIFICATION.json'
if path.exists():
    raise RuntimeError('Do not overwrite existing tracker verification')
path.write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(record,ensure_ascii=False,indent=2))
