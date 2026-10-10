# Audit of the four additional trisection TQFT approaches

Problem 30006636 / OWR-14299913-005. Independent follow-up audit, 8 October 2026.

## Verdict and version boundary

**Accept the corrected five-approach report as a partial answer.** Its finite-group extendability theorem, explicit component-color bordism functor, universal-construction rank defect, regular dihedral central-lift obstruction and finite-order mapping-torus criterion are correct with the qualifications below. The first-stage normalization audit remains unchanged.

One substantive correction was required: the three-manifold in the mapping-torus argument must be connected when normalization is a constant applied to each connected closed four-manifold. The corrected report adds that hypothesis and explains it. The original unqualified statement is not accepted.

The initial report has 16,445 bytes and SHA-256 `706122a31f7e3fdcf6b45d2220b5c498cd2d23c50937e2c0f37489b7862ce7ce`. The accepted corrected report has SHA-256 `e3c128de7015148827e998dbc5ac779e4167963dfa0fa1f95650f521244eb79c`. Both exact snapshots are retained separately. The accompanying `FIVE_APPROACH_CORRECTION.patch` displays the entire difference. No other mathematical change was made to the report during this audit.

The packet now contains five substantive approaches. This is a count of distinct investigated mechanisms, not five solutions or five successful obstructions. The broad workshop question is still unresolved in this packet. In particular, no general theorem about extension after normalization or realization by fusion 2-categories has been proved.

## Approach 2 source reduction and complete normalization

Let `N=|B||C|` and `m=|M|`, for a nonempty transitive `(C x B^op)`-set with the untwisted, standard-trace MMT data and identity pivotal functor. All simple region dimensions are one. Corollary 6.16 of the MMT v1 manuscript, pages 61--62, explicitly reduces the admissible-label count to `m` times the one-point count. Both pages were independently inspected, including a visual check. The source deserves and receives credit for this reduction.

The source's proof cuts along the red curves to a sphere with holes. Choosing one region label fixes every other region label. Blue and green crossings introduce no additional monodromy condition because the two actions commute; the remaining generators of the punctured sphere's fundamental group are boundary loops, controlled by the red-word constraints. Thus every one-point curve labeling lifts to exactly `m` region labelings. This justification does not require the action to be free or faithful.

In the one-point case the red crossing word lies in the direct product of the two groups. Its two components impose independent red-green and red-blue Heegaard relations. Each pair presents a free group of rank `k`. Consequently the curve count is `|C|^k |B|^k=N^k`, even when the groups are nonabelian. This counts assignments or based homomorphisms, without a conjugacy quotient.

Combining the count with Proposition 6.13 gives `av(T)=m N^(g+k)`. For a fixed simple boundary label in the punctured stabilizer there are `N` admissible assignments and three red factors `N`, so `C_st=N^4`, independently of `m`. Keeping the source normalization `xi^3=N^4` and defining `a=xi/N` gives `a^3=N` and

    I_a(X) = m N^k a^(-g) = m a^(2-chi(X)).

This is an exact normalization statement for every permitted root. It is not merely proportionality to a one-point invariant. In particular, `I_a(S^4)=m` and `I_a(Y x S^1)=m a^2` for every connected closed oriented three-manifold `Y`.

## Approach 2 necessity and sufficiency

The trace axiom requires `n=m a^2` to be a nonnegative integer. It cannot be zero, since `m>0` and `a!=0`. Therefore `a^2` is positive real. Together with `a^3=N>0`, this forces `a` to be the positive real root. Moreover `a=N/(a^2)` is rational. A rational cube root of an integer is an integer by reducing its numerator and denominator. Hence `N=r^3` and `a=r` for a positive integer `r`. The factor `m` cannot repair a noncubic `N`; dividing the integer `n` by the nonzero integer `m` still makes `a^2` rational.

Conversely, for such `r`, choose `n=m r^2` colors and `q=1/r`. The stated state space has dimension `n^b0(Y)` and includes the one-dimensional empty-object space. The map for a bordism is a finite sum over locally constant choices of a color on each connected component, weighted by `q^chi(W)`.

The gluing proof handles more than connected bordisms. Two component-colorings that agree on every seam component determine a unique coloring of the glued manifold; conversely, every coloring of the glued manifold restricts to exactly such a pair and determines its seam labels uniquely. If gluing creates a new closed component, the summation over seam colors accounts for its free choice precisely once. Previously closed components remain independent free choices. There is no missing division by `n` and no excess factor for cycles in the graph of glued components.

Euler characteristic adds under this gluing because the seam is a closed oriented odd-dimensional manifold. Cylinders enforce equality of the incoming and outgoing component labels and have Euler factor one. The disjoint-union tensorator is the canonical bijection of labeling bases, and its unit, associativity and symmetry coherences follow from restrictions of functions on finite component sets. Thus the construction is a strong symmetric monoidal functor, including births, deaths, disconnected bordisms and closed components.

