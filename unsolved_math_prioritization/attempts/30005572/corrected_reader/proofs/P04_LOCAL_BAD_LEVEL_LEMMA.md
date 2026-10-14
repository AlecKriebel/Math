# A local boundary calculation at arbitrary depth

This is a boundary-only calculation for PASS1 of the Eisenstein/Bianchi construction attempt. It does not prove a bad-prime relation for the specialized K₂ cocycle. The proposed use of such a calculation is already anticipated in Lecouturier–Sharifi–Shih–Wang, Remark 5.2.10. The point established here is the precise operator statement, including oldvectors: nilpotence, rather than an identically zero operator, is sufficient.

## 1. Conventions and statement

Let K be a nonarchimedean local field, O its valuation ring, π a uniformizer, and Q the residue-field cardinality. Let α, β:K×→C× be smooth characters with conductor exponents a,b: a=0 means α is unramified; for a>0, a is the least positive integer for which α is trivial on 1+πᵃO. Use the same convention for b. Let

V = Ind_B^{GL₂(K)}(α⊗β)

be **unnormalized** induction, realized by smooth functions f satisfying

f([[x,y],[0,z]]g) = α(x)β(z) f(g).

For n≥1 put

K₁(n) = {[[x,y],[z,t]]∈GL₂(O): z∈πⁿO, t≡1 mod πⁿ}.

Operators are the unnormalized sums of right translations. Define

U = [K₁(n) diag(π,1) K₁(n)],
V_op = [K₁(n) diag(1,π) K₁(n)].

Explicitly, for representatives t of O/πO,

(Uf)(g) = Σ_t f(g [[π,t],[0,1]]),
(V_op f)(g) = Σ_t f(g [[1,0],[πⁿt,π]]).

The letter V_op denotes an operator, whereas V denotes the representation. No designation of one operator as the paper's unspecified U_q* is assumed. Both opposite conventions are covered. Replacing a matrix by its inverse instead of its adjugate only introduces an invertible central action on a complex principal-series constituent and preserves nilpotence.

**Lemma.** Suppose a,b>0. If n<a+b then V^{K₁(n)}=0. Otherwise it has a basis e_j indexed by

b≤j≤n−a,

and, with missing basis vectors interpreted as zero,

Ue_j = Q α(π)e_{j−1},
V_op e_j = Q β(π)e_{j+1}.

Consequently both operators have nilpotence exponent at most d=n−a−b+1. If d≥2, both operators are nonzero. Thus the literal zero-operator assertion fails on the full oldvector space at excess depth; the nilpotence assertion remains true.

## 2. Complete support calculation

By Iwasawa decomposition, f is determined by its restriction to GL₂(O). Representatives for

B(O)\GL₂(O)/K₁(n)

are

k_j = [[1,0],[πʲ,1]], 0≤j≤n.

Here j=n represents the identity double coset. To see exhaustiveness, inspect the bottom row (c,d) of an integral invertible matrix. Its invariant is min(v(c),n). If 0<v(c)<n then d is a unit and left multiplication by an upper triangular matrix reduces to a lower unipotent matrix with lower entry πʲu; right multiplication by diag(u,1), followed by a left diagonal multiplication, identifies its double coset with k_j. If c is a unit, an upper unipotent right multiplication makes the bottom-right entry zero; this is the Weyl double coset, also represented by k_0. If c∈πⁿO, left diagonal multiplication makes the matrix belong to K₁(n). Right multiplication by K₁(n) and left multiplication by B(O) preserve the stated invariant, so the double cosets are distinct.

For h=[[x,y],[0,z]]∈B(O), compute

k_j⁻¹ h k_j = [[x+yπʲ,y],[πʲ(z−x)−yπ²ʲ,z−yπʲ]].

Membership in K₁(n) is equivalent to

z−yπʲ ≡ 1 mod πⁿ,
x ≡ 1 mod πⁿ⁻ʲ.

