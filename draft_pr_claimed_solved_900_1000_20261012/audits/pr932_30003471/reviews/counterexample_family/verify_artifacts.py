#!/usr/bin/env python3
"""Independent stored-coordinate receipt checks; optionally deterministic replay.

Usage: python verify_artifacts.py [--reproduce]
The verifier never imports or executes the author's original packet.
"""
import hashlib,itertools,json,pathlib,sys,contextlib,io,math
from datetime import datetime,timezone
import numpy as np
from scipy.spatial import ConvexHull

HERE=pathlib.Path(__file__).resolve().parent

def check_poly(normals,supports,claimed):
    a=np.array(normals);b=np.array(supports)
    assert np.max(abs(np.linalg.norm(a,axis=1)-1))<1e-10
    hull=ConvexHull(a)
    assert np.max(hull.equations[:,-1])<-1e-7
    corners=[]
    for inds in itertools.combinations(range(len(a)),3):
        aa=a[list(inds)]
        if abs(np.linalg.det(aa))<1e-10:continue
        point=np.linalg.solve(aa,b[list(inds)])
        if max(a@point-b)>2e-7:continue
        if any(np.linalg.norm(point-v)<2e-6 for v in corners):continue
        corners.append(point)
    assert len(corners)>=4
    inc=sorted(tuple(map(int,np.where(abs(a@v-b)<2e-6)[0])) for v in corners)
    assert inc==[tuple(v) for v in claimed['incidence']]
    assert abs(ConvexHull(corners).volume-claimed['volume'])<1e-8
    edges=[]
    for i,j in itertools.combinations(range(len(a)),2):
        members=[v for v in inc if i in v and j in v]
        if len(members)>=2:edges.append([i,j])
    assert edges==claimed['edges']
    return a,edges

def stored_check():
    counts=dict(families=0,trials=0,strict_candidates=0,weak_candidates=0)
    best=-2.;details=[]
    for name in ['SEARCH_RESULTS.json','EXTENDED_SEARCH_RESULTS.json']:
        data=json.loads((HERE/name).read_text())
        for family,search in data['searches'].items():
            counts['families']+=1
            p,edges=check_poly(search['p_normals'],search['p_supports'],search['p_polytope'])
            for t in search['trials']:
                assert 'error' not in t
                counts['trials']+=1
                q,qedges=check_poly(t['q_normals'],t['q_supports'],t['q_polytope'])
                assert qedges==edges and t['topology_equal'] and t['constraints_valid']
                diff=np.array([q[i]@q[j]-p[i]@p[j] for i,j in edges])
                assert max(abs(diff-np.array(t['edge_dot_differences'])))<1e-12
                assert abs(float(min(diff))-t['minimum_dot_difference'])<1e-12
                gap=float(np.sum((q@q.T-p@p.T)**2))
                assert abs(gap-t['gram_separation_squared'])<1e-10 and gap>=.01-1e-7
                strict=bool(min(diff)>1e-7);weak=bool(min(diff)>=-1e-9)
                assert strict==t['numerical_candidate_strict'] and weak==t['numerical_candidate_weak']
                counts['strict_candidates']+=strict;counts['weak_candidates']+=weak
                best=max(best,float(min(diff)))
            details.append(dict(family=family,trials=len(search['trials']),
                best_minimum_dot_difference=max(t['minimum_dot_difference'] for t in search['trials'])))
    assert counts==dict(families=18,trials=60,strict_candidates=0,weak_candidates=0)
    original=json.loads((HERE/'SEARCH_RESULTS.json').read_text())['searches']['pyramid_8']['local_lp']
    assert original['positive_stress_success'] is False and original['min_normalized_stress'] is None
    supplemental=json.loads((HERE/'EXTENDED_SEARCH_RESULTS.json').read_text())['supplemental_tolerance_stress_for_original_pyramid8']
    assert supplemental['success'] and not supplemental['exact_certificate']
    assert supplemental['residual_within_allowed']==(supplemental['residual']<=supplemental['allowed_residual'])
    return dict(status='PASS_FOR_STORED_COORDINATE_RECEIPTS',counts=counts,
        best_minimum_dot_difference=best,families=details,
        original_pyramid8_exact_equality_dual_failure_preserved=True,
        supplemental_pyramid8_stress_residual_valid=supplemental['residual_within_allowed'])

def prune(data):
    if isinstance(data,dict):return {k:prune(v) for k,v in data.items() if k not in ['started_utc','finished_utc','elapsed_seconds']}
    if isinstance(data,list):return [prune(v) for v in data]
    return data

def same(a,b):
    if type(a)!=type(b):return False
    if isinstance(a,dict):return a.keys()==b.keys() and all(same(a[k],b[k]) for k in a)
    if isinstance(a,list):return len(a)==len(b) and all(same(x,y) for x,y in zip(a,b))
    if isinstance(a,float):return math.isclose(a,b,rel_tol=1e-9,abs_tol=1e-9)
    return a==b

def replay():
    import controls as c
    import extended_controls as e
    destination=HERE/'tmp'/'reproduction';destination.mkdir(parents=True,exist_ok=True)
    c.HERE=destination
    with (destination/'REPLAY_STDOUT.txt').open('w') as out,contextlib.redirect_stdout(out):
        c.main();e.main()
    names=['SEARCH_RESULTS.json','EXTENDED_SEARCH_RESULTS.json','CONSTRUCTIVE_CONTROLS.json']
    records=[]
    for name in names:
        actual=json.loads((destination/name).read_text());expected=json.loads((HERE/name).read_text())
        equal=same(prune(actual),prune(expected))
        records.append(dict(file=name,equal_excluding_timestamps_and_elapsed=equal,numerical_tolerance=1e-9))
    assert all(r['equal_excluding_timestamps_and_elapsed'] for r in records)
    return dict(status='PASS_DETERMINISTIC_REPLAY',seed_primary=c.SEED,seed_extended=e.SEED,records=records,
        private_replay_directory='tmp/reproduction (excluded from curated public manifest)')

def main():
    result=dict(utc=datetime.now(timezone.utc).isoformat(),stored=stored_check())
    if '--reproduce' in sys.argv:result['reproduction']=replay()
    (HERE/'VERIFICATION_RECEIPT.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'stored':result['stored']['status'],'counts':result['stored']['counts'],
        'reproduction':result.get('reproduction',{}).get('status')},sort_keys=True))

if __name__=='__main__':main()
