"""Fresh source freeze now; website freeze ONLY after explicit new root GO.

No network, Git, website/source mutation, science or legacy helper execution.
All raw copied inputs are content-addressed under ignored blobs/.
"""
from pathlib import Path
import datetime
import json
import re
import sys
import xml.etree.ElementTree as ET
from stage_common import A,CAT,W,FACT,IDS,ADOPTIONS,FACT_CLOSURE,BASE_COUNTS,FINAL_COUNTS
from stage_common import need,read,obj,sha,names,guard_fact_and_owners,adopted_editorials,authorize,structured


def write_json(name,value):
    path=A/name;need(not path.exists(),'refuse overwriting frozen artifact: '+name)
    path.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')


def snapshot(path):
    body=read(path);h=sha(body);dest=A/'blobs'/h
    if dest.exists():need(read(dest)==body,'existing whole blob identity')
    else:dest.write_bytes(body)
    return {'path':str(path),'bytes':len(body),'SHA256':h,'blob':'blobs/'+h}


def source_freeze():
    original=guard_fact_and_owners();authorities=adopted_editorials()
    need(not (A/'SOURCE_INPUTS.json').exists(),'fresh source freeze only')
    paths={Path(r['path']) for r in original['files']}
    factfiles,_=names(FACT);paths.update(factfiles)
    paths.add(FACT_CLOSURE)
    paths.update(CAT/'verification'/('root-editorial-'+rid+'-20261115.json') for rid in IDS)
    rows=[snapshot(p) for p in sorted(paths)]
    # No website function/read/list is called in this source-only phase.
    guard_fact_and_owners();adopted_editorials()
    write_json('SOURCE_INPUTS.json',{'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),
               'schema':'lefschetz-link-source-only-freeze-v1','files':rows,'original_fact_input_count':244,
               'source_editorial_namespace_counts':[65,41,65,60],
               'root_editorial_adoption_SHA256':list(ADOPTIONS),'whole_original_root_adoptions':authorities,
               'website_read_list_or_baseline_capture':False,'raw_directories_ignored_before_creation':True,
               'whole_original_typed_objects_and_historical_flags_preserved':True})
    print(json.dumps({'phase':'source-only freeze','frozen_files':len(rows),'original244_unchanged':True,
                      'strict_source_editorial_counts':[65,41,65,60],'website_inspected':False,'rendering':False},indent=2))


def website_freeze(go_path,go_sha):
    # These checks precede EVERY website path read, namespace listing or snapshot.
    g=authorize(go_path,go_sha)
    need((A/'SOURCE_INPUTS.json').exists(),'adopted source-only freeze must precede website freeze')
    guard_fact_and_owners();adopted_editorials()
    for row in obj(A/'SOURCE_INPUTS.json')['files']:
        body=read(Path(row['path']))
        need(len(body)==row['bytes'] and sha(body)==row['SHA256'],'all source frozen inputs still current')
    for name in ['WEBSITE_BASELINE.json','AUTHORIZATION_BINDING.json']:
        need(not (A/name).exists(),'new immutable website freeze only')
    public,dirs=names(W/'public');need(len(public)==BASE_COUNTS[0],'actual fresh605public files')
    index=read(W/'public/research/index.html').decode();_,schema=structured(index)
    items=schema['mainEntity']['itemListElement']
    need(schema['mainEntity']['numberOfItems']==len(items)==BASE_COUNTS[1],'actual fresh90typed index records')
    need([v['position'] for v in items]==list(range(1,91)),'full original ordered index positions')
    sitemap=read(W/'public/research/sitemap.xml')
    need(len(ET.fromstring(sitemap))==BASE_COUNTS[2],'actual fresh91whole sitemap nodes')
    for rid in IDS:
        ed=CAT/'papers'/rid/'reviews/editorial'
        c=obj(ed/('config/publication.json' if rid==IDS[0] else 'publication.json'))
        need(not (W/'public/research'/c['slug']).exists(),'new target article leaf absent in authorized baseline')
    external=[W/'firebase.json',W/'.firebaserc',Path(g['prior_installation_receipt']['path']),Path(go_path),
              Path(g['root_fact_audit_adoption']['path']),Path(g['prior_root_stage_adoption']['path'])]
    rows=[snapshot(p) for p in sorted(set(public+external))]
    after,afterdirs=names(W/'public')
    need(after==public and afterdirs==dirs,'whole website namespace unchanged across snapshot')
    for row in rows:need(read(Path(row['path']))==read(A/row['blob']),'original website inputs unchanged across copy')
    write_json('WEBSITE_BASELINE.json',{'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),
               'schema':'fresh-lefschetz-link-authorized-605-baseline-v1','website_root':str(W),
               'root_GO_path':str(go_path),'root_GO_SHA256':go_sha,'files':rows,
               'public_namespace':[str(p) for p in public],'public_directory_namespace':dirs,
               'prior_index_whole_schema':schema,'baseline_counts':list(BASE_COUNTS),'virtual_counts':list(FINAL_COUNTS),
               'prior_installation_commit':g['prior_installation_commit'],'inherited_earlier_baseline':False,
               'Git_or_site_mutation':False})
    write_json('AUTHORIZATION_BINDING.json',{'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),
               'root_GO_path':str(go_path),'root_GO_SHA256':go_sha,'whole_original_root_GO':g,
               'website_baseline_frozen_only_after_explicit_GO':True,'production_installation_authorized':False})
    print(json.dumps({'phase':'fresh website freeze','baseline_counts':list(BASE_COUNTS),
                      'expected_virtual_counts':list(FINAL_COUNTS),'rendering':False,'site_writes':False},indent=2))


if __name__=='__main__':
    need(sys.argv[1:]==['sources'] or (len(sys.argv)==5 and sys.argv[1]=='website' and sys.argv[2]=='--root-GO'),
         'sources OR website --root-GO ABSOLUTE_JSON_PATH EXPECTED_SHA256')
    ignored=read(A/'.gitignore').decode().splitlines()
    need('inputs/' in ignored and 'blobs/' in ignored,'whole raw directories ignored before creation')
    # Merely creating own ignored empty directories does not inspect website inputs.
    (A/'inputs').mkdir(exist_ok=True);(A/'blobs').mkdir(exist_ok=True)
    if sys.argv[1]=='sources':source_freeze()
    else:website_freeze(Path(sys.argv[3]),sys.argv[4])
