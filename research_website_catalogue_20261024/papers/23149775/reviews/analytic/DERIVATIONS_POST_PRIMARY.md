# Analytic116: closed primary interfaces and exact derivations

This file supplements, rather than replaces, the immutable pre-exposure `INITIAL_RECONSTRUCTION.md`. The latter already contains the eight-family proof reconstruction, direct fixed-triangle certificate and general axial-triangle derivation. All foreign bodies, source programs, results and the published supplement were examined after initial seal SHA-256 `9aa2324160d7c3febb036bb5665d04e3ce67d93e9c00296fb42c355fb70f9cc7`. No sibling mathematical report has been read. This is a mathematical review of the actual published six-page version 1.0, not a repair or a proposed weaker result.

## 1. Canonical coordinates and the exact analytic category

The actual Stachel journal body, Theorem 4.3 and equation (4.9), printed p.1614, provides canonical coordinates for the whole family of closed billiards with the fixed confocal elliptical caustic. Its turning number permits the primitive star cases. Scaling the caustic major radius to one gives modulus `0<k<1`, minor radius `k'=sqrt(1-k²)`, and the common foci `(±k,0)`. The boundary is

`P(u)=(-a sn u,b cn u), a=dn(v)/cn(v), b=k'/cn(v), v=2K τ/N, δ=2v`.

Here `gcd(τ,N)=1`, `N≥3` and `0<τ<N/2`, so `0<v<K`, `a>1`, `b>k'`. The normal vectors of the caustic and boundary tangents are respectively `(-sn u,cn u/k')` and `(-sn u/a,cn u/b)`, with support height one. Applying Jacobi addition, in the modulus convention of the manuscript rather than the parameter `m=k²` convention of some literature, puts `P(u±v)` on the former line. Thus the chord-foot trace uses `w+v+jδ`; the tangent-foot trace uses `w+jδ`. This offset is essential.

The full supporting line, not a clamped segment, is projected onto. For a nonisotropic real normal `n`, the foot of `F` is `F+(1-n·F)n/(n·n)`. Continuation uses the bilinear dot product, never complex conjugation. Rational substitution of `sn²+cn²=1` and `a²-b²=k²` yields exactly

`q=((k-sn)/(1-k sn), k' cn/(1-k sn))`,

`Q=(a(k-a sn)/(a-k sn), ab cn/(a-k sn))`.

Their real denominators are positive. The focus lies strictly inside both ellipses. Consecutive boundary tangents are not parallel because their canonical parameters differ by `δ` strictly between zero and `2K`. Thus the outer polygon and every real foot/area in the theorem are defined. The target's pole computations concern meromorphic continuations; they do not assert complex orthogonal projection onto every isotropic line.

