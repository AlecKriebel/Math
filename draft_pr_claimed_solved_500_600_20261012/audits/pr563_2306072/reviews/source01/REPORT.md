# Independent source-scope and theorem audit: PR563 / problem2306072

Audit completed 2026-10-13 UTC. Verdict: **PASS_SOURCE_SCOPE**. The classical geometric inputs apply to the specified coefficient functional with the sign, normalization, orientation, and endpoint conventions used in the candidate. This verdict certifies the source-to-proof bridge; it does not independently certify every quantitative estimate in the full candidate, historical priority, or novelty.

## Claim, assumptions, and success criteria

The frozen candidate is PROOF.md under ../../original/unsolved_math_prioritization/attempts/2306072. It specifies
\[
L(f)=a_2(f)+i10^{-24}\bigl(a_4(f)-3a_3(f)\bigr)
\]
on the locally uniform topology of \(H(D)\), and claims that every maximizer of \(\operatorname{Re}L\) in normalized \(S\) supplies an omitted arc whose continuous argument and radial angle are nonmonotone.

This audit tests whether Hayman-Lingham Problem 6.72 is that target, whether the actual maximizing maps fall within the cited support-point theorem, and whether the differential and geometric conclusions can identify the author's constructed trajectory with the actual omitted arc. Failure would include a functional outside the theorem's domain, a missing hypothesis, a reversed differential sign, multiple incoming trajectories, an excluded ray case, use of an unsigned angle in place of a signed one, or a formal trajectory lying past the actual tip.

Only frozen PROOF.md, SOURCE_GATE.md, and SOURCE_MANIFEST.json were consulted before independent derivations. Previous author reviews were not read. Sources were retrieved afresh. No external messages, remote writes, original edits, or edits to another reviewer occurred.

## Primary-source custody and coverage

