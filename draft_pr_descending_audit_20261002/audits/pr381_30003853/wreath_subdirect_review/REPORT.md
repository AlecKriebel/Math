# PR 381 restricted-wreath and simple-derived subdirect audit

Frozen candidate: `5b7bd8db9f34294d10862fed0f723055da864df6`. Exact target: problem 30003853 / OWR-16167-025, Röver–Sapir Question 111. This family independently audits Turns 1–3, focusing on restricted wreath products, solvable images, and simple-derived subdirect products. All five candidate proof files and all executable checks were read; mathematical acceptance below is scoped to this family. No candidate, queue, index, Git ref, or service was modified. No outreach occurred.

**Disposition: PASS for this family's scoped mathematical results. No mandatory mathematical repair found. The original question remains unsolved, 5/5 research turns.** This is neither novelty certification nor a full-solution or merge certificate. Audit-family completion: 100%; estimated discovery completion of the original remains the candidate's expressly subjective 18%.

## Independence and source grounding

`EARLY_INDEPENDENCE_SEAL.json` timestamps the independent reconstruction at 2026-10-03T03:04:10.795384+00:00, before candidate proofs/checks, historical review, final verdicts, or sibling/root verdicts were read. Its six SHA-256 bindings were rechecked after comparison. `INDEPENDENT_RECONSTRUCTION.md` contains complete independent algebra proofs; `new_algebra_checks.py` and its full result were also sealed before candidate inspection. The candidate's historical review was read only afterward. It agrees with this independently obtained family conclusion; its verdict is not an input to the proof.

