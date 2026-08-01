# An exact complete-tripartition-PPT obstruction to the first DTH lift

## Theorem

Let

\[
 \mathscr X=\operatorname{Sym}^2(\wedge^2\mathcal H)\otimes\mathcal H,
 \qquad \mathcal H=(\mathbb C^3)^{\otimes3},
\]

and impose the complete first-level density-moment constraints: the first
Pluecker equation, the corrected density-level support constraint induced
by \(W^\dagger z=0\) after conjugation, and the lifted incidence constraint
induced by \(\operatorname{Tr}(D_zW)=0\).  Regard the three grouped moment
factors of this lift as

\[
 \mathcal A=(\wedge^2\mathcal H)_{12},\qquad
 \mathcal B=(\wedge^2\mathcal H)_{34},\qquad
 \mathcal C=\mathcal H_5.
\]

There is an explicit rational, local-unitary-invariant Hermitian moment
\(R\) on this constrained lift such that

\[
 R\succeq0,\qquad R^{\Gamma_{\mathcal A}}\succeq0,
 \qquad
 \operatorname{ran}(R^{\Gamma_{\mathcal A}})
 \subseteq\ker\mathcal C_{\rm supp},
 \qquad R^{\Gamma_{\mathcal C}}\succeq0,
\]

but

\[
 \operatorname{Tr}(R\widetilde{\mathcal O}_0)<0.
\]

All inequalities and the range inclusion are certified over \(\mathbb Q\).
Since the first two bivector grouped moment factors are exchange symmetric,
these two partial-transpose tests imply positivity under every partial
transpose of the tripartition
\(\mathcal A:\mathcal B:\mathcal C\).

Consequently, even the complete-tripartition-PPT strengthening of the
five-replica constrained first lift does not prove DTH.

This is a pseudomoment obstruction.  It is not of the physical rank-one form
\((w\otimes w)\otimes z\), so it is not a counterexample to DTH, square-zero
positivity, or unrestricted three-copy Werner positivity.

## Exact certificate data

The source certificate contains 125 rational invariant blocks.  Its 118
nonzero holomorphic blocks are positive definite on a face of reduced
multiplicity-rank sum 768; the largest block has dimension 16.  Exact
Sylvester tests succeed in every block, and the largest final leading minor
has 7480 decimal digits.

The unnormalized exact trace and witness pairing have decimal displays

\[
 \operatorname{Tr}R
 =1.00000004533662035943360398481\ldots>0,
\]

\[
 \operatorname{Tr}(R\widetilde{\mathcal O}_0)
 =-0.000976106094995776069240622096041\ldots<0.
\]

The exact rationals are stored entrywise in the source artifact.  Their
canonical numerator/denominator-string SHA-256 digests are respectively

```text
368a672912bcffa686528fdb6bb74effcb7e44f89f4bd3127af3a043cd1ed9bd
043d2e3235d928c9aea95e419c3b24f55feaa2906175365f93aea7910b47a15a
```

The first-bivector partial transpose lies exactly in the previously derived
physical product-DTH face.  Its 198 nonzero blocks have total reduced rank
2266 and maximum dimension 53.  The independent dyadic perturbation
certificate proves positive definiteness with

\[
 \begin{aligned}
 \text{minimum congruent margin}&=0.9999999999991039\ldots,\\
 \text{minimum certified scaled lower bound}&=
 1.056914006481907\times10^{-9},\\
 \text{worst perturbation ratio}&=
 6.21183886716376\times10^{-41}<1.
 \end{aligned}
\]

For the final-slot partial transpose, the exact crossed support first has
reduced rank 772.  The two-column support/incidence map has exact reduced
rank 21, leaving the face

\[
 772-21=751
\]

across 188 nonzero blocks.  Restoring carrier multiplicities gives full
support, defect, and face dimensions

\[
 1\,194\,102,\qquad 6\,552,\qquad 1\,187\,550.
\]

The certificate's final-slot partial transpose satisfies every primitive
integer face equation.  The CRT replay used 85 deterministic primes; its
1695-bit modulus exceeds twice the proved 1675-bit residual bound.  Thus the
face membership and reconstructed coordinates are exact, not probabilistic
modular tests.  The 188 reconstructed rational blocks have total reduced
rank 751 and maximum dimension 40.  Their independent exact positivity
certificate gives

