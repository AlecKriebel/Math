"""Independent exact walk counts: rational coefficients, partitions, and direct paths."""
from fractions import Fraction as F
from math import factorial, comb
from itertools import product
from collections import Counter
import json


def need(ok, why):
    if not ok:
        raise ArithmeticError(why)


def coefficient_counts(d, m, bound):
    need(d >= 1 and m >= 0 and bound >= 0, 'domain')
    base = [F(1, factorial(j)**2) for j in range(bound+1)]
    a = [F(1)] + [F(0)]*bound
    for unused in range(d-1):
        a = [sum(a[k]*base[j-k] for k in range(j+1)) for j in range(bound+1)]
    endpoint = [F(1, factorial(k)*factorial(m+k)) for k in range(bound+1)]
    counts = []
    for r in range(bound+1):
        value = factorial(m+2*r)*sum(endpoint[k]*a[r-k] for k in range(r+1))
        need(value.denominator == 1, 'multinomial integrality')
        counts.append(value.numerator)
    return counts, a


def partitions(s, largest=None):
    if s == 0:
        yield ()
    else:
        for j in range(min(s, largest if largest is not None else s), 0, -1):
            for rest in partitions(s-j, j):
                yield (j,) + rest


def histogram_count(d, m, r):
    total = 0
    n, transverse = m+2*r, d-1
    for first_negative in range(r+1):
        s = r-first_negative
        composition_total = 0
        for part in partitions(s):
            k = len(part)
            if k > transverse:
                continue
            multiplicities = Counter(part)
            label_den = factorial(transverse-k)
            for count in multiplicities.values():
                label_den *= factorial(count)
            labels, rem = divmod(factorial(transverse), label_den)
            need(rem == 0, 'coordinate-label integrality')
            composition_total += labels
            den = factorial(first_negative)*factorial(m+first_negative)
            for j in part:
                den *= factorial(j)**2
            count, rem = divmod(factorial(n), den)
            need(rem == 0, 'time-order multinomial integrality')
            total += labels*count
        target = (int(s == 0) if transverse == 0 else comb(s+transverse-1, transverse-1))
        need(composition_total == target, 'partition completeness against weak compositions')
    return total


def direct_layers(d, maxn, absorbing=None):
    origin = (0,)*d
    layer = {origin: 1}
    layers = [layer]
    for n in range(maxn):
        nxt = Counter()
        for state, count in layer.items():
            if state == absorbing:
                continue
            for i, sign in product(range(d), [-1, 1]):
                point = list(state)
                point[i] += sign
                nxt[tuple(point)] += count
        layer = dict(nxt)
        if absorbing is None:
            need(sum(layer.values()) == (2*d)**(n+1), 'direct layer total mass')
        layers.append(layer)
    return layers


def count_at(d, m, n):
    if n < abs(m) or (n-m)%2:
        return 0
    return coefficient_counts(d, abs(m), (n-abs(m))//2)[0][-1]


def is_valley(counts, multiplier):
    return multiplier*counts[0] > counts[1] and counts[2] > multiplier*counts[1]


def main():
    counts, transverse = coefficient_counts(26,17,26)
    target = counts[24:27]
    need(target == [histogram_count(26,17,r) for r in [24,25,26]], 'independent histogram count')
    expected = [
        472771905154760476735080239062089851901956874836451641200273716209080628940936220800,
        1278150092304717629532379079186301753285243215753138416912978330730296859707833144726912,
        3456384842264444627112655114583494162563305352377408768216137840217183860729498596697993728]
    need(target == expected, 'published three-count certificate')
    need(coefficient_counts(26,17,30)[0][24:27] == target, 'exact truncation stability')
    small_checks = 0
    for d in [1,2,3]:
        layers = direct_layers(d,9)
        for n in range(10):
            for m in range(12):
                direct = layers[n].get((m,)+(0,)*(d-1),0)
                got = count_at(d,m,n)
                need(direct == got, 'direct occupation kernel')
                if n >= m and (n-m)%2 == 0:
                    need(histogram_count(d,m,(n-m)//2) == got, 'small histogram')
                small_checks += 1
    differences = [2704*target[0]-target[1], target[2]-2704*target[1]]
    need(all(x > 0 for x in differences), 'strict valley')
    ratios = [F(target[1],2704*target[0]), F(target[2],2704*target[1])]
    need(F(999823,10**6) < ratios[0] < F(999824,10**6), 'first rational enclosure')
    need(F(1000077,10**6) < ratios[1] < F(1000078,10**6), 'second rational enclosure')
    controls = []
    def control(name, ok):
        need(ok,'control '+name)
        controls.append(name)
    control('single_step_normalization_does_not_give_valley', not is_valley(target,52))
    control('unsupported_even_times_are_zero', all(count_at(26,17,n)==0 for n in [64,66,68]))
    control('changed_endpoint_parity_invalidates_odd_times', all(count_at(26,16,n)==0 for n in [65,67,69]))
    control('dimension_one_positive_foil_is_not_this_valley', not is_valley([count_at(1,17,n) for n in [65,67,69]],4))
    control('wrong_dimension_changes_exact_certificate', count_at(25,17,65) != target[0])
    omitted = factorial(69)*F(1,factorial(17))*transverse[26]
    control('omitting_highest_coefficient_strictly_changes_W69', omitted > 0 and target[2]-omitted != target[2])
    control('count_and_probability_orders_differ', target[0]<target[1]<target[2] and ratios[0]<1<ratios[1])
    ordinary = direct_layers(1,3)[3][(1,)]
    first_passage = direct_layers(1,3,absorbing=(1,))[3][(1,)]
    control('occupation_is_not_first_passage', ordinary==3 and first_passage==1)
    control('origin_has_empty_walk_boundary', count_at(1,0,0)==1 and count_at(3,0,1)==0)
    control('initial_supported_parity_zeros_do_not_remove_valley', count_at(26,17,15)==0 and is_valley(target,2704))
    control('endpoint_reflection_preserves_counts', count_at(26,-17,65)==target[0])
    print(json.dumps({'schema':'independent-pr1311-exact-v1','status':'PASS','dimension':26,
        'endpoint':17,'times':[65,67,69],'counts':target,'positive_differences':differences,
        'denominator_per_step':52,'two_step_multiplier':2704,
        'direct_small_checks':small_checks,'controls':controls,'control_count':len(controls),
        'methods':['rational exponential-generating coefficients','partition histograms','direct neighbor path propagation'],
        'no_floating_point_authority':True,'author_programs_executed':False},sort_keys=True,indent=2))


if __name__ == '__main__':
    main()
