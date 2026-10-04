# Independent torsion-kernel/direct-group-law audit

## Scope and conclusion

The full kernel computation passes this family's independent mathematical checks. The residual polynomial, both ordinate signs, exact kernel converse, all-fiber inverse denominators, marked subgroup, and infinity identification are supported by fresh checkable artifacts, not by a package PASS label. The strongest extra certificate is the exact, fully symbolic identity

\[
\operatorname{disc}_x(\psi _5)=5^{11}\Delta_\beta^{22}.
\]

This was computed on the full Tate family, rather than inferred from a test curve or an unverified homogeneity argument. Together with the independently derived chord-law iff proof and the two exact resultants, it supplies a separate direct 25-point count.

The theorem counts points on the smooth normalization. At the allowed parameter \(\lambda_v=-(13+5r)/2\), two distinct fifth-torsion points map to each of the five plane vertices. This is a real coordinate boundary, not a counterexample to the normalization theorem. It should remain explicit when presenting optional plane images. There are no extra poles on the twenty residual points.

This report does not certify the full division-field, priority, publication, or global plane-normalization claims. C004's kernel/formula part is closed here; its identification with the normalization of the entire plane curve still depends on the separate C003/global geometry proof. Equation transport itself was checked afresh here. Public program replay is conducted by the parent; this family certifies static body/proof/output consistency and independent mathematical outputs. No external communication, installation, Git/index/branch operation, candidate edit, release or publication seal was performed. The assigned folder is held for parent closure after its final inventory.

## Source-first independence and inputs

The root AGENTS.md was read. The AIM source was independently downloaded by native curl with actual argv, start/end UTC, full stdout/stderr, exit zero, HTTP 200, effective URL and byte count preserved under native/aim_source_fetch. Its SHA256 is `8b64d2f6b91f791c35afae10b2ef79c15a927a94c2142a56386f80c8b8a596e6`. The frontmatter and physical page 51 were rendered and read visually, and text was extracted. All four Question 17 remarks were read. They concern the known infinity subgroup, torsor/Sha motivation and the universal X1(5) twist, relation to the workshop, and nonregular/star variants. They do not provide a full-kernel proof.

SOURCE_ONLY_BASELINE.md was frozen before any candidate or parent assessment read, at `2026-10-04T12:41:52.186383+00:00`, SHA256 `5c49c377cc5ad729b749c11bfd090cd14b4a35015d32b35432b5b8529bca2927`. baseline-freeze.json records its hash and source artifacts. The baseline selected direct tangent/secant arithmetic, a converse via 3P=-2P, denominator checks, both branches, infinity identification, and singular plane-image collisions as distinct falsification mechanisms.

Only after that freeze were the current qualification_v03 manuscript TEX/PDF/deposit JSON and the parent's stable ledger read. The torsion pages 4-5 of the actual current PDF were rendered and visually inspected. public_consistency_v01 pins the candidate input hashes: TEX `3338be58c5c6250a826f2a2af772db5a3838dad1d45c6c4a847c62cc00b4f9df`; PDF `0325be9bc4b754ad1d94baadf2f1b88af587e9443b9d242a2d7af7b2dda79420`; deposit JSON `b4d99b620320f9a0a46eac60f9e61308cbc859364fadd632fd9976e9e942b863`; ZIP `e916946b6ffaaec2dae08b4a3622d19293d087ced789297ee38b86c671d76dab`.

The existing actual Morton v4 PDF independently retrieved by the parent was inspected at physical/printed page 5, including every residual coefficient, and page 6 text was read. This family does not claim a second network retrieval of Morton. Its PDF hash is `f745a7f8c45d8f8d419678009622a0c49fc2018ec92e3eda68fb5e304869f31e`. Every one of its eleven D5 coefficients under b=-beta was independently transcribed from the visual source and checked against this family's fresh derivation. Sutherland's actual lecture 5 text was also read at sections 5.5-5.6 and Theorems 5.8/5.25; the manuscript's standard degree/separability statement agrees, although the present direct count does not need that imported statement.

## Universal tangent/secant derivation

