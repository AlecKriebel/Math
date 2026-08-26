# Literal-map tree--sunlet separator v2

This directory is a self-contained correction package for the ordinary
three-sunlet convention

```text
q_xyz = a_x b_y c_z [L f_y d_z + (1-L) f_x e_z].
```

The certificate keeps the displayed edge order `(a,b,c,d,e,f)` literally.  In
particular, the three composition margins are on `f`, while `d` and `e` occur
in the paired cross factors.  The six exact pullbacks are positive
arm/inheritance monomials times the factors printed in the JSON certificate;
their signs are part of the certificate.

Run all local checks from the project root:

```sh
python3 three_port/literal_separator_v2/generate_literal_separator_v2.py \
  --check three_port/literal_separator_v2/K3P_TREE_SUNLET_LITERAL_SEPARATOR_V2.json
python3 three_port/literal_separator_v2/verify_literal_separator_v2.py
python3 three_port/literal_separator_v2/test_literal_separator_v2_mutations.py
```

The generator performs deterministic sparse expansion over `ZZ`.  The
independent verifier imports no generator helpers and reconstructs the literal
map, tree pullbacks, six sunlet pullbacks, factorizations, expanded-polynomial
digests, and strictness cancellations.  The mutation suite includes a cyclic
`d/e/f` factor rename whose payload is resealed while the map remains fixed;
the independent re-expansion must reject it as a literal pullback mismatch.
