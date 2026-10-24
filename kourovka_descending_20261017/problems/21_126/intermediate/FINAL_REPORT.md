# 21.126 intermediate branch — original research checkpoint

**No complete resolution obtained.** Discovery estimate: **7%** toward a complete 21.126 witness. This family has no finite presentation with a verified RAAG injection and both the required superpolynomial lower bound and subexponential upper bound. Publication gate remains closed.

## Strongest mathematical outcome

`POLYNOMIAL_ARTIN_KERNELS.md` derives a polynomial intrinsic Dehn upper bound for every finitely presented rank-one integral Artin kernel. With d zero-weight vertices, the proof gives the nonsharp exponent (9·3^d−1)/2. It combines weighted height pushing, an explicit cubic ambient-distortion rewrite, exact residue-indexed identity-HNN kernel decompositions, and a filling procedure that deletes stable pinches while retaining the original base words.

**That strongest general theorem passed a NEW independent adversarial review dispatched by the parent**, at unchanged proof hash `cd2b7e0036bdac22fec20fac2cde0b994d14fe7d369f6753c6de09340d6b61c4`. The review directly checked the original MMV graph criterion, rectangular homotopical disk pushing, cubic distortion, residue/Britton decomposition, and retained-word filling induction. It found no substantive outstanding objection. The parent independently inspected the induction as well. The audit and receipt are in `../artin_kernel_adversary/`. This accepts a scoped partial theorem only: originality has not been established, and the note is a class obstruction rather than a solution of 21.126. The fresh review is an AI audit, not independent human peer review.

Three precursor results have already passed independent adversarial review at exact hashes:

- Fixed nonzero integral weights, simply connected flag complex: kernel finitely presented, δ≼n^4 (`WEIGHTED_HEIGHT_QUARTIC.md`). Unequal fixed slopes cannot create an intermediate scale in this class.
- Identity-HNN area estimate and independent zero-weight directions: a precise class of kernels has δ≼n^9 (`INDEPENDENT_ZERO_DIRECTIONS.md`). The proof bounds associated subgroup distortion and does not mistake distortion for the subgroup Dehn function.
- One fixed nonnegative transition matrix / finite positive substitution has polynomial or exponential prefix growth (`POSITIVE_TRANSITION_DICHOTOMY.md`). The statement is conditional when used for group fillings and explicitly does not cover arbitrary finite recurrences.

## Distinct mechanisms attempted

1. Unequal live height weights: ruled out by a reconstructed rectangular-metric height-pushing argument. The primary unit-weight pushing source was read directly and the adaptation was audited.
2. Height-zero directions: first handled independent dead vertices, then derived a sequential construction with arbitrary dead edges satisfying the exact MMV finite-presentation graph conditions. The latter is the pending broad theorem.
3. Positive finite transitions and varying fixed polynomial degrees: exact directed-graph argument rules out a genuine intermediate scale for these constant transition models. An exhaustive adjacency census and independent formula checks agree.
4. Scale-dependent recursive filling: the finite rule T(2^k)=2^k T(2^(k−1)) really gives an intermediate numerical scale. However no group realizes the necessary lower/global upper/injection combination. A simple cyclic-clock implementation fails RAAG power-conjugacy and cyclic-undistortion constraints.
5. Higher-corank kernel extension: rank-one induction cannot simply be iterated. An explicit finitely presented kernel of F_m^3→Z^m for m≥4 has no section because the ambient abelian rank is three. This falsifies a proposed universal clique-splitting shortcut; it is not an intermediate example (three-free-factor polynomial bounds apply).

## Checkable evidence

The main positive-transition census checked all 66,066 binary adjacency matrices of dimensions one through four, including 65,536 dimension-four cases. The fresh reviewer separately verified exact cycle/chain counting formulas and the intermediate numerical recurrence.

Independent weighted checks cover 207,640 local link-ray cases and 64,800 edge compatibilities. Independent zero-direction checks cover 73,811 reduced words and 162 residue identities in an exact Z×F5 model. A second authored test handles a genuine dead edge: the ambient group Z(a)×(Z(b)*Z²(z,w)), weights (2,3,0,0), has kernel Z(B)*Z²(z0,w0)*Z²(z1,w1); 58,747 eligible ambient words and 73,811 kernel-generator words were reproduced bidirectionally in exact normal form.

These finite checks corroborate the explicit examples and local formulas. They do not prove the general asymptotic theorems, whose proofs are written separately, and do not provide a complete target witness. `REPRODUCTION.md` gives the standard-library commands.

## Exact unresolved obstruction

The reviewed derived result removes rank-one integral kernels from this family of candidate mechanisms. Arbitrary subgroups of those kernels remain outside that result: an ambient polynomial upper bound is not inherited by subgroups. Higher-corank kernels and nonnormal constructions need new mechanisms. The recursive numerical scale lacks a finite group presentation with unavoidable fillings, a subexponential global filling upper bound, and a verified RAAG injection.

The family outcome for the original problem is therefore **unsolved**. No preprint, Zenodo upload, publication tracker row, outreach, Git operation, or novelty claim was made. All three completed precursor reviews are AI adversarial checks, not human peer review.
