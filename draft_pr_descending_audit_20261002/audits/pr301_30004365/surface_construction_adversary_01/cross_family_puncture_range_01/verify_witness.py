#!/usr/bin/env python3
"""Cross-family witness check through the previously independent lozenge code."""
import collections, datetime, gzip, hashlib, json, pathlib, sys
ROOT=pathlib.Path(__file__).resolve().parent
PARENT=ROOT.parent
sys.path.insert(0,str(PARENT))
import surface_fixture_audit as independent_surface

def quiver(m,n):
    # Index a_i by i and b_j by m+j; arrow u_i by i, v_j by m+j, z by m+n.
    arrows=[(i,(i+1)%m) for i in range(m)]
    arrows += [(m+j,m+(j+1)%n) for j in range(n)]
    arrows += [(0,m)]
    rels={(i,(i+1)%m) for i in range(m)}
    rels |= {(m+j,m+(j+1)%n) for j in range(n)}
    return m+n,arrows,rels

def all_paths(vertex_count,arrows,rels):
    # Exact monomial path basis: all vertices and all nonzero arrow sequences.
    result=[('vertex',i) for i in range(vertex_count)]
    for first in range(len(arrows)):
        todo=[(first,)]
        while todo:
            path=todo.pop(); result.append(path)
            for nxt,(s,t) in enumerate(arrows):
                if arrows[path[-1]][1]==s and (path[-1],nxt) not in rels:
                    assert nxt not in path, 'unexpected permitted cycle'
                    todo.append(path+(nxt,))
    return result

def verify(m,n):
    N,arrows,rels=quiver(m,n)
    assert independent_surface.local_extensions(N,arrows,rels) is not None
    assert independent_surface.finite(arrows,rels)
    exact=independent_surface.audit(N,arrows,rels)
    paths=all_paths(N,arrows,rels)
    lengths=collections.Counter(0 if p[0]=='vertex' else len(p) for p in paths)
    components=exact['certificate']['surface']
    assert len(components)==1
    c=components[0]
    boundary=c['boundary_collar_records'];punctures=c['puncture_collar_records']
    target={'original_vertices':8,'original_arrows':9,'dimension':20,
            'g':0,'b':1,'p':2,'white_marks':[7],'black_marks':[7],
            'outer_windings':[6],'puncture_windings':sorted([-m,-n])}
    actual={'original_vertices':N,'original_arrows':len(arrows),'dimension':len(paths),
            'g':c['g'],'b':c['b'],'p':c['black_interior'],
            'white_marks':[b['white'] for b in c['boundary_marks']],
            'black_marks':[b['black'] for b in c['boundary_marks']],
            'outer_windings':[b['w'] for b in boundary],
            'puncture_windings':sorted(p['w'] for p in punctures)}
    assert actual==target,(actual,target)
    assert lengths=={0:8,1:9,2:2,3:1}
    assert c['chi']-c['black_interior']==-1
    assert c['white_interior']==0
    key=sorted((r['n'],r['w']) for r in boundary+punctures)
    return {'m':m,'n':n,'actual':actual,'path_length_counts':dict(sorted(lengths.items())),
            'exact_monomial_path_basis':paths,'full_peripheral_key':key,
            'AG_pairs':sorted((r['n'],r['n']-r['w']) for r in boundary+punctures),
            'lozenge_certificate':exact}

module=pathlib.Path(independent_surface.__file__).read_bytes()
(ROOT/'imported_surface_fixture_audit.py.gz').write_bytes(gzip.compress(module))
cases={f'A({m},{n})':verify(m,n) for m,n in [(3,5),(4,4)]}
a,b=cases.values()
assert a['actual']|{'puncture_windings':None}==b['actual']|{'puncture_windings':None}
assert a['full_peripheral_key'] != b['full_peripheral_key']
result={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'mechanism':'Exact oriented lozenge quotient, vertex links and collar sectors; separate monomial path enumeration.',
        'imported_module_sha256':hashlib.sha256(module).hexdigest(),'cases':cases,
        'conclusion':'Claimed numerical witness verified; full peripheral keys differ.'}
(ROOT/'RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'utc':result['utc'],'module_sha256':result['imported_module_sha256'],
                  'cases':{k:{f:v[f] for f in ('actual','path_length_counts','full_peripheral_key','AG_pairs')} for k,v in cases.items()},
                  'conclusion':result['conclusion']},indent=2))
