"""Compare historical public inert monomial data, without running author code."""
import ast, json, re
from pathlib import Path

P = Path(__file__).parent
word = (1,2,3,2,4,2,1,2,3,2,4,2)
N = len(word)
source = (P/'sources/crystal_crystal_D_4.out').read_text()
blocks = re.split(r'==== Case\s+(\d+)\s+====', source)
case = None
for k in range(1,len(blocks),2):
    match = re.search(r'Long element decomposition:\s*(.+)', blocks[k+1])
    if match and tuple(ast.literal_eval(match[1])) == word:
        case = blocks[k], blocks[k+1]
if case is None:
    raise RuntimeError('Exact word not found')

def exponent(node):
    if isinstance(node, ast.Name) and re.fullmatch(r't([1-9]|1[0-2])',node.id):
        v=[0]*N; v[int(node.id[1:])-1]=1; return v
    if isinstance(node, ast.Constant) and node.value == 1:
        return [0]*N
    if isinstance(node, ast.BinOp) and isinstance(node.op,(ast.Mult,ast.Div)):
        a,b=exponent(node.left),exponent(node.right)
        sign=1 if isinstance(node.op,ast.Mult) else -1
        return [x+sign*y for x,y in zip(a,b)]
    if isinstance(node, ast.BinOp) and isinstance(node.op,ast.Pow) and isinstance(node.right,ast.Constant) and isinstance(node.right.value,int):
        return [x*node.right.value for x in exponent(node.left)]
    raise RuntimeError(f'Unexpected monomial syntax: {ast.dump(node)}')

prior=[]; groups=[]
for root,b in re.findall(r'Simple root:\s+(\d+)\n(.*?)==== End ====',case[1],re.S):
    lines=b.splitlines()
    idx=next(k for k,l in enumerate(lines) if l.startswith('Number of monomials:'))
    final=ast.parse(lines[idx-1], mode='eval').body
    rows=[exponent(m) for layer in final.elts for m in layer.elts]
    count=int(lines[idx].split(':')[1])
    if len(rows)!=count or len({tuple(r) for r in rows})!=count:
        raise RuntimeError('Count or uniqueness mismatch')
    prior.extend(rows);groups.append({'root':int(root),'count':count,'pullback_exponents':rows})

# Standard reciprocal chamber map y_j = product x_s^K[j,s], from word.
K=[[0]*N for _ in range(N)]
for j in range(N):
    jp=next((k for k in range(j+1,N) if word[k]==word[j]),N)
    K[j][j]=1
    if jp<N:K[j][jp]=1
    for s in range(j+1,jp):
        if (word[j]==2)!=(word[s]==2):K[j][s]=-1

canonical=[]
for b in prior:
    a=[]
    for j in range(N):a.append(b[j]-sum(a[i]*K[i][j] for i in range(j)))
    if [sum(a[i]*K[i][j] for i in range(N)) for j in range(N)] != b:
        raise RuntimeError('Triangular inverse failed')
    canonical.append(a)

root_output=json.loads((P.parent.parent/'ROOT_EXACT_VERIFICATION.json').read_text())
if {tuple(b) for b in prior}!={tuple(b) for b in root_output['transformed_rows']}:
    raise RuntimeError('Historical and current transformed support differ')

result={
 'prior_case':int(case[0]),'word':word,'prior_data_semantics':'Monomial support, not an assertion about coefficient multiplicities or facets.',
 'prior_groups':groups,'total_support':len(prior),'current_pullback_support_exactly_matches':True,
 'chamber_K':K,'canonical_reciprocal_y_exponents':canonical,
 'canonical_max_exponent':max(abs(v) for a in canonical for v in a),
 'canonical_squared_rows':[a for a in canonical if max(a)>1],
 'author_code_executed':False,
 'conclusion':'The exact reduced word and full string-coordinate support were public in earlier author data. Canonical support and exponent2 can be reconstructed from that support and the established chamber map. The prior data do not explicitly state the OWR2021 canonical-W converse is false or supply essential-inequality certificates.',
}
(P/'PRIOR_DATA_COMPARISON.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k not in ['prior_groups','chamber_K','canonical_reciprocal_y_exponents']},indent=2))
