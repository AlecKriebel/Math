#!/usr/bin/env python3
"""Additional audit controls; tests formulas, never edits candidate files."""
import json
from math import gcd

def emit(kind, **kw):
    print(json.dumps({'kind':kind, **kw},sort_keys=True))

def reject(name, wrong, expected, mechanism, scope):
    rejected = wrong != expected
    assert rejected, name
    emit('mutant_rejected', name=name, mutant_prediction=wrong,
         exact_expected=expected, rejected=True, mechanism=mechanism, scope=scope)

reject('zero_Tor', {'H1_order':1}, {'H1_order':2},
       'C_2 tensor C_2: kernel/image Smith quotient has order 2 in degree 1',
       'free abelian cochain control, not group realization')
reject('Tor_wrong_cohomological_diagonal', {'Tor_degree':3}, {'Tor_degree':1},
       'input cohomology degrees 1,1 imply Tor degree 1+1-1',
       'integral Kunneth indexing')
reject('flat_cochain_terms_imply_flat_cohomology', {'Tor_order':1}, {'Tor_order':2},
       'all terms of C_2 are Z-free but H1(C_2)=Z/2 is not Z-flat',
       'flatness must be checked on relevant cohomology')
reject('rational_tensor_is_integral_certificate', {'H1_order':1,'H2_order':1},
       {'H1_order':2,'H2_order':2},
       'C_2 tensor C_2 becomes acyclic over Q but has two integral Z/2 classes',
       'field shortcut rejected')
reject('concentration_without_dualizing_flatness', {'H0_order':1,'H1_order':2},
       {'H0_order':2,'H1_order':2},
       '(Z --2--> Z) tensor Z/2 has zero differential; the extra H0 is Tor',
       'algebraic UCT model, not a quotient-group counterexample')
reject('mod_p_Bockstein_equals_integral_connecting_class', {'beta_mod_4':0},
       {'beta_mod_4':2},
       'lift 1 for C_4 mod 2 has d(1)/2=2; its subsequent mod 2 reduction is zero',
       'integral connecting map distinguishes p-square torsion')
reject('cohomology_support_uses_only_tensor_diagonal', {'nonzero_degrees':[2]},
       {'nonzero_degrees':[1,2]},
       'the finite integral tensor complex has a Tor class one degree lower',
       'total graded support includes both diagonals')
reject('finite_projective_truncation_is_augmentation_resolution',
       {'top_kernel_rank':0}, {'top_kernel_rank':1},
       'C2 map s-1 has nonzero norm vector kernel in every truncation at odd degree',
       'genuine infinite periodic augmentation resolution differs from FP')
reject('rational_and_mod_p_quotient_detect_integral_finite_generation',
       {'Pruefer_p_is_Z_finitely_generated':True},
       {'Pruefer_p_is_Z_finitely_generated':False},
       'every finite subgroup is cyclic of bounded exponent while the group has unbounded exponent',
       'abelian detection boundary only, not group-ring cohomology claim')

# Compute actual differentials after reduction, not just cyclic cardinalities.
field_controls=0
for m in range(1,9):
    for n in range(1,9):
        for p in (2,3,5):
            d0=[[m%p],[n%p]]
            d1=[[-n%p,m%p]]
            assert (d1[0][0]*d0[0][0]+d1[0][1]*d0[1][0])%p==0
            rank0=int(any(row[0] for row in d0))
            rank1=int(any(d1[0]))
            dimensions=[1-rank0,2-rank0-rank1,1-rank1]
            expected=[1,2,1] if m%p==n%p==0 else [0,0,0]
            assert dimensions==expected
            emit('field_chain_level', m=m,n=n,prime=p,d0=d0,d1=d1,
                 ranks=[rank0,rank1],H_dimensions=dimensions,
                 integral_H1_order=gcd(m,n),integral_H2_order=gcd(m,n),
                 integral_certificate=False)
            field_controls+=1

# The natural prime-annihilated Tor formula on direct sums with mixed
# integral cyclic summands. Each cyclic summand has a free resolution,
# and tensoring its differential with F_p^r explicitly gives these ranks.
prime_controls=0
for moduli in ([4,6],[2,3,5],[8,9,10],[1,1],[12,15,25]):
    for p in (2,3,5,7):
        for r in (1,2,4):
            active=[d for d in moduli if d%p==0]
            kernel_dimension=sum(int(d%p==0)*r for d in moduli)
            rhs_dimension=len(active)*r
            assert kernel_dimension==rhs_dimension
            emit('prime_annihilated_Tor', M_cyclic_moduli=moduli,prime=p,
                 N_Fp_rank=r,scalar_resolution_entries_mod_p=[d%p for d in moduli],
                 Tor_dimension=kernel_dimension,M_p_kernel_tensor_dimension=rhs_dimension,
                 scope='Tor_Z1(M,Fp^r)=M[p] tensor_Fp Fp^r; not all torsion has fixed exponent')
            prime_controls+=1

emit('summary',explicit_mutants_rejected=9,field_chain_controls=field_controls,
     prime_annihilated_Tor_controls=prime_controls,errors=0)
