"""Read-only alignment of manuscript and already acquired finite primary data."""
from pathlib import Path
import json
import re

O = Path(__file__).resolve().parent
S = O.parent.parent/'sources/published-source/container-001/tree'
tex = (S/'manuscript/main.tex').read_text()
data = json.loads((O/'native/certificate.json').read_text())
rows = re.findall(r'\\texttt\{([012]{12})\} & \$\(([^)]+)\)\$',tex)
assert len(rows) == 22
for (a,z),entry in zip(rows,data['certificate_rows']):
    assert list(map(int,a)) == entry['a']
    assert list(map(int,z.split(','))) == entry['z']
text = (O/'primary/MIRONOV.decoded.txt').read_text()
case = text.split('==== Case  267  ====\n',1)[1].split('==== Case  268  ====',1)[0]
assert '(1, 2, 3, 2, 4, 2, 1, 2, 3, 2, 4, 2)' in case
groups = re.findall(r'^(\[\[.*\]\])\nNumber of monomials: +(\d+)',case,re.M)
assert [int(n) for _,n in groups] == [14,1,5,2]
support = set()
for value,count in groups:
    terms = value.replace('[','').replace(']','').replace(' ','').split(',')
    terms = [v for v in terms if v]
    assert len(terms) == int(count)
    for term in terms:
        assert term.count('/') <= 1
        pieces = term.replace('(','').replace(')','').split('/')
        vector = [0]*12
        for side,piece in enumerate(pieces):
            for variable in piece.split('*'):
                assert re.fullmatch(r't(?:[1-9]|1[0-2])',variable)
                vector[int(variable[1:])-1] += 1 if side == 0 else -1
        support.add(tuple(vector))
results = json.loads((O/'native/results.json').read_text())
assert support == set(map(tuple,results['transformed_support'])) and len(support) == 22
print(json.dumps({'status':'PASS','manuscript_certificate_rows_exact':22,'primary_case':267,'source_word_exact':True,'source_summand_counts':[14,1,5,2],'whole_transformed_support_equals_actual_primary_case':True,'native_reruns':0,'writes':0},indent=2))
