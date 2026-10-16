# PR51 independent eta algebra adversarial review

**PASS: the exact all-N positivity statement is a known affirmative theorem. No mandatory mathematical repair is identified.** Recommendation for problems 30000166 and 30000167: `already_solved`, with the original 0/5 fresh-attempt accounting and no new paper or new-discovery credit. This family supplies an independent mathematical recommendation, not ROOT merge approval.

The original immutable snapshot is commit `8006dd5f134ad0a2fa930e7278d3cb17945f4201`, with 15 files totaling 53,495 bytes. All were read. Initial question/proof/helper reading and the new exact reproduction preceded reading the historical independent review. Full content, length and mode bindings are in FULL_INPUT_BINDINGS.json. No original, canonical, native, Git reference, remote or sibling file was modified.

## Mechanism and strongest result

PROOF_AUDIT.md gives independent, checkable derivations of the Fourier shift, Mobius exponent identity, cyclic affine lattice difference, nonnegative specialization with finite sublevel sets, paired D-product and prime-power lift, and a complete positive-integer case split. The specialization is valid even for coincident bracket progressions. The proof retains its explicitly credited core partition, core theta and Berkovich–Garvan identities; the primary theorem and its functional-equation proof were checked, including an independent argument-principle justification of uniqueness.

The exact strongest verified result is nonnegative coefficients for eta(N tau)^phi(N) times the inverse Mobius divisor product, for every positive integer N. The normalized coefficients are integers. The rational shift A_N only changes exponents; it cannot change coefficient signs. N=1 cancels exactly, the prime case is a core series, and arbitrary composite and higher-power cases follow from the positive factorization. Strict positivity, unrestricted regular-weight products and all-cusp positivity are outside scope. No modular weight/level/cusp/Sturm argument is being used or claimed.

The exact original formula and the composite-case question appear in the official OWR report at pp. 54–55; the [2007 primary manuscript](https://arxiv.org/pdf/math/0702027), Conjecture 1.1 and Section 3, supplies the exact all-positive-integer answer. These statements agree with the candidate. Publication details are corroborated by the author's publication list; the journal PDF was not freshly compared. See PRIMARY_SOURCE_SCOPE.md for exact access and version limits. This is credited existing mathematics, not an unsolved variant or a new solution.

## Fresh reproducible evidence

Run `python3 independent_exact_checks.py` in this family. It uses only the standard library and writes independent_results.json. Actual child 36555 ran at 2026-10-03 09:45:13–09:45:23 UTC, returned zero, preserved its source bytes and had empty stderr. The bounded capture retains the complete source preimage and full output. It passed **324,186 exact assertions**, whose category totals and all case parameters are retained.

The tests use an independent Euler logarithmic-derivative coefficient recurrence, crossed against generalized-binomial factor expansion in 54 parameter cases. They test N=1 through 360 to degree 144, exact Mobius signs, the full prime-power split and lift, residue pair coverage and rational shifts. Direct partition hook enumeration checks core parameters t=1 through 10 to degree 22. A derived coordinate cutoff gives complete finite theta sublevels for 112 cases with a=2,3,4,5, 2<=M<=8, every 0<r<M, through degree 32. Positive D-factor convolutions agree with independently expanded products.

Four deliberate transcription mutations are detected: omitting E(q^M) first differs at degree 5; using the wrong a-2 exponent first differs at degree 28, producing -1; omitting one bracket residue differs at degree 4; failing to scale the numerator residue differs at degree 1. These witnesses validate that the controls detect concrete sign and normalization errors rather than only confirming canned pass flags.

Original immutable helper child 38799 at 09:48:28 UTC returned zero with empty stderr and reproduced the saved 2,837-assertion JSON **byte for byte**. Its source was unchanged. The old 35,980-assertion historical review was read after independent work, but is not counted as new execution in this family. The original helper's use of Boolean tuple membership would lose multiplicity for r=M/2; all its actual theta and factor cases have odd M, so that issue does not affect its stated scope. The new checker counts the two progressions separately and directly covers the coincident case.

These finite checks verify implementation, transcriptions and boundary cases. They are not a proof of infinite coefficient positivity; the universal derivation and explicitly identified classical inputs carry that conclusion.

## Adversarial dispositions and limits

No counterexample, sign defect, omitted integer case, uncontrolled formal substitution, circularity or unsupported transfer to another problem survived. The denominator-12 shift in the old OWR prime display is already correctly qualified and corrected to 24 in the candidate. The broader regular-weight-system conjecture is explicitly distinguished. The composite-case duplicate is mathematically the same target; native duplicate accounting remains ROOT's task.

No mandatory repair is requested. Remaining limitations are openly stated: imported classical identities, no formal proof-assistant certificate, no fresh line-by-line journal PDF comparison, and a bounded current-version/access check rather than an exhaustive correction search. This is independent adversarial AI review, not human peer review. This family creates no publication metadata, preprint, DOI, tracker entry or acceptance authority.
