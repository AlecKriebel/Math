#!/usr/bin/env python3
"""Operative read-only finite algebra and document checks; not an infinite proof checker."""
import hashlib,itertools,json,os,subprocess,sys
from pathlib import Path
INPUT_PINS = {'accepted/AUDIT_STATUS.json': {'bytes': 896, 'sha256': '9aea4be1283325a52e1a36bd697ef38f1d78d7c59603a22d9a353b3ed8df8efc'}, 'accepted/CHECK_RESULTS.json': {'bytes': 2947, 'sha256': '688e25aa00dc5429be4222c143e873df308ebdfeca1c2c1f4c11e25d993ef1c2'}, 'accepted/MANIFEST.json': {'bytes': 1024, 'sha256': '81c70019d4d9cc6de42ede026009ea899e56199e93b23aeed50f1c587fa9f2fc'}, 'accepted/SOURCE_METADATA.json': {'bytes': 3211, 'sha256': 'cd98e52d1b28ee929ef5e39a8d24a83da4f3800dc592a4799cfbc91ad02534c0'}, 'accepted/SOURCE_SCOPE_AND_PRIOR_PROOF_AUDIT.md': {'bytes': 17715, 'sha256': '3fed365528ba84b4edd9f8f146190917e18a4084d3215ded51fe82ad9dbbe27f'}, 'accepted/SOURCE_SCOPE_REPAIR.md': {'bytes': 2656, 'sha256': '984e49199391e3d26e68c32a67909c849a7bf91005e0a211580405d09cd94a3c'}, 'accepted/verify_known_chain.py': {'bytes': 3890, 'sha256': 'd36b57e55b0f92aa163f35697e1cfb5fcbd82b0780b931d1a57cdf9e64cd9105'}}
ACCEPTANCE = {'accepted_input_bytes_preserved': True, 'credit': ['Mikolaj Bojanczyk', 'Joanna Fijalkow', 'Bartek Klin', 'Joshua Moerman'], 'decision': 'ACCEPT_CREDITED_LITERAL_COUNTEREXAMPLE_AND_SOURCE_SCOPE_REPAIR', 'excluded_stages': {'dataset_replay': 'NOT_RUN', 'earlier_historical_counterexample_proof_replay': 'NOT_RUN', 'excluded_material_replay': 'NOT_RUN', 'formal_proof_assistant_verification': 'NOT_RUN', 'full_positive_theorem_proof_replay': 'NOT_RUN', 'historical_checker_execution': 'NOT_RUN', 'historical_inspection_replay': 'NOT_RUN', 'historical_result_replay': 'NOT_RUN', 'historical_retrieval_replay': 'NOT_RUN', 'infinite_theorem_computational_certification': 'NOT_RUN', 'new_source_search': 'NOT_RUN', 'source_body_replay': 'NOT_RUN'}, 'historical_checker_limit': 'Preserved with assert statements and adjacent output write; execution NOT_RUN. Only current_checks.py is replayed, with operative explicit guards and no output writes.', 'literal_catalogue_disposition': 'FALSE_BY_VERIFIED_PUBLISHED_COUNTEREXAMPLE', 'mathematical_proof_computationally_certified': False, 'mathematical_scope': {'chain': 'V=direct_sum_N F_2, G=GL(V), coefficient F_2; C_n spanned by n-space incidence sums, minimum nonzero support 2^n; strict infinite descent.', 'excluded_negative': 'No all-characteristics negative claim, odd-characteristic counterexample, all-finite-base-fields extrapolation, or refutation of separate ACC question.', 'extension': 'Every characteristic-2 coefficient field by exact faithful scalar extension.', 'historical': 'Earlier Evans-Gray and Ahlbrandt-Ziegler proof bodies not retrieved; no first-priority certification; direct complete counterexample proof checked in TheoretiCS 2024 Theorem 4.16 and Appendix B.', 'literal_catalogue': 'Arbitrary omega-categorical M and oligomorphic W: false by the published binary counterexample.', 'nonhomogeneity': 'Finite ternary presentation is not finite relational homogeneity; bounded-arity circuit argument rules out homogeneous finite relational presentation with same GL(V).', 'original_owr': 'OWR-14299587-002: M homogeneous in a finite relational language, W=M^k, k positive; NOT resolved.', 'positive_audit': 'Positive theorem statements and organization inspected; not every proof certified; final conference paper defers some second-method technical details.', 'positive_scope': 'LICS 2026 Theorem 5.4 under Definition 5.1 in characteristic zero, including vector atoms by Corollary 5.5. Theorem 7.3 and Corollary 7.5 retain unary/binary free-amalgamation hypotheses; stated Corollary 7.8 consequences only.', 'projective': 'Delete zero coordinate on augmentation C_1 to obtain Q=D_1>D_2>...; exact minimum support 2^n-1.', 'versions': 'Evans latest v2 dated 9 September 2026 distinguished from v1; LICS final Article 82 distinguished from provisional author Article 6.'}, 'new_proof_search_turns': 0, 'novelty_claimed': False, 'original_owr_target_resolved': False, 'problem_id': 30006513, 'proof_availability_hold': 'RELEASED_FOR_BINARY_COUNTEREXAMPLE', 'schema': 1, 'source_formulation_repair': 'REQUIRED', 'source_problem': 'OWR-14299587-002'}
STATUS = {'all_characteristics_negative_claimed': False, 'literal_catalogue_false': True, 'manuscript_status': 'Authored audit and proposed source repair of prior published mathematics; not a new solution to the restricted OWR question or an author/publisher-issued erratum.', 'new_proof_search_turns': 0, 'novelty_claimed': False, 'original_owr_target_resolved': False, 'positive_theorem_full_proofs_certified': False, 'problem_id': 30006513, 'schema': 1, 'source_scope_repair_required': True, 'status': 'credited_literal_counterexample_SOURCE_SCOPE_REPAIR'}
EXPECTED_FINITE = [{'affine_minimum_weight': 2, 'affine_rank': 1, 'ambient_dimension': 1, 'generators': 1, 'minimum_weight': 2, 'projective_minimum_weight': 1, 'projective_rank': 1, 'rank': 1, 'subspace_dimension': 1}, {'affine_minimum_weight': 2, 'affine_rank': 3, 'ambient_dimension': 2, 'generators': 3, 'minimum_weight': 2, 'projective_minimum_weight': 1, 'projective_rank': 3, 'rank': 3, 'subspace_dimension': 1}, {'affine_minimum_weight': 4, 'affine_rank': 1, 'ambient_dimension': 2, 'generators': 1, 'minimum_weight': 4, 'projective_minimum_weight': 3, 'projective_rank': 1, 'rank': 1, 'subspace_dimension': 2}, {'affine_minimum_weight': 2, 'affine_rank': 7, 'ambient_dimension': 3, 'generators': 7, 'minimum_weight': 2, 'projective_minimum_weight': 1, 'projective_rank': 7, 'rank': 7, 'subspace_dimension': 1}, {'affine_minimum_weight': 4, 'affine_rank': 4, 'ambient_dimension': 3, 'generators': 7, 'minimum_weight': 4, 'projective_minimum_weight': 3, 'projective_rank': 4, 'rank': 4, 'subspace_dimension': 2}, {'affine_minimum_weight': 8, 'affine_rank': 1, 'ambient_dimension': 3, 'generators': 1, 'minimum_weight': 8, 'projective_minimum_weight': 7, 'projective_rank': 1, 'rank': 1, 'subspace_dimension': 3}, {'affine_minimum_weight': 2, 'affine_rank': 15, 'ambient_dimension': 4, 'generators': 15, 'minimum_weight': 2, 'projective_minimum_weight': 1, 'projective_rank': 15, 'rank': 15, 'subspace_dimension': 1}, {'affine_minimum_weight': 4, 'affine_rank': 11, 'ambient_dimension': 4, 'generators': 35, 'minimum_weight': 4, 'projective_minimum_weight': 3, 'projective_rank': 11, 'rank': 11, 'subspace_dimension': 2}, {'affine_minimum_weight': 8, 'affine_rank': 5, 'ambient_dimension': 4, 'generators': 15, 'minimum_weight': 8, 'projective_minimum_weight': 7, 'projective_rank': 5, 'rank': 5, 'subspace_dimension': 3}, {'affine_minimum_weight': 16, 'affine_rank': 1, 'ambient_dimension': 4, 'generators': 1, 'minimum_weight': 16, 'projective_minimum_weight': 15, 'projective_rank': 1, 'rank': 1, 'subspace_dimension': 4}]
RUN_MUTATIONS = True

