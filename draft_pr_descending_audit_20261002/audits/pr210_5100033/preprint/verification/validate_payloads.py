"""Independent inventory/row checks, in addition to exact frozen JSON comparison."""
from pathlib import Path
from decimal import Decimal
from math import gcd
import hashlib,json
from integrity import BASE,digest
FAMILIES=['source_domain_adversary_01','physical_geometry_adversary_01','meromorphic_divisor_adversary_01','priority_author_updates_01','priority_classical_general_01']
PRIMARY_HASHES={'invariants_v11.pdf':'c56bb4ea29734ed04ee153206bb8619286df544714fd3f77fe97bdc945dfe1da','invariants_final.pdf':'c2a2e644521fd03a15833a23bd57c2498b5644036f6bc8fe682c40581f640d42','stachel_published.pdf':'9121028d7295435740cebb25ec60abe1a0dcc4e96686c226b1b6533bd49515d8'}

def load(p):return json.loads((BASE/p).read_text())
def require(x,label):
    if not x:raise ValueError(label)
def small(x,tol):
    v=Decimal(str(x));require(v.is_finite() and abs(v)<Decimal(tol),'Nonfinite/large residual: '+str(x))
def archive_checks():
    p=load('PROVENANCE.json');require(p['original_count']==20 and len(p['original_files'])==20,'original count')
    for r in p['original_files']:
        f=BASE/r['portable_path'];require(f.stat().st_size==r['bytes'] and digest(f)==r['sha256'],'original '+r['portable_path'])
    counts={}
    for family in FAMILIES:
        f=BASE/'audits'/family/'AUTHORED_MANIFEST.json'
        stated=next(x for x in p['families'] if x['family']==family)
        require(digest(f)==stated['manifest_sha256'],'family manifest '+family)
        m=json.loads(f.read_text());rows=m.get('authored_files',m.get('files'));counts[family]=len(rows)
        for r in rows:
            f=BASE/'audits'/family/r['path'];require(f.stat().st_size==r['bytes'] and digest(f)==r['sha256'],'family row '+family+'/'+r['path'])
    for name,prefix in [('MANIFEST.json','original_submission'),('independent_review/REVIEW_MANIFEST.json','original_submission/independent_review')]:
        m=load('original_submission/'+name)
        for rel,expected in m['files'].items():require(digest(BASE/prefix/rel)==expected,'original current manifest '+rel)
    old=load('original_submission/MANIFEST_V1.json');mismatches=[k for k,v in old['files'].items() if digest(BASE/'original_submission'/k)!=v]
    require(mismatches==['SOURCES.md'],'unexpected historical V1 mismatch set')
    require(old['files']['SOURCES.md']=='8abfe34830ecdb5e95124cc504d1696f360643466c310701f33b48e1853bc120','historical V1 source hash')
    primaries={r['file']:r['sha256'] for r in load('original_submission/source_manifest.json')['sources']}
    require(primaries==PRIMARY_HASHES,'primary source manifest')
    receipt={r['file']:r['sha256'] for r in load('audit_receipts/ROOT_SOURCE_READING_PROVENANCE.json')['sources']}
    require(receipt==primaries,'root source receipt')
    require(load('audits/meromorphic_divisor_adversary_01/results.json')['source_pdf_hashes']==primaries,'meromorphic frozen source hashes')
    hist=load('forensic_history/polarity_sign_intermediate_20261015/HISTORICAL_STATUS.json')
    for r in hist['files']:
        f=BASE/'forensic_history/polarity_sign_intermediate_20261015'/r['path'];require(f.stat().st_size==r['bytes'] and digest(f)==r['sha256'],'forensic row')
    correction=load('audit_receipts/ROOT_POLARITY_SIGN_CORRECTION.json')
    current=load('audit_receipts/ROOT_PROJECTIVE_PRESENTATION_RECONCILIATION.json')
    require(current['old_program']['sha256']==correction['corrected_program_sha256'],'historical corrected program binding')
    require(current['old_result']['sha256']==correction['corrected_result_sha256'],'historical corrected result binding')
    for item in ['old_program','old_result','current_program','current_result']:
        require(digest(BASE/current[item]['path'])==current[item]['sha256'],'projective reconciliation '+item)
    a=load(current['old_result']['path']);b=load(current['current_result']['path'])
    require({k:v for k,v in a.items() if k!='limits'}=={k:v for k,v in b.items() if k!='limits'},'unchanged projective algebra')
    require(current['changed_result_fields']==['limits'],'limited interpretation correction')
    return {'original_files':20,'family_payload_counts':counts,'family_manifests':5,'original_current_manifest_rows':17,'historical_V1_rows':len(old['files']),'historical_V1_documented_superseded_rows':mismatches,'forensic_manifest_rows':len(hist['files']),'attested_primary_hash_count':len(primaries)}

