# Independent hostile report for `Q2-E0-A2-B2-D2-N1`

**Audit completed (UTC):** 2026-07-26T09:43:40Z
**Verdict:** **PASS — promote this frozen row from provisional to certified.**

This verdict is row-sized.  It covers arbitrary quadratic and cubic lower
terms and every frozen coefficient-pivot piece.  It does not alter the
frozen denominator or assert anything about another row.

## 1. Clean-room routing verdict

The clean-room derivation was saved before any proposed bridge or lower
conic proof was opened.  From the tuple

\[
(e,a,b,\delta,\nu)=(0,2,2,2,1)
\]

alone, the leading map is, after an invertible target change (or a
simultaneous normalized conjugation),

\[
H_4=(p^2,pq,q^2)
\tag{1}
\]

for a coprime canonical quadratic pencil satisfying

\[
\mathbb C(p/q)=E_{H_4}.
\tag{2}
\]

This route uses the intrinsic image conic and its normalization.  It does
not select or divide by any coefficient of \(H_4\).

The image conic spans the target plane, so the three original component
quartics are linearly independent.  Therefore:

- every nonempty `C00`--`C14` routes pointwise to (1);
- `C15`--`C44` are empty, because the first component of \(H_4\) cannot
  vanish identically.

This is the required coefficient-pivot-independent coverage of all 45
frozen pieces.

## 2. Double-line exhaustiveness

A line in the space of ternary quadrics contains at most two squares.  If
the canonical pencil contained two distinct double lines
\(\ell^2,m^2\), then

\[
\frac pq\ \text{is Möbius-equivalent to}\
\left(\frac{\ell}{m}\right)^2.
\]

The element \(\ell/m\) is a genuine quadratic algebraic element over
\(\mathbb C((\ell/m)^2)\) inside
\(\mathbb C(\mathbb P^2)\), contradicting (2).  Hence two double-line
members are impossible in this row.

Both remaining values occur at the level of admissible leading data:

- zero: \(\langle x^2+y^2,\ y^2+z^2\rangle\);
- one: \(\langle x^2,\ yz\rangle\).

Their generic conics are geometrically integral, so relative closure does
not remove either locus.  Thus the internal split is exactly

\[
\boxed{0\ \text{or}\ 1\ \text{double-line member}.}
\]

The forbidden two-double-line presentation recomputes to

\[
H_4\sim(\ell^4,\ell^2m^2,m^4)
\]

and routes to `Q2-E0-A1-B4-D2-N2`, with canonical tuple
\((0,1,4,2,2)\).

## 3. Audit of the no-double-line proof

The following steps in `WORKING_CONIC_TYPE_22.md` were reconstructed
independently.

1. For \(C=JH_4\),
   \[
   \operatorname{adj}(C)=2(\nabla p\times\nabla q)
   (q^2,-2pq,p^2).
   \]
   The degree-eight identity is therefore
   \(D(n\cdot H_3)=0\).

2. The homogeneous first-integral argument is sound.  Relative closure
   puts \(S^2/q^7\) in \(\mathbb C(p/q)\).  Divisor parity forces every odd
   base multiplicity to be supported on a double line.  With none, the odd
   total degree seven is impossible, so \(S=0\).

3. The Hilbert--Burch matrix
   \[
   \begin{pmatrix}2p&0\\q&p\\0&2q\end{pmatrix}
   \]
   has signed maximal minors
   \(2(q^2,-2pq,p^2)\).  Since coprime \(p,q\) are a regular sequence, it
   gives the complete syzygy module, not merely candidate syzygies.  Hence
   the displayed linear-form parametrization of \(H_3\) is exhaustive.

4. An abstract-jet expansion, independent of a choice of \(p,q\), gives
   exactly
   \[
   [\det JF]_7
   =2D\!\left(n\cdot H_2-(q\ell-pm)^2\right).
   \]
   The degree-six first-integral and the same Hilbert--Burch resolution
   then give the complete \(H_2\) form
   \(\operatorname{Ver}(\ell,m)+M(p,q)\).

5. The three regular-pencil self-adjoint Jordan forms were replayed.  In
   each case the three components of \(D\) are independent, and
   \[
   \dim(W\cap\langle p,q\rangle)=0,0,1
   \]
   respectively; in no case is \(\langle p,q\rangle\subset W\).  Thus the
   degree-six equation forces the constant residual matrix to vanish, and
   the full map factors through two functions, contradicting the Keller
   rank.

No lower coefficient is specialized in this argument.

## 4. Audit of the unique-double-line proof

The two intrinsic pencil normal forms are exactly

\[
\langle x^2,yz\rangle,\qquad
\langle x^2,y^2+2xz\rangle.
\]

Their generic determinant polynomials are nonzero, and \(x^2\) is their
unique double line.  The polynomial kernels

