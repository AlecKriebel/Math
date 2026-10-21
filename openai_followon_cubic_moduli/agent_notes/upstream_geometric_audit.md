# Independent geometric audit of family 037

Audit checkpoint: 2026-10-07 05:11:49 UTC (2026-10-06 22:11:49 America/Los_Angeles).

## Verdict and precise scope

I found no blocking mathematical defect in the cone reduction, the small-stabilizer classification, or the fourfold companion on the passages inspected. This is a scoped handwritten audit, not formal certification of family 037 or an unconditional endorsement of the cubic application. In particular, the all-dimensional theorem still depends critically on the large-stabilizer semigroup and slice arguments, which are outside this assigned audit and must survive a separate review. The strongest checked claim here is that these three inspected components present coherent mechanisms with the numerical constants and pivotal orbifold-curve citation matching their stated uses.

Best-guess completion for this assigned geometric audit: 90%. Best-guess contribution to the overall mathematical resolution: no independent percentage assigned; the parent must combine all route reviews. Publication-package completion contributed here: 0% (only audit evidence; no publication candidate reviewed).

The exact desired upstream inequality is, for a singular closed point of a normal complex algebraic boundary-zero klt k-fold with Q-Cartier canonical divisor,

\[
\widehat{\operatorname{vol}}(x,X)\le 2(k-1)^k,\qquad k\ge2.
\]

The upper bound is the relevant input. Its equality assertion is unnecessary for the basic metric-density implication and was only checked incidentally here.

## Sources and immutability

Read the original user request, workspace AGENTS.md, upstream repository README, manuscript README, family 037 introduction, cone-reduction section, complete small-stabilizer section, bootstrap statements, and the entire fourfold companion TeX. Upstream `/Users/alec/Desktop/math` was kept read-only. HEAD was `adc7f1241b42e322a6451854ab7e4b4c146bf78a`; a read-only remote-ref lookup returned that same main commit during the audit.

Pinned SHA-256 inputs:

| File, relative to upstream | SHA-256 |
|---|---|
| `preprints/The-ordinary-double-point-gap-in-every-dimension-September-24-2026/build/sections/02-cone-reduction.tex` | `ae291fa3bae1940acb43296a0e5c110f1334106eb5d5738d36ae3bbbd1df644b` |
| `preprints/The-ordinary-double-point-gap-in-every-dimension-September-24-2026/build/sections/03-small-stabilizers.tex` | `3ec308d2622e15d57e519e2e94faa1aca2dfa7b682058f590eb5badf9d78fcb1` |
| `preprints/The-normalized-volume-gap-in-dimension-four-September-24-2026/build/paper.tex` | `2e1eb5a05a308182d34d75eb428474fbe11cce86445cb01bc4e654e9a5e25390` |

No `lean/docs/037.md` exists at this pin, and the formalization catalog did not contain an ODP/normalized-volume/Fano gap entry. I did not claim any Lean verification or run a Lean build. Absence of a formalization is not a mathematical objection.

## 1. Cone reduction: checks and falsification attempts

Source: `02-cone-reduction.tex`, especially lines 88–150 and 285–364.

1. **Infimum preservation is explicit.** Stable degeneration is invoked on a genuine normalized-volume minimizer, and the polystable cone's Reeb valuation is again asserted globally minimizing. Thus equality of its value with the original infimum is stronger than preservation of an arbitrary test valuation. This passage cannot by itself bound a metric Reeb valuation without the separate metric-minimization theorem, which the application audit must supply.
2. **The smooth-product direction is correct.** For an N-dimensional test valuation with discrepancy A and volume sigma, the extension of added-parameter weight A/N has discrepancy A+A/N and volume N sigma/A. Dividing by (N+1)^(N+1) returns A^N sigma/N^N. Taking infima yields the required density inequality in the upper-bound direction.
3. **Orbit semicontinuity has the correct sign.** The vertex is a specialization, so its normalized volume is at most the volume at a nonvertex orbit point. A slice transverse to a nonconstant grading orbit is étale-locally a smooth-curve factor; if its point were singular, the lower-dimensional ODP bound would give density at most p_(n-1), strictly below p_n. This forces a smooth puncture. No same-dimensional upper bound is used here.
4. **The canonical-index step uses only the universal bound.** A degree-q crepant index cover, with one point over the vertex, has density q times that at the cone. Hence d<=1/q, and p_n>1/2 forces q=1 for n>=5. The one-point fiber argument is supported by the graded canonical-cover multiplication: a nonzero residue-degree homogeneous element whose power is a unit would trivialize a smaller canonical power.
5. **Embedding dimension is controlled without a dubious limiting assertion.** Finite generation gives a locally finite positive value semigroup, and the finite-discrepancy Izumi bound makes successive initial-form cancellation terminate modulo m^2. The second degeneration uses ordinary upper semicontinuity of embedding dimension. This ensures the cone remains singular and gives the needed direction edim(original)<=edim(cone).
6. **Primitive approximations control absolute error.** Dividing lattice approximants by their gcd preserves an error tending to zero. If the primitive canonical weights stayed bounded on an irrational Reeb ray, a bounded lattice subsequence would force rationality. Thus the subsequent integer-rounding step has the appropriate absolute, rather than merely relative, approximation.