Work on the nonsingular completed cubic \(v^2=f(x)=x^3+Ax^2+Bx+C\), with origin at infinity. This is the generalized Tate equation after \(v=y+((1-\beta)x-\beta)/2\). A line of slope \(m\) intersects the cubic in three points whose abscissas sum to \(m^2-A\). The group sum is the reflection of the third intersection. At a finite point with \(v\ne0\), the tangent slope is \(f'/(2v)\), hence

\[
x_2=x(2P)=\frac{f'^2}{4f}-A-2x,
\quad D=x_2-x,
\quad Q_3=4f(3x+A)-f'^2=-4fD.
\]

The reflected doubled ordinate satisfies \(v_2/v=-1+f'(x-x_2)/(2f)\). Consequently

\[
H_6=16f^2\frac{v_2}{v}=2f'Q_3-16f^2.
\]

When \(D\ne0\), the secant through P and 2P has squared slope

\[
\left(\frac{v_2-v}{D}\right)^2=\frac{f'^2}{4f}+\frac{2f'}D+\frac{4f}{D^2}.
\]

Its Vieta formula gives \(x_2-x_3=D-2f'/D-4f/D^2\), and therefore

\[
Q_5=4fQ_3^2(x_2-x_3)
 =16f^2H_6-Q_3^3.
\]

direct_kernel_exact.py verifies these universal rational identities and expands Q3/H6 independently before Tate specialization. With \(b_2=4A,b_4=2B,b_6=4C,b_8=4AC-B^2\), their expansions are precisely the manuscript's displayed psi3 and H6. On the Tate family, \(A=(\beta^2-6\beta+1)/4,B=(\beta^2-\beta)/2,C=\beta^2/4\), so \(4f=T_\beta\). The degree-12 polynomial Q5 has leading coefficient 5 and is exactly \(x(x-\beta)R_\beta(x)\); every coefficient in all eleven residual rows matches.

The fully symbolic resultants, with the displayed order and constants, are

\[
\operatorname{Res}_x(Q_5,T_\beta)=\Delta_\beta^6,
\qquad \operatorname{Res}_x(Q_5,Q_3)=\Delta_\beta^8,
\qquad \Delta_\beta=\beta^5(\beta^2-11\beta-1).
\]

The independently computed discriminant is \(48828125\beta^{110}(\beta^2-11\beta-1)^{22}=5^{11}\Delta_\beta^{22}\). R(0)=5beta^8 and R(beta)=5beta^12 were also checked exactly.

These are identities in polynomial rings over Q, not empirical numerical samples. The resultant/discriminant degrees do not fall on a characteristic-zero specialization: leading coefficient 5 is fixed. Thus all these certificates apply to every nonsingular Tate fiber, including j=0 and j=1728. The equation transport and factorization of Delta_beta after the displayed lambda map were independently checked in extra_exact_checks.py; its only finite zero factors are lambda^5 and lambda+c, with denominator (lambda+5r)^7 and nonzero constants. Hence every allowed lambda yields a nonsingular Tate fiber without a hidden extra exclusion.

## Iff kernel and the 25-point count

Take a finite Q5-root on a smooth characteristic-zero Tate fiber. The resultant with T_beta gives v nonzero, so the tangent denominator is legitimate and 2P is finite. The resultant with Q3 gives D nonzero, so 2P and P have different abscissas and the secant denominator is legitimate; 3P is finite. The direct identity then gives x2=x3. On this cubic two finite points with equal abscissas are equal or negatives. Equality 2P=3P implies P=O by cancellation, contradicting finiteness. Thus 3P=-2P, which proves 5P=O. This does not assume the polynomial is already the fifth division polynomial.

Conversely, if P is a nonzero fifth-torsion point, v cannot vanish: v=0 would make P a 2-torsion point, and orders two and five are coprime. If Q3 vanished, x2=x; then 2P=P or 2P=-P, forcing P=O or 3P=O. Either contradicts nonzero fifth torsion. Therefore the tangent and secant formulas apply. As 3P=-2P, their abscissas agree and Q5=0. This proves the converse without circular use of a kernel oracle.

The nonzero exact discriminant shows Q5 has twelve distinct roots. The resultant with T_beta shows each has two distinct ordinates. Completing the square gives exactly the two signs in the manuscript, \(y=(-((1-\beta)x-\beta)\pm\sqrt{T_\beta(x)})/2\); both solve the actual Tate equation. Hence the iff argument gives 24 distinct finite fifth-torsion points and the origin, directly. Removing the two distinct marked abscissas x=0,beta (whose residual evaluations are nonzero) removes four points and leaves ten simple residual roots and twenty distinct normalization points. There is no reliance on finite samples to prove this universal claim.

## Marked points, infinity subgroup, and inverse charts

For P0=(0,0), beta is nonzero on all smooth Tate fibers. The tangent is y=0; the third intersection is (beta,0), whose generalized negation is (beta,beta^2). Thus 2P0=(beta,beta^2). The secant from P0 to 2P0 has slope beta and gives 3P0=(beta,0)=-2P0. As P0 is not O, it has exact order five. The four listed points are its four distinct nonzero multiples. extra_exact_checks.py checks the symbolic Vieta/negation calculations; finite_direct_control.py independently executes them on every tested finite fiber.

Put e=gamma-alpha, a nonzero constant in K. The inverse expressions after xi=q(x-beta) reduce exactly to

\[
z=\lambda\frac{-\alpha x+\gamma\beta}{x-\beta},
\quad z+\gamma\lambda=e\lambda\frac{x}{x-\beta},
\quad a+4rt=4r(z+\gamma\lambda),
\quad \frac Y\delta=\frac{k v(-\alpha x+\gamma\beta)}{20e x(x-\beta)}.
\]

For every allowed finite lambda, q,k,a3,lambda,e,r,d are nonzero. R roots have x neither zero nor beta. All displayed inverse denominators are therefore nonzero at all twenty residual points, including the allowed cuspidal plane member. No restriction is introduced by z=0: it is an inverse numerator zero, not a pole. Forward rational charts at a plane node may fail to distinguish branches; the smooth cubic coordinates retain the point.

Taking limits of X/Y at the two marked abscissas with their nonzero completed ordinates yields the exact images

| Tate point | Plane infinity slope X/Y |
|---|---|
| O | 0 |
| (0,0) | r/delta |
| (0,beta) | -r/delta |
| (beta,0) | -delta |
| (beta,beta^2) | delta |

Since (r/delta)^2=5-2r, these are exactly the five source infinity slopes. Their homogeneous equation is \(2X(X^2-dY^2)(X^2-(5-2r)Y^2)=0\). At Y=1, the plane X partial is 10 for slope zero and 160+80r or 160-80r for the other two squared slopes; none is zero. Thus all five infinity points are distinct, smooth, and K(delta)-rational. This explicit map identification closes the possible gap between two unrelated order-five subgroups.

For the rotation argument itself, writing Z=X+iY,W=X-iY makes rotation act as (Z,W)↦(zeta Z,zeta^-1 W). The terms Z^5+W^5 and the radial terms of P, as well as Q, are invariant. Rotation cycles the five infinity lines and induces an automorphism of order five on the normalization. Decompose this automorphism as a translation followed by an origin-fixing automorphism. On a nonsingular characteristic-zero short Weierstrass equation an origin-fixing automorphism has x↦u^2x,y↦u^3y; its coefficient conditions give u^4=1 when the x coefficient is nonzero or u^6=1 when the constant coefficient is nonzero. Nonsingularity ensures at least one applies, so there is no nontrivial origin-fixing automorphism of order five. The linear part of rotation is therefore trivial, and rotation is an exact order-five translation. This agrees with, and is no longer needed to infer, the direct marked-image identification.

## Singular plane-image duplicates

The inverse numerator z vanishes at x=phi*beta. Exact substitution gives X=1 and Y=0 for both ordinates. The kernel and branch evaluations there factor as

\[
R_\beta(\phi\beta)=\beta^8(56+25r)
 \left(\beta-\frac{11-5r}{2}\right)^3
 \left(\beta+\frac{2+5r}{11}\right),
\]

\[
T_\beta(\phi\beta)=\frac{3+r}{2}\beta^2
 \left(\beta-\frac{11-5r}{2}\right)(\beta+\phi).
\]

The singular Tate value (11-5r)/2 corresponds to lambda=infinity and is not an allowed finite fiber. The nonsingular residual zero beta_v=-(2+5r)/11 corresponds to lambda_v=-(13+5r)/2, and has T_beta(phi beta) nonzero. Hence the two normalization points are distinct fifth-torsion points with the same plane image [1:0:1]. Their parameter differs by -1/4 from the allowed plane cusp parameter, so this is a nodal event. Rotation sends the pair to the other four plane vertices while preserving fifth torsion, giving five pairs of duplicate images. Assuming the independently established whole-plane normalization with precisely the five vertex singularities, the 25 normalization torsion points then have 20 distinct plane images. The manuscript explicitly counts the normalization and preserves cubic/Tate coordinates, so no false 25-distinct-plane-image assertion was found.

## Finite implementation controls

finite_direct_control.py was written independently on the uncompleted generalized Tate equation. It enumerates curve points first, uses line intersection and generalized negation, and computes 5P=(2P+2P)+P. This is the torsion oracle; R is only a prediction compared afterward. Across primes 19,29,59,71,79,89,101,109 it checks 532 nonsingular beta fibers and 44,308 affine points. Every rational kernel matches x(x-beta)R=0; every kernel abscissa has both distinct ordinate branches; all marked signs match. Thirty tested fibers have all 25 torsion points rational (12 over F71 and 18 over F101). Rational finite-field counts of 5 versus 25 are kept separate from geometric characteristic-zero counts.

Where r and delta exist in the base finite field, the implementation transports residual points to W, checks the actual cubic equation, checks all inverse denominators, and substitutes their plane coordinates into the actual quintic. There are 360 such residual-point inverse checks over F101. Some other chosen primes lack delta or have no rational residual points; their zero inverse counts are not claimed as coverage. The p=101,lambda=83,beta=62 fiber exhibits exactly five plane-image collisions at rotated vertices, corroborating the separate universal collision calculation. The coefficient mutant is detected on 220 fibers; dropping an ordinate branch is detected on all 532 fibers. These controls are implementation evidence and falsifiers, not substitutes for the universal algebra/proof.

## Public proof/code/output and portability consistency

The actual extracted qualification_v03 archive's four exported programs were inspected against the current v03 directory and the historical original files. The archive and v03 program bytes match exactly, and each original byte count/hash and exported hash matches its PORTABILITY entry. The four entries and program bytes are unchanged across public v01,v02,v03.

For division_chord.py, division_model.py and division_finite.py, removing the declared optimization guard leaves the historical original byte-for-byte. For division_quintic.py the only further change is the declared coefficient read path: original native/independent_generic_chord_final.stdout is replaced by packaged expected/division_chord.json. The exact diff is in native/public_consistency_v01/stdout.bin. Guards reject -O/-OO before scientific assertions could be disabled.

division_chord.py genuinely starts with generic chord arithmetic and compares all residual rows/resultants. Its optional discriminant check evaluates the single nonsingular cubic v^2=x^3+1 only for the constant; its output explicitly says a separate homogeneity/separability proof is required for the exponent. SUPPLEMENT.md supplies that universal argument. Neither code nor output silently upgrades one sample to a universal discriminant computation. This family strengthens that certificate by a fresh exact full-Tate discriminant.

division_model.py checks full equation transport, discriminant and inverse-pole identities. Those tasks are appropriate algebraic checks; it explicitly leaves plane normalization and the full-level modular interpretation to separate proofs. The generic transport and pole identities were independently reconstructed here. division_finite.py uses the actual uncompleted Tate group law and enumeration; its 138 fibers/6,112 affine points and boundary/mutant claims are finite evidence. Its scope text and the supplement correctly limit them. Every generic psi3/H6 expression, all thirteen generic fifth-kernel coefficients, and all eleven residual coefficients in the packaged expected record match this family's fresh Vieta derivation exactly.

division_quintic.py is a conditional factor identity against a supplied independently derived coefficient record, not a standalone fresh division-polynomial derivation. Its emitted `input` wording still says “own direct chord/tangent native coefficient record”; PORTABILITY and README explicitly disclose the packaged-record rebinding. verify.py freshly executes division_chord, compares its complete mathematical JSON to that packaged record (only interpreter provenance removed), and does so before running the quintic checker. Thus full-suite use reconstructs and validates the coefficient dependency; direct standalone quintic execution needs that dependency qualification. Parent fresh replay remains the evidence for actual public program exit/output reproduction.

## Stable claim ledger

| ID | Family status | Evidence and exact boundary |
|---|---|---|
| C004 | VERIFIED kernel/formula component; CONDITIONAL plane identification | Fresh iff proof, exact full-Tate discriminant/resultants, both branches, marked maps and inverse-domain proof. Whole-plane normalization is C003, assigned to geometry family. No division-field conclusion follows from this row. |
| C031 | VERIFIED | Symbolic uncompleted Tate tangent/secant law and exact five-order argument; direct finite controls check signs on all 532 fibers. |
| C032 | VERIFIED coefficient identification | Actual existing Morton v4 p5 visually read; all eleven old D5 rows under b=-beta match freshly derived R exactly. No first-priority inference or independent Morton network retrieval claimed. |
| C033 | VERIFIED | All eleven residual rows match direct generic Vieta-derived Q5 factor. |
| C034 | VERIFIED | Completing-square identity and Res(Q5,T)=Delta^6 prove both ordinate signs solve the curve and stay distinct. |
| C035 | VERIFIED for required polynomials | Generic Q3/H6 expansions and Q5 secant numerator reproduce displayed psi3/H6/psi5 and x(x-beta)R. No claim of verifying every general n recurrence. |
| C036 | VERIFIED | Direct tangent/secant derivation tracks only f and Q3 denominators; generic identities and all exported coefficients agree. |
| C037 | VERIFIED universally | Exact symbolic resultants Delta^6 and Delta^8, with constants/signs as displayed. Fixed leading coefficients prevent specialization loss in characteristic zero. |
| C038 | VERIFIED universally | Exact residual evaluations 5beta^8 and 5beta^12, nonzero on all allowed fibers. |
| C039 | VERIFIED universally | Full forward and converse group-law argument above, with denominator exclusions and equality-versus-negation distinction. |
| C040 | VERIFIED universally | Exact disc(Q5)=5^11 Delta^22 and degree12/leading5 directly prove twelve simple abscissas and 25 points using C039. Standard degree/separability theorem also agrees with actual cited lecture. |
| C041 | VERIFIED universally, with explicit plane-image caveat | All inverse denominators nonzero for residual roots. Allowed node fiber lambda_v produces duplicate plane images; W/Tate points remain distinct. |
| C042 | VERIFIED | Exact infinity factor/slopes, nonzero plane partials, sqrt(5-2r)=r/delta, explicit marked images. |
| C043 | VERIFIED conditional on global normalization extension | Rotation invariance/order and no-origin-fixing-order5 argument are sound. Direct marked image calculation independently identifies the subgroup; global extension uses C003. |

No assigned route is blocked by a transferred central difficulty. The only outstanding dependencies are explicitly outside this family's scope: whole-plane normalization C003, arithmetic/full-level and priority/source claims beyond C032, and parent's actual extracted-package replay. PASS labels in prior review/gate files were not used as proof.

## Native evidence, failures, and hold

Every substantive execution in native/ has execution.json recording real native start/end UTC, exact argv/cwd, exit, stream hashes and executed program hash when applicable, plus full stdout.bin/stderr.bin. Successful mathematical executions are kernel_exact_v01 (12:43:53–12:43:54 UTC), map_boundaries_v03 (12:47:27–12:47:30), finite_direct_v01 (12:48:46–12:48:47), public_consistency_v01 (12:51:37), and extra_exact_v02 (12:53:51–12:53:52). Source rendering/extraction and failed-body preservation commands have their own actual receipts. Current successful bodies and every failed body remain available.

Three reviewer implementation failures are preserved, with their original bodies copied before corrections:

1. map_boundaries_v01, exit1 at 12:45:47 UTC: initial expected infinity-slope sign was wrong. The actual algebra indicated the opposite sign; the failed body is map_boundary_exact.failed_v01.py.
2. map_boundaries_v02, exit1 at 12:46:59 UTC: correct sign still appeared nonzero because cancel did not normalize the algebraic constant expression. Adding exact simplification resolves the false negative; map_boundary_exact.failed_v02.py is preserved.
3. extra_exact_v01, exit1 at 12:53:31 UTC: literal leading coefficient 5 was a Python integer without a .subs method. Converting it to an exact symbolic integer fixes the programming error; extra_exact_checks.failed_v01.py is preserved.

These were implementation/expectation failures, not candidate mathematical counterexamples. No timestamp or stream was reconstructed. All mathematical success claims have exit-zero native receipts with empty stderr. The independent baseline remains unchanged. EVIDENCE_INVENTORY.json records final artifact hashes and scopes; HOLD_INVENTORY.json is a parent-closure inventory, explicitly not a publication seal. Completion estimate for this assigned independent kernel audit: 100%; project discovery/publication approval is not implied.
