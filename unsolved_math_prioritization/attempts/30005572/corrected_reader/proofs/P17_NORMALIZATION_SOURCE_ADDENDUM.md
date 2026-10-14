# Normalization source check and root-of-unity scope

Shared PASS3/5. This addendum qualifies the source-identification wording in §1 of EXACT_THETA_RESIDUE_TEST.md (SHA256 8e9aee84bdec01f3a7209cf36a0703257cb2dc799860274bf458b3b03eb5d240). Its exact rational-function and tame-symbol claims are unchanged.

## Independently checkable primary formula

Masataka Chida, *On the equivariant Tamagawa number conjecture for CM elliptic curves*, RIMS Kokyuroku Bessatsu B4 (2007), pp.197–221, §8, printed pp.211–213, gives the Robert product and its Kato identification. Public PDF:

https://www.kurims.kyoto-u.ac.jp/~kenkyubu/bessatsu/open/B4/pdf/B04_014.pdf

The complete PDF was retrieved directly after web-renderer timeouts. Its SHA256 is 5d29e2cfc19ccee3540a7b75c666c157c2feffdbe52e9dd506a0c620013b4bcd. An accessible companion is §5, pp.6–7 of the author's preprint:

https://www.math.kyoto-u.ac.jp/~tetsushi/mw200705/chida_preprint.pdf

The source's eta-based lattice quantity, denoted η^(2), has scaling weight **one**, because it is ω₂^{-1}·2πi·η(ω₁/ω₂)². For L'=L/5, its scaling factor is five. The Robert product consequently has prefactor εΔ²/5, with ε a twelfth root of unity. The product over the twelve nonzero 5-torsion pairs is ψ₅/5. Dividing gives

  Robert_5 = ε Δ²/ψ₅,       ε∈μ₁₂.                       (A.1)

This argument only claims the source identification (A.1), not that Chida's unspecified root convention has independently been checked to give ε=1. The report's specified quotient Θ(z)²⁵/Θ(5z) fixes the rational function Δ²/ψ₅ by its leading coefficient. The exact computed object remains that fixed rational function.

## Why the distinction does not weaken the residue result

Multiplication by ε is zero in multiplicative-group notation after tensoring with R=Z[1/6]. Therefore Robert_5 and Δ²/ψ₅ give the same R-valued unit and the same R-valued Steinberg classes.

There is also exact cancellation for the local tame symbols of this test. The two valuations are (24,48) upstairs, and (12,24) downstairs. Multiplying both entries by the same ε changes the residue by ε raised to their valuation difference, namely 24 or 12. Both exponents kill μ₁₂. If a root convention is compared only after extending the field, the R-valued comparison suffices and avoids identifying a larger marked field with the base.

The primary-source normalization check therefore supports the seven-primary and R-valued theta-symbol statements. It still supplies no comparison with the LSSW Gersten cocycle and no global relative homology map.

## Retrieval boundary

The Chida RIMS PDF is complete and its relevant pages were extracted and inspected. An attempted full Kato 2004 PDF download timed out after 1,239,726 of 18,010,813 bytes; that incomplete private file is marked .partial and is not used as source evidence. Neither third-party PDF nor source text belongs in a public authored-proof publication bundle.
