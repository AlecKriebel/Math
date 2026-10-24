# Independent zero-weight directions still give a polynomial upper bound

October 24, 2026 UTC. **Derived partial obstruction, not a solution of 21.126; originality not established.** This is a distinct attempt to escape the nonzero-weight obstruction by adding height-zero directions. The attempt remains polynomial under the explicit hypotheses below.

## Claim

Let Γ be a finite graph whose vertex set is the disjoint union S⊔D. Suppose:

- D is an independent set (no edge joins two dead vertices);
- the flag complex L_S of the induced graph on S is simply connected;
- for each z∈D, the induced graph Λ_z on its neighbors in S is nonempty and connected.

Let φ:A(Γ)→Z have nonzero integer weights m_s on S and weight zero on D. Then H=ker φ is finitely presented and

    δ_H(n)≼n^9.

The exponent 9 is only an upper bound from the argument; it is not claimed sharp. The theorem does not cover edges between dead vertices, arbitrary coabelian kernels, or arbitrary subgroups of these kernels.

## 1. A quadratic distortion lemma

If Λ is a finite connected graph and ψ:A(Λ)→Z has only nonzero weights, then K=ker ψ is finitely generated and

    Dist_K^{A(Λ)}(n)≼n².

Proof: invert negative generators and divide the weights by their gcd. The rectangular height-pushing construction in WEIGHTED_HEIGHT_QUARTIC.md requires only connectedness of the flag complex when it is extended over the **one-dimensional** skeleton of each deleted vertex ball. Indeed, pos and neg need only be extended from the link to its cone 1-skeleton; choose the center image and finitely many connecting paths in the connected positive/negative link. Thus Q is defined on Y∪X^(1), has Lipschitz constant O(t+1) on height-t strips, and fixes the zero level set Z_Λ. This also makes Z_Λ path connected. The kernel acts properly and cocompactly on Z_Λ, by the same bounded-height cube argument as before, and therefore is finitely generated, with its word metric quasi-isometric to the intrinsic length metric on Z_Λ.

For k∈K of ambient word length at most n, a word geodesic from 1 to k lies in X^(1), has rectangular length O(n), and stays in a height strip O(n). Its Q-image is a path in Z_Λ of length O(n²), connecting the same endpoints. This proves the distortion bound. No simple-connectivity or finite-presentability assertion about K is used here.

## 2. A centralizer-extension filling estimate

Let G=⟨X|R⟩ be finitely presented. Let K_1,…,K_q≤G be finitely generated, with fixed finite generating words U_i in X. Form the simultaneous identity HNN extensions

    E=⟨X,t_1,…,t_q | R, [t_i,u]=1 for u∈U_i⟩.

The base G embeds by the HNN normal-form theorem. Let f(n) be a common upper bound, up to linear changes of constants, for all subgroup distortions Dist_(K_i)^G(n). Then

    δ_E(n)≼ n·δ_G(n+f(n)) + n·f(n) + δ_G(n).

Here one may replace δ_G by any nondecreasing isoperimetric upper bound. In particular δ_G≼n^4 and f≼n² imply δ_E≼n^9.

Proof: a null word w of length at most n containing stable letters has a Britton pinch t_i^ε u t_i^(−ε), where u is a word in X representing an element of K_i. Replace that segment by the **same X-word u**, deleting two stable letters. Throughout this process the total number of X-letters never increases; every pinch word u has length at most n. Choose a U_i-word v representing u, with |v|≤f(n) after changing the distortion constants. The relation t_i^ε u t_i^(−ε)=u has a filling using two G-diagrams for uv^−1 and |v| stable-letter commutation cells. Its area is at most 2δ_G(n+C f(n))+C f(n), where C bounds the X-lengths of U_i letters. There are at most n/2 pinches. Once all stable letters are removed, fill the remaining X-word, of length at most n, in G. This proves the bound. The point is that rewriting to v is used only inside a filling certificate; the boundary reduction keeps the original u and creates no iterated length expansion.

## 3. Exact kernel decomposition

Scale φ so its image is Z. Since dead weights vanish, its restriction to A(S) is onto. Choose t∈A(S) of φ-height 1. Put G=ker(φ|_(A(S))). For z∈D let

    d_z = gcd{|m_s| : s∈Λ_z},
    K_z = ker(φ|_(A(Λ_z))),
    K_(z,i) = t^i K_z t^(−i) ≤ G,  0≤i<d_z.

Then

    H ≅ ⟨ G, z_i (z∈D,0≤i<d_z) | [z_i,K_(z,i)]=1 ⟩,

where z_i maps to t^i z t^(−i). This is a finite simultaneous centralizer extension of G.

The graph hypothesis on D means that A(Γ) is exactly the simultaneous identity HNN extension of A(S) with stable letters z and associated subgroups A(Λ_z). Here is a direct check of the claimed kernel description.

Surjectivity: rewriting a height-zero word with powers of t produces elements of G and conjugates t^q z t^(−q), with q∈Z. Write q=i+ℓd_z, 0≤i<d_z. Choose v_z∈A(Λ_z) of φ-height d_z; such a word exists by Bézout's identity applied to the weights. Set h=t^q v_z^(−ℓ) t^(−i)∈G. Since v_z commutes with z,

    h (t^i z t^(−i)) h^(−1) = t^q z t^(−q).

Thus the displayed generators span H.

Injectivity: take a reduced word in the claimed simultaneous HNN extension. If its image were trivial in A(Γ), Britton's lemma in A(Γ) would give two consecutive stable z-letters with an intervening base word t^(−i) g t^j∈A(Λ_z), g∈G. Taking φ gives j−i∈d_z Z. Because 0≤i,j<d_z, this forces i=j; the membership condition then says g∈t^i K_z t^(−i)=K_(z,i). This would be exactly a forbidden pinch in the claimed reduced word. Hence no nonempty reduced word maps trivially. A word with no stable letters is handled by the obvious injection G≤A(S). The map is therefore injective as well as surjective.

## 4. Polynomial filling bound

The flag complex L_S is simply connected and all its weights are nonzero. WEIGHTED_HEIGHT_QUARTIC.md gives finite presentability of G and δ_G≼n^4.

Each Λ_z is connected and all its weights are nonzero, so section 1 shows K_z is finitely generated and quadratically distorted in A(Λ_z). The induced parabolic A(Λ_z) is isometrically embedded in A(S) for the standard word metrics: inclusion gives one inequality, and the generator-killing retraction gives the other. Fix any finite generating set of G. Its generators have bounded ambient A(S)-length. Conjugation by each of the finitely many fixed t^i changes ambient length by only a constant. Thus for k_i=t^i k t^(−i)∈K_(z,i),

    |k|_(A(Λ_z)) ≤ C |k_i|_G + C,
    |k_i|_(K_(z,i)) ≤ C' (|k_i|_G+1)².

Consequently the finitely many K_(z,i) have a common quadratic distortion bound in G. The presentation of section 3 uses finitely many stable letters and finitely many commutator relators, because every K_z is finitely generated. Apply section 2 to obtain δ_H≼n^9.

## Exact remaining gap

Adding independent zero-height directions to a simply connected live part with connected live links does not produce an intermediate example. This is a polynomial upper-bound result, not a lower-bound construction.

When dead vertices have edges between them, the clean simultaneous identity-HNN description over the single base G acquires extra relations between height-indexed stable letters. The argument above then does not give the required pinch reductions over G. Declaring the enlarged subgroup polynomial without a new filling mechanism would transfer the central difficulty to an unsupported assertion. That extension is left unresolved.
