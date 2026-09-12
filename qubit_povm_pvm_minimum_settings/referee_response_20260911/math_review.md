# Independent mathematical review of referee item R1

Checkpoint: 2026-09-11 21:15 PDT. Completion estimate: 100% of the bounded R1 counterexample, corrected-definition, time-orientation, and downstream-signature review. This is not an independent repeat of the full Lean build or a certification of every manuscript statement.

Scope: the referee report at `/Users/alec/.codex/attachments/9a7dba76-cd2f-40a6-a07b-6fd9a4725cb3/pasted-text.txt`, the current `paper/main.tex`, and the relevant production Lean definitions and proof dependencies. The report was treated as a claim to test, not as instructions. Production files were read only. No external communication was initiated.

## Finding

R1 is correct. The listed scalar inequalities do not imply signature `(1,3)`, even when the five coefficient rays are null, all ten distinct-ray products are positive, and the normalization vector has square one. The corrected definition currently in `paper/main.tex`, which retains signature `(1,3)` as a separate hypothesis and limits the common-cone equivalence to that hypothesis, fixes this error. The inspected physical Lean closure does not infer signature from `StrictParameters`.

## Exact rational counterexample

Use one-based ray labels here, matching the manuscript:

\[
r_1=(1,0,0,0),\quad r_2=(0,1,0,0),\quad
r_3=(0,0,1,0),\quad r_4=(0,0,0,1),\quad
r_5=(1,1,-1,-1),\qquad u=r_1+r_2.
\]

Set

\[
a=d=6/25,\quad b=c=3/100,\quad e=a+b+c+d-1/2=1/25,
\qquad
g=\begin{pmatrix}
0&1/2&6/25&3/100\\
1/2&0&3/100&6/25\\
6/25&3/100&0&1/25\\
3/100&6/25&1/25&0
\end{pmatrix}.
\]

All four pair sums in the strict scalar inequalities equal `27/100 < 1/2`, and all five scalar entries are positive. All five ray squares vanish. The distinct pairings are:

| Pair | Product |
|---|---:|
| 1,2 | 1/2 |
| 1,3 and 2,4 | 6/25 |
| 1,4 and 2,3 | 3/100 |
| 3,4 | 1/25 |
| 1,5; 2,5; 3,5; 4,5 | 23/100 |

For `v=(2,-2,5,-5)`, direct multiplication gives

\[
u^Tgu=1,\qquad u^Tgv=0,\qquad v^Tgv=12/5.
\]

Thus `span(u,v)` is positive definite, already contradicting positive index one. To determine the full signature without numerical eigenvalues, take the following four basis vectors:

\[
w_1=(1,1,0,0),\quad
w_2=(-27/50,-27/50,1,1),\quad
w_3=(1,-1,0,0),\quad
w_4=(21/50,-21/50,1,-1).
\]

If `W` has these columns, exact rational multiplication yields

\[
W^TgW=\operatorname{diag}(1,-529/2500,-1,241/2500).
\]

The right side is nonsingular, so `W` is invertible; this is an exact congruence certificate of signature `(2,2)`. All displayed identities, nullness tests, strict pairings, and diagonalization were independently evaluated with Python's `fractions.Fraction`, without floating-point comparisons.

Even adding the five inequalities `u^T g r_i>0` does not repair the scalar-only criterion: in this counterexample those values are respectively

\[
1/2,\ 1/2,\ 27/100,\ 27/100,\ 23/50.
\]

## Corrected definition and the orientation of u

For a real symmetric nondegenerate form with signature `(1,3)` and `u^Tgu=1`, the unambiguous orientation is the future causal cone whose nonzero elements satisfy `g(u,x)>0`. The vector `u` is in its timelike interior. For any nonzero null vector `x`, write `x=t u+z` with `z` orthogonal to `u`. Then `t=g(u,x)`, and `-g` is positive definite on `u`'s orthogonal complement; nullness implies `||z||=|t|`, so `t` is nonzero. For two nonproportional null vectors in the same orientation, Cauchy–Schwarz gives strictly positive `g(x,y)`. Opposite orientations instead give a strictly negative product; zero is possible only for proportional null vectors.

The five fixed coefficient rays are nonzero and pairwise projectively distinct. In this normal form, pairwise positive products imply that all of them have the same orientation. They also select the orientation of `u` itself: `u=r_1+r_2` and `g(r_1,r_2)=1/2`, so their sum is timelike in their common future cone. There is no additional unresolved choice of whether `u` is past-directed.

Equivalently, the products with `u` can be checked directly:

