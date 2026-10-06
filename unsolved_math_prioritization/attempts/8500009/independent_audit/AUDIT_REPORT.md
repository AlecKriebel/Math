# Independent audit: strong rational Diophantine quadruples

Problem 8500009 / AMR-084-0009, rank 932. Review date: 6 October 2026.

## Decision

**ACCEPT PARTIAL.** The frozen author report's four propositions, exact benchmark correction, regular-extension rejection, and nonlifting witness are mathematically valid under their stated hypotheses. No correction to the author packet is required. This is acceptance of an explicitly incomplete mathematical investigation, not acceptance of a solution to the existence problem or a claim of originality.

The proper mathematical status remains **partial, 3/5**. No strong rational Diophantine quadruple is constructed, and no nonexistence theorem is established. The three counted approaches are benchmark/regular-extension checks, the full lifting curve, and sign/zero-product analysis. The remaining rational-point and mutual-compatibility gaps are substantive.

## Frozen inputs and scope

The review used a fresh extraction of `STRONG_RATIONAL_8500009_AUTHOR_SAFE_FREEZE.zip`, exactly 15,851 bytes, SHA-256 `026cecc87b82627bf471ed37ee920ec2203ec8e94cd14f7e1fb0a629469c111c`. Its external manifest is exactly 1,500 bytes, SHA-256 `0fcc1d4e600a73113c40b708df26f9aa4d754a7d493af61f499a0c09f6e32342`. Every one of the seven author member byte counts and hashes matches the manifest. The original inputs and all author member bytes remain unchanged. No repository or queue changes were made.

The independent work includes proof-level scrutiny, private inspection of the cited primary-source bytes, exact-ID corpus-gate replay, author-program replay, and a separately implemented exact validator which imports no author code. Source or corpus text and private review material are not in the publication-safe package.

## Mathematical audit

### 1. Exact lifting: accepted

For a new rational element x, its diagonal condition is parametrized by x=(t^2-1)/(2t), t nonzero. If s^2=x^2+1, the inverse choice t=x+s cannot vanish because (s-x)(s+x)=1. Thus no admissible diagonal solution is lost. Conversely the displayed parametrization gives the rational diagonal square (t^2+1)^2/(4t^2).

For every fixed a_i, multiplication by the nonzero square 4t^2 gives exactly f_i(t)=4t^2(a_i x+1), with f_i(t)=2t(a_i t^2+2t-a_i). Consequently the equivalence is individual and simultaneous, not merely a product condition. A zero cross-value is valid and remains a square on the cover. The explicitly excluded t=0, x=0, and repeated-element values are necessary. The two inverse t-values of a diagonal solution both work; the author tests and independent validator check this for the benchmark extensions.

At a finite nonzero branch value at most one f_i vanishes, so no unaddressed common-branch singularity undermines the affine lifting statement there. The singular common fiber t=0 is excluded from the extension problem. The smooth projective normalization is correctly used only for the geometric calculation.

### 2. Geometric connectedness and genus: accepted

This part was checked as an abstract proof, not inferred from numerical examples or test success.

Each Q_i=a_i t^2+2t-a_i has two simple nonzero roots, because a_i is nonzero and a_i^2+1 is a nonzero square. If Q_i and Q_j shared a root with a_i unequal to a_j, their difference would force t^2=1. At t=1 and t=-1 every Q_i takes 2 and -2 respectively, so this cannot occur. Thus every Q_i supplies two branch points absent from every other Q_j and from zero.

Over the algebraic closure, any nonempty product of the f_i has odd valuation at a root belonging to a selected Q_i. No nonempty product is a square. The k square classes are therefore independent, and the function field has degree 2^k. This proves geometric connectedness of the normalized multiquadratic cover.

The branch locus has exactly 2k+2 points: two private roots per Q_i, together with zero and infinity. At a private root, exactly one generator has odd valuation. At zero all k generators have valuation 1; at infinity all have valuation -3. Over the algebraically closed residue field, local units are squares in the completed local field. Thus at either common branch point every ramified generator differs from a chosen one by a square, and the ramified local field extension has degree **2**, not 2^k. The geometric inertia group is the one-dimensional parity direction (1,...,1). Arithmetic residue-field issues do not alter this geometric genus computation.

For N=2^k, every branch point therefore contributes N/2 to Riemann-Hurwitz. Hence 2g-2=-2N+(2k+2)N/2=2^k(k-1), and g=1+2^(k-1)(k-1). In particular the pair curve has genus 3 and the triple curve genus 9.

