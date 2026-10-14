# Independent acceptance of the coarse tree countermodel

Shared PASS 2,14 October2026. Reviewed artifact: `pass2_concentration_audit/COARSE_TREE_COUNTERMODEL.md`, SHA-256 `35ac9aef233a2b29a752f5f393fe4c01c5084efdc240b2e0c54563e21c453cc5`.

**Accepted with its explicitly limited scope.** The construction disproves an implication from the four listed coarse abstract-tree hypotheses to completion-weighted ancestor-label concentration. It is not an avoidance-class counterexample, and its failure of the sharper avoidance-specific bound is correctly disclosed.

Independent checks:

1. Every vertex has exactly L distinct children, even when several children have the same type and label. The largest label is L+1. The sorted child-label lower bound holds in each of the three transition cases, including L=1,2,3.
2. For B-type label L, the descendant generating function C(z)^L solves `D_L=1+z sum_(j=2)^(L+1) D_j`, using C-1=z C^2. The A-only level counts, early exit, and later exits in G(z,u) have the correct levels and powers of u. The last-A-level marker includes terminal A vertices correctly.
3. Setting u=1 simplifies to `A=1+w+z^2/(1-3w)`, where z=w(1-w). The unique pole inside |z|<1/4 is rho=2/9. Its principal coefficient is2/81, since w'(rho)=3. This proves the stated growth rate9/2.
4. Algebra gives the displayed identity for I=1-1/A. The reciprocal-D coefficients begin1,2,6,18 and their recurrence preserves strict positivity and increase. Thus3d_n-d_(n-1)>0 and I has nonnegative integer coefficients. The positive-size atom-word interpretation yields a genuine concatenation injection, hence supermultiplicativity of the level-count sequence; it does not identify the original tree with a permutation class.
5. Near u=1 the only dominant pole is `rho(u)=(3u-1)/(9u^2)`. The competing pole near1/3 and Catalan singularity1/4 stay outside a fixed smaller circle. Analytic pole subtraction and uniform Cauchy bounds justify differentiating coefficient asymptotics. Here rho'(1)=-1/9 and rho(1)=2/9, so the exact uniform-level law gives `E R=n/2+O(1)`.
6. Before the first B exit, labels are j+1. The number of ancestor levels with label at least epsilon*n is bounded below by R-epsilon*n-1, including terminal A paths. Taking expectations yields the claimed liminf at least1/2-epsilon.
7. The stated stronger-bound failure is exact: D_3(A3)=3D_2(A4)=3(3*5+2)=51, while binom(5,3)*a_3=10*5=50. Therefore the note cannot refute an argument that actually uses that sharper constraint.

No mathematical correction is requested. This accepted obstruction does not affect the independently accepted adjoining-minimum merge theorem.
