# Hostile audit of both marked-critical mixed-companion orbits

**Verdict:** PASS. No algebraic defect, illegal gauge, missing orbit,
rank-drop branch, hidden division, incomplete converse, or scope inflation
was found.

**Audit date:** 2026-07-25 UTC.

The principal hostile reconstruction is an exact PARI/GP implementation
that starts from the displayed homogeneous pieces and rebuilds the
Jacobians, coefficient matrices, kernels, ranks, solutions, and converses.
It does not import matrices or row reductions from the original SymPy
certificate. A second independently written PARI audit of the \(R=xq\)
half is retained in `r_xq/`.

## 1. Orbit completeness

For the marked outer pair \(H_4=(p^2,q^2,0)\), the marked member is \(p\).
The residual pencil stabilizer fixes \(p\) and \(q\) and scales their ratio.
A companion pencil member therefore has exactly three incidence orbits:

1. \(p\), giving the excluded-from-scope triple orbit \(R=xp=x^3\);
2. \(q\), giving the mixed orbit \(R=xq\); or
3. \(ap+bq\) with \(ab\ne0\), for which residual scaling gives the single
   representative \(p-q\), hence \(R=x(p-q)\).

Thus the package contains both and only the mixed marked-pair orbits. The
triple orbit is correctly left outside its theorem.

## 2. Raw \(E_7\) kernels and gauges

For each of
\[
R=xq,\qquad R=x(p-q),
\]
PARI reconstructs the full \(36\times26\) coefficient matrix of
\[
E_7=\operatorname{Jac}(p^2,q^2,W)
 +\operatorname{Jac}(p^2,V,R)
 +\operatorname{Jac}(U,q^2,R).
\]
Both matrices have rank \(18\), nullity \(8\), and the fixed maximal minor
\[
-5343626510991360.
\]

In each case, the two target-shear directions and all three source
translation jets are exact kernel directions. The three stated normal
directions complete them to a basis. Their fixed independence minors are
\[
32\quad(R=xq),\qquad64\quad(R=x(p-q)).
\]
Nullity \(8\) proves that no raw direction is missing.

The five gauge directions come from actual invertible operations: target
shears by the third component and affine source translations. They preserve
the Keller property, \(H_4\), and the cubic leading term \(R\), while only
relabeling lower pieces. Direct linear combinations of the three quotient
directions reproduce, without parameter division,
\[
\begin{array}{c|c|c}
R&(U,V)&W\\ \hline
xq&(0,A x^3+2(w_2-w_3)zq)&w_2xz+w_3y^2,\\
x(p-q)&(0,2(w_3-w_2)zq)&w_0p+w_2xz+w_3y^2.
\end{array}
\]

## 3. Complete \(E_6\) solves

In both cases, the full \(E_6\) system is affine-linear in the twelve
claimed lower unknowns and has exact rank \(10\). Parameter-free maximal
minors are
\[
-100663296\quad(R=xq),\qquad
2717908992\quad(R=x(p-q)).
\]
The displayed solutions in `NOTE.md` satisfy every coefficient equation.
Two explicit independent kernel directions are the free \(a_3\) and \(b_3\)
directions; nullity \(12-10=2\) proves completeness. In particular,
\(\ell_{32}=0\) identically, before any parameter specialization.

Let \(d=w_2-w_3\). Both constant minors remain unchanged at \(d=0\), both
specialized matrices retain rank \(10\), and direct specialized converse
substitution still annihilates \(E_6\). Thus no step divides by \(d\).

## 4. Complete \(E_5\) solves and determinant exit

After the complete \(E_6\) substitution, the full \(E_5\) systems have rank
\(4\) on
\[
(\ell_{12},\ell_{13},\ell_{22},\ell_{23}),
\]
with parameter-free minors
\[
256\quad(R=xq),\qquad2304\quad(R=x(p-q)).
\]
The unique solutions are
\[
\ell_{12}=\ell_{22}=0,\qquad
(\ell_{13},\ell_{23})=
\begin{cases}
d(a_3,b_3),&R=xq,\\
-d(a_3,b_3),&R=x(p-q).
\end{cases}
\]
Direct substitution annihilates every coefficient of \(E_5\), so there is
no unrecorded compatibility condition on the remaining lower parameters.

At \(d=0\), each \(E_5\) matrix still has rank \(4\), its unique solution
specializes to zero in all four displayed variables, and the converse
continues to vanish. Together with \(\ell_{32}=0\), this gives
\[
\ell_{12}=\ell_{22}=\ell_{32}=0.
\]
The second column of \(L\) is zero, so \(\det L=0\). Since \(\det L\) is the
constant term of \(\det JF\), neither orbit can be Keller.

## 5. Adversarial findings and scope

No resultants, denominator clearing, irreducibility assumptions, or generic
recovery arguments occur. The constant minors rule out all parameter rank
drops, and the explicit \(d=0\) reruns rule out the most plausible omitted
branch.

The PASS verdict is exactly scoped to the two marked mixed companion
orbits. It does not audit the marked triple orbit, the completeness of the
larger rank-one-restriction reduction, or any priority claim.

Run:

```text
./verify_marked_mixed_pari_strict.sh
./r_xq/verify_r_xq_pari_strict.sh
../verify_marked_mixed_sympy.py
```

These exact computations are evidence about the encoded algebra, not peer
review.
