"""Root exact closed families and complete stored/actual result inspection."""
import datetime as dt
import hashlib
import json
import math
from pathlib import Path
A=Path(__file__).resolve().parent
def H(b):return hashlib.sha256(b).hexdigest()
def pairs(xs):
    d={}
    for k,v in xs:assert k not in d;d[k]=v
    return d
def number(s):v=float(s);assert math.isfinite(v);return v
def constant(s):raise ValueError(s)
def J(p):return json.loads(p.read_bytes(),object_pairs_hook=pairs,parse_float=number,parse_constant=constant)
objects={};readrows=[]
def item(p,z):
    assert p.is_file() and not p.is_symlink();b=p.read_bytes()
    assert type(z['bytes']) is int and len(b)==z['bytes'] and H(b)==z['sha256'],str(p)
    readrows.append(dict(path=str(p),bytes=len(b),sha256=H(b)))
    if p.suffix=='.json':objects[str(p.relative_to(A))]=J(p)
    return b
L=A/'literal_geometry_family';lm=J(L/'final_seal.json')
assert H((L/'final_seal.json').read_bytes())=='ad900516fdf42696ecfdc29f4e8c775fffa13ae7f49239e2127d8c46e381daae'
assert len(lm['first_party_closed_files'])==55 and len(lm['foreign_primary_excluded_files'])==25
lnames=[]
for z in lm['first_party_closed_files']+lm['foreign_primary_excluded_files']:
    assert z['path'] not in lnames;lnames.append(z['path']);item(L/z['path'],z)
assert {p.relative_to(L).as_posix() for p in L.rglob('*') if p.is_file()}==set(lnames)|{'final_seal.json'}
for z in lm['foreign_immutable_original_files_read']:item(A/'source_snapshot_v2'/z['path'],z)
for z in lm['foreign_parent_inputs_excluded']:assert H((L/z['path']).read_bytes())==z['sha256']
E=A/'exact_spectrum_family';em=J(E/'OWN_CLOSED_MANIFEST.json')
assert H((E/'OWN_CLOSED_MANIFEST.json').read_bytes())=='8817acbf2645b271cf9e28e553de30344648eb4192bbbe075e569a93e1bf387a'
assert len(em['own_files_including_self'])==42 and len(em['foreign_files_inside_root_individually_excluded'])==5
enames=[]
for z in em['own_files_including_self']+em['foreign_files_inside_root_individually_excluded']:
    p=Path(z['path']);assert p.is_relative_to(E);n=p.relative_to(E).as_posix();assert n not in enames;enames.append(n)
    if n=='OWN_CLOSED_MANIFEST.json':assert z['bytes'] is None and z['sha256'] is None
    else:item(p,z)
assert {p.relative_to(E).as_posix() for p in E.rglob('*') if p.is_file()}==set(enames)
for z in em['foreign_external_read_files_individually_pinned_and_excluded']:item(Path(z['path']),z)
verdict=J(E/'FAMILY_VERDICT.json');assert verdict['verdict']=='SCOPED_MATHEMATICS_VERIFIED' and verdict['mandatory_mathematical_corrections']==[] and verdict['full_target_resolved'] is False
O=A/'root_original_actual_reproduction_v2';om=J(O/'MANIFEST.json')
assert H((O/'MANIFEST.json').read_bytes())=='59043d2640eeabd4dadbad5bae1c238b470241270343d2d7cd75f919de83c46c'
for z in om['files']:item(O/z['path'],z)
assert {p.relative_to(O).as_posix() for p in O.rglob('*') if p.is_file()}=={z['path'] for z in om['files']}|{'MANIFEST.json'}
r=J(O/'RESULT.json');assert r['status']=='PASS_ROOT_GENUINE_ORIGINAL_REPRODUCTION' and r['author_assertions']==18306 and r['independent_assertions']==1263
assert r['whole_SQL_rows']==15458 and r['original_prior_raw_key_present'] is False
for run in r['actual_outer_runs']:
    assert run['actual_execution'] is run['completed'] is True and run['exit_code']==0 and type(run['pid']) is int and run['pid']>0
    for key in ['source','stdout','stderr','output_file']:item(O/run[key]['path'],run[key])
assert r['entire_original_independent_result']['passed']==len(r['entire_original_independent_result']['checks'])==1263
assert all(x=='PASS' for x in r['entire_original_independent_result']['checks'].values())
result=dict(status='PASS',utc=dt.datetime.now(dt.timezone.utc).isoformat(),literal_authored_members=55,literal_foreign_local_members=25,exact_authored_including_self=42,exact_foreign_local_members=5,complete_read_rows=readrows,complete_JSON_objects_consumed=len(objects),entire_exact_family_verdict=verdict,root_actual_result=r,root_full_reports_read=True,root_direct_primary_pages_read=[14,15],mandatory_provenance_correction='Absent raw prior key, not a null result; {} is only SQL fallback.',no_mathematical_correction_found=True,current_packet_and_new_whole_review_pending=True,new_substantive_attempts=0,audit_turns=0,full_problem_solved=False)
with (A/'ROOT_CLOSED_FAMILIES_INSPECTION.json').open('x') as out:json.dump(result,out,indent=2);out.write('\n')
print(json.dumps(dict(status='PASS',literal_owned=55,exact_owned_with_self=42,root_actual_pids=[x['pid'] for x in r['actual_outer_runs']],complete_JSON_objects=len(objects),inspection_sha256=H((A/'ROOT_CLOSED_FAMILIES_INSPECTION.json').read_bytes()))))
