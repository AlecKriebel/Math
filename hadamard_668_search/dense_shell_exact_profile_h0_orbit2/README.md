# Second exact dense-shell `h=0` profile orbit

## Result

The first heavy production prefix, `h0-p00-p05`, found the exact profile

```text
A IDs = 1,2,6,1,5,1,4,5,1,5,7,4
B IDs = 2,4,2,4,4,6,5,5,8,1,5,8
target  = (-3,0,0,3).
```

After expansion from the twelve order-three cyclotomic classes to all
positions of `F_37`, independent integer Eisenstein arithmetic gives

```text
D_0 = 167,
D_t = 0 for t=1,...,36.
```

The shell census is again `(n9,n3,n0)=(0,18,6)`.  Under the exact
24-element profile action, this representative is canonical with trivial
stabilizer and orbit size 24.  Its orbit is disjoint from the previously
certified 12-element `h=0` orbit, so it is a genuinely second profile orbit,
not a re-expression of the earlier point.

This is an exact compressed profile.  It is not a labelled placement,
Legendre pair of length 333, or Hadamard matrix of order 668.

## Verification

From the repository root:

```text
python3 \
  hadamard_668_search/dense_shell_exact_profile_h0_orbit2/verify_exact_profile_h0_orbit2.py
```

The verifier imports only the dependency-free Eisenstein and group-action
primitives from the first profile's independent verifier.  It does not
import the production classifier.  It reconstructs all 37 physical
positions and correlations, the full orbit and stabilizer, the semantic
hashes, the production digest, and disjointness from the first orbit.

## Provenance and census status

The hash-pinned production run stopped immediately on discovery, after
44,172 of the prefix's 110,976 raw skeletons.  Therefore neither this
prefix nor the two dense shells are classified yet.  The production source,
binary, raw candidate record, timestamp, counters, and digest are frozen in
`certificate.json`.

Continuation must enumerate rather than stop at exact profiles, retain every
distinct canonical orbit, and complete all 729 prefixes per shell before
making a shell-classification claim.
