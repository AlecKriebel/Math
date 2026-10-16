# Independent audit: zero-value IM-sharing counterexamples

Problem 30000700 / OWR-1460-004, queue rank 659.

## Verdict

**PASS, with an essential scope qualification.** The frozen author packet gives a correct negative answer to the universal IM replacement question literally printed after Theorem H. All three propositions are valid. No mathematical correction is required. The result is a zero-shared-value obstruction, not a determination of the strengthened nonzero-shared-value problem. Neither bibliographic novelty nor the proposers' intended scope has been established.

Audited archive: `author-packet.zip`, 15,098 bytes, SHA-256 `5caa2ded8af38610317260f2f002b0a3bb813b06c58962e628462394f7f2e512`. The archive was extracted into a separate working copy. All ten author-manifest entries match; all eleven archive members are accounted for. Originals were not edited. This audit was prepared independently of the author; no helpers or remote writes were used.

## Primary-source check

The EMS publisher PDF for [Normal Families and Complex Dynamics](https://doi.org/10.4171/OWR/2007/09) was independently retrieved. Its 2,885,678 bytes and SHA-256 `d38624e71305f8fbd26b92a7903e8d7fb57c22c24763409b1a7126887ba10496` match the author's copy. Fang's complete contribution, printed pp. 501–503, was read. Pages 502–503 were independently rendered and visually inspected; web screenshot failure did not prevent this check.

The relevant scope is nonconstant entire f, integer k≥2, and complex a,b with b≠0. CM at a is the hypothesis proposed for weakening; the second hypothesis is the pointwise implication f′=b ⇒ f^(k)=b. There is no a≠0 restriction in H and no multiplicity restriction at b. The conclusion is d exp(cz)+((c−1)/c)a, c,d≠0, c^(k−1)=1. The preceding definition of IM is equality of fibers without multiplicities. The neighboring results explicitly impose a≠0, but H restates its own parameters. The catalogue adds b≠a and has the wrong additive term; neither discrepancy affects the zero-value examples. [Publisher PDF](https://ems.press/content/serial-article-files/46093?nt=1).

## Independent mathematical review

### 1. Basic and universal polynomial counterexamples

For a=0, k≥2, b≠0 and arbitrary z0, take f=b(z−z0)^k/k!. This is a nonconstant entire function. Its first derivative is b(z−z0)^(k−1)/(k−1)!. The two zero sets are precisely {z0}; the multiplicities are k and k−1, so the sharing is IM and fails CM. The kth derivative is identically b. The b-fiber of f′ is nonempty and consists of k−1 distinct nonzero translates, since (z−z0)^(k−1)=(k−1)!.

At a=0 the conclusion reduces to a nonzero exponential, which has no zero. Since f(z0)=0, the conclusion fails regardless of its restriction on c. The parameters also satisfy b≠a. In particular, f=z²/2, b=1, k=2 has f′=z, f″=1 and its sole b-point is z=1. Nothing is vacuous. The counterexample does not exploit the catalogue's additive-constant error.

### 2. Exhaustive polynomial classification

Let n=deg f≥1. If a≠0, every root of f−a has derivative a and is consequently simple. For n≥2 this supplies n distinct roots of the degree n−1 polynomial f′−a, a contradiction. When n=1, the f−a fiber is one point, whereas the f′−a fiber is empty or all of C; sharing again fails.

For a=0, n=1 fails for the same reason. At n≥2 every root of f is multiple. If there are r distinct roots with multiplicities m_j, f′ has multiplicities m_j−1 there. Sharing forbids other derivative roots, so n−1=sum(m_j−1)=n−r and r=1. Thus f=A(z−z0)^n with A≠0.

The equation f′=b has n−1 distinct solutions because b≠0. If k>n, the kth derivative is zero and the required implication fails. If 2≤k≤n, the polynomial f^(k)−b has degree at most n−k≤n−2 yet vanishes at all those n−1 points. It must vanish identically. This forces k=n and A n!=b. The converse was just checked. This independent degree proof also confirms the author's root-of-unity proof. The classification is complete, including linear and k>n edge cases.

### 3. Transcendental family

For k≥3 let q=−1/(2^(k−1)−2), choose λ≠0 with λ^(k−1)=q, put b=−λ/2, and set f=(exp(λz)−1)². The denominator defining q is nonzero. With t=exp(λz), differentiation gives f′=2λt(t−1) and f^(k)=λ^k(2^k t²−2t).

Because t≠0, the zeros of f and f′ coincide at t=1, with respective multiplicities two and one; t has nonzero derivative there. Also f′−b=2λ(t−1/2)². Exponential surjectivity onto C\{0} makes this fiber nonempty (indeed infinite). At t=1/2 the kth derivative equals λ^k(2^(k−2)−1)=−λ/2=b, by the imposed equation for λ.

The points z=2πin/λ give infinitely many distinct zeros. The function is nonzero somewhere and is entire, so it is transcendental. Its zeros exclude any nonzero pure exponential. Thus the claim holds for every asserted k. It does not claim this formula works for k=2; in that case its second derivative is zero at t=1/2 while b≠0.

Multiplicity at the b-fiber deserves explicit attention: f′−b has double zeros, whereas f^(k)−b has simple zeros there. In the t coordinate the derivative of the latter at 1/2 is λ^k(2^k−2)≠0, and dt/dz=λ/2≠0. Hence the construction would fail a multiplicity-dominating b-implication. The actual hypothesis asks only for a value implication, so this is no defect. “CM at b” in control commentary should be understood as a stronger, unrequested condition, not as the printed hypothesis.

## Controls and adversarial tests

The author script was inspected, run from the extracted archive, and compared byte-for-byte with its saved JSON. It reproduced all 1,703 polynomial grid cases (33 positive, 1,670 negative), the quadratic control, and 22 transcendental identities, k=3…24. The remainder check is legitimate because f′−b is squarefree in the monomial tests. In the exponential tests it correctly uses the reduced fiber rather than its square.

A separate standard-library verifier imports none of the author's code. It exhausts 3,120 rational-coefficient polynomials of degrees 1…4 in a coefficient box, compares squarefree parts for a∈{−1,0,1}, and checks 480 b/order combinations for the 16 sharing pairs. It finds eight admissible combinations, all predicted by the classification. It additionally checks 99 translated, fractionally scaled polynomial examples and 38 exponential identities, k=3…40. Negative controls include degree one, wrong coefficients/orders, the multiple-b-point strengthening, λ=1, the k=2 exponential boundary, and an invalid additive shift intended to turn a=0 into a≠0. All pass. These finite checks corroborate algebra; the universal claims rest on the proofs above.

## Interpretation and literature limits

The shared value zero is exceptional for multiplicity reasons. At a nonzero shared value, f−a has simple zeros automatically; at zero, differentiation reduces positive zero multiplicities and IM discards that information. This explains the elementary obstruction. The surrounding discussion may motivate studying a nonzero-a question, but it does not authorize silently inserting that hypothesis into H. Historical intention would require additional evidence. Recommended description: “negative answer to the literal printed universal IM statement through its permitted zero-value case.” Avoid an unqualified claim to have solved a historically intended nonzero-a problem.

The [Chang–Fang publisher abstract](https://link.springer.com/article/10.1007/s10114-005-0861-5) was independently read. It requires a nonzero value and uses the same value in the two antecedents. Full text remains subscription-only in the accessed route. The publisher lists online publication on 15 December 2006 and volume 23, pp. 973–982 (2007); these dates are compatible.

The complete nine-page [Feng Lü 2010 paper](https://www.math.nthu.edu.tw/~amen/2010/090910-1.pdf) was read for scope, not audited as a separate theorem proof. Its freshly downloaded 111,061-byte PDF matches SHA-256 `8779a506205c668d0493e7fa73984b8271c88190ab0b44611130c4fe91f0d384`. Its principal theorem has a nonzero shared/antecedent value and a third-derivative conclusion at that same antecedent. It does not supply the distinct-b assertion reviewed here.

The [Fang–Zalcman 2003 article](https://www.sciencedirect.com/science/article/pii/S0022247X03000416), cited by the report as H's source, was not obtained in full. The direct web request failed; direct HTTP returned a short “Site Unavailable” page, not scholarly content. This audit does not claim fresh inspection of its publisher abstract. The catalogue-linked [CiteSeer item](https://citeseerx.ist.psu.edu/document?doi=1ad2e1a1746f584176b55465340661e21d712c62&repid=rep1&type=pdf) timed out, and the other [ScienceDirect item](https://www.sciencedirect.com/science/article/pii/S0022247X00970070) returned 403. Their identities and content are not established here.

Independent targeted searches did not establish a prior exact resolution, but the search is not exhaustive. Search snippets are not proof of full-text review. No novelty or priority is certified. No current claim that the nonzero-a variant remains open in the literature is certified; only that this packet and audit do not resolve it. Live repository duplicate checks and fresh remote dataset hashes were not repeated in this audit; the author's historical receipts are not promoted to independent current verification.

## Packaging and corrections

The source PDFs, extracted texts, rendered pages, dataset records, repository tool receipts, and private coordination are excluded from the portable audit. Its files contain authored analysis, executable exact controls, public source-identification/inspection metadata, and hash bindings only. `CORRECTIONS.json` records zero required mathematical corrections and the scope guardrails. `BINDING.json` links this audit to every archive member by path, byte count, and digest. No original file, external branch, PR, commit, or account was changed.
