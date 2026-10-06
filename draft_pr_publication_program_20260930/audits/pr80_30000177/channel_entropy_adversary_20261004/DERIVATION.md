# Independent channel derivation

This derives the original candidate's finite instrument and its asymptotic coding bridge. It was checked independently before author-code exposure. All units are bits per copy of W4, meaning per pair of transmitted qubits.

## Complete instrument and physical tensor order

The original physical tensor order is A1,A2,B1,B2. After A1 arrives at B1 and A2 at B2, rearranging to L=(A1,B1), R=(A2,B2) gives the coefficient table

    W = (|psi+>_L |00>_R + |00>_L |psi+>_R)/sqrt(2).

This equality is a tensor permutation, not a physical receiver operation. Each sender applies U in {I,X,Z,XZ} on its own transmitted qubit. With X=[[0,1],[1,0]] and Z=diag(1,-1), XZ=[[0,-1],[1,0]]. It is real orthogonal, with (XZ)^T=-XZ and (XZ)^T(XZ)=I. The usual Y=iXZ differs by a global scalar phase, which cancels from every density matrix. Replacing U^dagger with U for XZ would be erroneous; the independent computation uses the transpose explicitly.

B1 measures the complete Bell basis (phi+,phi-,psi+,psi-), where the first two vectors are (00 +/- 11)/sqrt(2), the second two (01 +/- 10)/sqrt(2). The instrument, including discarded L and outcome delivery to B2, has Kraus maps

    K_j = |j>_J tensor <Bell_j|_L tensor I_R.

Their effects sum to I_LR, because the Bell vectors are orthonormal and complete. Therefore the sum over all branches is trace preserving; this is not a successful-branch filter. The four-valued outcome travels only from one receiver to the other, after the two allowed quantum transmissions.

For zero input letters the unnormalized R vectors are (psi+/2, psi+/2, 00/sqrt(2), 0). Their densities are respectively (1/4)|psi+><psi+|, the same, (1/2)|00><00|, and zero. A positive branch has its conditional normalized pure state; the zero branch has zero weight and does not require defining a conditional normalized state. No operation divides its state by its probability.

The x input permutes Bell outcome blocks with the following signed preimages. The entries give the Bell vector arising under U_x^T from each row label; signs disappear only upon taking the outer product.

| x | phi+ | phi- | psi+ | psi- |
|---|---|---|---|---|
| I | phi+ | phi- | psi+ | psi- |
| X | psi+ | -psi- | phi+ | -phi- |
| Z | phi- | phi+ | psi- | psi+ |
| XZ | psi- | -psi+ | phi- | -phi+ |

The y input conjugates each density by U_y tensor I on R. These operations give all 64 outcome blocks from the four displayed baseline vectors. independent_channel.py also calculates each block afresh from the original physical order and independently from the explicit permutation; the output retains all integer amplitude vectors. In that representation v=k/(2sqrt(2)), so each density is k k^T/8 and each branch probability is sum(k_i^2)/8 exactly.

## Spectra and conditional information

The cq output is the direct sum over four J labels of the R blocks. Thus its ambient dimension is 4 times 4 = 16. Its spectrum is the union of the spectra of the unnormalized blocks, including zero eigenvalues. Every fixed-input output therefore has spectrum (1/2,1/4,1/4,0,...,0), rank 3 and entropy 3/2. It is not the spectrum of a normalized branch.

Independently uniform x,y induce the Pauli average on the first R qubit:

    T(tau) = (I_2/2) tensor tr_A2(tau).

This holds for every two-qubit operator, including complex operators: the independent checker proves it on all 16 real matrix units and extends by complex linearity. Averaging over y with x fixed turns the weight-1/2 product block into (I_2 tensor |0><0|)/4, and each weight-1/4 Bell block into I_4/16. The former contributes two eigenvalues 1/4; the latter together contribute eight eigenvalues 1/16; six eigenvalues are zero. Entropy is 3, rank 10, trace 1.

