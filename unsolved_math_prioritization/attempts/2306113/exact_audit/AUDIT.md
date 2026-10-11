# Independent exact-arithmetic and reproducibility audit

Problem 2306113 / AMR-022-6113; rank 1036. Audit date: 2026-10-08 UTC.

## Verdict

**PASS, with an explicit source qualification.** The authored counterexample is mathematically valid for each of the two expressly defined neighborhood conditions in PROOF.md and ALTERNATIVE_REPAIR.md. For x=0, rho=1/1000, gamma=1000000/1002001 and r=999/1000, the same normalized polynomial g satisfies the required strict neighborhood inequality throughout the disk, an explicitly defined function F is globally normalized and univalent, and their Hadamard product vanishes exactly at r.

This is not unconditional certification that either repaired formula is the historical definition in the original problem. The supplied source record reports malformed delimiters in the inspected Hayman–Lingham text and that the original 1989 article's full text was unavailable. Source identification remains unresolved. This audit does not claim a current-literature completeness search, novelty, human peer review, or proof-assistant verification.

A narrow malformed-input handling defect was found in the main checker: a 5000-digit JSON integer below the input byte cap triggered an uncaught Python ValueError instead of structured REJECT. It did not yield mathematical false acceptance. The actual one-line correction was independently prepared and approved for incorporation. All mathematical files, witness data, and successful outputs are unchanged; original freezes were preserved.

## Reviewed inputs and trust anchors

Both proof documents were read fully, as were both exact verifiers, the replay driver, witness, expected outputs, README, approach ledger, source metadata and optional discovery script. The optional floating-point search was inspected for scope and inventory only; it was not used as proof evidence or executed in this audit.

The v2 source packet has thirteen files, including its manifest. Its twelve listed file byte counts and SHA-256 digests independently matched. Relevant anchors:

- v2 manifest: 2f315877db00b3776fe55ab0e576012874078fd8e2df0fc61fec94ff7ac98c28
- v2 main checker: aff03b041039d7cbcddab95d2af02d64df361d4d7911e2f87aa0986b682fa675
- Alternative checker, unchanged: d6195d9189972b3f3aca70cf7c41ea1e59828c4c1e3af98b35290def5a7f09f1
- Replay driver, unchanged: 0be8f9a78270f7baf059af96c9c33f18631688e9aadc0159679acb84a62e13c4
- Main proof, unchanged: 71fb7cad064a4e1dd9fa0760f96ad2ff66aecac4cff1c7f156b1c06d536ea640
- Alternative proof, unchanged: 3aeb1fc5c84a8d757cdf96099218c56e51e357c23749fff5b4a51e598467d77f
- Witness, unchanged: 65ddace3d1b7718fee4195027432b440c6f7ba0f12e33d899c0d9839df6eafd7
- Patched main checker: 1e76693b2c5b1181b55fcd28e3e894e4828600e1471091ace06fbb6bbba09b25
- Independently tested patched-candidate manifest: d889cab7f0337d983b9bd352f61b6bdd5e330cd6d011927cb97949dd716471fb

An external pin, not a digest merely embedded in mutable input, is necessary before executing a checker or trusting a manifest. The replay driver imports only standard-library components under isolated Python; the alternative checker loads the sibling main checker by explicit path. Both files therefore belong in the authenticated inventory.

## 1. Global analytic construction

For unit u, K_u(z)=z/(1+uz)^2 is holomorphic on the disk. Cross-multiplication in K_u(z)=K_u(w) gives (z-w)(1-u^2zw)=0; the second factor cannot vanish in the open bidisk. Thus injectivity is global, not inferred from ten Taylor coefficients.

For the complement of the ray {t/u:t>=1/4}, the principal square root of 1-4uy is analytic with positive real part. Its Cayley transform J_u(y)=(1-s)/(u(1+s)) lies in the disk. Substitution establishes both inverse identities, so the stated image of K_u is correct. For 0<q<1, scaling that slit domain by q moves its excluded ray endpoint toward zero, hence q Omega_u is contained in Omega_u. Consequently J_u(qK_u(z)) is a holomorphic injective disk self-map with derivative q at zero.

The exact u1=-1, u2=(-39951-2800i)/40049 and u3=(-621+100i)/629 each have squared norm one; q1=63/80 and q2=2/25 are in (0,1). Composition followed by the nonzero factor 1/(q1q2) gives F(0)=0 and F'(0)=1 and preserves injectivity. No Loewner existence theorem, numerical ODE, finite-coefficient univalence heuristic or optimizer result enters this argument.

## 2. Independent coefficient reconstruction and zero

