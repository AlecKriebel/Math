# Independent acceptance audit: robust polynomial interpolation

Problem 2508 / EP-1133, rank 1037. Review date: October 8, 2026 (UTC).

## Verdict

**Accept the exact mathematical deduction, relative to the explicitly imported Bernstein interpolation theorem and standard analytic and measure-theoretic results. No unresolved mathematical gap was found. No correction to the frozen proof report is required.**

This is an independent review of a prior argument, not a new solution announcement. The April 29, 2026 draft and the authored verification have both been checked. The original ergodic extraction works; the verification report's reverse-Fatou replacement also works. Neither a finite computation nor the manuscript's public status label is being used as a proof.

The disposition is `PRIOR_SOLUTION_VERIFIED_RELATIVE_TO_IMPORTED_THEOREMS`. New solution approaches: zero. This audit does not establish journal acceptance, community consensus, human expert certification, effective constants in C, or proof-assistant formalization. The full proof of the imported interpolation theorem has not been independently reconstructed.

## Exact statement and provenance

The target is: for every C > 0 there are epsilon > 0 and n0 such that, for every integer n >= n0 and every indexed list of n points of [-1,1], some real labels of absolute value at most one force every complex polynomial with degree < (1+epsilon)n and interval norm <= C to disagree at more than epsilon n indices. Equivalently, agreement at at least (1-epsilon)n indices forces norm > C. Multiplicity is retained throughout.

The original question on printed page 72 of Erdős's survey has the same order of quantifiers and the same strict degree and norm thresholds, with distinct ordered nodes. The candidate covers the stronger indexed formulation. I inspected the original page visually, including its last paragraph. Its first page prints 1968; the archival filename contains 1967. This is a bibliographic difference, not a change of mathematical scope. [Original survey](https://users.renyi.hu/~p_erdos/1967-20.pdf).

