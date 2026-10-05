# Independent adversarial audit: refined slippery bounds

Problem identifier: 30002129. Supplied descriptor: OWR-12007-009, rank 714.
Audit date: 2026-10-05 UTC.

## Verdict

**PASS for the frozen, explicitly unresolved five-route investigation. No substantive mathematical correction is required by this audit.** The retained partial arguments are valid in their stated scopes, the three countercontrols refute the intended shortcuts, the exact finite computations independently reproduce, and the release has the supplied immutable binding. The full refined slippery conjecture remains **unsolved by this investigation after 5/5 substantive approaches**.

This verdict does not certify a solution, novelty, priority, exhaustive literature coverage, global current openness, formal proof-assistant verification, or human peer review. The finite test counts are diagnostics, not proofs of an infinite statement. The original release is preserved unchanged; this audit is a separate artifact. No remote write or helper delegation was performed.

## 1. Exact immutable object audited

- Author release manifest: 1,451 bytes; SHA-256 `4396be5d06045d5f619dbded61846c83008b2ea6d578a2d913273f136f691c22`.
- Author archive: 19,090 bytes; SHA-256 `1cc570a6030395b0e4e3677d9c492cd8f0ab11402479f51053f0438d50b879eb`.
- Retained mathematical report, RESULT.md: 16,332 bytes; SHA-256 `fe94159e5a771003f316ed1d310a665beab6ec6a79d8858057f53687b5116ea1`.

The auditor independently checked all nine manifest-listed files, the manifest itself, the exact ten-member flat ZIP inventory, regular-file types, absence of duplicate ZIP names, and byte equality of each ZIP member to its release counterpart. The full listing and hashes are in EXACT_BINDING.json. The original release and archive were re-read after the corruption tests and remained unchanged.

The external handoff digests are the trust anchors. A package cannot authenticate replacement of both its verifier and its externally supplied digest. The author accurately discloses this limitation.

## 2. Source and target verification

### Original mathematical question

The publisher's Oberwolfach report, printed pp. 2173–2174, defines R using real translation numbers of specified lifts and displays the refined bound on p. 2174. The auditor regenerated text from the supplied PDF and visually inspected that page. Calegari–Walker, section 3.7, printed p. 19 of the inspected arXiv PDF, explicitly requires p/q to be reduced. That page was separately rendered and visually inspected.

The target is consequently the following. For a positive cyclic word containing both generators, with alternating block pairs a^(alpha_j)b^(beta_j), j=1,...,m, put A=sum alpha_j and B=sum beta_j. If the supremal value R(w,r,s)=p/q is reduced, then

0 <= R(w,r,s)-Ar-Bs <= m/q.

The lower inequality follows from the rigid-translation representation. There are m pairs and 2m individual blocks. The denominator is the output denominator of the supremum; it is neither an input denominator nor an arbitrarily chosen unreduced denominator. The report handles pure powers separately, where the defect is zero.

Lifts commute with T(x)=x+1. Central integer shifts give R(w,r+j,s+k)=R(w,r,s)+Aj+Bk. This preserves the defect and the reduced output denominator, so normalization of the inputs to [0,1) is legitimate. Discarding the integer part of the final translation number is not. Rightmost-letter-first composition agrees with the primary source. Cyclic conjugacy preserves translation number.

### Prior special case and source limitations

Chowdhury's 2018 dissertation, Proposition 6.2.2, printed pp. 39–40, explicitly assumes that the reduced denominator of R equals the reduced denominator of one input. The coprimality conditions are visible in the displayed proposition. It does not prove the general refined bound. The auditor inspected regenerated text and a newly rendered p. 40. The author's full-period averaging proof supplies the needed justification without adopting the dissertation proof's unsupported-looking equal-gap shortcut or its inconsistent displayed notation.

The inspected source PDFs' sizes and hashes agree with SOURCE_VERIFICATION.json. SOURCE_CHECKS.json records the auditor's own inspection scope and public URLs. Public arXiv and university landing pages were also read; the publisher PDF was independently accessible through the web tool. Fresh public retrieval byte equality is not asserted merely from those web views.

The exact live catalogue page remained unavailable in the auditor's web attempt. Therefore the mathematical formulation is primary-source verified, while the catalogue identifier/rank association is the supplied descriptor association. The author-recorded HTTP 403 is historical retrieval metadata, not a new independently observed HTTP status in this audit. Raw AI corpus records remain absent and uninspected. No source PDF, extract, image, raw corpus record, or private coordination file is included in this audit package.

Primary references:

