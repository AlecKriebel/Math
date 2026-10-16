# Source, scope and provenance adversarial review

Review family: exact-source reconstruction, quantifier matching, native provenance and complete original-checker reproducibility. PR 239 / 30001321 / OWR-4081-005. Intake head: `7f17eef77c52b2d9b2ec3ad0803c016267fa6496`. Review completed independently of the new mathematical closure reviewers. No communication with individuals or other shard chats; no Git, index, ref or provider mutation.

## Disposition

**PASS for source-domain coverage and original-packet reproducibility.** No mandatory source-scope correction or provenance failure was found. The candidate's positive theorem has the same d=1 model and quantifiers as the displayed 2009 source theorem would have at d=1; it is directed against the printed negative conjecture. This report does not by itself certify the full asymptotic proof, establish novelty, certify current priority, or authenticate the provider's remote head independently of the frozen intake.

The strongest verified statement of this review family is that the exact native theorem statement is correctly targeted, all 32 original bytes and their recorded nested links pass, all four primary PDF pins match independently retrieved full objects, and all four full unmodified original checkers reproduce their recorded output bytes. No counterexample within the candidate's stated domain was found. The remaining promotion gap for this family is the separate independent mathematical audit of all analytic ingredients and the closure. Priority is deliberately unclassified.

## Exact claim, hypotheses and success criterion

Choose one probability law for p, fixed independently of N, with 0<p<1 almost surely. Assign iid copies to every space-time site (s,x), s≥0, x∈Z. The quenched walk starts at zero and jumps ±1, with right-jump probability p_(s,x). Put mu_N^omega=P_omega(X_N∈·) and alpha_N=E mu_N^omega. For every deterministic sequence M_N→∞, every deterministic alignment of consecutive equal M_N-site intervals P_N, every epsilon>0 and every K>0, the asserted conclusion is

    P_env( sum_(I in P_N) |mu_N^omega(I)-alpha_N(I)| > epsilon )
        ≤ C_(epsilon,K,law) N^(-K)

for all sufficiently large N. The eventual threshold may depend on the chosen scale sequence. Constants are uniform in the deterministic alignment. Section 6 also treats consecutive real half-open intervals of a common real length M_N, intersected with Z.

Success requires every diverging scale, including subpolynomial and arbitrarily slowly diverging sequences. Convergence in probability, an N^(1/4) quenched-mean scale, or a tail estimate only for M_N≥N^gamma at a fixed gamma>1/4 does not suffice. An admissible falsification would require one fixed iid elliptic law, one deterministic diverging scale sequence, fixed positive epsilon and a tail that fails to be smaller than every inverse power along an infinite sequence.

## Independent source reconstruction

Before opening the old independent review verdicts, I fetched the full EMS source, rendered and visually inspected PDF pages 37 and 38, corresponding to printed pp. 2151–2152, and wrote `SOURCE_RECONSTRUCTION.md`. The verified object is Berger's contribution to OWR 38/2009, DOI 10.4171/OWR/2009/38, [official full report](https://ems.press/content/serial-article-files/46239).

