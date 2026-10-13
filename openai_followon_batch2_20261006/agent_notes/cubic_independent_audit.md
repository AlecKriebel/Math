# Independent adversarial audit: cubic KE/GIT compactification consequence

Checkpoint: 2026-10-06 PDT. Audit completion estimate 95% for the proposed implication, not for the upstream proof. Verdict: **accept the compactification target; require separate arguments for stronger algebraic structure claims.**

## Verified chain

1. Family037 Theorem main applies to every singular boundary-zero complex algebraic klt germ of dimension k>=2 and gives normalized volume <=2(k-1)^k.
2. Li–Liu, *Kähler–Einstein metrics and volume minimization*, https://arxiv.org/abs/1602.05094, Theorem1.9 (=Theorem6.2), states that the Reeb valuation associated to a smooth Sasaki–Einstein link globally minimizes normalized volume over all centered valuations of its cone. Section6 explicitly includes irregular Reeb fields by approximation. This is the crucial bridge: a bound on an infimum alone would NOT bound an arbitrary Reeb valuation. It is necessary to invoke minimization.
3. For the Ricci-flat Kähler cone with isolated vertex, normalized volume of its Reeb valuation equals k^k times its metric volume density. Thus the new algebraic gap supplies Spotti–Sun's metric cone density conjecture in every required lower dimension, including irregular cones. The cone germ is in the standard algebraic klt, zero-boundary setting; no log pair is introduced.
4. Spotti–Sun, https://arxiv.org/abs/1705.00377, Theorem1.3(2), conditionally identifies the cubic GH/KE compactification with the classical GIT quotient. Their Section5.2 supplies the proof: cone-density control preserves the Cartier polarization on limits, Fujita classification shows limits remain cubic, and moduli continuity plus CM polarization matches the compactifications.

## Scope restrictions and publication target

Use the exact claim of a natural identification of the GH compactification of the KE moduli of smooth cubic n-folds with the classical GIT quotient, hence the corresponding coarse polystable KE/K-moduli identification. Focus novelty on n>=5 because dimensions<=4 are known.

Do not automatically upgrade this to a scheme/stack isomorphism, equivalence of moduli functors, or every nonclosed GIT semistable point being K-semistable. Those assertions require checking modern algebraic K-moduli comparison, stabilizers, families, and scheme structure. The GH theorem is already a clear, significant target without these upgrades.

The existence of KE metrics on smooth cubics is a consequence of the cited theorem chain but should undergo its own priority audit; it should not be advertised as the central novelty when the new boundary compactification is the stronger contribution. Likewise, canonical singularities of GIT semistable cubics have separate recent work and should be credited.

No remaining central conjecture occurs in this chain. The required work is source matching, contemporary priority audit, exact moduli formulation, and concise proof writeup. No base theorem has been independently checked or formalized in this audit.
