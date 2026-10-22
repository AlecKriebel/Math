# 2303019: Barth's tangential-limit question was settled by Aikawa

**Recommended status:** `already_solved`  
**Substantive verification turns:** `1/5`  
**Attribution:** Hiroaki Aikawa, 1990. No campaign novelty or priority claim.

For every fixed tangential path in the unit disk ending at 1, Aikawa constructed one bounded real harmonic function whose limit fails along every rotation of that path. A positive affine normalization settles the exact positive-harmonic question. The quantifier is every rotation of the fixed path, without an exceptional set of angles.

The exact source question and its affirmative resolution appear together in Hayman–Lingham, [Problem and Update 3.19, printed p.66](https://arxiv.org/abs/1809.07200v2). The resolving article is Aikawa, [*Harmonic functions having no tangential limits*, Proc. AMS 108(2) (1990), 457–464](https://doi.org/10.1090/S0002-9939-1990-0990410-X). Aikawa's [1991 follow-up, Section 1, Theorem A](https://www.isc.chubu.ac.jp/aikawa/research/AikawaPapers/har.pdf) repeats the exact disk result.

[PROOF.md](PROOF.md) gives a complete, attributed reconstruction, with all nontrivial geometric and analytic estimates. It builds real boundary data in [-1,1], obtains a Poisson integral h with liminf <= -1/4 and limsup >= 1/4 along every rotated path, and takes v=(h+2)/4. Thus 1/4<=v<=3/4 and the limit cannot exist even in the extended real sense.

The imported report's assertion that the question was open in the 2018 edition is contradicted by the update printed immediately after the question. The imported source statement is a historical question; its standalone `open` label does not represent the current mathematical status.

## Verification and limits

- Full proof reconstruction completed. The exact original target has no remaining mathematical gap under the source's standard tangential-path hypothesis.
- Standard dependencies: continuity, compactness, elementary Lebesgue integration and dominated convergence, and Poisson-kernel harmonicity/normalization, described in the proof.
- Twelve families of exact finite controls pass. These check supporting algebra, grid coverage representatives, overwrite invariants, tail arithmetic, and positive normalization; the analytic proof establishes the infinite and all-path assertions.
- This author package is frozen for independent review. It does not itself assert that an independent audit has passed.
- No claim covers disconnected sequential approach sets, nontangential paths, or one universal function for every initial path at once.

See [SOURCE_AUDIT.md](SOURCE_AUDIT.md), [APPROACH_LOG.md](APPROACH_LOG.md), and [validation.json](validation.json). Run `python3 controls.py` to reproduce the finite controls and `sha256sum -c MANIFEST.sha256` to check package integrity.