def need(ok,reason):
 if not ok:raise ValueError(reason)
def exact(a,b):
 if type(a) is not type(b):return False
 if type(b) is dict:return set(a)==set(b) and all(exact(a[k],v) for k,v in b.items())
 if type(b) is list:return len(a)==len(b) and all(exact(x,y) for x,y in zip(a,b))
 return a==b
def subspaces(d):
 levels=[{frozenset([0])}]
 for n in range(d):
  nxt=set()
  for u in levels[-1]:
   for v in range(1<<d):
    if v not in u:nxt.add(u|frozenset(x^v for x in u))
  levels.append(nxt)
 return [sorted(level,key=lambda u:tuple(sorted(u))) for level in levels]
def bits(points):return sum(1<<x for x in points)
def basis(rows):
 pivots={}
 for row in rows:
  while row:
   pivot=row.bit_length()-1
   if pivot in pivots:row^=pivots[pivot]
   else:pivots[pivot]=row;break
 return pivots
def contains(pivots,row):
 while row:
  pivot=row.bit_length()-1
  if pivot not in pivots:return False
  row^=pivots[pivot]
 return True
def min_weight(pivots):
 words=[0]
 for row in pivots.values():words += [x^row for x in words]
 weights=[word.bit_count() for word in words if word]
 need(bool(weights),'nonempty linear code')
 return min(weights)