The source question and surrounding example were independently fetched from [EMS OWR 26/2018](https://ems.press/content/serial-article-files/46748), printed 1624–1625, and both pages visually inspected. The question concerns all finitely presented subgroups of the dyadic finite-piece PL group F. The preceding Röver subgroup is finitely generated, with 2-torsion in its abelianization, and is not asserted finitely presented. The distinction is preserved.

For the wreath splitting dependency, [Bieri–Geoghegan–Kochloukova, arXiv:0807.5138v1](https://arxiv.org/pdf/0807.5138v1), p2 convention and p6 Theorem 2.7 including footnote 7, was independently fetched, read, and visually checked. It explicitly assumes FP_2 over a nonzero commutative coefficient ring and no nonabelian free subgroup, and supplies an ascending HNN decomposition over a finitely generated kernel subgroup with a stable letter generating the discrete character image. BGK is the precise primary-paper dependency used here; the original Bieri–Strebel proof was not newly obtained.

[Bleak, arXiv:math/0602038v2](https://arxiv.org/pdf/math/0602038v2), Theorems 1.1–1.2, Lemma 1.3 and terminal split-group argument/Corollary 4.8, was independently fetched and checked, with p2 inspected visually. Its standard wreath products and sums are restricted and its solvable groups have finite derived length. It embeds a solvable PL subgroup into G_n; it does not say arbitrary subgroups inherit a parent group's abelianization.

[Cannon–Floyd–Parry (1996)](https://www.imo.universite-paris-saclay.fr/~emmanuel.breuillard/Cannon.pdf), Theorems 4.1 and 4.5, independently supplies the actual F' kernel, Z^2 endpoint quotient, and simplicity input. This author-paper copy is on a university host; the E-Periodica publisher archive attempt returned verification HTML. [Guba–Sapir, arXiv:math/0301225v2](https://arxiv.org/pdf/math/0301225v2), Theorem 9.9, independently confirms free integral homology for diagram groups; its theorem does not automatically pass to arbitrary subgroups.

Raw source downloads, extracted text, images, and candidate runtime copy are in ignored local directories. Source metadata and hashes are in `SOURCE_RECEIPT.json` (the immutable early source receipt) and `ADDITIONAL_SOURCE_RECEIPT.json` (BGK). Independently downloaded EMS, Guba–Sapir, Bleak, and BGK PDF hashes match the corresponding candidate source manifests exactly. CFP is an additional source.

## Mechanism, evidence, status, exact gap

| Family | Mechanism and independent evidence | Status | Exact gap / boundary |
|---|---|---|---|
| Turn 1 FP_2 wreath obstruction | BGK gives finite kernel-base K; all K elements lie on one finite lamp support; a nonzero translating stable letter cannot preserve that support forward. For zero top projection, FP_2 implies finite generation inside a torsion-free abelian base. | Verified for the stated coefficient rings and restricted abelian lamps. | Does not cover an arbitrary F subgroup outside the stated wreath ambient group. |
| Röver ideal torsion | I_m=(m,x-1) in Z[x,x^-1]; H_m'= (x-1)I_m; the exact coinvariant map P -> (P(1)/m,P'(1) mod m) has a proved kernel and is onto. | H_m,ab=Z^2 direct sum Z/m, including trivial torsion at m=1. | All H_m have nonzero top and nontrivial base, hence fail FP_2 under the verified obstruction. The source example is not a finite-presentation counterexample. |
| Turn 2 subdirect products | H' projects onto each nonabelian simple derived factor; finite simple subdirects are twisted diagonal block products, self-normalizing in the derived-factor product. Thus H intersect product G_i'=H'. | Verified, including infinite simple factors; does not require H finite generation or finite presentation. | Every actual coordinate projection must satisfy the factor hypotheses. Proper small projections cannot be silently replaced by F. |
| Turn 2 congruence lattices | Full preimage of L contains the perfect kernel (F')^r, so H'=kernel and H_ab=L. Exact integer lattice basis has determinant m for the example. | Verified. Intrinsic H_ab is free although ambient quotient has order m. | An ambient finite quotient's torsion is not torsion in the lattice itself. Rational rank alone would not justify an integral kernel claim. |
| Turn 3 arbitrary-lamp image | The original FP_2 domain is split by BGK. Its finitely generated HNN base maps into finite lamp support. Lamp conjugations preserve nonidentity and top conjugation translates support exactly. | Verified with nonabelian lamps. | Nonzero top is necessary for the cyclic-image conclusion. No FP_2 assumption on the image is used or justified. |
| Turn 3 solvable images | Induct on Bleak G_n while retaining the original domain; finite generation reduces outer and inner restricted sums to finite products. | Verified: solvable PL images are abelian; solvable FP_2 PL subgroups are finitely generated free abelian. | No result for arbitrary nonsolvable or arbitrary elementary amenable images follows from this classification. |

The independent Röver calculation additionally proves H_m has index m in Z wr Z and is not finitely presented without using FP_2: omitted distance relators survive in an infinite graph RAAG semidirect Z. This is a consistency check on the finite-presentation scope, not a new target resolution.

The subdirect proof explicitly derives every required quotient map and kernel equality. For coordinate images F'<=G_i<=F, perfectness gives G_i'=F' and G_i/F'<=Z^2. A finite-index projection contains F' by the finite coset action and infinite simplicity. For a diagonal block, equality of inner automorphisms forces equality of coordinates after the twists because the simple factor is centerless. Hence a normalizing tuple belongs to the block. There is no appeal to rational saturation or to the false principle that subgroups inherit torsion-free abelianization.

## New exact adversarial controls

The new code imports no candidate code. Both scripts use only the standard library and this family's own arithmetic routines.

`new_algebra_checks.py` verifies 12 infinite restricted Laurent modules, with 100 random actual-group pair/character/derived-kernel checks per m=1,...,12; exact r-class order m and formal Laurent division include negative exponents. It computes rational ranks and maximal integral minor gcds for 84 cyclic lattices (m=1,...,12; n=2,...,8). Their torsion order is gcd(m,n), showing why a periodic truncation can erase the infinite-base torsion. All determinants and elimination use exact integers/rationals.

The same pre-comparison script constructs A5 from actual even permutations, checks perfectness, and enumerates normalizers in A5^2 for diagonal, outer-twisted diagonal, and full product cases. Each normalizer equals the subgroup. A new negative boundary uses the central extension G={(a,b,c):a,b in Z,c in Z/p}, product cross term ab' modulo p. G_ab=Z^2 and G'=C_p is simple but abelian. Its abelian-coordinate fiber product is subdirect, yet H_ab=Z^2 direct sum C_p. Exact commutators for p=2,3,5,7 demonstrate that nonabelian simplicity/perfectness cannot be omitted.

`nonabelian_and_lattice_controls.py`, added after comparison, checks 24,576 exact conjugations in a restricted wreath product with noncommuting A5 lamps, including negative/positive top displacements and nontrivial translating-element lamps; 1,000 actual associativity instances; and 2,790 nonempty finite-support shift obstructions. It reconstructs the full-rank congruence lattice integrally for m=1,...,12, proving unique coordinates, determinant m, ambient quotient order m, and intrinsic free rank 4. Full stdout files were inspected; stderr is empty and both results have `all_passed: true`.

These finite computations validate concrete algebra instances. The universal statements are checked by the written proofs plus the precise source inputs; the programs neither recognize FP_2 nor implement Bleak's geometric classification.

## Immutable bindings and full replay

All 45 files in the root snapshot manifest were independently read as bytes and compared in size and SHA-256 with their exact frozen Git blobs. **45/45 pass**, including the queue snapshot. `INPUT_MANIFEST.json` records every path, SHA-256, blob object ID, and content equality. This family did not audit the semantic queue diff or certify overall publication disposition.

Every candidate executable was read in full. An untouched candidate copy was placed in ignored `private_runtime/candidate`, with bytecode writing disabled. `REPLAY_ALL.py` exits 0 and reproduces the exact author assertion counts:

    17,826; 15,397; 75,294; 6,950; 447,168. Total 562,635.

It checks 26 historical bindings and **0 raw source bindings**, as required by the public replay mode. `verify_publication.py` exits 0 with the frozen public-hash PASS message and reproduces the historical independent 110,736-control stdout byte-for-byte. Both captured stderr files are empty. Full stdout and hashes are recorded in `REPLAY_RECEIPT.json`. The historical 20 local-only source binding claim is not represented as newly replayed by this family.

## Mandatory repairs and strongest verified result

No mandatory mathematical repair is identified in Turns 1–3. Retain all stated qualifiers: nonzero coefficient ring, no nonabelian free subgroup for the general-domain lemma, restricted supports, actual simple-derived coordinate projections, and finite derived length for the solvable classification. Retain `unsolved, 5/5`; none of these restricted theorems bridges to all finitely presented F subgroups. The central problem remains root-closure of the derived subgroup for an arbitrary finitely presented embedded subgroup, or an actual finitely presented embedded counterexample.

There was no sixth research search, no assertion of novelty, no merge or release certificate, and no contact with any individual. Descending PR 384/383/382 ordering is controlled by the parent audit; this family makes no independent disposition claim about those PRs.