The supplied checker uses the Catalan inverse expansion. The audit instead implemented Gaussian rational arithmetic independently, without importing either supplied verifier, and used:

1. Exact truncated formal-series division to calculate K_u(A)=A/(1+uA)^2.
2. The implicit identity B=Y(1+uB)^2, with Y=qK_u(A), to solve B's coefficients successively. Since Y has zero constant term, the equation for degree n depends only on already calculated lower coefficients of B.
3. Two such slit calculations, followed by one further series division for the terminal K and normalization.

All computations were in rational pairs, to degree ten inclusive. Each implicit construction was independently checked by K_u(B)=qK_u(A) through degree ten. The reconstructed coefficient-list digest is

    6e7dec6a524075e5626c60ef1adcc3e6655362e324825ea57d84a606117185f8.

This agrees with the supplied certificate. INDEPENDENT_RESULT.json records all eleven coefficient pairs, including degrees zero and one, and the entire exact complex scalar L. Its real part matches the numerator and denominator displayed in PROOF.md and is strictly greater than 2517/2500. The imaginary part is nonzero and negative; it is retained throughout. The coefficient factor for H=-h/L is (-Re L+i Im L)/|L|^2, not a replacement using Re L or |L|.

The independent implementation constructs g's rational coefficients and directly evaluates the coefficientwise product at 999/1000. Both real and imaginary components equal exactly zero. There is no tail estimate: h and g-z have degree ten, so later coefficients of F do not contribute. The parameter, normalization and nonzero-radius conditions needed to contradict membership in the Hadamard dual S* are all satisfied. Here S* is the dual defined in the proof, not the starlike class.

## 3. Symmetric norm: complete circle and disk

The supplied and independently reconstructed polynomials use coefficients (n+1)c_n and (n-1)c_n at exponent n-1. The angular reverse-triangle estimate yields sum n(n-1)|c_n|; replacing complex moduli by coordinate absolute sums gives exactly 6004273/500000.

For t=j/8192, -8192<=j<=8192, the rational map ((1-t^2)+2it)/(1+t^2) covers one semicircle; its negatives cover the other. Its angular derivative has magnitude at most two. A nearest grid value is at most 1/(2*8192) away in t, so each point on either semicircle is at most 1/8192 away in angle. Endpoint duplications are harmless. This proves coverage of the circle independently of the finite evaluation output.

The independent calculation evaluated all 32770 listed points by ascending polynomial powers, rather than the supplied Horner implementation. Its square-root enclosure used an independent integer identity to obtain the least upward multiple of 10^-9, with both defining inequalities checked. It reproduced exactly:

- Maximum sampled rational upper enclosure: 500679451/500000000.
- Angular Lipschitz bound: 6004273/500000.
- Complete-circle upper bound: 513446291949/512000000000 < 251/250.

The sum-of-moduli identity as a maximum of absolute values of phase-weighted analytic polynomials is correct. Applying the maximum-modulus principle to each such polynomial extends the circle bound to the closed disk. No empirical boundary sample is substituted for that argument.

The symmetric norm is absolutely homogeneous under multiplication by a complex scalar. Division by |L| therefore gives a strict bound below 2510/2517, and

    gamma - 2510/2517 = 1977490/2522036517 > 0.

Thus the intended strict condition holds even uniformly on the closed disk, which is stronger than the open-disk requirement.

## 4. Inner-absolute-value repair: genuinely two-dimensional bound

This repair is separately defined. In particular, it is not legitimate to infer its disk maximum from its boundary or to divide an unscaled alternative norm of h by |L| without accounting for phase. The companion checker correctly forms H=-h/L first, and then certifies that actual function directly.

With q(z)=H(z)/z, z=r exp(i theta), the identity |H(z)|/z=exp(-i theta)|q(z)| is correct. At r=0, both H' and q tend to zero, so the expression extends continuously by zero regardless of angle.

For H=sum d_n z^n, the radial bound follows by adding the first summand's derivative bound (n-1)^2|d_n|R^(n-2) and the second's (n(n-1)+(n-1))|d_n|R^(n-2), then halving. This gives n(n-1)|d_n|R^(n-2). The angular bounds similarly combine (n-1)^2 with n(n-1)+n, giving (n^2-n+1/2)|d_n|R^(n-1). Coordinate absolute sums are valid upper bounds for |d_n|. Reverse-triangle estimates remain valid at zeros, without differentiability assumptions for absolute values.