- Calegari, joint with Walker, “Ziggurats and rotation numbers,” Oberwolfach Report 35/2012, pp. 2173–2175: https://doi.org/10.4171/OWR/2012/35 ; publisher PDF https://ems.press/content/serial-article-files/46404
- Calegari and Walker, “Ziggurats and rotation numbers,” Journal of Modern Dynamics 5 (2011), 711–746: https://arxiv.org/abs/1110.0080 ; PDF https://arxiv.org/pdf/1110.0080
- Chowdhury, “Self-similarity of Ziggurat Fringes and Rigidity of Extremal Free Group Actions on the Circle,” dissertation (2018), Proposition 6.2.2: https://knowledge.uchicago.edu/records/phhzj-0mw78 ; DOI https://doi.org/10.6082/mzm4-8k43

## 3. Argument-by-argument adversarial review

### Route 1: conjugacy averaging and the global m bound — PASS

For a lift F, the displacement of F^n has oscillation at most one, since F^n preserves order and commutes with integer translation. Its minimum and maximum bracket n*tau(F): iterate F^n and divide by the number of iterates. Thus the asserted uniform displacement error at most one is valid.

The average h_K of the functions F^i(x)-i*tau(F) is continuous, strictly increasing, and degree one. Hence it is an onto homeomorphism, not merely a weakly monotone map. Its telescoping identity is correct. Conjugating F makes each displacement lie within 1/K of r. Simultaneous conjugacy preserves tau(G), because the conjugacy differs from the identity by a bounded periodic function.

Each a block contributes at most alpha*(r+1/K). Each b block contributes at most beta*s+1 by the same displacement estimate. Composing pointwise displacement inequalities, then taking translation number and K to infinity, proves R-Ar-Bs<=m for every real r,s. The rigid representation gives nonnegativity. This proves the conjectural bound when the output denominator is one. Replacing w by w^q multiplies the block count by q and yields no improvement after division. The report correctly stops there.

### Route 2: exact ab formula and powers — PASS

The exact product formula is a credited theorem, Calegari–Walker Theorem 3.9, rather than something established by the finite program. The floor formulation is equivalent to the source's rational-candidate formulation.

Let C=R(ab,r,s)=c/d, reduced, and E=C-r-s. If E=0 there is nothing to prove. If E>0, each candidate of denominator k exceeds r+s by at most 1/k. Thus all k>2/E lie uniformly below C, and the supremum is attained in a finite set. For a maximizing k, d divides k, and E<=1/k<=1/d. No unjustified assumption of attainment for a general infinite supremum is used.

For (ab)^m, translation-number homogeneity gives R=mC. Its reduced denominator is d/gcd(d,m), and the bound mE<=m/d<=m/q follows. Integer shifts extend the argument to all real inputs. The proof does not manufacture roots of arbitrary lifts, treat distinct appearances of a as independent maps, or induct by adding uncontrolled output denominators. It covers precisely the advertised power family and cyclic conjugates.

### Route 3: full-period averaging — PASS, with the essential denominator hypothesis retained

For rational input denominators N,V, the positive-word model theorem permits maximizing over disjoint finite X/Y orders. These are monotone step maps used to compute the supremum, not homeomorphisms claimed to realize the same step dynamics literally.

If the output denominator is N, a reduced N-cycle at an X phase occupies all N X residues. At every intermediate phase, distinct cycle points remain distinct; any collision would persist under the remaining word and contradict the cycle. After every a block all X points occur again. The b outputs must occupy distinct X gaps, because the following a block would otherwise collapse them.

A monotone degree-one bijection from all X indices to all gap indices is an integer shift i -> i+l. This is why the same l applies at every start within that phase. With t_i the numbers of Y points in successive X gaps, the b-hop yields a gap-count inequality for each start. Summing over all N starts counts every gap exactly l times and gives l*V<=N*beta*U. This step works for unequal gaps, including zero gaps; it does not require all t_i to be equal.

The following a block shifts the X index by l+1+alpha*P. Summing over the m phases gives C=AP+sum(l_j+1), and division by N yields the claimed m/N defect bound. The symmetric input case follows by swapping a and b.

For a real second input, fixed rational first input bounds all possible output denominators by N. Right continuity and this discrete range give a constant interval to the right. Rational approximants inside that interval preserve the same output C/N, allowing the rational proof to pass to the limit. The relevant dependencies are Calegari–Walker Lemmas 2.14, 3.3, 3.4 and the proof of Theorem 3.7. No lower-left continuity is substituted for this right-side argument.

