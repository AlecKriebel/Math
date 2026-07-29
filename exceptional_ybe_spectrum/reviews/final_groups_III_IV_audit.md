# Final adversarial audit: theorem groups III--IV

**Date:** 2026-07-29  
**Audited claims:** C55, C60, C61  
**Conclusion:** all three theorems are sound at their stated scopes. No
mathematical, normalization, hypothesis, or equivalence repair is required.
The theorem notes, claim ledger, dependency ledger, and manuscript were not
edited in this audit.

## 1. Audit targets

The proof targets and claim-ledger entries were:

- C55:
  `notes/low_schmidt_control_obstruction.md`, especially lines 23--64,
  66--110, 112--279, and 281--314; `CLAIMS.md`, line 65.
- C60:
  `notes/weyl_bell_diagonal_divisibility.md`, especially lines 5--9,
  13--58, 60--145, 147--226, and 228--281; `CLAIMS.md`, line 69.
- C61:
  `notes/osr4_clifford_frame_parity_audit.md`, especially lines 28--61,
  63--96, 98--217, and 265--286; `CLAIMS.md`, line 70.

Line numbers refer to the files as audited on 2026-07-29.

## 2. C55: low operator-Schmidt rank

### 2.1 Primary-source hypotheses

The imported classification results were checked against the primary
sources:

1. Scott M. Cohen and Li Yu, *All unitaries having operator Schmidt rank 2
   are controlled unitaries*, arXiv:1211.5201, Theorem 6.
   The theorem applies to arbitrary bipartite dimensions, says either party
   may be chosen as the control, and uses rank-one basis projections with
   unitary target blocks. The paper prints a target-absorbed normalization
   with only the control-side pre- and post-unitaries. This is sufficient for
   the four-factor form in the note by taking the other two local factors to
   be identities.

2. Lin Chen and Li Yu, *Nonlocal and controlled unitary operators of Schmidt
   rank three*, arXiv:1407.5464, definition on page 2 and Theorem 11.
   Local equivalence is explicitly \(U=S_1VS_2\) for arbitrary product
   unitaries \(S_1,S_2\), hence four independent local factors. The theorem
   applies to arbitrary finite \(d_A,d_B\), not necessarily equal, and
   guarantees a controlled form from one side or the other. It does not
   promise that both sides can control.

The note states these inputs correctly at
`notes/low_schmidt_control_obstruction.md:33-45`. It handles whichever
control side Chen--Yu supplies by tensor flip at lines 105--110. Exact ranks
two and three are supplemented correctly by the immediate rank-one case.

### 2.2 Four local unitaries versus a valid Yang--Baxter conjugacy

The delicate conversion at
`notes/low_schmidt_control_obstruction.md:66-103` is correct. Starting from

\[
H=(Q\otimes S)\left(\sum_iE_i\otimes U_i\right)(R\otimes T),
\]

the note does not apply the cubic relation to the controlled middle factor.
It makes the single legitimate sitewise conjugacy

\[
\widetilde H=(Q^*\otimes Q^*)H(Q\otimes Q),
\]

which yields exactly

\[
\widetilde H=\sum_iE_i(RQ)\otimes(Q^*SU_iTQ).
\]

This conjugacy simultaneously transforms both adjacent copies on three
sites, so it preserves the shifted cubic. General four-local equivalence is
never incorrectly treated as a Yang--Baxter equivalence.

### 2.3 Internal proof audit

- The Hermitian block equation and undirected support graph at lines
  112--145 have the correct adjoint and index orientations.
- On a nonbipartite component, the alternating projective classes collapse
  to one unitary class. The component factors as \(A_C\otimes W\), and a
  rank-one spectral projection of the normal unitary \(A_C\) commutes with
  the full operator; lines 147--178 are valid.
- If every component is bipartite, unitarity makes its two off-diagonal
  blocks square unitaries. The fixed-point-free basis form at lines
  186--228 is obtained without an additional first-leg basis transformation
  of the cubic.
