# Clasp-conjecture source bridge: a prior theorem, with scope qualification

Problem ID 30004222, OWR-17135-015, queue rank 718. Checked 2026-10-05. Corrected after independent audit on the same date; the original frozen release remains unchanged.

## Result and precise stopping point

The type-A scalar formula in the 2019 Oberwolfach question is a prior result: Stuart Martin and Robert A. Spencer, *Cell modules for type A webs*, Mathematische Zeitschrift 312, article 119 (published 26 March 2026), Theorem 5.11. The preprint first appeared in 2022; the inspected version is arXiv:2210.09639v4, 11 February 2026. Its argument identifies clasped light ladders with normalized lowering-operator bases through quantum skew Howe duality. The printed normalization labels are internally inconsistent: Eq. (5.15) defines a multiplicative normalizer N' whose INVERSE square is the local scalar. The corrected fixed-step reconstruction in `NORMALIZATION_RECONSTRUCTION.md` proves kappa=(N')^(-2)=B=K, retaining the representation-theoretic dependencies and without quoting the erroneous square label as a premise.

This establishes the formula for every type-A rank, not merely the earlier n <= 4 computations. It supplies a representation-theoretic explanation containing an explicit combinatorial cancellation. It is **not labeled here a purely combinatorial proof**, and no claim is made that every qualitative interpretation of “combinatorial explanation” has been settled. No new solution, novelty claim, universal result in other Lie types, or theorem at arbitrary roots of unity is asserted.

The investigation stops on the verified prior-result route. The formula and qualitative proof-style request must remain separate in any queue disposition. The disposition is `qualified_partial_prior_formula`, 1 substantive response out of 5. The original audit required revision; acceptance of this corrected release is pending a delta review. Do not change the row to `verified_solved` on the strength of this package, and do not call the formula open.

## Exact source and access boundary

The designated live URL is https://www.unsolvedmath.com/problems/30004222 . It returned internal fetch errors and a direct HTTP 403; its current full contents were not inspected. No access workaround was attempted after confirming the 403. The descriptor supplies the ID/title/code and points to https://doi.org/10.4171/owr/2019/39 . The original report was independently retrieved and visually inspected: Ben Elias, “Introduction to web algebras and local intersection forms,” printed pp. 2426–2429, especially pp. 2428–2429. The original report explicitly asks for a combinatorial explanation of the displayed formula. It discusses gl_n and exterior powers, not arbitrary Lie types.

The former raw AI-report corpus was unavailable and was not inspected. It is not a proof source. A catalog's `queued, 0/5` entry is a workflow observation, not evidence that no earlier attempt exists.

## Exact mathematical claim

Let n >= 2, let lambda=(lambda_1,...,lambda_n) be a dominant integral gl_n weight, and let mu in {0,1}^n have k ones, 0<k<n. Assume lambda+mu is dominant. Set

    I(mu) = {(i,j): 1 <= i < j <= n, mu_i=0, mu_j=1},
    d_ij = lambda_i-lambda_j+j-i.

In Elias's specified light-ladder basis and reflection pairing, the local intersection scalar is

    kappa(lambda,mu;q) = product_{(i,j) in I(mu)} [d_ij]_q/[d_ij-1]_q.

Here [m]_q=q^(m-1)+q^(m-3)+...+q^(1-m), and the identity is first interpreted over Q(q). At q=1 this is the Oberwolfach scalar:

    kappa(lambda,mu;1) = product_{(i,j) in I(mu)} d_ij/(d_ij-1).

The reference to sl_n in the quantum paper means root-system rank n-1. Naming the family A_n in prose does not impose a finite rank cutoff. Scalar shifts of all lambda_i do not affect any displayed factor. They correspond to determinant twists on the gl_n side.

## Complete elementary bridge proofs

### 1. Root-set identification

The positive roots are alpha_ij=e_i-e_j, i<j, and rho_i-rho_j=j-i. Hence <lambda+rho,alpha_ij>=d_ij and <mu,alpha_ij>=mu_i-mu_j. The denominator <lambda+rho+mu,alpha_ij> is one less than d_ij exactly when (mu_i,mu_j)=(0,1). This identifies the root set in the Oberwolfach report with I(mu), without choosing an ambiguous permutation convention. The empty product is 1 when mu is dominant.

### 2. Denominators and dominance

Because lambda is dominant, d_ij >= j-i. If d_ij=1 then j=i+1 and lambda_i=lambda_{i+1}. For a pair in I(mu), these equal adjacent entries become lambda_i and lambda_{i+1}+1, violating dominance of lambda+mu. Thus every relevant denominator d_ij-1 is a positive integer. Conversely, if lambda+mu is not dominant, an adjacent violation is possible only with equal lambda entries and mu pattern 01; that pair has d_ij-1=0. This proves the exact boundary condition, rather than silently evaluating an undefined factor.

