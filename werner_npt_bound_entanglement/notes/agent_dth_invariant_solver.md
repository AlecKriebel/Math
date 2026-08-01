# Matrix-free invariant solver for the corrected first DTH cone

## Status

This note records an exact finite reduction and a numerical discovery
calculation.  The exact reduction makes the complete corrected first-degree
DTH cone computationally accessible on the local machine.  The numerical
calculation currently points toward optimum zero, but it is **not** an exact
certificate and does not prove DTH.

No negative pseudomoment was found.  In particular, the negative iterates
reported below violate holomorphic--mixed consistency by a small but nonzero
amount and must not be quoted as counterexamples.

The discovery programs are

- `discovery/agent_dth_invariant_crossing.py`;
- `discovery/agent_dth_dual_sdp.py`;
- `discovery/agent_dth_affine_dual_sdp.py`;
- `discovery/agent_dth_primal_admm.py`.

The independent exact local crossing construction is
`verification/agent_dth_local_crossing_exact.py`.

## 1. Lossless invariant reduction

Local $U(3)^3$ twirling preserves both positive cones, every lifted range
constraint, trace, and the witness.  Hence it is lossless for the corrected
first-degree decision.

At one physical site the holomorphic covariant module has Schur multiplicity
sizes

\[
 (1,4,5,6,5)
\]

for partitions

\[
 [5],[4,1],[3,2],[3,1,1],[2,2,1].
\]

Thus its commutant dimension is

\[
 1^2+4^2+5^2+6^2+5^2=103.
\]

The mixed module 

\[
 \bar{\mathbf3}^{\otimes2}\otimes\mathbf3^{\otimes3}
\]

has multiplicity sizes

\[
 (1,6,6,2,5,1)
\]

for local types

\[
 (3,2),(2,1),(1,0),(1,3),(0,2),(4,0),
\]

and again

\[
 1^2+6^2+6^2+2^2+5^2+1^2=103.
\]

Partial transpose is a Hilbert--Schmidt isometry between these two local
commutants.  If $d_\lambda$ and $e_\mu$ are the corresponding carrier
dimensions and $T_{\mu\leftarrow\lambda}$ is the crossing in highest-weight
matrix coordinates, the normalized local crossing is

\[
 U_{(\mu,a,b),(\lambda,p,q)}
 =\sqrt{e_\mu d_\lambda}\,
   T_{\mu\leftarrow\lambda}[a,b,p,q].
\tag{1}
\]

It obeys

\[
 U^{\mathsf T}U=I_{103}.
\tag{2}
\]

The exact diagram-basis verifier proves the crossing without floating point.
The discovery implementation independently obtains

\[
 \|U^{\mathsf T}U-I\|_2=1.54\times10^{-14}.
\]

For three physical sites the full crossing is simply

