# Independent algebra audit of PR 826 / problem 30003060

**Decision: CLEAR for the stated mathematical counterexample and orbit calculation.** This is validation of the candidate at frozen head `286cc67c0727b4decfd4f261a0591cd8823ebce9`, not a novelty judgment or human/formal certification. No old reviewer conclusions, author checker, or old reviewer checker was read or reused. The candidate proof was read, then its algebra reconstructed from definitions and independently checked against the exact primary version below.

The exact unrestricted-field claim rejected by the example is: every Koszul quadratic algebra has vanishing positive-degree higher Koszul homology with coefficients in the algebra and differential induced by its fundamental cocycle. The reconstructed counterexample rejects that implication over every positive characteristic. The calculation does not resolve the characteristic-zero converse, the general sufficiency of vanishing in positive characteristic, or historical intention behind an ambiguously stated question. Those are outside this algebra audit.

## Assumptions and success criteria

Let k be any field and V a vector space with finite basis of size r. Form the ordinary associative tensor algebra A=T_k(V), internally graded by word length; this is not a superalgebra. Take R=0 in its quadratic presentation. Use algebra coefficients M=A, not trivial coefficients k. Homological degree and internal weight are distinct: C_1 in total weight n has coefficient weight n-1; C_0 in total weight n has coefficient weight n.

Success requires a linear free resolution proving Koszulness, an unambiguous two-stage homology calculation, a nonzero cycle with zero higher differential in each prime characteristic, and a proof of the full orbit formula including boundary/degenerate cases. Bounded computations are corroboration and falsification controls, not substitutes for these infinite deductions.

## Reconstruction of the two stages

For j>=2 the intersection defining W_j contains only zero subspaces because every term contains R=0. Hence W_j=0. The coefficient complex is exactly

    0 -> C_1=A tensor V --b--> C_0=A -> 0,
    b(a tensor v)=av-va.

There are no ordinary boundaries entering C_1, so HK_1=ker b as an actual subspace of C_1. HK_0=A/im b and HK_j=0 for j>=2.

For completeness, im b is the whole commutator subspace. If u,v are words, the concatenations uv and vu are cyclic shifts of each other; moving one final letter to the front at a time expresses uv-vu as a telescoping sum of generator commutators. Bilinearity then covers arbitrary elements. No quotient by a two-sided commutator *ideal* is taken: this is a quotient by a vector subspace, which retains the separate cyclic-word classes.

The fundamental degree-one cochain is e(v)=v. The primary left cap convention specializes to e cap (a tensor v)=va with sign +1. The primary right cap specializes to (a tensor v) cap e=-av. For a cycle z=sum a_i tensor v_i, the cycle equation is sum a_i v_i=sum v_i a_i. Consequently the left cap gives exactly sum a_i v_i even before passing to HK_0. This validates the candidate's delta([z])=[sum a_i v_i]; no sign or cap-convention repair is needed. Using the right cap instead would negate this map, preserving its kernels, image subspaces and higher homology in every characteristic. In degree one no other internal-weight sign occurs.

The higher complex therefore is

    0 -> ker b --delta--> A/im b -> 0.

It has HK^hi_1=ker delta, HK^hi_0=coker delta, and no higher groups. There are no incoming higher boundaries from HK_2. Independently of general characteristic restrictions for other derivations, this two-term higher complex squares to zero automatically; moreover the cited definition explicitly covers the fundamental cocycle in every characteristic.

## Koszulness, independently of commutator homology

Use the left A-module complex

    0 -> A tensor V --mu--> A --epsilon--> k -> 0,
    mu(a tensor v)=av.

The basis of A tensor V maps bijectively onto nonempty words: cut a word before its unique last letter. Thus mu is injective and has image ker epsilon. It is left A-linear and its generators have internal weight one, while A has its free generator in weight zero. This is a linear free resolution, proving Koszulness over every field, including r=0. The map mu is different from b; substituting one for the other changes the problem.

## Orbit proof with no division

Fix total weight n>0. Concatenation identifies C_1 and C_0 separately with a vector space E_n whose basis is all length-n words. These are identifications of vector spaces in different homological degrees, not an identification of the boundary groups. Let rho move the final letter of a word to its beginning. Then b=I-rho. The actual left cap is rho and the candidate representative is I; rho=I on ker(I-rho).

Break the word basis into disjoint cyclic orbits. For an orbit O of cardinality d, label its distinct words w_0,...,w_(d-1) with rho(w_i)=w_(i+1), indices modulo d. Write e_i for the corresponding degree-one tensors. Then b(e_i)=w_i-w_(i+1). A linear combination sum c_i e_i lies in ker b exactly when c_i=c_(i-1) for each i. Thus the degree-one kernel is k*z_O, with z_O=sum e_i nonzero. This proof uses equality of neighboring coefficients; it never divides by d.

In degree zero the displayed differences identify all w_i. Their common quotient class t_O is nonzero: the coefficient-sum linear functional kills every difference and evaluates to one on each w_i. Hence the coinvariant block is one-dimensional in all characteristics, even if d=0 in k. The higher differential is

    delta(z_O)=d*t_O.

If char k=0, the scalar d is invertible. If char k=p>0, it is zero exactly when p divides d, and otherwise is invertible because k is a field. This proves one higher class in each of degrees one and zero for the p-divisible orbits, and no higher classes from other orbits. All statements pass from these finite blocks to their direct sum because elements have finite support. Over any field extension the matrices have prime-field entries and the same ranks; no algebraic-closure or finiteness-of-field assumption is present.

One subtle boundary distinction is essential: when p divides d, the underlying vector sum w_i in C_0 really is an ordinary boundary. Explicitly, b(sum i*e_i)=sum w_i-d*w_0. That is exactly why the cap vanishes in HK_0. It does **not** make z_O a boundary in C_1, since the incoming C_2 is zero. The checker verifies this explicit identity for every tested primitive witness.

