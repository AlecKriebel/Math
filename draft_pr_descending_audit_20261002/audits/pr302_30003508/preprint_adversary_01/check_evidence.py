"""Independent provenance, scientific-field and source/render custody crosscheck."""
from pathlib import Path
from datetime import datetime,timezone
import difflib,gzip,hashlib,json,math,os,stat
R=Path(__file__).resolve().parent; A=R.parent; F=A/'preprint_package_v01'; W=R.parents[3]
def pin(p):
    p=Path(p);b=p.read_bytes()
    return {'path':str(p),'resolved_path':str(p.resolve()),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'mode':stat.S_IMODE(p.stat().st_mode)}
def write(p,o):p.write_text(json.dumps(o,indent=2,ensure_ascii=False)+'\n')
cases=json.loads((F/'CONTROL_CASES.json').read_bytes())
expected=json.loads((F/'EXPECTED_SCIENTIFIC_OUTPUTS.json').read_bytes())
provenance=json.loads((F/'PAYLOAD_PROVENANCE.json').read_bytes())
receipt=json.loads((R/'portable_replay'/'REPLAY_RECEIPT.json').read_bytes())
assert receipt['status']=='PASS_ALL_EIGHT_FINITE_CONTROL_SUITES'
assert receipt['runtime']['optimization']==0 and receipt['runtime']['sympy']=='1.14.0'
leaf_counts={'float':0,'exact_nonfloat':0}; differences=[];case_rows=[]
def compare(a,b,path):
    if isinstance(b,dict):
        assert type(a)==dict and a.keys()==b.keys(),path
        for k,v in b.items():compare(a[k],v,path+'.'+k)
    elif isinstance(b,list):
        assert type(a)==list and len(a)==len(b),path
        for i,(av,bv) in enumerate(zip(a,b)):compare(av,bv,path+'['+str(i)+']')
    elif type(b)==float:
        assert type(a) in (float,int) and math.isfinite(a),path
        diff=abs(a-b); bound=max(1e-14,1e-12*max(abs(a),abs(b)))
        assert diff<=bound,path
        leaf_counts['float']+=1
        if a!=b:differences.append({'path':path,'actual':a,'expected':b,'absolute_difference':diff,'accepted_bound':bound})
    else:
        assert type(a)==type(b) and a==b,path
        leaf_counts['exact_nonfloat']+=1
for case in cases:
    d=R/'portable_replay'/case['label'];exe=json.loads((d/'execution.json').read_bytes())
    assert exe['exit_code']==0 and exe['actual_child_PID']>0
    assert exe['runtime']['optimization']==0 and exe['runtime']['sympy']=='1.14.0'
    for key in ('stdout','stderr'):
        stream=exe[key];p=Path(stream['stored']['path']);body=gzip.decompress(p.read_bytes())
        assert len(body)==stream['logical_bytes'] and hashlib.sha256(body).hexdigest()==stream['logical_sha256']
        assert all(pin(p)[k]==stream['stored'][k] for k in ('bytes','sha256'))
        if key=='stderr':assert not body
    raw=json.loads(gzip.decompress((d/'stdout.bin.gz').read_bytes()) if case['output']=='stdout' else (d/case['output']).read_bytes())
    selected={k:raw[k] for k in case['scientific_fields']}
    assert selected==json.loads((d/'scientific_output.json').read_bytes())
    compare(selected,expected[case['label']],case['label'])
    row=next(x for x in provenance['payload_sources'] if x['package_path']==case['source'])
    original=W/row['original_source'];baseline=W/row['historical_expected_output']
    assert (F/case['source']).read_bytes()==original.read_bytes()
    assert all(pin(original)[k]==row[k] for k in ('bytes','sha256'))
    assert pin(baseline)['bytes']==row['baseline_bytes'] and pin(baseline)['sha256']==row['baseline_sha256']
    historical=json.loads(baseline.read_bytes());assert {k:historical[k] for k in case['scientific_fields']}==expected[case['label']]
    assert (d/Path(case['source']).name).read_bytes()==original.read_bytes()
    case_rows.append({'label':case['label'],'PID':exe['actual_child_PID'],'started_UTC':exe['started_UTC'],'completed_UTC':exe['completed_UTC'],
                      'exit_code':exe['exit_code'],'fields':case['scientific_fields'],'source':pin(original),'baseline':pin(baseline),
                      'actual_execution_receipt':pin(d/'execution.json'),'scientific_output':pin(d/'scientific_output.json')})
note_diffs=[]
for row in provenance['payload_sources'][8:]:
    a=W/row['original_source'];b=F/row['package_path']
    assert pin(a)['bytes']==row['original_bytes'] and pin(a)['sha256']==row['original_sha256']
    assert pin(b)['bytes']==row['public_bytes'] and pin(b)['sha256']==row['public_sha256']
    diff=''.join(difflib.unified_diff(a.read_text().splitlines(True),b.read_text().splitlines(True),fromfile=row['original_source'],tofile=row['package_path']))
    assert diff==row['wording_diff']
    note_diffs.append({'original':pin(a),'public':pin(b),'exact_diff':diff})
