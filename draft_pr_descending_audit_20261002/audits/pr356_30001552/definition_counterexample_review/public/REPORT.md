# Definition and counterexample audit of PR #356

Audited frozen head `12fc989f8635fd202eb66b553b9599f0546d05d3`, original base `efd29c05204703acca9a0860812f54b94fae54b1`, problem `30001552 / OWR-4425-007`.

## Verdict and exact scope

**PASS for the submitted universal mathematical claim.** No definition substitution, unproved central assertion, or counterexample was found. The proof answers the stronger original alternating conjecture. Present historical priority and novelty are not certified. Computational and provenance qualifications below remain separate from mathematical correctness.

The original source is Dirk Nowotka's contribution, joint with Bastian Bischoff, in [Oberwolfach Report 37/2010](https://ems.press/content/serial-article-files/46296), DOI [10.4171/OWR/2010/37](https://doi.org/10.4171/OWR/2010/37). Complete printed pages 2219–2222 (PDF pages 25–28), including printed 2220 visually, were independently read before any candidate artifact. An immutable hash-pinned source baseline records the actual read scope and exposure. Root explicitly released candidate inspection only after reading it and checking its pins. All sixteen submitted problem files, the snapshot manifest, and only this target's queue row were then read. This family's provisional mathematical verdict was recorded before reading the submitted prior review or current sibling conclusions.

The exact conjecture following Theorem 23 says: for an arbitrary alphabet A and an antimorphic involution theta on A*, if positive integers p,q are alternating theta-periods of w and

    |w| >= p + q - gcd(p,q),

then gcd(p,q) is an alternating theta-period of w. Alternating means a prefix of (u theta(u)) repeated, for a seed of the proposed period length. Independently selectable u/theta(u) blocks and weak letterwise periods are different definitions. The source's later numbered Conjecture 27 is a different morphic bordered-word question. An imported unqualified theta-period conclusion is weaker; the submitted proof correctly supplies the original alternating conclusion.

## Independent proof check

An involutive antimorphism of a free monoid maps letters to letters and equals reversal followed by an involutive letter permutation tau. Fixed letters are permitted. This follows from bijectivity, preservation of the empty word, and the impossibility of decomposing a letter into two nonempty words after applying the inverse antimorphism.

For each alternating p representation, its two-sided 2p-periodic extension has twisted reflection s(-1-i)=tau(s(i)). The finite segment indexed from -|w| through |w|-1 is therefore exactly theta(w)w, with ordinary period 2p. The q representation gives ordinary period 2q to the **same** finite word. No endpoint phase or complete final block is required.

Its doubled length meets the classical Fine–Wilf threshold for 2p,2q and gives ordinary period 2g, g=gcd(p,q). The source states this credited classical theorem as Theorem 20. Since |w|>=max(p,q)>=g, the central interval [-g,g-1] exists. Reading its negative half through theta and propagating modulo 2g gives alternating blocks v,theta(v), where v is the first g letters of w. All compared indices lie inside the doubled word. This proves the target for every permitted alphabet, involution and positive period pair; finite scans are not the proof.

Equal periods, divisibility, coprime pairs, large gcd, incomplete blocks and fixed letters cause no exception. Empty w cannot meet the positive-period threshold. Period zero is outside the infinite nonempty seed convention. Periods larger than |w| are admitted by the prefix definition over nonempty alphabets but are automatically excluded by the threshold.

The reversal example w=abb, p=2,q=3 has both alternating periods at length 3 and lacks alternating period 1. It is one below the threshold 4. It establishes sharpness of the universal length formula by one, with no claim that each numerical pair has this exact optimum.

## Distinct finite falsifier mechanism

The source-only plan designed a signed positional graph and a separate literal block oracle. For each period r, every word position is equated to a seed position, possibly after tau. Signed components have a canonical model with distinct transposed letter pairs; if an odd signed cycle occurred it would force a fixed letter. Assigning disjoint orbits makes this canonical word a universal test of each fixed finite premise system: a missing signed equality fails there, while an entailed equality holds under every assignment and every alphabet involution. In this geometry edge signs equal endpoint parity differences, so all cycles are balanced. Fixed-letter instances remain covered as quotient assignments, and are tested explicitly too.