\[
g(u,r_1)=g(u,r_2)=1/2,\quad
g(u,r_3)=a+c,\quad g(u,r_4)=b+d,\quad
g(u,r_5)=1-a-b-c-d.
\]

The scalar inequalities make all five positive. The ten distinct-ray products consist precisely of `1/2`, `a,b,c,d,e`, and

\[
1/2-a-b,\quad1/2-c-d,\quad1/2-b-d,\quad1/2-a-c.
\]

Consequently the corrected equivalence is valid with the independent signature hypothesis retained. Describing the future cone as the **causal** cone oriented by `g(u,x)>0` makes explicit that it contains the timelike vector `u` as well as the null rays; the phrase must not mean that `u` itself is null.

## Downstream signature and orientation audit

No inspected downstream argument silently derives Lorentz signature from the scalar inequalities. The following distinctions matter.

| Location | Hypotheses actually used and assessment |
|---|---|
| `paper/main.tex`, residual Gram construction | The effects are a basis and `g=E_A^T J E_A`; invertibility gives signature `(1,3)` by congruence. |
| Local physical completeness and smooth-incidence proposition | The current manuscript explicitly retains Lorentz signature and time orientation. Negative definiteness of `u`'s orthogonal complement follows from that signature and `u^Tgu=1`. It would fail on the counterexample. |
| Exact second-variation inertia argument | `S=P^T g^{-1}P` has signature `(1,3)` because `P` is invertible and the residual metric has that signature. Thus the displayed inertia `(4,12)` remains justified on the corrected residual domain; it is not valid for arbitrary scalar parameters. |
| `Bell/Lorentz.lean`, `StrictParameters` | This structure records only the scalar inequalities. Its module comment explicitly disclaims an inference to signature. It should continue to be described as a scalar parameter structure, not as the whole physical residual domain. |
| `ProjectiveFiber.lean` and `RankOne.lean` | These are algebraic null-quadric and stationarity statements with their explicit scalar hypotheses. Their stronger applicability beyond Lorentz signature is not a missing physical premise. |
| `RankZero.lean` and `RankZeroSimulation.lean` | Ray coefficients become positive using the explicit positive `timeFunctional` hypotheses. In the physical chain these are derived from actual future orientation. The metric-table transportation construction itself legitimately needs only scalar inequalities. The counterexample does not refute this classical simulation statement. |
| `IncidenceRank.lean`, high-rank exclusion | The Lean argument constructs an uphill rank-one direction using a positive vector and positive weights. It does not assert the manuscript's full inertia theorem from scalar inequalities. Its weaker algebraic hypotheses are therefore legitimate. Physical applicability is supplied separately. |
| `ResidualCoordinates.lean`, `ResidualFrames` | The structure contains an invertible Alice frame, positive future-null frame rays, and `alice * u = timeUnit`. Its metric is defined as `frameGram alice`. `parameters` derives scalar inequalities from these physical data, while `parameters_gram` retains the connection to the actual Gram form. |
| `ResidualClosure.lean`, `no_strict_residual_maximum` | The theorem explicitly requires invertible `E`, `frameGram E = metric ...`, `E*u=timeUnit`, feasible incidences, and `FramePositive E Y`. The final physical call passes all these premises. A scalar `(2,2)` counterexample cannot satisfy the invertible Gram premise. |
| `GramLift.lean`, local completeness | The local Gram lift starts from an actual invertible frame and remains continuous at that frame; it does not select a Lorentz frame from an arbitrary scalar parameter tuple. Neighborhood feasibility is converted to a physical strategy through an actual nearby Gram lift and open frame positivity. Invertibility and signature can also be retained by shrinking the neighborhood, although the target raw-POVM realization theorem needs only the proved frame properties. |

In particular, `ResidualClosure.frame_timeFunctional_positive` rewrites

\[
\operatorname{timeFunctional}_g(Yr_j)
=g(u,Yr_j)=J(Eu,EYr_j)=(EYr_j)_0>0.
\]

The premise `E*u=timeUnit` fixes the time orientation precisely where rank-zero rigidity needs it. `frame_future_pairing` separately obtains future timelikeness of the transformed normalization vector from positive ray time components and its positive square. Neither step treats a positive scalar norm alone as a future-orientation certificate.

## Remaining scope boundary

The scalar criterion should not be presented as a stand-alone characterization of Lorentz metrics, and auxiliary claims about exact inertia must stay on the physical/signature-restricted domain. The corrected current manuscript meets that requirement at the inspected uses. This review establishes that R1 needs a definition correction but does not identify a failure of the main physical Lean closure. Questions R2 and R3 about exhaustive manuscript coverage, build receipts, and the foundational trust boundary require their own artifact audit and are not certified by this bounded review.
