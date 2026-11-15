"""Pure read-only custody closure; import-safe, with no target science imports.

This checks byte custody and explicit scope labels, not mathematical truth.
No network, extraction, source execution or filesystem writes occur here.
"""
from pathlib import Path
from copy import deepcopy
import hashlib
import json
import zipfile

P = Path(__file__).resolve().parent
S = P.parents[1] / 'sources'
TERMINALS = {'OWNED_MANIFEST.json','CLOSURE_RESULT.json','FINAL_SEAL.json'}

def sha(data):
    return hashlib.sha256(data).hexdigest()

def obj(path):
    return json.loads(path.read_text())

def fixtures():
    return {
        'ready':obj(S/'SOURCE_READY.json'),
        'record':obj(S/'record.response.body'),
        'versions':obj(S/'versions-page001.response.body'),
        'files':obj(S/'files.response.body'),
        'initial':obj(P/'INITIAL_SEAL.json'),
        'verdict':obj(P/'VERDICT.json'),
        'controls':obj(P/'INDEPENDENT_CONTROLS.json'),
        'support':obj(P/'SUPPORT_INSPECTION.json'),
    }

def semantic(f):
    r,rec,versions,files,initial,v,c,s = (f[k]for k in ['ready','record','versions','files','initial','verdict','controls','support'])
    tests=[]
    def test(condition,label):
        tests.append((condition,label))
    test(r['record_id']==23440943 and r['status']=='SOURCE_READY','exact record')
    test(r['native_version_whole_field']=={'present':True,'original_value':'1.0.0'},'whole native version')
    test(r['all_enumerated_version_ids']==[23440943],'exact release identity')
    test(r['publication_date']=='2026-10-17','declared date')
    test(r['created']=='2026-10-17T19:04:32.905992+00:00' and r['updated']=='2026-10-17T19:04:33.294068+00:00','created and updated separate')
    test(r['HTTP_status_sequence']==[200,301,200,200,200,200,200] and r['actual_ordinary_native_HTTP_requests']==7,'ordered native transports')
    test([a['original_api_file_object']['key']for a in r['all_native_assets_in_original_order']]==['totally-mixed-face-posets-source-and-verification.zip','totally-mixed-face-posets.pdf'],'native assets ordered ZIP then PDF')
    test(type(rec['swh'])is dict and rec['swh']=={},'empty record object')
    test(versions['hits']['hits'][0]['swh']is None,'version hit null')
    test(type(files['entries'])is list and files['order']==[] and files['default_preview']is None,'literal files schema')
    test(r['whole_regular_payload_occurrences']==29 and r['expanded_bytes_all_depths']==347616 and r['nested_archive_count']==0,'whole archive scope')
    test(len(r['embedded_PDFs'])==1 and r['embedded_PDFs'][0]['identical_to_standalone_published_PDF']is True,'embedded PDF original association')
    test(r['printed_date']is None and r['printed_version']is None and r['printed_title_date_version_inspected']is False,'historical identity unread flags')
    test(r['mathematical_PDF_TeX_or_pixels_read']is False and r['source_programmes_executed']==[],'historical scientific exposure')
    test(r['scientific_verdict']is None and r['publication_authority']is False,'source-only authority')
    test(initial['root_gate']=='CLOSED' and initial['scientific_findings_released']is False,'immutable initial CLOSED boundary')
    test(initial['actual_PDF_pages_personally_read']==4 and initial['entire_controlling_TeX_lines_personally_read']==243 and initial['own_fresh_individual_rasters_personally_viewed']==4,'complete own reading')
    test(initial['printed_version']=='1.0.0' and initial['printed_date']=='October 17, 2026','actual printed identity')
    test(initial['target_foreign_primary_body_read_before_seal']is False and initial['native_science_code_results_read_imported_or_executed']is False,'paper-first initial')
    test(initial['current_root_sibling_or_archived_target_scientific_opinions_read']is False and initial['other_current_review_folder_opened']is False,'early independence')
    test(v['full_original_claim_assessed']is True and v['substantive_defect_found']is False and v['exact_defect']is None,'literal verdict')
    test(v['narrowing_or_repair_proposed']is False,'no repaired replacement')
    test(v['complete_result']=={'components':2,'each_component_pure_dimension':1,'each_component_vertices':50,'each_component_edges':60,'each_component_connected':True,'ordinary_rational_Betti_numbers':[2,22],'all_higher_homology_zero':True,'not_shellable_pure':True,'not_shellable_standard_nonpure':True,'not_rational_homology_of_wedge_of_3_spheres':True},'full all-parts result labels')
    test(all(v['exact_filter'].values()) and v['realization']=='ordinary order complex of nonempty strict chains; no artificial extrema','exact filter and realization')
    test(v['printed_source_actual_body_checked']['stated_general_position_assumption']is False,'printed source genericity')
    test(v['boundary_scopes']['stable_intersection_shellability_resolved']is False and v['boundary_scopes']['smallest_possible_dimension_claim']is False,'scope exclusions')
    test(v['followup']is None and v['publication_authority']is False and v['current_peer_or_root_scientific_packets_read']is False,'limits and authority')
    test(s['native_scientific_imports_or_executions_here']==[] and v['reproduction_here']['native_scientific_code_imported_or_executed']is False,'no native replay/import')
    test(len(s['personally_read_entire_native_code'])==2 and sum(x['lines']for x in s['personally_read_entire_native_code'])==707,'complete native code read scope')
    test(c['status']=='PASS' and c['base_nonempty_proper_faces']==180 and c['coordinate_inclusion_pairs_checked']==32400 and len(c['whole_face_coordinate_certificates'])==180,'own coordinate scope')
    test(c['base_f_vector']==[50,60] and c['two_copy_order_complex']['boundary_rank_over_Q']==98 and c['two_copy_order_complex']['rational_Betti_numbers']==[2,22],'own topology scope')
    test(len(c['signed_model']['spanning_tree'])==19 and len(c['signed_model']['fundamental_cycles'])==11,'checkable own graph certificates')
    test(c['four_index_boundary_control']['qualifying_faces']==6 and c['four_index_boundary_control']['shellable_pure_dimension_zero']is True,'low-dimensional control')
    return [label for good,label in tests if not good],len(tests)

