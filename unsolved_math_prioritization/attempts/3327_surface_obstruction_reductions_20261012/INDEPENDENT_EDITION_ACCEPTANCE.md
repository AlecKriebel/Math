# Independent acceptance review: first surface-obstruction edition

## Verdict and exact scope

**Accepted as a complete, recoverable edition of partial results, not as a solution.** The reviewed base edition is the first newly documented substantive investigation of problem 3327 / OPG-172. The lifetime attempt count is unknown. It does not reset an investigation budget or assert the absence of earlier work.

The mathematical target remains a finite ordinary graph G and h≥1 for which G does not embed in N_(h+1), although every proper minor embeds in N_h. Deletion, contraction, simplification, and isolated-vertex deletion are included. Connectedness is not assumed. No example and no universal nonexistence proof are established. Nothing from a later investigation is part of this acceptance.

The base edition contains eleven public files, totaling 89,082 bytes, including its manifest. The ten files listed by that self-excluding manifest total 87,062 bytes. The manifest SHA256 is cd42ee4cc48296552f957df78f680e326124f257be5e618b4665c0b331d59483. This acceptance report is a separate artifact and is not counted in that base manifest.

The reviewed public [structural report](STRUCTURAL_REPORT.md) has SHA256 e1f494f6e4961cdde99ade0a244a2d41d297ac823cedff23e8bfc3afbbf32177. The reviewed public [mathematical audit](INDEPENDENT_AUDIT.md) has SHA256 eb9ba8a1ff72d077eb4e5eb12c0ab91ef635d057a0635ce6a519aceaea70b17d. Both complete texts, the [source audit](SOURCE_AUDIT.md), the [K4,4 proof](K44_N2_PROOF.md), and the [certificate guide](CERTIFICATE_GUIDE.md) were read. Their proofs were assessed as mathematical arguments, not accepted solely because hashes or test runs matched.

## Mathematical acceptance

### Genus convention and existence reduction

The invariant ν is minimum positive nonorientable genus, so planar graphs and forests have ν=1. Euler genus E is distinct. The correction σ=ν−E belongs to {0,1}, with σ=1 only at even Euler genus. The original block theorem is used with the stated cyclic/nonplanar qualification and the disk-placement treatment of planar attachments; the cellular convention assigning zero to trees is not substituted into the positive-surface formula.

Restoring one missing edge with a handle proves ν(G)=h+2 and ν(G−e)=h for every edge of a target. There is no asserted equal-drop rule for contractions. The orientably simple case is exactly Euler criticality: parity handles the top minor genus r−1. In the σ=0 case the correct condition is an ordinary Euler hopper together with exclusion of a proper minor at E=r−2, σ=1. The exceptional case is automatic only when r is odd.

Doubling a σ=0 hopper is valid because the untouched copy forces the correction to zero. The resulting nonorientable genus is 2r, and an elementary minor has genus at most 2r−2. Planar changed summands and isolated-vertex coverage are treated explicitly. Positive-genus block reduction is an existence reduction, not an assertion that every target is 2-connected. These arguments support the stated equivalence with a positive orientably simple Euler-critical ordinary graph or a positive ordinary Euler hopper. They do not supply either object.

### Triangle exclusion and minimum degree

Campbell's Lemma 5.3 is correctly credited. Its local reversal of a consecutive rotation block, with corresponding edge-sign changes, merges the two relevant faces and adds a crosscap. After insertion of the missing triangle edge, the negative cycle gives the nonorientability check. The arbitrary-graph extension uses componentwise Euler-minimum embeddings and connected sums, rather than incorrectly assuming a cellular embedding of a disconnected graph.

The cubic reconstruction is exact: contract uv at a triangle-free cubic vertex u with other neighbors a,b; subdivide the uniquely produced edge va by u; add ub using the path u-v-b; then delete vb. Triangle-freeness is necessary to prevent suppression of a pre-existing va or vb from invalidating the reconstruction. The bound ν(G)≤E(G/uv)+1 contradicts the target, ordinary-hopper, and orientably-simple-critical hypotheses. Thus triangle-freeness and minimum degree four survive unchanged.

### Density, h=2, and squares

The deletion graph has minimum degree at least three, so its facial walks have length at least four in componentwise cellular Euler-minimum embeddings. Combining m≥2n with m−1≤2n−4c+2h gives h≥2c, hence h≥2. The auxiliary positive-genus blocks have Euler genus at least four. The conditional tight-girth exclusion keeps its essential nonforest qualification.

For h=2, connectedness and ν=E=4 leave m=2n or 2n+1. Contracting an edge creates no parallel copies, and counting triangular faces in the contraction gives at least two or four squares through the original edge, respectively. The nonconsecutive-corner argument uses an actual N_h embedding of the deletion graph. Its common-neighbor bound and matching restriction are valid; they are not a general global quadrangulation assertion.

In the degree-excess case every quartic vertex would need two high-degree neighbors. One degree-six vertex cannot provide them; two degree-five vertices force each quartic vertex to have only those two neighbors by triangle-freeness. This contradiction establishes quarticity. Every h=2 edge consequently lies in two or three squares, and K_(2,3) is excluded.

Attaching disks to all squares in the all-two-square case gives circular vertex links and Euler characteristic zero, excluding a target. At order eleven, the equality case in the two-step-walk count forces 66 vertex-square incidences, not divisible by four; hence order is at least twelve. The edge-deleted Klein-bottle face excess is two, giving one length-six walk or two length-five walks. No unwarranted simple-boundary assertion is used.

