"""Owned-folder proposal only. Does not modify receipts or shared pipeline code."""
from copy import deepcopy

def normalized_receipt_view(raw):
    if not isinstance(raw, dict):
        raise ValueError('Receipt must be an object')
    present = [key for key in ('files', 'assets') if key in raw]
    if not present:
        raise ValueError('Receipt has no deposited asset list')
    for key in present:
        if not isinstance(raw[key], list) or not all(isinstance(x, dict) for x in raw[key]):
            raise ValueError('Receipt asset list must contain objects')
    if len(present) == 2 and raw['files'] != raw['assets']:
        raise ValueError('Conflicting files and assets lists')
    result = deepcopy(raw)
    result['files'] = deepcopy(raw[present[0]])
    return result

if __name__ == '__main__':
    from pathlib import Path
    import hashlib, json
    path=Path(__file__).resolve().parents[2]/'sources/receipt.json'
    before=path.read_bytes(); raw=json.loads(before); raw_before=deepcopy(raw)
    view=normalized_receipt_view(raw)
    if view['files'] != raw['assets'] or raw != raw_before:
        raise ValueError('Fresh receipt normalization changed data')
    view['files'][0]['name']='MUTATED_VIEW_ONLY'
    if raw != raw_before or path.read_bytes()!=before:
        raise ValueError('View mutation affected the original')
    rejected=0
    for bad in ({}, {'assets':None}, {'assets':['bad']}, {'files':[],'assets':[{'name':'a'}]}):
        try: normalized_receipt_view(bad)
        except ValueError: rejected += 1
        else: raise ValueError('Invalid receipt accepted')
    if normalized_receipt_view({'files':[{'name':'a'}]})['files'] != [{'name':'a'}]:
        raise ValueError('Existing files format changed')
    if normalized_receipt_view({'files':[],'assets':[]})['files'] != []:
        raise ValueError('Identical simultaneous lists rejected')
    print(json.dumps({'read_only_proposal_contract':'PASS','negative_controls_rejected':rejected,
      'frozen_receipt_unchanged':path.read_bytes()==before,
      'raw_receipt_sha256':hashlib.sha256(before).hexdigest(),
      'shared_pipeline_modified':False}))
