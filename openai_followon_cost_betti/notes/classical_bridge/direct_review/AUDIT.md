# Independent adversarial audit of the direct Betti computation

Audit checkpoint: 2026-10-07 04:41:56 UTC (2026-10-06 21:41:56 America/Los_Angeles).
Reviewer: independent `direct_betti_falsifier` subagent.
Reviewed file: `../DIRECT_BETTI.md`.
Reviewed SHA-256:
`00a6e16cd486f04ddc23d9a3b5bd7f8f334bc9bb264c824232ba2844afd05f21`.

**Verdict:** the reviewed proof establishes, for its explicitly defined group,
`beta_n^(2)(Gamma)=0` for every `n>=0` and contractibility of the universal
cover of the displayed finite two-dimensional presentation complex. No
substantive mathematical gap or counterexample was found. This verdict does
not certify a cost lower bound, failure of fixed price, priority, or novelty.

The target conclusions were treated as hypotheses. Success required checking
the embeddings and presentation independently, deriving the cellular maps
with one fixed convention, establishing actual Hilbert-space injectivity,
and checking that the ordinary-homology and dimension deductions did not
assume the desired asphericity. Each requirement passed.

## Checks and exact mechanisms

| Reviewed lines | Potential failure attacked | Independent verification | Result |
| --- | --- | --- | --- |
| 20--34 | Amalgam presentation or vertex embedding is assumed incorrectly | Commuting with the listed generators is equivalent to commuting with J; maps from the presentation and amalgam are inverse by their universal properties. Moreover the presentation maps to `A x Z` by `a -> (a,0)`, `b_i -> (b_i,0)`, and `t -> (1,1)`. Its restrictions to A and to `J x <t>` are injective. Thus the particular needed embeddings and infinitude do not even require a normal-form theorem. | Pass |
| 47--60 | Surjectivity is mistaken for a free basis | Let the new abstract free basis be `a,U_1,...,U_99`. Define old-to-new by `b_i -> a^-1 U_(i-1)^-1 U_i`, with `U_0=1`, and new-to-old by `U_i -> u_i`. The compositions are identity on every generator, by the successive recursion for u. | Pass |
| 73--90 | Bipartite graph has hidden cycles because the identity label disappears | A nonbacktracking closed walk gives an alternating-sign word. Consecutive labels differ, so two zero labels cannot be adjacent. Removing a zero joins equal signs; any opposite-sign adjacent letters after deletion already had distinct labels. The resulting nonempty freely reduced word cannot be identity. Connectivity and degree 100 follow directly from the zero matching and free generators. | Pass |
| 92--112 | Regular-tree adjacency admits an L2 eigenvector at zero | For depth `n>=2`, the displayed Cauchy--Schwarz inequality sums to `E_(n+1)>=E_(n-1)` because every depth `n-1` vertex has exactly `q=d-1` children. Summability makes every positive odd and even layer energy zero; the equation at a depth-one vertex then kills the root value. The proof is valid for complex-valued f and for `d=2`. | Pass |
| 114--138 | Left/right convolution or cosets reversed | Coefficients of `fS` are `sum_i f(g u_i^-1)`, exactly T*. Also `(I T I f)(g)=sum_i f(u_i^-1 g)`, exactly Sf. Right multiplication preserves left cosets `gF`, and left multiplication preserves right cosets `Fg`; each restriction is unitarily a copy of the corresponding F operator. For `f(t-1)=0`, coefficients are constant on every infinite right t-orbit, hence zero. | Pass |
| 146--208 | Fox matrix transpose or coefficient order changes the kernel argument | Choose every lifted x-edge from 1 to x. Its boundary is `x-1`; a positive occurrence contributes its preceding prefix and a negative occurrence minus its following prefix. Free left-module coefficients q therefore multiply these prefixes on their right. Exact derivation gives `D_x r_v=t D_x v-r_v D_x v` for `x!=t`; setting `r_v=1` gives `(t-1)D_x v` in the written order. `D_t r_v=1-t v t^-1=1-v` in Gamma. | Pass |
| 210--217 | An unjustified commutation or inverse is needed for d2 injectivity | From `q_w(t-1)S=0`, injectivity of right S gives `q_w(t-1)=0`, then right `t-1` gives `q_w=0`. The b coordinates give `q_i=0`. All products are bounded finite group-ring convolutions; no closed-range assumption, bounded inverse, or interchange of S with t is used. | Pass |
| 226--247 | Dimension cancellation conceals a nonzero reduced homology module | `d1* f=0` implies right invariance under every generator, so f is constant and zero on infinite Gamma. Thus `closure(im d1)` has dimension 1. Polar decomposition identifies `closure(im d2)` with the 100-dimensional domain because the kernel is zero. Its inclusion in the 100-dimensional `ker d1` leaves an orthogonal complement of trace zero, which is zero by trace faithfulness. | Pass |
| 251--263 | L2 injectivity does not imply ordinary acyclicity, or acyclicity is mistaken for contractibility | Integral cellular chains have finite support and embed in the completed Hilbert chain groups. Therefore the ordinary d2 is injective and H2 is zero. The universal cover is simply connected, so H1=0, and its dimension makes higher homology zero. It is connected, so reduced H0=0. Successive Hurewicz, starting with pi2, kills every higher homotopy group; the CW Whitehead theorem gives contractibility. | Pass |
| 265--315 | Euler characteristic or classical machinery is promoted to the missing conclusion | The reviewed document explicitly rejects the Euler-only shortcut and explicitly reserves cost and novelty. Its invariant argument does not use upstream cost estimates. | Pass within assigned scope |

