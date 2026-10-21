# Checkable protocol and theorem-transfer derivations

These deductions were made in the current recheck from the supplied exact DFC generator and the recovered Allerton model. They are not claims of historical discovery. Coordinates are (a,b,x,y), D=x+y+1, N=a+b+x+y.

## A simple exact DFC partial-load result

Let V=2(a+b)+x+y. Each arrival adds 2; each of the four download/completion transitions subtracts 1. Thus

    QV = 2 lambda - R,
    R = [a(x+1)+b(y+1)+x(y+1)+y(x+1)]/D
      = [N+ax+by+2xy]/D
      >= N/D >= N/(N+1).

For any fixed 0<lambda<1/2 let delta=(1-2lambda)/2. Outside the finite set with N+1<=1/delta, QV<=-delta. V has finite sublevel sets. Together with nonexplosion and irreducibility, the classical continuous-time Foster criterion gives positive recurrence. Nonexplosion itself follows since only constant-rate arrivals increase N and all other jumps either preserve or decrease N; each peer makes at most two download jumps. Irreducibility follows from positive seed-assisted downloads/departures, Poisson arrivals of either committed type, and positive finite paths through zero. The bound proves nothing at lambda=1/2 or above.

This calculation gives a concrete reason to frame the substantive all-load theorem as an extension beyond a simple small-load argument. It does not identify an earlier published DFC partial-load theorem. No claim that even small-load DFC was historically unresolved is justified by a failed literature search.

## Allerton Common Chunk is a different process

The recovered Allerton 2012 paper, Section II, samples uniformly with replacement from the whole population including empties and the permanent seed. For k=2, at a state with just one singleton X and the seed, all three sampled peers carry X. The singleton can complete iff at least one sampled peer is the seed, so its rate is 1-(1/2)^3=7/8. DFC has rate x(y+1)/D=1/2 at (0,0,1,0).

At a state with one empty peer and the seed, a first download is allowed iff exactly one of three samples is the seed. Its total rate is 3(1/2)^3=3/8. DFC has total first-download rate 1 at (1,0,0,0). The ratio 7/4 of completion rates differs from the ratio 3/8 of first-download rates. Therefore even a constant global time change cannot identify these generators. Constant positive arrival rates also prohibit a nonconstant common clock multiplier from preserving the target generator.

With M empties and no singletons, Common Chunk's total first-download intensity is 3M^3/(M+1)^3<3; DFC's intensity is M. This seed-upload capacity distinction persists for arbitrary M. Forgetting latent first choices does not fix it: states (2,0,1,0) and (0,2,1,0) have the same (a+b,x,y), but rates of the jump to (a+b-1,x+1,y) are 2 and 0. The aggregate is not a strong Markov lump.

## Allerton's operative Lyapunov function is not already a DFC certificate

The Allerton high-load proof uses

    L = C sum_i(S-S_i) + sum_i S exp(-S_i) + S exp(-S_0).

For two chunks evaluated on DFC counts, put S=a+b+x+y+1, S_0=a+b, S_X=x+1, S_Y=y+1. Then sum_i(S-S_i)=V. Let r=exp(-1), G=S[r^(x+1)+r^(y+1)+r^(a+b)], so L=CV+G.

Consider lambda=1 and (a,b,x,y)=(1,0,M,1). The first A download and Y departure each have rate c=(M+1)/(M+2); X departure has rate 2M/(M+2). Both kinds of arrival have the same change in G and sum to rate 1. The respective G differences are

    arrival: r^(M+1)+(M+5)r^2-(M+3)r;
    A first: (M+3)[r^(M+1)(r-1)+1-r];
    X exit:  (M+2)r^M-(M+3)r^(M+1)-r^2-r;
    Y exit: -r^(M+1)+(M+1)r-(M+3)r^2.

Dividing their rate-weighted sum by M and taking M to infinity gives

    (r^2-r)+(1-r)+0+(r-r^2) = 1-r > 0.

Moreover QV=-2+6/(M+2), so C QV/M tends to zero for every finite C. Hence

    lim_(M->infinity) Q_DFC L(1,0,M,1)/M = 1-exp(-1) > 0.

The Allerton function therefore fails the required negative drift for DFC at lambda=1, independently of the finite choice of C. In the published Common Chunk process, the rare singleton's departure is restricted; that operative mechanism is absent in DFC. This rules out this direct theorem/function transfer, not every possible new adaptation of Allerton's ideas.

## Other clock and seed qualifications

A state-dependent acceleration preserves jump probabilities but can change positive recurrence through the expected return-cycle holding times. Therefore polynomializing DFC by multiplying its generator by D is not a recurrence equivalence without an integrability argument. Similarly, fixed-capacity seed theorems cannot be applied merely because the target has one permanent seed: at (M,0,0,0), DFC's seed supplies M downloads per unit time. A bounded-upload model has no such rate for any fixed capacity parameter. These are structural exclusions, not a proof that no comparison theorem could ever be built.

## Controls

identity_controls.py independently enumerates the 64 three-sample outcomes and checks the displayed witnesses, seed bound and exact DFC drift lower bound on 4096 states. Its deliberate false Common-Chunk=DFC assertion rejects with exit 1. theorem_transfer_control.py evaluates the last analytic limit at M=10000,100000,1000000 with the Allerton k=2 constant C=864e; all three drifts are positive. The universal conclusions above rely on the displayed algebra and limiting argument, not on the finite grids or floating-point checks. Neither control proves the candidate's hard all-load theorem or a worldwide historical absence statement.
