"""Inert AST parse of primary cached data; byte/provenance checks only."""
import ast, hashlib, json, lzma, pathlib, re
HERE=pathlib.Path(__file__).resolve().parent
B=HERE.parent.parent;P=B/'publication';V=P/'verification'

def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
source=B/'priority/independent/sources/crystal_data2020.xz'
text=lzma.decompress(source.read_bytes()).decode()
case=re.search(r'==== Case\s+267\s+====(.*?)==== Case\s+268\s+====',text,re.S).group(1)
word=tuple(ast.literal_eval(re.search(r'Long element decomposition:\s*(\([^\n]+\))',case).group(1)))
assert word==(1,2,3,2,4,2,1,2,3,2,4,2)

def monomial(node):
    if isinstance(node,ast.Name) and re.fullmatch(r't(?:[1-9]|1[0-2])',node.id):
        out=[0]*12;out[int(node.id[1:])-1]=1;return out
    if isinstance(node,ast.Constant) and node.value==1:return [0]*12
    if isinstance(node,ast.BinOp) and isinstance(node.op,(ast.Mult,ast.Div)):
        a=monomial(node.left);b=monomial(node.right);sign=1 if isinstance(node.op,ast.Mult) else -1
        return [u+sign*v for u,v in zip(a,b)]
    if isinstance(node,ast.BinOp) and isinstance(node.op,ast.Pow) and isinstance(node.right,ast.Constant) and isinstance(node.right.value,int):
        return [u*node.right.value for u in monomial(node.left)]
    raise ValueError('Unexpected source AST '+ast.dump(node))

old={}
for a,body in re.findall(r'Simple root:\s*(\d+)\s*(.*?)(?===== End ====)',case,re.S):
    nested=re.findall(r'^\[\[.*$',body,re.M)[-1]
    tree=ast.parse(nested,mode='eval').body
    assert isinstance(tree,ast.List)
    rows=[]
    for step in tree.elts:
        assert isinstance(step,ast.List)
        rows.extend(tuple(monomial(m)) for m in step.elts)
    expected=int(re.search(r'Number of monomials:\s*(\d+)',body).group(1))
    assert len(rows)==len(set(rows))==expected
    old[int(a)]=rows

data=json.loads((V/'certificate.json').read_text())
rows=[tuple(v['a']) for v in data['certificate_rows']]
adj={frozenset(e) for e in ((1,2),(2,3),(2,4))}
H=[[2 if a==b else -1 if frozenset((a,b)) in adj else 0 for b in range(1,5)] for a in range(1,5)]
nxt=[next((j for j in range(i+1,12) if word[j]==word[i]),12) for i in range(12)]
K=[[int(j==i or j==nxt[i]) if not i<j<nxt[i] else H[word[i]-1][word[j]-1] for j in range(12)] for i in range(12)]
pulled=[tuple(sum(a[i]*K[i][j] for i in range(12)) for j in range(12)) for a in rows]
assert set(pulled)==set(r for rs in old.values() for r in rs)
markers={1:6,2:11,3:8,4:10}
for root,pos in markers.items():
    assert set(old[root])=={v for a,v in zip(rows,pulled) if a[pos]==1}

fresh=V/'blind_reconstruction';original=B/'reviews/blind_family'
immutable=[]
for name in ('INITIAL_RECEIPT.md','blind_frozen.json','blind_frozen.sha256','REPORT.md','supplement_exact.json','source_regression.json','verify_blind.py','verify_supplement.py','verify_source_regression.py'):
    assert (fresh/name).read_bytes()==(original/name).read_bytes(),name
    immutable.append({'file':name,'sha256':digest(fresh/name),'identical_to_original':True})
assert digest(fresh/'blind_frozen.json')=='7881d1d0ef80ff7ca036f16a06d2d7f23cb666bab223500226d6cded3f66a30d'
assert digest(fresh/'INITIAL_RECEIPT.md')=='af766d1da012b3358d7aedd1955cd27aaa61cba6f2ac60a52b0f837440de8553'
old_digest=digest(V/'independent_output.json')
assert old_digest=='fc5a5208035b011683168d1114af93c613de4f001e19ab49ce70a464e0b0d459'
assert old_digest!=digest(fresh/'blind_frozen.json')
out={'source_xz_sha256':digest(source),'case':267,'word':word,'summand_counts':{a:len(r) for a,r in old.items()},'all_22_chamber_rows_match':True,'matches_separately_by_simple_root':True,'old_support':old,'immutable_fresh_family_files':immutable,'old_family_output_sha256':old_digest,'chronology_limit':'Equality of original local and packaged receipts is directly checked; agent context/input boundaries and historical timestamp claims are internal records, not independently timestamped external facts.'}
(HERE/'prior_and_provenance.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'status':'PASS','counts':out['summand_counts'],'all22_match':True,'immutable_fresh_files':len(immutable),'receipt_sha256':digest(fresh/'INITIAL_RECEIPT.md')},indent=2))