The candidate's title page says draft manuscript, dated April 29, 2026, and gives no named author. Public attribution is through Przemek Chojecki's posting, which names GPT-5.5 Pro assistance. Direct forum retrieval failed during this audit; an indexed forum result supplied that posting. This is provenance evidence only. [Candidate](https://www.ulam.ai/research/erdos1133.pdf), [public discussion](https://www.erdosproblems.com/forum/thread/1133).

The available AI-contributions index expressly stops at June 30, 2026 and lists EP-1133 as a candidate full solution. Its classification neither certifies nor refutes the argument. No claim about later consensus is warranted. [Dated index](https://github.com/teorth/erdosproblems/wiki/AI-contributions-to-Erd%C5%91s-problems).

## 1. Imported theorem and normalization

The required import is the necessity direction of Ortega-Cerdà and Seip, Theorem 1, for entire functions of exponential type at most tau bounded on the real line. For a real separated interpolation set, its upper uniform density is strictly below tau/pi. The original theorem page, its definitions, and the necessity section were inspected; the theorem page was also rendered. The university repository identifies the article as Journal of Functional Analysis 162 (1999), 400-415. [Repository record](https://diposit.ub.edu/items/5a79a097-d5af-48bd-8946-5354f8fd442f), [accepted manuscript](https://diposit.ub.edu/bitstreams/bbe5243b-6094-4096-b939-b6692a19f366/download), [DOI](https://doi.org/10.1006/jfan.1998.3357).

Here is the hypothesis match, independently checked:

- The paper's weighted boundedness condition on interpolation data becomes ordinary boundedness when all nodes are real.
- On the real line its distance is d/(1+d). A positive lower bound for this distance is equivalent to an ordinary positive gap.
- The two-sided Carleson sum is zero for real nodes.
- Every horizontal strip of positive height contains the whole real set. The outer strip-height limit is therefore vacuous.
- Passing among open, closed and half-open counting intervals costs at most two points, hence no asymptotic density. For half-open intervals the supremal count is subadditive in the interval length. The standard subadditivity argument, using local count bounds for the remainder, identifies the resulting limit with the limsup convention used in the draft.
- The convention is exponential type tau, not Fourier frequency measured in cycles. In particular P(cos z) for degree m has frequencies among the integers from -m through m and has type at most m. The interval length pi in angular coordinates and the critical density tau/pi fit exactly; there is no extra factor of two.

Only necessity is used. A non-strict density inequality would not suffice for this argument: the extracted intensity can equal the critical value exactly.

## 2. Negation of the finite local obstruction

For fixed C >= 1 the desired local assertion has quantifiers

    exists eta > 0 and L >= 1;
    for every indexed L-tuple of diameter <= pi(1+eta)L;
    exists real unit-bounded data;
    no norm-C element of B1 fits every entry.

Its negation allows an independent choice of a universally C-interpolable tuple for every prescribed pair (eta,L). Thus eta_k = 1/k and L_k = k+2 are legitimate simultaneous choices. Repetitions are impossible in such a tuple, since opposite labels at equal arguments cannot both be fitted. Translation gives a set U_k with endpoints 0 and T_k, cardinality L_k, and T_k <= pi(1+eta_k)L_k.

The growth estimate |f(x+iy)| <= C exp(|y|), followed by Cauchy's derivative estimate on a unit circle, gives |f'(x)| <= eC. Assigning opposite unit labels to any selected pair and integrating along the real segment forces a uniform gap delta = 2/(eC). This works for complex-valued interpolants. It follows that T_k >= delta(L_k-1), so T_k tends to infinity.

The draft instead uses the classical Bernstein derivative inequality and gets delta = 2/C. That is valid, but the weaker Cauchy bound already establishes everything needed and avoids a further specialized import. For C < 1 the local assertion is immediate with L=1 and label 1. The value C=1 is included in the nontrivial argument.

## 3. Compact configurations and stationary averaging

Represent a delta-separated closed set by its counting measure and include the empty set. The mass of any compact interval is uniformly bounded. Subsequence compactness on an exhausting sequence of intervals produces vague convergence. Separation prevents two unit atoms from coalescing and prevents fractional limiting atoms: a sufficiently small neighborhood of a surviving atom can contain only one approximating atom. Points may escape, explaining why the empty configuration must be allowed. The resulting configuration space is compact and metrizable.

Translation is continuous in this topology. For a continuous compactly supported test function phi, the sum N_phi over the configuration is continuous and uniformly bounded. These observables are used before passing to the weak limit; discontinuous interval counts are not erroneously treated as continuous.

Let nu_k average U_k-t over 0 <= t <= T_k. Weak compactness gives a probability limit nu. Translation by a fixed s alters the averaging interval only at its ends, and the difference against a bounded observable is at most 2|s| times its bound divided by T_k. Therefore nu is stationary.

The first-moment measure is locally finite by the same separation bound and is translation invariant. Hence it equals I times Lebesgue measure. To bound I from below, choose nonnegative phi supported in [-R,R]. Each point of U_k outside the two end intervals contributes the full integral of phi to the translate average. There are at most 2(1+R/delta) exceptional points. Their loss divided by T_k vanishes, whereas

    L_k/T_k >= 1/[pi(1+eta_k)].

Consequently I >= 1/pi. No hypothesis that the points are uniformly spread throughout the finite interval is needed; separation is exactly what controls the possible endpoint loss.

## 4. All support configurations inherit interpolation

Fix a configuration Lambda in the support of nu. Every open neighborhood of Lambda has positive nu measure. Portmanteau makes its nu_k measure positive for all sufficiently large k. A nested countable neighborhood basis therefore gives an increasing subsequence k_j and actual translation parameters t_j for which U_kj-t_j tends vaguely to Lambda.

Fix any finite subset of Lambda and any real unit-bounded labels on it. Disjoint small neighborhoods around its finitely many points, together with separation, provide distinct approximating points of the translated U_kj. Transfer the chosen labels to the corresponding original nodes and extend them arbitrarily to the other nodes. Translating the norm-C interpolants back gives entire functions with the uniform strip bound C exp(|Im z|).

Montel supplies a locally uniform subsequential limit. The strip bound persists, so its type is at most one and its real-line norm at most C. Values at the moving interpolation points converge to the prescribed labels. This works for every finite label pattern on every support configuration. There is no exchange of an uncountable family of almost-sure statements.

Every separated set is countable. For any one bounded real data sequence on an infinite support configuration, successively interpolate longer finite prefixes and use Montel again. Each prescribed value is eventually fixed, so the limit fits all entries. Scaling handles arbitrary real sup norm. For complex data, interpolate its real and imaginary parts separately and combine the two functions as f+ig. Their own values away from the nodes need not be real. The resulting complex interpolant has norm at most twice C times the data norm, and type at most one.

Thus the precise complex-data interpolation hypothesis of the imported theorem is established on every infinite configuration in the support, with finite configurations harmless.

## 5. Density contradiction: both routes checked

### Reverse-Fatou route in the verification report

For positive integers r define A_r(Lambda) as the number of points in [0,r), divided by r. These are Borel measurable and bounded by 1+1/delta uniformly in r. Their expectations are exactly I. This follows from the stationary first-moment measure; possible atoms at the interval endpoints have zero expected count.

Set H = limsup A_r. A finite configuration has H=0. An infinite support configuration has H <= D+ < 1/pi by the imported theorem. The support has full probability because the configuration space is second countable. Applying ordinary Fatou to the common upper bound minus A_r yields

    I <= integral H dnu < 1/pi.

The final inequality does not require a uniform density gap. The measurable function 1/pi-H is positive almost surely; a nonnegative function that is positive almost everywhere under a probability measure has positive integral. This contradicts I >= 1/pi. The direction of reverse Fatou and the strictness of the last step are both correct.

### Original ergodic route

Ergodic decomposition applies to the continuous real translation action on the compact metrizable configuration space. Component intensities are bounded and average to I. Among the components with full measure on the support of nu, at least one has intensity at least 1/pi: if all were smaller almost surely, their average would also be smaller.

The continuous-parameter ergodic theorem applies to the bounded Borel observable counting [0,1). Its time average is the component intensity almost surely. Integrating this moving unit-window count differs from the count in [0,R] by at most the number of points in two intervals of length one. Separation makes that error uniformly bounded, so division by R removes it. A typical configuration in the selected component is therefore infinite, lies in the support, and has one-sided density at least 1/pi. Its upper uniform density is at least that value, contradicting interpolation.

This is a valid use of ergodic theory. The report correctly lists these imports, and its alternate route does not rely on them. The manuscript's phrase about using one external theorem can only mean one specialized interpolation theorem; ordinary analytic and ergodic results are also used.

## 6. Global angular blocking and strict arithmetic

Choose the local eta,L depending only on C, and put q=(1+eta)L. Choose

    0 < epsilon < min(1/2, eta/[2(1+q)]).

Then a=(eta-epsilon)/q-epsilon is positive. Any integer n0 greater than (1+1/q)/a suffices for the block-count estimate. This is explicit in the local constants but gives no explicit functions eta(C), L(C), or n0(C).

For n >= n0 set D=ceil((1+epsilon)n). Sort the indexed angles arccos(x_i) in [0,pi], retaining multiplicities, and split them into floor(n/L) consecutive full blocks. Their spans h_b have disjoint interiors and total at most pi. A good block has D h_b <= pi q. If B blocks are bad, each consumes strictly more than pi q/D of the total span, so B < D/q, also trivially when B=0.

Consequently the number G of good blocks satisfies

    G >= floor(n/L)-D/q
      >= n(eta-epsilon)/q-1-1/q
      > epsilon n.

The unit floor and ceiling losses have both been included. The last strict inequality is the reason for the stated n0. It is not replaced by a non-strict count or an asymptotic assertion with unspecified sign.

In each good block, multiply angular offsets from its first node by D and apply the local obstruction to those indexed nodes. The chosen labels are fixed before any tested polynomial. Put zero on the remaining indices and undo the sorting permutation.

For a polynomial P of degree m < (1+epsilon)n, its angular function Q(z)=P(cos z) is a finite sum of integer-frequency exponentials of maximal frequency at most m, hence has type at most m. Its real-line norm is exactly P's interval norm. Since m<D, the rescaled function Q(alpha+u/D) lies in B1, with type strictly below one and the same norm bound. Thus P cannot fit every label in a good block. The zero polynomial is covered as well by the same type-zero observation, regardless of one's degree convention for it.

Disjoint good blocks force more than epsilon n missed indices. Accordingly fewer than (1-epsilon)n indices can be fitted. Equal nodes may belong to different blocks or appear repeatedly within one block; the local obstruction is indexed, and missed indices are counted only once because the blocks are disjoint. Nodes at -1 and 1 are ordinary angular endpoints. No real-coefficient restriction has been introduced.

## 7. Reproducibility and adversarial controls

The frozen original was not edited. Its archive is 17,247 bytes and contains exactly 16 ordinary files. Every member was compared byte-for-byte to the reviewed local counterpart, without extracting unsafe archive paths. All 15 payload identities listed in its frozen metadata matched.

The supplied controls were rerun using the independently pinned original verifier. They passed in normal, -O and -OO modes, with identical output. Finite coverage is 80 parameter choices, 400 exact large-n arithmetic cases and 15,192 block-pattern cases. These are finite checks, not a certificate of the universal analytic theorem.

**The author's 90 hostile rejections decompose exactly as 28 supplied bundle mutations times 3 modes = 84, plus 2 separately recorded source mutations times 3 modes = 6.** The two source categories are incomplete source groups and wrong PDF bytes. They are not additional cases inside controls.py.

The independent harness added 25 case categories, each run in all three modes, for 75 rejected invocations. Some categories intentionally overlap the author's controls, so these are not 75 new distinct threat classes. They include exact Boolean/integer distinctions, forbidden JSON floats and non-finite constants, malformed rational data, duplicate claim keys, incorrect record and source digests, all-or-none source groups, same-size altered PDF bytes, source swapping, symlink/missing/directory source arguments, and a wrong external manifest pin. It also detected substituted verifier bytes through the independent verifier pin without executing the substituted code.

Full-source replay matched all five external file hashes and sizes, selected exactly one record for 2508/EP-1133, matched its canonical record digest, and confirmed absence of EP-1133 from the supplied research corpus. The whole-source run had identical outputs in all three Python modes.

An actual nonroot process (effective UID 1000) replayed relocated copies of both the public bundle and all five source files after making them read-only. Four attempted writes, covering new and existing files in both trees, were denied. All three execution modes then passed with identical output, and both byte inventories were unchanged. This is stronger than merely setting mode bits while running as root.

### Exact trust boundary and optional hardening

The verifier uses explicit checks rather than assert statements for its decisions. The fixed manifest authenticates the complete payload, including descriptive metadata and the verifier itself. The caller must authenticate the verifier *before executing it* using an external trusted digest; an untrusted program cannot authenticate itself. The supplied control driver and this audit did that. External pins copied from an unknown bundle are not independent trust roots.

The direct interface is an identity verifier with selected semantic checks. It is not a complete generic validator of all descriptive source fields under an arbitrarily replaced trust root. Specifically, changing SOURCES.checked_utc to a Boolean and deliberately supplying the newly computed manifest digest is accepted; the same modified bundle is rejected under the reviewed fixed digest. Numeric fields used by the arithmetic, claims and identity checks do enforce exact types, and JSON floats and non-finite constants in bundle metadata are rejected globally. Whole source corpora are parsed less restrictively only after whole-file pins match, because legitimate corpus data may contain floats.

No malformed-input bypass under the reviewed pins was found. No patch is necessary for the documented frozen interface. If a future version advertises full schema validation independent of identity, inexpensive exact-key and exact-type checks for checked_utc, source pages, descriptive strings and lists should be added, with a newly reviewed manifest. That broader claim is not made here. No semantic check in these programs establishes the truth of prose, source acceptance, or the analytic imports.

## 8. External identities and publication boundary

Original archive SHA256:

    74b4b17367e5926f3fcf35307e8dff9c0d8cd37923b20066d31fe8bdfb1c9203

Original public manifest SHA256:

    97185d9d301079510b35dcc78944f1f536c10e34f4de5222aadf474093b1b15d

Original verifier SHA256:

    14733b9582625d2cdecc12312832a3af5b1f4737646088a54b7f4b9c8586af8d

Original frozen metadata SHA256:

    baf6e1ac604e413d3b5872f6874769846e03e0c73fcca631377a4fdd5d4b2176

Replayed external inputs:

- problems.json: 68,931,837 bytes; SHA256 04128381e42a5e312326d74adb0947ee02062ade70229e02d3060ac4ef9942cf.
- research_results.json: 80,334,822 bytes; SHA256 8da848d31c20eb4eecaa07702eced4724aa4a89f877c2a0774d9f3138389aa6b.
- Candidate PDF: 270,595 bytes; SHA256 193d41758154227673ccd0587a2e99d8464dbcc2aaa27da1f3daf202c10bd164.
- Density theorem PDF: 322,604 bytes; SHA256 ea6d4e6651e82a548ab64e70539e9df773ce1c38a9e5d6b011388c421d2505cd.
- Original survey PDF: 1,033,560 bytes; SHA256 a2bdb2f9e42b1f08d1a6d3500335f6d6a8d5de717dee94af1814cb6103f28c44.
- Canonical selected record: SHA256 bdb5a77c1ac83485add7ad62ca037ffaf8649e60a102f9941921c5c1a6c50414.

These authenticate the supplied frozen bytes. Web inspection independently checked the cited public mathematics and dated status information; this audit does not claim a fresh downloaded byte hash of every current URL.

The original source-free allowlist is the 16 members enumerated in evidence/archive_review.json: the seven public payloads, their public manifest, six evidence files, EXTERNAL_PINS.json and FROZEN_METADATA.json. The independent supplement's allowlist is enumerated in its own manifest. Publication may include only the authored mathematical review, audit scripts, and identity/replay metadata on those lists. Exclude source PDFs, text extractions, rendered source pages, dataset contents, local input paths and private coordination material. This audit performed no publication, queue mutation, or external outreach.