The independent BFS implementation uses literal repetition of seed+theta(seed) to verify both hypotheses and the gcd conclusion, rather than deciding the conclusion with its graph predicate. It passes **238,373 assertions**:

- all 20,100 unordered positive period pairs through 200 at the threshold;
- the same 20,100 pairs at length p+q-1;
- all 2,224 additional interior lengths between those endpoints for periods through 50;
- exhaustive unary, binary reversal, reverse complement, ternary reversal, and ternary/quaternary involutions with fixed letters, with empty and short prefixes;
- the submitted sharpness witness and explicit involution/convention checks.

It also constructs 19,002 failed gcd examples **below** the threshold. These falsify stronger bounds, not the conjecture. The expected output records the exact finite domains and first twenty witnesses. Finite period coverage remains supplemental even though each graph instance covers unrestricted alphabets; the independent proof check supplies the unbounded result.

The reflected-word mechanism genuinely needs its stated premises. Morphic identity with w=010,p=2 gives theta(w)w=010010 without ordinary period 4. Morphic complement with w=01,p=1 gives 1001 without ordinary period 2. Freely mixed reverse-complement blocks with w=001,p=1 give 011001 without ordinary period 2, and w is not alternating of period 1. These are excluded-scope controls, not target counterexamples.

## Frozen receipt and binding audit

All seventeen snapshot bodies match their SHA-256, byte length and independently computed Git blob-object hashes. All seven author, three review and fifteen publication-manifest bindings recompute correctly. This family did not inspect local repository history/objects; root's literal local Git binding was pending at audit time and is not certified here. Recorded API/ancestry/mode facts remain root evidence, distinct from these disk/hash checks.

| Saved receipt | Present reproduction | Exact stdout SHA-256 |
|---|---|---|
| TURN_1_CHECKS.json: 526,887 | PASS, all 252 bytes equal; includes 18,316 binary qualifying ordered pairs and 5,050 finite universal-alphabet graph pairs | `096fbd7ca92331f9d24a0758838e69d4dab14a1ce25f7277d008674385b246fb` |
| review/PORTABLE_CHECKS.json: 68,408 | PASS, all 233 bytes equal; seven author hashes plus 68,401 mathematical assertions | `0bc638bb0128e1fbc33b8957cf3fe3de4e1dc73b6dc9b6ee1dcce002ac9b8aad` |
| review/INDEPENDENT_CHECKS.json: 68,413 | NOT reproduced; literal program fails at its fixed original machine path and needs five original private source files | No successful stdout |

Pre-execution candidate pins, exact stdout/stderr streams, failure traceback and post-execution unchanged pins are retained privately. The failed original run exited 1 and its stderr SHA-256 is `5fcafbed42351b86a288466cffebc4ee5621edc4c16d7736c3284b42856fbd77`. The optional source-root mode was not run without the complete authorized original five-file bundle. The official OWR PDF matches its submitted source hash; four other original source artifacts were unavailable here. Reconstructed differing bytes and hardcoded expected counts were never substituted.

The hardcoded path/private source dependency is a supplemental portability and current coverage issue. It is accurately separated from the successfully reproduced public checks and from the valid universal proof. Historical prior-search statements, original AMS retrieval failure, fresh-main integration and claimed old all-source verification were not independently replayed by this family. No present novelty follows from a null imported research record. No candidate editing, install, Git mutation, external person contact, merge, release or formal certification was performed.

The included verifier and expected output provide a reproducible independent falsifier artifact using Python's standard library. Its output SHA-256 is `4ec27bea435a5ac8b9c3c0030854c1ea8a41a9db97d99ed95e8daf72996da336` (8,380 bytes). Package closure requires root's complete read and explicit approval; this report does not self-authorize sealing or a status change.
