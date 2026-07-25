# Hostile audit report: nonbinary fixed-quadratic line double cover

## Verdict

**PASS**, conditional only on the already-banked homogeneous
rank-two/taxonomy factorization and the established low-degree plane Keller
theorem.  No omitted specialization or counterexample was found.

The theorem note and supplied verifiers were not modified.

## 1. Leading normalization

In the row
\[
(e,a,b,\delta,\nu)=(2,1,2,1,2),
\]
the factorization theorem gives
\[
H_4=h\,A(p,q),
\]
where \(p,q\) are independent linear forms, \(h\) is quadratic, and the
coprime binary quadratic pair defining \(A\) gives a degree-two cover of a
line.  After sending that line to the first two target coordinates, write
\(A=(B_0,B_1,0)\).

Riemann--Hurwitz gives two distinct simple ramification points for
\([B_0:B_1]\), and their branch values are distinct.  Independent
projectivities on the source and target lines send both pairs to
\(\{0,\infty\}\).  The zero and pole divisors are then double points, so
\[
[B_0:B_1]=[p^2:q^2].
\]
Because \(B_0,B_1\) are coprime, the residual projective scalar is a
nonzero constant.  It is absorbed in the target, proving the exhaustive
normal form
\[
H_4=h(p,q,r)(p^2,q^2,0).
\]

## 2. Logarithmic residue and global square reduction

For
\[
k=(ph_r,qh_r,rh_r-4h),
\]
direct expansion gives
\[
\operatorname{adj}(JH_4)=-2hpq\,k e_3^T.
\]
Thus \(E_8=0\) is \(D_k(H_3)_3=0\).

On \(p\ne0\), put \(t=q/p,s=r/p\), \(h=p^2H(t,s)\), and
\(G=p^dg(t,s)\).  Direct differentiation, without using the note, gives
\[
D_kG=p^{d+1}(dH_sg-4Hg_s).
\]
Work in \(K[s]\), \(K=\mathbb C(t)\).  If
\(\phi^m\Vert H\), \(\phi\) has positive \(s\)-degree, and
\(\phi^v\Vert g\), the lowest \(\phi\)-adic term of the equation is
\[
(dm-4v)\phi_s=0\pmod{\phi}.
\]
Characteristic zero and irreducibility give \(\phi_s\not\equiv0\), hence
\[
4v=dm.
\]

For \(d=3\), neither \(m=1\) nor \(m=2\) works, so \((H_3)_3=0\).
For \(d=2\), a nonzero \((H_2)_3\) requires every \(s\)-dependent factor to
have multiplicity two.  Since \(h\) has degree two, its \(r^2\) coefficient
is constant, and its \(r\)-coefficient is binary linear, this forces
\[
H=c(s+ut+v)^2,\qquad
h=c(r+uq+vp)^2
\]
in the original homogeneous polynomial ring.  This explicitly closes the
possible gap between being a square over \(\mathbb C(t)\) and being a
global polynomial square.

For a nonbinary square, replacing \(r\) by its nonbinary linear square root
keeps \(p,q\) fixed and normalizes \(h=r^2\).  Then
\[
k=(2pr,2qr,-2r^2).
\]
On a degree-two monomial \(p^iq^jr^k\), \(D_k\) has eigenfactor
\(2(i+j-k)\); its quadratic kernel is therefore exactly
\[
r\langle p,q\rangle.
\]

## 3. Stabilizer orbits

The normalized leading form has fixed line \(r=0\), with multiplicity two,
and the reduced pencil has base point \([0:0:1]\).  Any linear source
stabilizer must preserve both.  Hence
\[
r\mapsto\gamma r,\qquad
(p,q)\mapsto G(p,q),\quad G\in\operatorname{GL}_2.
\]
Compatibility with the squaring cover forces \(G\) to preserve or exchange
the two ramification lines \(p=0,q=0\); it is diagonal or anti-diagonal.
The third target coordinate can only scale, because adding either leading
line coordinate would make its quartic component nonzero.

Consequently the zero pattern of
\(r(\alpha p+\beta q)\) is invariant up to exchange.  The nonzero forms
have exactly two orbits:
\[
pr,\qquad (p+q)r.
\]
The zero form is precisely the earlier plane-field branch.

## 4. Raw ranks and converses

An audit-only PARI/GP reconstruction starts from the raw Jacobian
determinant rather than importing either supplied verifier.  All four
coefficient matrices below are constant, so none can jump at a parameter
specialization.

| orbit | system | rank | nullity | full displayed solution |
|---|---:|---:|---:|---|
| \(pr\) | raw \(E_6\), 23 unknowns | 10 | 13 | \(H_3=(2pr(ap+bq+cr),U,0)\) |
| \((p+q)r\) | raw \(E_6\), 23 unknowns | 14 | 9 | \(H_3=(-pW+2prL,qW,0)\) |
| \(pr\) | raw \(E_5\), 18 unknowns | 4 | 14 | equation (14) |
| \((p+q)r\) | post-square \(E_5\), 18 unknowns | 6 | 12 | equation (24) |

The parameter-to-coefficient matrices of the four displayed families have
the listed nullities and lie in the corresponding kernels.  Therefore the
families are full affine solutions, not underparameterized subfamilies.

For the sum orbit, the coefficients
\[
[p^5]E_5=-3w_0^2,\qquad [q^5]E_5=-3w_2^2
\]
first force \(w_0=w_2=0\), after which
\([p^3q^2]E_5=-3w_1^2\) forces \(w_1=0\).  This is division-free and leaves
\(W=r(Dp+Eq+Tr)\).

