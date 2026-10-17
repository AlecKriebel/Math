# Removing lower-level unit-injectivity from the actual bad-U theorem

Shared PASS 3/5, row 1777 / 30005572. **Partial result; the full construction remains unsolved.** This extends the accepted PASS2 theorem to a genuinely additional class of levels. It does not kill a norm kernel, prove the identity on ramified characters, or construct the missing pure-prime-power specialization. No novelty claim is made.

## 1. The extended theorem

Let F be imaginary quadratic, O its integer ring, p >= 7, and q=(pi) a principal prime of norm Q. Write

    N = M q^n,  n >= 1,  (M,q)=1.

Assume that M is **proper**, but do **not** assume that O^times -> (O/M)^times is injective. Assume that the high level N is admissible, so the actual LSSW auxiliary arithmetic map f_{c,N}=c Pi_N exists. The auxiliary ideal c is prime to N. Retain all h ideal-class components and the accepted PASS2 row-lattice and unnormalized dual U* conventions.

Put

    u_A = |{epsilon in O^times : epsilon = 1 mod A}|,
    L_A = F(A),
    d_0 = Q^(n-1)(Q-1).

The admissibility assumption at N says u_N=1. The relative ray degree is

    d = [L_N:L_M] = d_0/u_M.                              (1.1)

**Theorem 1 (actual norm constraint with arbitrary proper M).**

    Cor_{L_N/L_M} f_{c,N}(U*_{q,N}-1) = 0.                (1.2)

**Theorem 2 (actual bad-U equation on inflated components).** If p does not divide d, and chi is a character of the prime-to-p part of Gal(L_N/F) trivial on I=Gal(L_N/L_M), then

    f_{c,N}^chi (U*_{q,N}-1) = 0.                         (1.3)

Since u_M divides 6 and p>=7, p∤d is equivalent to p∤d_0. At every high-level component where the source supplies an invertible auxiliary factor, legitimate cancellation yields the same equation for the existing unaugmented map Pi_N^chi. A separately established compactified map inherits the equation. No new compactification or integral-target theorem is implied.

The difference from PASS2 is precise: **M need only be proper, not admissible.** Neither an unprovided arithmetic map at M nor a theta value at the origin is used. The proof stays over the CM definition field at every lower level and accounts for the otherwise missing unit-stabilizer factor in base change.

## 2. Fixed conventions and the lower geometric maps

On component r, let a=a_r, and let

    Gamma_A^s = { [[a_0,b],[c_0,d_0]] in Aut_O(a ⊕ O), acting on rows:
                  c_0 in A a, d_0 = 1 mod A }.

Thus b lies in a^(-1), c_0 in a, and the determinant is a global unit. At the admissible high level, this strict group and the source's group have the same H_1 with Z_p coefficients: the source group is the product of the strict group with its central unit group of order dividing 6. We make **no such direct-product claim** at a nonadmissible lower level. The geometric argument there uses Gamma_A^s itself.

For N_j=Mq^j, write alpha=diag(1,pi). The high-to-low degeneracies are

    F: gamma -> gamma,
    D: gamma -> alpha^(-1) gamma alpha.

For N_j=Aq, the right cosets defining the accepted dual U* are

    h_t = [[1,0],[ell_t,pi]] = alpha k_t,
    k_t = [[1,0],[ell_t/pi,1]],
    ell_t in N_j a / pi N_j a.

There are Q cosets. If gamma h_t=h_s tau_t, then

    (f U*)(gamma)=sum_t f(tau_t).

This is the exact PASS2 convention; no division by Q and no Artin element at a q-divisible modulus is introduced.

Choose a rational prime l>3 with l=2 mod p, avoiding N, c, the fixed class representatives, and the discriminant, and choose a prime f above l. The degree of f over l is 1 or 2, so

    b_f = |(O/f)^times| = l^e-1

is congruent to 1 or 3 mod p. It is a p-adic unit. Also f is admissible. These conditions can be met by Dirichlet's theorem after removing finitely many primes. Use the source's CM curves E_r over F(f), and their coherent torsion markings, at all levels N_j. Choose the markings so that pi P_{N_j}=P_{N_{j-1}}.

