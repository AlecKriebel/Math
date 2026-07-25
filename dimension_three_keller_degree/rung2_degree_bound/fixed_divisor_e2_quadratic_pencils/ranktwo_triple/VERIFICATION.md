# Verification

## Current status

The corrected SymPy certificate and a methodologically independent
PARI/GP reconstruction both pass.  Hostile review found three unsafe
specializations in the provisional proof; every one is now rebuilt
fresh in both backends.  The theorem is audited but not peer reviewed.

Run

```sh
/usr/bin/python3 verify_ranktwo_triple_sympy.py
```

The script verifies:

- the raw \(36\times26\) \(E_7\) matrix, a nonzero rank-eight minor,
  and a complete eighteen-vector kernel;
- the five legal gauge directions and thirteen normal directions;
- the exact \(E_6\) compatibility split;
- the \(K\ne0\) resultant argument and both resonance charts, including
  the fresh rank-four aligned solve at \(9A=2K,\ B_1=B_3=0\);
- the aligned determinant exit on \(K\ne0\);
- the fresh rank-drop solve on \(K=0,A\ne0\);
- the three cross-multiplied polynomial syzygies at \(K=A=0\);
- the generic and both rank-drop nonzero-\((w_1,w_2)\) charts,
  including the fresh \(r=0,B_3=0\) solve that the generic left vector
  cannot cover; and
- the parameter-free terminal \(E_5\) product split when
  \(w_1=w_2=0\), followed by fresh \(a_4=0\) square and
  \(a_4\ne0\) linear \(E_4\) exits.

Assertions are mandatory; `python -O` exits with status \(2\).

Run the independent hostile audit with

```sh
cd audit_hostile
./verify_ranktwo_triple_pari_strict.sh
./test_fail_closed.sh
```

`audit_hostile/REPORT.md` records the three rejected generic
specializations, their repairs, the complete scope audit, and the final
PASS verdict.