A connected closed four-manifold receives `n q^chi(X)=m r^(2-chi(X))`, exactly the required value. For each connected three-manifold the state dimension is `n`, which is also forced for any extension by its product trace. This proves an **existence classification for unchanged extension within the stated subclass**. It does not classify all possible extensions up to monoidal natural equivalence, prove uniqueness, or retain all original categorical information in its boundary states.

The arbitrary-root repair `I_a/(m a^2)=a^(-chi)` is correct on connected closed manifolds, and its multiplicative extension uses a factor `(m a^2)^(-b0(X))`. Standard untwisted traces and `Phi=id` are essential limits on the subclass. Nothing here extends the classification to nontrivial cochains, nonidentity pivotal functors or general spherical fusion categories.

## Approach 3 universal construction and monoidal failure

The report's general construction is a well-defined linear functor, potentially to infinite-dimensional vector spaces. If a linear combination of fillings is in the gluing radical, composing any bordism with it remains in the radical: a test filling of the outgoing boundary can be composed back to a test of the incoming boundary. All statements here use algebraic finite linear combinations.

Disjoint union also descends to the radical quotients. To see this for a radical element on `Y` tensored with a filling of `Y'`, glue the latter to the `-Y'` part of any test filling. The result tests the radical element on `Y`, so the total pairing vanishes. The analogous argument applies to the other tensor factor.

The natural tensor map is injective because the two quotient pairings are nondegenerate and product tests separate a nonzero finite tensor. This reasoning remains valid when the quotient spaces are infinite-dimensional. It does not prove surjectivity. The empty state has dimension one because its pairing is `F(X)F(X')` and `F(empty)=1`. Once finite-dimensionality and tensor-map surjectivity are proved, the induced maps are isomorphisms and their canonical coherences give the required strong monoidal functor. Those are indeed the missing obligations for this route.

For `F(X)=n q^chi(X)` on connected closed manifolds, with nonzero `n,q`, the pairing on fillings of `S^3` has rank exactly one. Every filling has one boundary-bearing component; additional closed components contribute scalar factors. After gluing, the two boundary-bearing components become one closed component. Hence the pairing factors, and the four-ball self-pairing `n q^2` is nonzero.

For `S^3 disjoint-union (-S^3)`, the disconnected two-ball filling and the connected cylinder filling have the stated Gram matrix:

    [[n^2 q^4, n q^2], [n q^2, n]].

The three doubles are, respectively, two four-spheres, one four-sphere and `S^3 x S^1`, with compatible orientations. Its determinant is `n^2(n-1)q^4`. Therefore for `n!=1` the two-boundary state dimension is at least two, while the tensor product of the individual universal states has dimension one. This is a genuine failure of strong monoidality.

The cube-order example `N=8,m=1` has `n=4,q=1/2` and Gram matrix `[[1,1],[1,4]]`. Approach 2 provides an ordinary TQFT nevertheless. The vacuum-generated state space on a connected boundary sees only a symmetric sum of colors, whereas a connected two-boundary filling can correlate the colors. There is no contradiction. The report correctly limits this failure to the canonical universal construction, rather than turning it into a nonextension theorem for all possible state-space constructions.

## Approach 4 regular dihedral data

Use the order-eight dihedral group, not the order-sixteen convention sometimes attached to similar notation. The regular `Vec_G` module with one simple object per group element is indecomposable, and the ordinary trace gives dimension one in each grade. The bimodule right action of `Vec` is standard. The regular action is a permissible transitive-set input, so stabilization is nonzero by the already checked source formula.

Every module endofunctor is right tensoring by its value on the tensor unit. Composition reverses this tensor order, yielding `End_(Vec_G)(Vec_G)` equivalent to `Vec_(G^op)`. Taking `A` equal to this category and `Phi=id` meets the pivotal hypothesis. For this example `N=m=8`; the positive-root choice has `a=2` and the explicit unchanged-value extension has 32 colors.

A central lift of the identity would give every object a half-braiding. A monoidal natural isomorphism of its underlying functor to the identity is sufficient to transport the half-braidings to the original objects. Thus allowing an isomorphic underlying functor does not evade the argument.

For noncommuting `g,h`, the required crossing would be an isomorphism between simples of grades `gh` and `hg` (with the order convention reversed for `G^op`). These simples have zero morphism space between them. In the presentation `r^4=s^2=1` and `srs=r^(-1)`, the grades `rs` and `sr` differ. This proves the claimed impossibility without a classification theorem for fusion 2-categories.

The example is a counterexample to inferring a central lift from the MMT hypotheses or from pivotality. It is not a no-go theorem for ordinary TQFT extension, as its 32-color extension emphasizes. Nor does it rule out another higher-categorical realization using different structure.

## Approach 5 correction and connected mapping tori

