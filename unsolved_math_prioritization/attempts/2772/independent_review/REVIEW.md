# Independent review: restricted obstructions to three Kodaira fibrations

**Verdict: PASS as a partial, explicitly unresolved result.** The product-cover
exclusion, smooth ample-divisor obstruction, normal-and-ample corollary, and
numerical necessities are correct in their stated holomorphic/Kodaira scope.
No mandatory correction is required. The full existence question remains
**unsolved**; nonnormal or nonample product images are not excluded.

Frozen PARTIAL_RESULT.md SHA-256:
**4b91e8f2543db1d0cf6e430a1ec1bc3df38e5fae75d890d489b8ad28ad653002**.
Review date: 2026-09-30. Separate adversarial AI review by gpt-6-astra,
xhigh reasoning; not human peer review. No novelty determination is made.

## 1. Source scope and the imported theorems

I read and visually checked
[K3 Problem 2.24, p. 105](https://bpb-us-e2.wpmucdn.com/websites.umass.edu/dist/b/22144/files/2026/04/K3-problem-list-watermarked.pdf).
Its sentence asks about three or more non-isomorphic surface-bundle structures
on a complex surface. The surrounding remarks concern compact hyperbolic
bases and fibers, double Kodaira examples, and the distinction from smooth
examples without complex structures. The package does not exploit an omitted
genus convention to claim a solution.

[Catanese, Question 10](https://www.mathe8.uni-bayreuth.de/de/team/prof-fabrizio-catanese-old/pdf/156.pdf)
explicitly asks for three distinct Kodaira fibrations. In
[Llosa Isenrich–Py](https://www-fourier.univ-grenoble-alpes.fr/~py/Documents/Articles/llosa-isenrich-py-math-annalen.pdf),
the introduction defines a Kodaira fibration as a holomorphic submersion with
connected fibers which is not isotrivial; both genera exceed one. Theorem 2
requires three distinct such fibrations. This hypothesis must be retained
when using its finite-index conclusion.

Definition 1 distinguishes the fundamental-group kernels. Section 2.1,
Definitions 9–10 and the subsequent paragraph, explicitly identifies this
equivalence with equality of fibers for the submersions in question. One can
also see the relevant implication directly: if the kernels coincide, the
restriction of the second map to a fiber of the first has trivial induced
fundamental-group map. A nonconstant holomorphic map from a compact curve to
a hyperbolic curve has positive degree and cannot have that property.
Consequently it is constant on the first fiber, and the resulting map between
bases is an isomorphism.

Proposition 26 is precisely a statement that the normalization of the joint
product image is smooth. It does not assert that the image itself is normal.
The paragraph introducing that proposition establishes that the image is an
irreducible analytic surface. Lemma 13 separately states the smooth-image
descent and submersion property used in the package. All cited source
hypotheses agree with the hypothetical triple considered here.

These partial results concern holomorphic submersions and Kodaira fibrations.
They are not, by themselves, an identification of every possible smooth
surface-bundle structure on an arbitrary complex surface with such a
holomorphic map. Since the package retains an explicitly unresolved outcome,
no general existence conclusion is obtained by silently making that reduction.

## 2. Product maps and finite étale covers

Proposition 1 is valid for compact connected curves \(C,D\), without requiring
both to have hyperbolic genus.

The degree of the restricted maps \(f_c:D\to B\) is constant with \(c\).
A zero-degree holomorphic map between compact curves is constant; a nonconstant
one is surjective of positive degree. If this constant degree is positive,
differentiation in a tangent direction at a fixed \(c\) gives a global
holomorphic section of \(f_c^*TB\) over \(D\). Its degree is
\(\deg(f_c)(2-2g(B))<0\), so the section vanishes. The derivative in every
\(C\)-direction is therefore zero, and connectedness gives factorization
through \(D\). The degree-zero case factors through \(C\).

If the original map has connected fibers, a factor map of degree \(d>1\)
would have a regular fiber consisting of \(d\) disjoint copies of the other
factor. Hence its degree is one and it is an isomorphism.

For a finite étale cover \(q:C\times D\to X\), the pullback composite
\(f\circ q\) need not have connected fibers. The proof correctly does **not**
apply the preceding degree-one conclusion to that composite. It only uses
its submersion property to show the factor map is unramified and the pulled-back
fiber distribution is one of the two product distributions.

Equality of two such distributions descends through the surjective local
biholomorphism \(q\). The fibers of a connected-fiber submersion are the
connected leaves of its kernel distribution, so the two fibrations then
differ by a base isomorphism. No Galois-cover assumption is needed.
Thus there are at most two fiber foliations downstairs.

This result excludes precisely the indicated finite-étale-product route.
A ramified cover of a product is not covered by this argument.

## 3. The smooth ample-divisor obstruction

For a smooth divisor \(S\subset Y=C_1\times C_2\times C_3\), differentiation
of its defining section along \(S\) gives

\[
ds:T_Y|_S\longrightarrow L|_S,\qquad L=\mathcal O_Y(S).
\]

Its kernel is \(T_S\). Let \(E=p_2^*TC_2\oplus p_3^*TC_3\).
The restriction \(p_1|_S\) fails to be a submersion exactly when
\(T_S=E\), equivalently when \(ds|_E=0\). Thus the submersion hypothesis
would produce a nowhere-zero section of \(E^*\otimes L\) on \(S\).

A nowhere-zero section gives a trivial line subbundle with a line-bundle
quotient, forcing \(c_2(E^*\otimes L)=0\). Its two Chern roots are
\(D+K_2,D+K_3\), not \(D-K_2,D-K_3\). Consequently the number in the package is

\[
\int_Y D(D+K_2)(D+K_3)
 =D^3+D^2(K_2+K_3)+DK_2K_3.
\]

The strict positivity is justified for an arbitrary ample divisor class,
including classes with mixed cohomology components. An ample class has
\(D^3>0\), while each pulled-back canonical class \(K_i\) is nef since
\(g(C_i)\ge2\). Mixed intersections of these nef classes are nonnegative.
The proof does not restrict all ample divisors to product-type classes.

I checked the signs independently by adjunction. On \(S\),

\[
c_2(T_S)=\sum_{i<j}K_iK_j+D\sum_iK_i+D^2,\qquad
K_S=D+\sum_iK_i.
\]

Since \(K_1^2=0\),

\[
c_2(T_S)-K_1K_S=(D+K_2)(D+K_3).
\]

For a smooth submersion onto \(C_1\), the tangent-bundle exact sequence
would give \(c_2(T_S)=K_1K_S\), yielding the same contradiction. This
independent derivation confirms both the bundle choice and the Chern signs.

The product-type expansion in the artifact is also correct. In particular,
at \(a=b=c=1\) and \(g_2=g_3=2\), the number is
\(6+4+4+4=18\).

## 4. Normality is an essential condition in the corollary

For a hypothetical triple of Kodaira fibrations, the joint image is a reduced
irreducible surface in the smooth threefold product. If it is normal,
Proposition 26 identifies it with its smooth normalization. A smooth
codimension-one image is a Cartier divisor.

Every point of the image has a preimage in \(X\). At such a preimage,
the chain rule applied to the original submersion forces the corresponding
restricted projection on the smooth image to have surjective derivative.
This agrees with the cited Lemma 13. If the image were ample as well,
Proposition 2 would apply and give a contradiction.

For a nonnormal image, a smooth normalization does not make the embedded
divisor smooth, and its normal-bundle calculation cannot simply be transferred
from the normalization. For a nonample image, the strict positivity argument
is unavailable. The package expressly retains both possibilities.
Finite-index image on fundamental groups does not imply ampleness.

## 5. Numerical necessities and their limits

Theorem 2 supplies a finite-index subgroup \(H\) of the product of the three
base surface groups, and an epimorphism \(\pi_1(X)\to H\).
Restriction from the product to \(H\) is injective on rational \(H^1\):
a rational character vanishing on a finite-index subgroup vanishes on every
group element after taking a positive power. Pullback under the epimorphism
is also injective. Therefore

\[
b_1(X)\ge2(b_1+b_2+b_3).
\]

The surface-bundle group sequence gives
\(b_1(X)\le2b_i+2g_i\), which yields
\(g_i\ge b_j+b_k\). Euler-characteristic multiplicativity gives
\(e(X)=4(b_i-1)(g_i-1)\). These are necessary conditions in the stated
triple-Kodaira regime, not sufficient conditions.

The sample \(b_i=2,\ g_i=4\) satisfies the displayed numerical conditions
with Euler characteristic 12 and coincident lower/upper first-Betti bound 12.
It is not asserted to be geometrically realizable.

## 6. Verification and disposition

The author's **48,002 finite exact assertions** replayed with
**byte-identical output**. The K3 PDF and the complete Llosa Isenrich–Py PDF
match the supplied checksums; the earlier incomplete download was not used
as the source copy.

Run the independent checker from this review directory:

    python3 independent_checks.py

It passes **6,731 exact assertions**, using a separate adjunction calculation
and a multilinear permanent evaluation of triple intersections. It includes
a canonical-sign negative control, the nonample boundary case, tangent-line
degree checks, and the Betti/genus/Euler arithmetic. These checks do not
construct or classify surfaces.

The correct publication status is **unsolved**, with the restricted
obstructions retained. Related record 30003293 shares the existence component,
but its additional relative-irregularity question has not been resolved.
The surviving problem is the general existence or exclusion of triples whose
joint image is nonnormal or nonample, together with any broader source-scope
issues. No complete resolution or historical novelty follows from this package.
