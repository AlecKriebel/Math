# Independent prior-implication audit: PR 1129 / problem 30005461

Verdict: **VERIFIED_PRIOR_FULL_CONSEQUENCE**.

This verdict concerns the exact two-clause mathematical target at frozen head
`26fed29c1130e539ba018a37200f133870f0e036`. It is a **NEW audit deduction of a
consequence of prior results**, not a claim that the earlier sources explicitly
print the sentence `lim c_k = 3`. Relative to the stated theorem of the
February 2026 preprint *Stubborn Polynomials*, the full remaining threshold
clause follows after routine, completely supplied hypothesis checks. The other
clause is the published Blekherman--Kozhasov--Reznick (BKR) mixed-exponent theorem.
No essential unsupported mathematical step in this priority bridge was found.

The frozen principal proof can still be mathematically correct and independent
of that preprint. That independence does not prevent the same full conclusion
from being an earlier theorem's consequence. A generic disclaimer of novelty
does not remove the actual full two-clause conclusion from the audit's scope.
Under the supplied disposition rule, this evidence supports skipping PR 1129
entirely. This reviewer has made no PR, publication, tracker, Git index, branch,
remote, or original-input mutation.

## Claim and success criteria

Write

\[
M_c=x^4y^2+x^2y^4+z^6-cx^2y^2z^2,
\qquad f_c=M_c(x,y,1).
\]

The two target clauses, as found in the original Reznick contribution, are:

1. For real polynomials \(p,q\) and nonnegative integers \(i,j\), if
   \(p^{2i+1},q^{2j+1}\) are sums of squares (SOS), then
   \((p+q)^{2i+2j+1}\) is SOS.
2. For the thresholds defined by
   \(\{c:f_c^{2k+1}\text{ is SOS}\}=(-\infty,c_k]\), determine their limit.
   The frozen claim gives the value 3 and the stronger assertion that every
   real \(c<3\) has all sufficiently large odd powers SOS.

Success here means a checkable deduction of both full clauses from prior
primary results, with all target-specific hypotheses verified. A theorem that
only treats positive definite forms, a fixed parameter such as \(c=1\), even
powers, a different perturbation, or a statement merely conjectured in the
source would not suffice. No other review's acceptance was used as a premise.