Set K_A=F(Af). Even when A is nonadmissible, the point P_A and all the source's level-A marked torsion are defined over K_A. This follows from the CM setup of source §3.1, which requires admissibility of the **definition modulus f**, not of the torsion modulus A. The additional admissibility of A first appears in §4.1 to descend to F(A).

For every proper A among the N_j, define the **geometric** specialized homomorphism

    g_{c,A}: Gamma_A^s -> K_2(K_A) ⊗ Z_p

by specializing the actual trace-fixed geometric cocycle of source §3.4 at (0,P_A). We do not call this an arithmetic map to K_2(F(A)). Since Gamma_A^s fixes that point, evaluation of the cocycle is a homomorphism into constant coefficients. The source's moving-primitive support argument only requires P_A≠0 and c prime to A. Both hold because A is proper. No injectivity of the unit reduction at A is needed for its definition.

At the admissible high level N, source Proposition 4.1.4 identifies this map with restriction of the actual auxiliary map:

    g_{c,N} = res_{L_N}^{K_N} f_{c,N}.                    (2.1)

Here [K_N:L_N]=b_f is prime to p, so the comparison does not lose p-primary information.

## 3. The entire geometric norm argument survives

We give the dependencies explicitly rather than treating lower admissibility as a cosmetic hypothesis.

### 3.1 One-coordinate trace and supported specialization

The geometric primitive on E_r × E_1 is

    v_c = c theta_r ⊠ E_1[c] + Nc (0) ⊠ c theta_1.

For alpha=id × [pi], the **one-curve** theta normalization and its divisor give

    [pi]_* c theta_1 = c theta_1,
    alpha_* v_c = v_c.

This is not deduced from simultaneous scalar trace invariance alone. It is the same one-coordinate argument as the accepted PASS2 proof.

Choose x in c Hom(E_1,E_r) invertible at the proper lower level A. Use moving matrices mu_A with lower entry x and mu_{Aq} with lower entry pi x. Then

    mu_{Aq} alpha = alpha mu_A.

Every point R over P_A has (pi x)R=xP_A≠0, and R is not c-torsion. Therefore the moved primitive and its relevant translates avoid the entire alpha-fiber. Trace-fixed Gersten exactness over Z[1/30], hence over Z_p, identifies the generic pushforward cocycles. Changes to the source's usual moving representative yield a regular coboundary whose specialization on Gamma_A^s is zero. These statements are independent of u_A.

### 3.2 Fibers over the definition-field composita

Because Af is admissible, CRT gives

    [K_{Aq}:K_A] = Q            if q|A,
    [K_{Aq}:K_A] = Q-1          if q∤A.

The underlying fiber is the same geometric one used in PASS2. For q|A all Q points are primitive Aq-points. For q∤A it consists of the Q-1 primitive Aq-points and the one A-torsion point R_0=pi^(-1)P_A. The primitive points form a single relative ray-field orbit over K_A. Importantly, the unit stabilizers of A have been killed by the retained f-marking, so none of these orbit counts has a division by u_A.

For q∤A, choose a in O prime to Af such that a=pi mod A and a=1 mod f, and let

    sigma_A = Art_{Af}((a)) in Gal(K_A/F(f)).

This is well-defined independently of the chosen a. CM reciprocity identifies its action on P_A with multiplication by pi, so the lower-order point carries sigma_A^(-1). The exact identities are

    Cor_{K_{Aq}/K_A} g_{c,Aq} = g_{c,A} D,                         q|A,    (3.1)
    Cor_{K_{Aq}/K_A} g_{c,Aq} = g_{c,A} D - sigma_A^(-1)g_{c,A}F, q∤A.   (3.2)

They hold on every source component. They are geometric/arithmetic-fiber identities over K_A, and do not require or assert descent of g_{c,A} to L_A.

### 3.3 Cosets and the lower good-prime identity

The accepted PASS2 coset identities use only the strict congruences, strong approximation for the determinant-one lattice, and q∤A for the first step. They remain valid for the present Gamma_A^s:

    g F U*_{q,Aq} = Q g D;
    D U*_{q,Aq} = U*_{q,A} D,                              q|A;
    g D U*_{q,Aq} = g T*_{q,A}D - sigma_A^(-1)g F,          q∤A.        (3.3)

