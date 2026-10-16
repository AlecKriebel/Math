# Independent source-first reconstruction

Sealed before reading candidate mathematical proofs, checks, final results, historical review, or other audit-family conclusions. This is a deduction record, not a novelty claim or solution certificate.

## Exact source question and known exception

EMS serial article 46748, Oberwolfach Report 26/2018, printed pages 1624–1625 (PDF pages 46–47), presents Röver's finitely generated exception and then asks Question 111: whether every finitely presented subgroup of Thompson's dyadic PL group F has torsion-free abelianization. Both pages were downloaded and visually inspected. The source does not assert finite presentation of its exception. Bleak's 2006 Theorems 1.1–1.2 classify solvable groups through subgroup closure, bounded sums, and restricted wreath products; their subgroup operation cannot be omitted.

## Restricted wreath formula

Let W=(direct sum over Z of G_i) semidirect Z, where the generator shifts coordinate i to i+1 by conjugation. The base is restricted: only finitely many coordinates are nonidentity. Its abelianization is direct sum over Z of A=G_ab. A homomorphism W to A direct sum Z takes the sum of the coordinate images and the top exponent. The base commutators kill each G_i'; the shift commutators identify the images of adjacent coordinates. Every zero-total finitely supported vector is a sum of adjacent differences, by finite telescoping. Thus the kernel of that homomorphism is W', and W_ab=A direct sum Z. This proves the whole wreath-product formula for arbitrary G, including trivial and non-finitely generated G. It proves no corresponding formula for arbitrary subgroups of W. Repeated restricted wreath products starting from Z, and finite direct products of the resulting groups, have torsion-free abelianizations. Unrestricted products require a separate argument: infinite sums are not defined by this proof.

## Röver subgroup: exact integral answer