- The first-leg coefficient extraction at lines 230--274 is correct:
  the first cubic word vanishes, the second becomes
  \(\widetilde H(U_x\otimes I)\widetilde H\), and the linear term is
  \(U_x\otimes I\). It equates a unitary with \(c\) times a unitary, which is
  impossible when \(|c|\ne1\).
- Automatic standardness and C17 are used only in the exceptional
  application at lines 281--303. The rank-one spectator sector has
  dimension \(d^2\), common-one multiplicity \(d^2/8\), and hence
  \(8\mid d^2\), equivalently \(4\mid d\).
- The published rank-three \(d=4\) witness and identity stabilization retain
  operator-Schmidt rank three, so the sufficiency direction at lines
  305--314 is valid.

**C55 signoff:** proved as stated. No repair is required.

## 3. C60: primitive-Weyl Bell-diagonal branch

### 3.1 Primitivity and equivalence scope

The note fixes

\[
\zeta=e^{2\pi i/d},\qquad ZX=\zeta XZ,
\]

at `notes/weyl_bell_diagonal_divisibility.md:13-18`; this \(\zeta\) is
primitive. The Bell stabilizers have simple joint spectrum, so a Hermitian
involution commuting with both is exactly a sign-diagonal reflection in the
fixed Bell basis. Balance makes both partial traces zero. Thus the
equivalence claimed at lines 5--9 and 60--94 is an equivalence inside this
fixed symmetry class, not a claim that an arbitrary exceptional solution is
locally conjugate to it.

### 3.2 Common Weyl action and multiplicities

The three-site operators

\[
\mathsf X=X_1X_2X_3,\qquad
\mathsf Z=Z_1^{-1}Z_2Z_3^{-1}
\]

commute with both shifted copies, and their commutation phase is
\(\mathsf X\mathsf Z=\zeta\mathsf Z\mathsf X\), as asserted at lines
96--119. Primitivity makes the \(d^2\) Weyl monomials independent, so the
generated algebra is isomorphic to \(M_d(\mathbb C)\). Its representation
on the \(d^3\)-dimensional space has multiplicity \(d^2\), and every
eigenvalue multiplicity of a commuting operator is divisible by \(d\);
lines 120--145 are correct.

The shifted cubic gives

\[
(U-I)\left(U^2+\frac23U+I\right)=0.
\]

Conjugation by the reflection sends \(U\) to \(U^{-1}\), pairing the two
nonreal roots. The zero Bell marginals give \(\operatorname{Tr}U=0\).
Consequently the multiplicities are

\[
\left(\frac{d^3}{4},\frac{3d^3}{8},\frac{3d^3}{8}\right).
\]

Divisibility of the nonreal multiplicity by \(d\) gives
\(8\mid3d^2\), hence \(4\mid d\). All signs, factors of \(d\), and
root multiplicities at lines 147--207 check.

The finite \(d=4\) corollary at lines 228--281 is explicitly confined to
the same fixed Bell basis and is backed by an unquotiented exact exhaustion
of all \(\binom{16}{8}=12{,}870\) balanced sign tables.

### 3.3 Optional wording only

Two nonessential wording changes would make the scope even harder to
misread:

1. At `notes/weyl_bell_diagonal_divisibility.md:121`, change “the algebra
   generated by \(\mathsf X,\mathsf Z\) is \(M_d(\mathbb C)\)” to “is
   isomorphic to \(M_d(\mathbb C)\).” The present meaning is already clear
   from the representation discussion.
2. At line 51, change “the complete rank-\(18\)
   generalized-Bell-diagonal ansatz” to “the complete rank-\(18\)
   projection Bell-diagonal ansatz,” so “rank” cannot be mistaken for
   operator-Schmidt rank.

Neither wording point affects the theorem.