For clarity, in the last identity the missing branch is represented by h_infinity=w alpha=beta delta, where beta=diag(pi,1), w belongs to Gamma_A^s, and delta=beta^(-1)w alpha has bottom-right entry pi mod A. The source's geometric specialization rule makes delta act by sigma_A on the target over K_A. Since Gamma_A^s acts trivially after specialization, the crossed-homomorphism conjugation formula gives exactly sigma_A^(-1)g, with no residual coboundary.

The lower good-prime eigenvalue is

    g_{c,A} T*_{q,A} = (1+Q sigma_A^(-1))g_{c,A}.           (3.4)

It does not require admissibility of A. The source's full geometric Hecke relation and Remark 3.4.2 are established before arithmetic descent. At q∤A their cosets persist upon restriction. In those cosets, the bottom row sends the marked point to pi P_A, so specialization multiplies the constant-coefficient Hecke operator by sigma_A. The motivic eigenvalue Q+[pi]^* specializes to Q+sigma_A. Thus sigma_A gT*=(Q+sigma_A)g, which is (3.4). We do not insert Q+sigma_A directly as the eigenvalue of the dual constant-coefficient operator.

### 3.4 Geometric norm of the defect

At the first q-step, put C=g_{c,M}D-sigma_M^(-1)g_{c,M}F. Equations (3.3)-(3.4) give

    C U* = (1+Q sigma_M^(-1))g_{c,M}D
            -sigma_M^(-1)g_{c,M}F-Q sigma_M^(-1)g_{c,M}D = C.

Together with (3.2), this proves norm-zero at the first step. Equations (3.1) and the second identity of (3.3) propagate it through the q-power tower. Consequently

    Cor_{K_N/K_M} g_{c,N}(U*_{q,N}-1)=0.                  (3.5)

All uses of properness occur in avoiding the support at P_M. None can be replaced by the assertion that the origin is an allowed specialization.

## 4. Exact ray-field bookkeeping with unit stabilizers

This is the additional arithmetic point which the admissible-lower-level proof did not need.

Let V=U_M={epsilon in O^times:epsilon=1 mod M}, so |V|=u_M. Let

    A_q=(O/q^n)^times,    B_f=(O/f)^times.

The ray-class exact sequence and CRT identify

    Gal(K_N/L_M) = (A_q × B_f)/V,                         (4.1)

where V embeds diagonally by its residues. Its projection to B_f is injective because f is admissible. Its projection to A_q is injective because Mq^n=N is admissible. Hence

    Gal(L_N/L_M)=A_q/V_q,
    Gal(K_M/L_M)=B_f/V_f,                                (4.2)

where V_q,V_f denote the images of V, each of order u_M. These are quotient identifications, not claims that the unit subgroup was absent.

Let H_N and H_Mf be the kernels of the two quotient maps in (4.2). In (4.1), H_N is the image of {1}×B_f and H_Mf is the image of A_q×{1}. These two subgroups generate all of Gal(K_N/L_M). Their intersection has order u_M: a class represented by (1,b) also has a representative (a,1) exactly when they differ by a diagonal element of V. Therefore

    L_N ∩ K_M = L_M,
    [K_N:L_N K_M]=u_M.                                   (4.3)

In particular, the generally false equality K_N=L_N K_M is **not used**. The degrees are

    [L_N:L_M]=d_0/u_M,
    [K_M:L_M]=b_f/u_M,
    [K_N:K_M]=d_0,
    [K_N:L_N]=b_f.                                       (4.4)

The norm–restriction base-change identity, with (4.3), is

    Cor_{K_N/K_M} res_{L_N}^{K_N}(z)
       = u_M res_{L_M}^{K_M} Cor_{L_N/L_M}(z).             (4.5)

For completeness, factor through C=L_N K_M. Restriction from C to K_N followed by corestriction multiplies by [K_N:C]=u_M. The Cartesian field square C=L_N K_M, with intersection L_M, supplies the remaining base-change equality. This proves (4.5) on K_2 without an invariants-equal-descent assumption.

