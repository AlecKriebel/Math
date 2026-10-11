# Canonical algebra-group products: a source-grounded normalization derivation

AI-assisted proof exposition with a separate AI-assisted mathematical audit.

Date: 2026-10-11 UTC. Problem 20002813 / AIM-REPRESENTATION_THEORY-0085.

## Scope and status

This is a short derivation for the **standard two-sided-orbit supercharacter theory of a finite algebra group**. It answers the algebra-group subquestion in the 2010 AIM list in its canonical normalization. It does not classify arbitrary finite-group supercharacter theories. The underlying orbit construction is credited to Diaconis--Isaacs; no novelty is claimed. The accompanying AUDIT.md and acceptance records accept this exact restricted scope. This separate AI-assisted check is not external human peer review or formal proof-assistant certification.

## Primary source pins

- AIM, *Supercharacters and Combinatorial Hopf Algebras*, edited by Carolina Benedetti, workshop May 17--21, 2010, Problem 1.1, PDF p.1: https://aimath.org/WWN/supercharacters/supercharacters.pdf . 53,794 bytes, SHA-256 b25dad747e4e42f81db9346826caf0de42d54800c612e59d1031b0fafd48105c.
- P. Diaconis and N. Thiem, *Supercharacter formulas for pattern groups*, arXiv:math/0610161v1 (4 October 2006), Section 2.3, PDF pp.6--7: https://arxiv.org/pdf/math/0610161v1 . 271,277 bytes, SHA-256 e351061ff641525350cd80d945d2cd7d32bba3673fbc7de60513d0ec2c0af430. The displayed orbit formula and disjoint irreducible-support assertion on p.7 were visually inspected. Their underlying reference [10] is Diaconis--Isaacs.
- P. Diaconis and I. M. Isaacs, *Supercharacters and superclasses for algebra groups*, Transactions AMS 360 (2008), 2359--2392, DOI https://doi.org/10.1090/S0002-9947-07-04365-6 . Publisher PDF retrieval returned 403; no direct PDF inspection or byte hash is claimed for this source.

## Statement

Let J be a finite-dimensional associative nilpotent algebra over F_q and G=1+J. Fix a nontrivial additive character theta of F_q. For each two-sided orbit O in J*=Hom_Fq(J,F_q), let X_O be the irreducible-character block of the standard algebra-group supercharacter theory. Its canonical character is

sigma_O = sum_{chi in X_O} chi(1) chi.

For an element nu in a third orbit R, set

m(O,P;R)=#{(lambda,mu) in O x P : lambda+mu=nu}.

Then this cardinality is independent of the representative nu in R and

sigma_O sigma_P = sum_R m(O,P;R) sigma_R.

In particular every coefficient is a nonnegative integer.

## Proof, including the canonical normalization

For nu in J*, write e_nu(1+x)=theta(nu(x)). The map J* to the full character group of the additive group J sending nu to e_nu is a bijection: if nu is nonzero then its image is F_q and theta composed with nu is nontrivial, and both groups have cardinality |J|. Thus the e_nu form an orthonormal basis for functions on the underlying set of G under the normalized counting inner product.

Put F_O=sum_{nu in O} e_nu. The source's conventional supercharacter for O=G lambda G is

tau_O = (|lambda G|/|O|) F_O.

These tau_O are characters with pairwise disjoint irreducible supports, and every irreducible occurs in exactly one of them. Consequently each F_O is a positive scalar multiple of a character and has the same disjoint irreducible support X_O. Additive Fourier orthogonality gives

sum_O F_O(1+x) = sum_{nu in J*} theta(nu(x)) = |G| if x=0, and 0 otherwise.

The sum is therefore exactly the regular character rho_G. In its irreducible expansion the coefficient of each chi is chi(1). Because only the unique F_O with chi in X_O can contribute to that coefficient, the coefficient of chi in F_O is chi(1). Hence F_O=sigma_O. This proves the required canonical identity; it does **not** identify tau_O with sigma_O.

As an independent normalization check, tau_O(1)=|lambda G| and ||tau_O||^2=|lambda G|^2/|O|. Since tau_O=c_O sigma_O, the general formula c_O=||tau_O||^2/tau_O(1) gives c_O=|lambda G|/|O|, the same prefactor.

Now e_lambda e_mu=e_{lambda+mu}, so

F_O F_P = sum_{nu in J*} #{(lambda,mu) in O x P : lambda+mu=nu} e_nu.

Each two-sided transformation nu -> g nu h is an invertible F_q-linear map on J*. If nu'=g nu h, applying that same transformation to both entries is a bijection between decompositions of nu with entries in O,P and decompositions of nu' with entries in O,P. Both input orbits are preserved. The coefficient is constant on R, so grouping the final sum by R and using F_R=sigma_R proves the formula.

## Boundary checks and interpretation

- This uses **pointwise multiplication within a fixed group**, not induction products between groups of different sizes.
- The zero orbit gives the trivial character and is the multiplicative identity; the formula has coefficient 1 for O+{0}=O.
- A zero coefficient is allowed: the source's phrase 'positive integer combination' must mean a nonnegative-integer linear combination, as for character-ring structure constants.
- Finite field size is arbitrary, including characteristic two. Nilpotence ensures 1+J is a finite group; associativity is used in its two-sided action.
- For the coefficient at the zero orbit, the count is |O| if P=-O and 0 otherwise, matching the canonical inner product after conjugation.
- The action formula is (g lambda h)(x)=lambda(g^{-1} x h^{-1}). Right-action composition can be viewed via the opposite group; only invertibility, linearity, and orbit preservation are needed in the decomposition argument.
- No claim is made for an arbitrary supercharacter theory on the same underlying algebra group. Only its standard two-sided-orbit theory is addressed.

## Source hygiene

The unweighted assertion about the sum of 'distinct supercharacters' in paragraph (a) of the Diaconis--Thiem preprint p.7 is not used. For the displayed conventional normalization, the regular-character identity generally needs weights. The proof above establishes the correct identity directly for the unnormalized orbit sums and uses only the displayed orbit formula plus disjoint-support construction.

The public edition contains authored mathematics and public verification metadata only. Source documents, extracted source text, source images, datasets, and diagnostic programs are excluded.
