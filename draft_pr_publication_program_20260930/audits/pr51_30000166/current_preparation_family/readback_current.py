"""Handwritten read-only SOURCE checks. Never imports/compiles/executes submitted helpers."""
import datetime
import hashlib
import json
from pathlib import Path
import stat

F=Path(__file__).resolve().parent
O=F.parent/'original_preparation_family'
checks=0


def require(x):
    global checks
    assert x
    checks+=1


def pairs(ps):
    d={}
    for k,v in ps:require(k not in d);d[k]=v
    return d


def read(p):return json.loads(p.read_bytes(),object_pairs_hook=pairs)


def typed(a,b):
    require(type(a) is type(b))
    if isinstance(a,dict):
        require(a.keys()==b.keys())
        for k in a:typed(a[k],b[k])
    elif isinstance(a,list):
        require(len(a)==len(b))
        for x,y in zip(a,b):typed(x,y)
    else:require(a==b)


def bind(q):
    p=Path(q['path']);s=p.lstat();b=p.read_bytes()
    require(stat.S_ISREG(s.st_mode) and s.st_nlink==1)
    require(len(b)==q['bytes'] and hashlib.sha256(b).hexdigest()==q['sha256'])
    if 'full_mode' in q:require(format(stat.S_IMODE(s.st_mode),'04o')==q['full_mode'])


def main():
    require(not (F/'SELF_MANIFEST.json').exists())
    index=read(F/'CURRENT_SCIENCE_INDEX.json')
    require(index['science_files_count']==31 and len(index['rows'])==31)
    require(index['original_head']=='8006dd5f134ad0a2fa930e7278d3cb17945f4201' and index['future_authority'] is False)
    for q in index['rows']:bind(q);require(q['full_mode']=='0444')
    original=read(O/'SNAPSHOT_IDENTITY.json');unchanged=0;parsed=0
    replacements={'README.md','SOURCE_STATUS.md','PR_DRAFT.md','RESEARCH_LOG.md','provenance.json','independent_review/REVIEW.md'}
    for q in original['files']:
        r=q['snapshot_relative_path'];b=(O/'source_snapshot'/r).read_bytes();archive=F/'original_head_archive'/r
        require(archive.read_bytes()==b and hashlib.sha256(b).hexdigest()==q['sha256'])
        require(hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==q['git_blob_sha1'] and q['git_mode']=='100644')
        if r.endswith('.json'):typed(read(archive),read(O/'source_snapshot'/r));parsed+=1
        if r not in replacements:
            current=F/'current_science'/r;require(current.read_bytes()==b);unchanged+=1
            if r.endswith('.json'):typed(read(current),read(archive))
    require(parsed==8 and unchanged==9)
    source=(F/'current_science/SOURCE_STATUS.md').read_text();old=(O/'source_snapshot/SOURCE_STATUS.md').read_text()
    require(source[source.index('## 3.'):source.index('## 5.')]==old[old.index('## 3.'):old.index('## 5.')])
    require('A_N=\\frac{N\\varphi(N)-\\sum_{d\\mid N}d\\mu(d)}{24}' in source)
    for literal in ('A_2=1/8','A_3=1/3','A_6=5/12','no separately supplied source-verification response count','not a new independent family','324,186','140,708'):
        require(literal in source)
    require('Direct inspection of the PDF confirms' not in source)
    globalq=read(F/'current_science/GLOBAL_QUALIFICATIONS.json')
    for k in ('native_authority','root_acceptance_authority','git_authority','merge_authority','publication_authority','new_paper','new_DOI'):require(globalq[k] is False)
    for r,key in (('source_record.json',30000166),('duplicate_source_record.json',30000167)):
        q=read(F/'current_science'/r);require(type(q['id']) is int and q['id']==key and 'prior_report' not in q)
    ledger=read(F/'current_science/turns.json')
    require(type(ledger) is dict and ledger['substantive_proof_attempts']==0 and ledger['budget']==5 and len(ledger['events'])==2)
    require(not any(p.name=='prior_report.json' for p in F.rglob('*')))
    external=read(F/'EXTERNAL_BINDINGS.json');rows=[]
    for group in external['closed_inputs']+external['actual_root_capture_references']:
        for q in group['rows']:bind(q);rows.append(q)
        for q in group.get('directories',[]):require(format(stat.S_IMODE(Path(q['path']).stat().st_mode),'04o')==q['full_mode'])
    require(len(rows)==273==external['rows_count'] and len({q['path'] for q in rows})==273)
    require(external['future_authority'] is False and len(external['actual_root_capture_references'])==6)
    for name,n,status_key,status in [('eta_algebra_adversary_family',324186,'status','PASS_ALREADY_SOLVED_EXACT_ETA_PRODUCT'),('modular_geometry_adversary_family',140708,'verdict','PASS_ALREADY_SOLVED_EXACT_SOURCE_MATCH')]:
        root=F.parent/name;v=read(root/'VERDICT.json')
        require(v[status_key]==status and v['mandatory_corrections']==[] and v['recommended_status']=='already_solved')
        result=read(root/('independent_results.json' if name.startswith('eta') else 'captures/geometry_exact_v2/STDOUT.bin'))
        require(result['assertions']==n and result['status']=='PASS')
        categories=result['by_family'] if name.startswith('eta') else result['assertions_by_family']
        require(sum(categories.values())==n)
    cap=F/'captures/text_builder';p=read(cap/'PRELAUNCH.json');s=read(cap/'STARTED.json');c=read(cap/'COMPLETE.json')
    require(p['schema']=='pr51-current-private-command-prelaunch/v1' and c['schema']=='pr51-current-private-command-completed/v1')
    require(p['child_pid'] is None and c['child_pid']==s['child_pid']==70580 and c['completed'] is True and c['exit_code']==0)
    require(p['argv']==s['argv']==c['argv'] and p['cwd']==s['cwd']==c['cwd'])
    require([q['utc'] for q in (p,s,c)]==sorted(q['utc'] for q in (p,s,c)))
    bind(p['operator'])
    for q in p['sources']:bind(q['saved']);require(q['original']['sha256']==q['saved']['sha256'])
    for k in ('prelaunch','started','stdout','stderr'):bind(c[k])
    require(c['stderr']['bytes']==0 and read(cap/'STDOUT.bin')['checks_actual']==2498)
    print(json.dumps({'schema':'pr51-current-whole-readback-result/v1','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'status':'PASS_CURRENT_SCIENCE_SOURCE_ONLY','checks_actual':checks,'science_files':31,
            'literal_original_archive_files':15,'unchanged_operative_files':9,'original_json_documents':8,
            'external_body_mode_path_rows':273,'private_builder_capture_completed':True,
            'own_current_readback_capture_excluded_until_child_exit':True,
            'math_verdict_by_this_preparer':None,'all_native_root_git_merge_publication_authority':False},indent=2))


if __name__=='__main__':main()
