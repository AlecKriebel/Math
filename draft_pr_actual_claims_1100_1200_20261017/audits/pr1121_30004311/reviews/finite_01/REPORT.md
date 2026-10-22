# Independent finite audit: PASS

Frozen target: PR1121 / problem 30004311, head `f86b108ac1bc024302648eee9f47f74e26c810ec`.

Input `PROOF.md` SHA256: `68c040d5bfe5d536e6f33f0f319a2d721bac5c562ec60f802fc516f293205b75`.

The independently authored checker finds no mathematical defect in the direct finite construction, the stated finite invariants, the ideal-propagation proof, or the explicit obstruction witnesses. The final run completed at **2026-10-17T20:13:31+00:00**, with **4,327,588 unconditional guarded requirements passing** under Python 3.14.6 with optimization enabled. There are no Python `assert` statements. Guard counts are counts of requirements, not a claim that every single arithmetic operation is separately counted.

## Reproduction and artifacts

From this directory, run:

```text
python3 -O check.py
python3 -O check.py --trace-seed 1,3,1
```

Only the Python standard library is used. The checker verifies the frozen proof digest, but does not import any historical checker, certificate, dataset, or executable code. No dependency installation, external communication, Git mutation, publication action, source retrieval, or copied third-party source is involved.

- `check.py`: independent exact implementation and finite checks.
- `results.json`: complete stage results, counts, explicit witnesses, Python version, and fingerprints.
- `execution.log`: final optimized execution output.
- `ideal_seed_derivations.jsonl`: 19,999 deterministic per-seed transcript fingerprints, routes, and operation counts.
- `sample_ideal_traces.json`: five full sample derivations, including mixed-primary and pure-primary seeds.
- `RESEARCH_LOG.md`: checkpoint history and completion estimates.
- `SHA256SUMS`: final local artifact fingerprints, excluding itself.

A ring element is encoded by the integer `a1 + 5*a2 + 25*a3 + 125*a4`; a vector is its five-bit mask. Brace elements are triples `[ring_integer, vector_mask, z]`. The four vector basis masks are 17,18,20,24. A transcript node `lambda_difference` means `lambda_actor(previous_member) - previous_member`; a node `star` means `previous_member * actor`. Actors need not already belong to the proposed ideal. Every reference points to an earlier certified member.

## Exhaustive finite coverage

| Component | Coverage |
|---|---:|
| Ring logarithm homomorphism | all 390,625 ordered ring pairs |
| Ring automorphism compatibility with addition and multiplication | all 390,625 ordered pairs for each law |
| Logarithm/exponential inverses, eta formula, sigma identities | all 625 ring elements |
| Binary form bilinearity | all 4,096 ordered triples |
| Quadratic polarization | all 256 vector pairs |
| Rotation invariance of the form | all 1,280 exponent/vector-pair cases |
| Factored first-coordinate group-product identity | all 781,250 `(r,u,e)` cases |
| First-coordinate lambda equality with a separately assembled linear matrix | all 781,250 `(r,u,e)` cases |
| Factored binary group-product identity | all 5,120 `(v,w,s,z,Z)` cases |
| Binary lambda maps | all 80 maps, all 32 inputs each; linearity and bijectivity |
| Psi inverse, direct identities, direct two-sided inverses | all 20,000 brace elements |
| Direct lambda definition on additive generators | all 180,000 actor/generator pairs |
| Sylow-5 star equals polynomial multiplication | all 390,625 ordered pairs |
| Nonzero ideal seeds | all 19,999 |

Polynomial multiplication is implemented by a general truncated convolution of coefficients, rather than by the proof's closed eta formula. Logarithm and exponential are built from ring powers and modular inverses of the stated denominators. The direct brace multiplication, explicit lambda formula, and semidirect-product coordinate multiplication are separately implemented.

The full group-product identity factors into the exhaustive ring and binary cases above. The finite checks therefore establish the product-coordinate equality for every possible pair of brace inputs without explicitly visiting all 400,000,000 such pairs. Associativity then follows analytically because the target coordinate law is the ordinary direct product of two semidirect products. Similarly, the matrix identities establish additivity of every lambda map; its invertibility follows from the already established group law (or from the unit and triangular formulas). These are finite identities combined with elementary deductions, not an enumeration of all 20,000 cubed triples.

## All ideal-seed derivations

Every nonzero starting element is projected into a nonzero primary component and then propagated to all nine additive generators. There are 19,968 seeds with nonzero ring projection and 31 nonzero binary seeds. The longest derivation has 13 permitted ideal operations.

The transcript generator and a strategy-independent certificate consumer use opposite operation encodings: generated lambda differences are recomputed with the direct circle law; generated stars are recomputed with the independent lambda formula. Scalar operations are recomputed by repeated addition. The consumer checks prior references, each output, and containment of every terminal additive generator. It replayed **259,858 individual derived nodes** across all seeds.

