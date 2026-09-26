# Independent hostile algebra review, round 1

Reviewer: algebra subagent, independently encoded checks. Final checkpoint: 2026-09-26 04:58 UTC (2026-09-25 21:58 PDT). Assigned review completion estimate: **100%**; this is completion of this audit, not a probability that no error exists. No manuscript edits, commits, pushes, or external communications were performed. Public sources were read without contacting their authors.

## Scope and exact target

Reviewed `exceptional_ybe_d4/main.tex`, sections 2–4 and 7–8, against the snapshot with SHA-256 `9ef5716ef8c663ae0cb012899b4eea67a7500fee6006e2ce0e3f61e99803f51c`.

Targets: the literal five-word operator is a unitary ordinary YBO with the asserted spectrum and partial traces; the complete cubic residual is exactly the printed 18-word certificate and has precisely four solutions on the real reflection circle; the swap/blocking identification respects all tensor placements; the quaternionic factorization and literal displayed S satisfy the stated identities. External comparison targets were the cited literal GHR matrix and the GR §13.2 formulas.

I first read the manuscript, derived the checks, and wrote a fresh verifier without reading any earlier audit reports or production verifier. After identifying the GHR source issue independently, I inspected only the relevant production code to locate its mechanism. No earlier audit reports were read at any stage.

## Finding A1 — source-to-code mismatch in older GHR matrix comparison

**Severity: material correction required before submission (P2); peripheral to the new construction and localization theorem.** A claim of literal source fidelity is false for the accessible preprint. Whether the journal typesetting corrected the preprint is unverified, so this is not a claim that the journal contains the same defect.

**Locations:** main.tex lines 869–902, especially the residual table at 886–889, the same-spectrum assertion at 894–897, and repeated references to the displayed GHR operator. Production `verify_exact.py` lines 459–484 explicitly claim a literal transcription and use a common prefactor; lines 486–508 label their resulting fingerprint as literal.

