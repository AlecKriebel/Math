# Independent scope and primary-literature review — Zenodo 23387753

Scope conclusion: no publication-scope defect identified. Candidate page content remains conditional on separate analytic and adversarial mathematical gates. This is a scope and attribution review, not a mathematical proof certificate or a novelty certificate.

The independent conclusion was logged at 65% before consulting any archived or sibling mathematical review verdict. Read all five pages of the fresh published note and the full original authored `source/author/PROOF.md`. Earlier audit reports were not read as grounds for this verdict. Package README statements about verification are provenance information, not independent mathematical evidence.

## Published edition and source completeness

The fresh record is [Zenodo 23387753](https://zenodo.org/records/23387753), DOI 10.5281/zenodo.23387753. The metadata and manuscript agree on 2026-10-15 and version 1.0.0.

Both published assets were acquired directly. `finite-energy-percolation-note.pdf` has five pages. `finite-energy-percolation-verification.zip` contains 108 members; its only PDF is `note.pdf`, byte-identical to the separately published manuscript. No supplementary PDF was omitted. All 107 `package_index.json` entries passed byte-count and SHA-256 comparison; the index itself is the remaining unlisted member. Both published assets pass fresh-record MD5, receipt SHA-256 and size checks, and the ZIP passes CRC. See `source_integrity.json`. Integrity checks authenticate published bytes and do not verify the infinite proof.

The complete original abstract is in `content.json` with only whitespace and mathematical typography normalized, including its no-first-priority sentence. AI disclosure is a separate status field.

## Exact claim and public boundaries

For every d ≥ 2 the note constructs a bond law on nearest-neighbor Z^d that is invariant under every lattice graph automorphism and mixing under translations. Ordinary finite energy means that, after revealing all other output edges, any edge's conditional open probability is strictly between zero and one almost surely. No common positive lower bound is required.

The realized graph X almost surely has exactly one infinite component C. Fix that realization before introducing independent Bernoulli bond thinning. The internal bond thresholds of X and C are one; their internal site thresholds also equal one. This is an almost-sure quenched graph statement, and finite components are allowed. It does not say every vertex belongs to the infinite component. The external process is a bond law; the site conclusion concerns subsequent independent thinning within that graph.

The more general kernel needs a countably infinite connected simple bounded-degree graph and a connected one-ended spanning tree T. Delete a tree edge t with probability 2^(−s_T(t)), where s_T(t) is its finite-side cardinality; insert a non-tree edge e with probability 2^(−M_T(e)), where M_T(e) maximizes s_T along the unique tree path joining e's endpoints. Choices are independent conditional on T. A disconnected high-dimensional uniform spanning forest cannot replace that tree, because some required paths would be absent.

Small conditional probabilities given the hidden tree do not establish that marginal finite energy has no uniform lower bound. The page therefore neither claims uniform energy nor asserts its failure. No finite coding radius or quantitative mixing rate follows from the stated factor representation.

## Mechanism and added contribution

Finite sides along a one-ended ray increase and exhaust the graph. Every ambient bypass crossing a finite side has a tree path containing its separating edge. The maximum-along-path insertion rule bounds the total deletion/bypass probability by a summable series. Eventually each such boundary has exactly its retained tree edge as the sole crossing. Retained ray tails coalesce, giving uniqueness of the infinite component. Any independently thinned infinite path must retain arbitrarily many distinct bottleneck edges or vertices, with probability at most p^k.

Ordinary finite energy survives averaging over the hidden tree by conditional expectation of strictly positive open and closed probabilities. The kernel commutes with automorphisms. Timár's factor-of-iid tree input supplies an equivariant one-ended connected tree in all lattice dimensions under consideration, and a measurable equivariant factor of the joint iid marks inherits translation mixing.

The surprising feature is that an infinite cluster persists under an ordinary-finite-energy law yet every nontrivial independent thinning destroys infinity. The proposed specific contribution is the dimension-independent bypass rule and its eventual singleton-cut conclusion, plus an explicit consequence of an older planar model. First priority of either is not certified.

## Primary literature and credit boundaries

- [Benjamini–Tassion, arXiv:1505.06069v1](https://arxiv.org/html/1505.06069v1), §1.2 Question 1: inspected the exact ordinary-finite-energy existence question and the distinct everywhere-percolating sprinkling theorem. This confirms the target without confusing fixed-density sprinkling with tree-dependent rates.
- [Benjamini–Häggström–Schramm, arXiv:math/9906002v1](https://arxiv.org/abs/math/9906002v1): original abstract/metadata inspected. The exact historical question was cross-checked in Benjamini–Tassion, not by pretending the full original BHS proof was read.
- [Häggström–Mester, arXiv:1011.2872v1](https://arxiv.org/html/1011.2872v1), §2 and the beginning of §3 including Lemma 3.1: read the older ordinary-finite-energy site-flip construction and threshold discussion. The journal DOI is [10.1214/ECP.v14-1446](https://doi.org/10.1214/ECP.v14-1446). The accessible body inspected was the authors' arXiv text, not a downloaded publisher PDF whose identity had been independently verified.
- [Timár, arXiv:1805.10690v1](https://arxiv.org/html/1805.10690v1), Theorem 1, Corollary 2 and factor definition: inspected the actual connected one-ended factor-of-iid spanning-tree input and its hypotheses. It applies to deterministic rooted Z^d for d ≥ 2.
- [Pemantle, arXiv:math/0404043v1](https://arxiv.org/abs/math/0404043v1): identified as the classical UST input credited by the note and earlier planar work. The full original body was not independently re-read in this scope task; the all-dimensional argument here uses Timár instead.

Häggström–Mester must receive more than a similarity citation: their summable finite-past perturbation is the planar mechanism. The note's precise fixed-phase midpoint projection preserves the old rates, with all coarse vertices present. It is a coordinate marginal, not the induced bond graph on final open sites. The new note supplies a bounded-cutset argument for threshold one; that post-flip deduction is not a theorem stated in the inspected antecedent. The earlier site/bond threshold comparison alone does not convert external finite energy. This distinction supports neither an assertion that HM explicitly solved the later-restated bond question nor a verified first-resolution claim for the current note.

The all-dimensional maximum-path-size rule avoids dependence on a planar dual tree and yields eventual singleton cuts rather than only a subsequence of bounded-size cuts. These are precise contribution descriptions, with no exhaustive priority certification.

## Page decisions

The draft preserves the full abstract and explicit prior credit, describes the internal threshold in ordinary language, separates external bond energy from internal site thinning, and labels the note unrefereed and extensively AI-assisted. It invites substantive collaboration on the mathematics and journal preparation without promising authorship. The PDF and original verification ZIP suffice; there are no additional assets.

`follow_up` is null. Uniform-energy variants, coding-radius bounds and quantitative mixing rates are broad possibilities requiring distinct mechanisms and further literature comparison. None is advertised merely to fill a follow-up section. No published proof or asset was repaired or changed.
