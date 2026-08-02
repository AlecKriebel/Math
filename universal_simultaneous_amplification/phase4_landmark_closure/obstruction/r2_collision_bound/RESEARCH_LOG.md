# Research log: dB collision bound at fitness two

## 2026-08-02 09:43 PDT -- exact aggregate reduction

- Derived the complete dB harmonic at fitness two:

      phi_K(k) = [1-(n+k)/(n*2^k)]/[1-2^(1-n)].

- For an arbitrary graph committor, introduced the unweighted level marginal
  flux `D_k` and its heat-bath-weighted version `W_k`.  The opposing rates on
  every configuration edge sum to one, giving the exact aggregate recurrence

      W_k + W_(k-1) = D_(k-1).

- Used the exact Boolean coverage representation to rewrite both fluxes under
  the stationary geometric-union dual.  This avoids any false independence
  assumption about genealogies.
- Solved the complete killed Green kernel explicitly.  Pairing both endpoints
  of every Boolean-cube edge gives the exact comparison

      rho_dB(G,2)-rho_dB(K_n,2) = sum_k c_k (W_k-q_k^K D_k),

  with explicit positive rational `c_k`.
- Expanded `h(x)=2x/(1+x)` around the complete subset mass.  The comparison is
  exactly `L(G)-V(G)`, where `V` is a sum of nonnegative rational
  subset-dispersion atoms and `L` is one stationary weighted cut surplus.
- **EXACTLY FALSIFIED:** neither the per-level claim `R_k<=0` nor the linear
  cut claim `L<=0` is valid.  A regular weighted `K_4` has `R_2=1/205>0`; the
  weighted path `(1,2)` has `L=2/135>0`.  In both cases the full dispersion
  dominates and the complete comparison remains strict.
- Rewrote the cut surplus as the internal-pair deficit

      sum_({u,v} subset A) [2/(n-1)-w_uv(1/d_u+1/d_v)].

  Its average vanishes separately on every cardinality level under the
  complete dual reference law.  Hence `L` is exactly a covariance between
  the stationary likelihood ratio `Pi/Pi_K-1` and the internal-pair deficit.
  The full dispersion also controls the square of that same deficit
  pointwise after retaining only the all-holes subset atom.  Closing the
  theorem is now a sharp stationary likelihood-stability estimate; ordinary
  pointwise Cauchy leaves an uncontrolled chi-square factor.
- Solved the corresponding complete-dual Poisson equation abstractly to get
  the exact Dirichlet identity `L=E_Pi[(D_K-D_P)psi]`.  **EXACTLY
  FALSIFIED:** the tempting statewise domination of this forcing by the
  dispersion integrand fails already on the path `(1,2)`, at state `{0,1}`,
  with residual `-16/4455`.  Any proof must retain stationary averaging.
- Reduced the weaker universal density ceiling to the shortest exact
  cut-collision target.  If

      S1(A)=sum_cut (P_vu-1/(n-1))^2/(1+P_vu),

  then exact stationarity gives

      E[Z-S1] = n/(n-1)^2 * (E|A|^2-(n/2)E|A|).

  Thus `E Z<=E S1` is exactly the open stationary second-moment inequality.
  The comparison is false pointwise (slack `+16/135` on four states of the
  regular weighted `K_4`), so this does not collapse to elementary Cauchy.
- Derived the exact factorial hit/collision hierarchy

      E(B_j+B_(j-1)) = E[|A|*C(|A^c|,j-1)]

  and sharp row-local bounds on `B_j` in terms of `B_1`.  The open
  second-collision inequality `E B_2 >= (n/2-1)E|A|` would prove the universal
  density ceiling `rho_dB(G,2)<=1/2`, but the row-local bounds alone do not
  close it.
- **OPEN:** prove `L<=V`, or even the weaker stationary second-collision
  inequality.  Subtask completion estimate: **68%** for a finite-baseline
  reduction; the sign theorem remains unresolved.

## 2026-08-02 10:09 PDT -- stationary pair shortcut falsified

- Tested the proposed pair estimate

      Pr(v in A, i not in A)
      <= (1+P_vi) Pr(v in A) Pr(i not in A),

  which would imply the component-odds bound after multiplying by
  `h(P_vi)` and summing over `v`.
- **EXACTLY FALSIFIED on an unweighted graph:** on the path `0-1-2-3`, the
  endpoint pair `(v,i)=(0,3)` has `P_03=0`, marginals `p_0=p_3=2/7`, and
  crossing probability `16/77`; the proposed margin is `-2/539`.
- **EXACTLY FALSIFIED even on positive support:** on the regular weighted
  `K_4` with edges `02` and `13` of weight `18` and the other four edges of
  weight `1`, the weak edge `(0,1)` has `P_01=1/20`, all marginals equal
  `827/2026`, and proposed margin `-24507/82093520`.
- The stronger counterexample still has strictly positive component-odds
  slack `153822/1214587` at every vertex.  Hence only the pairwise route is
  closed; the summed component-odds and half-density targets remain open.
- Exact exhaustive screens over connected three-vertex weights in
  `{0,...,8}` and four-vertex weights in `{0,...,3}`, followed by extreme
  rational random screens through five vertices, found no violation of the
  summed component-odds inequality.  This is **NUMERICALLY/COMPUTATIONALLY
  OBSERVED**, not a proof.

## 2026-08-02 10:36 PDT -- independent integration audit

- Reconstructed the heat-bath complement identity, level-flux recurrence,
  complete killed Green weights, tangent remainder, conductance form of the
  cut surplus, all-holes quadratic bound, and factorial hierarchy directly
  from the two generators.
- Checked separately that the complete-reference likelihood term is centered
  on every rank and that the Poisson identity uses only stationary averaging;
  neither step supplies the still-missing sign.
- Confirmed the unweighted-path and positive regular-`K_4` pairwise
  counterexamples exactly.  The aggregate component-odds inequality remains
  positive in both examples and is not promoted from computational evidence.
- Made the standard-library verifier compatible with the repository's system
  interpreter and reran every exact check successfully.
- **OPEN:** `L<=V`, the component-odds inequality, the half-density ceiling,
  and the finite complete-graph maximizer theorem.