build=json.loads((F/'BUILD_RECEIPT_02.json').read_bytes())
pages=[pin(F/'private_build_02'/'pages'/('page-%d.png'%n)) for n in range(1,9)]
# Retain full existing extracted sources; do not duplicate large raw PDFs.
S=R/'retained_source_texts';S.mkdir()
sources=[
 ('reiss_original','math_scope_adversary_01/reiss_contribution_1507_1509.txt','math_scope_adversary_01/OWR_2017_24.pdf'),
 ('ems_identity','math_scope_adversary_01/ems_identity.text.txt',None),
 ('grubb_graph','math_empirical_adversary_01/grubb_regular_spectral_primary.txt','math_empirical_adversary_01/grubb_regular_spectral_primary.pdf'),
 ('grubb_sobolev','math_spectral_adversary_01/private_primary_sources/Grubb_dist6.txt','math_spectral_adversary_01/private_primary_sources/Grubb_dist6.pdf'),
 ('hansen1993_ocr','priority_mechanism_adversary_01/private_sources/hansen1993_ocr.txt','priority_mechanism_adversary_01/private_sources/hansen1993.pdf'),
 ('cv2006','priority_target_adversary_01/private_sources/cv2006.txt','priority_target_adversary_01/private_sources/cv2006.pdf'),
 ('cv2011_cwi','priority_target_adversary_01/private_sources/cv2011.txt','priority_target_adversary_01/private_sources/cv2011.pdf'),
 ('chen2009','priority_target_adversary_01/private_sources/chen2009_author.txt','priority_target_adversary_01/private_sources/chen2009_author.pdf'),
 ('gobet2004','priority_target_adversary_01/private_sources/gobet.txt','priority_target_adversary_01/private_sources/gobet.pdf'),
 ('chorowski_v2','priority_target_adversary_01/private_sources/chorowski.txt','priority_target_adversary_01/private_sources/chorowski.pdf'),
 ('nickl_v3','priority_target_adversary_01/private_sources/nickl.txt','priority_target_adversary_01/private_sources/nickl.pdf'),
 ('gw_v3','priority_target_adversary_01/private_sources/gw2025.txt','priority_target_adversary_01/private_sources/gw2025.pdf'),
 ('abjn_v2','priority_target_adversary_01/private_sources/abjn.txt','priority_target_adversary_01/private_sources/abjn.pdf'),
 ('bal2013','priority_mechanism_adversary_01/private_sources/bal2013_author.txt','priority_mechanism_adversary_01/private_sources/bal2013_author.pdf.xz'),
 ('kohn1988','priority_mechanism_adversary_01/private_sources/kohn1988.txt','priority_mechanism_adversary_01/private_sources/kohn1988.pdf.xz'),
 ('lenzen2004','priority_mechanism_adversary_01/private_sources/lenzen2004.txt','classical_reduction_adversary_01/sources/lenzen2004.pdf'),
 ('hansen2008','priority_mechanism_adversary_01/private_sources/hansen2008.txt','priority_mechanism_adversary_01/private_sources/hansen2008.pdf.xz')]
source_rows=[]
for name,txt,raw in sources:
    p=A/txt;q=S/(name+'.txt');q.write_bytes(p.read_bytes());q.chmod(0o444)
    source_rows.append({'label':name,'original_extract':pin(p),'retained_complete_extract':pin(q),
                        'raw_body':pin(A/raw) if raw and (A/raw).is_file() else None,
                        'raw_body_locator':str(A/raw) if raw else None})
S.chmod(0o555)
review={'UTC':datetime.now(timezone.utc).isoformat(),'PID':os.getpid(),'status':'PASS_INDEPENDENT_PROVENANCE_SCIENTIFIC_COMPARISON_AND_SOURCE_CUSTODY',
        'case_count':len(case_rows),'cases':case_rows,'leaf_counts':leaf_counts,'floating_differences':differences,
        'note_diffs':note_diffs,'page_pins':pages,'source_pins':source_rows,'build_receipt_pin':pin(F/'BUILD_RECEIPT_02.json'),
        'PDF_text_pin':pin(R/'FINAL_PDF_TEXT.txt'),'limits':'Entire scientific output trees and full control source inspected separately in the review. Raw source PDFs are reused read-only with these exact pins. Retaining a full extract is not a claim to have read every unrelated page.'}
write(R/'EVIDENCE_CROSSCHECK.json',review)
print(json.dumps({'status':review['status'],'case_count':len(case_rows),'leaf_counts':leaf_counts,'floating_differences':len(differences)},indent=2))