def generators(d):
 gs=[]
 for i in range(d-1):
  def swap(x,i=i):return x^((1<<i)|(1<<(i+1))) if ((x>>i)^(x>>(i+1)))&1 else x
  gs.append(swap)
 if d>=2:gs.append(lambda x:x^(((x>>1)&1)<<0))
 return gs

def finite_checks():
 rows=[];invariance=descent=hyperplanes=0
 for d in range(1,5):
  levels=subspaces(d);previous=None
  for n in range(1,d+1):
   incidence=[bits(u) for u in levels[n]];b=basis(incidence)
   affine=sorted({bits({x^v for x in u}) for u in levels[n] for v in range(1<<d)})
   ab=basis(affine);pb=basis(row>>1 for row in incidence)
   linear_weight=min_weight(b);affine_weight=min_weight(ab);projective_weight=min_weight(pb)
   need(linear_weight==1<<n,'linear minimum support')
   need(affine_weight==1<<n,'affine minimum support')
   need(len(pb)==len(b),'projective rank preservation')
   need(projective_weight==(1<<n)-1,'projective minimum support')
   need(all(row.bit_count()%2==0 for row in b.values()),'even augmentation')
   for g in generators(d):
    for u in levels[n]:
     need(contains(b,bits(g(x) for x in u)),'GL generator invariance');invariance+=1
   if previous is not None:
    for row in incidence:need(contains(previous,row),'chain containment');descent+=1
    need(len(b)<len(previous),'strict rank drop')
   if n>=2:
    for u in levels[n]:
     total=0
     for h in levels[n-1]:
      if h<=u:total ^= bits(h)
     need(total==bits(u),'hyperplane identity');hyperplanes+=1
   rows.append(dict(ambient_dimension=d,subspace_dimension=n,generators=len(incidence),rank=len(b),minimum_weight=linear_weight,affine_rank=len(ab),affine_minimum_weight=affine_weight,projective_rank=len(pb),projective_minimum_weight=projective_weight));previous=b
 domain=[0,1,2,4,7];image=[0,1,2,4,8];mapping=dict(zip(domain,image))
 triples=list(itertools.product(domain,repeat=3))
 need(all((x^y==z)==(mapping[x]^mapping[y]==mapping[z]) for x,y,z in triples),'ternary partial isomorphism')
 need((1^2^4^7)==0 and (1^2^4^8)!=0,'dependency obstruction')
 need(exact(rows,EXPECTED_FINITE),'exact finite identities and values')
 need(len(rows)==10 and len(triples)==125,'exact finite case counts')
 return dict(finite_tests=rows,finite_case_count=len(rows),GL_generator_incidence_checks=invariance,containment_incidence_checks=descent,hyperplane_identities=hyperplanes,ternary_relation_triples=len(triples),dependency_obstruction=True)