The nine terminal vectors generate the additive group: four polynomial monomials generate `F5^4`, the four independent masks generate the even-weight space, and the final bit generates `F2`. This verifies the construction's universal seed-propagation argument. It does not enumerate only coordinate ideals, and it does not assume that an ideal has a vector-space description. The mathematical input is the valid implication that ideal members remain members under integer multiples, `lambda_a(i)-i`, and `i*a`. As with any computation over a mathematical definition, this implication is a proof obligation rather than a property the finite computation can define into existence.

The complete per-seed receipt file has SHA256:

```text
50457c40dc45d0a3fd6c685830ad024e89c2a21c47552eda9718e403c1ad28c7
```

## Exact invariants and witnesses

| Invariant | Exact result |
|---|---|
| Globally lambda-fixed set | `{(c*x^4,0,z): c in F5, z in F2}`, order 10 |
| Socle / kernel of lambda | identity only, order 1 |
| Multiplicative center | order 5; in group coordinates, the second K-coordinate only |
| Derived subgroup | `C5^2 x C2^4`, order 400, abelian |
| Abelianization | order 50 |
| An explicit Sylow 5-subgroup | order 625, all 390,625 pairs commute |
| An explicit Sylow 2-subgroup | order 32, all 1,024 pairs commute |

The fixed set is computed by intersecting fixed sets for all 20,000 lambda maps, with 243,670 evaluations after eliminating impossible candidates. The group-coordinate generators are independently checked by traversal to generate all 20,000 group elements. The center is their common centralizer. The derived subgroup is computed from their commutators by conjugation closure and subgroup generation; its resulting 400 elements are checked pairwise commutative. Standard Sylow conjugacy extends the explicit Sylow subgroup checks to all Sylows.

The following proof witnesses match exactly:

- `x*x = x^2` and `(x*x)*x = x^3 != 0` in the additive Sylow 5-subbrace.
- `x^2 + 3*x^4` is central multiplicatively.
- For `k=(0,0,1)` and `h=(E(2*x),0,0)`, the commutator is `d=(E(x),0,0)=(x+3*x^2+x^3+4*x^4,0,0)`.
- `d*x=(x^2+3*x^3+x^4,0,0)` lies outside the globally fixed set, and `x*(d*x)=(x^3+3*x^4,0,0) != 0`.

## Adversarial controls and generalized obstruction

The following alterations produce concrete rejected controls:

1. Replacing eta by the raw fourth polynomial coefficient breaks associativity on `a=x`, `b=x^3`, and `c=(0,mask 3,0)`. The vector coordinates on the two sides are masks 6 and 3.
2. Removing Q from the exponent of sigma breaks associativity on `a=(0,mask 3,0)`, `b=(0,mask 5,0)`, `c=x`. The ring outputs are `4*x` and `x`.
3. Removing beta from the final multiplication coordinate breaks associativity on the same inputs.
4. Replacing sigma by the identity makes the crucial `b*x` propagation vanish.
5. Replacing M by the identity makes the crucial `a*(0,w,0)` propagation vanish.
6. Adding an extra cubic term to the exponential is detected by its failure to invert the logarithm.

For the generalized symmetric-cocycle claim, the checker starts without assuming biadditivity. It exhaustively enumerates 169 normalized symmetric maps over six small cyclic configurations: `(T,S)=(C2,C2),(C3,C3),(C4,C2),(C4,C2),(C3,C2),(C2,C4)`, with both the trivial and inversion actions on the two C4/C2 cases and inversion on C3/C2. Of 35 symmetric cocycles, 29 preserve the prescribed action. Exactly 12 give braces; all 17 remaining action-preserving cocycles are nonbilinear and fail the brace identity. All 12 valid cases are biadditive, and the computed lambda formula matches the manuscript's general formula. Ten have all multiplicative Sylow subgroups abelian; all 4,398 relevant primary triple tests vanish.

A necessary-hypothesis control uses `T=F2^2`, `S=F2`, the swap action, and the dot-product cocycle. All 512 triples satisfy addition associativity, multiplication associativity, and the brace identity. Its multiplicative Sylow 2-subgroup is nonabelian, and `a=(0,1), b=c=(1,0)` gives `(a*b)*c=(3,0) != 0` in the checker encoding. Thus the abelian-Sylow hypothesis is substantive and the test does not force zero triple products indiscriminately.

These finite generalized-product examples support the obstruction and expose missing hypotheses, but cannot prove its universal quantifier. The reduction from every admissible two-trivial-factor presentation to the abstract lemma remains an analytical claim for the independent theory audit. Likewise, the universal fixed-set/derived-complement and center assertions for simple two-trivial-factor products are not established by this checker. The exact finite quantities and witnesses they would use are verified here.

## Verdict and limits

**PASS for the assigned finite-construction audit; no concrete mathematical defect found.** Completion estimate for this finite audit: **100%**. The strongest checkable conclusion is a complete set of factored finite identities, independently replayed derivations for every nonzero ideal seed, exact group invariants, and verified obstruction witnesses, together with controls that fail when required construction details or hypotheses are removed.

This is an independently authored finite audit, not an external human review or proof-assistant certification. It makes no claim about historical novelty, the correctness of uninspected sources, or publication status. The universal two-trivial-factor exclusion requires the abstract mathematical argument; finite examples alone do not establish it.
