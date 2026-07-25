# Verification

## Primary exact certificate

Run the fail-closed wrapper:

```text
./verify_marked_triple_sympy_strict.sh
```

It invokes `/usr/bin/python3` with assertions enabled and requires the
literal final marker

```text
ALL MARKED TRIPLE-ORBIT SYMPY CERTIFICATES PASSED
```

The SymPy program reconstructs:

1. the raw \(E_7\) matrix, its fixed maximal minor, and the complete
   five-gauge/thirteen-normal kernel;
2. the constant-rank \(E_6\) solve and exact \(A/K\) compatibility
   ideal;
3. the \(K\ne0\) branch, including a fresh
   \(A=0,C\ne0\) solve rather than specialization of the generic
   \(A\)-pivot;
4. the \(K=0,A\ne0\) branch on the two explicit \(B_1/B_2\) open
   charts and on the freshly rebuilt \(B_1=B_2=0\) rank-drop strata;
5. the \(K=A=0\) literal product ideal for arbitrary \(V\), its
   \(a_3=0\) leaf, and the unique exceptional \(V=Czq\) leaf.

In particular, it explicitly checks that \(\ell_{13}\) remains free on
\(K=0,A\ne0,B_1=B_2=0,C\ne0\), and that \(a_3\) can remain nonzero
when \(K=A=0,V=Czq\).  The repaired \(E_3\) exits, not the invalid
generic specializations, close those leaves.

The primary corruption test is:

```text
./verify_marked_triple_sympy_fail_closed.sh
```

It independently corrupts the raw \(E_7\) minor and one assertion in
each of the three repaired rank-drop leaves.  It succeeds only if the
primary verifier rejects all four altered certificates.

## Independent hostile reconstruction

Run:

```text
./audit_hostile/independent/verify_marked_triple_pari_strict.sh
./audit_hostile/independent/verify_fail_closed.sh
```

The PARI/GP program independently rebuilds the weighted Jacobian systems,
fixed pivots, literal compatibility rows, and all repaired rank-drop
leaves.  Its report is
`audit_hostile/independent/AUDIT.md`; the full promotion-blocking defect
record is also in `audit_hostile/AUDIT.md`.

The SymPy and PARI/GP implementations are separate exact-algebra
backends.  Their agreement is evidence about the encoded algebra, not
peer review.