Write the base of Z wr Z additively as R=Z[x,x^-1], with a_i=x^i. For m>=1, let H_m=<t,r=x-1,s=m>. Its base is exactly the ideal I_m=mR+(x-1)R={P in R : P(1) is divisible by m}. Therefore H_m=I_m semidirect Z and H_m'=(x-1)I_m, since the base is abelian. Its base coinvariants have the explicit isomorphism

    I_m/(x-1)I_m -> Z direct sum Z/m,
    P -> (P(1)/m, P'(1) mod m).

The two generators m and x-1 map to (1,0) and (0,1), so the map is onto. Its kernel is exact: if P(1)=0, divide P=(x-1)Q in the Laurent polynomial ring; then P'(1)=Q(1), and the derivative congruence says Q belongs to I_m. This proves injectivity. Consequently H_m,ab=Z^2 direct sum Z/m. The m=2 case is exactly the source's r,s,t example: [r,t]=(x-1)^2; [s,t]=m(x-1); [r,s]=1. The r-class has order exactly m, not merely order dividing m.

The presentation of I_m by module generators s,r has only the relation (x-1)s=m r. Indeed mU+(x-1)V=0 implies U(1)=0, U=(x-1)C, and V=-mC, using the domain property of R. Setting x=1 gives m r=0, while s stays free. Tensoring with Q kills the r-class; any rational-only rank calculation misses this torsion.

The homomorphism W -> Z/m, given by total base coefficient, has H_m as its kernel, hence H_m has index m. W is not finitely presented: finite subsets of its infinite commutator presentation only impose distances at most N. The resulting group maps to the semidirect product of Z with the right-angled Artin group on vertices a_i, i in Z, with edges only when 0<|i-j|<=N. Translation preserves this graph. The induced two-vertex subgraph on 0 and N+1 has no edge, and the associated retraction to its free group proves [a_0,a_(N+1)] is still nontrivial. If the original relators normally generated the kernel by a finite set of words, each word and each derivation would use finitely many original relators, yielding some N, a contradiction. Finite presentation is invariant under passing to or from finite-index subgroups, so H_m is not finitely presented for every m>=1. The source exception cannot answer Question 111.

Finite cyclic shift controls are deliberately different: for n coordinates, I_(m,n)={v in Z^n : sum(v)=0 mod m}, its coinvariant torsion has order gcd(m,n). Periodic wrapping adds an n-dependent relation. These controls diagnose the danger of substituting a cyclic truncation for the infinite restricted base.

## Simple-derived subdirect theorem, independently proved

Assume G_i' = D_i is a nonabelian simple group and each G_i/D_i is torsion-free abelian. Let H be a subgroup of the finite product of the G_i that surjects onto every G_i. Then H_ab embeds in the product of G_i,ab and is torsion-free. No finite-presentation assumption is needed for this restricted theorem.

Proof: S=H' is contained in the product D_i and surjects onto each D_i, because a surjective homomorphism carries a derived subgroup onto the derived subgroup. A subdirect product of finitely many nonabelian simple groups is a direct product of diagonal blocks, each block joining isomorphic factors by isomorphisms. Here is the needed classification argument. Induct on the number of factors. The projection on the first n-1 factors is a product of diagonal blocks. Applying the elementary Goursat construction to that product P and the last simple factor D shows either the new factor is independent, or P/K is isomorphic to D. Normal subgroups of a finite product of nonabelian simple groups are products of its factors: commuting with each coordinate shows any nontrivial coordinate of a normal subgroup forces that entire factor, then factor them out. Thus in the second case K omits precisely one factor and D joins its diagonal block. This proves the classification, including the full-product and single-block cases.

Every such block product S is self-normalizing inside the product D_i. If (d_i) normalizes a diagonal block {(alpha_i(d))}, the equality of its induced coordinate conjugations says alpha_i^-1(d_i) and alpha_j^-1(d_j) induce the same inner automorphism. Their quotient is central in the nonabelian simple group, whose center is trivial. The normalizing tuple therefore lies in that block. Blocks have fixed coordinate supports, so an element of the direct product cannot permute them. The case n=1 is immediate.

Now K=H intersect product D_i normalizes H'=S, since H' is characteristic in H. Thus K is contained in S by self-normalization, and S is already contained in K. Hence H intersect product D_i=H'. The product abelianization map induces an injection H/H' -> product G_i/D_i. A subgroup of a torsion-free abelian group is torsion-free; for copies of F its image is a subgroup of Z^(2n), so it is also free abelian of finite rank. This establishes the kernel and commutator equality rather than assuming it.

For F, the assumptions are supplied by Cannon–Floyd–Parry (1996), Theorems 4.1 and 4.5: endpoint slope logarithms give F_ab=Z^2, and F' is simple. Nonabelianness follows because compactly supported copies of F lie in F', and F is nonabelian. Simplicity then makes F' perfect and centerless. The original author paper was obtained from a university mirror after the E-Periodica endpoint returned verification HTML; full source bytes are hashed in SOURCE_RECEIPT.json.

## Boundaries that must remain explicit

Surjectivity onto full factors matters. A subgroup can project only to proper subgroups, whose derived groups need not be simple. The Röver subgroup can be placed in a single F factor, or diagonally in F^n; such a subgroup is not subdirect onto the full F factors. An arbitrary subgroup of a group with torsion-free abelianization need not have torsion-free abelianization.

Nonabelian simplicity/perfectness matters. For a concrete counter-control, take G={(a,b,c):a,b in Z,c in Z/p}, with product (a,b,c)(a',b',c')=(a+a',b+b',c+c'+ab' mod p). Its derived subgroup is central C_p and G_ab=Z^2. The fiber product H={(g,h):g_ab=h_ab} is subdirect onto G twice, but H' is the diagonal C_p, whereas H intersect (C_p)^2=(C_p)^2. Thus H_ab=Z^2 direct sum C_p. A merely simple abelian derived subgroup does not suffice.

The quotient maps must be the actual maps G_i -> G_i/G_i'; choosing unrelated finite quotients or computing only rational relations does not establish H intersect product G_i'=H'. A finite-index lattice in a free abelian ambient group is still intrinsically free, even if the ambient quotient has torsion. Saturation is not required for the subdirect theorem once the kernel equality is proved.

## Success criterion and exact gap

Success for this audit family is verification or falsification of the claimed restricted wreath and subdirect results, with integral controls and source scopes. These results cover particular constructions. They do not show that every finitely presented subgroup of F belongs to one of them. The exact discovery gap remains classification or direct control of an arbitrary finitely presented subgroup's commutator kernel; no complete answer to Question 111 is implied.
