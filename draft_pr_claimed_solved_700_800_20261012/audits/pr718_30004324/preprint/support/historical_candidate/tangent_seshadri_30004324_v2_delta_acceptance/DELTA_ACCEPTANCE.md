# Final delta acceptance: tangent-Seshadri candidate 30004324, v2

Date: 2026-10-05.

## Verdict

**Proof delta: PASS. Tooling delta: PASS. Exact frozen derivative: PASS.**

I read the complete 18,747-byte v2 proof and examined every section of the exact v1-to-v2 unified diff. The four requested geometric expansions correctly implement the independent audit. They add no hypothesis on X, x, or the characteristic and introduce no new substantive approach. No essential mathematical gap or new false claim was found.

The two original geometry reports are copied byte-for-byte, with their original scope and reservations intact. The strict verifier and its fourteen mutation controls are the first audit's exact implementations. The historical nested-manifest defect is preserved accurately and reproduced. The unchanged original freeze remains intact.

This acceptance concerns a complete AI-audited **candidate**. It is not acceptance of the result by the mathematical community, human peer review, formal proof verification, or a historical-priority determination. The queue label `claimed_solved, 2/5` is consistent with the definition supplied for this review only when it continues to mean this candidate status. This review performs no queue edit or remote write.

## Exact acceptance pins

The acceptance binds these exact bytes:

- v2 archive: `TANGENT_SESHADRI_30004324_V2_SAFE_FREEZE.zip`; 57,356 bytes; SHA-256 `5c698341bff90fc5308d54115853c96c75ea326ce3a2deaa161b18c8e555ba9c`.
- v2 root manifest: `MANIFEST.json`; 4,343 bytes; SHA-256 `76d4c422d368cf1a91881edaa0429abbc32e5910ea3ad3415b20921d8ee0e024`.
- v2 proof: `candidate_proof.md`; 18,747 bytes; SHA-256 `dcad7d7677b1fff7fe1b659fd5b2f2c97e4daa0f0fe7b914a7752f19ad89c5a8`.
- exact diff: `TANGENT_SESHADRI_30004324_V2_FROM_V1.patch`; 124,052 bytes; SHA-256 `16bec841b55f8b0e3d27add239e2868d4e2a35af0efa2e07734fb04ced131cca`.
- machine delta: `TANGENT_SESHADRI_30004324_V2_DELTA.json`; 8,104 bytes; SHA-256 `916fdfa26e6bc1df456526c83e5c76a3427cc9d6a3758e47fe14022124627991`.
- replay output: 3,164 bytes; SHA-256 `5bcf561ce80764d9fd53f91ddba06471d7d06a52788f4288dabe748ccd79ac54`.

The original archive remains 19,163 bytes with SHA-256 `6483242536c534a84072815ae4c3aa9de57fd2769386eb2e5e1ad85041cc6a01`. Its original proof and manifest retain the hashes bound by the two original audits.

The frozen v2 files say that their delta review is pending. Those strings record the state at freezing and have not been changed. This separately bound acceptance supplies the later review outcome. Altering those frozen files would produce different bytes and require a new binding; the present acceptance must not be transferred silently to such a later version.

## Proof comparison

### 1. Geometric-field minimality

The inserted paragraph in Lemma 2 is correct. A rational image of degree c below d over an algebraically closed extension gives a point of the degree-c finite-type Hom scheme with 0 evaluated at x. Nonemptiness descends to existence of a k-point because k is algebraically closed. The resulting k-map has rational image of degree at most c, a contradiction. The argument handles geometric residue fields without introducing uncountability or a general-point hypothesis.

The newly explicit use of Lüroth's theorem is also appropriate in arbitrary characteristic. Mapping degree in the stable-map degree sum is the full field-extension degree, so the normalization and inseparable-cover distinctions remain correct.

### 2. Inertia and the projective coarse target

Lemma 3 implements the proper quasi-finite route supplied in the second audit. Geometric automorphisms are trivial by birationality. Infinitesimal automorphisms are vector fields killed by a generically injective differential, and vanish. The finite stabilizer is therefore the identity group scheme. The finite-inertia augmentation argument deals with a possibly nonreduced base.

The actual evaluation fiber is an algebraic space, proper over k. Its map to the full projective coarse scheme Q has at most one point in each geometric fiber and is proper, hence is quasi-finite and finite. The cited scheme criterion and proper-quasi-finite criterion apply in the stated order. Therefore the evaluation fiber and its reduced irreducible component are projective schemes.

This adds no assertion that arbitrary closed base change commutes with coarse moduli formation. It is sufficient for the later universal-family construction. The stabilizer and numerical arguments still do not require the whole ambient stack to be Deligne–Mumford.

### 3. The degree-one marking bundle

The marking is an effective Cartier divisor in the smooth relative curve. Its line bundle restricts to O(1) on each fiber. The rank-two pushforward and fiberwise evaluation identify the family with a projective-line bundle, so its total space is projective. The added assertion that the total space is integral follows from smoothness over the reduced integral base and the geometrically integral fibers.

This confirms the projectivity used downstream rather than assuming that an arbitrary proper family is projective. It retains a genuine global section; it does not replace that section by a multisection.

### 4. The generic-fiber closed-point curve

