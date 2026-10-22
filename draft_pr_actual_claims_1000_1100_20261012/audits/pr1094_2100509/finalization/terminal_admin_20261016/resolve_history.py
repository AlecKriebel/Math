"""Individually resolve dated stage pins without rewriting any old inventory."""
from pathlib import Path
import datetime, hashlib, json
R=Path(__file__).resolve().parent;A=R.parent.parent;P=A/'preprint_v1_0';K=P/'kit'
def sha(b):return hashlib.sha256(b).hexdigest()
def need(ok,msg):
    if not ok:raise ValueError(msg)
def rec(p,n):
    b=p.read_bytes();return {'path':n,'bytes':len(b),'sha256':sha(b)}
def wj(p,d):p.write_text(json.dumps(d,indent=2,sort_keys=True)+'\n')
def rows(x):
    for k in ('records','entries','members','files'):
        if k in x and isinstance(x[k],list):return x[k]
    raise ValueError('inventory row key absent')
def main():
    baseline=json.loads((R/'FROZEN_INPUT_PINS.json').read_text())['records']
    allowed={r['path'] for r in json.loads((R/'ALLOWED_CHANGES.json').read_text())['existing_edits']}
    indexed={}
    for p in sorted(A.rglob('*')):
        if p.is_file() and not p.is_symlink() and 'scratch' not in p.parts:
            q=rec(p,'');indexed.setdefault((q['bytes'],q['sha256']),[]).append(p)
    def resolve(row,expected):
        size,digest=row['bytes'],row['sha256']
        preferred=[expected,R/'before'/expected.relative_to(A),A/'repairs/package01/before'/expected.relative_to(A)]
        for p in preferred+indexed.get((size,digest),[]):
            if p.is_file() and not p.is_symlink() and rec(p,'')=={'path':'','bytes':size,'sha256':digest}:
                name=p.relative_to(A).as_posix()
                return {'recorded_path':row['path'],'expected_audit_path':expected.relative_to(A).as_posix(),'bytes':size,'sha256':digest,'resolution':name,
                        'meaning':'Exact dated bytes; current successor is not substituted' if p!=expected else 'Unchanged original bytes',
                        'public_selection':'Local-only old ZIP/current binding dependency intentionally omitted from new terminal selection' if p.name.endswith('.zip') or p.name=='DEPOSIT_BINDING.json' else 'Current or previously retained exact authored/input evidence; no new source-body copy'}
        raise ValueError('unresolved dated pin '+str(expected)+' '+digest)
    specs=[('preprint_v1_0/FROZEN_INPUT_PINS.json',A),('preprint_v1_0/OUTPUT_PINS.json',P),
           ('reviews/package_01/INPUT_PINS.json',A),('reviews/package_01/OUTPUT_PINS.json',A/'reviews/package_01'),
           ('repairs/package01/FROZEN_INPUT_PINS.json',A),('repairs/package01/OUTPUT_PINS.json',A/'repairs/package01'),
           ('repairs/package01/CURRENT_ARTIFACT_PINS.json',A),
           ('reviews/package_02/FROZEN_INPUT_PINS.json',A),('reviews/package_02/OUTPUT_PINS.json',A/'reviews/package_02'),
           ('reviews/collar_algebra_01/OUTPUT_PINS.json',A/'reviews/collar_algebra_01'),
           ('reviews/geometry_rigidity_01/OUTPUT_PINS.json',A/'reviews/geometry_rigidity_01'),
           ('reviews/priority_01/OUTPUT_PINS.json',A/'reviews/priority_01')]
    stages=[]
    for n,base in specs:
        data=json.loads((A/n).read_text());rr=rows(data)
        resolved=[resolve(r,base/r['path']) for r in rr]
        stages.append({'inventory':n,'inventory_pin':rec(A/n,n),'count':len(rr),'records':resolved})
    # Re-resolve all 69 nested family paths from their own explicit original
    # locators, hashing bytes directly. No source body is reread as mathematics.
    family=json.loads((A/'reviews/package_02/FAMILY_HISTORY_PATHS.json').read_text())
    nested=[]
    for row in family['rows']:
        p=Path(row['resolution']);p=p if p.is_absolute() else A/p
        need(rec(p,'')=={'path':'','bytes':row['bytes'],'sha256':row['sha256']},'nested family path differs')
        nested.append({'artifact':row['artifact'],'recorded_path':row['recorded_path'],'resolution':str(p),'bytes':row['bytes'],'sha256':row['sha256']})
    need(len(nested)==69,'family nested count')
    # Check the exact 171-stage old partition and every current repair-stage
    # row. Both objects remain unchanged; terminal ledger is separate.
    old=json.loads((A/'repairs/package01/before/preprint_v1_0/kit/CUSTODY_MAP.json').read_text())
    current=json.loads((K/'CUSTODY_MAP.json').read_text())
    need(old['exact_partition_count']==171 and len(old['copies'])==57 and len(old['exclusions'])==114,'old partition')
    need(current['exact_partition_count']==309 and len(current['copies'])==99 and len(current['exclusions'])==210,'repair partition')
    need(current['copies'][:57]==old['copies'] and current['exclusions'][:114]==old['exclusions'],'old partition rows changed')
    bmap={r['path']:r for r in json.loads((A/'repairs/package01/FROZEN_INPUT_PINS.json').read_text())['records']}
    originrows=[]
    for r in current['copies']:
        n=r['original_path'];need(rec(K/r['copy_path'],n)==bmap[n],'selected old copy differs')
        originrows.append({'path':n,'selected_copy':r['copy_path'],'bytes':r['bytes'],'sha256':r['sha256']})
    for r in current['exclusions']:
        n=r['path'];need(all(r[k]==bmap[n][k] for k in ('path','bytes','sha256')),'exclusion differs')
        resolution=resolve(bmap[n],A/n)
        originrows.append({'path':n,'explicit_old_omission':r['reason'],'exact_local_resolution':resolution['resolution'],'bytes':r['bytes'],'sha256':r['sha256']})
    need(len(originrows)==len({r['path'] for r in originrows})==309,'partition not exact')
    inputs=[]
    for r in baseline:
        p=R/'before'/r['path'] if r['path'] in allowed else A/r['path']
        need(rec(p,r['path'])==r,'initial freeze unresolved')
        inputs.append({'path':r['path'],'bytes':r['bytes'],'sha256':r['sha256'],'resolution':p.relative_to(A).as_posix()})
    wj(R/'PRIOR_STAGE_RESOLUTION.json',{'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS','stage_count':len(stages),'stage_rows':sum(s['count'] for s in stages),'stages':stages,'nested_family_paths':nested,'nested_family_count':len(nested),'no_old_inventory_rewritten':True})
    wj(R/'PRESERVED_PARTITIONS.json',{'status':'PASS','original_partition_count':171,'repair_partition_count':309,'original_57_copies_114_exclusions_exact':True,'repair_99_copies_210_exclusions_exact':True,'repair_rows':originrows,'new_terminal_selection_separate_not_a_repartition':True})
    wj(R/'BEFORE_INPUT_RESOLUTION.json',{'status':'PASS','baseline_count':len(inputs),'records':inputs})
    print(json.dumps({'status':'PASS','stage_inventories':len(stages),'stage_rows':sum(s['count'] for s in stages),'nested_family_paths':len(nested),'baseline_inputs':len(inputs),'old_partition_counts':[171,309]},indent=2))
if __name__=='__main__':main()