def check_files(rows,base=None):
    errors=[]
    for row in rows:
        path=Path(row['path'])
        if base is not None:
            if path.is_absolute()or'..'in path.parts:
                errors.append('unsafe owned path '+str(path));continue
            path=base/path
        if path.is_symlink()or not path.is_file():
            errors.append('missing/nonregular '+str(path));continue
        b=path.read_bytes()
        if len(b)!=row['bytes']or sha(b)!=row['SHA256']:
            errors.append('byte binding '+str(path))
    return errors

def verify():
    inputs,owned=obj(P/'INPUT_MANIFEST.json'),obj(P/'OWNED_MANIFEST.json')
    errors=check_files(inputs['inputs'])+check_files(owned['owned_files'],P)
    original_manifest=obj(S/'SOURCE_READY_MANIFEST.json')
    errors+=check_files(original_manifest['files'],S)
    original_seal=obj(S/'SOURCE_READY_SEAL.json')
    for name,key in [('SOURCE_READY_MANIFEST.json','MANIFEST_SHA256'),('SOURCE_READY_CLOSURE.json','CLOSURE_SHA256')]:
        if sha((S/name).read_bytes())!=original_seal[key]:
            errors.append('source acquisition terminal '+name)
    actual={str(f.relative_to(P))for f in P.rglob('*')if f.is_file()and f.name not in TERMINALS}
    if actual!={x['path']for x in owned['owned_files']}:
        errors.append('owned file universe')
    f=fixtures();sem,n=semantic(f);errors+=sem
    anchors={
        S/'SOURCE_READY.json':'928fb2b26bd31a0678fc3954c29f8a7897a3d6352e9b5dab791224a72a828235',
        S/'SOURCE_READY_SEAL.json':'0fed874ecff807d3250957b196f39902b124825dd0c5fa90bd1efa2bf406679e',
        P/'INITIAL_SEAL.json':'31c22f1f8a1575fff0164771f333d62aaf6919ba23969ef249a3041410ca5c82',
        P/'INITIAL_RECONSTRUCTION.md':'4a3da7f511460311c56ea9cc58c597932885e3e724d8e3f6c28f9f81e6e474f8',
        P/'INDEPENDENT_CONTROLS.json':'ad0cc4ccea6bbda36df2552140ff1ac3f31e495032393caf1e7de1f34a399099',
    }
    for path,h in anchors.items():
        if sha(path.read_bytes())!=h:
            errors.append('immutable anchor '+str(path))
    ready=f['ready']
    for asset in ready['all_native_assets_in_original_order']:
        b=Path(asset['path']).read_bytes();md5=asset['original_api_file_object']['checksum'].split(':',1)[1]
        if sha(b)!=asset['SHA256']or hashlib.md5(b).hexdigest()!=md5:
            errors.append('native asset checksum '+asset['path'])
    custody=obj(S/'ARCHIVE_CUSTODY.json');members=custody['regular_payload_occurrences']
    with zipfile.ZipFile(ready['all_native_assets_in_original_order'][0]['path'])as z:
        infos=z.infolist()
        if len(infos)!=29:
            errors.append('whole ZIP central-directory count')
        for info,member in zip(infos,members):
            b=z.read(info)
            good=(info.filename==member['original_member_name']and info.file_size==member['bytes']and info.compress_size==member['compressed_bytes']and f'{info.CRC:08x}'==member['CRC32']and info.compress_type==member['compression_method']and info.external_attr==member['native_external_attr']and info.create_system==member['native_create_system']and info.flag_bits==member['native_flags']and list(info.date_time)==member['native_date_time']and sha(b)==member['SHA256']and b==Path(member['extracted_path']).read_bytes())
            if not good:
                errors.append('ZIP original occurrence '+info.filename)
    embedded=Path(ready['embedded_PDFs'][0]['extracted_path']).read_bytes()
    if embedded!=Path(ready['selected_actual_PDF']['path']).read_bytes():
        errors.append('embedded/standalone identity')
    if(P/'FINAL_SEAL.json').exists():
        for name,h in obj(P/'FINAL_SEAL.json')['terminal_bindings'].items():
            if sha((P/name).read_bytes())!=h:
                errors.append('terminal binding '+name)
    return {'status':'PASS'if not errors else'FAIL','errors':errors,'input_files':len(inputs['inputs']),'owned_files':len(owned['owned_files']),'original_acquisition_manifest_files':len(original_manifest['files']),'ZIP_regular_occurrences':len(members),'semantic_checks':n,'science_executed_or_imported':False,'writes':False,'network':False}

