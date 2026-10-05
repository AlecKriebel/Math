# Independent adversarial audit: 30004491

## Verdict

**PASS, scoped to the frozen unsolved investigation.** The original unrestricted conjecture remains **UNSOLVED, 5/5 approaches**. This is neither a solution certificate nor an independent proof of the imported literature. No mandatory correction to the frozen mathematics, target interpretation, or reported verification results was found.

The assessed author archive has 20,834 bytes and SHA-256 `4f5e1bddcfb9720f76f50cdff5118409d3c764dd24e0701677d01bb54ed98a5b`. Its ten files match the author directory exactly. The assessed proof has SHA-256 `c90303d06ae5b773b79e280a471db197e4f1f56a323df23afea00749eb67ee28`. Neither the directory nor its archive was modified.

The principal positive conclusion is valid: the specified singular foliation on a smooth projective rational surface has infinite transverse birational action, becomes defined by a closed rational form on a degree-two cover, has no closed rational defining form on the base or any birational model of it, and has no rational first integral after any generically finite cover. These statements are mutually compatible. They refute only the stronger conclusions identified by the author.

## 1. Target and literature gate

The target is OWR Conjecture 4, printed p.1294, and published LBPRT Conjecture D, printed p.46. The audit independently retrieved both complete PDFs and visually inspected these pages. Singular holomorphic complex-codimension-one foliations, projective ambient manifolds, dominant rational self-maps, and generic leaf-fixing are the relevant categories. Invertibility, regularity, and a pre-existing transverse projective structure cannot be silently assumed. Definition 3.1 allows generically finite dominant meromorphic covers. On projective models this gives the stated rational-form formulation. [OWR report](https://ems.press/content/serial-article-files/46857), [published article](https://frederictouzet.perso.math.cnrs.fr/ARTICLES/end.pdf).

The published article was checked at pp.44-53 and the Section 4 reductions. Theorem A has an additional transverse-projective hypothesis. Proposition E assumes the actual Picard group is Z and a regular endomorphism of degree at least two. Theorem F concerns birational symmetries with singularity and bigness assumptions. The low-orbit-dimensional results do not manufacture an invariant surface in arbitrary dimension. The package preserves these limitations. The source's semigroup quotient is a leaf-equivalence congruence; treating every dominant rational self-map as an automorphism would be incorrect, but the package does not do this. [Published article](https://frederictouzet.perso.math.cnrs.fr/ARTICLES/end.pdf).

Fazoli's 2025 Theorem C(A) still requires projective space of dimension at least three, absence of global foliated one-forms, and instability of the specified first transverse-jet sheaf. Proposition 5.3 gives an affine structure and Remark 5.4 supplies the virtually additive strengthening under those hypotheses. Neither the source nor this investigation deduces the hypotheses from arbitrary infinite transverse dynamics. [Primary paper](https://arxiv.org/pdf/2509.13510v1).

Claudon-Touzet's revised Theorem E assumes a regular holomorphic foliation on a compact Kähler manifold with a transverse Kähler metric of quasi-negative Ricci curvature. Its conclusion concerns automorphisms. The paper's Section 8 explicitly leaves a bimeromorphic enlargement as a proposed extension. This is not a theorem for arbitrary singular foliations with dominant rational dynamics. [Primary paper](https://frederictouzet.perso.math.cnrs.fr/ARTICLES/KF.pdf).

Fresh targeted searches and current author publication lists found no verified resolution of the general target. This is a bounded negative search, not a proof that no such resolution exists. The arXiv revision records, six PDF byte pins, publication-list link to the published PDF, and repository dataset pins were independently checked. The full imported proofs and all their foundations were not re-proved.

## 2. Global rational forms and the infinitesimal argument

The rational calculations define genuine singular projective foliations. On a smooth projective variety, a rational differential can be multiplied locally by equations for its pole divisor and interpreted as a twisted holomorphic differential. Removing divisorial common factors and taking the saturated kernel gives a coherent tangent sheaf. Integrability holds generically and therefore identically. This construction does not assert that the foliation is nonsingular along the boundary.

Conversely, the generic conormal line of a codimension-one algebraic foliation has a nonzero generator over the function field. Projectivity identifies the relevant meromorphic sections and algebraic rational sections. Thus the manuscript does not confuse a globally defined rational one-form with a globally holomorphic one-form. In particular, P1 x P1 need not possess a nonzero holomorphic one-form for the example to work.

For the infinitesimal assertion, set a=omega(v) and beta=omega/a. The Lie derivative of beta is proportional to beta. Evaluating on v gives zero, since beta(v)=1 and [v,v]=0, so L_v beta=0. Cartan's identity then gives i_v(d beta)=0. Contracting beta wedge d beta=0 gives

`d beta - beta wedge i_v(d beta) = 0`.

Consequently d beta=0. The contraction signs are correct, poles cause no problem in the function field, and completeness of the rational vector field is not required. A transverse connected algebraic-group orbit supplies such a vector field. An arbitrary infinite cyclic birational group does not automatically do so. The leafwise product-translation control correctly separates ambient infinitude from transverse infinitude.

## 3. Constant fields: universal, not bounded

Write t=(sqrt(5)-1)/2, K=C(x,y), and D=t x d/dx-y d/dy. The exact symbolic checks of finitely many weights are not needed for the following universal argument.

Let R=P/Q in K be D-constant, with P,Q Laurent polynomials and Q nonzero. Choose a point (x0,y0) in the torus where Q does not vanish. On a small disk in z, the curve (x0 exp(tz),y0 exp(-z)) is an integral curve of D, and R has a constant value c. Therefore

`(P-cQ)(x0 exp(tz),y0 exp(-z)) = 0`.

Distinct Laurent monomials give distinct exponents tm-n. Indeed equality would imply t(m-m')=n-n', and irrationality of t forces equality of both integer coordinates. A finite sum of exponentials with distinct exponents is identically zero only when all coefficients vanish: its derivatives of orders 0 through N-1 at zero give an invertible Vandermonde system. Since x0 and y0 are nonzero, every Laurent coefficient of P-cQ vanishes. Thus R=c and Const(K,D)=C.

For any finite extension L/K, characteristic zero gives a unique extension of D. If Dh=0, differentiate the monic minimal polynomial of h over K. Its differentiated relation has degree smaller than the minimal polynomial, so every coefficient derivative is zero. The original polynomial therefore has coefficients in C. Algebraic closedness of C forces h in C. This proves the constant assertion for every finite algebraic extension, with no degree bound, Galois requirement, or unramified hypothesis.

A generically finite dominant map induces a finite extension of function fields. In a one-dimensional foliation, a rational first integral is exactly a rational function killed by its nonzero tangent derivation. The lemma therefore excludes nonconstant rational first integrals on all such covers of Y, not merely those used in the example.

## 4. Irrational leaves and all iterates

On the universal cover C2 of the torus, use x=exp(u), y=exp(v) and ell=u+t v. Every lifted leaf is an affine complex line ell=c. Its image is a full torus leaf: local integral curves lift to these lines, and any continuation still lies on a lift of the same level. Deck transformations change ell by the countable group Lambda=2 pi i(Z+t Z). Therefore two torus points are on the same leaf precisely when their lifted labels differ by Lambda. Density of Lambda along the imaginary direction does not make different labels leaf-equivalent; its countability remains decisive.

The monomial map g has exponent matrix M=[[2,1],[1,1]], inverse (x/y,y^2/x), and g*beta=lambda beta for beta=dx/x+t dy/y and lambda=(3+sqrt(5))/2>1. Consequently g^k multiplies ell by lambda^k for every positive integer k. A positive iterate fixing general leaves would force (lambda^k-1)ell in Lambda on a transverse open disk. Since lambda^k-1 is nonzero, the possible labels form a countable set, which cannot contain that disk. This is an all-k proof, not an inference from the forty powers tested by the author.

The coordinate boundary of the torus is invariant for the saturated foliation. At smooth boundary points a leaf meeting an invariant divisor is locally contained in it; uniqueness of leaves prevents a torus leaf from crossing into the boundary. Singular boundary points are not part of regular leaves. Compactification therefore does not add equivalences between torus leaves.

## 5. Double cover, quotient, and birationality

The involution sigma:(x,y)->(1/x,1/y) commutes with g and satisfies sigma*beta=-beta. In coordinates a=(x+1)/(x-1), b=(y+1)/(y-1), it is simultaneous sign change. Let s=a^2 and r=b/a. Then K=C(a,r), C(s,r) is the fixed field, and [K:C(s,r)]=2. For example, s is not a square in C(s,r), as its valuation along s=0 is odd. The involution is the nontrivial field automorphism. This verifies degree two rather than merely degree at most two.

The invariant differential a beta descends to

`alpha = (1/(1-s)+t r/(1-s r^2)) ds + 2t s/(1-s r^2) dr`.

The independent computation verifies both pi*alpha=a beta and

`d alpha = t/(1-s r^2) ds wedge dr = (ds/(2s)) wedge alpha`.

Over a^2=s, alpha/a is closed. The cover can ramify; there is no claim of an étale trivialization. The model X=P1_s x P1_r is smooth and projective. The map pi is a generically finite dominant rational map from the smooth projective Y, as required.

Because g and g^{-1} both commute with sigma, they induce inverse automorphisms of the invariant function field, so the descended map f is birational. Independently deriving the quotient formulas from g and deriving its inverse from g^{-1} reproduces the author's S,R formulas. Both compositions with the independently derived inverse are the identity. Pullback of alpha has the asserted rational multiplier. No dominance or birationality conclusion is inferred from numerical sampling.

### Leaf equivalence after the quotient

Let Q=Y/<sigma>. On the torus away from the four fixed points, Y->Q is a genuine unramified two-sheeted covering and the foliation downstairs pulls back to the upstairs foliation. If two downstairs points are joined by a regular leaf path in this open set, lifting that path starting at a chosen preimage ends at one of exactly two preimages of its endpoint. The lift stays in a single upstairs leaf. Conversely an upstairs leaf path projects to a downstairs one. Hence the equivalence on labels is precisely ell modulo Lambda and sign.

The omitted fixed points concern only finitely many upstairs leaves; these are exceptional leaves for this test. Boundary divisors are invariant. A general leaf path therefore cannot acquire an extra identification through either the boundary or a singular quotient point. In particular, going around a fixed point contributes only the already recorded deck sign, not an arbitrary new transverse identification.

One need not assert that these exceptional nonalgebraic leaves are contained in a proper algebraic closed subset. Each has a countable set of labels on a local transversal, obtained by translating one label by Lambda. Excluding the finitely many such leaves removes at most countably many labels. This suffices for the contradiction on any transverse open disk, even if an exceptional leaf is Zariski dense.

The rational surface X is birational to Q. Here is the detail behind the manuscript's birational invariance assertion. Resolve both models to a common smooth surface and factor the resulting birational morphisms into point blowups. Outside exceptional curves and finitely many centers these are isomorphisms. For a regular leaf not contained in an exceptional curve, its intersection with a removed algebraic curve is a closed discrete analytic subset of its intrinsic Riemann surface. Removing such points leaves that Riemann surface connected: paths can be perturbed locally around the isolated points. A contracted invariant curve is an exceptional leaf, and singular centers cannot be used as joining points of regular leaves. A regular center lies on a unique regular leaf, which remains the same leaf after puncturing. Thus these modifications neither join two distinct general leaves nor split one into distinct equivalence classes on the common open locus. The assertion is only about generic leaf equivalence; exceptional leaf spaces need not be isomorphic.

It follows that f^k fixing general leaves on X would force, on a local transverse disk upstairs,

`(lambda^k-1)ell in Lambda` or `(lambda^k+1)ell in Lambda`.

Each of the two sets is countable because lambda>1. Their union cannot contain the disk. Taking a countable union over k also leaves possible transverse labels outside all these sets. Thus the infinite transverse action is established with the source's exact meaning, including the quotient and the projective birational model.

## 6. Descent obstruction and arbitrary further covers

Suppose a nonzero closed rational theta on X defines the descended foliation. Since pi is generically finite and separable, pullback of a nonzero differential is nonzero, and pi*theta=h beta for h in K*. The equality of kernels gives this proportionality in the one-dimensional conormal line. Closedness gives dh wedge beta=0, or equivalently

`t x (dh/dx) - y (dh/dy) = 0`.

The constant-field result forces h=c in C*. But pi*theta is sigma-invariant and c beta is sigma-anti-invariant, a contradiction. Vanishing of the trace by itself would not suffice; uniqueness of closed defining forms up to constants is the essential extra argument, correctly supplied here. Existence of such a form depends only on the rational conormal line and exterior differentiation, so the obstruction survives every birational model.

Now suppose E/C(X) is a finite extension giving a rational first integral h. Embed E and K in an algebraic closure of C(X) and take their compositum L. It is finite over K. There is a minor bookkeeping point worth making explicit: D itself changes sign under sigma and need not preserve C(X); the scalar multiple aD is invariant and does preserve C(X). In (a,b) coordinates,

`D = t(1-a^2)/2 d/da - (1-b^2)/2 d/db`.

Under simultaneous sign change both a and D change sign. Thus delta=aD is a nonzero rational tangent derivation downstairs. Its unique extension to L agrees with a times the unique extension of D. Since h is a first integral of the pulled-back foliation, delta(h)=0, so D(h)=0. The finite-extension constants lemma applied over K then gives h in C. This justifies the author's compositum argument even though D alone is anti-invariant. No correction to its conclusion is needed.

This separates three assertions sharply: a closed rational form exists after a cover; none exists downstairs; and even after further finite covers no rational first integral exists. Closed logarithmic differentials need not have algebraic primitives or rational first integrals.

## 7. Covariance, slicing, and the five attempts

For omega(v)=1, integrability gives d omega=eta wedge omega with eta=-i_v(d omega). Pullback and differentiation of f*omega=A omega give

`(f*eta-eta-dA/A) wedge omega = 0`.

Applying d to d omega gives d eta wedge omega=0. The signs and the rational gauge ambiguity are correct. This does not imply d eta=0: eta=y dx and omega=dx already give a counterexample in dimension three. If eta is closed, then eta_f=f*eta-dA/A is closed and has the same connection equation. A nonzero difference eta_f-eta is a closed defining form; a zero difference yields nothing. The equation for an algebraic integrating factor, (dh/h+eta) wedge omega=0, is necessary and sufficient after a finite extension, but no such h is obtained from the arbitrary dynamics here.

The slicing control is also correct. For q(x,y,z)=(x^2,y^3,z^5), the orbit of (2,3,5) is Zariski dense: order the finitely many terms of a hypothetical vanishing polynomial lexicographically by the powers of z,y,x. Dividing by the largest term leaves ratios whose leading exponential logarithms have strictly negative dominant term, hence all tend to zero. Its nonzero leading coefficient cannot vanish. The surface x+y+z=1 is not preserved, as the image of (1/3,1/3,1/3) has sum 37/243. This example does not present itself as a counterexample to the conjecture.

The five approaches are distinct, and each has an identified missing step or a disproved stronger intermediate claim. No argument in the package constructs the required transverse structure for a general higher-dimensional purely transcendental foliation with arbitrary dominant rational dynamics. Preserving the unsolved disposition is mandatory.

## 8. Computational, provenance, and publication checks

- Author verifier: 3,588 checks reproduced, output byte-exact, under ordinary Python and Python -O.
- Author manifest: nine listed payload files plus the manifest; both modes pass.
- Author's seven corruption classes reproduced in both modes: all 14 cases reject. These cover appended proof text, same-length modification, a missing file, an extra file, duplicate inventory entry, path traversal, and a symlink.
- Independent implementation: 34 exact algebraic controls, including a separately derived descended inverse, two-sided inverse checks, the square-root integrating factor, and the invariant tangent derivation. It uses the exact real algebraic number sqrt(5), rather than copying the author's polynomial-remainder representation.
- Independent verifier also runs under Python -O and gives byte-identical output. All its validation uses explicit exceptions.
- Six complete freshly retrieved public PDFs match the reported sizes and SHA-256 values. Two initial HTTP 502 failures were retried successfully; the retrieval record distinguishes these events.
- Both complete public dataset files match the actual pinned repository manifest. There are 15,458 problem records and 6,701 prior-report keys; exactly one target record is present and the target prior-report key is absent, rather than present with a null value.
- Fresh exact-ID repository code, PR, commit, and branch searches returned no hits. These do not cover deleted, private, or unindexed work.
- No source PDFs, rendered pages, extracted source text, dataset contents, personal material, or coordination material are included in this audit package. No remote writes were made.

The author's 3,362 finite weight-window checks mainly test an encoding of integer pairs. The forty matrix powers are finite controls. Neither family proves the universal assertions. The proofs above supply the unbounded arguments; the report and source package accurately describe the computational limits.

## Mandatory corrections and optional clarification

**Mandatory corrections: none.** Retain the unsolved status and the exact publication boundary. Do not promote this PASS to a proof of the general conjecture or a novelty claim.

Optional exposition: a future revised manuscript could spell out the invariant tangent generator aD in the compositum argument, and the closed-discrete intersection argument in birational leaf equivalence. These are valid justifications of existing steps, not repairs of a false claim. The frozen author package should remain untouched.

## Reproduction

Run `independent_verify.py` with `--author` pointing to the extracted author directory and `--archive` pointing to the unchanged author ZIP. Optional `--sources` accepts six public PDFs named 0.pdf through 5.pdf in the order of the author's source list; optional `--datasets` accepts the two complete public JSON files. Run both normally and with `python -O`. The retained `INDEPENDENT_OUTPUT.json` records the full-input run. `SOURCE_AUDIT.json` records source retrieval and inspection metadata. `AUDIT_MANIFEST.json` seals this audit's authored files and verification output.
