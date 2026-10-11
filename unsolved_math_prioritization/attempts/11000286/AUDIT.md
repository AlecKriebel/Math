# Independent mathematical audit: bounded integral stabilization obstruction

## Verdict

This is an AI-assisted mathematical audit. The independent calculations and source checks described below are separate review work; no external human peer review or formal proof-assistant certification is claimed. Acceptance remains dependent on the cited source theorems.

**ACCEPTED within the stated bounded scope.** The frozen candidate's proposition is correct. No substantive mathematical correction is required. The expanded accompanying proof removes shorthand about the Pin convention, the central-extension cocycle, and detection of an integral bar cycle.

Candidate fingerprint: 4,557 bytes; SHA-256 `93f4168b1c4cb0e70df591deb15f51fa1efe5f844f58b571f60e6c24871ef03d`.

The accepted theorem is: if `n,m>=8`, `n!=m`, and `m<binomial(n,2)`, every homomorphism `Out(F_n)->Out(F_m)` has zero induced map on `H_2(-;Z)`, while both second homology groups are nonzero. This includes every adjacent-rank case `m=n+1`, `n>=8`.

## Dependency audit

- **Original question:** Bridson-Vogtmann Question 3.6 is on printed p.326/PDF p.333. Integral coefficients occur explicitly immediately before the question. The later Burnside-type quotient discussion is a separate paragraph, not an additional clause of Question 3.6.
- **Rank interpretation:** The isolated question omits a literal distinct-rank restriction. The identity solves the equal-rank case, so that case is excluded explicitly. Nearby context concerns increasing ranks. The accepted proposition states its own direction and bounds and does not promote an inference about the source's intended generality to an exact quotation.
- **Kielak:** Theorem 6.8, printed/PDF p.26 and repeated on p.2, applies to distinct positive `n,m`, `n>=6`, and strict `m<binomial(n,2)`. It requires neither even `n` nor an injective homomorphism. Its conclusion is image contained in `C_2`, not merely arbitrary finite image. The latter weaker conclusion would not imply the needed integral vanishing.
- **Factorization:** A homomorphism whose image is contained in a copy of `C_2` factors through that group. The trivial image is included. Functoriality therefore factors the second homology map through `H_2(C_2;Z)=0`.
- **Cyclic homology:** In the trivial-coefficient periodic complex, `d_2=2` and `d_3=0`. Thus the asserted degree-two vanishing is correct. Odd positive integral homology of `C_2` need not vanish; the proof does not generalize this step to all degrees.
- **Galatius:** Theorem 1.1 is a statement about the actual free-basis permutation map `S_r->Aut(F_r)`. Its strict bound `r>2k+1` gives `r>=6` at `k=2`. The integral interpretation is explicit in the equivalent formulation on p.3. The result is not limited to rational coefficients.
- **Hatcher-Vogtmann:** The exact numbered citation is Corollary 1, printed p.1271/PDF p.19, with integral coefficients stated on p.1253/PDF p.1. The map is the quotient `Aut(F_r)->Out(F_r)`. The degree-two isomorphism starts at `r>=8`; at `r=7` the cited corollary states only surjectivity. The audit does not substitute the flawed earlier 1995 proof for this correction.
- **Clifford sign convention:** The expanded proof fixes `e_i^2=+1` and uses twisted conjugation. This gives reflections by `x -> -uxu`. The orthogonal lifts of `(12)` and `(34)` have squares `+1`, anticommute, and have commutator `-1`.
- **Double-cover kernel:** The expanded proof establishes the central kernel `{+1,-1}` directly from the Clifford monomial basis and word reversal, instead of relying on unspecified Pin notation. It applies in every rank `r>=4` used for the symmetric-group nonvanishing.
- **Integral detection:** The chain `[a|b]-[b|a]` is an integral cycle. A normalized `F_2`-valued group cocycle extends Z-linearly to integral chains and kills integral boundaries. Its value on this cycle is one. This directly proves nonzero integral `H_2`; nonsplitting of an extension by itself would not suffice, and that invalid shortcut is not used.
- **Stable range:** For each of `r=n,m>=8`, both comparison maps on `H_2` are isomorphisms, so both outer-automorphism second homology groups are nonzero. Degree two lies within the common verified stable range. No natural homomorphism between different-rank outer-automorphism groups is assumed.
- **Adjacent ranks:** `binomial(n,2)-(n+1)=(n^2-3n-2)/2>0` for `n>=8`. The strict inequality is preserved.
- **Rational variant:** For positive degrees in the common range `r>=2k+4`, rational homology is zero by the finite symmetric-group comparison. The degree-zero map is the identity. The integral obstruction is therefore not a rational obstruction.

## Verification performed

1. Independently recomputed the candidate byte count and SHA-256 and matched the frozen fingerprint.
2. Independently fetched all four cited PDFs from their primary public URLs. Every retrieved byte string equals the corresponding frozen source, with the same size and SHA-256. The retriever logs only public URL, date, result, and file fingerprint metadata.
3. Extracted source text and visually inspected the displayed mathematical statements, including the inequalities that automated PDF text extraction can misread. The inspected pages are listed in `SOURCE_PINS.json`.
4. Wrote an expanded proof with explicit bar differentials, cocycle identity, Clifford kernel computation, sign convention, and range substitutions.
5. Ran an independent exact-arithmetic finite check inside `Cl_4^+`. It constructs 48 lifts over all 24 permutations, checks both-element fibers and the exact kernel, checks all 576 factor-set values and all 13,824 cocycle identities, and confirms integral boundary zero and cocycle evaluation one. The general-rank proof does not depend on this finite check.
6. The upstream audit repeated the checker with Python normal, `-O`, and `-OO` execution, and ran intentional fault controls. This publication packet retains the aggregate checker-run outcomes in `AGGREGATE_CHECKS.json`; checker scripts and control files are excluded. These historical computations were not rerun while preparing this packet.

## Acceptance boundaries

This is a verified bounded consequence of known theorems, not a claimed new theorem about all rank jumps. It does not settle target ranks `m>=binomial(n,2)`, equal ranks, low ranks, or all homological degrees. It does not exclude abstract stable-homology isomorphisms. It does not establish that the complete original Question 3.6 has been solved or remains open in the literature today.

This publication packet contains the full authored proof and mathematical audit, public bibliographic and source-fingerprint metadata, aggregate check results, and acceptance and inventory records. Copied source PDFs, extracted source text, source-page screenshots, imported dataset contents, raw finite-group or cocycle tables, checker scripts, control files, and coordination material are excluded. `MANIFEST.json` defines the closed public inventory. No repository publication or queue change was performed by this audit or by preparation of this packet.
