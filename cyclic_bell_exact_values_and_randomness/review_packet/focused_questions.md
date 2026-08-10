# Focused questions for specialist review

Please address the six bounded core questions below. They isolate the places
where a short expert check is most valuable; no reviewer is being asked to
“check the whole paper.” Two optional secondary-benchmark questions follow.

## 1. Source baseline and exact-value strengthening

Is the attribution boundary accurate?

In particular, does the originating paper receive explicit credit for the
two family definitions, canonical strategies and lower bounds, the general
first-family upper bound $d\sqrt2$, NPA evidence through $d=6$, the second-
family SOS, and the canonical full-behavior numerical framework? Do the
radical values and reported NPA decimals/levels agree, and is the isolated
Conjecture 2 normalization discrepancy described without rhetorical use?

## 2. Commuting-operator upper bound

Does the polar-decomposition proof establish

\[
\mathcal I_d\le2\csc(\pi/(2d))I
\]

without an implicit tensor-product or finite-dimensional assumption?

Please check the strong-limit construction of the support projection and
canonical polar partial isometry in Alice's bicommutant, the resulting
commutation with Bob, all kernel identities, and the left/right placement of
$A_0$ in the functional-calculus terms. Is the finite source strategy used
only for the matching lower bound, so that $q=qa=qc$ follows correctly?

## 3. Finite-dimensional support rigidity

Does Theorem `thm:support-rigidity` prove exactly its stated narrow result?

Please audit conversion of exact augmented saturation into separate residual
stabilizers; Schmidt-support cancellation for nonfaithful $\rho_A$; the bad-
phase/kernel cancellation; invariance and reduction of
$K=\operatorname{supp}\rho_A$; the adjacent half-angle reflection; and the
rank argument forcing every root multiplicity to equal $\dim K/d$. Does any
sentence silently extend the conclusion from every attained finite-
dimensional tensor-product exact maximizer of the first augmented family to
the unaugmented, second-family, approximate, or general commuting-operator
setting?

## 4. Permutation orbit, nonuniformity, and $d=4$ entropy

Does the conditional phase-permutation theorem characterize exactly the
**admissible maximizers claimed**, as a sufficient family rather than a full
classification?

Please check both product-one conditions, paired row permutations, weighted-
cycle order and spectrum, the target-projector DFT, the final-two-swap
autocorrelation, and the guessing bound for every $d\ge4$. At $d=4$, do
independent calculations give the $1/32,3/32$ table, $G=3/32$, and
$H_{\min}=5-\log_2 3$ only for the displayed trivial-Eve realization? Is that
entropy used only as an upper bound on value-only worst-case entropy?

## 5. Precise scalar-value randomness conclusion

Is the relationship to Conjecture 2 stated at the correct logical strength?

In the displayed-operator normalization, the intended disproved implication
is

\[
\langle\overline{\mathcal I}_d\rangle=M_d+1
\Longrightarrow G(AB\mid1,d,E)=1/d^2
\qquad(d\ge4).
\]

Does trivial Eve suffice for the counterexample? Does the paper clearly avoid
claiming that the final-two swap is worst-case, that the canonical strategy
lacks maximal randomness, or that an SDP fixing the complete canonical
behavior is invalid? Is behavior-level nonuniqueness proved only up to local
output relabelings, without an unsupported classification under every
strategy-level equivalence?

## 6. Second-family SOS and conventions

Does the second-family extension follow from the complete credited SOS of
Perito et al., Eqs. (22)--(23)?

Please verify its prefactor $1/(2d)$, coefficient conjugations,
phase in $\widehat B_\ell=d\lambda_\ell D_\ell$, the order-$d$ parity
calculation, and annihilation of **every** SOS factor. Is the transfer of the
first-family target table to $A_1,B_d$ exact? Is the alternative source-
appendix all-Bob-adjoint convention handled consistently as outcome inversion
$b\mapsto-b$, rather than mixed termwise with the main/SOS convention?

## Optional secondary checks

### A. Binary benchmark

Does the two-square identity prove $q=qa=qc=3\sqrt3$, and do its equality
relations force all nontrivial operator-valued Fourier coefficients at
$(0,0)$ to vanish for every attaining finite-dimensional tensor-product
strategy? Is the Wooltorton--Brown--Colbeck prior-art credit clear, and is the
privacy conclusion kept separate from arbitrary commuting maximizers?

### B. Private-MUB composition

Do the private reference condition, perfect Bob matching, and supported MUB
sandwich imply $\sigma_E^{a,\pi(b)}=\rho_E/d^2$ with the displayed
normalization? Is the lemma visibly sufficient only, with no necessity or
low-setting existence claim?