def self_test():
    baseline=fixtures()
    if semantic(baseline)[0]:
        raise RuntimeError('invalid baseline')
    mutations=[
        ('record identity',lambda f:f['ready'].__setitem__('record_id',23440942)),
        ('native version',lambda f:f['ready']['native_version_whole_field'].__setitem__('original_value','latest')),
        ('declared date',lambda f:f['ready'].__setitem__('publication_date','2026-10-18')),
        ('created vs updated',lambda f:f['ready'].__setitem__('created',f['ready']['updated'])),
        ('transport history',lambda f:f['ready'].__setitem__('HTTP_status_sequence',[200]*7)),
        ('asset order',lambda f:f['ready']['all_native_assets_in_original_order'].reverse()),
        ('empty object',lambda f:f['record'].__setitem__('swh',None)),
        ('version null',lambda f:f['versions']['hits']['hits'][0].__setitem__('swh',{})),
        ('files type',lambda f:f['files'].__setitem__('entries',{})),
        ('preview null',lambda f:f['files'].__setitem__('default_preview','')),
        ('archive count',lambda f:f['ready'].__setitem__('whole_regular_payload_occurrences',28)),
        ('historical unread flag',lambda f:f['ready'].__setitem__('mathematical_PDF_TeX_or_pixels_read',True)),
        ('original CLOSED flag',lambda f:f['initial'].__setitem__('root_gate','OPEN')),
        ('whole personal read',lambda f:f['initial'].__setitem__('actual_PDF_pages_personally_read',3)),
        ('printed version',lambda f:f['initial'].__setitem__('printed_version',None)),
        ('paper-first',lambda f:f['initial'].__setitem__('native_science_code_results_read_imported_or_executed',True)),
        ('homology',lambda f:f['verdict']['complete_result'].__setitem__('ordinary_rational_Betti_numbers',[1,22])),
        ('nonshellability',lambda f:f['verdict']['complete_result'].__setitem__('not_shellable_standard_nonpure',False)),
        ('dimension filter',lambda f:f['verdict']['exact_filter'].__setitem__('dimension_of_sum_equals_sum_of_dimensions',False)),
        ('source genericity',lambda f:f['verdict']['printed_source_actual_body_checked'].__setitem__('stated_general_position_assumption',True)),
        ('unwarranted stable promotion',lambda f:f['verdict']['boundary_scopes'].__setitem__('stable_intersection_shellability_resolved',True)),
        ('follow-up',lambda f:f['verdict'].__setitem__('followup',{})),
        ('native import',lambda f:f['support'].__setitem__('native_scientific_imports_or_executions_here',['check_topology'])),
        ('own certificate count',lambda f:f['controls'].__setitem__('base_nonempty_proper_faces',179)),
    ]
    rows=[]
    for label,mutate in mutations:
        f=deepcopy(baseline);mutate(f);rejected=bool(semantic(f)[0])
        rows.append({'mutation':label,'rejected':rejected})
        if not rejected:
            raise RuntimeError('accepted mutant '+label)
    row=deepcopy(obj(P/'OWNED_MANIFEST.json')['owned_files'][:1]);row[0]['SHA256']='0'*64
    rejected=bool(check_files(row,P));rows.append({'mutation':'forged owned byte hash','rejected':rejected})
    if not rejected:
        raise RuntimeError('forged hash accepted')
    row=deepcopy(obj(S/'SOURCE_READY_MANIFEST.json')['files'][:1]);row[0]['SHA256']='0'*64
    rejected=bool(check_files(row,S));rows.append({'mutation':'forged original acquisition hash','rejected':rejected})
    if not rejected:
        raise RuntimeError('forged acquisition hash accepted')
    return {'status':'PASS','in_memory_falsifiers':rows,'mutant_count':len(rows),'files_changed':False,'science_executed_or_imported':False}

if __name__=='__main__':
    import sys
    result=self_test()if sys.argv[1:]==['--self-test']else verify()
    print(json.dumps(result,indent=2))
    if result['status']!='PASS':
        raise SystemExit(1)