In the corrected statement, `Y` is connected. Therefore every mapping torus of `f^j` is connected, and a normalization factor applied on connected closed four-manifolds multiplies every entry `t_j` by the same nonzero scalar `lambda`.

If the mapping class of `f` has order dividing `h`, functoriality of mapping cylinders gives `A^h=identity`. The polynomial `x^h-1` is separable over the complex numbers, so `A` is diagonalizable with eigenvalues among the `h`th roots of unity. Fourier inversion recovers their multiplicities as `lambda b_l`. Each must be a nonnegative integer. No unitarity is required.

For a finite list, the common-scalar criterion is exactly the positive-rational-ray condition in the report: the ratio of any two nonzero coefficients must be a positive rational. Conversely, scaling by the reciprocal of one coefficient and a positive common denominator produces integer multiplicities. If all coefficients vanish, the zero-dimensional representation realizes the zero trace list. This local sufficiency does not construct a TQFT or guarantee that the same scalar meets constraints from every other three-manifold. The report states that limitation.

The modulus inequality follows from the sum of `dim Z(Y)` roots of unity; multiplication by nonzero `lambda` cancels from its two sides. Mapping tori have Euler characteristic zero, so a pure Euler factor cannot change the values. The synthetic involution list `(1,3)` is a valid illustration of incompatible multiplicities, and is explicitly not represented as a source evaluation.

For connected `Y` in the graded subclass all mapping-torus values equal `m a^2`; only the trivial Fourier coefficient is nonzero. Thus this criterion supplies no new obstruction after scalar normalization in that subclass. The missing calculation for general MMT data is accurately identified: a source-admissible non-Euler example with explicit mapping-torus evaluations violating the condition. That calculation has not been supplied.

### Why connectedness is a mathematical requirement

Take `Y` to be two copies of `S^3` and let `f` swap them. Its identity mapping torus has two connected components, while the swap mapping torus has one. For the accepted `C_2` family set `n=a^2`, so `n^3=4`, with the positive root. The unnormalized pair of values is `(n^2,n)`.

The valid componentwise normalization `lambda=1/n` changes these to `(lambda^2 n^2,lambda n)=(1,1)`, as required by the explicit Euler TQFT. Treating this as a uniform common factor instead would produce Fourier coefficients `(n^2+n)/2` and `(n^2-n)/2`. Their ratio `(n+1)/(n-1)` is irrational: a rational ratio would solve for a rational `n`, impossible when `n^3=4`. The original unqualified test would consequently reject every uniform normalization even though the correct componentwise normalization gives a TQFT.

This explicit counterexample is why the added connectedness hypothesis is necessary, rather than an editorial preference. The source-free correction diff and pinned report record the repair transparently.

## Independent finite checks and limits

The accompanying `check_followup.py` independently tests the component-color maps by composing finite boundary-component partitions and comparing exact matrix multiplication to direct gluing. It includes empty boundaries, existing closed components, newly formed closed components, conflicting labels and cylinders. Calculations use integer and rational arithmetic.

Further checks verify the Gram determinant at nonzero rational parameters, the full order-eight dihedral multiplication associativity table and noncommuting grades, and fourth-order Fourier inversion with exact Gaussian rational coefficients. A disconnected-boundary normalization regression distinguishes the correct componentwise exponent from the erroneous common scalar. These are supplementary checks; general functoriality, source admissibility and the irrationality argument are proved above.

## Final scope and accounting

The corrected report supports five mechanisms: product trace integrality, direct component-color construction, universal-construction gluing ranks, central half-braidings, and cyclic mapping-class traces. The new four approaches contain genuine mathematical work and clear outcomes or remaining gaps. Source searches, figure inspection, computational tests and audits add zero to that count.

The strongest new positive result is the exact **extendability classification for the standard untwisted transitive-set subclass with identity pivotal functor**. The strongest new cautions are that a canonical universal construction can fail even when another extension exists, and that pivotality does not imply the proposed central lift. These results justify partial-answer status, not completion of the entire workshop problem.

The MMT general constructor, finite-set evaluation and transitive-set reduction remain external mathematical dependencies, explicitly credited. The audit certifies neither novelty nor current priority. No source bodies, private datasets or private coordination material form part of this authored audit or its checks.

## Public sources

- Meusburger, Mulevicius and Torzewska, *Categorical 4-manifold invariants from trisection diagrams*, arXiv:2511.19384v1, especially pages 32, 53--59 and Corollary 6.16 on pages 61--62. https://arxiv.org/abs/2511.19384v1
- Meusburger's workshop contribution, *Trisection invariants of four-manifolds*, Oberwolfach Report 12/2026, printed pages 767--768. https://doi.org/10.4171/OWR/2026/12
- Gay and Kirby, *Trisecting 4-manifolds*, Geometry & Topology 20 (2016), 3097--3132. https://msp.org/gt/2016/20-6/gt-v20-n6-p02-s.pdf