The independently reconstructed oracle checks 584 configurations with full X-period and 1,114 full-period phase averages in the bounded family. One nonuniform-gap example is w=abb, r=1/4, s=2/5, gaps (1,1,1,2), with model value 5/4. These checks support implementation consistency; the written counting proof supplies the general special case.

### Route 4: non-full orbits and failed local replacement — PASS as a reduction, not as a solution

Tracking an actual closed q-cycle through mq phases yields exactly

cN=qAP+mq+sum l.

Every full gap crossed before the b endpoint contributes to the weighted inequality. Substituting the identity into the proposed m/q bound gives exactly the retained missing inequality

sum l <= qNB(U/V)+m(N-q).

There is no missing factor q or N. The weighted sums control sum M_h*t_h and do not by themselves control the unweighted sum M_h. For a proper subset of X, the constant-shift property from Route 3 is unavailable. The report explicitly leaves this global extremal-orbit problem unresolved.

The counterexample to the independent-phase estimate is valid. With gap counts (1,1,1,1,96), N=5, V=100, U=beta=1, starts X_0,...,X_3 each skip one full X gap. Their endpoints occupy distinct gaps. The total 4 exceeds the proposed 6/5 bound. With P=1 the following a-hop has image residues {0,1,3,4}; these are not the starting residues {0,1,2,3}. Hence this configuration does not establish a closed four-cycle and is not a counterexample to the conjecture.

The audit independently checks the closure identity and its exact equivalence to the missing inequality on every one of the 47,700 bounded configurations. This verifies the finite reduction arithmetic, not its universal inequality.

### Route 5: slippery limits and the half-rotation dihedral case — PASS with all limits kept distinct

For a slippery point, a monotone rational sequence from the strict lower-left quadrant is cofinal there and its R values tend to L. Each value is rational, bounded, and strictly below L. If the reduced denominators failed to tend to infinity, infinitely many values would belong to a finite bounded set of rationals. A repeated value along an infinite subsequence of the monotone sequence would force the limit to be attained, contradicting slipperiness. Therefore the denominator-divergence argument is valid.

Assuming the refined bound at all rational inputs then makes the defect tend to zero, proving the qualitative slippery equality. The assumption remains explicit. At a nonslippery rational pair, enlarging an attaining lower pair to a rational lower pair preserves the attained supremum by monotonicity, so the lower-left value is rational. This is not a quantitative finite-q result.

For the half-rotation case, the rotation-conjugate interpretation of L is a cited theorem (Calegari–Walker Proposition 3.15 at rational inputs). Such lifts satisfy f^2=g^2=T. With c=fg^(-1), the identity gcg^(-1)=c^(-1) holds exactly, so tau(c)=0. Rewriting a word as c^k*g^ell is justified by gc=c^(-1)g. For even ell, g^ell is central translation by ell/2. For odd ell, (c^k*g)^2=T, giving translation number 1/2 before the remaining central shift. Thus L(w;1/2,1/2)=(A+B)/2. No commutativity of f and g is assumed.

The report correctly does not identify L with the pointwise R or infer that the half-rotation pair is slippery for every word. As an extra control, the independent product formula gives L(ab;1/2,1/2)=1 but R(ab,1/2,1/2)=3/2. For all diagonal t<1/2 sufficiently near the target, R(ab,t,t)=1: the k=1 candidate gives one, while for even k the floor sum is below one and for odd k it is at most one. This explicitly rules out conflating the lower-left value with right continuity. The seven sequence evaluations in the audit are a diagnostic illustration of this exact distinction.

## 4. Exact countercontrols

### Output versus input denominator

The product formula gives R(ab,1/5,1/5)=1. The actual reduced output denominator is one, and the defect is 3/5. Replacing it with either input denominator would falsely require 3/5<=1/5. Both implementations reproduce the exact value.

### Supremum versus an arbitrary representation

The piecewise-linear f is continuous, strictly increasing, degree one, and has slopes 5 and 1/5. Its branches agree at 1/6, and it fixes zero. Its stated inverse is correct. For g=f^(-1) composed with translation by 2/3, g fixes 1/6 because f(1/6)=5/6. Therefore both input translation numbers are zero, whereas fg is exactly translation by 2/3.

Using that nonextremal product's reduced denominator three would falsely require 2/3<=1/3. The actual supremum is R(ab,0,0)=1. This refutes only the variant that drops extremality. The fixed points establish real translation number zero, not merely rotation zero modulo integers. The exact PL identities are independently checked on all affine pieces and period translates; the algebra, rather than a sample alone, justifies the global identity.

### Phase averages without closure

