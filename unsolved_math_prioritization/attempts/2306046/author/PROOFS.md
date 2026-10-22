# Elementary mathematical controls

These are authored, self-contained scope and sharpness checks. They do not reconstruct Leung's theorem for an arbitrary member of S*.

## 1. A normalized starlike two-pole family

For complex numbers γ,ζ with |γ|=|ζ|=1 put

    F_(γ,ζ)(z) = z / ((1-γz)(1-ζz)),   |z|<1.

The denominator does not vanish in D, so F is holomorphic, F(0)=0 and F'(0)=1. If F(z)=F(w), cross multiplication gives

    (z-w)(1-γζzw)=0.

Because |γζzw|<1, necessarily z=w. Thus F is injective.

Its logarithmic derivative satisfies, with the removable value 1 at zero,

    zF'(z)/F(z) = (1-γζz²)/((1-γz)(1-ζz))
                 = 1/2 [(1+γz)/(1-γz) + (1+ζz)/(1-ζz)].

For any |u|<1,

    Re((1+u)/(1-u)) = (1-|u|²)/|1-u|² > 0.

Thus Re(zF'/F)>0 throughout D. Here is a direct geometric justification that this proves starlikeness for this already-injective F. Fix 0<r<1. The image of |z|=r is a simple closed curve, since F is injective on a neighborhood of the closed radius-r disk. F has one zero there, simple at zero. The argument principle therefore makes a continuous argument of F(re^(it)) increase by 2π in one circuit. Its derivative is Re(zF'(z)/F(z))>0. Consequently the curve has exactly one intersection with each ray from zero and bounds a region consisting of the radial segments from zero to those intersections. Injectivity and the argument principle identify that region with F({|z|<r}). It is starlike. Every point of F(D) belongs to one of these regions, so their increasing union F(D) is starlike as well. Hence F_(γ,ζ) belongs to S*.

## 2. Exact coefficient inequality within that family

Expansion of the two geometric series gives

    a_n = sum_(j=0)^(n-1) γ^j ζ^(n-1-j),  n≥1.

Equivalently a_0=0, a_1=1 and a_(n+1)=(γ+ζ)a_n-γζa_(n-1). Choose real θ,φ with γ=exp(i(θ+φ)), ζ=exp(i(θ-φ)). If sin φ≠0, geometric summation gives

    |a_n| = |sin(nφ)| / |sin φ|.

The addition formula implies

    |sin((n+1)φ)| ≤ |sin(nφ)| |cos φ| + |cos(nφ)| |sin φ|
                  ≤ |sin(nφ)| + |sin φ|.

Applying the same formula backward, to sin(nφ)=sin((n+1)φ)cos φ-cos((n+1)φ)sin φ, gives the reversed inequality. Therefore

    ||sin((n+1)φ)| - |sin(nφ)|| ≤ |sin φ|,

and division proves ||a_(n+1)|-|a_n||≤1 for every n≥1 in this family. If sin φ=0, γ=ζ and a_n=nγ^(n-1), so equality holds for every n. This handles the coincident-pole case without dividing by zero.

This proves the full estimate only for the explicitly defined family. The proof makes no claim that all normalized starlike functions have two poles or this coefficient form.

## 3. Three exact sharpness sequences

All three maps below belong to the two-pole family, so the preceding analytic, injectivity and starlikeness proofs apply.

1. γ=ζ=1: F(z)=z/(1-z)² has a_n=n. Thus |a_(n+1)|-|a_n|=1 for every n≥1. No smaller universal upper constant is possible.
2. γ=1, ζ=-1: F(z)=z/(1-z²). The coefficients are a_n=1 for odd n and a_n=0 for even n. The signed difference of moduli is -1 for odd n and +1 for even n. Both endpoints occur, and the outer absolute value is indispensable.
3. γ=exp(2πi/3), ζ=exp(-2πi/3): F(z)=z/(1+z+z²)=z(1-z)/(1-z³). Its coefficient pattern is a_(3k+1)=1, a_(3k+2)=-1, a_(3k+3)=0. The signed differences are 0,-1,+1 periodically. This checks that neither coefficients nor their moduli need be monotone, and that consecutive coefficients can have opposite phase. In particular |a_2-a_1|=2, so replacing the difference of moduli by the modulus of the difference would make a false assertion in the very same normalized starlike class.

The identity map f(z)=z is also normalized and starlike. Its difference at n=1 is -1, and at n≥2 is zero. Thus the n=1 quantifier is meaningful, including functions with a_2=0.

## 4. Normalization and rotation

If f is as in the target and θ is real, g(z)=exp(-iθ)f(exp(iθ)z) is normalized, injective and starlike. Its coefficient b_n=exp(i(n-1)θ)a_n has |b_n|=|a_n|. The target quantity is therefore rotation invariant.

Normalization f'(0)=1 is essential for the constant 1. For any real c>1, h(z)=c z/(1-z)² is analytic, injective, vanishes at zero, and has a starlike image, but h'(0)=c and |a_(n+1)(h)|-|a_n(h)|=c>1. Thus one cannot remove the derivative normalization while leaving the bound unchanged.

## 5. Exact algebraic test for the finite controls

For complex x,y, write A=|x|²≥0 and B=|y|²≥0. Then

    ||x|-|y|| ≤ 1

is equivalent to A+B-2sqrt(AB)≤1. Let T=A+B-1. If T≤0, the inequality holds. If T>0, it holds exactly when T²≤4AB, because both sides of T≤2sqrt(AB) are nonnegative. The verifier uses this criterion with rational A and B, so it never rounds a square root or a coefficient modulus.

All finite tests are controls of these arguments and their implementation. Their finite range does not establish any universal statement beyond what is proved above, and does not check the proof of Leung's theorem.