Apply (4.5) to each value z=f_{c,N}(U*-1), and use (2.1) and (3.5). Then

    u_M res_{L_M}^{K_M} Cor_{L_N/L_M}(z)=0.

Both u_M and [K_M:L_M]=b_f/u_M are p-adic units. Thus u_M can be cancelled, and restriction to K_M is injective by corestriction composed with restriction. This proves Theorem 1.

## 5. Actual vanishing and auxiliary cancellation

If p∤d, I=Gal(L_N/L_M) is a prime-to-p subgroup. On a source character component chi trivial on I, the entire I-action is trivial, including on any retained class-group p-primary module. Therefore

    res Cor(z)=sum_{g in I} g z = d z.

The p-adic unit d can be cancelled. Applying Theorem 1 proves Theorem 2. This is exactly the accepted norm-injectivity step, now at the correct relative degree d_0/u_M.

At the admissible high level, source Corollary 4.3.2 permits cancellation of a smoothing factor (Nc)^2-R_N(c) on the stipulated nonexceptional character components. That factor commutes with precomposition by U*, so the actual unaugmented high-level equation follows. No auxiliary cancellation at a nonadmissible lower level has been asserted or needed.

## 6. The enlargement is nonempty, and its limits are explicit

For a simple parameter check, take F=Q(i), M=(1+i), q=(3), n=1. Then M is proper and q-free; all four units of Z[i] are 1 mod M, so u_M=4. The high level N=Mq is admissible, Q=9, and

    [F(N):F(M)]=(9-1)/4=2.

For p=7, Theorem 2 applies to every source prime-to-p character inflated from F(M). This example verifies that the additional level range is nonempty; it makes no claim that these particular arithmetic K_2 values are nonzero. More generally, nonadmissible proper moduli lie among divisors of the ideals generated by epsilon-1 for nontrivial global units. The extension is thus a small-lower-level repair, not a claim to remove the major ramification obstructions.

The following restrictions remain:

1. q is principal. Marked nonprincipal CM products have not been assembled into the standard (r,1) tuple here.
2. N is admissible so the high-level map is the actual existing source map. No general small-high-level construction is supplied.
3. M is proper. The pure-prime-power case M=O still has an origin-specialization obstruction.
4. The actual U*=1 identity is only on components inflated from L_M and with p∤d. A nontrivial relative character can lie wholly in the norm kernel; wild q|p depth is not cancelled.
5. No 5-primary argument is made; the proof uses source trace-fixed exactness over Z[1/30] and p>=7.
6. No unrestricted compactification, integer-ring target improvement, or relative theta-symbol formula is obtained.

## 7. Why the stronger attempted routes do not yet prove more

Direct use of the Q high-level cosets still sends the marked primitive point to a lower-order point; summing their actual specializations supplies the proved fiber norm. It does not identify each value in the norm kernel with zero. A geometric Hecke class identity must be checked in the subcomplex regular at the relevant marked orbit before specialization; a generic coboundary meeting that orbit cannot be discarded.

Adding an auxiliary tame level would require both a bad-U identity there on the desired character and a suitable degeneracy-map descent or surjectivity statement. PASS2 does not give the first on characters ramified at q, and no Bianchi substitute for the already known Fukaya–Kato input in the cyclotomic argument has been proved. This note makes no such substitution.

## 8. Sources and verification scope

The baseline is the accepted PASS2 proof, SHA256

    7af38b596ee39ad4447a63eac17ea4c28e0c07177021e4f15277c2b2d5e29e5a.

Source mathematical inputs are Lecouturier–Sharifi–Shih–Wang, *Eisenstein cocycles for imaginary quadratic fields*, especially the CM construction in §3.1, geometric trace-fixed complex and representative in §§3.2–3.4, and the actual high-level descent in Proposition 4.1.4. Public sources:

- https://arxiv.org/pdf/2504.19125v1
- https://www.math.ucla.edu/~sharifi/publ/imagquad.pdf

The retained author PDF and text were inspected. The distinct author manuscript is not called arXiv v2. No third-party source text is reproduced in this deliverable. The mathematical novelty claim is intentionally left open; independent review is required before accepting this extension.