Lemma 5 correctly replaces unnecessary general-hyperplane language with a closed point in the nonempty generic evaluation fiber over an arbitrary integral curve Gamma. Its residue field is a finite extension of k(Gamma), so its reduced closure in U is an integral proper curve with positive generic degree q. Projection of line-bundle degrees then gives numerical triviality downstairs.

The argument applies to all integral Gamma, including curves avoiding x and curves of positive genus. The characteristic may divide q; q remains a nonzero positive integer in the intersection-number equality. No separability assumption is added.

### Other mathematical changes

- The expanded relative Seshadri definition retains the pushforward multiplicity and Frobenius-normalized minimum slope. It does not introduce global nefness.
- The added fixed-value Cech lifting explanation in Lemma 4 is the same characteristic-free obstruction argument checked previously. The source points 0 and infinity remain distinct, and the value at 0 remains the specified x. Smoothness is proved at the chosen map rather than inferred by generic smoothness.
- Replacing numerical invariance of ampleness with an explicit Nakai–Moishezon calculation is valid. Equality of divisor classes against all curves implies equality of the top intersections used there. The positive coefficient b/d and Cartier property of -K_X provide the criterion's hypotheses.
- The final imported result remains FM21 Proposition 4.8(1), with the original x and field. The separate general-point, characteristic-zero clause is still unused.
- The unchanged proof target includes all n at least one. No extra Fano, general-point, characteristic-zero, nef-tangent, or separability premise was inserted.

## Citation check

The FM21 and AO theorem references and hypotheses remain those directly checked in the original independent audit. The expanded proof correctly preserves the boundary that the full Kollár monograph has not separately been inspected or re-proved.

The exact Stacks tags 04SZ, 03XX, 02LS, 0EX7, and 0B91 are the propositions and lemmas used in the reconstructed argument. The newly added [Tag 0GKA](https://stacks.math.columbia.edu/tag/0GKA) was directly opened for this delta review: its proper, connected, at-worst-nodal relative-curve hypotheses include this smooth P1-family, and it supplies universal structure-sheaf pushforward.

[Gounelas, Proposition 4.7](https://ems.press/content/serial-article-files/26314?nt=1), printed p. 299, was checked in the public web source and the retrieved PDF text. It contains the stated two-point cohomology calculation and smooth evaluation implication. Its discussion of general source points does not replace the v2 proof's explicit vanishing at the chosen distinct points on P1.

[Fujino–Miyamoto, Theorem 1.3](https://www.math.kyoto-u.ac.jp/~fujino/Nakai-Moishezon3.pdf) and the arbitrary-characteristic convention were checked directly in the available source PDF text. An attempted web open returned an internal error; the already retrieved source bytes were inspected instead. The Cartier special case used by v2 is within that theorem. The PDF hashes and sizes match the copied first-audit metadata.

The old section-level Stacks links in the verbatim first report are identified as historical links in REVIEW_HISTORY.md; the new proof uses exact statement links. Nothing was silently rewritten in an old report.

## Exact-copy and integrity findings

Independent checks establish all of the following:

1. The v1 archive, local tree, and manifest have exactly the same thirteen files and bytes previously audited.
2. The v2 archive has exactly 27 unique file entries, with no duplicate names or symlink entries. Its local tree, root manifest, and every file's declared hash and size agree exactly.
3. The machine delta was recomputed from actual v1 and v2 bytes. Its classification is exactly five unchanged files, eight modified files, fourteen additions, and zero deletions.
4. A new unified diff was independently generated from the two trees and compared with the complete supplied patch. It is byte-for-byte identical.
5. Both geometry reports, both verdict records, both source-metadata records, the original integrity finding, the strict verifier, the fourteen-mutation test program, and the historical verifier were compared against their original files. All copies are byte-exact.
6. The authoritative verifier was executed with the externally pinned v2 manifest hash and passed for all 26 payload files.
7. The complete replay succeeded in the original v2 directory, in a temporary extraction of the archive, and in a temporary tree produced by applying the supplied patch to unchanged v1 with zero fuzz. All three replay outputs are byte-identical to the pinned 3,164-byte output.
8. The patched tree was compared file-for-file and byte-for-byte with v2 before its replay. It is exact.
9. The original and v2 trees were rechecked after all replays and remained unchanged.

The portable tests accept the clean fixture and reject all fourteen mutations. The dedicated historical test demonstrates that the old verifier accepts an unlisted nested MANIFEST.json and that the authoritative v2 verifier rejects it. The historical implementation is clearly labeled and is invoked only for that regression; the original REVISE_REQUIRED finding is not erased.

The 909,136 finite controls remain byte-for-byte unchanged and pass again. They provide finite algebraic/combinatorial checks only, not a verification of the geometric theorem.

## Decision and scope

No proof-level or tooling-level revision is required for the exact v2 bytes pinned above. The final delta-audit gate is satisfied at the level of a checked candidate. The two-approach log remains unchanged in substance, so this expansion does not consume a new approach.

The independently obtained machine evidence is in INDEPENDENT_VERIFICATION.json and INDEPENDENT_REPLAY.json. DELTA_ACCEPTANCE.json records the separate proof/tooling decisions and the exact pins. This acceptance package contains no source PDFs, source extracts, images, raw datasets, or private coordination records. No original audit or author-freeze file was edited, and no remote action was taken.
