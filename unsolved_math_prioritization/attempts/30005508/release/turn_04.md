# Approach 4: direct-product transfer and the limit of Morita reductions

## Aim

Seek a valid transfer principle that preserves the actual centralizers and conjugacy intersections, rather than merely the number of ordinary or Brauer characters.

## Product theorem

Suppose B is a real nonprincipal 2-block of G with defect pair (D,E), and let T be any finite 2-group. The corresponding product block B'=B⊗kT of G'=G×T has defect pair

(D',E')=(D×T,E×T).

For example this follows directly by taking the old real defect class times {1}; its centralizer and extended centralizer acquire the factor T.

Let ((x,z),b') be the product subsection, where b'=b⊗kC_T(z), and assume b has one simple module. Then b' also has one simple module. Its unique projective character is

Φ'=Φ⊗ρ_{C_T(z)},

where ρ denotes the ordinary regular character. Take a root (y,w)²=(x,z), so y²=x and w²=z. Centralizers split:

C_{G'}(x,z)=C_G(x)×C_T(z),
C_{G'}(y,w)=C_G(y)×C_T(w).

The regular character restricted from C_T(z) to C_T(w) is [C_T(z):C_T(w)] copies of the latter's regular character. Therefore

⟨Φ'_{C_{G'}(y,w)},1⟩
=⟨Φ_{C_G(y)},1⟩ [C_T(z):C_T(w)].  (4)

The relevant conjugacy class and coset likewise split, giving

|(y,w)^{C_{G'}(x,z)}∩(E'\D')|
=|y^{C_G(x)}∩(E\D)| · |w^{C_T(z)}|
=|y^{C_G(x)}∩(E\D)| [C_T(z):C_T(w)].  (5)

The common multiplier is a positive integer. Thus the local formula for the product block is equivalent, for these data, to the original formula. A valid instance transfers, and a failure would transfer as well.

## Why this does not finish the problem

This product argument works because it controls all three items explicitly: the local projective character, the subgroup on which it is restricted, and the conjugacy-class intersection. Ordinary Morita equivalence alone does not supply such control of ambient-group centralizers or of orbit permutation modules.

The all-pair construction in Approach 3, combined with this theorem, gives further positive examples. It does not reduce an arbitrary one-simple-module block to those examples. In particular, “one simple module” cannot be replaced by “nilpotent”: a one-by-one Cartan matrix records a scalar, whereas the required multiplicities depend on separate conjugation orbits. The following approach tests this distinction in an explicit nonnilpotent block.

## Outcome

A genuine transfer theorem is proved, but its hypotheses do not cover arbitrary blocks or arbitrary Morita equivalences. No unproved compatibility of a Morita equivalence with conjugation-orbit modules is used.
