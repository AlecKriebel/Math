# Classical-priority and mechanism audit of PR #826

Date: 2026-10-15 UTC. Target: problem 30003060 / Solotar's OWR 2016/10 contribution, pp. 479–481. Supplied frozen head: `286cc67c0727b4decfd4f261a0591cd8823ebce9`. Candidate inspected: `../../source/author/PROOF.md`, SHA-256 `59efb88c21c7e62fd70fa06f7f5a0b59bc96672c70523bc5a1330b094c0a2bb3`.

## Finding

The positive-characteristic free-algebra obstruction is a fully assembled elementary corollary of classical tensor-algebra Hochschild calculations and the very definition of BLS higher Koszul homology. This is stronger than saying its “methods are classical”: the prior complex and exact operator already determine every block of the answer, with no remaining homological argument or unsupported bridge.

The inspected originals do **not** establish that someone previously stated this exact positive-characteristic higher-Koszul counterexample or explicitly disposed of Solotar's question. Those historical claims must be distinguished. The candidate already disclaims novelty and first priority, so it can accurately be presented as a newly written elementary application/correction to the literal unrestricted formulation. It should not be promoted as a new homology mechanism, a new substantial tensor-algebra theorem, or a resolution of the characteristic-zero converse.

## Exact claim and scope

Let k be any field, V a vector space with a basis, and A=T_k(V), with every generator assigned internal weight one. View A as the quadratic algebra T(V)/(0), and use coefficients A and BLS's fundamental degree-one Koszul cocycle e_A. For n>0, let E_n be the vector space on words of length n and let rho move the last letter to the front.

The audited assertion is

`HK^hi_1(A)_total=n = ker(q_n),  HK^hi_0(A)_total=n = coker(q_n),`

where `q_n : E_n^rho → (E_n)_rho` is the natural invariant-to-coinvariant map. All higher groups in homological degrees at least two vanish; the total-weight-zero higher H0 is k. On an orbit O of size d, q_n is multiplication by d. Consequently in characteristic p>0, each p-divisible orbit contributes one dimension in each of homological degrees zero and one. In characteristic zero, every positive-weight block is acyclic.

The word `x^(p−1)y` in two generators has orbit size p. It supplies a nonzero higher H1 class although T_k(kx⊕ky) is Koszul. Thus the literal unrestricted-field forward implication in the OWR question fails. This does not resolve any characteristic-zero converse.

## Constructive deduction from prior results

**1. Prior ordinary chain model, including assumptions.** Loday–Quillen (1984), §5, Lemmas 5.1–5.2, printed pp. 581–582, gives the free bimodule resolution of T(V) and its two-term Hochschild small complex

`0 → A⊗V --b→ A → 0,   b(a⊗v)=av−va.`

Their cyclic action on V^(⊗n) is explicitly unsigned. Over a field all required flatness hypotheses hold. Loday's 1998 second edition §§3.1.1–3.1.4, printed pp. 90–92, gives an explicit homotopy equivalence with the Hochschild complex, even for any base k-module V. Under concatenation `A_(n−1)⊗V ≅ A_n ≅ E_n`, the differential is `1−rho`. Hence `HH1(A)_n=E_n^rho`, `HH0(A)_n=(E_n)_rho`, and `HHj(A)=0` for j≥2. See [the original Loday–Quillen paper](https://www.sas.rochester.edu/mth/sites/doug-ravenel/otherpapers/loday-quillen.pdf).

For the quadratic presentation R=0, W0=k, W1=V, Wj=0 for j≥2. Thus its Koszul complex with coefficients A is this same small complex. Koszulness itself also has a direct check: concatenation `A⊗V→A` maps a basis bijectively to all nonempty words, so `0→A⊗V→A→k→0` is a linear free resolution. There is no relation-space exclusion or finite-global-dimension issue.

**2. Prior exact operator.** Goodwillie (1985), Theorem II.4.2 and formula II.4.8, printed p. 194, defines for a derivation D on a flat unital associative K-algebra

