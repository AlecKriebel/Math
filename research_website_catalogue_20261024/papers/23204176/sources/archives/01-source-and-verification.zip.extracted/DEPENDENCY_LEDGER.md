# Dependency ledger

Version: candidate audit, 6 October 2026. All OpenAI inputs use public commit
`adc7f1241b42e322a6451854ab7e4b4c146bf78a`; hashes are in
`sources/UPSTREAM_MANIFEST.json`. Source-proof inspection is distinct from
machine checking and human refereeing. Early scoped audits retain their
then-pending dependencies; reconciliation below does not erase their limits.

## D1 — rational Chow-motive splitting

**Input:** T.-H. Bülles, *Motives of moduli spaces on K3 surfaces and of special
cubic fourfolds*, arXiv:1806.08284v1, Theorem 0.1; Manuscripta Math. 161
(2020), 109–124, DOI 10.1007/s00229-018-1086-0.

**Exact scope used:** S is a complex projective K3 surface, alpha is in Br(S),
and M is a smooth projective moduli space of Gieseker-stable alpha-twisted
sheaves, or of sigma-stable objects in D^b(S,alpha) for generic Bridgeland
sigma relative to fixed numerical data. For positive dimension, h(M) is a
summand of a finite sum of h(S^k)(t), 1 <= k <= dim M, t integral.
No fine-moduli or primitive-vector hypothesis is added. The actual stable
space is assumed smooth and projective. Empty and zero-dimensional cases
are treated directly, outside the literal positive bound on k. We do not
use the abelian-surface or cubic-fourfold scope.

**Validation:** primary statement/proof and Markman arXiv:math/0009109v4
Section 3 checked independently. Normalized quasi-universal/Brauer–Severi
Chern characters, not raw replicated Ext classes, justify non-fine data.
For M=S, doubling a universal family makes its raw Ext c_2 equal 4 Delta;
thus that unnormalized substitute would be false. It is not a counterexample
to the normalized splitting. Bülles's printed twist sign differs from a
printed Hom convention; our proof uses actual cycle codimensions.
Details: `agent_notes/bulles_transfer.md`.

## D2 — arbitrary mixed K3 products

**Input:** OpenAI, *The rational Hodge conjecture for products of K3 surfaces*,
cover date 4 October 2026, introduction Theorem 1.1: rational HC in every
codimension of every finite product of projective complex K3 surfaces,
with arbitrary different or repeated factors.

**Applicability:** tensoring D1 gives precisely such mixed products of
S_i powers. Separate self-power HC is insufficient. Conversely S^[1]=S
makes the universal target include this base theorem.

**Exact proof chain:**

1. `setup.tex` realization proposition requires a rational middle-degree
   class killed by the symplectic form and H^1-wedge injectivity for its
   degree-two annihilator. It supplies an ordinary mirror perfect complex,
   common nonzero rational Euler normalization and an Ext^2 bound.
   `exactks.tex` and `auxiliary.tex` check these hypotheses for their inputs.
2. `topology.tex`, `curvature.tex`, `comparison.tex`, `realization.tex`
   construct that complex: exact local domain/action control; relative
   interior-rooted perturbations with fixed ordinary child outputs;
   reciprocal corners including empty words; zero-input cyclic Stokes;
   cost-controlled ordinary copies, ultraproduct, telescope, saturation
   and proper Serre projection. The fresh analytic audit gives an explicit
   colored quasi-component extension and cited hypothesis mapping, not
   merely agreement of finite signs. Ordinary HMS/generation and topological
   inputs are separate cited obligations; they are not certified by that
   audit's verdict alone.
3. `cohomology.tex`: the cap action factors through Ext^2; sharp rank forces
   injectivity of the full semiregularity trace. Pridham's perfect-complex
   deformation and proper effectivity/spreading apply with smooth proper
   ambient assumptions. Proper relative cycle spaces and countability
   propagate a global horizontal Hodge section across a connected base.
4. `exactks.tex`: cap-rank rigidity recovers the exact full even-Clifford
   target, followed by deformation and specialization. Euler tests alone
   are not used to identify a transcendental component.
5. `auxiliary.tex`: the extra spin tensor requires a totally real Galois
   field, dimension >=5 congruent to 5 mod 8, signature (2,d-2) at every
   real place and Witt index >=2. The mixed proof constructs such data.
6. The quadratic-locus companion's general exact-KS criterion gives ordinary
   self-power HC by Clifford composition/PBW injectivity, an algebraic
   adjoint and divisor algebraicity. The general criterion itself does not
   retain the special-locus embedding assumption.
7. `mixed.tex` checks the joint Hodge group, shared simple constituents,
   central signs, graph cycles, torus-endpoint paths and CM pieces. It does
   not presume a product of individual Hodge groups. Finite spin/graph
   certificates support only the indicated algebraic identities.