## Independent derivation of the decisive maps

Write `P_i=u_(i-1)a` and `S=sum_(i=0)^99 u_i`. The a occurrences in
`w=ab_1a...b_99a` have preceding prefixes `u_0,...,u_99`, while the
unique b_i occurrence has preceding prefix P_i. Hence

    D_a w = S,       D_bi w = P_i.

For `r_v=t v t^-1 v^-1`, the full free-group identity is

    D_x r_v = t D_x v - r_v D_x v       (x != t).

After imposing the relator, this becomes `(t-1)D_x v`. Thus in free
left cellular modules, with q written to the left of cells,

    (d2 q)_a    = q_w (t-1) S,
    (d2 q)_bi   = q_i (t-1) + q_w (t-1) P_i,
    (d2 q)_t    = sum_i q_i (1-b_i) + q_w (1-w),
    d1 f        = sum_x f_x (x-1).

The free-group telescoping identity is

    S(a-1) + sum_i P_i(b_i-1) = w-1.

For the w row, composition of the proposed d2 with d1 is consequently
`(t-1)(w-1)+(1-w)(t-1)=tw-wt`, which is zero by the defining relation.
For the i row it is `tb_i-b_it`, likewise zero. The exact order of
every factor agrees with the injection argument above.

## Reproducible algebra and boundary cases

`check_fox.py` uses exact integer group-ring coefficients and freely reduced
words. Running it with Python 3 reproduces `check_results.json`. It verifies
both directions of the free-basis substitutions, the S and P derivatives,
the full relator derivatives before quotienting, and all full Fox boundary
identities, for n=0,1,2,99. All checks passed. Its n=99 checks use the exact
words in the reviewed proof, not a numerical approximation or a finite
permutation representation. These checks supplement the mathematical
argument; they do not numerically certify infinite-dimensional injectivity.

- The tree lemma covers the limiting rank-one case (`d=2`, `q=1`). It
  does not assert anything for `d=1`, where an infinite connected
  1-regular tree does not exist. In the zero-b_i parameter case S=1 is
  directly injective and the presentation is the torus group Z^2.
- The t argument really uses infinite order. A finite-order replacement
  admits nonzero square-summable constants on its finite right orbits.
- The free-basis step is essential to the particular tree argument. One
  cannot replace the u_i by an arbitrary dependent list while retaining
  the claimed tree. The reviewed proof establishes independence by inverse
  maps, not by an unverified subgroup-rank estimate.
- Injectivity does not mean invertibility or positive lower singular
  bound. The dimension argument uses closure of the image throughout.
- The contractibility argument uses simple connectivity of the universal
  cover, not a claim that an arbitrary acyclic complex is contractible.
- Here the finite presentation gives a genuine finite two-dimensional
  K(Gamma,1) after the contractibility proof; higher L2 Betti numbers
  therefore have no uncomputed higher-dimensional chain contribution.

## Scope, exact gap, and completion estimate

Strongest verified result: the all-degree Betti vanishing and finite
two-dimensional classifying-space claim in the reviewed file.
Exact remaining mathematical gap for those claims: none found.

For the original relation-level target, a strictly positive cost gap is
still required; this audit supplies no evidence for it. Establishing
novelty or priority likewise requires its own source audit. The conclusion
here is correctness of this derivation, not a claim that its output is new.

Assigned adversarial direct-proof review completion estimate: **100%**.
No Git mutations, publication/deposit writes, upstream writes, external
communications, or cost-proof audit were performed. All created files are
inside `notes/classical_bridge/direct_review`.
