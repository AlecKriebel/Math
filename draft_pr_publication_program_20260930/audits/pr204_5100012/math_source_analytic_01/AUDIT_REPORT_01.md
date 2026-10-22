# PR204 / 5100012: source and analytic audit

## Verdict and exact boundary

**Mathematical PASS for the explicit least-physical-period theorem in ROOT_SOURCE_FIRST_CONTRACT_01.md.** I found no missing analytic transition for a>b>0, a proper confocal elliptical caustic 0<lambda<b², and least N>=3 that is odd or divisible by four, including every admitted coprime star winding and either orientation. The areas are the signed shoelace areas of the original orbit and the ordered origin-to-original-side-LINE feet.

Two qualifications are material. The source table does not literally say “least” or “primitive”; the theorem uses an explicit necessary interpretation of N. An unrestricted repeated-list reading is false, with a rigorous obstruction below. Also, original numerical/exact PASS counts are conditional on assertions being enabled. Their enforcement fails under Python optimization. This tooling limitation does not invalidate the written universal proof.

This is a mathematical/source audit, not a novelty, effort, publication, merge, or human peer-review certificate. No original bytes were changed. No Git/ref/index/branch/checkout command, external contact, publication/tracker mutation, installation, dependency copy, new fulltext, or PDF rendering was used.

## Independence and actual access

The frozen attack plan was written at 2026-10-16T09:48:15.828740+00:00, SHA256 `12c931101f0b5300407ddb456d4c2e7d3595f552420ac2115227f07463987590`. Before it, I read the contract, custody receipt, primary access manifest, and primary RGK arxiv pages1–6 and journal pages341–346. I did not read the original proof, favorable review, Root proposed route, or other campaign/family reports before the freeze. A directory listing exposed only the Root-route filename, not its content.

After the freeze I attempted a combined extraction of the Chavez/Stachel PDFs; that tool output truncated. Next I read the original source_record/SOURCES/PROOF, then reread the relevant published theorem/proof inputs in bounded page batches. Stachel pp1610–1616, including the complete Theorem4.3/equation4.9 proof, were read directly. Chavez's flag-curve/area setup and complete Theorem6/proof on p104 were read directly. I then checked DLMF directly, read the remaining original native source/code/metadata except the favorable review receipts, developed the explicit residue calculation below, and only then consumed the original favorable FINAL_REVIEW and its source/hash receipts. All20 original native files were inspected. No Root proposed-route file or new/prior203/new204 family report was read. Root later sent a matching coefficient calculation after mine had already been communicated to Root.

The pre-proof elementary chord route in the frozen plan remains **partial as an independently discovered proof route**. It anchors the geometry but did not independently produce the full universal invariant before the submitted proof was read. The present complete result is an adversarial audit and independent derivation of its critical residue, not an independent rediscovery claim.

## Primary source and credited inputs

RGK arxiv2004.12497v11, introduction/Section2/Section3.3/Table3, and the final journal DOI10.1007/s40598-021-00174-y, pp341–346, agree on the confocal ellipse setting, signed shoelace area, original-side pedals, M=O, and A*A_M with N not2mod4. Neither table literally prints a least/primitive qualifier. Historical “?” and imported OPEN-TRIAGE are not current priority evidence. The archived source_record is preserved as historical data.

