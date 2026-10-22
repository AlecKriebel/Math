# Attempt 3 of 5: make the localization candidate finitely generated

**Verdict: NO RESOLUTION.** The natural finitely generated repair is an ascending HNN extension, but its Euler characteristics vanish in every field. A general kernel/cokernel argument shows why this repair destroys the defect whenever the kernel has finite ordinary homology.

## The obvious repair: BS(1,p)

Attempt 2 produced an actual Euler-characteristic difference for the additive group A=Z[1/p], at the cost of failing finite generation. Multiplication by p is an automorphism of A. Form

    B = A semidirect_p Z
      = <a,t | t a t^{-1} = a^p>.

This two-generator group is BS(1,p). Its standard presentation complex is a finite K(B,1): view it as a graph of spaces with vertex and edge circles, and attaching maps the identity and the degree-p covering. Both induce injective homomorphisms on fundamental groups. The universal cover is a tree of contractible vertex and edge spaces, hence contractible. Equivalently, the Bass-Serre graph-of-spaces construction gives the usual asphericity proof. It follows that B is FL(Z), and therefore FL over all fields.

Could the difference from A survive this repair? No. With the trivial coefficient module F, the cellular complex of that finite K(B,1) is

    0 -> F --d2--> F^2 --0--> F -> 0,
    d2(1)=(1-p,0)

in the ordered basis (a,t), up to the harmless simultaneous sign convention for the relation. This follows by taking exponent sums of the relator t a t^{-1} a^{-p}: 1-p in a and 0 in t.

If char(F) does not divide p-1, the Betti vector is (1,1,0); if char(F) divides p-1, it is (1,2,1). In both cases the Euler characteristic is zero. In characteristic p itself the first case holds. Thus both required FL conditions are now satisfied, but the desired Euler difference has disappeared.

The extra H_2 over primes dividing p-1 is essential. Dropping it and comparing only H_1 would produce a false positive. Integrally, H_1(B;Z)=Z direct_sum Z/(p-1), and H_2(B;Z)=0; the extra H_2(Fq) is exactly the Tor contribution from H_1(Z).

## A general no-go result for this repair

Let 1 -> N -> G -> Z -> 1 be any group extension. It splits by choosing a lift t of 1 in Z. Fix a field F and assume that V_i=H_i(N;F) is finite-dimensional for every i and is zero above some degree. Let T_i be the automorphism induced by t.

The homological Lyndon-Hochschild-Serre spectral sequence has

    E^2_{a,b}=H_a(Z;V_b).

The standard length-one free resolution of the trivial module over F[Z] gives

    H_0(Z;V_b)=coker(T_b-1),
    H_1(Z;V_b)=ker(T_b-1),
    H_a(Z;V_b)=0 for a>1.

There are only two columns, so there are no possible nonzero higher differentials. The resulting finite filtration of H_n(G;F) yields

    dim H_n(G;F)=dim coker(T_n-1)+dim ker(T_{n-1}-1).

For every endomorphism of a finite-dimensional vector space, kernel and cokernel have the same dimension. Hence

    chi_F(G)
      =sum_n (-1)^n [dim coker(T_n-1)-dim ker(T_n-1)]
      =0.

No FL hypothesis on N is needed. The result applies separately in both fields when N has finite ordinary homology in both. It explains the failure of BS(1,p) without relying on its finite classifying space, and rules out repairing the localization example by any finite-dimensional-homology-by-cyclic construction.

## Other straightforward amplification operations

For groups with finite homology over F, the field Kunneth theorem gives chi_F(G x H)=chi_F(G) chi_F(H). Taking a product with Z therefore also kills the characteristic difference. Taking a product with a finitely generated group cannot cure the original failure of finite generation, because the projection onto A would make A a finitely generated quotient.

Likewise, A*H remains non-finitely-generated: A is a retract, so finite generation of the free product would imply finite generation of A. Products and free products therefore do not convert this near-counterexample into a valid one.

These arguments do not exclude arbitrary embeddings of A into finitely generated groups. Such an embedding supplies neither control of the ambient homology nor a finite resolution of its trivial module; claiming either would be a new unsupported realization theorem.

## Remaining gap

A positive construction must put the coefficient-sensitive defect into higher homology while avoiding the automatic cancellation from a finite-homology-by-Z extension. The next attempt examines Bestvina-Brady groups, where finiteness properties genuinely vary with the coefficient field and higher homology is explicit.