An independent way to check the calculation is to stay on the x-line and adjoin square roots of x^2+1 and each a_i x+1. The cover then has degree 2^(k+1), with branch points i, -i, the k distinct rational points -1/a_i, and infinity. At infinity the diagonal radicand has even valuation and the linear radicands have common odd valuation, again producing index 2. Riemann-Hurwitz again gives 2g-2=2^k(k-1). This agrees with the t-line proof and guards against losing the diagonal double cover.

The independent exact program additionally checks branch-vector ranks and genus arithmetic for k=1 through 8. The sum of the genera of the nontrivial double-cover quotients is checked as an arithmetic cross-check; it is not substituted for the abstract proof above.

### 3. Positive normalization with its exception: accepted

Simultaneous negation preserves all product conditions and permits a positive maximum a. With every cross-value nonzero, ab+1 is a strictly positive rational square. For each other element b<a, e_b=(a-b)/(ab+1) is therefore positive. The three identities in the author report are correct after clearing denominators. They prove the pivot cross-condition, transformed diagonal condition, and transformed pairwise cross-conditions respectively.

Distinctness is preserved: subtracting two transformed values yields (c-b)(a^2+1)/((ab+1)(ac+1)), which is nonzero when b and c differ. Also e_b=0 forces b=a, and e_b=a forces b=0. Neither is allowed. The transformation thus preserves the tuple's size as well as rationality and every square condition.

The zero-cross exclusion is essential for this transformation. The published triple (37620/26299,195/28,-28/195) is strong and has one cross-value zero, so the denominator issue is realized by genuine inputs. The report does not claim its argument eliminates such tuples or that no different transformation could help them. This scope is correct.

### 4. At most one zero cross-value: accepted

The statement is understood, consistently with the problem and the report, for distinct elements; its conclusion counts unordered pairs of different values. If ab=-1 with a>0>b, then for any other c the nonnegative cross-values ac+1 and bc+1 imply b<=c<=a. Thus a and b are the two extreme values. Any second product-minus-one pair would have to be the same pair of extremes. This proves uniqueness without needing the diagonal conditions. The proof actually uses only nonnegativity of the cross-values, and applies over the reals as stated.

These two sign propositions leave the correct exhaustive alternatives for a putative strong quadruple: a positive example can be obtained from any zero-free example, while an example with a zero cross-value has exactly one such extreme pair. Neither alternative is settled.

## Exact examples and traps

- All ten benchmark conditions were recomputed independently. Exactly pair (3,4) fails; every diagonal succeeds. The exceptional reduced value is 459627303/309488, with both claimed consecutive-square bounds correct.
- Both ordinary regular extensions of the recorded positive triple are exactly 135938/106533 and 789662/11837. Their three new cross-values are squares, but each new diagonal fails. Rejecting these two candidates is not an exhaustive extension classification.
- The quotient nonlifting example is valid. The base (3/4,-4/3) is a strong pair, including its zero cross-value. At t=3/4 the new element is -7/24 and the two new cross-values are 25/32 and 25/18. Both are nonsquares, but their product is (25/24)^2. Independently, Q_1=75/64 and Q_2=25/12, so Q_1 Q_2=(25/16)^2. There is a rational point on the product quotient and no rational lift at that t to both individual equations.
- Zero elements, repeated elements, ordinary integer quadruples, and a product-only square check are correctly rejected as substitutes for a strong quadruple.

## Primary-source audit

The source claims were checked against primary materials, with the following limits made explicit.