For 0<j<n, the possible diagonal entries x,z range independently over 1+πⁿ⁻ʲO and 1+πʲO. At j=0 the condition on z is unrestricted among units, and at j=n the condition on x is unrestricted among units. Therefore the inducing character is trivial on the stabilizer of the jth double coset exactly when

a≤n−j and b≤j.

There is then one free value f(k_j); otherwise f(k_j)=0. Defining e_j by e_j(k_i)=δ_{ij} gives the asserted basis. This argument also proves its dimension, with no irreducibility assumption on the principal series.

## 3. Double cosets and matrix identities

For h=diag(π,1), the subgroup K₁(n)∩hK₁(n)h⁻¹ imposes the additional condition that the upper-right entry lie in πO. Representatives for its left quotient in K₁(n) are [[1,t],[0,1]]. This gives the displayed representatives [[π,t],[0,1]].

For h*=diag(1,π), the corresponding additional condition is that the lower-left entry lie in πⁿ⁺¹O. Representatives are [[1,0],[πⁿt,1]], giving [[1,0],[πⁿt,π]]. Thus both formulas are genuine double-coset operators and preserve K₁(n)-invariants.

For an allowed index j, both a,b>0 imply 1≤j≤n−1. Put s=1+πʲt. The exact factorization

k_j [[π,t],[0,1]]
= [[π,t],[0,s]] k_{j+1} diag(s⁻¹,1)

shows that its f-value is α(π)β(s)f(k_{j+1}). Since j≥b, β(s)=1. Summing gives

(Uf)(k_j)=Q α(π) f(k_{j+1}).

For the other operator put s=1+πⁿ⁻ʲt. The exact factorization

k_j [[1,0],[πⁿt,π]]
= diag(s⁻¹,π) k_{j−1} diag(s,1)

gives

(V_op f)(k_j)=Q β(π) f(k_{j−1}),

since n−j≥a. The rightmost diagonal factors belong to K₁(n). Values at unsupported indices vanish automatically because both outputs remain K₁(n)-invariant functions. This proves the formulas and the lemma.

For example, a=b=1 and n=3 give matrices, in the basis (e_1,e_2),

U = [[0,Qα(π)],[0,0]],
V_op = [[0,0],[Qβ(π),0]].

They are nonzero and square-zero. Their noncommutativity with one another is irrelevant: only one chosen level operator at each prime is added to the commutative away-from-level Hecke algebra.

## 4. Why nilpotence is enough integrally

If W is any module preserved by an operator T and Tᵈ=0, then

(1−T)(1+T+⋯+Tᵈ⁻¹)=1.

Thus T−1 is invertible, and localizing at a maximal ideal containing T−1 annihilates W. If nilpotence is first proved on W⊗Q_p and W is a torsion-free Z_p-lattice preserved by T, the same identity Tᵈ=0 holds on W. No division by Q or by character values is used in this inference.

In the global boundary decomposition, individual characteristic-zero principal-series summands need not split integrally. One must consequently apply the finite-Hecke-algebra support argument in BOUNDARY_REPORT.md, rather than assume an integral direct-sum decomposition by the pairs (α,β).

## Sources and credit

- E. Lecouturier, R. Sharifi, S.-C. Shih, J. Wang, *Eisenstein cocycles for imaginary quadratic fields*, arXiv:2504.19125v1, §5.2, Lemma 5.2.2 and Remark 5.2.10, pp.40–44: https://arxiv.org/pdf/2504.19125v1
- Distinct author-hosted manuscript, retrieved 14 October 2026, same title, §5.2, Lemma 5.2.2 and Remark 5.2.10, pp.41–45: https://www.math.ucla.edu/~sharifi/publ/imagquad.pdf

The induction and good-prime normalization match the displayed computation in the proof of their Lemma 5.2.2. The complete local support and opposite-operator calculations above are supplied here. They do not establish a newness claim or a bad-U identity for any K₂-valued map.
