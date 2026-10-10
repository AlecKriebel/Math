# Boundary constructions and remaining obstructions

Problem 30006636 / OWR-14299913-005. Authored follow-up, 8 October 2026.

## Status

**Partial answer to the original normalization-unspecified question.** Five substantive mathematical approaches are recorded below. The first gives an exact nonextension example for unchanged numerical values. The second completely classifies ordinary complex TQFT extension for the untwisted finite-group/transitive-set subclass of MMT Section 6.2 and constructs the boundary functor when possible. The remaining approaches expose a canonical universal-construction failure, refute an unjustified central-lift shortcut, and give scale-independent mapping-torus tests. No general extension, general impossibility theorem, or fusion-2-category realization is claimed.

The original accepted first proof is `PROOF.md`; its mathematical content is retained. Its “one approach” accounting describes that first stage only. This follow-up adds four distinct mechanisms. The public problem source and precise conventions are those in that proof. All TQFTs below are strong symmetric monoidal functors from oriented smooth 4-bordisms to finite-dimensional complex vector spaces; disconnected bordisms and the empty object are included.

## Approach 1: product trace and fixed normalization

See PROOF.md, Theorem 3. With `B=Vec`, `C=Vec_(C2)`, `M=Vec`, `A=End(M)`, and identity pivotal functor, direct averaging gives 4 on the standard `(1,1)` diagram of `S1 x S3` and 16 on the balanced stabilizer of S4. Thus the normalized product value x satisfies `x^3=4`, for every allowed cube-root choice. It cannot equal the nonnegative integer `dim Z(S3)`.

**Mechanism:** categorical trace on a product manifold. **Outcome:** rigorous unchanged-value counterexample. **Limit:** rescaling connected closed values removes this example; arbitrary normalization remains in scope for the workshop question.

## Approach 2: classify the graded subclass by an explicit boundary-color theory

This is a construction and classification, not another numerical test of the C2 example.

Let B and C be finite groups, M a finite nonempty transitive `(C x B^op)`-set, and use the untwisted data of MMT Section 6.2 with its standard traces and `Phi=id`. Write

    N=|B||C|,   m=|M|,   a=xi/N,   a^3=N.

**Theorem A.** On connected closed oriented four-manifolds the source invariant is

    I_a(X)=m a^(2-chi(X)).                                    (A1)

It extends, with these unchanged connected closed values, to an ordinary complex oriented four-dimensional TQFT **if and only if** N is a perfect cube and a is its positive real cube root. When this holds, write `N=r^3`; an extension has `m r^2` states on each connected closed 3-manifold. Regardless of N or root choice, the rescaling `I_a/(m a^2)` is the Euler TQFT in PROOF.md.

**Proof of (A1).** MMT Corollary 6.16 (PDF pp. 61--62) reduces the transitive-set label count to m times its one-point-set count. For completeness, the factor records a choice of one region label; the commuting B and C actions propagate it, and the red-word relations ensure consistency. For the one-point set the red relation lies in `C x B^op`, so its two component relations are independent. The red-green Heegaard diagram presents a free group of rank k, as does the red-blue diagram. Therefore the numbers of green and blue assignments are respectively `|C|^k` and `|B|^k`. The total count is `m N^k`. Corollary 6.14 then gives `m N^k a^(-g)=m a^(2-chi(X))`. This reduction retains the full standard-trace normalization, not just proportionality.

**Necessity.** The product trace identity requires `n=m a^2` to be a nonnegative integer. It is nonzero. Since `a^3=N>0` and `a^2=n/m>0`, a must be positive real. Moreover `a=N/(n/m)` is rational. A rational number whose cube is a positive integer is an integer: writing a in lowest terms forces its denominator to divide its numerator cubed. Thus `a=r` is a positive integer and `N=r^3`.

**Construction proving sufficiency.** Put `n=m r^2` and `q=r^(-1)`. For a closed oriented 3-manifold Y let

    V(Y)=C[Maps(pi_0(Y), {1,...,n})].

A basis vector is a labeling of every connected component of Y by one of n colors. For the empty manifold there is one labeling, so `V(empty)=C`. Disjoint union of labels gives the tensor and unit isomorphisms.

For a bordism W, define the matrix coefficient between an input boundary labeling u and an output labeling v to be

    q^chi(W) times the number of component-colorings of W
    whose restrictions to the incoming and outgoing boundaries are u and v.  (A2)

A component of W meeting the boundary must carry the common color of all of its boundary components; conflicting boundary colors contribute zero. A closed component has n freely chosen colors. Formula (A2) is finite and specifies the entire linear map, including births, deaths, connected and disconnected bordisms and closed components.

