# Independent audit: transfer and limit barriers

Completed 2026-10-24T20:51:11.183764+00:00. Assigned-review completion estimate: **100%**. Verdict: **PASS within the explicitly partial scope**. AI review only; no human peer review or originality assertion.

## Homomorphisms and equality requirements

Every commutator expression pushes forward under a homomorphism, proving cl_G(f(w)^n)<=cl_H(w^n) and hence the asserted scl monotonicity. An embedding therefore gives only the stated ambient upper bound. A retraction gives the reverse inequality by the same argument. If an extremal homogeneous quasimorphism extends with the same defect, Bavard gives the reverse inequality and hence equality; the draft does not claim such an extension exists.

For a quotient, any chosen commutator decomposition of h downstairs lifts factor by factor to a w in the derived subgroup of the free group upstairs. If h has an irrational scl value, the resulting free-group w still has rational scl by free-group rationality. This correctly disproves an inference of irrationality from an irrational lower bound. It makes no unsupported claim about arbitrary prescribed preimages.

The cited finite-index non-isometry obstruction is valid as an element statement in the explicit one-boundary example separately audited in FINITE_INDEX_AUDIT.md. The old rank-two isometry conjecture is used as a limitation of that source, not as an asserted present-day open question or theorem that all inclusions preserve scl.

## Amenable-kernel counterexample

The total golden-ratio Thompson lift G fits the central extension 1->Z->G->T_tau->1. The kernel is cyclic, hence amenable. The primary Fournier-Facio–Lodha arXiv:2110.06286v2, Lemma3.15 (printed p10), puts the unit translation z in G'. Its translation number is1, and the same paper's exact computation of scl on G' gives scl_G(z)=1/2. Its image in T_tau is the identity and has scl0. Consequently amenability of the quotient kernel alone does not give equality of scl for all commutator-subgroup elements.

This is consistent with the bounded-cohomology mapping theorem. The comparison map Hb²->H² and its kernel matter for homogeneous quasimorphisms; an isomorphism on full bounded cohomology under the quotient pullback need not be an isomorphism on those kernels. The central-extension Euler class is precisely compatible with a primitive rotation quasimorphism upstairs. No extra descent or defect-preservation claim is assumed.

## Frozen 2026 Rips-limit source

I independently downloaded arXiv:2603.12095v1 and matched the parent's cached PDF exactly (SHA256 29911f50ad94711f0c41fe94159b8ef4b4f438e126c774458366c4e33b4ab06e). Its title is *Profinite isomorphisms, stable commutator length, and fixed point properties*, Francesco Fournier-Facio. Theorem3.2 and its proof (printed pp9–10) construct quotient stages Gi that are torsion-free, hyperbolic and virtually special, with a residually finite direct limit G∞ and normal subgroup N∞ with vanishing intrinsic scl. Theorem4.1 and its proof (printed pp11–14) additionally make N∞ perfect and ensure G∞ surjects onto Higman's group. The introduction also explicitly distinguishes the finite stages from the limit.

The nontriviality needed for the obstruction can be justified without adding a source hypothesis: G∞ surjects onto nontrivial Higman's group, so is nontrivial; residual finiteness gives a nontrivial profinite completion; the asserted isomorphism of profinite completions N∞^ -> G∞^ then forces N∞ nontrivial. A nontrivial perfect group cannot be abelian, so there are u,v in N∞ with c=[u,v]!=1. Intrinsic scl_N∞(c)=0. Monotonicity gives scl_G∞(c)=0. Under an injective homomorphism of G∞ into a RAAG, c remains a nontrivial commutator and again has ambient scl0.

This contradicts the sharp RAAG gap. I checked the published primary Heuer article *Gaps in scl for Amalgamated Free Products and RAAGs*, Geom. Funct. Anal.29(2019),198–237, DOI10.1007/s00039-019-00477-5: Theorem7.3 states scl(c)>=1/2 for every nontrivial derived-subgroup element of a RAAG. Its exact published PDF is independently cached and hashed. For an infinite defining graph, the finite-support retraction reduces this to the same finite-graph theorem. Thus the proposed limit embedding would indeed be impossible, rather than a consequence of the finite-stage virtual specialness.

The draft correctly refrains from concluding either specialness, virtual specialness, or embeddability of the direct limit merely from the stage properties. It also does not assert that every arbitrary direct limit has the same obstruction. The frozen paper's main theorems concern vanishing/unbounded scl and profinite invariants; no theorem resolving RAAG scl rationality appears in its text. The word search for rationality was empty, supplemented by inspection of its introduction, stated theorems and concluding limitations. This is a scope check, not a new correctness audit of that entire paper.

## Infinite graphs and limiting constructions

For any finite-support word w in an infinite RAAG, the induced finite special subgroup contains w and is a retract. Inclusion and retraction give both inequalities for every cl(w^n), hence equality of cl and scl. If w is known only to be a commutator product in the full group, retraction also proves its membership in the finite subgroup's derived subgroup. Thus infinite graph size alone adds no new elementwise scl values.

Real chain homogeneity can trivially create irrational values by irrational coefficients, but that does not give a group element answering the problem. Likewise limits of values on varying words do not realize a value on one fixed word. The draft observes these differences correctly.

Automorphism invariance follows from monotonicity in both directions. The finite rational linear-program observation is standard and correct for a rational objective over a rational polyhedron with finite attained optimum. It only excludes obtaining irrationality from a complete finite rational LP description of the optimization; the draft does not purport to have such a description for all RAAG surfaces. More complicated infinite, nonlinear or nonpolyhedral mechanisms remain unaddressed.

## Exact scope left open

These arguments identify failures of proposed transfer and limiting shortcuts. They establish neither universal RAAG rationality nor a fixed RAAG word with irrational scl. The genuine remaining requirement is an exact computation or a matching extremal proof for an eligible fixed word. No publication gate opens from these partial barriers.
