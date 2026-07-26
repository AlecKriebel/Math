# Audit report: binary fixed-conic E7/E6 repair

## Verdict

\[
\boxed{\textbf{PASS-CLOSED for the assigned E7/E6 tangent reduction}}
\]
\[
\boxed{\textbf{FAIL-CLOSED for the later branch endgames from this
artifact alone}}
\]

The retained exact checker begins with equation (4), all 12 coefficients
of \(V\), all 18 coefficients of \(H_2\), and all 9 entries of the linear
part.  It uses no parameter-dependent pivot.

## Exact results

| conic | E7 equations | \(H_2\)-rank | free \(H_2\) | reduced E7 compatibility |
|---|---:|---:|---:|---|
| \(h=pq\) | 22 | 7 | 11 | \(e=f=b=c=0\), \((3a-d)v_8=(a-3d)v_3=0\) |
| \(h=p^2\) | 20 | 7 | 11 | \(e=f=b=0\), \((a-4d)v_2+6(2d-a)v_7-6cv_3=0\), \((a-2d)v_3=0\) |

After substitution of the complete affine E7 fibres, with every free
lower coefficient and arbitrary \(L\) retained,
\[
[r^2]E_6=12p^2q^2(a-d)^2(a+d)
\]
for \(h=pq\), and
\[
[r^2]E_6=24dp^2\bigl(cp+(d-a)q\bigr)^2
\]
for \(h=p^2\).  Thus equations (7) and (8) are universal.

Polynomial sections with \(V=0\), free \(H_2=0\), and \(L=0\) prove that
the exact tangent-elimination ideals are
\[
I_{pq}=\langle(a-d)^2(a+d)\rangle,\qquad
I_{p^2}=d\langle c,d-a\rangle^2.
\]
Their radicals are
\[
\sqrt{I_{pq}}=\langle(a-d)(a+d)\rangle
\]
and
\[
\sqrt{I_{p^2}}
=\langle dc,d(d-a)\rangle
=\langle d\rangle\cap\langle c,d-a\rangle.
\]
These components give exactly
\[
h=pq:\quad 2A,\ pA_p-qA_q,\ 0,
\]
\[
h=p^2:\quad 2A,\ pA_p,\ pA_q,\ 0.
\]
All intersections and E7 compatibility-rank jumps are checked exactly.
No counterexample to equations (7)--(9) was found.

## Fail-closed implementation

`verify_binary_fixed_conic_repair.py` uses explicit `require` checks which
raise `VerificationFailure`; it contains no Python `assert` statements,
so optimization cannot erase a mathematical check.  `verify_strict.sh`
runs it under `python -O`, pins exact SymPy 1.14.0, and exits on the first
failure.

## Remaining composition boundary

This repair supplies a complete ingress to every tangent branch, but it
does not rederive the later branch-specific families in Sections 3--8 of
`WORKING_FIXED_CONIC_ROW.md` from all eleven free \(H_2\) parameters and
the compatible \(V\) space.  Therefore it closes the audit's specific
equations-(7)--(9) gap, while leaving the later full-fibre spanning
obligation unclaimed.  See Section 7 of `NOTE.md` for the precise
interface.