Averaging over x with y fixed makes each outcome block equal to

    (1/8)(U_y tensor I)(|00><00|+|psi+><psi+|)(U_y^T tensor I).

The two vectors are orthogonal. Four blocks consequently give eight eigenvalues 1/8 and eight zeros; entropy is 3, rank 8, trace 1.

After both averages each block is diag(3,1,3,1)/32, trace 1/4. The cq grand mean has eight eigenvalues 3/32 and eight eigenvalues 1/32, rank 16 and entropy

    5 - (3/4)log2(3) = 3 + h(1/4).

The checker certifies the full characteristic polynomial of every relevant matrix, computing trace powers and Newton identities in exact rational arithmetic. This fixes multiplicities as well as eigenvalues. Nonnegative spectra, symmetry, trace, zero blocks and ambient dimension are explicit checks. Entropies are calculated formally as rational pairs (a,b), meaning a+b log2(3), rather than by rounded diagonalization.

Writing Q=JR, the classical product prior gives

    I(X:Q|Y) = average_y S(omega_y) - average_xy S(omega_xy) = 3/2,
    I(Y:Q|X) = average_x S(omega_x) - average_xy S(omega_xy) = 3/2,
    I(XY:Q) = S(average) - average_xy S(omega_xy)
            = 7/2 - (3/4)log2(3) = 3/2+h(1/4).

The exact inequality 3^3=27<32=2^5 gives h(1/4)>3/4. Hence (r1,r2)=(9/8,9/8) satisfies both individual constraints strictly and has total 9/4 strictly less than the sum constraint. It also exceeds the benchmark 2 strictly. No floating-point comparison is necessary to establish advantage.

## Tensor extension and established asymptotic theorem

For n independent resources, local tensor-product encodings and copywise Bell measurements give conditional vectors that factor over copies. The measurement contractions distribute over tensor products, so the cq output is exactly the product of one-copy cq outputs, up to the harmless ordering of classical labels. Direct two-copy contractions for all 256 input combinations and 16 outcome pairs (4096 checks) validate this implementation. The symbolic distributivity argument, rather than finite testing, establishes the arbitrary n identity.

Winter quant-ph/9807019v3, Sec.II and Theorem 9, pp.4-5, applies to this finite memoryless cq MAC with independent classical encoders. The three stated information constraints therefore imply asymptotic existence of separate codebooks and a block output POVM with vanishing average error. No claim that a Holevo bound is one-copy accessible information is used. Rates approaching the sum face with both coordinates below 3/2 give the claimed supremum lower bound 3/2+h(1/4).

All of Q^n is at B2. Since each channel output is diagonal in J^n, pinching any decoding POVM by the J^n projectors changes no probability. The pinched measurement has conditional POVMs on R^n, with positivity and completeness inherited from the original POVM. Reading received J^n and executing its corresponding POVM is a local quantum operation at B2. If B1 also needs the reconstructed messages, B2 returns only classical decoded labels. This is a finite-round LOCC protocol at every blocklength and introduces no receiver quantum transmission, feedback to senders, or extra entanglement.

## LO exclusion and negative control

The separately source-fixed marginals yield C_LO=2h(1/4). It is below 2; an exact certificate is 27>16, which implies log2(3)>4/3 and 2h(1/4)<2. Any resource-discarding classical fallback gives at most the threshold 2. The strict LOCC gain therefore establishes membership in the original shell, which excludes LO-DC.

If B2 also Bell-measures each output R pair, a joint outcome amplitude is sum_l b_l k_l/4, giving a squared probability (sum_l b_l k_l)^2/16. Exact enumeration shows four nonzero outcomes each 1/4 for every input, and a uniform mean over all sixteen outcomes. Their entropies are 2 and 4, so the mutual information is 2. This control verifies that the exhibited gain comes through block quantum decoding. It is not an upper bound on all possible one-copy strategies.
