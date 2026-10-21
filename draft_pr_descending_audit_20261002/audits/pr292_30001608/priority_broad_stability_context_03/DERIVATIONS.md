# Independently written operative comparison and checks

These equations are research deductions and source-model identification. They
are not copies of manuscript proof or inherited reviewer conclusions. Prior
familiarity with the exact DFC proof is declared. This bounded context review
does not independently reprove the entire published queueing literature.

## 1. Model and scaling identification

Bramson's model routes arrival-rate1 customers through
(1,b),(2,b),(3,l,a),(3,l,b),(2,a),(1,a), with uniformly chosen l in1..L.
Each a class preempts the b class at its station. The means are

    m1a=3/4, m1b=gamma, m2a=gamma, m2b=3/4,
    m3la=3L/4, m3lb=gamma/L, 0<gamma<1/8.

Consequently rho1=rho2=3/4+gamma<1 and rho3l=3/4+gamma/L^2<1.
State counts alone are Markov because arrivals and service times are exponential,
routing is memoryless and service is preemptive static priority. For fixed L,
the total possible service rate is bounded by a constant independent of total
queue population. The operational fluid scaling is

    (Tbar(t),Zbar(t))=lim (T^zn(t|zn|),Z^zn(t|zn|))/|zn|,
    |zn|->infinity, external arrival rate fixed at1.

Flow balance, capacity and priority-complementarity constrain a fluid model.
The growing model solution proves that these deterministic constraints alone
do not enforce finite-time draining. Section4/10 adds high-probability
stochastic estimates: events H_z with P(H_z)->1 exclude the exceptional middle
queue growth. Therefore the correct primary recurrence bridge is asymptotic
fluid-limit stability, not identification of every model solution with a limit.

The theorem quantifiers are existential examples: for gamma fixed in its stated
interval and L sufficiently large, this chosen network is positive recurrent;
for each L its fluid equations admit a growing solution. There is no theorem
about every positive load of an unrelated four-dimensional peer-contact chain.

## 2. Polling example reconstructed at b=1/3

Use station/service rates

    mu_1^(1)=mu_1^(2)=4/5,
    mu_2^(1)=11/6, mu_2^(2)=7/6,
    lambda_1=lambda_2=1.

Walking times are0, service is exhaustive, input/services exponential.
When both servers first empty station1, the limit keeps an interface branch.
The probability that server1 stays indefinitely at the microscopic queue while
server2 moves is1/10; the symmetric alternative is1/10; both moving has
probability4/5. These probabilities follow from exponential competition and
the survival probability of an arrival-rate1/service-rate4/5 birth-death chain,
as computed in primary Lemma6.2/Corollary6.3. Count-state Markov dynamics also
retain the finite server-mode coordinate; queue counts alone omit necessary
information.

Start with queue mass(Q,0), both servers at station1. Combined service net
drain is3/5, hence station1 empties at t=5Q/3; station2 mass is then5Q/3.
If both move to station2, combined net drain there is2, ending after another
5Q/6 with new station1 mass5Q/6. The multiplier is5/6.
If server1 stays, station2 server2 net drain is1/6. Its phase lasts10Q;
station1 net growth is1/5 and ending mass is2Q. The multiplier is2.
If server2 stays instead, station2 server1 net drain is5/6. Its phase lasts2Q;
ending mass is2Q/5. The multiplier is2/5. Thus the mean regenerative mass
multiplier is

    (4/5)(5/6)+(1/10)2+(1/10)(2/5)=68/75<1.

Every such cycle has duration bounded above by(35/3) times its starting mass.
This is the explicit algebra behind the primary recurrence inequality, not a
substitute for its tightness, uniform integrability, stopping-time closure and
transfer-to-Markov-process theorems. The primary theorem has these hypotheses
and source verifications; its A4 proof is abbreviated and partly left to the
reader. I checked the exhibited parameters and mechanism, not every omitted
general A4 proof case as a new result.

For the branch that always leaves server1 at station1, there are two phases:

    both at station1: (q1',q2')=(-3/5,1),
    split:             (q1',q2')=(1/5,-1/6).

Both give (35q1+24q2)'=3. Starting from(1,0), the weighted mass is35+3t.
Cycle k ends with mass2^k and elapsed time(35/3)(2^k-1); the branch has finite
prefix probability10^(-k)>0. For any fixed horizon only finitely many
interfaces occur because the cycle durations increase geometrically. Thus a
random genuine weak fluid limit follows the growing prefix with positive
probability at every finite horizon. No deterministic T enforces a.s. norm
contraction below1 for this fluid limit.

But the probability of following this branch at every cycle is
lim_k10^(-k)=0. Accordingly the conclusion is failure of a uniform deterministic
time a.s. contraction criterion, not positive probability of never draining.
The primary generalized theorem instead yields a finite random draining time
with a moment greater than1, and Lp stability for some p>1. The coexistence of
these two conclusions is logically consistent. exact_polling_check.py verifies
the displayed rational identities and ten finite prefixes; the arbitrary-k
formulas above are deductions, not conclusions from those ten cases alone.

## 3. DFC generator and different large-system operation

The exact state is(A,B,X,Y), denominator D=X+Y+1. The six rates are

    A arrival: lambda/2; B arrival: lambda/2;
    A->X: A(X+1)/D; B->Y: B(Y+1)/D;
    X departure: X(Y+1)/D; Y departure: Y(X+1)/D.

A,B are invisible waiting-room peers and the permanent seed supplies the1s.
The DFC source's population limit increases ONLY external arrival intensities
by N while taking state/N and fixed time. With strictly positive interior
coordinates, seed contributions vanish and the limiting ODE is

    a'=lambda/2-ax/(x+y), b'=lambda/2-by/(x+y),
    x'=(a-y)x/(x+y),       y'=(b-x)y/(x+y).

For example, dividing A(X+1)/(X+Y+1) at(A,X,Y)=(Na,Nx,Ny) byN tends to
ax/(x+y), whereas dividing the unscaled fixed arrival rate byN would tend to0.
The N multiplier is therefore substantive. If one also accelerated time byN
in DFC, these population-order internal rates would contribute a second N
factor. The fixed-rate server queue scaling is not the DFC scaling.

The original author's Proposition3.5 describes an unbounded equilibrium curve
and an open divergent set for this deterministic ODE. Its Conjecture3.6 concerns
stability of the stochastic DFC system. Stable queueing/model mismatch in1999
does not provide an identity of generators or a proof of DFC recurrence at all
fixed positive lambdas. Conversely, exact DFC recurrence does not make the
concept of stochastic stability differing from fluid-model stability new.

## 4. Claims this audit declines

No proof here of positive probability of an infinite growing polling path;
no assertion all Bramson pathwise limits are stable; no equivalence of fluid
model solutions with true limits; no fixed-lambda time-accelerated DFC
interpretation; no stationarity/large-system limit interchange; no all-load
theorem imported from one service-parameter example; no exact worldwide DFC
firstness or preprint/publication acceptance. These are materially stronger
claims than the acquired evidence establishes.
