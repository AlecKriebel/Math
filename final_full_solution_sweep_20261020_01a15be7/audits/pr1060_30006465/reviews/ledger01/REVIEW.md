# Independent adversarial review: PR1060 existing-publication ledger repair

**Verdict: ready to record the existing external publication, subject to the root's final live duplicate/state checks. No substantive objection or required row change remains.** This accepts the exact proposed four-cell row in `LEDGER_RECONCILIATION_PLAN.json`, SHA-256 `1269c870ea443934d15c6cb280a4cb43e755b9ee6c5ca2bf9ab1916c4ad0a00f`. It authorizes no new publication. This reviewer made no spreadsheet, Zenodo, PR, branch, index, root-cursor, or other external mutation.

## Object and evidence boundary

The object is the missing accounting entry for problem30006465 / OWR-14299577-018 and [PR1060](https://github.com/AlecKriebel/Math/pull/1060), not a claim of a new solution. Fresh read-only PR retrieval found an open draft with head `30779cf262f565de043c65e7e8f6fa3148b4eda4` and base `f6caddda8f8be2cdb3e91494325d8f7f365bc3fc`. Reading the actual Git diff and all seven corresponding complete head blobs confirmed no QUEUE edit and an express prior-work disposition. The PR itself credits Ferudun and disclaims independent discovery, historical-priority certification and new proof-search turns.

Independently retrieved: the complete live spreadsheet range, PR JSON, original source PDF, public Zenodo metadata, DOI destination and all three deposited files. Read the full five-page paper's extracted text, complete TeX, bibliography, license, verification report, reproduction README and all seven PR blobs. Visually inspected original PDF page56 (printed2756) and deposited manuscript page1. This review does not claim visual inspection of the other manuscript pages. Raw source/provider/sheet contents, renders and reviewer checks remain under ignored `private/`; the public report contains original assessment and public bibliographic links.

## Original question and exact mathematical scope

The [primary OWR51/2025 report](https://ems.press/content/serial-article-files/52435), printed2756, attributes the question to Christian Bernert and Nuno Arala Santos. It assumes n>=1, A contained in the nonzero integers from -n to n, cardinality n, and at least one of k,-k in A for each1<=k<=n. There are n disjoint pairs and n elements, so this is precisely the deposited paper's exactly-one hypothesis. The questions ask near-total coverage of positive differences in [1,n], and an asymptotic positive-density quadratic **ordered-pair** count for every B contained in [1,n]. The k versus 1-k variant mentioned negatively by the source is a different question and is not silently substituted.

I challenged the normalization, omitted zero, equal-parity restriction, injectivity and endpoints in the short proof. With odd g, reflection x -> -x-d pairs ++ and -- defects, and the potential midpoint cannot be a defect. Positive outer defects together with the strict upper half of the negative inner interval contain exactly one representative per defect orbit, hence have size r(d), not 2r(d). A same-parity pair d<e provides j=(e-d)/2 and precisely one of the two allowable charges. Its sign and first coordinate recover the original pair, so different pairs cannot collide. This proves the same-parity binomial lower bound. Three missing differences force a same-parity collision; splitting B by parity minimizes the two binomial terms at balanced sizes and yields floor((|B|-1)^2/4). Empty B and cardinalities1,2 give zero as required. No computation or unresolved ancillary assertion is used by this deduction.

The block construction's three pair-count terms count the two same-sign blocks and the positive-minus-negative block. Its breakpoint ordering follows from 2a>=n; the only zeros are a,a+1. Substituting n-2=3t+rho, a=n-1-t verifies the stated sufficient equality range in each residue class, including n=2,3,4. It establishes attainment for n>=2 and 1<=m<=floor(2n/3)+1, without proving necessity of the cutoff for arbitrary n. The row does not promote the proposed missing-pair characterization or uniqueness assertion to theorems.

The density implication must be asymptotic. At n=2, A={1,-2}, B={1,2}, the ordered count is zero. The proposed row explicitly avoids an all-small-n positive lower bound. For fixed positive epsilon, the proved bound does give the original asymptotic question; these finite exceptions are not a failure to answer that question. The abstract's broad sharpness language is qualified by the precise theorem and the proposed entry's restrictions.

As an additional finite attempt to falsify the central deductions, I authored a separate small checker rather than importing or executing an archived program. It checked all2046 signed sets for1<=n<=10,33448 same-parity pair charges, the exact half-defect budget, injectivity, equal-parity subset lower bounds, every B-cardinality lower bound including empty B, and the coverage conclusion. It also directly checked the explicit equality construction for2<=n<=100. All passed. This is bounded supporting evidence, not proof of arbitrary n, validation of every numerical assertion in the external note, or a rerun of the author's exhaustive suites.

## DOI, authorship and supporting files

The [DOI](https://doi.org/10.5281/zenodo.23006720) freshly resolved with HTTP200 to `https://zenodo.org/records/23006720`. Fresh API metadata says submitted=true, state=done, version1.0, publication date2026-09-28, resource type preprint, author Ferudun, Alper, affiliation Mercury Software GmbH, CC BY4.0. Title, author, date, version and DOI agree among provider, PDF, TeX, PR and proposed row. No Alec authorship, firstness, independent-discovery, human-peer-review or proof-assistant-certification claim is introduced.

Fresh file downloads matched provider sizes/MD5 and the root's independent SHA-256 pins:

| Deposited file | Bytes | SHA-256 |
|---|---:|---|
| Paper PDF |92822|25a5474f26518179b2b2a8db952868e6689c89adcdbc1a05156aa85cbbdd43ca|
| Source ZIP |39801|42f42f6d97a08726c9f8844df3c7791c36cf126ad3703c5d4534b529e5cd2a9e|
| Verification report |4701|1de29f590bf6269049ead9b0f5a76b354ac2f0179a367b878b9280b87152a9cd|

The ZIP contains20 unique safe members,15 regular files and5 directories; full CRC validation passed. The TeX, bibliography, license, report, reproduction instructions, five checker source files across the claimant/lead/two-referee families and five recorded outputs are present. The separately deposited report is byte-identical to the archived report. There is no promised but absent hash manifest. Paper and support are therefore deposited together, rather than relying on an unavailable private companion package. This establishes file coverage and identity; it does not certify that all recorded large computations have been independently replayed. No archived program was executed.

The PDF/source and public metadata disclose extensive AI assistance and unrefereed status. The repository audit independently states the same limitations. The row's file-verification sentence is supported by the download/identity/inventory checks; it is not a claim of formal computational or human certification.

## Duplicate challenge and proposed row

Fresh Google Workspace CLI read of `'Math Puzzles'!A:AQ` returned178 rows including the header. The first row is exactly Original Problem / Solution Chat URL / DOI / Notes. Result-identity searches across every returned cell for problem ID, source alias, DOI, title phrase, proposers and PR reference returned zero. A broader Ferudun search yielded20 leads, and a substring signed search yielded18 leads; their union contains30 rows. I examined their original-problem identities, DOI and mathematical scopes. They concern such distinct topics as billiard areas, trajectory laws, PDEs, polynomial factorization, skew braces, line configurations, chip-firing and birational cycle distributions. None represents this signed-representative difference result. Some broad matches are substrings of assigned, illustrating why title or token matching alone is insufficient. Full lead classifications are preserved privately.

The proposed row uses the exact four-column schema and intentionally leaves the chat-URL field empty rather than inventing one. It provides both problem identifiers, the correct OWR location, exact publication title, author/affiliation, version/date, resolving DOI, PR reference, exact accepted mathematical content and important scope limits. It explicitly says this is an existing external publication and credits Ferudun. It does not represent a new sweep publication. I find no factual correction necessary.

I inspected the root's prepared reconciliation script without executing it. It binds the accepted plan/review, reads the owned-account publication/draft inventory, rechecks PR/body/state, remote main, published metadata/file map and DOI, rereads the whole sheet immediately before append, writes a durable intent before a single append, refuses blind retry after uncertain outcome, and reads back a unique exact row/DOI. Its post-append readback cannot make the preceding provider or sheet snapshot permanently current; the remaining final live checks and any concurrent-race recovery belong to the root. The root's separate account receipt is not relabeled as this reviewer's independent authenticated account read.

## Decision and limits

**No substantive concern remains with this exact existing-publication accounting repair.** Final writer should retain the reviewed row and refresh duplicate/provider/account/PR/main checks as planned. A concurrent preexisting or changed row must be reconciled rather than duplicated. No new DOI deposit is warranted. This bounded review does not determine exhaustive historical priority or perform the sweep's separate merge decision, and it does not weaken the requirement for final append/readback verification.

This is an AI-assisted internal adversarial review, not conventional independent human peer review. All reviewer writes were confined to the assigned review folder. A read-only offline verifier and closed public/private SHA-256 inventories accompany it; these seals establish byte identity and completeness of the recorded review evidence, not mathematical truth.