The 4>6/5 counterexample above has distinct selected starts and endpoint gaps but fails the necessary closed-orbit condition. It refutes the local auxiliary estimate only. NEGATIVE_CONTROLS.json separates these mathematical controls from the independent file and archive corruption tests.

## 5. Computational audit and reproducibility

### Author replay

- Normal strict inventory, mathematical replay and six mutation tests: PASS.
- Mathematical output: byte-identical to the frozen MATH_CHECKS.json, reporting 23,189 explicit checks.
- Direct `python3 -O` mathematical replay: byte-identical.
- `python3 -O` bundle verification, replay and mutation tests: identical to the normal bundle output.
- Fresh relocation to a temporary directory, invoked with an unrelated working directory: identical output.

The bundle's subprocess does not inherit optimization automatically merely because the parent verifier is optimized. This audit therefore ran verify_math.py under -O directly as well. The author uses explicit RuntimeError-based guards, so its checks are not removed by Python optimization.

### Independent implementation

The new independent_controls.py does not import author code. It enumerates weak compositions of V into N gap counts; constructs blockwise maps on lifted X indices using cumulative Y counts; examines every X-start orbit; and checks monotonicity, degree one, closure, minimal period, phase injectivity, weighted gap counts, and the exact orbit identities. This is structurally different from the author's XY-site tables and reversed letter-by-letter map composition.

It reconstructs the same 10 rational inputs with reduced denominator at most five, 12 words, 1,200 word/parameter cases, and 47,700 configuration evaluations. These counts include rooted orders that can be cyclic rotations of one another; they are not a claim of that many distinct cyclic necklaces. All finite refined-bound tests pass. The maximal recorded q-times-defect is six, attained at r=s=0 for the six-pair word abaabbabbbababaab, matching the author summary.

The independent run executes 1,350,916 exact guard evaluations, many of which are repeated invariants across the finite configurations. That larger count is not a stronger universal proof. It also runs under -O with byte-identical results. All arithmetic is integer or Fraction arithmetic.

A separate comparison harness deliberately loads both completed implementations. It checks every corresponding configuration value, all 1,200 maxima, 1,200 reversal identities and 1,200 generator-swap identities. All pass. The search for a nonextremal step-model violation in this same bounded family also independently returns none, consistent with the author; this is not a universal absence claim. The canonical 1,200-case stream agrees exactly: 79,328 bytes, SHA-256 `0b9d8d2c756673a940dde489421a25532a41f6b46eb38dd82a2bb2525643fa08`.

For rational r,s, the exact product formula can be truncated at lcm(input denominators): its candidate there is r+s+1/L, while every k>L has value at most r+s+1/k. This supplies a valid finite oracle for the cross-check. The combinatorial enumeration equals the homeomorphism supremum only through the credited positive-word theorem; neither implementation independently proves that theorem.

### Integrity countertests

The auditor-owned binding verifier independently rejects changed file, missing file, extra file, extra directory, symlink, and changed manifest. Its ZIP checks additionally reject changed member contents, extra members, and duplicate member names. These tests use temporary copies only. They supplement, rather than merely relabel, the author's six-corruption replay.

## 6. Five-route count, dependencies, and residual limitations

The five routes are substantively distinct: averaging conjugacy, exact product formula/powers, full-period counting, non-full-orbit combinatorics, and limit/dihedral structure. The fourth is a failed extension of the third but develops a different global obstruction, an exact reduction, a concrete refuted auxiliary estimate, and a separate exact oracle. It is not simply a repetition or an extra source lookup. The log accurately reports five approach families rather than five independent solutions or five chronological chat turns.

All retained partials and obstacles are present. No failed route is hidden. No finite test is promoted to a proof. The source model theorem, exact ab theorem, fixed-rational-input right continuity, and rational lower-left rotation-conjugacy theorem are credited dependencies. The general proper-subset extremal-orbit inequality remains unproved. The report conservatively leaves general real-parameter passage among the remaining work rather than silently applying the fixed-rational-input special-case argument everywhere.

The supplementary literature check was bounded; no later general solution was identified in the inspected primary material and narrow search. No statement that the conjecture is globally open as of this date is warranted. The author's repository-search record was read as dated metadata; this audit does not independently certify absence of other branches, attempts, private records, or unindexed literature.

**Required corrections: none identified.** Preserve the unsolved disposition, the five-route count, the credited special-case scope, and every stated access and evidence limitation when describing or publishing these artifacts. Do not replace those qualifications with a claim that the conjecture has been proved or that 23,189 (or 1,350,916) finite checks constitute such a proof.
