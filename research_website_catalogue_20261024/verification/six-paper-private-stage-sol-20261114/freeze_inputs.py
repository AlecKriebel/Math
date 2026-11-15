"""One authorized input/current-public snapshot; writes only this private stage."""
from six_common import *
from datetime import datetime,timezone
import subprocess

def freeze():
    require(not (OWN/'FROZEN_INPUT_SET.json').exists(),'refuse_existing_input_freeze')
    a=authenticate_root();paths={ROOT_ADOPTION};spec={}
    for row in [a['previous106_adoption'],*a['new_five_adoptions']]:paths.add(Path(row['path']))
    for rid in IDS:
        T=PROGRAMME/'papers'/rid;c=load(T/'publication.json');g=load(T/'promotion.json');E=T/'reviews/editorial';S=T/'sources'
        for folder in [E,S]:
            paths.update(x for x in folder.rglob('*') if x.is_file() and '__pycache__' not in x.parts)
        paths.update([T/'publication.json',T/'promotion.json']);science=contained(PROGRAMME,g['root_clearance_file']);paths.add(science)
        require(bind(science)['sha256']==g['root_clearance_sha256']==c['review_metadata']['root_clearance_sha256'],'root_science_hash')
        root=load(science);require(root['status']==STATUSES[rid],'literal_root_scientific_status')
        # Bind actual local file references in the whole root object, without
        # executing or rewriting any referenced proof/review/program.
        def refs(x):
            if isinstance(x,dict):
                for v in x.values():refs(v)
            elif isinstance(x,list):
                for v in x:refs(v)
            elif isinstance(x,str) and not x.startswith(('http:','https:')):
                try:
                    q=Path(x);q=q if q.is_absolute() else PROGRAMME/q
                    if len(x)<500 and q.is_file() and q.resolve().is_relative_to(PROGRAMME):paths.add(q)
                except (ValueError,OSError):pass
        refs(root)
        ready=load(S/'SOURCE_READY.json');api=load(S/'record.raw.json')
        arrkey='assets' if rid=='23124601' else 'all_native_assets_in_original_order' if rid=='22929857' else 'all_assets_in_original_order'
        objkey='native_file_object' if rid=='23124601' else 'original_api_file_object'
        trans=['transport-receipts.json'] if rid=='23124601' else ['api-receipts.json'] if rid in {'23333046','23383952','23539734'} else ['record.transport.json','acquisition.transport.json'] if rid=='22929857' else ['transport-01-record.json','transport-02-latest.json','transport-03-versions.json','transport-04-asset.json','transport-05-asset.json','transport-receipts.json']
        spec[rid]={'ready_keys':list(ready),'ready_array':arrkey,'asset_object_key':objkey,'digest_key':'SHA256' if rid=='22929857' else 'sha256',
                   'md5_key':'MD5' if rid=='22929857' else 'md5','asset_keys':[list(x) for x in ready[arrkey]],
                   'asset_order':[x['key'] for x in api['files']],'native_record_keys':list(api),'native_metadata_keys':list(api['metadata']),
                   'transport_files':trans,'transport_objects':[load(S/n) for n in trans],
                   'whole_root_science':{'path':str(science),'sha256':bind(science)['sha256']},
                   'citation_path':str(T/(c['source_binding'].get('prepared_bibtex_path') or 'reviews/editorial/citation.bib'))}
    rows=[{'path':str(p),**bind(p)} for p in sorted(paths)]
    public=[]
    for p in sorted(PUBLIC.rglob('*')):
        if p.is_file():require(not p.is_symlink(),'public_symlink');public.append({'path':str(p.relative_to(PUBLIC)),**bind(p)})
    require(len(public)==532,'fresh_actual_public_count')
    corepaths=sorted([*PROGRAMME.joinpath('scripts').glob('*.py'),PROGRAMME/'verification/final-content-check.py'])
    core=[{'path':str(p),**bind(p)} for p in corepaths]
    require(not any((PUBLIC/'research'/load(PROGRAMME/'papers'/rid/'publication.json')['slug']).exists() for rid in IDS),'new_six_dirs_absent')
    base=OWN/'baseline/research';base.mkdir(parents=True)
    for n in ['index.html','sitemap.xml']:(base/n).write_bytes((PUBLIC/'research'/n).read_bytes())
    out={'UTC':datetime.now(timezone.utc).isoformat(),'root_adoption_sha256':ROOT_ADOPTION_SHA,'records':list(IDS),'files':rows,'native_specs':spec}
    baseline={'UTC':out['UTC'],'website_HEAD':subprocess.check_output(['git','rev-parse','HEAD'],cwd=WEBSITE,text=True).strip(),
              'public_files':public,'installed_core_files':core,'article_count':72,'sitemap_count':73,'unchanged_public_except':['research/index.html','research/sitemap.xml']}
    (OWN/'FROZEN_INPUT_SET.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
    (OWN/'FRESH_BASELINE.json').write_text(json.dumps(baseline,indent=2)+'\n')
    seal={'UTC':out['UTC'],'frozen_input_sha256':bind(OWN/'FROZEN_INPUT_SET.json')['sha256'],'baseline_sha256':bind(OWN/'FRESH_BASELINE.json')['sha256'],
          'native_inputs':len(rows),'old_public':len(public),'installed_core':len(core),'records':list(IDS),'private_only':True}
    (OWN/'INPUT_FREEZE_SEAL.json').write_text(json.dumps(seal,indent=2)+'\n')
    return seal
if __name__=='__main__':print(json.dumps(freeze(),sort_keys=True))
