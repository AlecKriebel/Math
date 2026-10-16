"""Own read-only custody/metadata check, not a mathematics or priority certificate."""
from pathlib import Path
import datetime as dt, hashlib, json, os, stat, sys, xml.etree.ElementTree as ET
P=Path(__file__).absolute().parent;A=P.parent;R=A.parents[2]
def sha(b):return hashlib.sha256(b).hexdigest()
def utc():return dt.datetime.now(dt.timezone.utc).isoformat()
def need(v,m):
    if not v:raise ValueError(m)
def ref(p):
    need(p.is_file() and not p.is_symlink(),'Regular source input');b=p.read_bytes()
    return dict(path=str(p.relative_to(R)),bytes=len(b),sha256=sha(b),full_mode=stat.S_IMODE(p.stat().st_mode))
def main():
    rows=[];route_count=success=fail=0
    for i in (1,2,3):
        d=P/f'actual_public_routes_{i}_capture';c=json.loads((d/'CAPTURE.json').read_bytes());v=json.loads((P/f'PUBLIC_RETRIEVAL_{i}.json').read_bytes())
        need(c['actual_execution'] is True and c['completed'] is True and c['exit_code']==0 and type(c['pid']) is int and c['pid']==v['actual_pid'],'Actual own completed retrieval child')
        need(c['source_unchanged'] is True and sha((d/'PRELAUNCH_SOURCE.py').read_bytes())==c['source_sha256']==v['source_sha256']==sha((P/'fetch_public_routes.py').read_bytes()),'Whole retained actual source')
        need(c['input_sha256']==sha((P/f'PUBLIC_ROUTES_{i}.json').read_bytes()),'Actual source input unchanged')
        for k in ('stdout','stderr'):
            b=(d/c[k]['path']).read_bytes();need(len(b)==c[k]['bytes'] and sha(b)==c[k]['sha256'],'Complete actual streams')
        for z in v['routes']:
            route_count+=1
            if z['complete_body_retrieved']:
                b=(P/'private_cache'/z['private_cache_filename']).read_bytes();need(len(b)==z['bytes'] and sha(b)==z['sha256'] and z['pdf_magic']==b.startswith(b'%PDF-'),'Exact entire retrieved response, not final article inference');success+=1
            else:need(z['error_type']=='timeout' and 'private_cache_filename' not in z,'Actual timeout carries no invented response hash');fail+=1
        rows.append(dict(actual_child_pid=c['pid'],capture=ref(d/'CAPTURE.json'),retrieval=ref(P/f'PUBLIC_RETRIEVAL_{i}.json')))
    title=json.loads((P/'private_cache/hal_exact_combined_title.raw').read_bytes())['response'];need(title['numFound']==1,'Exact title single response');record=title['docs'][0]
    need(record['halId_s']=='hal-04293155' and record['version_i']==1 and record['submitType_s']=='notice' and record['openAccess_bool'] is False and 'fileMain_s' not in record,'Primary notice and absent deposited file field')
    ns={'t':'http://www.tei-c.org/ns/1.0','d':'http://datacite.org/schema/kernel-4'}
    tei=ET.fromstring((P/'private_cache/hal_xml_tei.raw').read_bytes());rights=ET.fromstring((P/'private_cache/hal_openaire.raw').read_bytes())
    bibl=tei.find('.//t:biblFull',ns);need(bibl is not None,'Bibliographic TEI body')
    availability=bibl.find('t:publicationStmt/t:availability',ns);need(availability.attrib['status']=='restricted','TEI restricted bibliographic availability')
    paper_links=[z.attrib for z in bibl.findall('.//t:ref',ns)];need(paper_links==[],'No linked text ref in exact record bibliographic body')
    access=rights.findall('.//d:rights',ns);need(len(access)==1 and access[0].text=='metadata only access','Exact primary OpenAIRE-schema access state')
    need(sha((A/'reviewed_candidate/CANDIDATE.md').read_bytes())=='8ac19b70bd9081107e903ca47bb9dd6ad05274f604d03000a7fd18e3cfb3bf12','Exact current candidate')
    names=['reviewed_candidate/CANDIDATE.md','priority_access_resolution/VERDICT.json','priority_access_resolution/ACCESS_RESOLUTION_REPORT.md','priority_exact_family/PRIORITY_REPORT.md','primary_scope_family/verdict.json','cap_chart_family/verdict.json','density_area_family/VERDICT.json']
    out=dict(schema='pr18-revisit-own-readonly-source-check/v1',actual_pid=os.getpid(),actual_argv=sys.argv,utc=utc(),status='PASS_CUSTODY_AND_METADATA_ONLY',retrieval_routes=route_count,complete_HTTP_responses=success,timeouts=fail,actual_children=rows,existing_sources=[ref(A/n) for n in names],primary_metadata_findings=dict(HAL_title_matches=1,version=1,submit_type='notice',open_access=False,fileMain_s_absent=True,TEI_bibliographic_availability='restricted',OpenAIRE_schema_rights='metadata only access'),complete_final_article_obtained=False,new_mathematical_review_credit=0,new_problem_attempts=0,native_Git_remote_mutation=False)
    b=(json.dumps(out,indent=2,sort_keys=True)+'\n').encode()
    with (P/'SOURCE_CHECKS.json').open('xb') as f:f.write(b)
    print(json.dumps(dict(status=out['status'],actual_pid=os.getpid(),result_sha256=sha(b),routes=route_count,responses=success,timeouts=fail)))
if __name__=='__main__':main()