def result_checks(job,d):
    if job=='author':
        require(d['status']=='PASS' and d['exact_assertions']==20718 and d['primitive_odd_rotations']==4141 and d['direct_geometry_odd_families']==82 and d['numerical_comparisons']==15076 and d['complex_pole_cases']==8,'author counts')
        require(len(d['even_parity_countercontrols'])==8,'author even rows')
        for r in d['even_parity_countercontrols']:require(Decimal(r['relative_change'])>Decimal('1e-15'),'author negative control')
        small(d['max_normalized_numerical_error'],'1e-68');small(d['max_finite_epsilon_pole_error'],'1e-17')
        return {'exact_assertions':20718,'finite_rotations':4141,'uncertified_comparisons':15076,'real_odd_families':82,'complex_pole_cases':8,'even_controls':8}
    if job=='inherited':
        require(d['status']=='PASS' and d['exact_assertions']==9303 and d['primitive_rotations_checked']==1104 and d['numerical_comparisons']==4941 and d['real_families']==27 and d['complex_pole_cases']==27,'inherited counts')
        small(d['max_scaled_error'],'1e-16');small(d['max_finite_epsilon_residue_error'],'1e-16')
        return {'exact_assertions':9303,'finite_rotations':1104,'uncertified_comparisons':4941,'real_families':27,'complex_pole_cases':27}
    if job=='source_domain':
        require(len(d['symbolic_checks'])==5 and all(d['symbolic_checks'].values()),'source symbolic')
        require(d['real_family_count']==86 and len(d['real_families'])==86 and len(d['analytic_diagnostics'])==3 and len(d['exact_lattice_controls'])==236,'source counts')
        for r in d['real_families']:
            require(gcd(r['N'],r['tau'])==1 and r['least_period']==r['N'],'source primitive')
            require(len(r['products_over_a4'])==len(r['winding_values'])==5,'source phase count')
            for v in r['errors'].values():small(v,'1e-57')
            for v in r['winding_values']:small(Decimal(v)-r['tau'],'1e-57')
            if r['N']%2:small(r['product_span'],'1e-57')
            require(Decimal(r['min_outer_side_over_a'])>0 and Decimal(r['min_tangent_determinant_scaled'])>0,'source sides')
        for r in d['analytic_diagnostics']:
            for v in r['identity_errors'].values():small(v,'1e-55')
            require(len(r['simple_pole_diagnostic'])==3,'source pole samples')
        for r in d['exact_lattice_controls']:
            require(gcd(r['N'],r['tau'])==1 and r['distinct_phase_classes']==r['N'] and r['singular_indices_at_zminus']==[0,1] and r['focus_shift_is_half_period']==bool(r['N']%2),'source lattice row')
        return {'symbolic_zero_identities':5,'real_families':86,'odd_rows_including_two_scaling_controls':82,'even_rows':4,'phases':430,'analytic_cases':3,'finite_lattice_cases':236}
    if job=='physical_geometry':
        require(d['all_passed'] and d['even_product_nonconstancy_detected_in_every_even_control'] and d['exact']['passed'],'physical status')
        require(d['case_count']==len(d['cases'])==22,'physical cases')
        for r in d['cases']:
            require(r['passed'] and r['strictly_nested_elliptic'] and gcd(r['N'],r['turn'])==1,'physical case status')
            require(len(r['phases'])==r['phase_count'],'physical phase count')
            for v in r['max_errors'].values():small(v,'1e-48')
            for k in ['focus_pairing_error','orientation_reversal_error','cyclic_shift_error','scaling_degree_four_error','isometry_error']:small(r[k],'1e-48')
            if r['N']%2:small(r['product_spread_normalized'],'1e-48')
            else:require(Decimal(r['product_spread_normalized'])>Decimal('1e-8'),'physical even negative');small(r['focus_area_difference_normalized'],'1e-48')
            for phase in r['phases']:
                for k in ['closure','boundary','caustic_tangency','reflection','outer_side','independent_projection_agreement','auxiliary_circle','winding_error']:small(phase[k],'1e-48')
                require(Decimal(phase['min_pair_separation'])>Decimal('1e-40') and Decimal(phase['min_adjacent_tangent_det'])>0,'physical distinctness')
        for r in d['exact']['two_exact_distinct_family_triangles']:require(r['all_exact_boundary_reflection_tangency_outer_side_circle_checks_zero'] and r['product']=='12544/25','physical exact triangle')
        return {'cases':22,'strict_odd_cases':17,'even_controls':4,'circle_extension_case':1,'phase_rows':sum(len(r['phases']) for r in d['cases']),'exact_triangles':2}
    if job=='meromorphic_divisor':
        require(len(d['exact_symbolic']['checks'])==11 and all(d['exact_symbolic']['checks'].values()),'meromorphic exact')
        l=d['lattice_enumeration'];require(l['primitive_cases']==3503 and l['pole_phase_checks']==354690 and l['all_exact_fraction_assertions_pass'],'meromorphic lattice count')
        require(len(l['selected_certificates'])==88,'meromorphic selected count')
        for r in l['selected_certificates']:
            require(gcd(r['N'],r['tau'])==1 and r['orbit_size']==r['adjacent_pairs']==r['N'] and r['bezout'][0]*r['tau']+r['bezout'][1]*r['N']==1,'meromorphic Bezout row')
        rows=d['high_precision']['families'];require(len(rows)==11 and d['high_precision']['all_numeric_assertions_pass'] and not d['high_precision']['interval_certification'],'meromorphic numerical status')
        for r in rows:
            for k,v in r['character_and_geometry_errors'].items():small(v,'1e-24' if 'removable' in k else '1e-90')
            for k in ['wrong_cn_period_residual','wrong_dn_real_shift_sign_residual']:require(Decimal(r[k])>Decimal('1.99'),'meromorphic negative control')
            require(len(r['complex_pole_controls'])==3 and len(r['normalized_product_samples'])==3,'meromorphic pole rows')
            small(r['complex_pole_controls'][-1]['T_residue_error'],'1e-26');small(r['complex_pole_controls'][-1]['mutant_double_pole_error'],'1e-25')
            if not r['N']%2:require(Decimal(r['normalized_product_spread'])>Decimal('1e-12'),'meromorphic even control')
        return {'symbolic_checks_including_mutant':11,'finite_primitive_cases':3503,'pole_phase_checks':354690,'selected_Bezout_certificates':88,'numerical_families':11,'complex_pole_rows':33}
    if job=='priority_author':
        require(d['all_checks_pass'] and d['check_count']==len(d['checks'])==84 and all(r['pass'] for r in d['checks']),'priority author checks')
        require(set(d['phases'])=={'H','V'},'priority author phases')
        return {'exact_finite_checks':84,'exact_triangular_phases':2}
    if job=='priority_classical':
        require(len(d['exact']['zero_identities'])==15 and all(v=='0' for v in d['exact']['zero_identities'].values()),'classical exact')
        require(len(d['numerical'])==11,'classical case count')
        for r in d['numerical']:
            require(len(r['samples'])==5,'classical phases')
            for v in r['max_errors'].values():small(v,'1e-45')
            if r['N']%2:small(r['relative_product_range'],'1e-40')
            else:require(Decimal(r['relative_product_range'])>Decimal('1e-10'),'classical negative control')
        ce=d['exact']['nonconfocal_homothetic_N3_counterexample']['phases'];require(len(ce)==2 and ce[0]['product']!=ce[1]['product'],'classical counterexample')
        return {'exact_zero_identities':15,'numerical_cases':11,'numerical_phase_rows':55,'exact_nonconfocal_counterexample_phases':2}
    if job=='root_exact_geometry':
        require(d['exact_zero_assertions']==113 and len(d['phases'])==2 and all(r['outer_product']=='12544/25' for r in d['phases']),'root geometry')
        return {'exact_zero_assertions':113,'exact_triangular_phases':2}
    if job=='root_exact_even':
        require(d['primitive_period']==4 and d['caustic_lambda']=='4/5' and d['exact_zero_count']==96,'exact even parameters/count')
        require([x['outer_pedal_product'] for x in d['cases']]==['16','25'],'exact even products')
        require([x['original_unit_inverse_product'] for x in d['cases']]==['1','25/16'],'corrected source inverse products')
        for r in d['cases']:
            require(r['exact_zero_count']==48 and len(r['zero_residuals'])==48 and set(r['zero_residuals'].values())=={'0'},'exact even residuals')
        require(d['literal_printed_Ferudun0062_p6_rectangle']['genuine_billiard'] is False,'source false fixture labelled')
        return {'exact_zero_residuals':96,'genuine_primitive_even_phases':2,'source_false_fixture':1}
    if job=='root_projective':
        require(len(d['checks'])==10 and all(v=='0' for v in d['checks'].values()) and d['polar_dual_circle']['exact_triangle_center_x']=='-21*sqrt(5)/4','root corrected projective')
        return {'exact_zero_identities':10,'corrected_plus_focus_polarity':True}
    raise ValueError('Unknown job')