## Uniform nonzero witness and edge cases

For every prime p let w=x^(p-1)y. Its p rotations are distinct because the unique y occupies p distinct positions. The associated z=sum e_i is nonzero, b(z)=0 by telescoping, and delta(z)=p*t_O=0. It cannot be an ordinary or higher boundary. It has homological degree one, coefficient weight p-1, and total weight p. Thus A=k<x,y> supplies the desired counterexample in every positive characteristic. In characteristic two the witness is x tensor y+y tensor x and every step remains valid; it uses no averaging or division by two.

The size d divides n but need not equal n. For x^p, d=1: the single degree-one tensor x^(p-1) tensor x caps to the nonzero class x^p in every characteristic. Listing all p rotations with repetition would instead produce the zero tensor and cannot establish nonvanishing. At n=6, (xy)^3 has d=2 and contributes precisely in characteristic two; (xxy)^2 has d=3 and contributes precisely in characteristic three. The full formula correctly retains this distinction.

For r=0, A=k, C_1=0, and the only class is weight-zero HK^hi_0=k. For r=1 every positive-weight orbit has size one, so all positive-weight higher groups vanish in every characteristic. At total weight zero for any r, C_1=0 and C_0=k, leaving k in degree zero. At total weight one all orbits have size one, so the coefficient-weight-zero degree-one classes are killed injectively by cap. All HK^hi_j with j>=2 vanish. The example's rank-two assumption is therefore material for the positive-characteristic nonvanishing claim, and the candidate uses it correctly.

## Independently checkable computation

`exact_chain_check.py` is newly written for this audit, uses only Python's standard library, and imports no supplied implementation. It performs exact Gaussian elimination over Q using Fraction, and over F_p using modular inverses. The matrix calculation builds b from the two explicit tensor multiplications, computes a basis Z of ker b, and evaluates the actual left cap L. It computes the rank induced into the quotient by

    rank(delta)=rank([b | L*Z])-rank(b).

It obtains the two higher dimensions from this rank. The comparison calculation independently forms minimal representatives of necklaces using left shifts and determines their least repeating block lengths. It does not read matrix ranks or kernel bases. The calculations agree in 234 cases spanning r=0,1,2,3,4; Q and characteristics 2,3,5,7,11; maximum word weight 12 (rank one), 7 (rank two), 4 (rank three), and 3 (rank four). Explicit primitive witnesses for 14 primes from 2 through 43 also pass both vanishing-in-characteristic-p and nonvanishing-in-Q/another-characteristic controls.

Ten falsification controls detect replacing orbit size by word length, ignoring repeated-word stabilizers, using a plus sign or multiplication-only map for b, setting cap to zero or changing to trivial coefficients, falsely treating repeated rotations as distinct, and treating all ordinary cycles as higher cycles. Detailed parameters, matrices' dimensions/ranks, witness fillers, and control outcomes are in `RESULTS.json`. The checker does not calculate an empirical substitute for the infinite proof.

Reproduce from this audit directory with `python3 exact_chain_check.py --output RESULTS.json`. The JSON contains its checker's SHA-256 and frozen head. The output timestamp changes on rerun; all dimensions/control outcomes should remain unchanged.

### Current acceptance interface and optimization replay

The original v1 checker used removable Python assertions. On 2026-10-15, those checks were replaced by an explicit `need` helper that raises `VerificationFailure` on a failed condition, with case-specific diagnostics. No assertion statements remain in the current checker. Every former acceptance condition remains active with `python -O`; three explicit coverage checks additionally enforce all 234 comparisons, 14 witnesses and 10 controls. No mathematical formula or tested parameter range changed.

`replay_verification.py` replays normal and optimized modes into `RESULTS_NORMAL.json` and `RESULTS_OPTIMIZED.json`. Both runs passed and each executed 2,110 explicit checks. All semantic results agree when only the timestamp and checker-digest fields are ignored. Every historical mathematical result and witness/control array also agrees with the byte-preserved v1 output. Current `RESULTS.json` is byte-identical to the verified normal replay.

For an operational rejection control, `--inject-wrong-expectation` deliberately changes the expected degree-one higher dimension at r=2, n=2, characteristic 2 from 1 to 2. Normal and optimized modes both exited with status 1, reported the exact matrix/necklace mismatch, and wrote no acceptance artifact. `REPLAY_RECEIPTS.json` records interpreter details, output digests, complete captured failure diagnostics, semantic comparison and preservation checks. Reproduce the full interface test with `python3 replay_verification.py`.

`historical_v1/` contains the exact pre-hardening checker, decision and results with their byte counts/digests and a README marking them historical. These preserved files are not the current acceptance interface. No previous reviewer implementation was introduced during hardening.

## Primary definition check and remaining gap

The independently retrieved primary reference is [Berger–Lambre–Solotar, *Koszul calculus*, arXiv:1512.00183v3 (20 June 2017)](https://arxiv.org/abs/1512.00183v3), specifically the coefficient differential in (2.3), fundamental cocycle in Definition 3.6, cap conventions in Definition 4.1, and higher homology in Section 5.2. This establishes the invariant and signs used here. `SOURCE_RECEIPTS.json` records the exact PDF digest and retrieval limits; raw PDF/text are ignored private material.

There is **no remaining mathematical gap in the audited counterexample or orbit formula**. The statement about the literal unrestricted-field question remains conditional on a separate source-scope determination: if the intended problem is restricted to characteristic zero, this result is not its solution. This audit makes no OWR historical-scope, novelty, priority, journal-version, human-review, or formal-proof claim. In characteristic zero the present computation proves vanishing only for these free algebras; it does not establish the general converse.