The 3-connected conclusion is correctly limited to h=2 and depends on Mohar–Škoda Part I. The exact proof of Theorem 5.11 rules out Euler genus above three in the connectivity-two threshold-critical class; the mere count of 668 graphs is not used as a substitute. Together with the block argument this excludes connectivity two for the putative Euler-genus-four target. The complete classification computations were not independently rerun.

## Independent certificate checks

### K4,4

A fresh verifier reconstructed the sixteen cross edges and validated every cyclic order and signature in the [complete certificate](K44_N2_CERTIFICATE.json). Its face permutation has 64 signed darts, sixteen directed boundary orbits, and eight geometric quadrilateral faces. Each graph edge occurs twice among those faces. The surface has χ=8−16+8=0. An independent vertex-sign consistency test fails, and the stated cycle has sign product −1, proving nonorientability. Thus the certificate is an actual N_2 embedding, not an inference from Euler genus two alone.

This verifies the supplied small-order argument: triangle-free minimum degree four forces at least eight vertices, and equality forces K4,4; that graph embeds in N_2, so every target has at least nine vertices. No complete-bipartite genus formula or obstruction catalogue is needed.

### Co-Heawood

A fresh verifier reconstructed the Fano lines from binary vector addition, the fourteen labelled vertices, twenty-eight nonincidence edges, and all twenty-one distinct squares. It checked quarticity, bipartiteness, the common-neighbor bound, and exactly three squares per edge.

Every state of the [complete eleven-node exact-cover tree](COHEAWOOD_SQUARE_CERTIFICATE.json) was checked independently: chosen squares, remaining-edge masks, the minimum-choice branch edge, all eligible choices, every child, all failed leaves, and exact reachability of the entire node set. No branch may be omitted. Independently, all 116,280 seven-square subsets were enumerated and none partitions the edges.

An Euler-genus-two embedding would require fourteen distinct quadrilateral faces, making the seven omitted squares an edge partition. Its impossibility therefore proves E≥3 for this graph. This edition does not establish an N_3 embedding, E=4, ν=4, or minor-minimality. It makes no claim about results obtained after this edition's investigation.

## Executed checks and hostile controls

The new independent semantic checks ran successfully in normal Python, -O and -OO, with byte-identical outputs. Eighteen malformed or false mathematical certificates were rejected, including omitted and repeated K4,4 edges, invalid rotations, false face/orientability claims, a false negative cycle, all-positive signatures, omitted co-Heawood squares or branches, stale masks, duplicated children, false leaves, and stronger unproved genus claims.

Nineteen additional independent edition controls rejected corrupted or missing actual source bytes, unsafe source paths, recursive old archives, incomplete or false reverse maps, public executable and internal-path leaks, broken links, false solved/lifetime-count/classification-replay statements, false PDF metadata, and copied third-party source text. Semantic tests were called directly on the changed mathematical objects, so their rejection does not rely merely on an unchanged digest.

The retained earlier finite-reduction checker was also rerun in all three modes. Its outputs matched exactly: 1,425 orientably-simple criterion cases, 2,788 σ=0 criterion cases, 2,611 doubling cases, 6,229 small triangle-free labelled graphs, 16,872 cubic reconstructions, 31,321 contraction/square correspondences, and the stated local signed-rotation families. These are bounded regression checks supporting the prose proofs. They are not exhaustive searches for hoppers or proofs of arbitrary-genus nonexistence.

## Complete text, sources, and recovery

Ten source-to-public maps were checked forward and backward over the entire text, including every unchanged span and every edit. The structural report's changes are heading/history normalization, public links, and removal of operational material. The mathematical audit's changes are a public structural-report link and wording that does not promise an accompanying executable. No proof was replaced by a digest or an abridged summary. The source audit, K4,4 proof, and both mathematical certificates are unchanged.

All twenty-four local links in the base edition resolve. The public boundary contains only authored prose, source-identity metadata, the two small exact mathematical certificates, and their byte manifest. It contains no executable, third-party PDF, extracted source document, private source, personal data, or private coordination material. A fifty-word source-overlap check also found no copied source passage in the public prose; this is a supplemental mechanical check, not a copyright adjudication.

Original cited-source bytes are recoverable, including all seven PDFs identified by the public metadata. Each PDF's actual hash, size, and PDF header were verified against the retained byte objects. The complete source pool is content-addressed and contains no recursively embedded old archive. Actual archive extraction and an independent content-addressed byte-store restoration reproduced the frozen preparation and the review materials. Complete inventories, source maps, public gates, and mathematical certificate checks were rerun on restored bytes. Hashes identify those bytes; their existence and successful restoration, rather than hashes alone, establish recovery.

## Source and conclusion boundaries

The [source audit](SOURCE_AUDIT.md) distinguishes the 2020 preprints from the 2024 journal publications and states the bounded nature of the later-literature search. The present review directly inspected Campbell's Lemma 5.3, the positive-crosscap and cellular distinctions in Parsons–Pica–Pisanski–Ventre, and the exact low-connectivity genus argument and block formula in Mohar–Škoda Part I. The original Stahl–Beineke 1977 proof was not independently read in full. The source classifications and their computer dependencies remain credited inputs.

This is an independent mathematical and computational acceptance review, not human peer review. No novelty claim or certificate of current global open status is made. The accepted h=2 conditions are necessary, not sufficient, and the unrestricted arbitrary-genus target remains unresolved by this edition.