## 5. The \(pr\) branch

The split \(K=2bc-e=0\) versus \(K\ne0\) is exhaustive.

- At \(K=0\), the three displayed \(E_4\) coefficients make the first row
  of \(L_0\) equal to \((d-2ac)\) times its third row, including all
  specializations where either row is zero.
- At \(K\ne0\), the degree-four table has constant rank after factoring
  \(K\), and gives the stated \(U\) and first row.  The subsequent
  \(E_3\) matrix has rank four and is exactly \(K\) times a constant
  matrix; the \(E_2\) matrix has rank three and is exactly \(K\) times a
  constant matrix.  Thus no values of \(A,B,C,a,b,c,d,g,j\) create a
  further rank branch.  Their full solutions are (18) and (19).
  Substitution makes \(E_1\) vanish and \(\det L_0=0\) identically.

## 6. The \((p+q)r\) branch

The degree-four recurrence on \((X,Y)\) has matrix
\[
\begin{pmatrix}
D&0\\ A&D\\ \beta&A\\0&\beta
\end{pmatrix},\qquad A=\alpha+E.
\]
Its \(2\times2\) minors are
\[
D^2,\ DA,\ D\beta,\ A^2-D\beta,\ A\beta,\ \beta^2.
\]
Thus its only rank-drop point over \(\mathbb C\) is
\[
D=A=\beta=0,
\]
equivalently \(D=0,E=2a,b=a\).  There is no omitted rank-one
specialization.

Away from that point, \(X=Y=0\).  The remaining \(E_4\) solve has a
constant \(5\times5\) matrix of determinant \(-32\), so it is valid at
every specialization.  The three \(E_3\) coefficients are
\[
\frac D2M,\qquad \frac A2M,\qquad \frac\beta2M.
\]
At least one multiplier is nonzero, hence \(M=0\).  Exact polynomial
division in the unsolved linear entry gives remainder zero:
\[
M\mid\det L_0.
\]

At the exceptional point, the same constant-rank \(E_4\) solve is valid,
and
\[
[p^3]E_3=-2X^2,\qquad[q^3]E_3=-2Y^2
\]
forces \(X=Y=0\).  With the note's \(M_*,A\),
\[
[pr]E_2=M_*A,\qquad[p]E_1=M_*(aA-M_*).
\]
The division-free combination
\[
a[pr]E_2-[p]E_1=M_*^2
\]
forces \(M_*=0\).  Independent exact division gives
\[
M_*\mid\det L_0.
\]
This remains valid when \(a,c,\gamma,R-S\), or any other parameter is zero.

## 7. Plane-field exit

When \((H_2)_3=(H_3)_3=0\), the third component of \(F\) is a nonzero
linear form because \(L_0\) is invertible.  Linear changes give
\[
F=(P,Q,r),\qquad
\frac{\partial(P,Q)}{\partial(p,q)}\in\mathbb C^\times.
\]
Over \(K=\mathbb C(r)\), \((P,Q)\) has degree at most four in \(p,q\).
The established plane low-degree theorem applies after base change to
\(\overline K\).  This does not inherit or assume the full plane Jacobian
conjecture: a hypothetical degree-four failure over \(\overline K\) would
descend to finitely generated characteristic-zero coefficients and embed
into \(\mathbb C\), contradicting the known complex low-degree theorem.

Generic degree is invariant under algebraic base change, so the plane map
has degree one already over \(K\):
\[
K(p,q)=K(P,Q).
\]
Hence \(F\) is birational over \(\mathbb C\), and the classical birational
Keller theorem makes it a polynomial automorphism.

## 8. Verifier audit and corrections

- The supplied SymPy verifier is protected against optimized Python:
  `PYTHONOPTIMIZE=1` exits nonzero before any `assert` can be skipped.
- Its raw parameter spaces are complete: 20 cubic, 12 quadratic, and the
  relevant linear coefficients are present before the proved reductions.
- Some later completeness facts are implicit rather than asserted:
  specifically the \(K\ne0\) \(E_3/E_2\) ranks and the literal determinant
  quotients.  The audit verifier now checks these independently.
- The supplied PARI/GP verifier begins after several proved normalizations
  and does not check the raw ranks.  This matches its disclosure; the
  audit GP file supplies those checks.
- The supplied strict GP wrapper passed fault injection: it rejected a GP
  diagnostic, extra output after the sentinel, and a nonzero GP exit.

Recommended exposition corrections, none theorem-breaking:

1. Spell out the passage from a square in \(\mathbb C(t)[s]\) to
   \(h=c(r+uq+vp)^2\) in \(\mathbb C[p,q,r]\).
2. Prove full stabilizer exhaustion using the fixed line, reduced base
   point, and ramification lines; diagonal normalization alone does not by
   itself prove there are exactly two full-stabilizer orbits.
3. State that all four raw coefficient matrices are constant, and record
   the \(K\ne0\) \(E_3/E_2\) ranks.
4. For maximal auditability, state the two explicit identities
   \(M\mid\det L_0\) and
   \(a[pr]E_2-[p]E_1=M_*^2\) as polynomial identities.

## 9. Exact audit artifacts

- `audit_reconstruct_pari.gp`
- `audit_reconstruct_pari_strict.sh`
- `audit_supplied_wrapper_selftest.sh`
- `RESEARCH_LOG.md`

The strict audit marker is
`AUDIT_FIXED_QUADRATIC_LINE_PARI_PASS_41D8C2`.
