# Target 174 / record 60: exact cyclic nine-minor certificate

## Claim

For the graph-derived target direction 174 (record 60, ordered split
`01|23`), the quartet Fourier flattening has rank strictly greater than four
at every parameter point in the strict K3P principal domain
\(\mathcal D_{3,+}\), with both inheritance probabilities strict.

This claim is not inferred from the old unit-cube sign search.  The descriptor
is rebuilt from the frozen switching signatures, and every polynomial identity
below is checked as equality of sparse integer coefficient dictionaries by
`verify_record60_cyclic_certificate.py`.

## Notation

Let \(p=\lambda _0\) and \(q=1-p\).  For a nonzero K3P character
\(s\in\{C,G,T\}\), denote the sector-\(s\) spectra of edge classes
0, 2, 4, and 5 by

\[
a_s,\qquad b_s,\qquad c_s,\qquad d_s,
\]

respectively, and define

\[
K_s=p a_s b_s+q c_s,
\qquad
L_s=p a_s+q b_s c_s.
\]

Every one of these edge spectra is in \((0,1)\), and \(p,q>0\), on the
strict principal domain.  No relaxation to the full unit cube is used.

## The nine normalized minors

Use the zero-character Fourier block and, for every nonzero character \(s\),
the row and column pair \((0,s)\).  After removal of a strictly positive
monomial, the three diagonal minors are exactly

\[
F_s=b_s-d_s^2K_sL_s.
\]

For distinct \(s,t\), put \(r=s\mathbin\oplus t\) and

\[
M_{st}=p b_s a_r+q b_t c_r.
\]

The six ordered cross minors, using rows \((0,s)\) and columns \((0,t)\),
are exactly

\[
E_{st}=d_rM_{st}-d_sd_tK_sL_t.
\]

The removed monomials are recorded in the JSON audit.  They are products of
strict edge spectra and \(\lambda _1\), so they are positive.  Consequently,
vanishing of the original nine minors is equivalent to vanishing of these
nine normalized polynomials.

## Exact elimination

For each cyclic choice of distinct \(r,s,t\), define

\[
C_r=d_r^2M_{st}M_{ts}-b_sb_t.
\]

Direct sparse expansion gives the ideal-membership identity

\[
\begin{aligned}
C_r={}&E_{st}\,d_rM_{ts}
      +d_sd_tK_sL_t\,E_{ts}\\
    &-b_sF_t-b_tF_s+F_sF_t.
\end{aligned}
\]

There is then a second exact identity

\[
\boxed{
b_rC_r+b_sb_tF_r
=d_r^2pqa_rc_r
 (b_t-b_sb_r)(b_tb_r-b_s).
}
\]

Both sides of the boxed identity have exactly eight nonzero monomials before
collection.  All three sector instances are checked independently.

If the nine minors vanished, the first identity would give \(C_r=0\), and
the boxed identity would give

\[
(b_t-b_sb_r)(b_tb_r-b_s)=0,
\]

because \(d_r^2pqa_rc_r>0\).  Thus, for every \(r\),

\[
b_r\in\left\{\frac{b_t}{b_s},\frac{b_s}{b_t}\right\}.
\]

Put \(B_s=-\log b_s>0\).  The three sector relations become

\[
B_r=|B_t-B_s| \qquad(r=C,G,T).
\]

Choose \(r\) for which \(B_r\) is maximal.  Since the other two numbers are
strictly positive and at most \(B_r\), their absolute difference is strictly
smaller than \(B_r\), a contradiction.

## From the block to the full flattening

The conservation-supported Fourier flattening is the direct sum of four
\(4\times4\) character blocks.  Every block is nonzero at a strict point.
Rank at most four would therefore force every block to have rank one, hence
would force the nine selected zero-block minors to vanish.  The contradiction
above proves that rank at most four is impossible.

## Replay and adversarial checks

Run

```text
.venv/bin/python cut_recovery/strong_crossbridge/audit_simplex/verify_record60_cyclic_certificate.py
```

The replay regenerates `RECORD60_CYCLIC_CERTIFICATE_AUDIT.json` and verifies:

- three diagonal-minor formulas;
- six ordered cross-minor formulas;
- three ideal-membership identities;
- three cyclic factorizations; and
- rejection of eight mutations involving the wrong target, wrong Fourier
  block, wrong edge class, wrong inheritance variable, transposed ordered
  minor, omitted eliminant term, and a changed factor sign.
