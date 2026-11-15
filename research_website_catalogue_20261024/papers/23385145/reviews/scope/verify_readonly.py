#!/usr/bin/env python3
"""Read-only closure: no network, subprocess, import of deposited programs or writes.
Hashes/CRC authenticate retained inputs; semantic checks are not proof certification.
"""
from pathlib import Path, PurePosixPath
from copy import deepcopy
from fractions import Fraction
import hashlib, json, math, stat, sys, zipfile

HERE=Path(__file__).resolve().parent
SOURCE=HERE.parents[1]/'sources'
READY_SHA='398351e05ac4ddc92510ea191c109dd22a48a177869872a8008ff2f8328581e5'
INITIAL_SHA='b1796bef5cb75f3c3e0a8be6f9d0e6e16f1525531954843e6165f275cf737b1d'
TERMINAL={'OWNED_MANIFEST.json','SEAL.json','CLOSURE.json'}
checks=[]
def require(ok,name):
    if not ok:raise AssertionError(name)
    checks.append(name)
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def read(p):return json.loads(Path(p).read_text())
def bound_file(p,e,label):
    p=Path(p)
    require(p.is_file() and not p.is_symlink(),label+':regular file')
    require(p.stat().st_size==e['bytes'] and sha(p)==e['SHA256'],label+':bytes/SHA256')

def validate_verdict(v):
    assert v['schema']=='row118_scope_literal_verdict_v1'
    assert v['record_id']==23385145 and v['native_version']=='1.0' and v['declared_date']=='2026-10-14'
    assert v['full_original_claim_supported'] is True
    assert v['substantive_gap_found'] is False and v['new_repair_supplied_by_review'] is False and v['narrowed_substitute_promoted'] is False
    i=v['exact_input'];assert all(i[k] is True for k in ('finite','nonempty','connected','simple'))
    assert i['edge_lengths']=='unit' and i['graph_category']=='promised median' and i['profile']=='finite nonnegative reals'
    assert i['representation']=='adjacency lists' and i['supplied_embedding_required'] is False and i['bounded_cube_dimension_required'] is False
    assert all(x is True for x in v['exact_output'].values())
    assert v['complexity']['encoding_independent_bit_bound'] is False and v['complexity']['deterministic_exact_operations']=='O(n log^5(2n))'
    assert v['proof_dependency_status']['correct_additive_integer_arrival_interface'] is True
    assert v['proof_dependency_status']['final_SODA_full_body_read'] is False
    for k in ('additive_algorithm_new','implicit_optimization_new','classical_median_structure_new','absolute_firstness_verified','worldwide_current_open_status_verified'):assert v['credit'][k] is False
    assert v['reproducibility']['fast_general_oracle_implementation_verified'] is False and v['reproducibility']['finite_controls_prove_asymptotic_theorem'] is False
    r=v['review_status']
    for k in ('human_peer_review','proof_assistant_certification','current_sibling_scientific_packets_read','root_118_initial_gate_open_at_packet_finalization','scientific_release_authorized','publication_authorized','site_or_tracker_change_authorized'):assert r[k] is False
    assert r['root_adoption'] is None
    assert v['source_ready_SHA256']==READY_SHA and v['initial_seal_SHA256']==INITIAL_SHA