**C60 signoff:** proved at the stated primitive-Weyl, fixed-Bell-basis
scope. No mathematical repair is required.

## 4. C61: four-product Clifford frame

### 4.1 Exact load-bearing hypothesis

The theorem at `notes/osr4_clifford_frame_parity_audit.md:28-51` assumes
that the four **product** involutions

\[
T_j=A_j\otimes B_j
\]

anticommute pairwise. It does not assume that either local family itself is
pairwise anticommuting, and it does not infer that conclusion.

For each pair, equality of two nonzero simple tensors gives a scalar
\(\zeta_{ij}\). Involutivity forces \(\zeta_{ij}^2=1\), so each local pair
either commutes or anticommutes, with the opposite choice on the other leg.
The complementary commutation-graph identity at lines 98--127 is therefore
valid.

### 4.2 Clifford and parity steps

- An alternating commutation matrix of binary rank \(2r\) supplies \(r\)
  commuting Weyl pairs and a unital copy of \(M_{2^r}(\mathbb C)\).
  Representation dimension is therefore divisible by \(2^r\); lines
  132--149 are valid.
- The four-vertex complement lemma at lines 151--176 correctly follows from
  the two Pfaffian equations. Its path/star case split is complete.
- For \(d=2s\) with \(s\) odd, the complete-graph commutation matrix has
  binary rank four. Neither local graph can have rank four, so both have
  rank two. The complement lemma supplies an isolated original generator
  on one leg and an anticommuting pair on that same leg.
- The anticommuting pair is unitarily \(Z\otimes I_s,X\otimes I_s\).
  The isolated generator is therefore \(I_2\otimes L\). A Hermitian
  involution \(L\) in odd dimension has nonzero trace, contradicting the
  assumed tracelessness of the local factor. The proof at lines 178--217 is
  complete.

The theorem does not use the exceptional cubic, automatic standardness,
faithfulness, or a controlled-unitary normal form. The limitations at lines
53--61 and 265--286 correctly state that arbitrary operator-Schmidt-rank
four involutions need not have involutory Schmidt factors or pairwise
anticommuting product terms.

The auxiliary rank-existence statement at lines 63--73 was also checked
against Alexander Müller-Hermes and Ion Nechita,
*Restrictions on the Schmidt Rank of Bipartite Unitary Operators Beyond
Dimension Two*, arXiv:1612.07616, Theorem 1.3: outside
the \(2\times2\) exception, every rank from \(1\) through
\(\min(d_A,d_B)^2\) occurs; in \(2\times2\), rank three is the sole missing
rank.

**C61 signoff:** proved exactly under the pairwise-anticommuting
product-term hypothesis. No repair is required.

## 5. Independent exact replay

From `/Users/alec/Documents/Math-kissing5`, using
`/Users/alec/Documents/Math/.venv/bin/python`, the following verifiers were
run and their standard output compared byte-for-byte with the retained
outputs:

```text
verifiers/verify_low_schmidt_control_obstruction.py
  results/low_schmidt_control_obstruction_exact.txt

verifiers/verify_weyl_bell_diagonal_divisibility.py
  results/weyl_bell_diagonal_divisibility_exact.txt

verifiers/verify_d4_bell_diagonal_exhaustive.py
  results/d4_bell_diagonal_exhaustive_exact.txt

verifiers/verify_osr4_clifford_frame_parity.py
  results/osr4_clifford_frame_parity_exact.txt
```

All four comparisons passed. The replay produced respectively
6, 8, 5, and 6 output lines and completed in approximately 27 seconds on
the audit machine.

## 6. Final disposition

- C55: **SIGNOFF**
- C60: **SIGNOFF**
- C61: **SIGNOFF**
- Required theorem repairs: **none**
- Optional wording clarifications: **two**, both in C60 and listed in
  Section 3.3
- Source theorem notes, ledgers, and manuscript edited by this audit:
  **none**