A cylinder's components connect matching boundary components, so its matrix is the identity. For gluing `W:Y0->Y1` and `W':Y1->Y2`, compatible component-colorings on the two pieces with matching Y1 labels are in bijection with component-colorings of the glued bordism. Matrix multiplication sums exactly over those Y1 labels. Also `chi(W'W)=chi(W')+chi(W)` because every closed 3-manifold Y1 has Euler characteristic zero. The scalar factors multiply correctly. Disjoint union independently combines colorings and adds Euler characteristics, proving strong symmetric monoidality and its coherences. Diffeomorphisms simply transport component labels. A connected closed X has n colorings, so its scalar is

    n q^chi(X)=m r^(2-chi(X))=I_a(X).

This proves sufficiency. QED.

**Outcome and limits.** This explicitly solves extension for the entire untwisted transitive-set subclass, including nonabelian B and C and nontrivial M. It does not address nontrivial cocycles, a nonidentity pivotal functor, or general spherical fusion categories. The constructed functor need not retain the original categorical data as boundary labels, and no fusion-2-category realization is asserted. The construction is ordinary, possibly decomposable TQFT; the workshop did not impose an indecomposable target theory.

## Approach 3: the canonical universal construction and a two-boundary rank defect

One standard route from closed invariants is to span state spaces by fillings and divide by the gluing radical. We analyze it rather than assume that finite-dimensional source categories make it monoidal.

Given a multiplicative complex invariant F of closed 4-manifolds with `F(empty)=1`, let U(Y) be the free complex vector space on compact oriented fillings of Y. Pair it bilinearly with U(-Y) by gluing and applying F. Quotient by the left/right radicals. Gluing a bordism to a filling preserves the radical, because any test on the new boundary composes with that bordism to give a test on the old boundary. Thus this procedure always gives a linear functor on bordisms. The natural map

    Ubar(Y) tensor Ubar(Y') -> Ubar(Y disjoint-union Y')        (A3)

comes from disjoint union. Nondegeneracy of the quotient pairings and multiplicativity of F make (A3) injective: a finite nonzero tensor can be separated by product tests. Surjectivity is an additional requirement, not a consequence of that argument. If all quotient spaces are finite-dimensional and (A3) is surjective for every pair, the construction is a strong monoidal TQFT whose closed values equal F. Finiteness and surjectivity are the exact outstanding general obligations for this route.

There is already an explicit failure for a family that Approach 2 can extend by a different construction.

**Proposition B.** Suppose

    F(X)=n q^chi(X)  for connected closed X,

multiplicatively extended, with `n,q in C^x`. The universal space on S3 has dimension 1. If `n != 1`, the universal space on `S3 disjoint-union (-S3)` has dimension at least 2. Hence the canonical universal construction is not strong monoidal, even when n is a positive integer and the colored construction of Approach 2 is a valid TQFT.

**Proof.** Every filling of S3 consists of one component meeting its boundary and some closed components. In the S3 pairing the unique two boundary-bearing components glue to one closed component, so the pairing factors as n times a function of each filling separately. The other closed components supply scalar factors. The rank is exactly 1 since the two four-balls pair to `n q^2 != 0`.

For the two-sphere boundary take D to be two oriented four-balls, and C to be the cylinder `S3 x I`, considered as a filling of `S3 disjoint-union (-S3)`. Gluing yields respectively two copies of S4, a single S4, and `S3 x S1`. Their pairing matrix is

    [ n^2 q^4    n q^2 ]
    [ n q^2      n     ].

Its determinant is `n^2(n-1)q^4`, nonzero for n!=1. Thus the target of (A3) has dimension at least 2 while the source has dimension 1. QED.

For the source's C2 example, n=a^2 and q=a^(-1), so the matrix simplifies to `[[1,1],[1,n]]`. For a cube-order example, `N=8,m=1`, it is `[[1,1],[1,4]]`: the unchanged invariant genuinely has a TQFT extension by Approach 2, but this vacuum-generated construction still fails. Therefore declaring a universal construction “the extension” without checking (A3) would be erroneous.

**Mechanism:** boundary gluing ranks and monoidal generation. **Outcome:** explicit obstruction to a natural construction; exact general finite-rank and tensor-surjectivity gaps identified. **Not claimed:** a rank defect here obstructs every possible TQFT extension.

## Approach 4: testing a central-lift shortcut for the categorical data

A tempting route toward a higher-categorical description is to promote the pivotal functor `Phi:A->E`, with `E=End_(C,B)(M)`, to a central tensor functor `A->Z(E)`. The source hypotheses do not imply such a lift. This is a concrete algebraic test of a proposed realization, not an appeal to the title “fusion 2-category.”

Take the nonabelian dihedral group G of order 8. Let `C=Vec_G`, `B=Vec`, and let `M=Vec_G` be the regular left module, with ordinary trace in each grade. This is the regular transitive-set instance of Approach 2. Right tensor multiplication gives

    E=End_(Vec_G)(Vec_G) equivalent to Vec_(G^op).

Let `A=E` and `Phi=id`. All source hypotheses hold, including stabilization. Here `N=m=8` and the positive root is a=2, so Approach 2 even constructs an **unchanged** extension with n=32 colors.

**Proposition C.** The identity tensor functor of E has no central lift whose composition with the forgetful functor `Z(E)->E` is tensor-isomorphic to the identity.

**Proof.** Such a lift would assign to every object x of E a half-braiding with every object y, naturally and coherently in x. For simples `delta_g` and `delta_h` in a group-graded category this requires an isomorphism

    delta_(gh) -> delta_(hg),

with the multiplication order reversed if one uses `G^op`. Distinct simple grades have zero Hom space. In the dihedral group take r of order 4 and s a reflection; `rs != sr`. The required isomorphism is therefore impossible. Equivalently, a central lift of the identity would make E braided, but this elementary calculation rules that out. QED.

**Mechanism:** an explicit obstruction to a central half-braiding, using the noncommuting simple objects. **Outcome:** the central-lift route fails for admissible data even when an ordinary unchanged-value TQFT exists. A correct fusion-2-category construction must use more general structure, impose additional hypotheses, or discard information; it cannot silently infer this lift from pivotality. **Gap:** failure of this specific lift does not rule out other higher-categorical encodings or prove that all admissible data fit a known fusion-2-category state sum.

## Approach 5: finite-order mapping tori give normalization-independent tests

The product-trace obstruction is sensitive to a connected-component scalar. A distinct route compares several mapping-torus traces, where that scalar cancels.

Let Y be a connected closed oriented 3-manifold and f an orientation-preserving diffeomorphism whose mapping class has finite order dividing h. Connectedness ensures that every mapping torus below is connected, so a connected-component normalization multiplies all of their values by the same scalar. Write `M_(f^j)` for its oriented mapping torus and `t_j=F(M_(f^j))`, `0<=j<h`. If some constant rescaling `lambda F` extends to a TQFT, then

    lambda t_j = Tr(A^j),   A^h=1,  A=Z(f).

Over C, `x^h-1` has distinct roots. With `zeta=exp(2 pi i/h)`, let n_l be the multiplicity of eigenvalue `zeta^l` of A. Fourier inversion forces

    n_l = lambda b_l,
    b_l = (1/h) sum_(j=0)^(h-1) zeta^(-l*j) t_j.              (A4)

Every n_l must be a nonnegative integer.

**Proposition D.** If two nonzero Fourier coefficients b_l and b_s have ratio outside the positive rationals, no nonzero constant normalization lambda can turn these mapping-torus values into the traces of a finite-dimensional representation of the cyclic group. Hence no such normalization can give a TQFT. Conversely, for this finite list of numbers alone, a suitable lambda exists exactly when all nonzero b_l lie on one positive rational ray (or all are zero).

**Proof.** Necessity follows from `b_l/b_s=n_l/n_s`. For sufficiency choose one nonzero coefficient b_s, write all ratios in positive rational form and multiply by a common positive integer clearing their denominators. That integer divided by b_s is the required lambda. If all coefficients vanish, use the zero representation. QED.

A simpler necessary, scale-independent inequality is

    |t_j| <= |t_0|,

because the eigenvalues of A are roots of unity; no unitarity assumption is needed. Pure Euler rescaling also has no effect because every mapping torus has Euler characteristic zero.

For h=2, `b_+=(t_0+t_1)/2` and `b_-=(t_0-t_1)/2`. For example, hypothetical values `(1,3)` would give coefficients `(2,-1)` and prohibit every scalar normalization. These are a synthetic check of the criterion, **not claimed MMT values**.

For every graded input of Approach 2 all mapping-torus values are the same nonzero constant `m a^2`. Its Fourier transform has only `b_0=m a^2`, so a scalar normalization passes this test. Thus this approach cannot improve the obstruction in that subclass. For general MMT data, no explicit finite-order mapping-torus evaluation violating (A4) was obtained here. That is the exact gap: one needs source-admissible non-Euler data and concrete mapping-torus diagrams/evaluations, rather than more formal trace algebra. Even a pass for all currently computed traces would not construct the remaining bordism maps.

## Combined conclusion and accountability

The original source's full scope is still open in this packet. What is established is:

1. A completely explicit unchanged-normalization nonextension example.
2. A closed formula and exact ordinary-TQFT extension classification for all standard untwisted finite-group/transitive-set data with identity pivotal functor.
3. A concrete monoidal-surjectivity defect for the canonical universal construction.
4. A central-lift counterexample showing why pivotal data cannot simply be treated as central data.
5. A normalization-independent mapping-torus obstruction criterion, with its remaining computational gap honestly isolated.

These are five distinct mathematical mechanisms: trace integrality; direct component-color bordism construction; gluing-radical ranks; central half-braidings; and cyclic mapping-class representations. Literature searches, source inspection, test runs and audits count as zero approaches. The first proof's counterexample remains valid, while the new constructions make its normalization limitation sharper rather than hiding it.

External mathematical dependencies are the MMT constructor and finite-set evaluation (Theorem 4.28, Definitions 6.12, Propositions 6.13, Corollaries 6.14 and 6.16), the standard trisection topology in Gay--Kirby, and elementary Heegaard presentation theory. The boundary-color functor, universal-rank calculation, noncentrality argument and Fourier obstruction are fully proved above. None depends on a claimed general TQFT extension.

Source URLs: https://arxiv.org/abs/2511.19384v1 ; https://publications.mfo.de/handle/mfo/4446 ; https://msp.org/gt/2016/20-6/gt-v20-n6-p02-s.pdf . Exact retrieval hashes and inspection locators are in SOURCES.json. Source PDFs, full extracted text, data corpora and private coordination files are excluded from the candidate.
