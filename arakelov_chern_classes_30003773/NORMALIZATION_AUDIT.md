# Normalization-only patch audit

Date: 21 October 2026.

**Verdict: PASS.** The normalization-only revision preserves the accepted conditional partial mathematics; it is not a solution of the original problem.

## Byte-level scope

- Accepted original: 8,513 bytes; SHA-256 `92d71e5db90e2b71b4d4d509ab73769840b564e71b84cd8a6089c0220f3770b1`.
- Audited final `vertical_euler_classes.md`: 8,902 bytes; SHA-256 `0b1b1b82bdf921fcf1c053edb4401130ffbe36019769bf22048ec19199184f46`.
- The exact unified difference is `NORMALIZATION.patch`, independently regenerated and compared byte-for-byte. There is one changed paragraph, in Section 4; all other manuscript text is unchanged. The accompanying acceptance receipt is unchanged.

## Mathematical checks

1. The added Bott identification sends `c_1(L)` to `1-[L^dual]`, precisely the normalization stated in the acceptance receipt.
2. The Koszul complex is explicitly placed in cohomological degrees -1 and 0. Its sole cohomology is `Z/p` in degree zero, yielding positive Euler length one, consistently with the receipt.
3. The added references and regular mixed-characteristic base `Spec(Z)` match the receipt's cited imports: Panin–Pimenov–Röndigs, Corollary 1.2.7 and Sections 2.6–2.7; Naumann–Spitzweck–Østvær, Theorem 3.1. These remain standard imported facts, not newly proved comparison theorems. This audit checks the patch against the accepted receipt, not a fresh independent retrieval of those sources.
4. Supported K-theory, MGL, and A nonvanishing remain distinct from the globally forgotten A-class. No global A nonvanishing, `log(p)` formula, metric formula, numerical Arakelov degree, unrestricted specialization, or solution of the general Chern-class problem is added.

The patch merely makes the previously audited normalization, grading, and source scope explicit in the manuscript. No manuscript edits were made during this audit.
