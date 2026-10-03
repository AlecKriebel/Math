# Attempt 3 — exact reduction for split semisimple kernels

Third substantive proof attempt. The goal is to remove faithfulness and irreducibility from the split case, while keeping precise control over which hypothesis fails in general.

## 1. A subdirect decomposition of a semidirect product

Let H be finite, and let M=M_1 direct_sum ... direct_sum M_t be a finite direct sum of nonzero irreducible modules M_i over prime fields F_{p_i}; the primes may differ. H acts on M componentwise, and the action on M is not assumed faithful. Put G=M semidirect H. Let K_i be the kernel of H's action on M_i and Q_i=H/K_i. Put A_i=M_i semidirect Q_i, with its faithful irreducible action.

There are surjective homomorphisms

pi_0:G->H,       pi_i:G->A_i,

where pi_i sends (m_1,...,m_t,h) to (m_i,hK_i). Surjectivity follows by choosing an arbitrary lift h of the quotient element and an arbitrary component m_i. The combined map into H x product_i A_i is injective: pi_0 determines h, and the remaining pi_i determine every component m_i. Consequently G is a subdirect product of H and the A_i, and

var(G) = var(H) join var(A_1) join ... join var(A_t).         (6)

This equality holds even when several M_i are isomorphic. Repeated factors do not change the join.

## 2. Exact spectrum comparison and convergence criterion

Each A_i is covered by attempt 2 and has root limit |Q_i|. Put d=max_i |Q_i|. From (6) and the pointwise inequalities of attempt 1,

max(a_H(n), max_i a_{A_i}(n)) <= a_G(n)
                                <= a_H(n)+sum_i a_{A_i}(n). (7)

In particular,

limsup a_G(n)^(1/n) = max(limsup a_H(n)^(1/n), d),
liminf a_G(n)^(1/n) = max(liminf a_H(n)^(1/n), d).           (8)

For completeness, the liminf identity follows because max_i a_{A_i}(n)^(1/n) converges to d. If y_n->d, then liminf max(x_n,y_n)=max(liminf x_n,d). The nth-root difference between the upper and lower bounds in (7) is bounded multiplicatively by (t+1)^(1/n), which tends to 1. All sequences are uniformly bounded by the Birkhoff bound, so this multiplicative squeeze is valid.

If H has a root limit L, then G has root limit max(L,d). If limsup a_H(n)^(1/n)<=d, then G has limit d even without assuming convergence for H. Thus a sufficiently strong semisimple action can dominate an unresolved quotient spectrum.

## 3. An explicit infinite family

For G=C_p semidirect C_m, with a faithful action and m dividing p-1, (5) gives root limit m. Composite m is allowed. For example C_5 semidirect C_4 has limit 4. More generally, if a finite abelian H acts semisimply on M, then H has limit 1 and G has limit max_i |H/K_i|, an integer. When p_i is coprime to |H|, semisimplicity is automatic by Maschke, but the theorem also applies to semisimple modular modules.

This action-image formula is more precise than simply replacing G by H: H can have potential 1 while G has arbitrarily large integer potential. For example the abelian group C_m has limit 1, whereas the faithful affine extension above has limit m. Therefore an induction step that replaces an arbitrary abelian extension by its quotient cannot be correct.

## 4. Why this does not finish the general case

An arbitrary abelian normal subgroup need not be a semisimple H-module. For example let H=C_p act on M=F_p^2 by the nonidentity unipotent matrix [[1,1],[0,1]]. M has an invariant line but no invariant complementary line: its only invariant lines are contained in the 1-eigenspace, which is one-dimensional. Thus the component projections needed in (6) do not exist.

The quotient module and its submodule are both trivial H-modules, but the whole action is nontrivial. Composition factors cannot be substituted for direct summands in (6). This example is a p-group semidirect product and therefore does itself have limit 1; it refutes the proposed decomposition argument, not the original conjecture.

A nonsplit group extension has a second independent obstruction: even if its abelian normal subgroup is semisimple as a module, a projection G->M_i semidirect Q_i may not exist. The split group is a section of a direct square of G, giving a lower bound only. The opposite inclusion of varieties is not supplied by that construction.

## Outcome

A full formula is proved for split semisimple abelian kernels, conditional only on whatever is known for the quotient H. The resulting exact limsup/liminf formula sharply identifies potential domination and shows why naïve quotient invariance fails. Arbitrary nonsplit extensions and nonsplit module layers remain unresolved.