The t parameter contributes a factor at most two to the angular Lipschitz bound. Adding the radial and t midpoint errors therefore bounds every point of each closed parameter rectangle. The nested modulus enclosure is also valid: an upward Q enclosing |q| differs by at most 10^-10, and substitution into the second argument changes its outer modulus by at most that amount. The extra half-error term is retained after halving the total. All three square-root decisions are exact integer comparisons.

The audit implemented the entire adaptive traversal independently in breadth-first order. It matched the supplied depth-first traversal's result exactly:

- 4050 inspected rectangles.
- 2026 accepted leaves.
- Maximum leaf depth 21.
- The same strictly positive, exact minimum margin recorded in ALTERNATIVE_RESULT.json.

The two signed trees were additionally checked for exact prefix completeness and area two per root parameter rectangle. All exact leaf rectangles and bounds were saved. A separate geometric checker then reconstructed the two full midpoint-bisection trees bottom-up, checking that every sibling pair partitions its parent and each root is precisely [0,1] times [-1,1]. This avoids relying only on area or on a count of visited nodes. It rejected a missing leaf, duplicate leaf, non-strict bound and artificially introduced rectangle gap.

Hence this is an entire-closed-disk certificate, not a sampled boundary surrogate. Overlapping seam points and the multiply represented origin do not create gaps.

## 5. Additional analytic scope checks

The center-case equivalence argument in Section 6 is consistent: balanced scalar rescaling would force a convolution zero if its auxiliary analytic function exceeded one; Schwarz's lemma then supplies the radius factor. The converse imports the classical growth lower bound for normalized univalent functions. That imported theorem is not needed by the explicit counterexample in Sections 2–5 or by the alternative certificate.

The proof does not exchange coefficient neighborhoods with Sigma neighborhoods, and it does not exchange starlikeness with the Hadamard dual. The source ambiguity is maintained explicitly in the revised cross-reference. The two certified formulas do not exhaust all possible readings of malformed notation.

## 6. Executed reproducibility and rejection controls

Interpreter: CPython 3.12.14. Execution was genuinely nonroot, UID=EUID=1000. Packet directories were mode 0555 and files mode 0444. The replay driver actually attempted to append to the witness and create an unauthorized packet file; both writes raised PermissionError.

Both the original v2 freeze and the separately patched freeze completed the full supplied replay:

- Main and alternative positives in normal, -O and -OO modes: six successful executions per freeze.
- Twenty-eight malformed/wrong-witness cases per checker per mode: 168 structured rejections per freeze.
- Hostile working directory and Python environment ignored under -I -B.
- Exact successful output equality and post-run unchanged file hashes.

The patched candidate additionally passed 38 independent adverse input cases for both checkers in all three modes: 228 structured rejections. These cover strict int-versus-bool/float distinctions, exponent and nonfinite overflow, a 5000-digit JSON integer, canonical rational syntax, zero denominator, oversized rational strings, schema errors, invalid UTF-8, trailing JSON, short/long coefficient lists, zero perturbation, deleted leading coefficient and inadequate circle coverage settings. A hostile fractions module, hostile sitecustomize module, PYTHONPATH, PYTHONHOME, PYTHONOPTIMIZE and bytecode environment settings did not compromise isolated execution.

Seven trust-boundary controls also rejected the intended failures: wrong external manifest pin, missing file, extra inventory file, modified manifest, witness-byte mutation, a checker with its circle loop truncated, and a checker with one disk child replaced by a duplicate of the other. The last two are rejected by authenticated code digests, as they must be; an arithmetic checker cannot compensate for executing maliciously changed covering code.

No acceptance check uses assert, so optimization does not remove its predicates. Python integers and Fraction avoid machine integer overflow. The newly broadened ValueError catch retains the existing Invalid rejections because Invalid is a ValueError subclass. The correction changes malformed-input reporting only.

## 7. Limits and publication-safe inventory

The review trusts the Python interpreter, standard-library integer/rational arithmetic, operating-system execution and independently conveyed digest anchors. This is computer-assisted verification with independently reconstructed arithmetic, not formal kernel verification. Permission bits establish actual process-level read-only behavior; they do not protect against an owner changing permissions, root, concurrent malicious replacement, or arbitrary resource-exhaustion attacks. Finite resource budgets reject rather than accept unfinished disk traversals.

No source document, copied scholarly passage, private coordination file, external dataset content or personal data is included in the audit deliverables. SOURCE_FREE_ALLOWLIST.json lists the authored audit files suitable for a publication review, with independently calculated byte counts and SHA-256 digests. The original authored packet can be assessed separately under its pinned manifest; its SOURCE_METADATA.json contains public bibliographic/retrieval metadata, not source documents.

No repository publication, queue change or external outreach was performed by this audit.