1. The inspected [author-maintained problem list](https://web.math.pmf.unizg.hr/~duje/pdf/open2.pdf) is 335,080 bytes with SHA-256 `4309f64423915c4e6d48f98408cc0e38a419a44d4dcb30942928cdf580240d24`. Its rendered cover says **October 5, 2026**. Its rendered page 4 retains Problem 1.15 and prints **2223/3046** in the almost-quadruple. Both were visually checked, so this is not reliance on an older cached March 28 extraction or an OCR-only typo inference.
2. The [2008 author manuscript](https://dujella.github.io/pdf/strong3.pdf) is 167,991 bytes with SHA-256 `d3c77d825491fb18e91d667277a3295db58e02bcc6b4ce407d46bd2931895f49`. Definition 1, the genus-two necessary product curve, the listed triples, and Section 5 were checked. The rendered page 11 visibly has **2223/30464** and identifies the failed last cross-condition. The [maintained survey, Section 5.5](https://web.math.pmf.unizg.hr/~duje/ratio.html#5.5) agrees. Independent arithmetic shows 2223/3046 fails its own diagonal condition, supporting the report's choice of the original value.
3. The [sextuples-with-strong-pair manuscript](https://dujella.github.io/pdf/strongDKP.pdf), including Theorems 1 and 2, asserts a strong pair inside ordinary sextuples. It supplies no strong quadruple. Its RACSAM 119 (2025), Article 36 publication metadata is independently confirmed on [Dujella's publications page](https://dujella.github.io/papers1.html). No arXiv submission-date claim is needed or endorsed here.
4. Definition 1.1 in [the specified quartic-quadruple v1](https://arxiv.org/html/2604.19140v1) concerns i<j, so fourth-power cross-values do not impose the missing diagonal squares. Referring to that inspected v1 is accurate even if later publication metadata changes.
5. The related D(q)-triple and Eulerian-triple manuscripts concern triples and/or a different parameter. The two older 2014 title matches were inspected sufficiently to confirm that their terminology cannot by itself establish the current ten-square problem; this audit makes no broader adverse judgment about those papers.

All nine stored source objects' byte counts and hashes agree with the author's metadata. `source_hash_replay.json` records these integrity checks without source contents. The original exact problem-page access failure is disclosed by the author; this review does not convert that failure into a statement discrepancy. The mathematical definition is independently reconciled against the primary sources.

The status conclusion is deliberately limited to the inspected current problem list and related sources. It does not purport to certify the absence of every possible result in the literature or establish novelty.

## Exact-ID inherited-work gate

The whole catalog, problem-record corpus, and research-report corpus were independently rehashed with matching byte counts, record counts, and supplied hashes. The complete exact-ID problem record and associated report were read. Their contents are literature-status discussion and source retrieval, including the benchmark misdescription corrected by this work. No substantive inherited authored proof, reduction, or computation was found. The gate is **literature-only eligible**, not justified merely by its queue label or unused budget.

The canonical pair was recomputed using precisely `json.dumps([whole exact-ID record, reports.get(problem_number,{})], sort_keys=True)` with Python's default formatting and UTF-8 encoding. It is 5,244 bytes with SHA-256 `5fc827d969326cb47716a9c640734509f600cd5471988fb677f9bfa6214686ca`, matching the catalog review hash. ID, code, and rank also match. `corpus_gate_replay.json` contains only verification metadata, never the records themselves.

The author's historical repository-search statements are not a novelty certificate. This audit made no repository changes and does not assert that a default-branch code search exhausts repository history.

## Reproducibility and adversarial controls

The author suite has nine test methods. It passes in fresh relocated directories under normal Python, -O, -I, and combined -I -O. Certificate output is byte-for-byte identical to the frozen 3,638-byte certificate in all four modes. The author mutation runner was rerun and all eight negative controls were killed by executed test failures, not syntax errors:

1. Drop diagonal conditions.
2. Admit a zero element.
3. Admit repeated elements.
4. Force the missing benchmark cross-value to pass.
5. Accept a negative value as a square.
6. Use a wrong cover scale.
7. Replace individual squares with a product-square condition.
8. Use the wrong branch count.

The separately authored `independent_exact.py` imports no author implementation. It verifies eight formal polynomial identities, 648 lifting fixtures, six positive-normalization fixtures, 336 ordered-real zero-edge fixtures, the exact source examples, the quotient coordinates, and branch/genus arithmetic for k=1,...,8. Its checks use explicit exceptions, so optimization cannot erase them. It produces identical output in all four execution modes.

Run `python replay_all.py` from the safe packet to verify pinned author member hashes and repeat the complete relocated mathematical test/mutation replay. No packages beyond the Python standard library, network access, source PDFs, or datasets are needed for that replay. The historical source/corpus integrity evidence is separately recorded and cannot be re-established from the safe packet alone because those third-party materials are intentionally absent.

The code checks examples, algebraic identities, and arithmetic consequences. It is not an exhaustive rational-point computation, and the finite fixtures are not the proof of the general genus or sign propositions. Those proofs have been separately audited above.

## Privacy and publication boundary

The frozen safe package is allowlisted to unchanged author deliverables, this authored audit, standalone exact/replay code, generated mathematical test evidence, and public verification metadata. No PDFs, extracted source text, page images, raw corpus records, private personal data, credentials, private coordination, or repository/queue copies are included. Full execution logs are limited to authored programs and mathematical results, with relocated paths normalized.

No patch or derivative of the author report is required. Acceptance applies only to the exact pinned author packet and the explicit partial scope. Any later mathematical edits require corresponding review; this acceptance must not be relabeled as a solution or a proof of novelty.