### 3. Classical specialization and central shift

The finite Laurent-polynomial definition gives [m]_1=m for m>=1. Each denominator above has m>=1, so the rational formula has a regular q=1 specialization, yielding the report's ordinary-number product. Replacing lambda by lambda+c(1,...,1) preserves every difference lambda_i-lambda_j. In particular an arbitrary dominant integral gl_n weight may be shifted to a partition without altering this scalar; the light-ladder normalization is the type-A normalization of the cited theorem. This does not identify arbitrary separately rescaled bases: normalization is addressed below.

### 4. A directly checkable tableau cancellation

Let sigma subset tau be partitions with tau/sigma a horizontal strip. Pad to r rows so tau_i>=sigma_i>=tau_{i+1}, with tau_{r+1}=0. Put N_i=tau_i-sigma_i. Let alpha=sigma^t, beta=tau^t and mu=beta-alpha, padded to tau_1 columns. Then mu is a 0-1 vector. Write K(alpha,mu) for the root product, not an independently defined intersection form. Define c_ik=tau_i-tau_k+k-i, allowing k=r+1. The following identity holds as a rational function in q:

    K(alpha,mu)
      = product_{i=1..r: N_i>0}
        product_{k=i+1..r+1}
        product_{ell=1..sigma_(k-1)-tau_k}
          [c_ik-ell]_q/[c_ik-ell-N_i]_q.                 (T)

Proof. A new box in row i has column b in {sigma_i+1,...,tau_i}. Its old column height is i-1. An old column a with no new box and a<b necessarily has a<=sigma_i; it has the same height h in sigma and tau. Its root factor is [h-i+b-a+1]/[h-i+b-a]. For fixed a, multiplying through the consecutive b range telescopes to [h-i+tau_i-a+1]/[h-i+sigma_i-a+1]. Group the unchanged columns by h=k-1. Their indices are exactly tau_k<a<=sigma_(k-1). Substitute a=tau_k+ell and h=k-1 to obtain (T). Every factor came from the original product, so no new zeros are introduced. Empty groups contribute 1. This exhausts all original pairs exactly once.

The extra k=r+1 term matters for general horizontal strips. In the tableau convention of the cited Lemma 5.10, sigma_s=0 and this final group is empty; omitting it without that hypothesis is incorrect. This identity illustrates the combinatorial content of the prior proof. It is not, by itself, a proof that K equals a local intersection form: that identification is the substantive representation-theoretic theorem cited above.

### 5. Normalization cannot be inferred from multiplicity one

If E is the preferred light ladder and the scalar pairing is iota(E)E=kappa times the identity on the relevant simple summand, replacing E by tE changes the scalar to t^2 kappa, since the reflection involution is linear on scalars. Thus a one-dimensional multiplicity space or Pieri's multiplicity-free rule alone does not determine kappa. In Martin–Spencer the required match is between the specified diagrammatic form and the lowering-operator form; the multiplicative normalizer N' is B^(-1/2) by Eq. (5.15). The correct norm equation is 1=(N')^2 kappa, so kappa=(N')^(-2)=B. Lemma 5.10's printed N'^2 label contradicts that definition. For T=[1,2], T'=[1], kappa=[2] while (N')^2=1/[2], giving 2 versus 1/2 at q=1. This is a substantive reciprocal error in the original dossier, not an omitted-square abbreviation. The complete noncircular quotient derivation and representation-theoretic norm comparison are in `NORMALIZATION_RECONSTRUCTION.md`, Sections 3–5.

## Dependency map and limits of verification

The prior theorem attribution is Martin–Spencer Theorem 5.11. The mathematical bridge is reconstructed explicitly in `NORMALIZATION_RECONSTRUCTION.md`; the printed normalization proof is not accepted literally. For a horizontal strip sigma subset tau padded to s rows with sigma_s=0, set N_i=tau_i-sigma_i and c_ik=tau_i-tau_k+k-i. Define the single-step quotient

    B_i = product_(k=i+1..s) Cq(c_ik-1,N_i)
          / product_(k=i+1..s-1) Cq(c_ik+N_k,N_i),
    B = product_(i=1..s-1) B_i.