I attempted failures from nonisolated points, finite kernels in the grading, equality at the universal smooth bound, and a singular slice hidden by an étale cover. The manuscript's hypotheses address these cases. This review relies on the cited stable-degeneration and finite-degree theorems; it does not independently reprove those established inputs.

## 2. Small stabilizers: citation and internal mechanism

Source: `03-small-stabilizers.tex`, all 515 lines. The density assumption is already used in cone reduction; the classification itself operates on a K-polystable Gorenstein cone with smooth puncture.

### Pivotal orbifold-curve input

Read the primary source [Li–Zhou, *Minimal log discrepancy and orbifold curves*, arXiv:2502.11847v1](https://arxiv.org/html/2502.11847v1), Proposition 2.6 and its preceding deformation/bend-and-break argument. It supplies a representable map from a weighted projective line with at most one stack point and anticanonical degree plus inverse age at most dim(B)+1. Its Fano-orbifold hypothesis matches the quotient stack here. The separate ample-tangent hypothesis belongs to another theorem and is not required by Proposition 2.6.

### Potential failure points attacked

* **Minimal degree and source inertia.** Since stabilizer orders are bounded and source inertia injects, the possible rational L-degrees have bounded denominators and possess a least positive value. If the source is P(1,ell), with pullback O(e), ell divides the endpoint stabilizer m. The quantity em/ell is a positive integer, and the small-stabilizer bounds put it below 2, forcing e=1 and ell=m. No unsupported continuous minimization is hidden here.
* **Deformation dimension and fixed lift.** The Euler-characteristic calculation retains source coordinates and torsor identification, so it correctly counts a rank-n bundle rather than only the rank-(n-1) tangent of B. Fixing the residual gerbe subtracts the invariant fiber dimension. Representing the trivial character by m gives chi=n+r/m-sum b'_j/m. Tests on ordinary affine space and the quadratic cone reproduce their expected n and n-1 dimensions, respectively.
* **Finite evaluation.** A finite basepoint of a limiting map loses positive L-degree on the horizontal component of a stable graph map. A terminal leaf has one node and no markings, so it cannot be constant by stability and is of the one-stack-point type used in the minimum. That leaf consumes the whole minimum degree. Consequently the horizontal map is constant, and a vertex evaluation is the unique contracted orbit map. Positive grading plus graded Nakayama makes evaluation finite. This avoids assuming a compact parameter space of affine maps.
* **Norm tensor.** The additive source transformation y->y+t x^m gives a nonzero vector along evaluation of derivation weight -m. The symmetric product over all generic sheets is nonzero in characteristic zero; taking a trace instead could cancel, but that is not what is done. Its coefficients are integral over the smooth base and lie in its fraction field, hence regular. Normality of the source is unnecessary for this descent.
* **Metric tensor estimate.** On the Ricci-flat smooth puncture, the induced Chern connection on Sym^b T has zero mean curvature. Bochner and Cauchy–Schwarz make every positive power of the tensor norm subharmonic. A tensor of derivation weight tau has norm radial degree tau+b. If tau+b<0, a sufficiently small positive norm-power has radial exponent in (2-2n,0); angular integration of the cone Laplacian is then negative, contradicting subharmonicity. Thus tau>=-b. This checks both the rank dependence and sign; it does not use a scalar-function obstruction as a substitute for a tensor argument.
* **Irregular Reeb fields and unbounded ranks.** Pairing a tensor with products of generator differentials embeds it into tuples of regular functions. A nonzero pairing of degree at most const*r*b has a monomial representative with at most const*b generator factors, giving character norm O(b), independent of the changing rank. Hence the approximation error contributes O(b*||epsilon||), and division by b makes integer rounding legitimate. The inequality 0<=nm-r<=const*||epsilon|| eventually forces nm=r. This is valid on a constant exact rational grading as well.

No explicit counterexample to this mechanism was obtained. Full analytic verification of the Collins–Szekelyhidi existence theorem was not duplicated; the smooth-puncture, Q-Gorenstein klt, K-polystable input stated here is the appropriate setting for that established theorem.

## 3. Sole fourfold companion: proof path and arithmetic

Source: `The-normalized-volume-gap-in-dimension-four-September-24-2026/build/paper.tex`, entire manuscript. The unrestricted upper bound 162 is a genuine base input; Liu's lci theorem alone would not supply it without the structural reduction.

### Transverse-jet stabilizer estimate

The test valuation on the grading-extraction slice has weights (1,alpha,alpha,alpha). Its discrepancy is r+3 alpha. A given-degree component can contribute at most the smaller of its Hilbert dimension and the available transverse jets in its stabilizer character. Faithfulness gives 1/m of the leading three-dimensional jet count. The integral

\[
4\int_0^1\min\{h z^3,(1-z)^3/(m\alpha^3)\}\,dz
=h/(1+\alpha(mh)^{1/3})^3
\]

has the stated value. If m/r>=2/5, Q=mhr^3>=324/5>64; the logarithmic derivative at zero of the normalized comparison is 12-3 Q^(1/3)<0. A fixed small rational delta therefore contradicts convergence of the degree tests to the actual infimum. This provides the strict m<r/(5/2), with constants allowed to depend on each fixed grading. Integer discrepancies then yield A_C(F)>=3 for every primitive divisor centered at the vertex.

### Hilbert duality and Fourier tests

The pole exclusion is supported by a Koszul finite-length argument: a root of unity cannot be a Hilbert-series pole unless it fixes a nonvertex point. Rescaling lambda m<1 moves every nonzero pole frequency outside [-1,1]. Cohen–Macaulay graded duality supplies the negative-index expansion via the canonical module, so the signed full-line coefficient measure has no finite Laurent-polynomial error. Band-limited Schwartz tests therefore equal the zero-frequency polynomial integral. The approximation procedure only passes polynomial moments and fixed atom values to a limit; it does not exchange an uncontrolled infinite discrete sum with a limit.

I recomputed the stated Fourier-test arithmetic exactly using `fourfold_constants_check.py` (standard-library Fractions, no numerical approximation). The checks produce:

| Quantity | Exact value |
|---|---|
| M0, M2, M4, M6 for shifted g3 profile | 13/16, 61/64, 685/256, 11101/1024 |
| coefficient of c in fourfold test | 50065/9216 |
| fourfold moment expression at c=-1 | 26581/4096 |
| conservative fourfold contradiction margin | 209183/1440000 > 0 |
| dimension-three conservative margin | 19/324 > 0 |
| dimension-two integral | 5/27+c/3 > 0 |

The canonical-positive injection lemma has the correct direction: lowering a q-th canonical power by e>0 forces canonical weights positive and yields L1>=e L/(2q)>0. Its subleading-coefficient additivity is a height-one DVR computation; codimension-two errors do not affect the coefficient used.

### Threshold and terminal section

The low-weight basis is not assumed to generate the maximal ideal. The comparison d0*ord(b)/B>=ord(m) correctly gives an upper bound on the powered low-weight ideal's threshold, even with additional positive-dimensional centers. Averaging sufficiently many general powered sections yields an lc homogeneous boundary whose lc centers are contained in the common zero locus of low-weight functions. Its total weight is less than the canonical weight, so the vertex cannot itself be an lc center.

Affine subadjunction gives a normal Cohen–Macaulay minimal center. For a curve, its generator weight is its punctured stabilizer order after rescaling. For a surface, Q-factoriality of a klt surface pair gives a positive canonical generator power. For a threefold center, it is a Cartier divisor on the smooth ambient puncture; the order of a low-weight function along that divisor gives the required generically nonzero canonical-power injection of degree b-q*(5/2)<0. Reflexive extension across the vertex preserves it. These three cases support the threshold contradiction lct(m)>3/2.

Finally the terminal section argument uses both A_i>=3 and A_i/b_i>3/2. If b_i=1, A_i-b_i>=2. If b_i>=2, A_i-b_i>b_i/2>=1. Thus all ordinary hyperplane-section discrepancy coefficients A_i-1-b_i are positive. A normal Gorenstein terminal threefold is cDV and hence a hypersurface, bounding edim(C)<=5. Only then is the established lci normalized-volume bound applied. I found no circular invocation of the sought fourfold bound in this chain.

## Remaining validation limits

* This does not check the all-dimensional large-stabilizer semigroup saturation or filtration/slice comparison. Those are indispensable to the unrestricted n>=5 inequality and can block the entire publication route despite the favorable scope of this audit.
* The correctness of the cubic consequence also needs metric Reeb minimization, treatment of iterated singular cone strata, precise polarization/Cartier descent, and the exact Spotti–Sun topology. None is established by this note.
* No publication, external communication, git mutation, or upstream source build was performed by this audit. No citation metadata or authorship was altered.