The original is Bruce Reznick, *The Odd Powers of the Motzkin Polynomial, etc.*,
Oberwolfach Report 14/2023, contribution printed pp.778--780, DOI
[10.4171/owr/2023/14](https://doi.org/10.4171/owr/2023/14). The mixed-exponent
conjecture and the precise affine threshold family both appear on printed
p.780, physical PDF p.40 of the [original PDF](https://ems.press/content/serial-article-files/47007).
The different positive definite perturbation later on that same page is not
being confused with \(M_c\).

## Imported prior input and its boundary

The version-pinned primary preprint is L. Baldi, G. Blekherman, K. Kozhasov,
D. Plaumann, B. Reznick, R. Sinn, [*Stubborn Polynomials*, arXiv:2602.01191v1](https://arxiv.org/abs/2602.01191v1),
submitted 2026-02-01, PDF dated 2026-02-03. It is treated as an arXiv preprint,
not as a journal publication or a formal proof-assistant certificate.

Theorem 6.4, on PDF p.20, states in mathematical paraphrase:

\[
F\text{ nonnegative ternary sextic},\quad F\notin\mathrm{SOS},\quad
\delta^{\mathbb R}(F)\le8
\quad\Longrightarrow\quad F\text{ is not stubborn}.
\]

Theorem 1.2 gives the larger classification. Definition 2.1 makes stubbornness
the failure of **every positive odd integer power** to be SOS. Definition 6.3
defines real delta by successive real infinitely near points, adding
\(m(m-1)/2\) at a point of multiplicity \(m\). These exact definitions and the
full proof of 6.4, including its preceding reduction, were inspected, not just
the abstract. The theorem statement adds no irreducibility, reducedness,
complex-singularity, ordinary-node, or general-position hypothesis.

The import remains a theorem-level import: this audit has not reconstructed
every cited result in algebraic geometry. Its actual anticanonical mechanism
and the applicable primary supporting formulas were checked further below.

## Complete threshold bridge

### Nonnegativity, real zero set, and all real parameters

For real \(x,y,z\), AM--GM gives

\[
x^4y^2+x^2y^4+z^6\ge3x^2y^2z^2.
\]

For \(0<c<3\), this implies
\(M_c\ge(3-c)x^2y^2z^2\ge0\). A real projective zero must have \(xyz=0\).
If \(z\ne0\), either \(x=0\) or \(y=0\) leaves the positive value \(z^6\).
On \(z=0\), the zero condition is \(x^2y^2(x^2+y^2)=0\), so the only real
projective zeros are \(P=[1:0:0]\) and \(Q=[0:1:0]\).

For \(c\le0\), there is already an SOS:

\[
M_c=(x^2y)^2+(xy^2)^2+(z^3)^2+(\sqrt{-c}\,xyz)^2.
\]

This handles zero, negative parameters, and arbitrarily large negative values
without applying a theorem whose non-SOS hypothesis they fail.

### Independent proof of non-SOS for every \(c>0\)

Suppose \(M_c=\sum h_r^2\), with homogeneous cubics \(h_r\). The zero
coefficients of \(x^6,y^6\) force the \(x^3,y^3\) coefficients of every
\(h_r\) to vanish. Next the zero coefficients of \(x^4z^2,y^4z^2\) force
the \(x^2z,y^2z\) coefficients to vanish: the only remaining contributions
to each are sums of squares of the named root coefficients. Finally the zero
coefficients of \(x^2z^4,y^2z^4\) similarly eliminate \(xz^2,yz^2\).

The surviving cubic monomials are exactly
\(x^2y,xy^2,z^3,xyz\). In a square supported on these, the coefficient of
\(x^2y^2z^2\) is precisely the square of the coefficient of \(xyz\).
The coefficient in their SOS is therefore nonnegative, contradicting \(-c<0\).
This supplies the required hypothesis without assuming the classical Motzkin
argument or a Newton-support theorem. The coefficient eliminations are exact
symbolic checks in `check_bridge.py`.

### Independent real-delta computation for every \(0<c<3\)

At \(P\), use \(u=y/x,v=z/x\). Then

\[
F_0=u^2+u^4+v^6-cu^2v^2.
\]

The following are the main strict-transform charts, each obtained by dividing
by the square of the new exceptional coordinate:

\[
\begin{aligned}
u=av:&\quad F_1=a^2+a^4v^2+v^4-ca^2v^2,\\
a=bv:&\quad F_2=b^2+b^4v^4+v^2-cb^2v^2,\\
b=tv:&\quad F_3=1+t^2-ct^2v^2+t^4v^6.
\end{aligned}
\]

The centers \(F_0,F_1,F_2\) have multiplicity 2 and tangent cones
\(u^2,a^2,b^2+v^2\), respectively. The first two exceptional equations
are \(a^2=0,b^2=0\), each giving one real next center. After the third
blowup the exceptional equation is \(1+t^2=0\), with no real solution.

Both charts at each step are necessary. The complementary strict transforms,
under \(v=wu\), \(v=wa\), and \(v=wb\), are respectively

\[
\begin{aligned}
&1+u^2+w^6u^4-cw^2u^2,\\
&1+w^2a^4+(w^4-cw^2)a^2,\\
&1+w^2-cw^2b^2+w^4b^6.
\end{aligned}
\]

Their exceptional restrictions are \(1,1,1+w^2\), so no real direction
or intersection at infinity was omitted. The infinitely near centers are free
points on the newest exceptional curve; no satellite intersection adds a
missing contribution. Definition 6.3 therefore gives
\(\delta_P^{\mathbb R}=1+1+1=3\). Symmetry gives the same at \(Q\), hence

\[
\boxed{\delta^{\mathbb R}(M_c)=6<9\quad(0<c<3).}
\]

The charts hold identically in the symbolic parameter \(c\). This is not an
extrapolation from \(c=1\) and does not replace real delta with complex delta.

### Odd power, eventuality, and the limit

All three hypotheses of prior Theorem 6.4 now hold for each \(0<c<3\).
Consequently there is a positive odd integer \(m=m(c)\) and real forms
\(H_r\) such that \(M_c^m=\sum H_r^2\). If \(m'\ge m\) is odd, then

\[
M_c^{m'}=\sum_r\left(M_c^{(m'-m)/2}H_r\right)^2.
\]

The same conclusion holds for \(c\le0\) from its explicit SOS. Setting
\(z=1\) proves the exact claimed affine eventual odd-SOS conclusion for
**every real \(c<3\)**. The exponent may depend on \(c\); no uniform bound
or convergence rate is required or inferred.

BKR's published Theorem 6.3 supplies precisely
\(V_{2k+1}=(-\infty,c_k]\) for this homogeneous family, with
\(c_k\in[0,3)\). It agrees with the affine convention: any SOS of
\(f_c^m\), of degree \(6m\), has root degrees at most \(3m\), since
top-degree squares cannot cancel over the reals; homogenizing each root to
degree \(3m\) gives an SOS of \(M_c^m\). The converse is dehomogenization.

For each fixed \(c<3\), eventual SOS gives \(c_k\ge c\) eventually, hence
\(\liminf c_k\ge3\). For \(c>3\), \(M_c(1,1,1)=3-c<0\), so no odd
power is SOS. Thus \(c_k\le3\), proving

\[
\boxed{\lim_{k\to\infty}c_k=3.}
\]

This does not assert non-stubbornness at \(c=3\). Four additional real zeros
appear there, and the real delta count becomes 10; the prior classification
then agrees with stubbornness of the Motzkin endpoint. For \(c>3\), the
nonnegativity hypothesis fails. Both boundaries therefore behave consistently.

## Adversarial checks on source applicability and its proof

**Possible hidden geometric assumptions.** Theorem 6.4's statement has none of
the suspected extra restrictions. Its use of irreducibility in the proof is a
reduction from nonnegative sextic plus non-SOS, not an added theorem hypothesis.
For this application the six centers are explicit. They form two disjoint
chains of three free points. No line passes through four of them: \(y=0\)
meets all three over \(P\), \(x=0\) all three over \(Q\); any other line
through one original point misses the next tangent direction, while the line
through both original points is \(z=0\), missing both next centers. With
only six centers, the seven-point conic obstruction is absent.

I checked Demazure's original seminar version of *Surfaces de Del Pezzo III*,
Definition 1 and Theorem 1 (physical p.7), against these conditions: they imply
nef anticanonical class. Its square is \(9-6=3>0\), as required for the weak
Del Pezzo route. This also checks the target-specific role of the reduction
without depending only on the preprint's very compressed Lemma 6.2 proof.

**Contraction and positivity.** The full proof of 6.4 resolves the real zeros,
contracts to the anticanonical model, descends the now strictly positive
bi-anticanonical section, applies Scheiderer there, then pulls back and pushes
down the SOS. I independently inspected the primary Demazure IV corollary
following Proposition 2 (physical p.7): an anticanonical-multiple divisor
meeting a fundamental cycle contains that cycle. Demazure V, Theorem 2
(physical p.7), gives the contraction fibers and the required invertible
canonical-sheaf pullback/pushforward identities; its Corollary 3 (physical p.8)
gives the anticanonical ampleness. These are the actual needed formulas.
They support the source's mechanism rather than a wish to apply positivity
directly to a sextic with zeros. In this target all contracted curves are real
and have real points, so descent does not conceal a real point with only
nonreal preimages. Division by each exceptional factor is by a square, and
preserves the nonnegative sign before the last real zeros disappear.

**Source typographical defect.** Theorem 6.4's last paragraph prints
\(L=M=\omega_{\bar Z}\) in its invocation of Scheiderer, although the section
is in \(\omega_{\bar Z}^{-2}\), the asserted roots are in
\(\omega_{\bar Z}^{-k}\), and the ample bundle is anticanonical. The
consistent invocation is \(L=M=\omega_{\bar Z}^{-1}\). This is a local inverse
sign correction determined by the surrounding formulas, not a new existence
lemma or an unresolved obstacle to the theorem. No theorem from the source's
unneeded converse direction 6.6 is used.

**Complex singularities, independently.** Although not required by 6.4,
there is no mismatch with BKR's published description using only real
singularities. If \(xyz\ne0\), vanishing gradients give
\(x^2=y^2\), \(3x^2=cz^2\), and \(3z^4=cx^4\), forcing \(c^3=27\).
This is impossible for real \(c<3\). If a coordinate vanishes, the gradients
leave only \(P,Q\). Locally the analytic substitution
\(U=u\sqrt{1-cv^2+u^2}\) gives \(U^2+v^6\), an \(A_5\) singularity
with complex delta 3 as well. Thus no nonreal singular point is being silently
dropped in this family. The two complex directions after the third blowup
are not real infinitely near points, exactly as Definition 6.3 requires.

This also gives an independent irreducibility check for the source's reduction
in this target. Finite singular locus implies that the sextic is reduced. Each
\(A_5\) point has exactly two smooth complex branches, with mutual local
intersection multiplicity 3, since the ideal of \(U-iv^3,U+iv^3\) has
length 3. If there were two global components of degrees \(e,6-e\), every
intersection would be at \(P\) or \(Q\), and their total intersection would
be 3 or 6. Bezout instead gives \(e(6-e)\in\{5,8,9\}\), a contradiction.
Three or more components are also impossible: every distinct pair must
intersect, but each of the only two singular points accommodates at most one
pair of distinct components. Thus the curve is geometrically irreducible for
\(0<c<3\), without importing the full general reducible-sextic reduction.

**Reproducibility.** `check_bridge.py` passed 172 exact checks under Python
3.14.6 and SymPy 1.14.0. These include all six local charts, three multiplicities,
the non-SOS coefficient elimination, parameter identities, 64 mixed-exponent
factorizations and their parity, and adverse controls rejecting a wrong
exceptional exponent, premature delta termination, the two-zero claim at
\(c=3\), and the nonnegativity claim at \(c=4\). This verifies transcriptions;
it does not computationally prove the imported existence theorem. See
`CHECK_RESULTS.json` and the reproduction note in `SOURCE_VERSION_NOTES.md`.

## First clause and full-target accounting

BKR, [*On odd powers of nonnegative polynomials that are not sums of squares*](https://doi.org/10.1017/fms.2026.10221),
Forum of Mathematics, Sigma 14 (2026), e65, online 2026-04-27, Theorem 5.3,
proves the exponent \(K+L-1\) for odd \(K,L\). The published proof and its
Pinelis ingredient, Theorem 5.2, were inspected. Substituting
\(K=2i+1,L=2j+1\) gives the exact first-clause exponent.

Its homogeneous equal-degree presentation also covers arbitrary real
polynomials: choose a common even degree \(2d\) at least their degrees and
homogenize both to that degree. If \(p^K\) is SOS, homogenizing its roots to
degree \(dK\) makes \(P^K\) SOS, and similarly for \(q\). Apply Theorem 5.3
and dehomogenize. Zero polynomials and \(K=1\) or \(L=1\) are included.
Thus no part of the actual two-clause target remains outside the prior bridge.

The current BKR paper's paragraph before Problem 6.2 explicitly acknowledges
the Stubborn classification, while its final paragraph still asks about the
threshold limit. I verified both statements in the same current publisher
PDF. That unupdated question supplies no mathematical counterexample to the
bridge. Neither the Stubborn text inspected nor the focused primary-source
search supplied an explicit printed \(\lim c_k=3\) statement; the present
verdict deliberately says **prior full consequence**, not prior explicit
target sentence. No absence-of-search-hit claim is needed for the verdict.

## Priority judgment and remaining boundary

The new work supplied here to connect the theorem to this target consists of
the exact local real-delta computation, elementary non-SOS and boundary checks,
and the square-multiplication/threshold deductions. These are routine
applications of the prior criterion, fully displayed above; they do not
transfer the main odd-SOS existence difficulty to a new unsupported claim.
The preprint even discusses the same \(c=1\) family and its two local delta-3
zeros on p.19, though that single example alone would not prove all parameters.

The strongest verified statement is the entire two-clause target as a
consequence of BKR Theorem 5.3 plus Stubborn v1 Theorem 6.4, with the threshold
convention from BKR Theorem 6.3. There is no remaining target-specific
mathematical gap in this bridge. The exact boundary is reliance on the prior
preprint theorem, whose full proof and essential anticanonical formulas were
read and checked at the level stated, rather than formally verified or
republished as a journal theorem. Its preprint status must remain visible.

Audit completion estimate: **100% of this assigned prior-implication audit**.
No external individual was contacted and no outreach was prepared.