def main():
    require(sha(SOURCE/'SOURCE_READY.json')==READY_SHA,'literal source-ready hash')
    require(sha(HERE/'INITIAL_SEAL.json')==INITIAL_SHA,'personal early seal unchanged')
    for e in read(HERE/'INPUT_MANIFEST.json')['inputs']:bound_file(e['path'],e,'input '+e['path'])
    owned=read(HERE/'OWNED_MANIFEST.json')
    expected={e['path'] for e in owned['files']}
    actual={str(p.relative_to(HERE)) for p in HERE.rglob('*') if p.is_file() and str(p.relative_to(HERE)) not in TERMINAL}
    require(actual==expected,'exact owned file set, terminal exclusions explicit')
    for e in owned['files']:
        p=HERE/e['path'];require(p.resolve().is_relative_to(HERE),'owned confinement '+e['path']);bound_file(p,e,'owned '+e['path'])
    ready=read(SOURCE/'SOURCE_READY.json')
    require(ready['record_id']==23385145 and ready['version']=='1.0' and ready['publication_date']=='2026-10-14','record/version/date literal')
    require(ready['created']=='2026-10-15T05:18:05.239497+00:00' and ready['updated']=='2026-10-15T05:18:05.515462+00:00','created/updated not substituted for declaration')
    require(ready['selected_actual_PDF']['pages']==5 and ready['controlling_TeX']['lines']==311,'actual entire manuscript identity')
    require(ready['target_manuscript_scientifically_read'] is False,'acquisition historical unread flag preserved')
    native={o['role']:read(o['path']) for o in ready['whole_native_API_objects']}
    require(native['record']['swh']=={} and [h['swh'] for h in native['versions_page_001']['hits']['hits']]==[None],'heterogeneous native swh retained: record dict, per-hit null, aggregate list')
    require(isinstance(native['files']['entries'],list) and native['files']['order']==[] and native['files']['default_preview'] is None,'native files schema and null retained')
    assets=ready['all_assets_in_original_order']
    require(native['record']['files']==[a['original_api_file_object'] for a in assets],'complete native file objects/order')
    for a in assets:
        b=Path(a['path']).read_bytes()
        require(hashlib.md5(b).hexdigest()==a['md5']==a['original_api_file_object']['checksum'].removeprefix('md5:'),'native MD5 '+a['path'])
        require(hashlib.sha256(b).hexdigest()==a['sha256'] and len(b)==a['bytes']==a['original_api_file_object']['size'],'complete native asset SHA/size '+a['path'])
    receipts=read(ready['actual_transport_receipt_path'])
    require(isinstance(receipts,dict) and len(receipts['receipts'])==7,'seven whole native transport objects')
    archive=read(ready['whole_archive_custody_path']);occ=archive['all_safe_regular_occurrences']
    zpath=Path(assets[1]['path'])
    with zipfile.ZipFile(zpath) as z:
        infos=z.infolist();require(len(infos)==len(occ)==93,'whole native ZIP directory count')
        require(z.testzip() is None,'whole native ZIP CRC')
        for inf,e in zip(infos,occ):
            path=PurePosixPath(inf.filename)
            require(not path.is_absolute() and '..' not in path.parts and not inf.is_dir() and stat.S_ISREG(inf.external_attr>>16),'safe native regular ZIP member '+inf.filename)
            require(inf.filename==e['original_member_name'] and inf.CRC==int(e['CRC32'],16) and inf.file_size==e['bytes'] and inf.compress_size==e['compressed_bytes'] and list(inf.date_time)==e['native_date_time'] and inf.external_attr==e['native_external_attr'],'native member order/CRC/size/date/attributes '+inf.filename)
            body=z.read(inf);require(hashlib.sha256(body).hexdigest()==e['SHA256']==sha(e['extracted_path']),'whole payload bytes '+inf.filename)
    require(archive['nested_archives']==0 and archive['expanded_bytes_all_depths']==705178,'archive scope unchanged')
    for rpath in sorted((HERE/'primary').glob('*.receipt.json')):
        r=read(rpath);p=Path(r['path']);require(p.resolve().is_relative_to(HERE/'primary'),'primary receipt body confinement')
        bound_file(p,r,'whole primary '+rpath.name)
        require(isinstance(r['headers_ordered'],list),'primary ordered headers retained '+rpath.name)
        require(p.read_bytes().startswith(b'%PDF-')==r['actual_PDF'],'actual primary PDF signature '+rpath.name)
    fail=read(HERE/'primary/SODA-final-attempt.receipt.json')
    require(fail['status']==403 and fail['actual_PDF'] is False,'failed final SODA transport preserved honestly')
    ledger=read(HERE/'READ_LEDGER.json')
    require(ledger['actual_target_PDF']['pages_personally_read']==list(range(1,6)) and ledger['actual_controlling_TeX']['all_lines_personally_read']==311,'literal personal full target ledger')
    require(len(ledger['honest_exposures'])==4 and ledger['initial_seal_precedes_all_118_foreign_code_results_opinions'] is True,'exposure and independent sequence retained')
    v=read(HERE/'VERDICT.json');validate_verdict(v);require(True,'custom verdict literal scope/limits')
    mutants=[(('exact_input','edge_lengths'),'arbitrary'),(('exact_input','graph_category'),'all graphs'),(('exact_output','entire_center_set'),False),(('complexity','encoding_independent_bit_bound'),True),(('proof_dependency_status','final_SODA_full_body_read'),True),(('proof_dependency_status','correct_additive_integer_arrival_interface'),False),(('credit','absolute_firstness_verified'),True),(('credit','implicit_optimization_new'),True),(('credit','worldwide_current_open_status_verified'),True),(('reproducibility','fast_general_oracle_implementation_verified'),True),(('reproducibility','finite_controls_prove_asymptotic_theorem'),True),(('review_status','human_peer_review'),True),(('review_status','proof_assistant_certification'),True),(('review_status','current_sibling_scientific_packets_read'),True),(('review_status','publication_authorized'),True),(('review_status','root_adoption'),'adopted')]
    for route,value in mutants:
        m=deepcopy(v);m[route[0]][route[1]]=value
        try:validate_verdict(m)
        except AssertionError:require(True,'synthetic mutation rejected '+'.'.join(route))
        else:raise AssertionError('accepted mutant '+str(route))
    c=read(HERE/'INDEPENDENT_CHECKS.json');require(c['status']=='PASS' and c['statistics']['profiles']==367 and c['statistics']['complete_threshold_vectors']==13455,'retained bounded control coverage')
    w=c['succinct_volume_witness'];N=w['N'];ell=w['cube_dimension'];t=w['leaves_at_unit_vertices'];q=1<<ell
    require(q+ell*t+w['leaves_at_zero']==N and w['minority']==q//2+t,'succinct median construction counts')
    require(56*w['minority']<N<2*(q-1+ell*t)==w['duplicated_volume'],'precise literal-volume negative witness')
    require(sum((Fraction(7)**j)/math.factorial(j) for j in range(12))>1000,'exact finite Taylor certificate, no float')
    b=read(HERE/'BOUNDARY_FALSIFIERS.json')
    require(b['strict_threshold_equality']['true_centers']==[1,2] and b['all_center_output']['required_centers']==[1,2],'multiple centers/equality falsifier')
    require(4*b['unweighted_row_middle_progress']['infeasible_entries_deleted']<b['unweighted_row_middle_progress']['M_before'],'unweighted row-middle progress mutant falsified')
    seal_checked=False
    if (HERE/'SEAL.json').exists():
        seal=read(HERE/'SEAL.json')
        for name,key in [('OWNED_MANIFEST.json','OWNED_MANIFEST_SHA256'),('INPUT_MANIFEST.json','INPUT_MANIFEST_SHA256'),('REPORT.md','REPORT_SHA256'),('VERDICT.json','VERDICT_SHA256'),('CLOSURE.json','CLOSURE_SHA256')]:require(sha(HERE/name)==seal[key],'final seal '+name)
        seal_checked=True
    print(json.dumps({'status':'PASS','read_only':True,'network_or_program_replay':False,'checks':len(checks),'input_files':len(read(HERE/'INPUT_MANIFEST.json')['inputs']),'owned_files':len(owned['files']),'synthetic_semantic_mutants_rejected':len(mutants),'whole_ZIP_payloads':93,'final_seal_checked':seal_checked,'scope':'custody and explicit report consistency; not a formal proof checker'},indent=2))

if __name__=='__main__':
    try:main()
    except Exception as e:
        print(json.dumps({'status':'FAIL','error':str(e),'checks_completed':len(checks)}));sys.exit(1)
