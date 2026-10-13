"""Selected target-only source reconciliation; no unrelated SQL-row audit or cache copying."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,math,os,sqlite3,subprocess
H=Path(__file__).resolve().parent;R=H.parents[2];B=R/'unsolved_math_prioritization'
def sha(b):return hashlib.sha256(b).hexdigest()
def parse(b):
    def pairs(items):
        o={}
        for k,v in items:assert k not in o;o[k]=v
        return o
    def finite(x):
        v=float(x);assert math.isfinite(v);return v
    return json.loads(b,object_pairs_hook=pairs,parse_float=finite,parse_constant=lambda x:(_ for _ in ()).throw(ValueError(x)))
def equal(a,b):
    if type(a) is not type(b):return False
    if type(a) is dict:return a.keys()==b.keys() and all(equal(a[k],b[k]) for k in a)
    if type(a) is list:return len(a)==len(b) and all(equal(x,y) for x,y in zip(a,b))
    return a==b
def main():
    source=parse((H/'original/source_record.json').read_bytes());refs=[]
    def local(n):
        p=B/n;b=p.read_bytes();refs.append({'path':p.relative_to(R).as_posix(),'bytes':len(b),'sha256':sha(b)});return parse(b)
    manifest=local('manifest.json');assert manifest['revision']==source['dataset_revision']
    raw=local('cache/problems.json');selected=[p for p in raw if str(p.get('id'))=='10600042'];assert len(selected)==1 and equal(selected[0],source['problem'])
    reports=local('cache/research_results.json');assert equal(reports['AMR-105-0042'],source['upstream_report'])
    for n in ['problems.json','research_results.json']:
        pinned=manifest['files'][n];actual=next(z for z in refs if z['path'].endswith('/'+n));assert actual['bytes']==pinned['bytes'] and actual['sha256']==pinned['sha256']
    con=sqlite3.connect('file:'+str((B/'cache/catalog.sqlite').resolve())+'?mode=ro',uri=True)
    row=con.execute('SELECT payload,report FROM records WHERE key=?',('10600042',)).fetchone();assert row and equal(parse(row[0]),source['problem']) and equal(parse(row[1]),source['upstream_report']);assert con.execute('SELECT revision FROM metadata').fetchall()==[(source['dataset_revision'],)];con.close()
    catalog=local('catalog.json');entry=[p for p in catalog if str(p['id'])=='10600042'];assert len(entry)==1
    assessment=local('assessments.json')['10600042'];related=local('review_v2/related_target_groups.json');matches=[x for x in related['groups'] if '10600042' in json.dumps(x)]
    queued=[line for line in (B/'QUEUE.md').read_text().splitlines() if '10600042 / AMR-105-0042' in line];assert len(queued)==1
    meta=parse((H/'captures/original_gh_metadata/stdout.bin').read_bytes());comp=parse((H/'captures/original_gh_compare/stdout.bin').read_bytes());assert comp['status']=='diverged' and comp['ahead_by']==5 and comp['behind_by']==2 and comp['base_commit']['sha']==meta['baseRefOid'] and comp['merge_base_commit']['sha']=='01358d66fc67d1c462bddf31c0d4ee5b120e6737';assert comp['commits'][-1]['sha']==meta['headRefOid']
    expected={x['path'] for x in meta['files']};assert {x['filename'] for x in comp['files']}==expected and len(expected)==16
    q=[x for x in comp['files'] if x['filename']=='unsolved_math_prioritization/QUEUE.md'];assert len(q)==1 and q[0]['additions']==1 and q[0]['deletions']==1
    out={'schema':'pr50-selected-source-reconciliation/v1','utc':datetime.now(timezone.utc).isoformat(),'actual_pid':os.getpid(),'status':'PASS_EXACT_SELECTED_RAW_SQL_ORIGINAL_RECORD','raw_selected_problem_matches_original_typed':True,'raw_selected_report_matches_original_typed':True,'selected_SQL_problem_report_match_original_typed':True,'selected_SQL_rows_read':1,'dataset_revision':source['dataset_revision'],'input_metadata_pins':refs,'current_selected_catalog':entry[0],'current_selected_assessment':assessment,'selected_related_groups':matches,'current_selected_queue_row_dated':queued[0],'original_queue_patch':q[0]['patch'],'original_GitHub_base_matches_merge_base':False,'original_reported_GitHub_base':meta['baseRefOid'],'original_actual_merge_base':comp['merge_base_commit']['sha'],'original_comparison_status':comp['status'],'original_comparison_ahead':5,'original_comparison_behind':2,'original_changed_paths':sorted(expected),'original_selected_source_copied_unchanged':True,'current_main_dated':subprocess.check_output(['/usr/bin/git','rev-parse','HEAD'],cwd=R,text=True).strip(),'cache_or_PDF_bodies_copied':False,'unrelated_SQL_rows_audited':False,'fresh_native_authority':False,'acceptance_approved':False}
    with (H/'SELECTED_SOURCE_INVENTORY.json').open('x') as f:f.write(json.dumps(out,sort_keys=True,indent=2)+'\n')
    print(json.dumps({'status':out['status'],'actual_pid':os.getpid(),'selected_SQL_rows':1,'raw_SQL_typed_match':True,'original_paths':16,'related_exact_id_groups':len(matches),'acceptance_approved':False},sort_keys=True))
if __name__=='__main__':main()