\[
 \boxed{U^{\otimes3}.}
\tag{3}

It acts on only $103^3=1,092,727$ real coefficients and is applied by
three mode products; the dense tensor-cube matrix is never formed.

## 2. Exact block cone

On the holomorphic side there are $5^3=125$ ordered local-type blocks.
After pair symmetry, the first Pluecker equation, and Omega, their supported
multiplicity dimensions sum to

\[
 \boxed{768.}
\tag{4}

Each individual supported block has size at most $16$.

On the mixed side there are $6^3=216$ ordered blocks.  Before support their
dimensions sum to

\[
 (1+6+6+2+5+1)^3=9261.
\]

The support contraction has total target dimension

\[
 (1+2+1)^3=64
\]

and full row rank.  Therefore the sum of the mixed support-kernel dimensions
is exactly

\[
 \boxed{9261-64=9197.}
\tag{5}

Let $\widehat X_\lambda$ denote the Hilbert--Schmidt normalized holomorphic
block and $\widehat Z_\mu$ the normalized mixed block.  The corrected invariant
primal is exactly

\[
\begin{aligned}
 \text{minimize }&\sum_\lambda
 \sqrt{d_\lambda}\,
 \operatorname{Tr}(O_\lambda\widehat X_\lambda),\\
 \text{subject to }&
 \widehat X_\lambda\succeq0,
 \quad\operatorname{ran}\widehat X_\lambda\subseteq K_\lambda,\\
 &\sum_\lambda\sqrt{d_\lambda}
     \operatorname{Tr}\widehat X_\lambda=1,\\
 &\widehat Z=U^{\otimes3}\widehat X,\\
 &\widehat Z_\mu\succeq0,
 \quad\operatorname{ran}\widehat Z_\mu\subseteq L_\mu.
\end{aligned}
\tag{6}
\]

Thus the apparent (3,326,427)-dimensional ambient problem reduces exactly
to projections onto 125 holomorphic and 216 mixed matrices, the largest of
which is (216\times216).

## 3. Matrix-free ADMM

The solver splits (6) between the holomorphic and mixed cones.  Because
(U^{\otimes3}) is orthogonal, the holomorphic update is projection of

\[
 (U^{\otimes3})^{\mathsf T}(Z-u)-O/\rho
\]

onto the positive holomorphic range cone with trace one.  This projection is
computed exactly at discovery precision by a single global eigenvalue
threshold.  The mixed update independently compresses each block to
(L_\mu), takes its positive part, and reconstructs it.  One iteration uses
about 25 MB of state and took about (0.2) seconds on the local machine.

Every displayed iterate is positive in each split cone to eigensolver
precision.  Its only substantive defect is the reported crossing residual

\[
 \|U^{\otimes3}\widehat X-\widehat Z\|_2.
\]

## 4. Discovery results

Two restricted dual searches were first audited.

1. The ansatz (Y=C_{\rm supp}^\dagger T C_{\rm supp}), with all 216
   invariant target coefficients before site averaging, has best numerical
   common margin about
   
   \[
   -0.57485.
   \]

2. The general affine zero-on-(L) ansatz

   \[
   Y=C_{\rm supp}^\dagger R+R^\dagger C_{\rm supp}
   \]

   was searched with the complete site-symmetric
   
   \[
   \operatorname{Sym}^3(\mathbb R^{23})
   \]

   parameterization, of dimension (2300).  Its best numerical common
   margin is about
   
   \[
   -0.42245.
   \]

These are failures of restricted certificate families only.  A general dual
operator may be positive and nonzero on (L).

The full primal ADMM was then run with increasing penalty.  Representative
iterates were

\[
\begin{array}{c|c|c|c}
 \rho & \text{iteration} & \text{objective} &
 \text{crossing residual}\\ \hline
 100 &1000&-0.38349&1.11\times10^{-3}\\
 1000&1200&-0.02420&7.01\times10^{-5}\\
 1000&2000&-0.01809&4.79\times10^{-5}\\
 1000&3200&-0.01257&2.75\times10^{-5}
\end{array}
\tag{7}
\]

The scaled ADMM normal provides at every iterate a mixed-dual operator which
is positive on (L).  At the last row its minimum compressed eigenvalue was

\[
 -3.6\times10^{-14},
\]

and the corresponding numerical dual lower margin was

\[
 -0.00784.
\tag{8}

Since physical equality points give the exact upper bound zero, the current
floating-point discovery bracket is approximately

\[
 \boxed{-0.00784\ \lesssim\ \mu_1\ \le 0.}
\tag{9}

This is not a rigorous interval certificate.  It records the behavior of two
independent sides of the numerical cone calculation.  Both bounds move
toward zero as the residual falls.  The active primal is broad: 118 of the
125 ordered holomorphic blocks carry visible mass, generally at ranks larger
than one.  This behavior does not support a small negative pseudomoment
reconstruction; it instead points toward optimum zero on a highly singular
common face.

## 5. Remaining exact task

The calculation has not decided the first lift.  The next proof-first task is
to extract the limiting mixed-dual normal in the exact 103-diagram basis and
identify an exact exposing identity

\[
 Y\in C_{\rm mixed}^*,
 \qquad
 O-(U^{\otimes3})^{\mathsf T}Y\in C_{\rm hol}^*.
\tag{10}

If the dual limit is not attained, one must first reconstruct the common
facial-reduction ray, restrict both block cones to its exact kernels, and
rerun (6).  Only an exact positive certificate on the final face proves DTH.
Conversely, only an exactly consistent negative density proves failure of
the first lift.  Neither has yet been obtained.
