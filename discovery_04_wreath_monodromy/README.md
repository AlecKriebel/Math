# Discovery 04: full wreath monodromy through the third iterate

Status: **public research draft; not peer reviewed**.

First public repository release: **21 July 2026, 18:44:48 UTC**.
Strengthened site edition: **22 July 2026, 02:24:28 UTC**.

The provisional theorems are

```text
Mon(F^2) = S_3 wr S_3,
Mon(F^3) = S_3 wr S_3 wr S_3.
```

for the newly announced three-dimensional Keller map `F`. The groups have
orders `1296` and `13,060,694,016` in their natural imprimitive actions on
nine and 27 sheets. The normalized map
`((F o F)_1/4,(F o F)_2,(F o F)_3)` has Jacobian determinant one. A separate
bounded-memory certificate in [`w4_search/RESULT.md`](w4_search/RESULT.md)
proves `Mon(F^4)=W_4`; it is deliberately kept outside the level-three paper
so the two upgrades can be reviewed independently. The all-level full-wreath
assertion remains open.

Start with [`NOTE.md`](NOTE.md). The source-specific novelty investigation is
in [`PRIORITY_AUDIT.md`](PRIORITY_AUDIT.md), and the chronological research
record is in [`RESEARCH_LOG.md`](RESEARCH_LOG.md).
The complete file and claim inventory is in [`MANIFEST.md`](MANIFEST.md).
The rendered paper is [`output/pdf/wreath_monodromy.pdf`](output/pdf/wreath_monodromy.pdf).

## Verification

The primary exact verifier requires SymPy 1.14:

```console
python3 -m pip install -r requirements.txt
python3 verify_symbolic.py
```

An independent verifier uses only the Python standard library:

```console
python3 verify_modular.py
python3 verify_iterate_inertia.py
```

Independent PARI/GP and GAP checks are also supplied:

```console
gp -q verify_pari.gp
gap -q verify_group.g
python3 verify_level3_newton.py
python3 verify_level3_wreath.py
python3 w4_search/test_finite_field_norm.py
python3 w4_search/verify_w4_modular.py
```

`search_wreath.py` repeats the exploratory PARI `polgalois` calculation at
five unrelated rational fibers. Those arithmetic specializations are
corroboration; the proof in `NOTE.md` is geometric.

## Authorship and warning

Author: Alec Kriebel, with heavy assistance from ChatGPT 5.6 Sol (OpenAI).

Alec Kriebel is a complete amateur exploring the limits of AI-assisted
mathematics and cannot independently verify the claims. Nothing here should be
treated as established until algebraic geometers and Galois/monodromy experts
have reviewed it.
