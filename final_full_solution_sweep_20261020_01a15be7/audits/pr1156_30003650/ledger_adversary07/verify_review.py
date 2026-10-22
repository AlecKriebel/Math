#!/usr/bin/env python3
"""Verify closed review artifacts and evidence, never contact services or mutate."""
import hashlib,json
from pathlib import Path
HERE=Path(__file__).resolve().parent

def require(value,message):
    if not value:raise RuntimeError(message)

def sha(data):return hashlib.sha256(data).hexdigest()

def verify_entries(entries,root):
    names=[]
    for e in entries:
        name=e['path'];p=root/name
        require(not Path(name).is_absolute() and '..' not in Path(name).parts,'Unsafe entry path')
        require(not p.is_symlink() and p.resolve().is_relative_to(root.resolve()),'Unsafe bound file')
        b=p.read_bytes();require(len(b)==e['bytes'] and sha(b)==e['sha256'],'Bound file mismatch: '+name);names.append(name)
    require(len(names)==len(set(names)),'Duplicate manifest path')
    return set(names)

def main():
    data=(HERE/'MANIFEST.json').read_bytes();m=json.loads(data)
    require((HERE/'MANIFEST.sha256').read_text().split()[0]==sha(data),'Manifest seal mismatch')
    listed=verify_entries(m['files'],HERE)
    actual={str(p.relative_to(HERE)) for p in HERE.rglob('*') if p.is_file() and not ({'private','__pycache__'}&set(p.relative_to(HERE).parts)) and p.name not in {'MANIFEST.json','MANIFEST.sha256'}}
    require(listed==actual,'Public manifest not closed')
    private=json.loads((HERE/'PRIVATE_SNAPSHOT_MANIFEST.json').read_text());names=verify_entries(private['files'],HERE)
    require(names=={str(p.relative_to(HERE)) for p in (HERE/'private').rglob('*') if p.is_file()},'Private snapshot manifest not closed')
    for e in json.loads((HERE/'SOURCE_PINS.json').read_text())['files']:
        for p in [Path(e['original']),HERE/e['snapshot']]:
            b=p.read_bytes();require(len(b)==e['bytes'] and sha(b)==e['sha256'],'Source pin mismatch: '+str(p))
    target=HERE.parent
    require(sha((target/'reconcile_external_ledger_v7.py').read_bytes())=='f0ea77020bddab4ad518a819004434a654eda9c247a7c9e507226825e274c27f','Exact reviewed v7 changed')
    require(sha((target/'LEDGER_RECONCILIATION_PLAN.json').read_bytes())=='83df78463704c63ea3969a87325f18ab21c21893d6e1b8b49c5b16a6b4e3b2e1','Immutable plan changed')
    for n in ['ROOT_LEDGER_REVIEW07_ACCEPTANCE.json','LEDGER_RECONCILIATION_INTENT.json','LEDGER_RECONCILIATION_RESPONSE.json','LEDGER_PUBLICATION_VERIFICATION.json']:
        require(not (target/n).exists(),'Unapproved real operation artifact exists: '+n)
    prior=json.loads((target/'ledger_adversary06/RESULTS_NORMAL.json').read_text());modes=[]
    for i,name in enumerate(['RESULTS_NORMAL.json','RESULTS_OPTIMIZED.json','RESULTS_DOCSTRINGS_REMOVED.json']):
        main=json.loads((HERE/name).read_text());q=json.loads((HERE/('QUERY_BOUNDARY_MODE_'+str(i)+'.json')).read_text());s=json.loads((HERE/('SERIALIZATION_MODE_'+str(i)+'.json')).read_text());minimal=json.loads((HERE/('MINIMAL_MODE_'+str(i)+'.json')).read_text())
        require(len(main['results'])==600 and q['case_count']==50 and s['case_count']==21,'Incomplete matrices')
        require([r['case'] for r in main['results'][:371]]==[r['case'] for r in prior['results']],'Prior371 controls changed')
        require(all(r['passed'] for r in main['results'][:371]),'Prior regression failed')
        require(main['originals_unchanged'] and not main['denied_real_service_attempts'] and not q['denied_actual_services'] and not s['denied_actual_services'] and not minimal['denied_actual_services'],'Actual service attempt or changed originals')
        allr=main['results']+q['results']+s['results'];bad=[r for r in allr if not r['passed']]
        require(len(allr)==671 and len(bad)==82,'Outcome count changed')
        require(all(r['error'] is None and r['state']['append']==1 and r['receipt_saved'] for r in bad),'Unexpected failure mechanism')
        require(not any(r.get('unexpected_service_paths') or (r['error'] and 'Errno 28' in r['error']) for r in allr),'Unexpected boundary or infrastructure error')
        positive=next(r for r in main['results'] if r['case']=='v7_actual197_native_account_and_actual181_ledger')
        require(positive['passed'] and positive['state']['account_gets']==197 and positive['state']['append']==1 and positive['simulated_ledger_rows']==182,'Native197 positive failed')
        require(len(minimal['results'])==5 and sum(r['passed'] for r in minimal['results'])==1,'Minimal reproductions incomplete')
        modes.append([(r['case'],r['passed'],r['expected'],r['state']) for r in main['results']])
    require(modes[0]==modes[1]==modes[2],'Optimization mode outcomes differ')
    summary=json.loads((HERE/'VALIDATION_SUMMARY.json').read_text());require(summary['total_primary_executions']==2013 and summary['unsafe_verified_appends']==246,'Summary differs')
    verdict=json.loads((HERE/'VERDICT.json').read_text());require(verdict['ready_for_existing_publication_record'] is False and len(verdict['material_findings'])==3,'Unsafe verdict changed')
    print(json.dumps({'review_artifact_verification':True,'public_files':len(actual),'private_files':len(names),'primary_executions':2013,'prior_regressions_passed':1113,'unsafe_mock_appends':246,'verdict':'NOT_READY_FOR_LIVE_EXECUTION'},indent=2))

if __name__=='__main__':main()
