#!/usr/bin/env python3
"""Reproduce unresolved resolver-reference gap in the exact complete helper.

These are lexical conservative-review leads, not a claim that any fabricated
suffix resolves or that a resolver reference is HTTP-equivalent to the target.
"""
import importlib.util
import json
from pathlib import Path
import sys

HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('independent_offline_review04',HERE/'offline_whole_helper.py')
review=importlib.util.module_from_spec(spec)
spec.loader.exec_module(review)
results=[]
for alias in ['//shortdoi.org/abc','//doi.org/abc','shortdoi.org/abc','doi.org/abc']:
    for column in range(4):
        results.append(review.case_run({'name':'ledger_column_'+str(column)+'_'+alias,
            'cfg':{'edit_rows':lambda rows,c=column,v=alias:rows.append(['' if i!=c else v for i in range(4)])},
            'expect':'reject','appends':0}))
    results.append(review.case_run({'name':'owned_account_metadata_'+alias,
        'cfg':{'edit_account':lambda rows,v=alias:rows[1]['metadata'].__setitem__('related_identifier',v)},
        'expect':'reject','appends':0}))
for alias in ['https://shortdoi.org/abc','https://doi.org/abc']:
    results.append(review.case_run({'name':'positive_full_url_block_control_'+alias,
        'cfg':{'edit_rows':lambda rows,v=alias:rows.append(['',v,'',''])},'expect':'reject','appends':0}))
after={p:{'bytes':len(Path(p).read_bytes()),'sha256':review.PIN(Path(p).read_bytes())} for p in review.ORIGINAL_PINS}
receipt={'schema':1,'mode':sys.flags.optimize,'helper_sha256':review.PIN(review.SOURCES[str(review.HELPER)]),
         'plan_sha256':review.PIN(review.PLAN_BYTES),'originals_unchanged':after==review.ORIGINAL_PINS,
         'real_service_attempts':review.DENIED,'offline_only':True,'cases':len(results),
         'unexpected_verified_simulated_appends':sum(r['error'] is None and r['state']['append']==1 for r in results),
         'full_url_positive_controls_blocked':all(r['passed'] for r in results if r['case'].startswith('positive_')),
         'results':results,'interpretation':'Unresolved bare/domain-relative short resolver references escape the conservative alias gate. No asserted resolver equivalence, actual duplicate, or network request.'}
review.json_write(HERE/('ALIAS_BOUNDARY_MODE_'+str(sys.flags.optimize)+'.json'),receipt)
print(json.dumps({k:receipt[k] for k in ['mode','cases','unexpected_verified_simulated_appends','full_url_positive_controls_blocked','originals_unchanged','real_service_attempts']},indent=2))
