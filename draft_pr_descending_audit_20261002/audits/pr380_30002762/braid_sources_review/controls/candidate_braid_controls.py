"""Postseal exact controls of the actual frozen two-generator presentation.
Uses only our independently authored faithful Artin-action engine; no candidate imports.
"""
import contextlib,io,json,runpy
from pathlib import Path
with contextlib.redirect_stdout(io.StringIO()):
 ns=runpy.run_path(str(Path(__file__).with_name('exact_braid_controls.py')))
action=ns['action'];inverse_word=ns['inverse_word'];generator=ns['generator'];compose=ns['compose'];power=ns['power'];conjugate=ns['conjugate'];commute=ns['commute'];identity=ns['identity']
rows=[]
for K in range(2,27):
 n=K+2;delta=tuple(range(1,n));t=action(n,delta);ti=action(n,inverse_word(delta));a=generator(n,1);a1=conjugate(t,a,ti)
 assert a1==generator(n,2)
 assert compose(compose(a,a1),a)==compose(compose(a1,a),a1)
 for j in range(2,K+1):
  aj=conjugate(power(t,j),a,power(ti,j));assert aj==generator(n,j+1)
  assert commute(a,aj)
 assert not commute(a,a1) # Mutating the lower index2to1 invalidates the quotient.
 # At the first omitted shift, the transported edge returns across the cycle boundary.
 missing=conjugate(power(t,K+1),a,power(ti,K+1))
 assert not commute(a,missing)
 # A wraparound assertion transporting sigma_(n-1)to sigma1 is false.
 wrap=conjugate(t,generator(n,n-1),ti)
 assert wrap!=a
 # Opposite-sign shift fails the specific nonwrapping-index equality.
 assert conjugate(ti,a,t)!=generator(n,2)
 g=compose(compose(power(generator(n,-1),4),a1),compose(power(a,2),a1))
 assert g==action(n,(-1,)*4+(2,1,1,2))
 rows.append({'K':K,'N':n,'commuting_relators':K-1,'maximal_j':K,'boundary_generator_index':K+1,'all_relators_pass':True,'distance1_mutation_fails':True,'first_omitted_distance_fails':True,'wraparound_mutation_fails':True,'reverse_shift_mutation_fails':True,'detector_exact':True})
# Actual infinite-model support argument, also tests why distance1 must be excluded.
checks=[]
for m in [1,2,3,7,31,100,257]:
 supports=[{3*i,3*i+1} for i in range(m+1)]
 gap=min(abs(x-y) for i in range(m+1) for j in range(i+1,m+1) for x in supports[i] for y in supports[j])
 assert gap==2
 badgap=min(abs(x-y) for x in {0,1} for y in {2,3});assert badgap==1
 checks.append({'m':m,'fixed_t3_minimum_index_gap':gap,'stride2_invalid_index_gap':badgap})
print(json.dumps({'actual_frozen_finite_model':rows,'actual_fixed_displacer_controls':checks,'infinite_uniform_norm_bound':'14 * norm(t^3) <= 42','signature_nonzero_argument':'Exact GG primary formula plus commuting central decomposition: |sigma_hom(alpha)|=2, not sampled-signature detection','scope':'K=2..26 exact finite actions; m in 1,2,3,7,31,100,257; universal written proofs remain necessary'},indent=2))
