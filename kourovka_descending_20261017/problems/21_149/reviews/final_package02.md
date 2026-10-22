# Frozen package 02: independent adversarial mathematical and reproduction review

**Completed 17 October 2026, 20:41:06 UTC / 13:41:06 America/Los_Angeles. Review completion estimate: 100%.** This percentage describes completion of the assigned review; it is not a probability of mathematical correctness or of first priority.

**Verdict: no outstanding substantive objections found to the frozen manuscript's explicit ambient theorem or its stated application to the standard real Dlab families.** I independently reconstructed its proof, actively searched for failures of its infinite/support and arbitrary-embedding deductions, checked the principal dependencies and named prior results, and reproduced the package. I found no counterexample, circular step, missing uniformity assumption, or necessary mathematical correction. This is a separate AI adversarial review, not independent human peer review or formal verification. The precise source-access and priority limitations below remain material qualifications.

## 1. Frozen objects and independence

The three objects supplied for this review have these SHA-256 hashes, both at entry and after the checks:

| Object | SHA-256 |
|---|---|
| `publication/paper.pdf` | `e4f442fada2f0203678eb5344ce420875947cca02506b2c19df255947e614fe7` |
| `preprint/main.tex` | `edb1b5751a57f51477efd03cb3a6b5fb4f6485d7a51c3234f064ccac819bcd57` |
| `publication/source-and-verification.zip` | `4450dddd0ba400e4b97347bbf317c7e2f11bf3b21b9e971d32c430e7be72baf6` |

I read the whole frozen TeX before prior review verdicts. I did not participate in discovery or drafting. After my initial reconstruction, I used `audits/primary_left_germ_evidence.md` for reproducible primary-source queries and later the earlier package report to recover its successful p. 543 query arguments; the returned primary text was checked independently. No earlier verdict is a premise of this assessment. A separately spawned subagent, provided only the manuscript path and a targeted attack request, read no previous reviews and independently checked the centralizer, least-component and orientation steps. It returned no mathematical objection at 20:38:45 UTC. Its scope excluded literature and simplicity, which I checked separately.

All generated evidence is under `reviews/package02_reproduction/`, with this requested report at `reviews/final_package02.md`. I made no manuscript edit, Git mutation, external contact or publication action.

## 2. Exact target and external dependencies