8. Full HC for CM abelian varieties is an additional upstream input, D3.

**Validation basis:** independent algebraic/Hodge-group, topology, realization
and fresh analytic/category audits rederived the indicated mechanisms and
matched their pivotal primary-source hypotheses. Root read the full
comparison/curvature and propagation arguments. The separate ordinary-HMS
audit matched Seidel's generating enhanced quartic comparison and Abouzaid's
finite-object faithful functor to the actual spheres/graphs; the source proves
the needed graph fullness, uniform generation and product generation.
No demonstrated substantive gap remains in these scoped deductions. The
source proofs, rather than absence of a counterexample or agent verdicts,
are the mathematical inputs. Complete-package acceptance is recorded
separately by exact file hashes. Details are in `agent_notes/mixed_k3_audit.md`,
`ks_tensor_audit.md`, `realization_audit.md`, `ks_geometry_audit.md`,
`root_cm_and_deformation_audit.md`, `reviews/analytic_falsification.md`, and
`reviews/ordinary_hms_verifier.md`.

## D3 — CM rational HC and overlapping universal KS

**CM input:** OpenAI, *The rational Hodge conjecture for CM abelian varieties*,
cover date 30 September 2026, main theorem: rational HC in all degrees for
every complex CM abelian variety. Products of CM abelian varieties remain
CM. This is a new upstream theorem, not a classical consequence of CM theory.

**Mechanism checked:** CM tensor reduction/scalar descent; four-line surface
period; theta positive filtration and common-level continuity; rational
unitary splitting; full PEL moduli and Hecke correspondences; unnormalized
Satake factors; good ordinary CM points and commuting Frobenius/Albanese;
filtration-preserving idempotents and weak admissibility for both summands;
actual-compositum conjugate ranks; final scalar descent. Root read tensor,
moduli, Frobenius, CM-type and assembly sections. The independent theta/
Satake pass checked its complementary scope. A fresh arithmetic reviewer and
distinct finite-locus/Hecke reviewer independently rederived the ordinary-point,
full-tuple specialization, central normalization, complementary filtered
projector, actual-compositum rank and assembly deductions, with no identified
substantive gap. These audits rely on the precise standard moduli and p-adic
comparison results cited, and do not reconstruct their general foundations.
Finite counts do not certify theta or PEL geometry. See
`agent_notes/cm_theta_audit.md`, `cm_arithmetic_falsification.md`,
`cm_finite_locus_falsification.md` and root audit.

**Universal KS companion:** OpenAI, *Algebraicity of Kuga–Satake
Correspondences for K3 Surfaces*, cover date 3 October 2026, main theorem:
the prescribed exact full-even-Clifford KS tensor is algebraic for every
projective complex K3, with transported isogenous realizations. Its mechanism
overlaps D2. It is not an independent fallback and does not alone prove the
different-base assertion. It establishes an implicit single-base application
relevant to priority if the geometric input is sound.

## D4 — explicit transfer proved in this note

Split maps give A_j in CH^{a_j}(X x K_j)_Q, B_j in CH^{b_j}(K_j x X)_Q,
a_j+b_j=dim X+dim K_j, and sum B_j o A_j=Delta_X. For z of type (p,p),
A_j*z has type (q_j,q_j), q_j=p+a_j-dim X. Choose an algebraic representative
Z_j in that degree, or zero if its cohomological target is zero. Then
sum B_j*Z_j has codimension p and class z. Exterior products of split
maps preserve the diagonal identity and add codimensions.

**Status:** conditional implication independently checked, including r=0,
empty/zero-dimensional factors, codimension range, Hilbert n=0 and n=1,
mixed/repeated bases and non-fine/twisted data. Main.tex Proposition 2 gives
the self-contained proof. The unconditional theorem requires D2.

## D5 — attribution and verification limits

Arapura arXiv:math/0102070v5 Theorems 5.4, 5.7(3) and *Motivation for
Hodge cycles* Lemma 4.2, Theorems 7.4, 7.8 are earlier conditional transfers.
Quadratic-locus Corollary 9.5 already prints restricted moduli/self-power
consequences; its general criterion plus universal KS implicitly removes
the base restriction for self-powers. The mixed-moduli assembly is not
explicitly printed in the inspected primary corpus, which does not establish
novelty or a first claim. Only corollary-level scope recording is claimed.
The dated primary-source audit is `agent_notes/priority_audit.md`.

The actual Lean file contains Clifford/tensor identities only, no geometric
HC/KS or moduli theorem. No Lean build is relied on. `checks/FORMAL_SCOPE.md`
records this limit. AI tools were used extensively; these audits are not
conventional human peer review. No external person was contacted.