| Source | Fresh bytes and SHA-256 | Actual coverage |
| --- | --- | --- |
| [Hayman-Lingham, arXiv:1809.07200v2 PDF](https://arxiv.org/pdf/1809.07200v2) | 1,706,228; 8e28fd4403a07e4e19a9816b7efaafddf9f475d59cf8c34a8255cb03833ed4f0 | Entire PDF retrieved; printed p.143 / PDF p.144 visually inspected, including Problem and Update 6.72. Reference 116 inspected in the full extracted bibliography. |
| [Duren, Arcs omitted by support points of univalent functions, ETH scan](https://www.e-periodica.ch/cntmng?pid=com-001%3A1981%3A56%3A%3A30&bot=1), [publisher DOI](https://doi.org/10.1007/BF02566218) | 17,295,781; dc2fea90c784fdedba74fa99a2225754e413368855fb94e87960e628b2ea7ec0 | Complete paper pp.352-365 read as text and all 14 article pages visually inspected. Its generated cover is PDF p.1; printed p.352 is PDF p.2. |
| [Pfluger, Lineare Extremalprobleme bei schlichten Funktionen, journal PDF](https://www.acadsci.fi/mathematica/1971/no489pp01-32.pdf), DOI 10.5186/aasfm.1971.489 | 2,647,035; 7e854da1875678f57db42df1ffeba6181f0a945c6e035c6af9a2d22ec8f8cdd6 | Complete 32-page source retrieved. Original proofs in sections 4.1-4.5, pp.21-29, read and all nine pages visually inspected. Relevant earlier setup and Schiffer-equation statements inspected as extracted text. |

The Hayman-Lingham fresh hash matches the author's receipt. The Duren fresh hash does **not** match the author's old 17,295,782-byte hash 099c6a5e7e7945fb06a4b858e6b81f3ad0bb7f4de2911f844048d2c180499ef0. The fresh PDF has a generated download sheet dated 13.10.2026 and a CreationDate dated 2026-10-13; it is not an immutable publisher binary. A second fresh GET matched our first file and each of the 14 decoded article-image payloads. SOURCE_CONTENT_CHECK.json contains those payload hashes. The author's old binary is absent, so old-versus-new article-payload equality is untested. Dynamic metadata is a concrete reason that full-file hashes can change; this is not a claim of proven binary equivalence.

The ETH wrapper assigns scan DOI 10.5169/seals-43249. That identifies the digital archive item, while 10.1007/BF02566218 is the article DOI. The article title, author, volume 56 (1981), and pp.352-365 match. Publisher access through the web parser failed; the complete ETH scan is the inspected evidence.

## Exact target and chronology

Problem 6.72 asks the two universal geometric questions about an analytic arc omitted by a support point of \(S\), and attributes the problem to P. L. Duren. The candidate's single counterexample functional, if its quantitative proof holds, is sufficient to negate both questions. The question does not require a formula for the maximizer or its uniqueness.

The source's claim about no progress is an editorial report in the 2018 version. The [arXiv version history](https://arxiv.org/abs/1809.07200v2) dates v2 to 21 September 2018; the PDF metadata's later creation date is not a distinct problem version. Neither observation certifies the current literature state.

Reference 116 in this version is Brown, A method for investigating geometric properties of support points and applications, Trans. AMS 287(1) (1985), 285-291. Duren p.353 separately cites Brown's 1979 point-evaluation paper. These are different bibliographic records, not incompatible normalizations or a reason to interchange the two papers. Duren's paper was received 25 November 1980 and published in volume 56 (1981). No priority conclusion is drawn here.

## Source-to-premise map

| Candidate premise | Source location and scope | Audit result |
| --- | --- | --- |
| \(S\) is analytic univalent functions on \(|z|<1\), \(f(0)=0,f'(0)=1\) | Duren p.352 defines the Taylor normalization. Pfluger p.3 has the same normalized class. | Exact agreement. |
| Continuous complex-linear supporting functional, with nonconstant real part | Duren p.352 uses a complex-valued continuous linear functional nonconstant on \(S\). Pfluger represents these by a contour kernel in (4). | Candidate satisfies the stronger real-nonconstancy condition explicitly. |
| Complement is a single analytic arc, finite tip to infinity, increasing modulus | Duren p.352 and section 2 p.354 state these for general support points. Pfluger section 4.5 pp.28-29 proves the single-arc conclusion and radial growth from its preceding variation results. | Applies to all actual maximizers of this \(L\). |
| \(Q_D=\Phi/w^2,\ \Phi=L(f^2/(f-w)),\ Q_D\,dw^2>0\) | Duren p.352 equation (1), visually read. | Correct sign and denominator. |
| Interior radial angle has magnitude \(<\pi/4\) | Duren p.352 explicitly supplies the strict interior version; endpoints may be exceptional. Pfluger pp.28-29 gives the non-strict bound in an older sign convention. | No conflict. Candidate does not require strictness at the finite tip. |
| \(L(f^2)\ne0\), simple pole at infinity | Duren p.353 attributes general nonvanishing to Pfluger. Pfluger section 4.4 pp.25-28 gives the original variation proof. | Also established directly for the present coefficient functional below. |
| Unique trajectory ending at a simple pole | Duren p.353 explicitly uses this fact. Pfluger p.28 uses the corresponding one-arc consequence. | Independently derived below in the candidate's cover coordinate. |
| Signed radial angle is outward \(\arg(w'/w)\), tends to zero at infinity | Duren p.354 chooses outward parametrization from finite tip to infinity; p.355 defines the angle and explains its limiting behavior. | Candidate \(\arg Z\) agrees after its parameter reversal. |
| General monotonicity is not already imposed by Duren's theorem | Duren section 4 theorem pp.358-364 concerns derivative point evaluation at a fixed nonzero disk point. | It is a special family, not an added hypothesis for the general slit theorem. |

Provenance precision: Duren p.352 describes the general slit statements as previously known and cites earlier works, rather than proving them anew. This audit therefore also inspected Pfluger's original geometric proofs. It does not claim to have formally reconstructed every foundational variation and analytic-continuation theorem that those proofs invoke. The core source-scope claim is that these established general theorems are stated with applicable hypotheses, and the candidate correctly uses them.

## Independent applicability and sign checks

For \(0<r<1\), Cauchy's coefficient formula gives
\[
|a_n(h)|\le r^{-n}\sup_{|z|=r}|h(z)| .
\]
Thus each coefficient map is continuous complex-linear on \(H(D)\). Their finite combination is also such a functional. In Pfluger's kernel convention,
\[
K(z)=z^{-3}+i\varepsilon(z^{-5}-3z^{-4}),
\qquad
L(h)=\frac{1}{2\pi i}\int K(z)h(z)\,dz.
\]
The kernel has only the allowed pole at zero. This supplies direct membership in his class (4).

For \(k=z/(1-z)^2\), \(a_2=2,a_3=3,a_4=4\), so \(\operatorname{Re}L(k)=2\); for \(h=z\), it is zero. Therefore the real part is nonconstant on \(S\). Once compactness supplies a maximizer, its support status follows without requiring uniqueness, a numerical search, or a converse statement about arbitrary trajectories.

There is a potentially consequential convention change in the older source, which the candidate avoids. Write \(Q_P\) for Pfluger's differential and \(Q_D\) for Duren's. Pfluger p.23 equation (50) gives
\[
L\!\left(\frac{\omega f}{\omega-f}\right)-L(f)
=\omega^2 Q_P(\omega).
\]
Independently,
\[
\frac{\omega f}{\omega-f}-f
=-\frac{f^2}{f-\omega}.
\]
Consequently \(Q_P=-Q_D\). Pfluger's negative trajectory condition and Duren's positive condition describe the same omitted curve. The manuscript uses Duren's convention consistently.

The simplest falsifiable sign control is \(L=a_2\): coefficient extraction gives \(\Phi=-1/w\) and \(Q_D=-1/w^3\). On the Koebe omitted negative real ray this differential is positive; on the positive real ray it is negative. Reversing either the denominator or the differential sign fails that control.

Independent sparse-Laurent expansion through \(z^4\) verifies
\[
[z^2]\frac{f^2}{f-w}=-w^{-1},\quad
[z^3]\frac{f^2}{f-w}=-2a_2w^{-1}-w^{-2},
\]
\[
[z^4]\frac{f^2}{f-w}
=-(2a_3+a_2^2)w^{-1}-3a_2w^{-2}-w^{-3}.
\]
It follows exactly that
\[
Q_D=-aw^{-3}-bw^{-4}-cw^{-5},\quad
a=1+i\varepsilon(2a_3+a_2^2-6a_2),\
b=i\varepsilon(3a_2-3),\
c=i\varepsilon.
\]
In particular \(a=L(f^2)\). The ordinary bounds \(|a_2|\le2,|a_3|\le3\) give \(|a-1|\le22\varepsilon<1\), independently of the fine Koebe-proximity estimates. Thus the candidate's pole at infinity cannot degenerate. In the sphere coordinate \(u=1/w\),
\[
Q_D(w)\,dw^2=(-a/u-b-cu)\,du^2,
\]
so its order there is exactly a simple pole.

## Independent unique-trajectory and actual-slit argument

Under \(w=-v^{-2}\), direct substitution gives
\[
Q_D(w)\,dw^2=4(a-bv^2+cv^4)\,dv^2=4P(v)\,dv^2.
\]
Since \(P(0)=a\ne0\), choose a square root \(p=\sqrt P\) on a small disk and define \(G(v)=\int_0^v p(s)\,ds\). The inverse-function theorem applies at zero. A positive trajectory is horizontal in \(G\): the positivity condition is \(4(dG)^2>0\), and a trajectory ending at zero must have \(\operatorname{Im}G=0\). There are two lifted halves \(G=t>0\) and \(G=t<0\). Because \(P\) is even, the chosen \(p\) is even, \(G\) is odd, and its local inverse \(V\) is odd. The projection \(-V(t)^{-2}\) identifies those halves. Hence exactly one unparameterized positive trajectory ends at infinity in the \(w\)-plane. There is no hidden choice among several slit branches.

On the author's larger disk, provided its explicit \(P\ne0\) and inverse estimates hold, the same argument gives a regular curve \(W(t)=-V(t)^{-2}\), \(0<t\le7/4\). It is injective: equality of two \(W\) values implies \(V(t_1)=\pm V(t_2)\), and applying the odd inverse relation gives \(t_1=\pm t_2\); for positive parameters only equality is possible. Its differential satisfies \(Q_D(W)W'^2=4\).

The actual omitted arc and this regular curve coincide near infinity by the preceding local uniqueness. At a common regular point with \(Q_D\ne0\), a local square-root coordinate again gives an ordinary unique horizontal trajectory, so their coincidence continues. The only potential termination is at the actual finite slit tip. The author's tip estimate is \(r_{\rm tip}<3/10\), while the constructed segment satisfies \(|W|>25/81\). The exact gap is
\[
\frac{25}{81}-\frac{3}{10}=\frac7{810}>0.
\]
Therefore that segment cannot contain the tip or continue through it into a fictitious inner portion. This is the necessary use of global support-slit geometry. It is not a sufficiency claim that the constructed differential itself proves extremality.

The arc's increasing modulus comes from the general theorem. Along a regular outward parametrization, \(d|w|/ds>0\); the \(\pi/4\) bound also shows that the real part of \(w'/w\) cannot be zero there. Thus following \(W\) from infinity toward increasing positive \(t\) is indeed the inward direction, and \(-W'\) points outward.

## Signed, unsigned, and argument-lift conventions

Independently differentiating gives
\[
\frac{W'}{W}=-2\frac{V'}{V},\qquad
\frac{-W'}{W}=\frac2t Z,\qquad Z=\frac{tV'}V.
\]
For any continuous argument lift \(\theta\), \(\theta'=-2\operatorname{Im}Z/t\). Derivative signs at two regular points are independent of changing the lift by \(2\pi m\), and reversing traversal only interchanges increasing and decreasing. The candidate does not rely on a discontinuity of principal argument across the negative real axis.

Where \(\operatorname{Re}Z>0\), the signed outward radial angle in Duren's convention is \(\beta=\arg Z\), and the ordinary unsigned angle is \(|\beta|\). Since \(V(t)=a^{-1/2}t+O(t^3)\), \(Z(t)\to1\) and \(\beta(t)\to0\) at infinity.

Conditional on the manuscript's stated bound \(|Z-1-i\varepsilon q|\le2000\varepsilon\eta\), independent exact arithmetic gives \(q(1)=3/5\), \(q(7/4)=-441/640\), and \(2000\eta=1/500000000\). Both signs retain margin greater than \(1/2\) in units of \(\varepsilon\). Thus \(\theta'\) has opposite signs, and \(\beta\) has opposite signs while its initial limiting value is zero. Neither can be monotone. Continuity forces an intermediate zero of \(\beta\), so \(|\beta|\) is positive, zero, positive on an ordered triple, also disproving unsigned monotonicity. Choosing the inward tangent changes the ordinary vector angle to \(\pi-|\beta|\), which likewise is nonmonotone. The acute tangent-line interpretation is \(|\beta|\).

The limiting unperturbed case \(\varepsilon=0\) has \(P=1,W=-t^{-2},Z=1\): the ray and zero radial angle are monotone. The proof requires strictly positive perturbation; its uniform explicit error is what permits a tiny perturbation to reverse sign. No exception for rays is being silently assumed in the theorem.

## Falsification results, limits, and later-phase leads

No incompatible normalization, missing functional hypothesis, excluded slit type, wrong trajectory sign, ambiguity of signed angle, or infinity-branch multiplicity was found. All source-based bridge claims pass. SOURCE_BRIDGE_CHECKS.json records the independently executable exact algebra and boundary checks; running check_source_bridge.py with Python reproduces them without the author's scripts.

This is not an independent verification of every scalar remainder in PROOF.md or the classical coefficient/area theorem foundations. Those are separate mathematical-verification responsibilities. Given their validity, this source audit leaves no unresolved source-scope obstacle to the claimed counterexample. No historical-priority conclusion, current-open certificate, or novelty judgment is implied.

Useful later-phase primary-source leads are Brown's 1979 point-evaluation paper, his \(a_3+\lambda a_2\) paper cited as forthcoming in Duren, Brown's 1985 paper actually numbered 116 in Hayman-Lingham, Duren's later univalent-functions textbook, and Hibschweiler's 1995 eventual-monotonicity work. The finite coefficient perturbation lies outside the derivative point-evaluation family treated by Duren's principal theorem. These leads identify where to search; they are not a bounded-search novelty verdict.