`e_D(a0⊗a1⊗...⊗aq) = (−1)^(q+1)(D(aq)a0)⊗a1⊗...⊗a(q−1).`

The ground ring K is commutative and this statement has no characteristic-zero assumption. This is the degree −1 Rinehart–Goodwillie cap operator. For the weight derivation D and q=1, its restriction to a small chain is `e_D(a⊗v)=va`, because D(v)=v. In HH0 the words va and av are equal. Therefore the induced map from invariants to coinvariants is exactly q_n. The sign in BLS, `(−1)^(q−1)`, agrees because its exponent differs by two. See [Goodwillie's original](https://www.sas.rochester.edu/mth/sites/doug-ravenel/otherpapers/goodwillie-free.pdf), not merely an analogy with de Rham theory.

**3. BLS identifies the named invariant.** BLS arXiv:1512.00183v1, §§5.1–5.2, printed pp. 19–20 (already 1 December 2015), explicitly identifies Hochschild derivation cap with e_D and defines the fundamental-cocycle higher Koszul differential in every characteristic. Their formula on a degree-one cycle is the class of av, equivalently va modulo commutators. The candidate's cited v3, pp. 17–18, has the same needed bridge. Thus the computation in steps 1–2 is precisely higher Koszul homology, with coefficients A, not an unrelated invariant. The char≠2 condition for an arbitrary derivation in §5.1 is bypassed by the explicitly unrestricted fundamental-cocycle construction in §5.2; in this two-term case the square is also zero for degree reasons. See [BLS v1](https://arxiv.org/pdf/1512.00183v1) and [v3](https://arxiv.org/pdf/1512.00183v3).

**4. Elementary orbit computation; no division hidden.** On a cyclic permutation orbit O, `ker(1−rho)` is generated by `s_O=sum_(w∈O) w`: equality of adjacent coefficients proves this over any field. The coinvariant quotient is generated by one [w]; the coefficient-sum functional is well-defined and takes [w] to 1, proving this generator remains nonzero even when p divides d. Hence `q_n(s_O)=d[w]`. There are no incoming degree-two groups and no higher boundary to remove the resulting kernel. The exact kernel and cokernel above follow orbit by orbit.

The sum of the p distinct rotations of `x^(p−1)y`, with each word split before its last letter to obtain a chain in A⊗V, is nonzero. Applying b telescopes; applying e_A-cap gives p times a single coinvariant class, hence zero. This completes the unrestricted-field counterexample using only the previously published complex/operator and BLS's definition.

## Euler cap, Connes B, and cyclic homology must remain distinct

Loday–Quillen Lemma 5.3, pp. 582–583, identifies **Connes B** with the norm

`N_n=1+rho+...+rho^(n−1) : (E_n)_rho → E_n^rho.`

In the bases [w] and s_O, an orbit O of size d has

| Map | Direction | Scalar |
|---|---|---:|
| Euler cap e_D, hence higher Koszul differential | invariants → coinvariants | d |
| Connes B | coinvariants → invariants | n/d |

The second scalar occurs because n rotations list every distinct word n/d times. Both compositions are multiplication by n. This is exactly the induced Cartan identity `e_DB+Be_D=L_D` in Goodwillie II.4.2/Corollary II.4.3 (or Loday Corollary 4.1.9), because L_D acts by total weight n.

This distinction is falsifiable in the smallest relevant blocks. In characteristic p, the primitive length-p orbit of `x^(p−1)y` has Euler cap zero but B an isomorphism. The orbit of `x^p` has size one and has Euler cap an isomorphism but B zero. Thus nontrivial de Rham homology, nontrivial cyclic homology, and nontrivial higher Euler-cap homology cannot simply be substituted for one another. Merely observing the failure of division by n in the Cartan identity would not prove the candidate's result; the orbit-size calculation does.

There is also an integral formulation of the classical Euler-cap complex. For a free abelian V, each positive-weight orbit gives the block `Z --d→ Z`; its homology is zero in degree one and Z/d in degree zero. Reduction to characteristic p gives one-dimensional kernel and cokernel precisely when p divides d. This is a deduction here from the original integral small-complex/operator formulas; it is not represented as an explicitly located earlier theorem about “higher Koszul homology over Z.”

## Priority assessment

Three separate findings are supported:

1. **Classical consequence:** the entire candidate calculation is forced by Loday–Quillen plus Goodwillie plus the BLS definition. All hypotheses, signs, operators, and the orbit computation are written above. No novel central lemma is needed.
2. **Explicit earlier exact resolution:** none was identified in the inspected primary passages or the bounded query set. The older works predate the named invariant. BLS v1 itself considers T(V) and computes higher **cohomology** on pp. 28–30; this is not evidence of the exact higher-**homology** obstruction. It is inappropriate to call an older cyclic/TC theorem the identical resolution without proving the operator bridge.
3. **Current manuscript wording:** the candidate makes no novelty or first-priority claim and excludes the characteristic-zero converse. The right description is an elementary characteristic obstruction, transparently derived from classical machinery. Adding Loday–Quillen/Goodwillie/Loday as explicit prior-mechanism credit would make that provenance clearer.

If an `already_solved` gate means “an identified earlier source explicitly states the same resolution of the question,” this lane has **not** established that gate. If it also includes elementary consequences completely determined by established results, then this lane establishes such an inherited-result issue and the work should not be counted as a newly discovered substantial theorem. The mathematical counterexample remains valid either way; the policy classification must not silently change the meaning of historical priority.

## Coverage, checks, and exact remaining gaps

The main anchors were read in original full texts and version/page/hash pinned in SOURCE_LEDGER.md. QUERY_LEDGER.md records 25 verbatim focused public queries, inspection limits, failed retrievals, and stopping rule. The original Loday–Quillen p. 582, Goodwillie p. 194, and BLS v1 p. 20 were visually checked. Rinehart's original was unavailable from the attempted AMS endpoint (HTTP 403); no exact uninspected Rinehart theorem is used. Hesselholt's selected 1997 circular-word/free-algebra sections confirm broader classical necklace arithmetic but concern Witt/THH/TC, with no inspected identical Euler-cap higher-Koszul assertion.

An independent small operator check is included in `check_operator_blocks.py` and `OPERATOR_CHECK.json`: it expands cap and Loday's cyclic derivative directly on words and checks their different orbit scalars, boundary cancellation, and the Cartan product over integers, with explicit characteristic-p contrast examples. The algebraic proof above supplies the unlimited result; finite computation is a control only.

Diagnostic-interface repair, 2026-10-15 04:30 UTC: the first accepted script, output, and decision are preserved byte-for-byte under `historical_v1/`, with a README and SHA-256 manifest. The current script replaces removable Python `assert` acceptance statements with explicit `need` checks that raise errors under ordinary and optimized Python. No mathematical expression changed: `replay_operator_blocks.py` normalizes only guard syntax/helper code and verifies identical syntax trees for the computational content. It executes disposable copies in normal and `-O` modes, verifies that their acceptance JSON is byte-for-byte and semantically identical to the preserved original output, and verifies identical standard output. A separate disposable mutation changes the expected Euler scalar from d to d+1; both modes reject at that check before writing an acceptance file or printing a success summary. The accepted `OPERATOR_CHECK.json` is unchanged. `REPLAY_RECEIPT.json` records the commands' modes, statuses, output hashes, exact failure reason, and source hashes. This repairs the portable diagnostic interface only; it does not alter or extend the prior normal-mode algebraic evidence or the proof.

Exact remaining historical gap: identify an earlier primary text explicitly writing the same positive-characteristic higher-Koszul obstruction or an earlier response to the literal OWR question. This lane does not claim exhaustive worldwide novelty, present openness of the characteristic-zero question, human peer review, or formal proof-assistant certification. No outreach, Git mutation, queue mutation, PR update, or release was performed.