\[
 \begin{aligned}
 \text{minimum congruent margin}&=0.9999999999699818\ldots,\\
 \text{minimum certified scaled lower bound}&=
 1.4995135884402178\times10^{-8},\\
 \text{worst perturbation ratio}&=
 3.6773767779268204\times10^{-43}<1.
 \end{aligned}
\]

## Why these are all PPT cuts

The physical monomial motivating the lift is

\[
 h(w,z)=w_{12}\otimes w_{34}\otimes z_5.
\]

The holomorphic support is contained in the positive eigenspace of the real
pair exchange \(S_{\mathcal A\mathcal B}=(13)(24)\).  The candidate is
supported there and is therefore pair-exchange invariant.  Directly on
matrix units,

\[
 S_{\mathcal A\mathcal B}R^{\Gamma_{\mathcal A}}
 S_{\mathcal A\mathcal B}
 =
 (S_{\mathcal A\mathcal B}RS_{\mathcal A\mathcal B})
 ^{\Gamma_{\mathcal B}}.
\]

Thus \(\Gamma_{\mathcal A}\)-PPT is equivalent to
\(\Gamma_{\mathcal B}\)-PPT on this support.  Moreover

\[
 R^{\Gamma_{\mathcal A}\Gamma_{\mathcal B}}
 =T_{\rm full}(R^{\Gamma_{\mathcal C}}),
\]

and full transpose preserves positive semidefiniteness.  The cyclic
complement identities cover the remaining two-factor cuts.  This is PPT
completeness for the grouping \(\mathcal A:\mathcal B:\mathcal C\), not
PPT under each of the five replica transposes separately.

## Independent verification architecture

The top-level verifier reconstructs everything from the source artifact.  It
does not consume a cached floating-point matrix or an unbound temporary
coordinate file.

1. Decode the rational holomorphic blocks, rebuild their exact support
   charts, prove blockwise positive definiteness, and evaluate the two exact
   linear functionals.
2. Apply the exact \(\Gamma_{\mathcal A}\) crossing, prove all full-face
   equations by bounded CRT reconstruction, and verify all exact rational
   face blocks against a source-hash-bound positive-definiteness reference.
3. Apply the independently derived exact \(\Gamma_{\mathcal C}\) crossing,
   prove all 751-face equations by bounded CRT reconstruction, and verify its
   exact rational blocks against a second source-hash-bound reference.
4. Audit the pair-exchange and complementary-transpose identities on matrix
   units.

Run

```text
python3 verification/verify_dth_complete_ppt_pseudomoment.py
```

The verifier is deterministic and exact, but it uses NumPy and SymPy for
integer/rational block orchestration; it is not dependency-free.

The four deterministic artifacts and SHA-256 hashes are

```text
4a42cfc9a3fcafdbf5667f5fb220eb417cea1b2f76398096668e70179e94606a
  dth_complete_ppt_pseudomoment.json.gz
d4b10997430cbe1755a07cd5e52867538577604e0a9563c0c714b3e72dacbb1b
  dth_complete_ppt_gamma1_pd_reference.json.gz
6caf453f0043a2e7296b31e2f14bc90b01f38163b1d89ece39276ac625ded9aa
  dth_gamma5_face_integer_charts.json.gz
ebc375184ff929016fda41f344b99cbe8f0d2042e563347a297e0ccd08c6b031
  dth_complete_ppt_gamma5_pd_reference.json.gz
```

The final-slot chart artifact itself is generated entirely by exact sparse
integer elimination.  Its uncompressed canonical payload hash is

```text
a69b3868fc0ae9e5098a8e54f5221a8a8f8b1f9b63485dfcfc0bc87161cbee77
```

## Consequence and remaining problem

The first constrained Pluecker lift already failed without PPT.  The theorem
above shows that the failure survives the strongest PPT condition intrinsic
to the grouped moment tripartition.  No further partial-transpose positivity
constraint at this grouped level can close the proof.  A successful DTH
proof must add a genuinely rank-one Veronese--Segre relation, a higher
Pluecker prolongation, or direct critical-point geometry on the physical
variety.

Even if DTH is later proved, the compatible common-plane/square-zero cross
inequality remains necessary before unrestricted three-copy positivity
follows.