MUTATIONS = [
 ('minimum replaced by maximum','return min(weights)','return max(weights)','linear minimum support'),
 ('retain zero projective coordinate','pb=basis(row>>1 for row in incidence)','pb=basis(row for row in incidence)','projective minimum support'),
 ('drop zero from hyperplane sum','total ^= bits(h)','total ^= bits(h-{0})','hyperplane identity'),
 ('invert containment requirement','need(contains(previous,row),','need(not contains(previous,row),','chain containment'),
 ('invert strict rank drop','need(len(b)<len(previous),','need(len(b)>=len(previous),','strict rank drop'),
 ('replace linear generator by constant zero','gs.append(swap)','gs.append(lambda x:0)','GL generator invariance'),
 ('destroy ternary partial isomorphism','image=[0,1,2,4,8]','image=[0,1,2,4,3]','ternary partial isomorphism'),
 ('erase dependency obstruction','(1^2^4^8)!=0','(1^2^4^8)==0','dependency obstruction'),
]

def algebra_mutations(root):
 source=(root/'current_checks.py').read_text();before,after=source.split('\nMUTATIONS = ',1);results=[]
 flags=['-I','-S','-B']+([] if sys.flags.optimize==0 else ['-'+'O'*sys.flags.optimize])
 for label,old,new,reason in MUTATIONS:
  need(before.count(old)==1,'unique mutation anchor: '+label)
  variant=before.replace(old,new).replace('RUN_MUTATIONS = True','RUN_MUTATIONS = False')+'\nMUTATIONS = '+after
  launcher='exec(compile('+repr(variant)+',"<finite-algebra-mutant>","exec"),{"__name__":"__main__","__file__":'+repr(str(root/'current_checks.py'))+'})'
  r=subprocess.run([sys.executable,*flags,'-c',launcher],cwd=root,env=dict(PATH=os.defpath,HOME='/tmp',TMPDIR='/tmp',LC_ALL='C'),capture_output=True,timeout=60)
  expected=('REJECT: current check: '+reason+'\n').encode()
  need(type(r.returncode) is int and r.returncode==1 and r.stdout==b'' and r.stderr==expected,'intended algebra rejection: '+label)
  results.append(dict(identity=label,exit_code=r.returncode,stdout=r.stdout.decode(),stderr=r.stderr.decode(),intended_rejection_reason=reason,intended_rejection_reason_matched=True,rejected=True))
 need([r['identity'] for r in results]==[m[0] for m in MUTATIONS] and len(results)==8,'exact algebra mutation identities/count')
 return results

def main():
 need(os.getuid()==os.geteuid()==1000,'UID/EUID1000')
 need(sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode,'require -I -S -B')
 root=Path(__file__).resolve().parent;documents=[]
 for name,pin in INPUT_PINS.items():
  raw=(root/name).read_bytes();actual=dict(bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest())
  need(exact(actual,pin),'accepted document bytes: '+name)
  documents.append(dict(document=name,bytes=len(raw),sha256=actual['sha256'],preserved=True))
 need(exact(json.loads((root/'ACCEPTANCE.json').read_bytes()),ACCEPTANCE),'exact acceptance scope')
 need(exact(json.loads((root/'STATUS.json').read_bytes()),STATUS),'exact status scope')
 finite=finite_checks();mutations=algebra_mutations(root) if RUN_MUTATIONS else []
 result=dict(schema=1,problem_id=30006513,status='passed',uid=os.getuid(),euid=os.geteuid(),python_optimize=sys.flags.optimize,document_byte_checks=documents,document_byte_check_count=7,scope_declaration_controls=[dict(identity='exact acceptance declaration',passed=True),dict(identity='exact status declaration',passed=True)],scope_declaration_control_count=2,algebra_mutation_controls=mutations,algebra_mutation_control_count=len(mutations),source_theorem_computationally_certified=False,infinite_proof_basis='Written induction and mathematical arguments in accepted audit; finite computation corroborates small cases only.',historical_checker_execution='NOT_RUN',historical_result_replay='NOT_RUN',**finite)
 print(json.dumps(result,indent=2,sort_keys=True))
if __name__=='__main__':
 try:main()
 except (ValueError,OSError,TypeError,KeyError,subprocess.TimeoutExpired) as e:print('REJECT: current check: '+str(e),file=sys.stderr);sys.exit(1)
