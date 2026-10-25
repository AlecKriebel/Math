"""Bounded source/format controls in memory; no source fixture or program run."""
import sys
sys.dont_write_bytecode=True
from pathlib import Path
from copy import deepcopy
import json
O=Path(__file__).resolve().parent
P=O.parents[1]
sys.path[:0]=[str(O),str(P/'scripts')]
from odd_ear_blocking_source import OEB_IDS, odd_ear_blocking_source_view, validate_oeb_assets, verify_oeb_archive, same
rb,rt=Path.read_bytes,Path.read_text
rows=[]
def reject(rid,name,call):
    try:
        call()
    except (ValueError,KeyError,FileNotFoundError,TypeError) as error:
        rows.append({'record_id':rid,'case':name,'rejected':True,'actual_reason':str(error)[:320]})
    else:
        raise RuntimeError('changed_input_accepted:'+rid+':'+name)
for rid in sorted(OEB_IDS):
    paper=P/'papers'/rid
    c=json.loads(rb(paper/'publication.json'));g=json.loads(rb(paper/'promotion.json'));b=c['source_binding']
    raw=json.loads(rb(paper/b['source_receipt_path']));api=json.loads(rb(paper/b['raw_record_path']))
    inv=json.loads(rb(paper/'sources/archive-members.json'))
    add=json.loads(rb(paper/b['tar_custody_addendum_path'])) if rid=='23331258' else None
    before=deepcopy([c,g,raw,api,inv,add])
    original,view,root=odd_ear_blocking_source_view(paper,c,g)
    if not same(original,raw) or len(view['files'])!=2:
        raise RuntimeError('pristine_source_view')
    rows.append({'record_id':rid,'case':'pristine_complete_source_and_archive','accepted':True})
    for name in ('borrowed_version','borrowed_code_license','float_completion','changed_whole_family_verdict','generic_root_status_suffix'):
        bc,bg=deepcopy(c),deepcopy(g)
        if name=='borrowed_version':bc['version']='1.0' if rid=='23576280' else '1.0.0'
        elif name=='borrowed_code_license':bc['license']='MIT' if rid=='23331258' else 'CC BY 4.0 for all code'
        elif name=='float_completion':bc['review_metadata']['completion_percent']=100.0
        elif name=='changed_whole_family_verdict':bg['reviews']['scope']['verdict']={}
        else:bg['status']='PASS_UNAUTHENTICATED_SUFFIX';bg['root_clearance_record']['status']=bg['status']
        reject(rid,name,lambda:odd_ear_blocking_source_view(paper,bc,bg))
    paths=[paper/b['source_receipt_path'],paper/b['raw_record_path'],paper/b['initial_intake_receipt_path'],paper/'sources/archive-members.json',paper/b['source_tex_path'],paper/'sources'/c['pdf_filename'],P/('verification/root-editorial-'+rid+'-20261025.json')]
    for path in paths:
        data=rb(path);bad=bytes([data[0]^1])+data[1:]
        Path.read_bytes=lambda q,_p=path,_d=bad:_d if q.resolve()==_p.resolve() else rb(q)
        Path.read_text=lambda q,*a,**kw:Path.read_bytes(q).decode(kw.get('encoding') or 'utf-8')
        try:
            reject(rid,'changed_actual_read:'+str(path.relative_to(P)),lambda:odd_ear_blocking_source_view(paper,c,g))
        finally:
            Path.read_bytes,Path.read_text=rb,rt
    for name in ('reorder_both_native_assets_and_API','invent_files_alias','float_asset_size','uppercase_SHA'):
        br,ba=deepcopy(raw),deepcopy(api)
        if name=='reorder_both_native_assets_and_API':br['all_assets'].reverse();ba['files'].reverse()
        elif name=='invent_files_alias':br['files']=br.pop('all_assets')
        elif name=='float_asset_size':br['all_assets'][0]['bytes']=float(br['all_assets'][0]['bytes'])
        else:br['all_assets'][0]['sha256']=br['all_assets'][0]['sha256'].upper()
        reject(rid,name,lambda:validate_oeb_assets(paper,rid,br,ba))
    if rid=='23576280':
        for name in ('drop_embedded_reader_occurrence','escape_outer_extraction_mapping'):
            bi=deepcopy(inv)
            if name=='drop_embedded_reader_occurrence':bi['files']=[x for x in bi['files'] if x['member']!='paper.pdf']
            else:bi['files'][0]['path']='../outside'
            reject(rid,name,lambda:verify_oeb_archive(paper,rid,paper/'sources'/c['supplement_filename'],bi,paper/'sources'/c['pdf_filename']))
    else:
        for name in ('lose_nested_tar_occurrence','escape_nested_existing_body_mapping'):
            bad=deepcopy(add)
            if name=='lose_nested_tar_occurrence':bad['regular_members'].pop()
            else:bad['regular_members'][0]['existing_exact_original_member']='/tmp/not-an-original'
            reject(rid,name,lambda:verify_oeb_archive(paper,rid,paper/'sources'/c['supplement_filename'],inv,paper/'sources'/c['pdf_filename'],bad))
    if not same(before,[c,g,raw,api,inv,add]):
        raise RuntimeError('original_arguments_mutated')
reject('UNSUPPORTED','exclude103_and_every_other_ID',lambda:odd_ear_blocking_source_view(P/'papers/23217863',{},{}))
print(json.dumps({'status':'PASS','optimized':sys.flags.optimize,'checks':rows,
                  'pristine_acceptances':sum(x.get('accepted',False) for x in rows),
                  'rejections':sum(x.get('rejected',False) for x in rows),
                  'original_arguments_unchanged':True,'source_fixture_writes':0,
                  'source_programs_executed':False},indent=2))
