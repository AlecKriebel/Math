"""Proposed source-bound diagnostic, not an independent proof.
Loads the actual supplied checker only to test its endpoint generator against
literal nonempty left exchanges transcribed from Kamada pp.6–7 / KL p.30.
The separate independent_controls.py never loads the author checker.
"""
import hashlib, json, pathlib, runpy, sys
from independent_controls import diagram, canonical

path=pathlib.Path(sys.argv[1]).resolve()
code=path.read_bytes()
ns=runpy.run_path(str(path))
State=ns['State']; even_scheme=ns['even_scheme']
a=b=(("s",1,1),)
literal_L=(State(4,(("s",2,1),("s",1,-1),("s",2,1),("s",1,1))),
           State(4,(("s",2,1),("v",1,1),("s",2,1),("v",1,1))))
literal_BL=(State(4,literal_L[0].word+(("s",3,1),)),
            State(4,literal_L[1].word+(("s",3,1),)))
def matrix(state):
    letters=tuple(100+i if t=='v' else i*sign for t,i,sign in state.word)
    return diagram(state.strands,letters)
cases=[]
for name,literal in [('L',literal_L),('BL',literal_BL)]:
    actual=even_scheme(name,4,a,b)
    mats=list(map(matrix,actual))
    expected_mats=list(map(matrix,literal))
    row={'scheme':name,'literal_endpoints':[[x.strands,x.word] for x in literal],
         'actual_endpoints':[[x.strands,x.word] for x in actual],
         'literal_matrices':expected_mats,'actual_matrices':mats,
         'matches_literal':actual==literal,
         'actual_invariant_equal_up_to_component_relabel':canonical(mats[0])==canonical(mats[1]),
         'literal_invariant_equal_up_to_component_relabel':canonical(expected_mats[0])==canonical(expected_mats[1])}
    assert row['literal_invariant_equal_up_to_component_relabel']
    cases.append(row)
passed=all(x['matches_literal'] and x['actual_invariant_equal_up_to_component_relabel'] for x in cases)
print(json.dumps({'status':'PASS_LITERAL_PRIMARY_LEFT_CONTROLS' if passed else 'FAIL_LITERAL_PRIMARY_LEFT_CONTROLS',
                  'checker_sha256':hashlib.sha256(code).hexdigest(),'checker_bytes':len(code),'cases':cases,
                  'scope':'Author code is loaded solely for a proposed diagnostic; independent proof/falsification checker is separate'},indent=2))
raise SystemExit(0 if passed else 1)
