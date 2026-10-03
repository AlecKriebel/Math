#!/usr/bin/env python3
"""Exact finite image certificates; no faithfulness assumption or external packages."""
import json

def reduce_word(word):
    out = []
    for x in word:
        if out and out[-1] == -x:
            out.pop()
        else:
            out.append(x)
    return tuple(out)

def inverse_word(word):
    return tuple(-x for x in word[::-1])

def substitute(word, automorphism):
    return reduce_word(y for x in word for y in
                       (automorphism[x-1] if x > 0 else inverse_word(automorphism[-x-1])))

def multiply(left, right):
    return tuple(substitute(word, left) for word in right)

IDENTITY = tuple((i,) for i in range(1, 5))

def sigma(i, inverse=False):
    out = list(IDENTITY)
    if inverse:
        out[i-1] = (i+1,)
        out[i] = (-(i+1), i, i+1)
    else:
        out[i-1] = (i, i+1, -i)
        out[i] = (i,)
    return tuple(out)

def braid(word):
    result = IDENTITY
    for x in word:
        result = multiply(result, sigma(abs(x), x < 0))
    return result

A, B, C = (2,), (3,), (1, 1, 2, 3, -2, -1, -1)
WORDS = {'a': A, 'b': B, 'c': C,
         'd': inverse_word(B)+A+B, 'e': inverse_word(C)+B+C,
         'f': inverse_word(A)+C+A, 'p': A+B, 'q': B+C, 'r': C+A}
WORDS.update({k.upper(): inverse_word(w) for k, w in list(WORDS.items())})
GENERATORS = {k: braid(w) for k, w in WORDS.items()}

def evaluate(word):
    result = IDENTITY
    for k in word:
        result = multiply(result, GENERATORS[k])
    return result

def invert(word):
    return ''.join(k.swapcase() for k in word[::-1])

def image_ball(radius):
    result = {IDENTITY: ''}
    for depth in range(radius):
        for value, word in list(result.items()):
            if len(word) != depth:
                continue
            for label, generator in GENERATORS.items():
                result.setdefault(multiply(value, generator), word+label)
    return result

def run():
    # Each generator/inverse really is invertible, and all defining A relations hold.
    for i in range(1, 4):
        assert multiply(sigma(i), sigma(i, True)) == IDENTITY
        assert multiply(sigma(i, True), sigma(i)) == IDENTITY
    for u, v in [('a', 'b'), ('b', 'c'), ('c', 'a')]:
        assert evaluate(u+v+u) == evaluate(v+u+v)
    for row in [('ab', 'bd', 'da', 'p'), ('bc', 'ce', 'eb', 'q'), ('ca', 'af', 'fc', 'r')]:
        assert len({evaluate(word) for word in row}) == 1
    assert len(image_ball(1)) == 19
    results = []
    for radius in (1, 2, 3):
        ball = image_ball(radius)
        g, h = 'a'*(2*radius), 'p'*(2*radius)
        gi, hi = evaluate(invert(g)), evaluate(invert(h))
        ng = [word for value, word in ball.items() if multiply(gi, value) in ball]
        nh = [word for value, word in ball.items() if multiply(hi, value) in ball]
        assert ng == ['a'*radius], ng
        assert nh == ['p'*radius], nh
        # Explicit image-level controls; no uniqueness claim in A at radii 2 or 3.
        assert evaluate('a'*radius) != evaluate('p'*radius)
        triple_images = {value for value in ball
                         if multiply(gi, value) in ball and multiply(hi, value) in ball}
        assert not triple_images, triple_images
        # Exact equalities in A are independently derived in the accompanying proof.
        connecting_word = ('bad'*(2*radius//3+1))[:2*radius]
        assert evaluate(invert(g)+h) == evaluate(connecting_word)
        results.append({'radius': radius, 'image_ball_size': len(ball),
                        'centers': ['', g, h],
                        'common_first_second_image_words': ng,
                        'common_first_third_image_words': nh,
                        'triple_intersection': [],
                        'pairwise_witnesses': ['a'*radius, 'p'*radius,
                                               g+connecting_word[:radius]],
                        'connecting_word': connecting_word})
    print(json.dumps({'all_assertions_passed': True, 'certificate': results}, indent=2))

if __name__ == '__main__':
    run()