\[
\ker(-y\partial_y+z\partial_z)=\mathbb C[x,yz],
\quad
\ker(-x\partial_y+y\partial_z)=\mathbb C[x,y^2+2xz]
\]

make the degree-eight solution
\(n\cdot H_3=x\Phi_3(p,q)\).  Combining the four-dimensional binary cubic
image with the same complete tangent syzygies gives all of equation (19).

The lower proof's previously prose-only completeness assertions were
reconstructed as exact rational linear systems:

| Assertion | Independent exact certificate |
|---|---|
| Degree-seven map on the 18 coefficients of \(H_2\), both pencil forms | matrix size \(36\times18\), rank \(12\) |
| Degree-seven kernel | exactly the six-dimensional space \(\{M(p,q)\}\) |
| Degree-seven compatibility | exact ideal \(\langle\alpha\ell_y,\alpha\ell_z\rangle\) in both forms |
| Degree-six map on the 9 coefficients of \(L_0\), both forms | matrix size \(28\times9\), rank \(6\) |
| Degree-six kernel | exactly the three-dimensional arbitrary-first-column space |
| The \(\ell=0\) branch | the forced matrix \([a,v m_y,v m_z]\) is a particular solution; adding the full kernel changes only \(a\), so the singular family is exhaustive |
| \(q=yz,\ \bar\ell\ne0\) compatibility | exactly \(\langle\beta\ell_1^2,\beta\ell_2^2,\gamma\ell_1^2,\gamma\ell_2^2,\delta\ell_1^2,\delta\ell_2^2\rangle\) |
| \(q=y^2+2xz,\ \bar\ell\ne0\) compatibility | exactly \(\langle\beta\ell_2^2,\beta\ell_1\ell_2,\gamma\ell_2^2,\gamma\ell_1\ell_2,\delta\ell_2^2,\delta\ell_1\ell_2\rangle\) |
| Sole Jordan residue \(\ell=\lambda y,m=kz\) | equation (28) is a particular solution and already contains the whole three-dimensional kernel, hence is the full affine solution |

The five degree-five coefficients in equation (29) were then recomputed.
For \(\lambda\ne0\), they successively force
\(\beta=\gamma=\delta=0\).  The remaining factorization obstruction was
also recomputed: its top degree is

\[
2(a_1Q^2-2a_2PQ+a_3P^2),
\]

so the last target vector vanishes and the Jacobian rank contradiction
follows.

The affine translations used between these branches only adjust the
linear parts of \(p+\ell,q+m\); they preserve the leading pencil and the
Keller determinant.  Constants are removable by a target translation.
Thus they do not discard lower terms.

## 5. Checker assessment

The original SymPy and PARI scripts both pass and independently reproduce
the displayed candidate identities.  By themselves they did **not** prove
the rank, kernel, cokernel, or full-solution assertions: they checked
sufficiency of the displayed families.  That was a genuine certification
gap, not a mathematical counterexample.

The attached independent verifier closes that gap.  It:

- pins the frozen taxonomy, manifest, working theorem, and both lower
  implementations by SHA-256;
- checks the frozen tuple and all 45 pivot labels;
- reconstructs the universal degree-eight and degree-seven identities;
- computes every exact matrix, kernel, and compatibility ideal listed
  above;
- reruns both lower implementations and requires their exact pass tokens;
- fails closed if SymPy or PARI is unavailable;
- requires deliberate mutations of an input hash, pivot list, E7 rank, E7
  compatibility ideal, E6 rank, and lower pass token all to fail;
- refuses optimized Python, so assertions cannot be disabled.

Strict replay result:

```text
INDEPENDENT_Q2_E0_A2_B2_D2_N1_AUDIT_PASS
INDEPENDENT_Q2_E0_A2_B2_D2_N1_STRICT_PASS
```

Relevant artifact hashes at the successful replay:

```text
9725df621656b296c4a9739477a3da6b39e01f279c7bb288e6f814e2b80f113b  INDEPENDENT_BRIDGE_DERIVATION.md
205dc5e42e4d309f2d26059a7740cfd27db13a2f00d78cee226cf7feafa6a28c  verify_independent_bridge_q2_e0_a2_b2_d2_n1_v1.py
75f34af8ea8d23c8fef65224ab7deef0f831eaf921b645f4cc7c480d6d493bff  verify_independent_bridge_q2_e0_a2_b2_d2_n1_v1_strict.sh
```

## 6. Final recommendation

There is no surviving sublocus and no unproved completeness step within
the routed row.  The exact recommendation is:

\[
\boxed{\texttt{Q2-E0-A2-B2-D2-N1}: \text{CERTIFY}.}
\]

`CERTIFIED_EXCLUSION_STATUS.md` was not modified.  No commit or push was
made.
