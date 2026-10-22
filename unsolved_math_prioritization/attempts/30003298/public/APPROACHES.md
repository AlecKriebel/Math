# Five routes, retained deductions, and gaps

Throughout, g>=2, Gamma<=Mod_g is torsion-free and finite-index, D_Z=H_(2g-2)(C_g;Z), D=D_Z tensor Q, n=6g-6, q=2g-1, d=4g-5. The outcome remains **unsolved for general genus; five approach families**. Routes 1–4 establish reductions and test obstructions; Route 5 proves the top-degree theorem and the exact genus-two case.

## Approach 1. Compactification, boundary homology, and the obstruction

Let M be the compact thick-Teichmüller quotient with boundary B. It is oriented, n-dimensional, and homotopy equivalent to BGamma. Treat D_Z as a local coefficient system via this equivalence. Poincaré–Lefschetz duality gives H^q(M;D_Z)=H_d(M,B;D_Z), since n-q=d.

**Conditional kernel criterion.** Suppose H_d(B;D_Z)=0. Then there is an exact sequence

    0 -> Z -> H^q(Gamma;D_Z) -> K -> 0,
    K = ker[H_(d-1)(B;D_Z) -> H_(d-1)(M;D_Z)].

**Proof.** Duality for Gamma identifies H_d(M;D_Z) with H^0(Gamma;Z)=Z. The long exact homology sequence of (M,B) has consecutive terms

    H_d(B;D_Z) -> H_d(M;D_Z) -> H_d(M,B;D_Z)
      -> H_(d-1)(B;D_Z) -> H_(d-1)(M;D_Z).

Insert the assumed zero, the Z identification, and Poincaré–Lefschetz duality. Exactness produces the displayed sequence. QED.

**Consequence.** Under this hypothesis the requested abelian group is finitely generated if and only if K is finitely generated. One direction passes to a quotient. For the other, lift finitely many generators of K and adjoin a generator of the kernel Z; these elements generate the middle group. A single nonzero or infinite-order obstruction therefore does not by itself answer the infinite-generation question.

Avramidi's 2017 manuscript claims the needed boundary vanishing using a small singular model, and derives a nonzero primary obstruction in §9. Its current public author page labels the manuscript under revision. We do not reprove that specialized stabilizer/small-model argument or elevate it to a newly verified theorem. The criterion above is retained with its hypothesis explicit. The main theorem of this packet does not depend on that manuscript.

**Gap.** No infinite-rank family in K was constructed. Compactness of B does not make homology with the infinite-rank coefficient system D_Z finitely generated: the cellular coefficient groups themselves may have infinite rank.

## Approach 2. Transgression of equivariant endomorphisms

Use rational coefficients. The homotopy fibration C_g -> E=(EGamma x C_g)/Gamma -> BGamma has E homotopy equivalent to the boundary B. Pull the local system D back from BGamma. Since C_g is simply connected and has reduced homology only in degree m=2g-2, the cohomological Serre spectral sequence has only two rows:

    E_2^(a,0)=H^a(Gamma;D),
    E_2^(a,m)=H^a(Gamma;Hom_Q(D,D)).

The action on Hom is conjugation, (gamma f)(x)=gamma f(gamma^(-1)x). These identifications follow from the universal coefficient theorem over Q; there is no replacement of Hom by D tensor D. For an infinite-dimensional D those are different modules.

The only possible differential between the rows has length m+1=q. The low-degree filtration therefore gives an exact segment

    H^m(E;D) -> End_(QGamma)(D) --tau--> H^q(Gamma;D)
      -> H^q(E;D).

**Proof of exactness at the two middle terms.** At position (0,m), no differential enters and the sole possible outgoing differential is d_q to (q,0). Thus E_infinity^(0,m)=ker(tau), precisely the image of the edge homomorphism from total degree m. At position (q,0), the sole possible incoming differential is this tau and no differential leaves the bottom row; hence E_infinity^(q,0)=coker(tau), which is the first filtration piece in total degree q and embeds in H^q(E;D). QED.

Consequently, infinite dimension of End_(QGamma)(D)/im[H^m(E;D)] would prove the rational target infinite-dimensional. The identity endomorphism transgresses to the primary fibration obstruction, up to the conventional sign. This follows by constructing a section over the m-skeleton: on each (m+1)-cell its attaching sphere produces the corresponding element of H_m(C_g)=D, which is both the obstruction cocycle and the transgression of the identity on fiber homology.

**Gap.** Neither the endomorphism quotient nor its image was calculated. Producing infinitely many invariant bilinear forms in Approach 5 gives maps D->D*, not endomorphisms D->D. No self-duality D=D* or lift into D is available. In particular, the infinitely generated free abelian homology of C_g cannot silently be replaced by its generally much larger cohomology module.

