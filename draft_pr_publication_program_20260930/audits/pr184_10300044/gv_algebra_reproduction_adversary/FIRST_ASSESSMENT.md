# Independent first assessment: GV algebra and reproduction family

This assessment was derived before any original reviewer, independent_checks.py, stored verification receipt, imported report, or sibling/root verdict was read. The title and negative answer were treated as hypotheses. Primary-dependency confirmation is still pending at this seal.

## Target and source

The actual 2002 v1 Calegari paper, printed p. 25, asks: "Is there a uniform bound on the Godbillon–Vey invariants of the taut foliations of a hyperbolic manifold in terms of its volume?" I read the complete question and remark, Definition 1.1 on p. 1, and section 13.1 on p. 29. The single-circle condition is explicit in Definition 1.1. Section 13.1 discusses the usual sufficiently smooth foliation invariant, with C2 sufficient. No minimality restriction occurs in Question 10.6. The remark suggests a fixed-manifold estimate, so a purported fixed-manifold counterexample requires especially careful scrutiny; the remark itself supplies no differential bound in the text.

The claimed theorem has a fixed closed oriented hyperbolic M and, for every positive integer N, a smooth cooriented foliation with one closed transversal meeting every leaf and GV=Na, for fixed a>0. This would refute every finite volume-only bound, and is stronger than merely disproving a linear bound.

## Independently derived differential-form obligations

Use oriented coordinates (x,y,z), alpha=dz+p dx+q dy, eta=p_z dx+q_z dy. Then

- alpha wedge d alpha = (q_x-p_y+q p_z-p q_z) dx dy dz;
- eta wedge d eta = (q_z p_zz-p_z q_zz) dx dy dz;
- d alpha=alpha wedge eta holds exactly when the displayed Frobenius coefficient vanishes.

The signs agree with the candidate and author script. Arbitrary p,q used by the author need not satisfy Frobenius; their equality checks test identities, not actual foliation existence.

For an actual normalized integrable local example, F=z+x z^2+y z^3, D=F_z=1+2xz+3yz^2, and alpha=dF/D have p=z^2/D and q=z^3/D. On any region D>0, alpha(partial_z)=1 and Frobenius holds. Direct quotient differentiation yields density

(-6z^2-16xz^3-(8x^2+18y)z^4-12xy z^5)/D^4.

In particular it is -6z^2 on x=y=0. A nonzero local density is not a global GV certificate: alpha is a local rescaling of exact dF and its local GV form is exact. The independent rational Taylor-jet control checks actual integrable examples, this formula, and affine compression, with explicit failure checks for dz+x dy and a zero denominator. These are finite consistency tests; the formulas above are the general derivation.

For a positive compression z=(t-a)/ell with ell>0, alpha_new=ell h*alpha and eta_new=h*eta. Derivatives give d alpha_new=alpha_new wedge eta_new, and the top form pulls back with its required 1/ell Jacobian. Its integral over the compressed slab is unchanged by the oriented change of variables. ell=0 is undefined, and ell<0 reverses orientation; the construction uses only ell>0. Every finite N admits positive widths, for example the explicit separated rational slabs in the script. No infinite stack or limiting foliation is required. Derivatives can grow with N without violating smoothness for each finite N; no uniform derivative hypothesis appears in the target.

Gauge check: for alpha'=f alpha with f>0, eta'=eta-d log f satisfies d alpha'=alpha' wedge eta'. Its GV change is -d(log f d eta). Changing eta to eta+h alpha changes GV by d(h alpha wedge eta), since alpha wedge d eta=0 follows from d^2 alpha=0. Thus the closed integral is invariant. On a relative block these boundary terms vanish when eta=0 on fixed collars and rescalings preserve the prescribed collar forms. The candidate uses this stronger collar situation rather than assuming arbitrary relative GV integrals are invariant.

## Independently inspected global assembly

Conditional on the cited nonzero compactly supported suspension block, I found no algebraic or elementary gluing obstruction:

1. Finitely many compactly supported increasing generator maps have a common compact support interval, preserved by all words. After compactifying to [0,1], endpoint collars have exactly identity holonomy, with all derivatives fixed.
2. Averaging increasing local fiber coordinates with base partition-of-unity weights gives a positive fiber derivative and the common endpoint coordinate. This supplies a smooth interval-bundle trivialization relative collars, without turning the interior foliation into a product foliation.
3. In this trivialization normalize alpha(V)=1. Frobenius and contraction give d alpha=alpha wedge i_V d alpha, and eta=0 on product collars. Constant positive affine rescaling glues alpha to dt and eta to zero, so the global GV integral adds with positive orientation.
4. A suspension leaf projects onto the connected closed base by path lifting, because holonomy maps are diffeomorphisms of the whole compact interval. Thus it meets every chosen interval fiber. Boundary leaves and leaves in intervening product slabs meet the same vertical circle. A monodromy representative fixing a base disk closes this circle smoothly. This is a genuine geometric tautness argument, not a finite test or a Reebless substitution.
5. The fixed manifold is independent of N. Hyperbolization and existence of the nonzero smooth compact-support suspension are theorem-level obligations, not numerical outputs.

The exact remaining mathematical dependency at this seal is verification that Tsuboi's actual primary statements and commutative diagram supply the indicated nonzero suspension on a trivial oriented interval/circle bundle, with the required homology and regularity conventions. Pseudo-Anosov mapping-torus hyperbolization must also be checked in the cited primary text. If those inputs match, the assembly appears sufficient for the printed target. This is not a novelty/prior-art certificate.

## Initial executable reproduction

Author verify.py and CANDIDATE.md were copied byte-for-byte to a private own directory before execution. Source hashes are respectively 49dfe680fa2a6a7ee796ccf579b716274d01df5576850ba84b7748a9eba187b4 and 28d66c68f4497b1b2a3476d3f858902e8def73e65357320a743da43cb0564c6f. The fresh author execution returned exit 0 and 2660 assertions. The independent control returned exit 0 and 58 checks. Full exact argv, UTC clocks, exit statuses, stdout/stderr, and bindings are in receipts. No stored PASS was accepted as reproduction.

A control weakness is already visible: author check() uses Python assert, so -O removes its enforcing statements while incrementing the reported assertion count. Printed hashes are provenance information, not expected-digest gates. Adversarial optimization, scientific-input and source corruption will be tested only after this first seal. These checks do not certify global existence or tautness, and the author's scope disclaimer correctly says so.

Review completion estimate: 40%; the mathematical validity judgment remains provisional pending actual dependency reading and adversarial controls.