**Mechanism:** [GHR's author-hosted preprint](https://people.tamu.edu/~rowell/GHRarx1.pdf), p.26, Eq. (5.2), visually puts the factor `−exp(−πi/3)/sqrt(2)` on its first 4×4 block and `1/sqrt(2)` on its second block. The same mixed-prefactor display occurs in [arXiv:1105.5048v1](https://arxiv.org/pdf/1105.5048). The production verifier applies `−exp(−πi/3)/sqrt(2)` to both blocks while saying both displayed blocks have that factor. It checks a different matrix.

Let q=(1+i√3)/2. A completely fresh dense transcription of the visually inspected preprint gives:

| Check | Literal mixed-prefactor preprint | Common-prefactor matrix used by code |
|---|---:|---:|
| trace | 1+i√3 | −2+2i√3=4(q−1) |
| characteristic polynomial | (t+1)²(t−q)⁴(t−q̄)² | (t+1)⁴(t−q)⁴ |
| squared Frobenius norm, shift 1 residual | 30 | 0 |
| squared Frobenius norm, shift 2 residual | 60 | 48 |
| squared Frobenius norm, normalized Hecke residual | 18 | 0 |

A trace discrepancy alone excludes the claimed same-spectrum comparison. More strongly, the literally printed preprint matrix fails even the asserted (3,1) generalized braid equation. Its zero-based residual entry (0,0) at shift 1 is `(1−i)(−√3+3i)/8`, so this is not numerical noise or a norm convention. These values are independently asserted in `evidence/algebra_ghr_source.py` and printed in `evidence/algebra_ghr_source.txt`.

The common-prefactor matrix is mathematically sound and can be explicitly defined without making a claim about source fidelity:

`K_common = −q̄/2 · (III + i IXI − i ZZZ + ZJZ)`.

Its shift-1 residual is zero, its shift-2 residual norm² is 48, and its required shift-2 far commutator is zero. However, these facts do not retroactively make it a literal transcription of the accessible preprint.

**Concrete repair:** remove the unnecessary old-matrix residual/same-spectrum comparison from the manuscript, retaining the intrinsic checks `||Y_1(K)||_F²=24` and `Y_2(K)=0`, and cite the GHR localization theorem only for the existence of the known (3,1) localization. If retained in a supplement, independently DEFINE the common-prefactor matrix, label the difference from the accessible preprint, and remove every assertion of literal transcription/fingerprint fidelity. Include the mixed-prefactor negative check so later readers cannot silently erase the distinction. Do not infer or assert the original authors' intent or claim an unverified journal typo.

The parent proposed precisely this disposition during review; I endorse it. The manuscript's ordinary YBO, generalized blocking, quaternionic comparison with GR, and core localization proof do not depend on this defective source identification.

**Primary evidence retained locally:** `tmp/pdfs/algebra_GHR.pdf` (SHA-256 `099639fe71b91addb538010127245d53db210676b66ae836f823acee8a40794b`) and visually inspected page rendering `tmp/pdfs/algebra_GHR_p26.png` (SHA-256 `5bf27c061b224a0bbdc20c70326706ce65006c960c411eae44885e75d452c144`). These are research-source evidence, not proposed publication assets. The journal landing page did not yield an accessible full text; the source reviewer independently reported the same access limitation.

## Verified claims and attempted falsifications

### Sections 2–4: five-word matrix, reflections, full converse

No defect found. Fresh `evidence/algebra_independent.py` encodes each word as X^x Z^z and computes the product sign from `(-1)^(z·x')`, rather than copying the printed multiplication table. It independently obtains exactly all 18 displayed residual words with exactly their coefficients. This is an unrestricted polynomial identity in α and β, not merely equality modulo the circle relation.

Adding α²+β²−1 to the residual coefficient ideal produces the exact reduced Gröbner basis

`[α²−2/3, β²−1/3]`.

Thus the converse is exact, there are no overlooked real/complex circle points, and no nonzero parameter was divided out illicitly. All four signed candidate points pass; the four axis endpoints fail. The printed edge-case coefficients agree.

Independent literal 2×2 Kronecker matrices also confirm symmetry, involutivity, pairwise commutation of A–D, D=ABC, and anticommutation with E. The graph-phase identity was checked on all eight bit triples. H²=I, trace(H)=0, both partial traces of H vanish, R is unitary, its normalized Hecke polynomial vanishes, and the ordinary braid residual vanishes exactly. A separate dense contraction gives both partial traces of P equal to 2I4. Multiplicities follow from the verified Hermitian involution and trace.

### Section 7: tensor ordering and generalized blocking

No defect found in Proposition `prop:gybe` or the general blocking observation. Swapping each adjacent qubit pair in all five words produces exactly `I ⊗ K_H` with the displayed signs, including the order-sensitive `JJZ−JZJ` pair. Generator placements were independently checked for every i and n=2,…,7; the general mechanism is the explicit word-position identity and does not rely on extrapolating these finite samples.

After sitewise swapping, ordinary generator i starts with its own spectator and K acts on qubits `2i,2i+1,2i+2`. Removing the single global first qubit leaves K starting at `2i−1` in the remaining chain, exactly the claimed generalized placement. Adding a site adds two trailing qubits. Distant triples are disjoint. This proves the claimed chain conjugacy, tower compatibility, and equality of kernels for all n≥2. Faithfulness on H_n is conditional only on Proposition `prop:markov`, outside this assigned algebra scope.

The independently computed intrinsic residual norms are exactly 24 at shift 1 and 0 at shift 2. The statement that any (3,2) operator blocks to an ordinary operator on W⊗W is valid: on three blocked sites both sides of the ordinary relation are I_W tensored with the five-factor generalized relation.

### Section 8: quaternionic form and literal S

No defect found. With A_math=−i√2M and B_math=iE, multiplication gives A_math²=−2I, B_math²=−I, and their anticommutation. The printed formulas for U_K,V_K give both skew-Hermitian square-minus-one identities and `U_K V_K=B_math`. The sum is `−i√3 H`, and the scalar conversion to R is exact.

The independent dense verifier uses the literal S entries from the manuscript, direct 2×2 Kronecker products, and a permutation matrix built from `(a,b)→(b,a)`. It verifies S†S=I and all three identities C(U)=U_K, C(V)=V_K, C(UV)=U_KV_K, followed separately by the full R identity. It also confirms that deleting the swap while keeping this S fails, so the stated opposite-operator caveat is necessary for the displayed conjugacy. This is not evidence against the existence of some different direct local equivalence; the manuscript correctly leaves that question open.

The [GR §13.2 primary source](https://arxiv.org/html/2608.16865v1#S13.SS2) was read directly. Its Eq. (13.9) tensor words P_Z and P_X, Eq. (13.10) scalars, and Eq. (13.11) R normalization agree exactly with the manuscript. This comparison has no GHR scalar ambiguity.

## Checkpoint log, approach separation, and strongest result

- 04:48–04:49 UTC: manuscript-only examination; fresh binary-word and dense-matrix approaches selected; approximately 15% of assigned audit complete.
- 04:50 UTC: full 18-word polynomial certificate, exact converse ideal, axis cases, ordinary braid residual, and intrinsic generalized norms verified; approximately 55% complete.
- 04:52–04:53 UTC: visual primary-source scalar discrepancy identified before inspecting production GHR code; independent dense S, quaternionic generators, full R, and partial traces verified; approximately 80% complete.
- 04:54–04:55 UTC: exact literal-versus-common-prefactor GHR counterchecks and compact corrected formula completed; parent and reproduction reviewer notified; approximately 95% complete.
- 04:58 UTC: source-version limitation bounded and concrete disposition reviewed; report complete; 100% of assigned review complete.

Approach families: binary symplectic word algebra (full symbolic cubic support, complete converse); dense literal Kronecker matrices (basis conventions, S, traces, quaternionic identities); chain-position argument (all-n blocking); visually transcribed primary-source comparison (the source mismatch). None imports a production verifier. The exact coefficient ideal establishes the converse independently of the manuscript's case split. The GHR source mismatch was not inferred from a failed test of the same production encoding.

**Strongest verified result:** every internal matrix identity and tensor-placement assertion required by §§2–4 and 7–8 is exactly valid, including the complete reflection-circle classification and the explicit local equivalence to GR's opposite. The older GHR literal-matrix comparison has an independently checkable source mismatch requiring the local editorial/code repair above.

**Exact remaining limits:** I did not audit the all-n Markov/localization proof, the global braid/link conclusions, or minimality in this assignment. The final journal version of GHR Eq. (5.2) was inaccessible and its typography remains unverified. No claim of direct local equivalence without the opposite is established. These limits are not gaps in the verified local algebra.

## Reproduction

Use a normal Python interpreter with SymPy 1.14.0 (the successful run used `/Users/alec/Documents/Math/.venv/bin/python`, Python 3.9.6):

```
python evidence/algebra_independent.py
python evidence/algebra_ghr_source.py
```

Run from this review effort's root. The former performs all symbolic and dense internal checks and emits a completion timestamp; the latter asserts the positive and negative GHR residual values and prints exact diagnostic entries. Captured outputs accompany both scripts. No production code or earlier audit is loaded.