The [official current Notebook](https://kourovkanotebookorg.wordpress.com/wp-content/uploads/2026/10/21tkt-1.pdf), printed p. 199 / PDF page index 198, asks whether there are order automorphisms of Dlab groups not induced by conjugation by elements of a possibly bigger Dlab group. It attributes the problem to V. M. Kopytov and N. Ya. Medvedev and lists A. V. Zenkov. There is no ambient rank-one restriction in that statement. The frozen manuscript addresses this stronger quantifier, not just non-innerness in its source.

I downloaded the [primary Dlab 1968 PDF](https://www.cambridge.org/core/services/aop-cambridge-core/content/view/2FC98980CF8D6CE6001298088EC1E5FA/S1446788700006261a.pdf/div-class-title-on-a-family-of-simple-ordered-groups-div.pdf), read its definition and cited results, and visually inspected printed pp. 592, 602 and 603. Its full interval group uses the stated right affine germ at every point before 1, including 0; its compact-support subgroup matches the manuscript's source. Theorems 4.1 and 4.3 give the stated order correspondence and algebraic simplicity for that subgroup. The manuscript's use of these theorem numbers is correct.

## 3. Independent proof reconstruction and attempted failures

### 3.1 Ambient groups, well ordering and perfectness

Composition and inversion preserve exact right affine germs with positive slopes; the eventual affine formula in the real case is likewise preserved. No finite-piece assumption on compact sets has entered the proof. Accumulation of affine pieces from the left remains allowed.

For a nonempty family of support components with finite left endpoints and finite infimum a, failure to attain a gives distinct fixed left endpoints decreasing to a. Continuity fixes a, and its right affine germ then has slope 1 because it fixes arbitrarily close points to the right. It is the identity on a right interval, contradicting those component endpoints. This establishes an actual least member, not just existence of infima. On the unit interval the infimum is finite and below 1. In the real ambient class, an eventual nonidentity affine formula gives a unique initial support component and bounds every other component below; an identity initial ray directly gives the lower bound. The identity map's empty component family presents no problem.

The slope homomorphism at 0 is trivial on a perfect subgroup. In the real case the eventual-affine homomorphism has image in a metabelian affine group and hence is also trivial on a perfect subgroup. Thus the particular q used in the centralizer application has no support component beginning at minus infinity. These identity neighborhoods may depend on q; neither the proof nor my reconstruction assumes a common neighborhood for the whole group.

The source and every G(L) are nontrivial simple groups by the cited theorem and affine interval rescaling. They are nonabelian because increasing interval homeomorphisms are torsion free, whereas a nontrivial abelian simple group has prime order. Therefore they are perfect. The manuscript explicitly defines L to be a nonempty relatively compact open interval, so the argument does not incorrectly invoke simplicity for disconnected open sets.

### 3.2 Perfect centralizers and disjoint local supports

A map commuting with q increasingly permutes q's support components. Every increasing bijection of a well-ordered set fixes each member: at a first nonfixed member, a later image leaves no possible preimage for that member, while an earlier image conflicts with already fixed predecessors. This also handles infinite order types and limit stages.

On a preserved component (a,b) with finite a, each element of the perfect centralizer fixes a and has slope 1 at a. Its identity right neighborhood can again depend on that element. One of the two iteration directions of q tends to a from every point of the component: an interior limiting value would be a fixed point. Commutation transports identity back along that orbit. Consequently the perfect centralizer fixes the entire support of q pointwise. This uses the exact affine germ, not merely existence of derivative 1.

For disjoint source intervals, the two local groups commute. Each q in the first image belongs to a perfect subgroup, and the second image is a perfect centralizer. Taking the union over q proves disjoint action supports. I found no illicit conversion of elementwise local information into a uniform group bound.

### 3.3 Least action components and arbitrary embeddings

Every action component is invariant because its finite endpoints are common fixed points. Its restriction kernel is a proper normal subgroup of the simple source, and is therefore trivial. Hence one fixed nonidentity source element acts nontrivially on every action component. Its least support component identifies a least action component: any earlier action component would contain an even earlier support component of that same element. There is no prior assumption that the whole action-support set is well ordered.

The same reasoning applies to local groups inside J0. Their action there is nontrivial because the full source action there is faithful. Common fixed boundaries of J0 prevent local action components from crossing it. Thus K(L) exists and is a genuine global action component of the local subgroup. This remains valid when action components are unbounded or when the action has many components.

Conjugation gives exactly gG(L)g^-1 = G(gL), including compact containment; g maps compact subsets to compact subsets and maps interior intervals to interior intervals. Consequently K(gL) = e(g)K(L). This reasoning is algebraic in e. No topological continuity, spatial realization, order preservation or surjectivity of the embedding is assumed.

For segment ratio r, the stated two slopes s and 2s give lengths ell(2s-r)/s and ell(r-s)/s. They are nonnegative, sum to ell, and yield total image length r ell. The cases r=s or r=2s simply omit a zero-length piece. Fixing common outer endpoints and doing this on successive segments produces a source element for every increasing finite tuple map. In particular it transports every positively separated ordered interval pair to every other. Equivariance and increasing e(g) therefore force one uniform orientation. I found no gap from touching intervals because the actual tails have strict positive gaps.

### 3.4 Construction, orders and final contradiction

The bump formulas agree at one third of each bump, fix its endpoints, and strictly move all interior points to the right. The bump intervals are pairwise disjoint and accumulate only at 0 and 1. Preservation of each closed bump interval and shrinking lengths give endpoint continuity. Both h and its inverse are finite piecewise affine on every compact interior interval. Conjugating a compact-support source element only requires these interior germs; near the boundary the conjugate is the identity. This proves both directions of the normalizer assertion.

The first support slope determines a positive cone. With different first support points the earlier germ persists; with equal points the slopes multiply. Inversion reciprocates it, and source conjugation preserves it. The Dlab order theorem identifies the resulting two orders. The h-conjugate's first support point is transported increasingly and its slope is unchanged by cancellation of the two conjugating germs. Thus both orders are preserved. No right germ of h at 0 is required.

On each tail interval L, h preserves L and moves an interior point. A sufficiently small V and h^-1(V) are disjoint, so a nontrivial compact finite bump supported in V is altered by conjugation. Thus alpha preserves every selected local subgroup but is nontrivial on it.

An implementing u would normalize the full image, preserve its least component J0, and then preserve each selected least local component K(L). If it fixed a K(L) pointwise, faithfulness of the local restriction would force alpha to be the identity on that local group, a contradiction. A moved point therefore supplies a support component U(L) of u wholly inside K(L), since finite boundary points of an invariant interval are fixed. Disjoint K(L)'s give distinct U(L)'s. In the increasing orientation the C tail descends; in the decreasing orientation the D tail descends. Either contradicts the well ordering of support components of u. This applies even though u need not belong to a perfect subgroup and even if u has an initial support component in the real case.

### 3.5 The countermodel is correct and essential

I independently checked the twisted diagonal construction for an arbitrary automorphism beta, including negative integer powers. The cells partition the negative ray up to endpoints; each image map preserves every cell, is continuous at 0, and has an identity right neighborhood at every finite cell endpoint. The shift v(x)=x/2 moves cell n to n+1, so v^-1 E(f) v acts by beta^(n+1)(f) on cell n, exactly as E(beta(f)) does. The image and v have support bounded above and the required finite right germs. No germ at minus infinity is available. This is a valid counterexample to extending the theorem by silently dropping that hypothesis; the manuscript does not do so.

## 4. Standard real-family inclusion and its evidentiary boundary

I independently reproduced indexed primary extracts from [Zenkov–Medvedev 1999](https://www.mathnet.ru/php/getFT.phtml?jrnid=al&option_lang=eng&paperid=2480&what=fullt): p. 538 defines the initial-ray-fixing real subgroup; p. 542 factors every full-group element as an affine map times such an element and explicitly supplies the affine germ when the first support point is minus infinity; p. 543 places bounded-above-support D_*H inside that same full group. Thus it is not the larger countermodel class. The inference to eventual left affinity is valid. Although the order-theory propositions assume rank one, this particular germ deduction uses no rank restriction. With the same defining affine behavior it applies to any positive-real slope subgroup. The four interval groups are directly contained in A_I.

Successful p. 542 queries were the three-query batch in `audits/primary_left_germ_evidence.md`. Successful p. 543 queries were `"О группах Длаба" "289–298" doi`, `"Длаба" "полупрямым" "T" "-1"`, and `"Длаба" "D_{*H}" "543"`. The p. 538 batch was `"Длаба" "§ 2" "538"`, `"Длаба" "D_{H*}" "538"`, `"Длаба" "локально" "прямой"`, and `"Длаба" "ТЕОРЕМА 2.1"`.

**Access limitation:** I did not obtain the 1999 PDF bytes or visually authenticate its pages. Direct web opens of both its article record and full-text URL timed out; the evidence is indexed, page-sized primary text independently returned by the web tool. The frozen package discloses this. I found no contradictory source definition. My scope verdict concerns the standard real families and the explicit ambient classes in the paper, not arbitrary ordered-field generalizations or arbitrary groups someone might choose to call Dlab groups.

## 5. Lean and prior-result/priority comparison

I downloaded the [exact pinned Lean source](https://github.com/pitmonticone/Kourovka/blob/64a4fe59b1df1893a0a1a68641d6806ccaaa7150/Kourovka/Problem_21_149.lean), SHA-256 `4a69f3e9d739fc1119d5fbf561fc4ca63c064bcdeece6766ff987eabcd8c5655`. Its actual 778-line file explicitly labels the endpoint theorem at lines 768–775 as the original formulation. The statement has existential H, order and automorphism followed by exclusion from the source's inner-automorphism subgroup. It has no universal larger ambient group or embedding quantifier. Its conjugator has just two affine pieces with slopes 2 and 1/2; it belongs to the full interval Dlab group while failing the compact source's boundary identity condition. Thus its particular automorphism is implemented after inclusion in that larger Dlab group. The manuscript's pinned lines and mathematical distinction are accurate. I did not rebuild Lean or audit all its imported foundations; its scope is visible directly in the theorem statement.

The primary [van Doorn–Judin–Monticone–Morrison v2 appendix](https://arxiv.org/html/2607.17477v2) expressly describes the change from non-innerness to the possibly larger Dlab-group question. The manuscript's historical attribution is consistent with it.

The current [Gong–Yang–Zeng arXiv record](https://arxiv.org/abs/2609.18630) lists only v1, submitted 16 September 2026. Its [Theorem 1.1](https://arxiv.org/html/2609.18630v1) quantifies over rank-one H, exactly six named families and order-preserving embeddings; its text expressly excludes the reflected real family. It already supplies the one-tail obstruction credited by the manuscript. The frozen paper's additional arbitrary slope, arbitrary embedding and full/reflected real-family quantifiers exceed that stated result; they are the appropriate novelty claim. I found no duplicate of those full quantifiers in fresh English/Russian Dlab-automorphism and problem-number searches.

**Priority limitation:** These are bounded public-source checks through this timestamp, not a guarantee of first priority. I did not exhaust subscription bibliographic databases, unpublished work, unindexed material, or all later consequences of every older embedding theorem. The honest claim is that the named nearest prior results do not state the new full quantifiers and no stronger prior result was found. The paper already states this bounded assessment and credits the known mechanism.

## 6. Reproduction and presentation

- Safely extracted the supplied ZIP into the reproduction directory. Its 15 entries equal exactly the 14 manifest payloads plus the manifest; there are no extra or missing entries. Every listed byte count and SHA-256 matches. Extracted TeX and PDF equal the separately frozen source/PDF byte for byte. Evidence: `manifest_check.json` and `zip_inventory.json`.
- Ran the exact standard-library verifier from the extracted package. Its output exactly equals the stored JSON: 1,562 segment cases, 3 tuple cases, 200 bump intervals, 441 affine-germ cases and 36 affine-group cases, all passed. Also verified that optimized Python deliberately refuses to run. These tests are finite supplements and do not certify the universal theorem, as both script and README explain.
- Rebuilt extracted `main.tex` with Tectonic successfully after creating an output directory. No TeX warning or missing-reference message appeared. The rebuilt PDF has the same six pages and extracted text as the published PDF. Its binary hash differs because creation metadata differs; all six corresponding 100-dpi PNG files are byte-identical. Evidence: `rebuild/main.pdf`, `render_comparison.json` and the published/rebuilt page images.
- Visually inspected every rendered manuscript page. I found no clipped or overlapping text, broken equations, missing glyphs, unreadable reference, or unresolved cross-reference. The split of Corollary 8 across pp. 5–6 is legible and is not a substantive defect. The abstract, theorem, final scope statement, references and AI/no-human-review disclosure agree.

No correction is required by this pass. A future direct download and visual check of the 1999 source would strengthen source authentication, and future human review or a formalization would provide a different kind of assurance. Neither has occurred here, and neither is claimed by this verdict.