[Stachel, DOI10.1007/s40879-021-00524-2](https://doi.org/10.1007/s40879-021-00524-2), Theorem4.3/equation4.9 and proof, supplies exactly the caustic-eccentricity modulus, parametrization (-a sn w,b cn w), physical step2v, and coprime turning number. It is not restricted to turning number1. Its real ellipse-caustic domain matches the claim. **The displayed dn real-shift sign on printed p1613 is a typo**: dn(w+2K)=dn(w), not -dn(w). The submitted proof uses the correct identity; this audit verifies it directly from [DLMF22.4 Tables1–3](https://dlmf.nist.gov/22.4), rather than relying on the typo.

DLMF was read directly: [22.2](https://dlmf.nist.gov/22.2) for meromorphy, parity, simple orders and real values; [22.4](https://dlmf.nist.gov/22.4) for periods, zeros, poles and shifts; [22.8](https://dlmf.nist.gov/22.8) for addition formulas; [22.13](https://dlmf.nist.gov/22.13) for derivatives. All use modulus k; the numerical library receives parameter k². These inputs justify the submitted Jacobi facts, including the crucial imaginary anti-period and reflection identities.

[Chavez-Caliz, DOI10.1007/s40598-020-00154-8](https://doi.org/10.1007/s40598-020-00154-8), Theorem6, printed p104 (Theorem3 in its introduction), is about a Poncelet polygon and its **tangent-outer polygon**, for even n and concentric conics in general position. It is not an origin-pedal theorem. Its proof already uses meromorphic area products, pole/zero cancellation and compactness. I did not import its conclusion for the pedal polygon or assume its scope extends there.

The methodological credit to [Akopyan–Schwartz–Tabachnikov, arxiv2001.02934v2](https://arxiv.org/html/2001.02934) is supported by direct reading of §§4–7: complex continuation with a bilinear dot product, cancellation between neighboring terms at infinity, and Liouville arguments precede this submission. Their Theorem3 is an odd-n tangent-outer **area ratio**. No origin-pedal theorem was identified in that paper. This is positive prior overlap in mechanism and neighboring results; it does not decide priority for the exact target. No external theorem of that paper is needed as an unverified logical premise of the submitted proof.

## Check of every analytic transition

### Physical chart, least order, and real geometry

Write caustic axes alpha,beta and k=sqrt(alpha²-beta²)/alpha, k'=beta/alpha. Strict a>b and beta>0 give 0<k<1. Since beta/b lies strictly in (0,1), there is a unique v in (0,K) with cn v=beta/b. Confocality then gives a=alpha dn(v)/cn(v). Stachel's step is delta=2v, so 0<delta<2K. The real map w↦(-a sn w,b cn w) parametrizes the ellipse once modulo4K: its derivative never vanishes and its Jacobi amplitude is strictly increasing. Consequently physical least period N is equivalent to N delta=4K tau with gcd(N,tau)=1 and 0<tau<N/2 after choosing orientation. This includes stars and rules out changing parity by repeating a shorter orbit.

The elementary pre-proof chord anchor is independent: for ordinary ellipse angles m-d,m+d the chord is n(m)·X=cos d, where n=(cos m/a,sin m/b); the origin foot is cos d*n/(n·n). Confocal tangency gives cos²d=1-lambda(n·n). This agrees with the submitted canonical tangent and ensures the object audited is an original-side projection.

In canonical coordinates, substituting the addition formulas shows n(u)·P(u±v)=1 for n=(-sn u/alpha,cn u/beta). The common denominator is 1-k²sn²u sn²v, and its remaining numerator equals that denominator. The caustic contact (-alpha sn u,beta cn u) is indeed on that line. For real u, n·n=dn²u/(alpha²k'²)>0. Thus Q=n/(n·n) is the stated foot. Its complex extension is bilinear, so it is meromorphic; a Hermitian denominator would destroy that premise.

### Original area and finite reindexing

The direct determinant of P(u-v),P(u+v) is 2ab sn(v)cn(v)dn(u)/(1-k²sn²u sn²v). The addition formula for dn(u-v)+dn(u+v) has the same denominator and numerator2dn(v)dn(u). After the shoelace factor1/2, summation counts each vertex dn exactly twice, giving

    A(w)=C_A S(w),  C_A=ab sn(v)cn(v)/dn(v)>0.

All real denominators are nonzero. As complex identities these are meromorphic equalities, so exceptional chart denominator zeros do not introduce a missing domain. This is an algebraic identity, not a generic numerical inference. The actual pedal phase is u=w+v, not w.

### Reduced torus and divisor of S

Let m=N for odd N and m=N/2 for even N, ell=2K/m. The order of delta modulo2K is m, since delta/(2K)=2tau/N. Its N residues have multiplicity N/m. Bezout gives ell as a period of S; reindexing gives evenness. Its other period is4iK' and its anti-period2iK'. Thus X=C/(ell Z+4iK' Z) is a valid compact torus; no assertion of a larger real primitive period is required.

At p=iK', exactly N/m summands have poles, all at real2K translates of p. Their residues are equal and nonzero. More explicitly dn(p+epsilon)=-i/epsilon+O(epsilon), so Res_p S=-i*N/m. The only other pole on X is3p with opposite residue. This remains true for every fixed0<k<1; no generic-modulus exception or residue cancellation is concealed.

At z=p+ell/2, the equality -z+ell+2p=z combines evenness, real periodicity and the imaginary anti-period to force S(z)=0. This point is not a pole; 3p+ell/2 is its second distinct forced zero. There are exactly two simple poles, so the elliptic divisor degree gives exactly these two simple zeros. The divisor of S(w)S(w+ell/2) is zero, hence this product is constant by compactness. It is positive on the real line. This part is complete; it does not transfer the problem to a conjectured cyclic identity.

### Pedal poles, collisions, and T

At the common sn/cn/dn poles, the numerator of Q has order1 and dn² order2, so Q extends and vanishes. Its only other possible singularities are the dn zeros r=K+iK' and their translates. These are simple zeros of dn with finite nonzero sn,cn, giving Q at most order2. DLMF shifts and parity give Q(2r-z)=Q(z), so its Laurent series at r contains only even powers.

At one singular index, the two oriented incident area terms combine as

    (1/2) det(Q(r+e), Q(r+delta+e)-Q(r-delta+e)).

The neighbors are holomorphic: real pole separations are multiples of2K and 0<delta<2K. Their difference vanishes at e=0 by reflection. An order2 pole times an order1 zero is at most simple. No determinant ever has two singular endpoints. For even N there are two singular indices, separated by m>=2. Grouping incident terms never counts an edge twice: an edge has only one singular endpoint. This explicitly covers m=2/N4. N3 has m=3 and no collision. In N4 the two neighbors happen to be zeros of Q, which strengthens rather than invalidates the estimate.

Q(u+2K)=-Q(u) and Q(u+2iK')=diag(1,-1)Q(u). Determinants give T period2K and anti-period2iK'; the closed cyclic sum gives perioddelta. Therefore T lives on the same X and has only the two permitted simple poles at r,r+2iK'. These match S(u+K), since p-K and r differ by2K, a multiple of ell. One residue match fixes a scalar; anti-periodicity matches the other residue. The difference is holomorphic on X, hence constant, and its anti-period forces that constant to vanish. This proves T=C_T S(u+K) even if a coefficient vanished. No nonzero-pedal-area assumption is needed.

### An explicit independent residue control and nonvanishing

The candidate does not require the scalar to be nonzero, but I derived it to attack hidden exceptional cases. DLMF quarter shifts give the exact identity

    Q(r+x)=(alpha/k) [cn(x)/sn²(x)] (dn(x),i).

Hence Q(r+e)=(alpha/k)(1,i)e^-2+O(1). Put h(x)=cn(x)/sn²(x). The incident residue is

    i(alpha²/k²) [h(x)(1-dn(x))]' at x=delta.

Using 1-dn²x=k²sn²x and the Jacobi derivatives,

    h(x)(1-dn x)=k² cn x/(1+dn x),
    [h(x)(1-dn x)]'
      =-k² sn x [dn x+k'²]/[1+dn x]².

Thus each singular index contributes

    -i alpha² sn(delta)[dn(delta)+k'²]/[1+dn(delta)]².

The N/m multiplicity is the same as for S(u+K), so

    C_T=alpha² sn(delta)[dn(delta)+k'²]/[1+dn(delta)]²>0.       (*)

Every factor is positive on0<delta<2K. There is no vanishing coefficient anywhere in the proper physical domain. At N4, delta=K and C_T=alpha² k'/(1+k')>0; the two incident singular indices give exactly the required multiplicity2. This exact computation independently checks the Laurent cancellation and the residue normalization without needing favorable-review assertions.

### Parity and orientation

The product is C_A C_T S(w)S(w+K+v). For odd N, (K+v)/ell=N/2+tau is a half-integer. For even N it is (m+tau)/2. If N is divisible by4, m is even and coprimality forces tau odd, giving a half-integer; if N=2mod4, both are odd, giving an integer. The target cases therefore have the constant half-period product. This is valid for every coprime winding, without a convexity assumption.

Reversal changes the signs of both areas and preserves their product. In the chosen orientation, A>0 follows from S>0; (*) gives A_O>0 as well. The proof did not discard possible signed zeros or divide by A_O; the additional residue calculation rules out actual zeros within this proper real domain. Absolute values of signed shoelace areas also have constant product. That does not authorize replacing signed star area by ordinary unweighted filled-region area.

The strict circular and caustic-collapse endpoints are excluded from this complex torus proof: at k=0 or1 the torus degenerates. The circular statement separately noted by the author follows from rigid rotation of regular star polygons. No hyperbolic/degenerate/nonconfocal, moving-point, or segment-clipping extension follows from the above reasoning.

## A necessary least-period qualification: rigorous failure of repeated-list reading

For any primitive N6 family with0<k<1, m=3 and the excluded parity gives

    A(w)A_O(w)=C_A C_T S(w)².

C_A,C_T are positive and S has genuine poles, so S² is nonconstant meromorphic. It cannot be constant on the real phase line, by the identity theorem. Listing each orbit twice produces a listed N12 polygon; both signed areas double and their product becomes four times this nonconstant function. Thus listed N12 without least-period enforcement is a false extension. This obstruction is analytic, not dependent on the numerical example.

For orientation only, a diagnostic example uses caustic(alpha,beta)=(1,0.6), k=0.8, v=K/3, outer axes approximately(1.0939772445350245,0.7461810849656032), lambda≈0.1967862115604448. At w/K=0.13 and0.41 the twice-listed product is approximately13.33775100064912 and13.30802132294185. No source bytes were altered to insert the missing qualifier.

## Code, counts, effort, and custody

The submitted author script and original review script were read fully. The author `ck` and numeric `num`, the review's lattice checks, and `assert_close` use bare `assert`. Extracted original-function controls reject false statements normally but accept and increment PASS counters under `python -O`. An actual in-memory mutation of the first symbolic contact identity (its zero polynomial required to equal1) raises `AssertionError: universal_chord_contact_plus` normally and exits0 with `{'universal_chord_contact_plus':1}` under optimization. Original bytes were preserved. Detailed receipts are in ENFORCEMENT_CONTROLS_01.json.

The numerical tests are high precision, not interval certificates. The symbolic local-cancellation control assumes the displayed even Laurent model; that finite algebraic check cannot establish the real Jacobi reflection property by itself. The written proof and the independent residue calculation do establish it. Similarly the thousands of finite rational-lattice cases corroborate, but do not replace, the general coprimality argument. Full unchanged author/reviewer reproduction and broad mutations belong to the separate reproduction family, not this audit.

My small independent script has187 explicitly enforced checks,21 parameter/winding cases at80digits, including N3,N4, near-circular k=1e-5, k=0.8 and near-collapse k=0.999, maximal stars, real chord-foot comparison with (*), and two-distance complex residue checks. It imports no author/reviewer modules, uses existing read-only runtime packages, and rejects a false sentinel with explicit exceptions. Normal and optimized outputs are identical except the recorded optimization flag. Maximum real coefficient-versus-direct-foot scaled discrepancy was about1.69e-80. These remain finite noninterval diagnostics. An initial wrong-parity diagnostic threshold1e-10 was too large near the circle, stopped the run, and was corrected to1e-60 at80digits; the test-design correction is logged.

The original self-reported one substantive author turn is consistent with its checkpoint/log narrative, and the shared contribution to k203,a is disclosed. I cannot independently authenticate a turn count, actual model, or actual effort setting from these files; metadata explicitly leaves actual_model_verified and actual_effort_verified null. Two native commits are not evidence of two mathematical turns or of a particular model/effort. Treat “1/5” as original author metadata unless separate trusted evidence verifies it.

ORIGINAL_BYTE_CHECK_01.json recomputes length/SHA256 for all20 original files,59343B, and matches every custody entry. Publication manifests and historical reviewer hashes are consistent with those bytes. The reviewed proof hash is `d1e04cf42d4358243365969487348887f3451f9b3fcef63b5215e7389af0e039`.

## Strongest verified result and exact remaining gap

The full stated least-period signed origin-pedal theorem passes this analytic/source audit. The stronger formula (*) is independently derived here and checks that no physical coefficient vanishes. The unrestricted repeated-list extension fails. No analytic gap remains identified for the exact contract domain.

Remaining work outside this audit is the parent's broad original-runtime/mutation reconciliation, bounded positive-priority investigation, and publication disposition. Published complex-cancellation methods and neighboring tangent-outer area theorems have already been encountered and must be credited. This audit does not certify novelty or claim that failure to encounter an exact prior theorem proves absence. The initial independent elementary route remains partial; the complete result here is an audited proof with a new independent residue check. Completion:100% of this source/analytic audit scope, not100% of historical-priority or publication goals.
