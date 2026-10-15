"""Authenticated primary literals, original results, and independent reconstruction."""
from pathlib import Path
from fractions import Fraction as F
from hashlib import sha256
import json,re,sys
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
from independent_exact import FACES,WORD,EDGES,C,SQRT5,PHI,require
pinned=(HERE/'private/PINNED_PROBLEM_AND_PROOF.md').read_text()
face_matches=re.findall(r'^F(\d+)\s*=\s*\[([^\]]+)\]',pinned,re.M)
faces={int(i):list(map(int,re.findall(r'\d+',s))) for i,s in face_matches}
require([faces[i] for i in range(12)]==FACES,'authenticated primary faces')
word_block=pinned.split('develop the face occurrences')[1].split('```text')[1].split('```')[0]
word=list(map(int,re.findall(r'\d+',word_block)))
require(word==WORD,'authenticated primary word')
edge_block=pinned.split('fifteen crossed edges')[1].split('```text')[1].split('```')[0]
edges=[tuple(map(int,x)) for x in re.findall(r'(\d+)-(\d+)',edge_block)]
require(edges==EDGES,'authenticated primary edges')
ind=json.loads((HERE/'private/runs/independent_exact_normal.stdout').read_text())
orig=json.loads((HERE/'private/runs/original_certificate_normal.stdout').read_text())
turn=json.loads((HERE/'private/runs/original_half_turn_normal.stdout').read_text())
def parse_pair(s):
    m=re.fullmatch(r'\(([^)]+)\)\+\(([^)]+)\)\*sqrt\(5\)',s)
    require(m is not None,'pair parse')
    return [str(F(m[1])),str(F(m[2]))]
require(all(parse_pair(a['t'])==b['t'] and parse_pair(a['s'])==b['s'] for a,b in zip(orig['crossings'],ind['witness']['crossings'])) and len(orig['crossings'])==15,'all crossing pairs agree')
require(all(a['edge']==b['edge'] and a['permutation']==b['permutation'] and a['vertex_distance_histogram']==b['histogram'] for a,b in zip(turn['all_30_half_turns'],ind['half_turns'])),'all half-turns agree')
physical={i:set() for i in range(20)}
for face in FACES:
    for a,b in zip(face,face[1:]+face[:1]):physical[a].add(b);physical[b].add(a)
require(2 not in physical[0] and 16 in physical[0]&physical[2],'independent graph distance 2')
# eta=e^(i*pi/5) has eta+conj(eta)=phi, so norm(A+B eta)=A²+phi AB+B².
require('eta = exp(i*pi/5)' in pinned and 'A = 31/2 + (13/2)*sqrt(5)' in pinned and 'B = -17 - 8*sqrt(5)' in pinned,'actual pinned coordinate formula')
A=(31+13*SQRT5)/2;B=-17-8*SQRT5
computed=A*A+PHI*A*B+B*B;claimed=(307+137*SQRT5)/2
require(computed==(425+189*SQRT5)/2 and computed!=claimed,'pinned endpoint coordinate defect')
record={'primary_body_sha256':sha256(pinned.encode()).hexdigest(),'primary_faces_word_and_crossed_edges_match':True,'independent_crossing_pairs_matching_original':15,'independent_half_turn_permutations_matching_original':30,'independent_graph_distance':2,'pinned_endpoint_coordinate_formula':{'eta':'exp(i*pi/5)','A_pair':['31/2','13/2'],'B_pair':['-17','-8'],'computed_norm_pair':computed.pairdata(),'claimed_norm_pair':claimed.pairdata(),'difference_pair':(computed-claimed).pairdata(),'identity_used':'norm(A+B eta)=A^2+phi*A*B+B^2','is_internally_consistent':False},'independent_geometry':ind}
(HERE/'INDEPENDENT_RESULTS.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps({k:v for k,v in record.items() if k!='independent_geometry'},indent=2))
