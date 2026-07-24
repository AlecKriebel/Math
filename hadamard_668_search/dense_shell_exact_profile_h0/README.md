# Exact dense-shell `h=0` profile certificate

## Result

The production dense-shell classifier found the explicit order-three
profile

```text
A IDs = 1,1,2,4,4,5,1,1,2,4,4,5
B IDs = 5,5,1,7,4,1,5,5,1,7,4,1
target  = (2,-2,-4,-2).
```

With `omega^2+omega+1=0`, profile ID `(p0,p1,p2)` denotes

```text
(p0-p2) + (p1-p2) omega.
```

Using the recorded channel/parity normalization, the independent verifier
expands the two compressed words to all 37 physical positions and obtains

```text
D_0 = 167,
D_t = 0 for every t=1,...,36.
```

The profile has shell counts `(n9,n3,n0)=(0,18,6)`.  Under the exact
`C6 x C2(A-star) x C2(B-star)` action it is canonical, has stabilizer order
2, and has orbit size 12.  The stabilizer is profile-level half-turn
symmetry only; it must not be imposed as equality on a labelled physical
lift.

This is a decisive exact **profile-level** discovery.  It is not yet a
labelled Legendre pair of length 333 and therefore not yet a Hadamard matrix
of order 668.

## Independent verification

From the repository root:

```text
python3 \
  hadamard_668_search/dense_shell_exact_profile_h0/verify_exact_profile_h0.py
```

The verifier uses only the Python standard library.  It does not import the
production classifier or any incremental correlation logic.  It rebuilds:

- the ten-profile Eisenstein alphabet;
- all twelve cyclotomic classes in `F_37^*`;
- both 37-position physical compressed words;
- all 37 exact Eisenstein correlations;
- the exact 24-element orbit and stabilizer;
- the production witness digest; and
- three canonical semantic SHA-256 hashes.

## Lift status

Independent follow-up audits give 54 placement trits and a consistent first
upper phase digit of rank 18 and nullity 36.  The exact trivial-character
transfer has 64 compatible signatures and intersects the universal
row-margin catalog in 72 rows, representing
`297,203,044,612,626,864,000` labelled root-character assignments.

A bounded exact endpoint pilot on catalog row 17 remained `UNKNOWN`; no
labelled lift is claimed.  The shortest rigorous continuation is to shard by
the 72 row margins, solve all 18 second-digit quadrics jointly, require
consecutive third- and fourth-digit replays, and then check the remaining
digits/full 166 Legendre-pair correlations.  The profile half-turn is not a
valid labelled-lift symmetry and must not be added as a word constraint.

## Provenance

The minimal certificate records the original production source and binary
hashes, shard, timestamp, raw candidate-file hash, production digest, orbit
hash, and full physical-replay hash.  The large transient runner record was

```text
/tmp/h668-dense-nonzero-smoke/candidates/h0-p00-p00.json
```

and its SHA-256 is pinned in `certificate.json`.
