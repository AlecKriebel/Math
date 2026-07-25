# Verification transcript

UTC run time: `2026-07-25T09:45:21Z`

## Artifact hashes

```text
1e47543dd2f7acc9ed59d1705d17b4f69d2fd594dd5616148533aa3919c3e41a  verify_ranktwo_triple_sympy.py
a086286182886fbcf520a5c98355f9bdd553ddd466628434ffa1547c3790361d  audit_hostile/verify_ranktwo_triple_pari.gp
6bd00fce6a3b3d7a2b92f9b6ead7a05f490d2d274aff9620275eae163212abf6  audit_hostile/verify_ranktwo_triple_pari_strict.sh
80401dcf8a2dacf76c15e8242229fa6cdc6afe1956c815af3fdada8934351b62  audit_hostile/test_fail_closed.sh
```

## Strict PARI run

```text
PASS raw E7: rank 8/nullity 18; five legal gauges plus thirteen normals form the full kernel
PASS E6: constant pivot makes w3=w5=0 and the K/M split specialization-safe
PASS K!=0 E5: polynomial left syzygies and exact resultant force w1=w2=0, leaving only S=0
PASS aligned nonresonant K!=0: E5 localization is exactly (3A-8w4)(3A-4w4), and E4 forces det(L)=0
PASS 9A=2K: nonzero ends are excluded by z4 after y/z symmetry; the freshly solved aligned rank-drop chart also forces det(L)=0
PASS 9A=K: B3-localized solve forces det(L)=0; y/z symmetry covers B1-only, and the zero pair lies in the nonresonant aligned chart
PASS K=0,A!=0: six E5 compatibilities leave only B2, and a fresh A-localized solve zeros four entries of L
PASS K=A=0 open chart: necessary tail parametrization and an exact localized E5 solve give 4*s^4/27
PASS K=A=0 rank drops: C=0 is global; r=0 splits safely into B3!=0 cross-multiplied E5 and B3=0 fresh E4 charts
PASS terminal chart: global literal E5 rows split on a4, and both branches force l32=l33 without the unsafe B1 localization
ALL HOSTILE PARI/GP RANK-TWO e=2 TRIPLE-COMPANION CHECKS PASSED
```

## Fail-closed run

```text
PASS fail-closed injections: arithmetic corruption and missing attestation rejected
```

The primary verifier also completed normally, and
`/usr/bin/python3 -O verify_ranktwo_triple_sympy.py` exited with status
`2` and the required assertion-disabled diagnostic.
