#!/usr/bin/env python3
"""Pure validation-to-hash receipt race, with no service or Git dispatch."""
import datetime,hashlib,json,pathlib,sys,tempfile
from unittest.mock import patch
sys.dont_write_bytecode=True
OUT=pathlib.Path(__file__).resolve().parent;AUDIT=OUT.parents[2]
fixture=AUDIT/'reviews/operations_01/check_helpers.py'
ns={'__name__':'receipt_binding_fixture','__file__':str(fixture)}
exec(compile(fixture.read_bytes(),str(fixture),'exec'),ns)
p=ns['p'];results=[]
for change_receipt in ['publication','inspection']:
    with tempfile.TemporaryDirectory(dir=OUT,prefix='receipt-binding-') as td:
        root=pathlib.Path(td)
        for name,data in ns['PUB'].items():(root/name).write_bytes(data)
        (root/'CURRENT_PRIORITY_AND_STATUS.md').write_bytes(ns['SOURCE'])
        rp=root/'publication-receipt.json';ip=root/'inspection-receipt.json'
        initial=ns['receipt']()
        for path in [rp,ip]:path.write_bytes(p.json_bytes(initial))
        target=rp if change_receipt=='publication' else ip
        initial_bytes=target.read_bytes();invalid=p.json_bytes(initial|{'title':'INVALID CHANGED RECEIPT'})
        real=p.regular_bytes;counts={}
        def regular(path):
            counts[path]=counts.get(path,0)+1
            if path==target and counts[path]==2:target.write_bytes(invalid)
            return real(path)
        with patch.object(p,'regular_bytes',side_effect=regular):
            _,validation=p.publication_inputs(root,ns['DOI'],rp,ip,original=ns['ORIGINAL'])
        key='publication_receipt_sha256' if change_receipt=='publication' else 'inspection_receipt_sha256'
        p.require(validation[key]==p.sha(invalid),'not hashed changed bytes')
        p.require(validation[key]!=p.sha(initial_bytes),'receipt did not change')
        try:p.publication_inputs(root,ns['DOI'],rp,ip,original=ns['ORIGINAL'])
        except ValueError as exc:p.require('not confirmed production publication' in str(exc),'wrong negative control');fresh='REJECTED'
        else:raise ValueError('fresh invalid receipt unexpectedly accepted')
        results.append({'changed_receipt':change_receipt,'race_outcome':'ACCEPTED_UNVALIDATED_HASH',
                        'validated_initial_receipt_sha256':p.sha(initial_bytes),
                        'returned_receipt_sha256':validation[key],
                        'returned_hash_binds_invalid_title':True,'fresh_invalid_receipt_outcome':fresh,
                        'target_read_count':counts[target]})
obj={'captured_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'python_optimization':sys.flags.optimize,
     'results':results,'remote_mutations':0,'git_mutations':0,'writes_outside_review_folder':0}
(OUT/('RECEIPT_BINDING_O'+str(sys.flags.optimize)+'_RESULTS.json')).write_text(json.dumps(obj,indent=2)+'\n')
with (OUT/'RESEARCH_LOG.md').open('a') as log:
    log.write('\n'+obj['captured_utc']+' — Additional mandatory P2 receipt-binding race confirmed for both publication and inspection receipt: original receipt validates, second read supplies wrong-title bytes for returned hash, fresh validation of changed bytes rejects. Python optimization '+str(sys.flags.optimize)+'. Review completion estimate: 100%; readiness estimate: 90%, same immutable-read repair family.\n')
print(json.dumps(obj,indent=2))