Theorem 1 expressly has iid, nearest-neighbor, elliptic space-time RWRE in dimension 1+d, d≥2, every sequence M_N→∞, a partition into equal cubes of that side length, and faster-than-polynomial environment tails for the sum of absolute quenched/annealed cell-mass differences. The following Conjecture 1 denies the d=1 extension. The next remark imposes quantitative scale restrictions for an extension to ordinary RWRE satisfying (T'); it does not add those restrictions to Theorem 1. Page 2152 describes an exposure/bootstrap mechanism and a martingale inequality, without adding hypotheses to the stated source theorem.

The source's Z in a d-dimensional cube sentence is an apparent dimensional typography issue; at d=1 there is no discrepancy. The candidate correctly reads d as the transverse dimension. One directed coordinate is deterministic time, so the state is 1+1 dimensional in the source's notation and has one random spatial coordinate.

## Scope comparison and attempted mismatches

| Issue | Source and candidate comparison | Finding |
| --- | --- | --- |
| Dynamic versus static environment | Source refreshes a spatial environment after each step; candidate has fresh independent layers. | Matched. No claim about static RWRE. |
| Spatial independence | Source theorem explicitly says iid; candidate is iid at all (s,x). | Matched. Temporal refresh alone would be insufficient; see boundary example below. |
| Jump support | Source says nearest-neighbor and describes the annealed law as a biased simple random walk. In d=1 the ordinary transverse support is {-1,+1}, parametrized by scalar p. | Matched. Neither the source target nor the proof is a theorem for arbitrary finite-range kernels or a holding jump. Yilmaz–Zeitouni's explicit space-time support (1.2) independently confirms this standard convention. Relabeling time as the first versus last coordinate changes nothing. |
| Ellipticity | The source prints elliptic, without a common deterministic lower bound. Candidate uses 0<p<1 a.s. | Matched, and also includes the uniformly elliptic subclass. No inverse moment is assumed. |
| Parity | ±1 jumps fix endpoint parity at each time. | Retained by the half-difference chain and same-parity coupling. No span-one finite-range theorem is silently imported. |
| Equal intervals and alignment | A partition of Z into equal consecutive integer-length intervals is a translate of a single grid. | All deterministic integer alignments are included; the estimates are uniform in them. |
| Noninteger geometric length | The source does not explicitly restrict M_N to integer site counts. | PROOF §6 supplies the real equal-length grid interpretation by replacing M with M+1 in the point count. The convergence argument remains valid. |
| Unequal or selected intervals | The source asks for equal cubes. | Arbitrary unequal intervals and environment-selected partitions are not required by this source statement and are not asserted in the review disposition. |
| Scale rate | Every M_N→∞, without a lower rate. | The candidate's slow target scale appears only in rho(ell,M_N)→0; concentration uses the separate fixed polynomial auxiliary scale. No hidden choice gamma=gamma_N is made in the statement. |
| Law quantifier | One fixed law, then N→∞. | Matched. Uniformity over laws approaching arrow environments is false and is expressly disclaimed. |
| Sign of answer | The source conjectures failure at d=1. | Candidate asserts the positive analogue for every admitted law, thereby contradicting that conjecture if the proof passes. It does not claim to prove the negative conjecture. |

## Explicit boundary checks

These examples test interpretation of the assumptions, rather than replacing the main mathematical review.

**Merely elliptic can have no reciprocal moment.** For k≥2 give each of p=2^(-k) and p=1-2^(-k) probability 2^(-k). This is a fixed probability law with q=1/2, a=1/4 and delta=E[p(1-p)]=11/84. It has no positive common ellipticity constant and E[1/p]=infinity. The stated proof inputs still have q∈(0,1), delta>0. The exact geometric sums are checked in `check_source_domain_boundaries.py`; no lower-bound truncation or reciprocal-moment regularity is implicit in the source matching.

**Uniformity over changing laws is false.** At horizon N let the iid law put equal mass on p=2^(-N) and p=1-2^(-N), and take M_N=floor(N^(1/4)). Every fixed environment has a distinguished path that follows its locally preferred arrows with quenched probability at least 1-N2^(-N). Its endpoint lies in some M_N-site cell, whose annealed mass is at most M_N times the central binomial peak, O(M_N/sqrt(N)). Thus the coarse L1 distance is at least

    2[1-N2^(-N)-M_N binom(N,floor(N/2)) 2^(-N)] → 2

in every environment. The exact finite lower bounds at N=16,256,4096 are about 1.214,1.601,1.801. This triangular array is elliptic at each N but does not choose one fixed law, so it is outside the source and candidate. It explains why the law dependence of constants and thresholds is essential.

**Refreshing whole spatially correlated layers is insufficient.** Let p_(s,x)=xi_s for every x, with iid xi_s equal to 1/4 or 3/4. This has independent time layers and a fixed uniformly elliptic law, but not independent spatial sites. At frequency t/sqrt(N), every quenched endpoint characteristic function has modulus

    (1-(3/4)sin²(t/sqrt(N)))^(N/2) → exp(-3t²/8),

whereas the annealed modulus tends to exp(-t²/2). Their positive modulus separation lower-bounds the endpoint L1 distance. For equal cells M_N=o(sqrt(N)), replacing the exponential test by a constant on each cell costs at most 2|t|M_N/sqrt(N), so the coarse L1 distance also remains bounded away from zero. This provides a direct falsification of the broader interpretation “arbitrary spatial layers independently resampled in time.” The explicit iid hypothesis prevents that interpretation.

Pure random-arrow laws (delta=0), constant scales M_N≡1, and opposite-parity kernel coalescence likewise fall outside necessary hypotheses. Deterministic elliptic laws are allowed and give zero discrepancy, but the claimed theorem is universal and does not use this easy case as its solution.

## Historical provenance and reproducibility

`NATIVE_PROVENANCE.json` records every relative native path, byte length, SHA256 and canonical Git-blob SHA1 checked against INTAKE.json. Exactly 32 files exist in the frozen subtree. The 44 entries of TURN_1_MANIFEST, TURN_2_MANIFEST, FROZEN_MANIFEST and REVIEW_MANIFEST all match. The 24 author entries in old reviewed_hashes.json also match. The turn-2 earlier-manifest and budget links bind the exact turn-1 manifest; the old review binds the exact proof and frozen manifest. The three source_manifest pins match the first three old reviewed source pins, and the fourth pin and URL occur in the turn-3 source addendum. No hidden native source files or mismatched hashes were found.

The chronology is internally consistent: turn 1 gives ordinary expectation/probability convergence (25% snapshot), turn 2 gives the fixed polynomial-scale tail (40%), turn 3 claims all diverging scales (90% pending review), and the later old review states PASS. The unchanged turn-1 research log/continuity and older partial current-status files explicitly remain historical snapshots. PROOF's pending-review language is likewise its frozen author-stage language. None of the historical partial labels changes which exact proof the later review binds. Three substantive author turns of five are recorded; source retrieval is counted as zero turns.

The TARGET statement hash, review hash and revision are preserved native provenance fields. Their upstream generating documents are not separately present in the 32-file packet, so I do not claim to recompute those imported hashes or authenticate their originating revision. Directly inspecting Berger's primary source and the frozen target wording independently resolves the material mathematical scope.

I read all four original checker implementations before executing them. `replay_original_checkers.py` makes byte-identical script copies in separate fresh working directories and runs each complete unchanged loop under Python `-I -B`. The runtime was probed as Python 3.14.6 / SymPy 1.14.0. No downloaded source code was executed. All four exit 0 with no stderr, PASS and output bytes identical to their frozen receipts:

| Checker | Exact assertions | Receipt SHA256 |
| --- | ---: | --- |
| Author turn 1 | 486 | b24e7fbdbcea5a62967894f88410bbd41705edcc014c622516a8a354cc20d275 |
| Author turn 2 | 50,324 | 83535b37641ad3be183f91884b377e256ded1434aac01da9aacc4f2d02034959 |
| Author turn 3 | 17,148 | a7add66866ca039dba3f42797fb2fea39a820002e5cb89cc7814881ea0cd1a8e |
| Old independent checker | 31,888 | 471e3ff1aeb75d3b04ab3574a939e72d691c5f67117535af0d8277cdc8bce66e |

These total 99,846 exact finite assertions. They test finite identities, supports, dependencies and algebra. They do not prove limiting estimates or certify the asymptotic theorem. The replay uses an existing read-only scientific runtime from another audit; the path and version are recorded in EXACT_REPLAY_RECEIPT.json. `verify_provenance.py` reproduces the local 32-file and nested-manifest checks, and `--fetch-sources` optionally verifies all four PDF hashes directly in memory.

## Primary source pins and credits

All four full primary objects were independently fetched over HTTPS and matched their frozen SHA256 pins; byte counts and UTC fetches are in SOURCE_AUTHENTICATION.json:

| Primary object | Bytes | SHA256 |
| --- | ---: | --- |
| Berger, OWR 38/2009 | 591192 | 4642f579215a28b58adb465e3eb3f1512b6dde596505df5a64b3eaae69b86847 |
| Balazs–Rassoul-Agha–Seppalainen, rap.pdf | 423524 | b3df2347dab68baa430029ff0042159200c2c38bceeada1e5ba6b3a9df8433f0 |
| Yilmaz–Zeitouni 2010 | 393379 | e6e0480fabfdbab0507a71b708e54228f1cf7283ec82aceca26b8acc4106a92f |
| Joseph–Rassoul-Agha–Seppalainen 2019, walkers.pdf | 396866 | 6dfd26c58e1f8bbc5e45ba2bbcedf9d96fcb10d1356d65b0ae0c3596c92e5690 |

The [Balazs–Rassoul-Agha–Seppalainen manuscript](https://www.math.utah.edu/~firas/Papers/rap.pdf), Theorem 3.1 and §4, supplies established quenched-mean fluctuation and difference-chain context. Its later span-one assumptions are not imported into the candidate's periodic ±1 proof. The [Yilmaz–Zeitouni paper](https://link.springer.com/content/pdf/10.1007/s00220-010-1119-3.pdf), model (1.2) and Theorem 1.5, concerns uniformly elliptic space-time large-deviation rate functions. Ballistic rare-tail rate comparisons do not settle fixed-epsilon coarse-L1 concentration in the central mass. The [2019 Joseph–Rassoul-Agha–Seppalainen chapter](https://www.math.utah.edu/~firas/Papers/walkers.pdf), model (1.1)–(1.5), Theorem 1.1 and §2, has bounded finite-range iid kernels, a span-one hypothesis and particle equilibrium/matching-coupling results. It is broader in jump support but has different hypotheses and conclusions; it is not an all-scale endpoint-tail theorem being assumed here.

Replica, exposure and coalescing-coupling methods have prior credits. This review classifies neither novelty nor current priority. Full PDF copies, extracted text, rendered pages, raw provider output and copied replay scripts were temporary reading/replay materials and are removed before the public authored manifest is sealed. Only authored summaries, deterministic audit/replay scripts and receipts remain in this folder.
