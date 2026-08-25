# Adversarial audit of the K3P sharpness package

## Verdict

**Mathematical sharpness claim: PASS.**  The independent adversarial replay found no proof gap in the three-leaf strict-continuous-time common germ, the two rank-15 submersions, the weak-not-strong topology classification, or the all-(n) (6n-3) extension.

**Provenance: PASS with one documentary gap.**  The cloud certifier refers to `sharpness_relative_root.json`, but that file is absent.  Consequently the numerical discovery trajectory and pre-truncation approximate root cannot be replayed end to end.  This does not prevent exact verification of the final theorem witness: the supplied final JSON contains all graph-independent rational slice data needed to rebuild the polynomial system, derive a fresh exact inverse, and prove the box certificate.

No parent `PASS` Boolean was used as evidence.  The machine-readable record is `SHARPNESS_ADVERSARIAL_AUDIT.json`.

## Independent analytic replay

The audit rebuilt the two 16-coordinate three-leaf K3P Fourier maps from the primitive arcs, all four reticulation switchings, descendant reachability, and character XOR.  It then substituted the 15 scaled pivot variables and expanded all 15 nonconstant equality equations over the rationals.

- The equation term counts are `[5, 5, 4, 4, 3, 3, 7, 5, 4, 2, 5, 3, 7, 4, 3]`.
- Every equation is multiaffine in the slice variables.
- The graph-derived expansion agrees coefficient-for-coefficient with the embedded parent expansion.
- The independently rebuilt map-term hashes are `85667791ca63c772123907734ff8b1c8132865a7edd0191d9106716a82583840` for (W) and `844ffb6cc7ca75a31d36123534f97734ddea15cce34875642de102855cdefc88` for (W').
- The exact point Jacobian determinant is nonzero, approximately (-3.056932495160	imes10^{-2}).
- The largest exact center residual is approximately (3.028381609949	imes10^{-89}).

The interval replay uses exact rational **center-radius** arithmetic, not the endpoint implementation in the parent verifier.  For multiplication it encloses

\[
(m\pm r)(n\pm s)\subset mn\pm\bigl(|m|s+|n|r+rs\bigr),
\]

so there is no floating-point rounding mode or endpoint-orientation assumption.

For the certified radius (ho=10^{-50}), it independently obtains

\[
\|I-J_F(y_0)^{-1}J_F(X)\|_\infty
\le 8.077023076476\times10^{-47}<1,
\]

and the maximum operator distance from the box center, divided by (ho), is

\[
9.740999384091\times10^{-41}<1.
\]

All 15 Krawczyk balls lie strictly inside (X).  The minimum absolute inclusion slack is approximately (10^{-50}); equivalently, the operator occupies only about (9.74	imes10^{-41}) of the available normalized radius.

The uniqueness argument has all required hypotheses: (X) is convex, (F) is polynomial and hence (C^1), the preconditioner is the exact inverse of a nonsingular point Jacobian, the interval Jacobian contains every segment mean Jacobian, and the preconditioned error norm is below one.  Therefore every such mean Jacobian is invertible by the Neumann lemma, excluding two distinct zeros in the slice.

## Rounding, orientation, and self-map attacks

The audit exercised the following failure modes.

- In binary64, all 15 intervals (y_{0,j}\pm10^{-50}) collapse to a single floating-point number.  A double-precision replay cannot certify this box.
- A four-corner mixed-sign product fixture gives ([-2,-1][-3,4]=[-8,6]).  The unsafe two-corner rule produces reversed endpoints; the center-radius implementation encloses the correct interval and rejects reversed input.
- Transposing the actual preconditioner makes the strict self-map fail and raises the norm bound to approximately (2.729838084890	imes10^3).
- Reducing the radius to (10^{-92}) makes the normalized operator radius approximately (97.40999285618), so inclusion fails.
- Enlarging the radius to (1/10) makes the norm bound approximately (8.872323263192	imes10^2), and inclusion fails.
- A scalar fixture shows a subtle point: changing (y_0-YF(y_0)) to (y_0+YF(y_0)) can still map a symmetric box into itself, but its operator point has residual (-1/2) rather than zero.  Thus the fixed-point-to-zero algebraic identity, not self-inclusion alone, fixes the Krawczyk sign.

These tests kill the proposed mutations rather than merely comparing stored summaries.

## Equality slicing, rank persistence, and physical margins

The audit verified 64 direct parameters, 15 distinct in-range pivots, 49 frozen parameters, 15 nonzero row scales, the exact edge orders, and the complete nonconstant zero-sum output order.  Duplicating a pivot is rejected, dropping an equation leaves rank at most 14, replacing a nonconstant row by (q_{000}) leaves rank at most 14, and altering one polynomial coefficient breaks the graph-derived symbolic equality.

Fresh lexicographic exact minors give:

| map | columns | point determinant | uniform Neumann bound |
|---|---|---:|---:|
| (W) | `[0,1,2,6,7,8,9,10,11,12,13,14,15,16,18]` | nonzero, about (1.3077310392\times10^{-336}) | (1.543152096600\times10^{-45}) |
| (W') | `[0,1,2,6,7,8,9,10,11,12,13,14,15,16,17]` | nonzero, about (-6.7413241575\times10^{-325}) | (4.582719524575\times10^{-45}) |

The bounds hold throughout the full equality box, not only at its center.  Duplicating one selected column makes the test determinant exactly zero.

For every rooted arc spectrum, the audit checks (0<C,G,T<1), all four inverse-Fourier transition probabilities, all three strict-CT inequalities, and both sides of every inheritance interval.  It additionally multiplies the two artificial-root arc spectra and checks the effective root-suppressed semi-directed edge directly.

- The smallest (W) margin is (C-GT\approx4.964484595360\times10^{-10}) on edge 8.
- The smallest (W') margin is (C-GT\approx1.395195552339\times10^{-9}) on edge 8.

A mutation with spectrum ((C,G,T)=(1/20,4/5,1/10)) remains in the principal stochastic domain but violates (C>GT).  The CT gate rejects it.  A zero eigenvalue is likewise rejected.

At the certified equality root, both maps are therefore strict-CT submersions into the 15-dimensional normalized Fourier space.  Each image contains an ambient-open neighborhood of the common tensor, and their intersection is a common regular 15-germ.

## Rooting census and topology definitions

The audit reconstructed `sd_0` explicitly for every candidate rooting.  It orients only ordinary edges, retains every reticulation arrowhead, checks rooted binary degrees, acyclicity, reachability, exact dominators, the LSA condition, and tree-childness, and finally suppresses the root again and demands literal equality with the fixed mixed graph.

The resulting censuses are

\[
W:(5,2,3),\qquad W':(7,2,5),\qquad
\text{collision}:(7,0,7),
\]

where each triple is (admissible, tree-child, non-tree-child).  Each admissible root edge has exactly one valid orientation.

Both sharpness graphs are simple, binary, and level 2.  The no-omnian criterion independently finds the expected failures: (U) tails the two problematic retained edges in (W), and (V) tails the two in (W').  Together with the explicit tree-child and non-tree-child rooting witnesses, this proves membership in (W_{\mathrm{TC}}\setminus S_{\mathrm{TC}}).

Two definition mutations were tested on purpose.

- A synthetic binary acyclic rooted network has common stable vertices `v` and `t`.  It is accepted if the LSA condition is removed and rejected when LSA validity is required.
- Erasing all retained heads from the (W) mixed graph preserves its underlying graph, but the original rooted presentation no longer suppresses to that mutated fixed graph.  Explicit `sd_0` equality rejects it.

## Nonisomorphism and triangle equivalence

There is a short independent labelled invariant:

\[
\begin{array}{c|ccc}
&d(0,1)&d(0,2)&d(1,2)\\\hline
W&4&4&3\\
W'&3&4&4.
\end{array}
\]

Hence the labelled underlying graphs are not isomorphic.  Ordinary triangle redirection changes retained heads but not the labelled underlying graph, so the pair is not ordinary-triangle-equivalent.

This invariant also strengthens the all-(n) proof.  Every prescribed graft is above leaf 2, so (d(0,1)) remains 4 on the (W_n) side and 3 on the (W'_n) side for every (n).  No iterative-isomorphism assumption is needed.

## Cherry inverse, dimension, and class persistence

For

\[
R_h=u_h/v_h,\qquad P_h=u_hv_h,
\]

the independently formed rational (6\times6) Jacobian has determinant

\[
\frac{8u_Cu_Gu_T}{v_Cv_Gv_T}.
\]

At the supplied spectra it is exactly (176/25).  Exact substitution into a generic positive three-leaf Fourier tensor then recovers all six edge eigenvalues via

\[
u_h=\sqrt{R_hP_h},\qquad v_h=\sqrt{P_h/R_h},
\]

and recovers every old tensor coordinate by division by the corresponding nonzero pendant factor.  The positive branch is essential and is guaranteed here by the strict-CT domain.  The example spectra pass every stochastic and CT inequality, with minima (83/630) and (367/2772).

The dimension conclusion has both sides:

- Upper bound: the entire grafted-network tensor factors through `(old tensor, u, v)`, so a cherry adds at most six image dimensions.
- Lower bound: the nonzero six-observable determinant and old-tensor recovery give a local analytic inverse, so it adds at least six.

Thus each graft increases the full intrinsic model dimension by exactly six, and the common regular germ has dimension

\[
15+6(n-3)=6n-3.
\]

Duplicating a product observable drops the cherry Jacobian rank to 5; tying the two pendant spectra drops it to 3.  These mutations confirm that the six-dimensional gain comes from the proved inverse, not a raw parameter count.

The audit lifts an explicit tree-child and an explicit non-tree-child rooting through every stage (4\le n\le12), suppresses each lifted rooting back to its fixed mixed graph, contracts the newest cherry to recover the preceding graph, verifies all new edges are bridges, and rechecks binary standardness, unchanged triangles, and level 2.  The uniform local argument then covers every (n): pendant replacement preserves the tree-child witness, leaves the old non-tree-child witness untouched, and cannot change a blob.

## Residual gaps and strongest verified claim

There is **no remaining mathematical gap within the assigned sharpness scope**.

The one residual issue is documentary: `sharpness_relative_root.json` is missing, so the discovery computation that produced the final rational witness cannot be reconstructed from its original approximate input.  The theorem certificate itself remains replayable because it needs only the final rational witness, not its discovery history.

Strongest verified claim: for every (n\ge3), the prescribed pair of binary standard semi-directed level-2 networks is weakly but not strongly tree-child, is neither labelled-isomorphic nor ordinary-triangle-equivalent, and its two strict-CT K3P images share a common full-dimensional regular analytic germ of dimension (6n-3).

## Replay

From the project root:

```bash
python3 sharpness/adversarial/adversarial_audit.py
```

The replay uses the Python standard library only and takes about 12 seconds on the supplied M1 machine.  The audit completion estimate is **100%** for mathematical verification and **documentary-gap noted** for discovery provenance.
