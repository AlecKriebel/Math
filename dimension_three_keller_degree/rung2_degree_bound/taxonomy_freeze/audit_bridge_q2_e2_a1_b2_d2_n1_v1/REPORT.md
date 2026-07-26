# Post-freeze audit of `Q2-E2-A1-B2-D2-N1`

## Verdict

\[
\boxed{\textbf{FAIL-CLOSED}}
\]

Do not promote the global fixed-conic row from the supplied working notes
and exact scripts.  The smallest retained-evidence gap is the binary
degree-six branch reduction: equations (7)--(9) of
`WORKING_FIXED_CONIC_ROW.md` are checked only on a particular specialization,
not derived as necessary compatibility conditions for arbitrary lower
terms.

This is a failure of the proposed bridge package, not a counterexample to
the claimed theorem.  The spot identities checked by the scripts all pass.

## 1. Independent frozen-row route

Before opening either working bridge, this audit derived
\[
F=LX+H_2+H_3+h(p,q,r)(p^2,pq,q^2)^T,                \tag{1}
\]
where \(L\in GL_3\), \(H_2\) and \(H_3\) are completely arbitrary
homogeneous vector maps of dimensions 18 and 30, and \(h\) is every nonzero
ternary quadratic.  Independent source and target changes are required;
one may not simultaneously demand \(L=I\).

The conic triple is a basis of the binary quadratics.  Hence every original
target component of \(H_4\) is nonzero.  The coefficient-pivot-independent
coverage map is therefore:

| frozen pivots | route |
|---|---|
| `C00`--`C14` | pointwise to (1), without division by the frozen pivot |
| `C15`--`C44` | intrinsically empty |

`verify_phase_a_uniform_nf.py` retains the frozen tuple, all 45 labels, this
coverage, the leading kernel identities, and the complete lower-term
dimensions.

## 2. What was independently recovered downstream

For binary \(h\), the degree-eight identity gives the full cubic normal
\[
H_3=V(p,q)+r((ap+bq)A_p+(cp+dq)A_q)
       +\frac{r^2}{2}(eA_p+fA_q),                    \tag{2}
\]
with all 12 coefficients of \(V\).  Starting with (2) and all 18
coefficients of \(H_2\), the independent raw degree-seven calculation
confirms
\[
\begin{array}{c|c}
h=pq&e=f=b=c=0,\\
h=p^2&e=f=b=0.
\end{array}                                         \tag{3}
\]
This calculation is retained in
`verify_binary_raw_e7_and_retention_gap.py`; thus the failure is strictly
after equation (6) of the working binary note.

The seven quadratic normal forms
\[
p^2,\ pq,\ r^2,\ r^2+p^2,\ r^2+pq,\ pr,\ pr+q^2
\]
are an exhaustive parabolic classification over \(\mathbb C\).  The four
upstream exact scripts also execute successfully.  In particular, this
audit found no arithmetic mismatch in the displayed nonbinary endgames.
None of those facts repairs the binary gap below.

## 3. Exact smallest gap

The working note next claims that, after solving the remaining
degree-seven equations, degree six necessarily supplies
\[
12p^2q^2(a-d)^2(a+d),\qquad
24dp^2(cp+(d-a)q)^2,                                \tag{4}
\]
and therefore that its listed tangent branches are exhaustive.

The retained SymPy check does something weaker:

* it defines only the already-specialized tangent fields
  `split_W = a*p*Ap + d*q*Aq` and
  `double_W = a*p*Ap + (c*p+d*q)*Aq`;
* it sets \(V=0\);
* it replaces the arbitrary 18-coefficient \(H_2\) by one displayed
  \(r^2Z\);
* it sets the linear part to zero; and
* it expands the determinant of that particular tuple.

Concretely, these are
`verify_fixed_conic_row_sympy.py` lines 127--154.  Although a general
`H2_general` is constructed at lines 168--173, it is never loaded anywhere
in the script.  The PARI checker repeats precisely the same specialization
at lines 19--27.  Neither implementation computes a left-null
compatibility, elimination remainder, kernel-spanning certificate, or
division-free ideal containment showing that (4) follows for **every**
\((V,H_2)\) satisfying degree seven.

Checking a polynomial on one particular solution does not prove it is a
necessary compatibility condition on the full affine solution family.
Consequently an unretained branch could exist before every later
branch-specific endgame.  The later prose saying that an adversarial raw
solve found none is aggregate audit prose and, under the requested audit
standard, cannot fill this gap.

## 4. Minimal repair needed for promotion

Retain an exact binary checker which starts from (2), a general
18-coefficient \(H_2\), and an arbitrary \(3\times3\) linear part, then:

1. solves the full degree-seven system without generic-rank division;
2. proves by explicit compatibility or ideal certificates that degree six
   forces exactly the factors in (4);
3. proves the resulting tangent-orbit list, including all zero and
   rank-jump specializations, is exhaustive; and
4. proves each later displayed \(H_3,H_2\) family spans the complete
   solution fibre before applying its terminal obstruction.

Until that retained calculation exists, the inclusive binary locus and
hence the global row are not certified.  The mutable status ledger was not
edited, and no commit or push was made.

## 5. Audited file identities

The audit examined these exact SHA-256 versions:

| file | SHA-256 |
|---|---|
| `WORKING_FIXED_CONIC_ROW.md` | `e69e9adbf553f2de9a123dc870b0ef8a971c79335fbd42461756f43824cb4586` |
| `WORKING_NONBINARY_FIXED_CONIC_ROW.md` | `257467292fe6d8146e0b0165eb3718af5fa2d2ecc66a583a9c7aafad87b75e04` |
| `verify_fixed_conic_row_sympy.py` | `e30489e57476a447d22bcdeccb1d16aea77a537a5f11842f6d74bc110f405e94` |
| `verify_fixed_conic_row_pari.gp` | `d2b281896f1d5ce09d22dd668c6f89ca0328099ef52995beff563f7f2826e303` |
| `verify_nonbinary_fixed_conic_sympy.py` | `02c6174c6baffaf496017ed2155a6312ba404b0718c80ae126b908b2849d60de` |
| `verify_nonbinary_fixed_conic_pari.gp` | `b0f09b2660579cb1cf9a214e8b17f215135493ccdaaa122c8798776a3cb082d4` |