## Approach 3. Duality and positive-degree chain obstructions

The general-coefficient duality formula gives exactly

    H^q(Gamma;D) = H_k(Gamma;D tensor D),   k=2g-4.

An explicit method would require bar k-cycles with these coefficients and independent functionals on their homology classes, or an independently justified equivalent resolution. For a surjective coefficient map A->V with kernel J, the homology long exact sequence contains

    H_k(Gamma;A) -> H_k(Gamma;V) -> H_(k-1)(Gamma;J).

Thus a coefficient surjection is not automatically a homology surjection when k>0. Vanishing of the connecting map (sufficiently, vanishing of H_(k-1)(Gamma;J)) is an additional obligation.

**Countermodel to lifting the degree-zero argument.** Let G=Z=<t> and M=Q[G]. The diagonal module M tensor_Q M has basis t^a tensor t^b, indexed by (a,b) in Z^2. The change of coordinates (a,b)->(a,b-a) identifies it with a direct sum, indexed by Z, of regular Q[G]-modules. Hence its coinvariants are a direct sum of infinitely many copies of Q. On the other hand, the length-one free resolution for Z has differential multiplication by t-1. This multiplication is injective on Q[t,t^(-1)] and on any direct sum of its copies, because a nonzero finite Laurent polynomial cannot be annihilated by t-1. Therefore H_1(G;M tensor M)=0, and H_k=0 for every k>1 because the resolution has length one. Thus infinite-dimensional H_0 can coexist with vanishing in every positive degree.

**Gap.** For g>=3 the required k is positive. No surviving positive-degree cycles or connecting-map vanishing were established. This countermodel is not a counterexample to Avramidi's mapping-class question; its role is to invalidate the formal inference from the top-degree theorem to the target degree.

## Approach 4. Finite-index transfer and descent

Let Lambda<=Gamma have finite index e, and let A be a rational Gamma-module. Restriction and transfer obey

    cor circ res = e id on H^j(Gamma;A).

One way to see this is to use the finite covering of classifying spaces: transfer sums all e lifts of a simplex with the coefficient transport, so composing the pullback with this sum is chain homotopic to multiplication by e. Since e is invertible in Q, restriction is split injective. Therefore infinite rational rank for Gamma propagates to every finite-index Lambda.

If Lambda is normal, set F=Gamma/Lambda. The Lyndon–Hochschild–Serre spectral sequence collapses to

    H^j(Gamma;A) = H^j(Lambda;A)^F.

Indeed higher cohomology of the finite group F over Q vanishes by averaging, leaving only the invariant column. Averaging also shows that a class survives descent precisely through its invariant component; an infinite-dimensional space below need not have an infinite-dimensional invariant subspace.

**Explicit failed reverse implication.** Let Gamma=Z=<t>, Lambda=2Z, and let A be a countable direct sum of copies of Q on which t acts as -1. The length-one resolution gives H^1(Gamma;A)=A/(t-1)A=A/2A=0, whereas t^2 acts trivially and H^1(Lambda;A)=A, which has infinite dimension. This is a rigorous countermodel to a coefficient-independent upward-propagation claim, not a claimed model of D.

**Gap.** A proof for a specially chosen smaller mapping-class subgroup cannot be transferred upward without invariant-class information. Varying the level in ordinary rational top cohomology also changes the group and does not prove infinite generation for a fixed group. Approach 5 avoids both pitfalls: the group remains fixed while finite-image quotient forms are varied.

## Approach 5. Finite-image quotients and invariant bilinear rank

Fullarton–Putman's equivariant finite-image quotients D->V_p have unbounded dimensions for fixed genus. Averaging positive rational forms on each finite quotient and pulling back gives Gamma-invariant forms on D with rank dim(V_p). A finite-dimensional span of finite-rank forms has bounded rank, by rank subadditivity. Hence these forms span an infinite-dimensional subspace of ((D tensor D)_Gamma)*. The coinvariants are infinite-dimensional, and duality places this in H^d(Gamma;D). The finite classifying-space chain complex commutes with rationalization, so H^d(Gamma;D_Z) has infinite rational rank. Every step is proved in `PROOF.md`.

**Exact success.** This settles the source degree for g=2 because q=d=3. It also proves a top-degree statement for every g>=2. There is no new computation of Steinberg relations, no assumption that Gamma is a congruence subgroup, and no use of irreducibility, a symplectic Steinberg quotient, or finite-group simplicity.

**Remaining gap.** For every g>=3 one still has to determine whether H_(2g-4)(Gamma;D tensor D), equivalently H^(2g-1)(Gamma;D), is infinitely generated (and integrally, whether torsion can matter if rational rank is finite). The arguments here do not settle this. The failure tests in Approaches 2–4 explicitly explain why the successful degree-zero construction does not close that gap.
