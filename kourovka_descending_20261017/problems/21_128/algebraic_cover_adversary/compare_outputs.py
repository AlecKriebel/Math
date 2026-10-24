#!/usr/bin/env python3
"""Cross-check independently generated lattices against frozen author data."""
from collections import Counter
from fractions import Fraction
from pathlib import Path
import hashlib, json, datetime

HERE=Path(__file__).resolve().parent
AUTHOR=HERE.parent/'common_cover'
def load(path):return json.loads(path.read_text())
manifest=load(AUTHOR/'FROZEN_MANIFEST.json')
for name,expected in manifest['files_sha256'].items():
    assert hashlib.sha256((AUTHOR/name).read_bytes()).hexdigest()==expected,name
frozen=load(AUTHOR/'log_volume_data.json')
replayed=load(HERE/'author_reproduction.json')
for kind in frozen:
    a=dict(frozen[kind]);b=dict(replayed[kind])
    del a['elapsed_seconds'];del b['elapsed_seconds']
    assert a==b,kind
author={**frozen,**load(AUTHOR/'known_cover_checks.json')}
independent=load(HERE/'cartan_reproduction.json')
results={}
for kind,d in author.items():
    v=independent[kind]
    correspondence={'hyperplane_count':'root_line_count',
       'initial_cube':'initial_cube','point_cube_correction':'point_correction',
       'final_log_divisor_cube':'log_volume',
       'projective_complement_euler':'euler_characteristic',
       'volume_over_abs_euler':'ratio',
       'line_multiplicity_histogram':'line_histogram',
       'point_multiplicity_histogram':'point_histogram'}
    for x,y in correspondence.items():assert d[x]==v[y],(kind,x,d[x],v[y])
    line_count=Counter((x['multiplicity'],x['D_dot_line'],x['normal_degree'],x['cube_correction'])
                       for x in d['projective_lines'])
    other=Counter({(x['m'],x['d'],x['normal'],x['term']):x['count']
                   for x in v['line_cube_term_profiles']})
    assert line_count==other,(kind,'line_term_profiles')
    points=list(map(frozenset,d['projective_points']))
    lines=[frozenset(x['hyperplanes']) for x in d['projective_lines']]
    point_profiles=Counter((len(p),tuple(sorted(Counter(len(l) for l in lines if l<=p).items())))
                           for p in points)
    other=Counter({(x['multiplicity'],tuple(sorted((int(k),n) for k,n in x['line_multiplicities'].items()))):x['count']
                   for x in v['point_line_profiles']})
    assert point_profiles==other,(kind,'point_line_profiles')
    line_profiles=Counter((len(l),tuple(sorted(Counter(len(p) for p in points if l<=p).items())))
                           for l in lines)
    other=Counter({(x['multiplicity'],tuple(sorted((int(k),n) for k,n in x['point_multiplicities'].items()))):x['count']
                   for x in v['line_point_profiles']})
    assert line_profiles==other,(kind,'line_point_profiles')
    results[kind]={'root_count':v['root_count'],'root_lines':v['root_line_count'],
                  'rank2_flats':v['rank2_count'],'rank3_flats':v['rank3_count'],
                  'volume':v['log_volume'],'euler':v['euler_characteristic'],
                  'ratio':v['ratio'],'all_compared_quantities_match':True}
assert independent['B4']['log_volume']==8*independent['A4']['log_volume']
assert independent['B4']['euler_characteristic']==8*independent['A4']['euler_characteristic']
difference=Fraction(independent['F4']['ratio'])-Fraction(independent['H4']['ratio'])
assert difference==Fraction(3,20)
out={'timestamp':datetime.datetime.now(datetime.timezone.utc).isoformat(),
     'frozen_input_recheck':'all matched',
     'exact_author_replay':'all fields matched except elapsed times',
     'independent_cartan_and_rref_results':results,
     'ratio_difference':str(difference),'positive_control_cover_degree':8,
     'verdict':'PASS for the stated bounded algebraic-cover theorem only'}
(HERE/'COMPARISON_RESULT.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