The reconstruction proves B=K using falling q-factorial cancellation against the row telescope (T). Eq. (5.15) with fixed j=s gives N'=B^(-1/2). Form compatibility, coefficient-one divided-power/light-ladder identification, and the independent lowering-operator orthonormality theorem give 1=(N')^2 kappa. Thus kappa=B=K without assuming the conjectured scalar. Every admissible strip is realized by an explicit parent/child tableau. The proof also verifies parent-path cancellation if a global norm product is used.

The identified dependencies are §5.1 Eq. (5.4), Lemma 5.4, §5.4 Eqs. (5.14)–(5.22), Lemma 5.7, and the actual norm recursion Eq. (4.4). These are representation-theoretic inputs, not independently re-proved foundational theorems. Original input PDFs and published metadata are unchanged. Targeted primary-text inspection and this corrected elementary reconstruction do not amount to a line-by-line audit of all 36 pages and every cited source.

Three separate source hazards must not be conflated:

- Normalizer and step range: Lemma 5.10 and Eq. (5.38) label the direct quotient N'^2, contrary to Eq. (5.15). Eq. (5.38) additionally uses all j rather than the fixed terminal step. For T=[1,2,3], T'=[1,2] the terminal B=3 at q=1 while the all-step product is 6. Fix j=s, or explicitly divide by the parent product; changing only the exponent is insufficient.
- Partition restatement (2.15): both the increment condition and axial-distance shape are wrong as printed. For old alpha and new beta the correct set is beta_a=alpha_a, beta_b=alpha_b+1, and the distance is alpha_a-alpha_b+b-a. For alpha=(1,0), beta=(1,1), literal printed selection gives 1; fixing only its increment condition leaves [1]/[0] rather than [2].
- Permutation direction: under the standard left action, Conjecture 1 sends mu to the dominant weight while retaining the inverse-root expression from the opposite convention in Elias Definition 3.13. For mu=(0,1,1) the stated sorting permutation is [3,1,2]; its printed inverse-root set is {(1,3),(2,3)}, whereas the intended 01 set is {(1,2),(1,3)}. The explicit coordinate set I(mu) is used throughout this dossier, avoiding that convention error.

No broader categorical theorem, elementary bijection, cancellation-free web proof, or arbitrary-characteristic extension is supplied. Whether the user's intended qualitative standard excludes representation theory is not inferred. The strongest established result is the all-rank type-A prior formula plus its documented tableau/representation-theoretic explanation.

## Reproduction and negative controls

Run `python3 -B verify_clasp_bridge.py --output /tmp/clasp-replay.json` from this directory. The script uses only the Python standard library. It checks exact factor-multiset equalities, 7,085 admissible vertical strips (dimensions 2 through 6, partition entries 0 through 4), 10,935 inadmissible cases, 7,085 central shifts, and 12,173 horizontal strips (1 through 5 rows, entries 0 through 6). These bounded diagnostics are not the proof of any unrestricted representation-theoretic statement. The corrected checker now evaluates the actual inverse-square quotient in every horizontal-strip case, and includes exact reciprocal-normalizer, all-j, partial-priming-repair, and source-permutation-direction witnesses. The separately authored audit checker is retained unchanged as `audit_controls.py`; it supplies 36,519 rational-q evaluations, 14,170 q-sign checks, rank-one and roots-of-unity boundary checks. Both recorded outputs are replayed by `verify_release.py`.

The former norm-versus-square control was insufficient to detect the source reciprocal error. It is now supplemented by the actual Eq. (5.15) normalizer control. Controls reject replacing the selected-root product by the full Weyl-dimension ratio, reversing 01 to 10, rescaling the chosen basis, omitting dominance, omitting the final row group, and confusing a norm with its square. For example lambda=(3,1,0), mu=(0,1,0) has kappa=3/2 while dim(L_lambda)/dim(L_(lambda+mu))=1.

## Public primary references

- Ben Elias, report contribution, 2019, pp. 2426–2429: https://doi.org/10.4171/owr/2019/39 ; retrieved report https://ems.press/content/serial-article-files/46818?nt=1
- Ben Elias, *Light ladders and clasp conjectures*, Conjecture 3.16 and Claims 3.14–3.15, pp. 53–55: https://arxiv.org/abs/1510.06840
- Stuart Martin and Robert A. Spencer, *Cell modules for type A webs*, Theorem 5.11 and Lemma 5.10: https://doi.org/10.1007/s00209-026-03990-0 ; inspected preprint https://arxiv.org/abs/2210.09639v4
- Author's publication page: https://robertandrewspencer.com/research/cell-modules-for-a-n-webs/

This package contains authored analysis and public verification metadata only. Source PDFs, extracted text, screenshots, raw upstream records, and private coordination/history payloads are excluded from the release.