The actual official DLMF sections [22.4](https://dlmf.nist.gov/22.4), [22.5](https://dlmf.nist.gov/22.5), [22.8](https://dlmf.nist.gov/22.8) supply the periods, special values and addition/quarter-shift identities used here. The response retained locally is a web extraction, explicitly not native PDF/HTML custody. Direct ordinary HTML retrieval failed and those failure bodies remain labelled as such.

There is an ancillary misprint in the actual Stachel p.1613 period display: it assigns a factor `(-1)^j` to `dn(u+2jK)`. The correct real period of `dn` is `2K`, as in DLMF. This does not propagate to the target: its real reduction uses `sn/cn` with period `4K`, and its imaginary reflection uses the correct `sn/cn` shifts. The canonical-coordinate interface and all identities used in the manuscript agree with the correct Jacobi identities. No target repair is required or made.

## 2. A universal principal-part proof, rather than finite evidence

Let `A(w)` be half the cyclic determinant sum of the `q(w+v+jδ)` and `B(w)` that of `Q(w+jδ)`. Cyclic reindexing and coprimality give the real period `L=4K/N`. The imaginary shift `2iK'` fixes `sn` and negates `cn`, reflecting both foot maps and reversing their determinant sums. Hence both traces are meromorphic on the compact torus with periods `(L,4iK')`, with common antiperiod `2iK'`.

Common Jacobi poles are removable in each rational foot map: numerator and denominator have compatible simple poles with nonzero leading denominator coefficient. Set `r=K+iK'`. DLMF quarter shifts give

`sn(r+z)=dn z/(k cn z), cn(r+z)=-i k'/(k cn z)`.

The degree-two `sn` map on its `(4K,2iK')` torus has one double preimage of `1/k`, namely `r`. The `q` germ is even and starts with `2(1,i)/(kz²)`. At a phase where one original foot is singular, primitivity makes it the only singular original foot. Its two incident area edges combine into

`(1/2) det(q(r+z), q(r+z+δ)-q(r+z-δ))`.

The second vector is odd holomorphic, hence `O(z)`. Therefore the double vertex pole yields at most a simple area pole. Removable Jacobi poles at a neighbor are harmless, including `δ=K` in the four-period case. This cancellation is an exact germ identity, not an extrapolation from a numerical Laurent fit.

The outer map denominator has the two distinct simple roots `r-v,r+v`, since `sn=a/k` there and `0<v<K`. At either root the numerator vector is `-ab²(1,i)/k`. The denominator derivatives are `+b² sn v` at `r-v` and `-b² sn v` at `r+v`. Thus the residues are `-R,+R` with `R=a(1,i)/(k sn v)`. They occur at two adjacent outer feet; the common edge's possible double-pole coefficient is `det(-R,R)=0`. The other incident edges have only one singular endpoint. Primitivity excludes any further singular vertices, and the same reasoning covers the cyclic closing edge and `N=3`.

After the real period reduction the only possible poles of either area trace are `r-v` and `r-v+2iK'`, each of order at most one. The midpoint offset in `A` makes these the same pair as in `B`.

For either ellipse with semiaxes `R,S`, its real outward normal `n=(-sn/R,cn/S)` satisfies `det(n,n')=dn/(RS)>0`. A continuous normal angle increases by exactly `π` on each interval of length `2K`. Therefore every step `δ∈(0,2K)` advances that angle strictly between zero and `π`. Relative to the focus, every foot is a positive scalar multiple of its outward normal. Each consecutive determinant, including the closing edge in a continuous lift, is strictly positive. The lifted total advance is `2πτ`; the conclusion holds for stars as well as convex orbits. Translation invariance of a closed shoelace sum gives `A(w)>0`, `B(w)>0` for every real phase.

If either possible pole of a trace were absent, antiperiodicity would remove the other, and compact-torus holomorphy would make the trace constant. Antiperiodicity forces that constant to zero, contradicting positivity. Both traces therefore have genuine simple poles with nonzero residues. Choose `C0=Res(B)/Res(A)` at the first pole. Then `B-C0 A` is pole-free there and, by common antiperiodicity, at the other. It is holomorphic on the compact torus, hence constant, hence zero. Real positivity now proves `C0` real and positive. No independent assumption that a complex residue ratio is real has been made.

Central inversion is the real shift `2K`; it preserves orientation and exchanges foci. Thus `A_-(w)=A(w+2K)` and `B_-(w)=B(w+2K)`, giving the SAME multiplier for the other focus. All four denominators are nonzero before taking the focal ratios. Reversal negates all areas, and a positive integral repetition multiplies all by the same positive integer. For even primitive `N`, `2K` is a real period and the focal ratio is one; for odd `N` it is only `L/2` modulo `L`. Confusing these two situations would incorrectly infer focal-ratio constancy.

The circular case is separate: the original pedal feet have radius `R cos θ`, the tangent pedal feet radius `R`, and their angular increments are `2θ`, where `θ=πτ/N∈(0,π/2)`. Their positive signed sums therefore have ratio `sec²θ`. No hyperbolic/collapsed caustic, diameter limit, unsigned lobe sum or clamped projection is proved or asserted.

## 3. Exact triangles, independently of historical center loci

For the actual ellipse `x²/21+y²/16=1`, the listed axial triangle has side lengths `8,32/5,8`. Its actual confocal caustic has squared semiaxes `189/25,64/25`, whose difference is five, and its oblique contact points `(9sqrt(21)/25,±32/25)` occur at segment fraction `2/5`; the vertical contact is its midpoint. Exact incoming/outgoing unit-vector reflections hold at all three vertices. Thus the example is an actual primitive positively oriented triangular billiard in the claimed strict caustic category.

Direct line projections and determinants, reproduced symbolically with both focus signs, give

`A_e=84(7sqrt(21)+e sqrt(5))/625`,

`B_e=7(7sqrt(21)+e sqrt(5))/10`, `e=±1`.

Their multiplier is `125/24`. The common focal ratio is greater than one. The centrally inverted triangle is a phase of the same fixed family, preserves orientation and yields the reciprocal, less than one. This is an exact nonconstancy certificate; it does not refute the displayed focal-ratio equality. It is also not a newly claimed historical theorem.

For the full prior triangular multiplier, set `X=a²`, `Y=b²`, `D=sqrt(X²-XY+Y²)`, `t=(D-Y)/(X-D)`. Since `X>Y>0`, `Y<D<X` and `2D>X+Y`, so `t>1`. The defining relation gives `X/Y=t(t+2)/(2t+1)`. After scaling choose `X=t(t+2)`, `Y=2t+1`, `a=sqrt X`, `c=sqrt(t²-1)`. The actual axial triangle is

`(a,0), (-at/(t+1),Y/(t+1)), (-at/(t+1),-Y/(t+1))`.

Its squared caustic axes are `Xt²/(t+1)²`, `Y/(t+1)²`, strictly nested and confocal. Oblique contact occurs at fraction `1/(t+1)∈(0,1)`; direct reflection holds. Direct shoelace projection gives

`A_e=X[a(t+2)+e c(t-1)]/(t+1)^4`,

`B_e=(t+2)[a(t+2)+e c(t-1)]/[2(t+1)]`.

Thus the multiplier is `(t+1)^3/(2t)` for both foci. The universal analytic result makes it the multiplier at every phase of that triangular family. This independent derivation was sealed before reading the deposited historical deduction. It confirms the stated formula without treating a locus's shape as simultaneous center-coordinate information. It is verification of an existing claimed formula, not an extended repair or proposed narrower substitute.

The historical book Theorems 2.1 and 2.3 (printed pp.13–17), Helman et al. §§3.4–3.5, and the published supplement's explicit simultaneous-coordinate premise have been checked at the actual statement/proof-interface level. The five deposited exact historical-power residuals replay to zero. The generic computer-algebra derivation behind the old locus theorem was not independently recertified. The main theorem and the direct triangular certificate do not depend on that generic historical derivation. Querret's actual scanned opening p.280 and closing p.285 and Fierobe Lemma 4.1 have been read; the entire historical signed formula was not reconstructed from imperfect French OCR. Those limitations are retained, without replacing the independently checked exact certificate by an unverifiable historical assertion.

## 4. Meaningful computational checks and their precise force

`independent_exact.py` implements 57 explicit guarded identities in each of normal and optimized modes: universal projection identities and auxiliary circles, the even original quarter germ and its leading sign, derivative/outer residues, collinearity cancellation, general triangle geometry/reflection/contact/projections, fixed radical areas and multiplier, orientation/repetition, and rejection of four false algebraic assertions. These are rational/polynomial identities under stated algebraic relations. Real domain inequalities and the all-`N` torus argument are proved above, not inferred by a CAS from finite examples.

`independent_complex.py` uses 90-digit mpmath arithmetic without importing deposited functions: ten families, two real phases per family, both foci, convex and star turning classes, direct geometric feet/outer intersections, phase/focal multiplier equality, complex periods/antiperiods, and near-pole diagnostics. It produces 407 checks with maximum normalized discrepancy `3.448543526657284e-24`; the near-pole finite-ε comparison allows `1e-9`, while ordinary complex identities use `1e-50` and the near-pole multiplier uses `1e-40`. Normal and optimized receipts are byte-identical. These are NONINTERVAL finite diagnostics, not rigorous error bounds or proofs over a continuous domain.

Five in-memory faults, each tested in both execution modes, corrupt the original double-pole sign, outer residue sign, triangular scalar, chord midpoint and opposite-focus phase. All ten executions reject the intended error with explicit runtime guards. No pristine file or source is mutated.

Four byte-identical mathematical source copies were executed normally in the isolated review cache: `verify_exact`, `verify_triangle`, `verify_historical_power`, `verify_reflection`, with the byte-identical `reflection_geometry` module imported. All four complete stdout streams equal the deposited receipts byte for byte, and all stderr streams are empty. The first reports literal `PASS`, 3133 exact assertions and 89 finite lattice pairs; the reflection program reports literal `PASS`, 18 finite 100-digit samples over nine geometric families. Counts and finite reflection samples supplement the proof; they do not establish its universal quantifiers. The other two deposited numerical program bodies were read, but their campaigns and the larger 117-sample main entrypoint were not gratuitously repeated. No generic builder, finalizer, publication action or source-program writer was invoked.

The source exact checker uses Python `assert`. An in-memory wrong-scalar control (`125/24→126/24`) is rejected normally, but optimization removes the assertions and prints literal `PASS`. Both outcomes are preserved in `ASSERT_MODE_SENSITIVITY.json`; its raw optimized `PASS` is not coerced into successful mathematical validation. The published instructions use normal Python, and the actual native reproduction was normal. This is a disclosed execution-mode limitation, not evidence against the mathematical theorem or permission to rewrite the published source.

## 5. Historical statements and exact remaining limits

The actual RGK versions display the same equality with different identifiers: v1 Table 5 p.6 k605, v11 Table 7 p.9 k606, actual journal Table 7 p.349 k607. The journal uses signed area and explicitly gives the even symmetry case. The newly fetched AMJ PDF is byte-identical to the historical raw copy first recovered here. A previous status-200 HTML response is not misrepresented as journal PDF custody.

The actual KLS §4.1 equations (39)–(42) and Roitman et al. local cancellation/Liouville interfaces confirm that principal-part comparison on an elliptic torus is established methodology. The actual pinned original-foot and outer-foot mathematical proofs show the credited specialized local cancellations. Their parity-restricted final conclusions are not imported as the universal theorem. The three precisely cited recent notes have been checked for their actual statement/quantities/version/date: original focal pedal–antipedal products for least period divisible by four, odd Steiner-centroid ratios, and outer-area/pedal products for least period two modulo four with a separate centered odd extension. They concern different quantities or restricted least-period classes. Their entire separate proofs have not been reviewed here.

No global absence of earlier results, absolute firstness, independent discovery of the invariant, novelty of the triangular or negative results, human peer review, or proof-assistant certification follows. The six unavailable journal editions remain unavailable in the target's bounded audit; no stronger literature claim is adopted. The imported AMR record body itself was not independently retrieved, so this lane authenticates the displayed primary equality and the exact nonconstancy certificate without certifying every historical imported-record wording. There is no identified mathematical gap in the full literal Theorem 1 within its explicit elliptical-caustic/supporting-line/signed-area category. The limitations above concern evidence type, ancillary source custody, historical attribution coverage and execution mode, rather than an unresolved step in that theorem's proof.
