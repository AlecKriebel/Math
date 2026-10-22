"""Exact comparison of historical public data with the submitted candidate.
Uses ast parsing only for the source's Laurent monomials; never executes source code.
"""
from pathlib import Path
import ast, json, re, hashlib
root=Path(__file__).parent
text=(root/'sources'/'d4_data.txt').read_text()
word=[1,2,3,2,4,2,1,2,3,2,4,2]
blocks=re.split(r'==== Case\s+(\d+)\s+====',text)
case={int(blocks[k]):blocks[k+1] for k in range(1,len(blocks),2)}[267]
assert tuple(word)==ast.literal_eval(re.search(r'Long element decomposition:\s*(.*)',case).group(1))
N=12
zero=(0,)*N
def monomial(s):
 def walk(n):
  if isinstance(n,ast.Name):
   q=int(n.id[1:]); assert n.id=='t'+str(q) and 1<=q<=N
   return tuple(int(j==q-1) for j in range(N))
  if isinstance(n,ast.Constant) and n.value==1: return zero
  if isinstance(n,ast.BinOp) and isinstance(n.op,(ast.Mult,ast.Div)):
   a,b=walk(n.left),walk(n.right)
   sign=1 if isinstance(n.op,ast.Mult) else -1
   return tuple(x+sign*y for x,y in zip(a,b))
  if isinstance(n,ast.BinOp) and isinstance(n.op,ast.Pow):
   k=ast.literal_eval(n.right); assert isinstance(k,int)
   return tuple(k*x for x in walk(n.left))
  raise ValueError(ast.dump(n))
 return walk(ast.parse(s,mode='eval').body)
def layers(s):
 # Historical lines have a list of lists of symbolic Laurent monomials.
 tree=ast.parse(s,mode='eval').body
 assert isinstance(tree,ast.List)
 nodes=[x for layer in tree.elts for x in layer.elts]
 return [monomial(ast.unparse(node)) for node in nodes]
by_root={}
for part in case.split('==== Begin ====')[1:]:
 j=int(re.search(r'Simple root:\s*(\d+)',part).group(1))
 lines=[x for x in part.splitlines() if x.startswith('[[')]
 assert len(lines)>=1
 by_root[j]=layers(lines[-1])
 assert len(by_root[j])==int(re.search(r'Number of monomials:\s*(\d+)',part).group(1))
A=[[2 if i==j else (-1 if 2 in (i+1,j+1) else 0) for j in range(4)] for i in range(4)]
K=[[0]*N for _ in range(N)]
for k,ik in enumerate(word):
 kp=next((m for m in range(k+1,N) if word[m]==ik),N)
 K[k][k]=1
 for l in range(k+1,kp): K[k][l]=A[ik-1][word[l]-1]
 if kp<N: K[k][kp]=1
# For row b=aK, triangular backsolving recovers a without numerical inversion.
def recover(b):
 a=[]
 for j in range(N): a.append(b[j]-sum(a[k]*K[k][j] for k in range(j)))
 assert all(sum(a[k]*K[k][j] for k in range(N))==b[j] for j in range(N))
 return tuple(a)
canonical={j:[recover(b) for b in rows] for j,rows in by_root.items()}
all_t=[b for rows in by_root.values() for b in rows]
all_y=[a for rows in canonical.values() for a in rows]
proof=(root.parent.parent/'submitted'/'PROOF.md').read_text()
expected=[tuple(map(int,s)) for s in re.findall(r'\|\d+\|([012]{12})\|',proof)]
assert len(expected)==22
assert sorted(all_y)==sorted(expected)
assert len(set(all_y))==22
assert all(all(x>=0 for x in a) for a in all_y)
assert all(max(map(abs,b))<=1 for b in all_t)
# All old data rooted at minuscule 1/3/4; root2 monomial t12, which is immediate.
assert by_root[2]==[tuple(int(k==11) for k in range(N))]
# Canonical counterexamples are already recovered from prior rows t1 and t2*t4*t6/t7.
bad=[{'root':j,'string_row':b,'canonical_y_row':recover(b)} for j,rows in by_root.items() for b in rows if max(recover(b))>1]
assert len(bad)==2
result={
 'source_repository':'https://github.com/mironovd/crystal',
 'historical_source':'https://github.com/mironovd/crystal/blob/573b512df531ec2d349ed05b3aa9f385989e13dd/crystal.D4.out.xz',
 'current_path_source':'https://github.com/mironovd/crystal/blob/0d6e564cf5e69d79c1074d5d1e3e72ac700904d6/crystal_D_4.out.xz',
 'file_sha256':hashlib.sha256((root/'sources'/'d4_data.xz').read_bytes()).hexdigest(),
 'history_versions_byte_identical':all((root/'sources'/x).read_bytes()==(root/'sources'/'d4_data.xz').read_bytes() for x in ['d4_20200306.xz','d4_20220529.xz']),
 'case_number':267,'word':word,
 'prior_type':'BK/string Laurent monomial support, not a printed canonical W polynomial',
 'prior_root_counts':{j:len(rows) for j,rows in by_root.items()},
 'change_of_variables_K':K,
 'prior_string_rows_by_root':by_root,
 'canonical_y_rows_recovered_from_prior_data':canonical,
 'canonical_bad_exponent_rows':bad,
 'exact_same_canonical_support_as_submitted':sorted(all_y)==sorted(expected),
 'number_of_unique_rows':len(set(all_y)),
 'all_prior_string_absolute_exponents_at_most_one':True,
 'all_prior_canonical_coefficients_known_from_this_support_file':False,
 'coefficient_note':'The file enumerates support only; it is not a general coefficient certificate. Coefficients for minuscule roots 1,3,4 and trivial root2 are known from separate prior theory; candidate exact mutation proof independently gives coefficient1.',
 'facet_note':'OWR2021 p1125 minuscule bullet or KS2022 Theorem6 gives nonredundancy for roots1,3,4; root2 is the lone final-position term. KS2022 Proposition3/Lemma4 prevents cross-root redundancy, and Proposition5 transports cones. KS2022 Theorem2 can also be applied directly to all22 squarefree string rows. This is an application of published results, not evidence that anyone explicitly published the canonical-W counterexample conclusion.',
 'reader_executed_source_author_software':False,
}
(root/'PRIOR_DATA_COMPARISON.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:result[k] for k in ['history_versions_byte_identical','prior_root_counts','canonical_bad_exponent_rows','exact_same_canonical_support_as_submitted','number_of_unique_rows','all_prior_string_absolute_exponents_at_most_one']},indent=2))
