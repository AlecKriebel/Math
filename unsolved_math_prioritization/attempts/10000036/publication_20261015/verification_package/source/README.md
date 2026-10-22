# Invariant finite-energy percolation with internal threshold one

Problem **10000036 / AMR-099-0036**, rank 875. This package presents an affirmative proof under the source question's **ordinary, nonuniform finite-energy convention**, accepted without mathematical correction by two independent written AI audits.

## Exact accepted result

For every integer **d ≥ 2**, there is a bond-percolation law on nearest-neighbor **Z^d** which is invariant under every lattice graph automorphism, mixing under translations, and gives both states of every edge strictly positive conditional probability given all other output edge states. Almost surely the resulting graph X has exactly one infinite component C and its quenched internal Bernoulli bond thresholds satisfy **p_c(X) = p_c(C) = 1**. The manuscript's additional internal site-thinning conclusion is also accepted. Finite components are permitted.

The proof uses Timár's established [one-ended factor-of-iid spanning-tree theorem](https://doi.org/10.1214/19-ECP274). Tree-dependent insertion and deletion rates leave eventual singleton boundaries along every original tree ray. These boundaries survive in X, while every independent thinning with p < 1 must retain infinitely many distinct prescribed edges to percolate. The conditional-expectation argument establishes ordinary finite energy after the hidden tree is forgotten. Häggström–Mester's [summable-flip construction](https://doi.org/10.1214/ECP.v14-1446) is expressly credited as a close antecedent.

## Proof and review

- [Unchanged author proof](author/PROOF.md), [three-approach record](author/APPROACHES.md), [review guide](author/AUDIT_GUIDE.md), and [historical author status](author/STATUS.md)
- [First independent audit](independent_audit/AUDIT.md) and [separate acceptance](independent_audit/ACCEPTANCE.md)
- [Second independent adversarial audit](second_independent_review/SECOND_ADVERSARIAL_AUDIT.md) and [separate acceptance](second_independent_review/SECOND_ACCEPTANCE_REPORT.md)
- [Publication acceptance](PUBLICATION_ACCEPTANCE.json), [static test results](PUBLICATION_TEST_RESULTS.json), and [exact publication inventory](PUBLICATION_MANIFEST.json)
- [Author public-source metadata](author/SOURCES.json), [first source checks](independent_audit/SOURCE_VERIFICATION.json), [second source checks](second_independent_review/SECOND_SOURCE_VERIFICATION.json), and [public dataset verification metadata](second_independent_review/SECOND_INPUT_VERIFICATION.json)

No mathematical correction or derivative proof was required. The author and both review freezes, their ZIPs, and external manifests are preserved byte-for-byte. Historical pending-review and not-yet-published statements inside them describe their freeze time; the later separate acceptances and this publication wrapper record the subsequent disposition without replacing those historical bytes.

## Scope and status limits

No uniform finite-energy conclusion is asserted. Neither finitary coding, finite dependence, positive association, nor a claim that every vertex percolates follows from this package. The existence theorem for the input tree is an explicitly cited external dependency, not re-proved here.

Mathematical acceptance is not a verified novelty, priority, first-solution, live catalog status, journal-acceptance, human-peer-review, or proof-assistant claim. Bounded literature searches found no exact prior resolution but cannot establish its absence. The queue status is **claimed_solved**, with **3/5** substantive approaches used; no new approach was added in review or publication.

## Byte and publication boundary

The three archives contain fifteen regular Markdown/JSON data members in total and no executable mathematical checker. Publication preparation checked fixed external archive and manifest pins, exact inventories, every member, strict UTF-8/JSON formats, and the bindings between the unchanged author proof and both acceptances. Twenty-one corruption and safety controls rejected the expected bad inputs in each of isolated normal and optimized Python modes. These are static byte/safety checks; they do not prove the mathematics.

Only authored mathematical proof/audit/acceptance text and public verification metadata are included. Source PDFs, extracts, images, raw dataset records, private sources, personal data, private coordination material, and private checker fingerprints are excluded. Public citation links, source titles and status, retrieval/inspection history, and source/dataset hashes and sizes are retained where already recorded.

Only the current queue row's Status, Turns and Findings cells change. All unrelated queue content, notes, and chat links are preserved. This is a draft review package with no CI-pass claim; exact remote verification is a separate post-publication check.
