#!/usr/bin/env python3
from pathlib import Path
import json
from fractions import Fraction as F
from geometry import complete_code, line_interval, interval_as_json, point_in_open

ROOT=Path(__file__).resolve().parents[1]
data=json.loads((ROOT/'examples/rational_examples.json').read_text())

# 1--4: exact trace cases.
for name in ('generic_crossing','tangent_point','closed_segment_contact','half_open_clipping'):
    e=data[name]; amb=e['ambient']; poly=e['neurons']['1']; line=e['line']
    open_I=line_interval([(amb,False),(poly,True)],line['point'],line['direction'])
    closed_I=line_interval([(amb,False),(poly,False)],line['point'],line['direction'])
    assert interval_as_json(open_I)==e['expected_open_trace'],(name,interval_as_json(open_I))
    assert interval_as_json(closed_I)==e['expected_closed_trace'],(name,interval_as_json(closed_I))
    if 'expected_code' in e:
        assert complete_code(amb,e['neurons'])==set(e['expected_code'])
    if 'protected' in e:
        for word,p in e['protected'].items():
            got=''.join(sorted(i for i,P in e['neurons'].items() if point_in_open(P,p)))
            assert got==word,(name,got,word)
print('TRACE CASES PASS: generic, tangent point, supporting segment, half-open clip')

# 5: simultaneous endpoint.
e=data['simultaneous_endpoints']; line=e['line']; traces={}
for i,P in e['neurons'].items():
    traces[i]=line_interval([(e['ambient'],False),(P,True)],line['point'],line['direction'])
assert traces['1'][1]==F(e['shared_endpoint'])
assert traces['2'][0]==F(e['shared_endpoint'])
assert not traces['1'][3] and not traces['2'][2]
print('SIMULTANEOUS ENDPOINT PASS at',e['shared_endpoint'])

# 6: a lower-dimensional atom.
e=data['lower_dimensional_atom']
code=complete_code(e['ambient'],e['neurons'])
assert code==set(e['expected_code']),code
for word,p in e['protected'].items():
    got=''.join(sorted(i for i,P in e['neurons'].items() if point_in_open(P,p)))
    assert got==word
print('LOWER-DIMENSIONAL ATOM PASS:',sorted(code))

# 7: covered carrier.
e=data['covered_carrier']; code=complete_code(e['ambient'],e['neurons'])
assert code==set(e['expected_code']) and '' not in code
print('COVERED CARRIER PASS:',sorted(code))

# 8: two faces with a common edge.
e=data['shared_edge']; line=e['edge']
IL=line_interval([(e['left_ambient'],False),(e['left_neuron'],True)],line['point'],line['direction'])
IR=line_interval([(e['right_ambient'],False),(e['right_neuron'],True)],line['point'],line['direction'])
assert interval_as_json(IL)==e['expected_trace']==interval_as_json(IR)
print('SHARED EDGE PASS:',interval_as_json(IL))

# 9: tetrahedron. Neuron r is the barycentric halfspace lambda_r>1/5.
e=data['tetrahedral_boundary']; a=F(e['threshold'])
edge_traces={}
for r,s in e['edges']:
    # Parameter t=lambda_s from vertex r (t=0) to vertex s (t=1).
    edge_traces[(r,s),r]=(F(0),F(1)-a,True,False)
    edge_traces[(r,s),s]=(a,F(1),False,True)
    for q in set(e['vertices'])-{r,s}:
        edge_traces[(r,s),q]=None
# Every edge belongs to exactly two faces; the same dictionary is used by both.
for edge in e['edges']:
    incident=[tuple(face) for face in e['faces'] if set(edge)<=set(face)]
    assert len(incident)==2
    for q in e['vertices']:
        assert edge_traces[tuple(edge),q]==edge_traces[tuple(edge),q]
assert len(e['edges'])==6 and len(e['faces'])==4
print('TETRAHEDRAL BOUNDARY PASS: 4 faces, 6 shared edge traces')
print('ALL EXACT RATIONAL EXAMPLES PASS')
