# Clean-room referee report: ordinary JC triangle redirection

Status: **VERIFIED**, with the scope limitation stated below.

## Verdict

The active ordinary-triangle certificate is mathematically correct for the
locked `sd0` convention and the strict open JC parameter domain.  A wholly
separate standard-library implementation verifies all of the following.

1. Each of the three rooted witnesses is a valid binary, acyclic,
   LSA-rooted, tree-child network.
2. One-step reticulation-preserving root suppression produces a simple binary
   mixed graph.  Each graph has one reticulation, one triangle, no omnian, and
   exactly five admissible rootings; all five are tree-child.
3. The three labelled mixed graphs are pairwise nonisomorphic.  Exhausting the
   three possible choices of reticulation vertex on the fixed labelled
   triangle produces exactly these three graphs.  Removing the two local
   triangle arrowheads gives one common labelled graph and one ordinary-`T`
   quotient.
4. At the claimed strict interior rational parameters, direct displayed-tree
   summation gives identical values for all 64 Fourier coordinates.  The
   independently regenerated tensor has SHA-256
   `de5a240bc79bd3d5b5bf89df8f82aa46ceffed3b8a62b637568e7336b1a38324`,
   agreeing with the active claim.
5. Exact differentiation of each rooted physical parameterization gives rank
   four at the common point.  The three nonzero physical determinants are,
   in taxon order `L_0,L_1,L_2`,
   `-9/4722366482869645213696000`,
   `9/4722366482869645213696000`, and
   `-9/4722366482869645213696000`.
6. A second, independently enumerated suppressed-edge parameterization gives
   the active effective-chart determinant
   `-3/23058430092136939520` exactly.

The normalized three-leaf JC Fourier tensor has only four nonconstant orbit
coordinates.  Thus rank four is both the exact generic rank and maximal at the
common point.  By the submersion theorem, each orientation's open stochastic
image contains a neighborhood of that same tensor.  Their intersection is
therefore a common full-dimensional regular germ.

The same conclusion descends to the positive projective port-tensor quotient.
For positive arm scalings `(s1,s2,s3)`, the four coordinates transform as

```
(q12,q13,q23,q123)
  ->
(s1 s2 q12, s1 s3 q13, s2 s3 q23, s1 s2 s3 q123).
```

The stabilizer of a positive tensor is trivial, and
`q123^2/(q12 q13 q23)` is an invariant quotient coordinate.  Its value at the
certified point is `16/25`.  Since the two local images already share an open
normalized tensor neighborhood, their quotient images share an open regular
projective germ as well.

## Scope and nonclaims

This certificate proves the local positive statement needed for ordinary
triangle redirection `T`: the three labelled orientations have a common
full-dimensional regular JC port-tensor germ, and that equality can be
contracted with corresponding external contexts.

It does **not** prove equality of the complete open stochastic model images.
It does not classify any non-`T` local relation, any larger generator, or any
global network class.  Those conclusions require their own atlas and
local-to-global certificates.

## Independent method

The referee implementation imports no module from `primary/` or from another
review directory.  From first principles it implements:

- rooted degree, reachability, acyclicity, LSA, and tree-child checks;
- locked one-step `sd0` reduction;
- exhaustive edge-insertion rooting census;
- labelled mixed-graph canonicalization by exhaustive internal-vertex
  permutations;
- exhaustive orientation of the unique triangle;
- displayed-tree enumeration and descendant-split masks;
- all 64 JC Fourier coordinates over `Z_2 x Z_2`;
- exact monomial differentiation, rational row reduction, and determinant
  calculation.

The active JSON is read only as a claim.  Its topology counts, parameter-role
map, tensor, orbit coordinates, effective Jacobian, determinant, and explicit
nonclaim of complete-image equality are compared against the independent
result.

## Adversarial mutations

All eleven mutations are rejected:

1. invalid triangle-arrow orientation;
2. a boundary edge multiplier;
3. a wrong inheritance weight evaluated through the Fourier engine;
4. a reticulation/ordinary arm-role swap evaluated through the Fourier engine;
5. one changed Fourier coordinate in the claimed certificate;
6. a boundary parameter in the claimed certificate;
7. a wrong claimed inheritance weight;
8. a wrong claimed arm-role assignment;
9. collapse of two distinct orientation hashes;
10. a forged Jacobian determinant;
11. a false complete-open-image-equality claim.

The initial implementation failure is preserved under
`history/implementation_failures/`.  It exposed two useful points: structural
parameter names must be compared semantically rather than literally, and
reversing just one triangle arrow produces another valid ordinary-`T`
orientation rather than an invalid graph.  The final mutation reverses both
incoming arrows and is correctly rejected by binary validity and
root-reachability checks.

## Reproduction

From this directory, run:

```sh
bash verify_all.sh
```

The wrapper uses a clean environment, regenerates both JSON certificates in a
temporary directory, compares them byte-for-byte with the committed files,
checks the input-claim hash, and verifies the local manifest.

