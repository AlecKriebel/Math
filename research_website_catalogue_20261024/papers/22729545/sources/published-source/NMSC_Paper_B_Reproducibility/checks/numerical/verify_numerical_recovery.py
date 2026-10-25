#!/usr/bin/env python3
"""Independent exact raw-event regression; imports no project implementation.

All rates are integer multiples of log(2), all durations are integers, and
survival factors are exact Fractions. A prescribed merger density is divided
by log(2); a two-merger density is divided by log(2)^2. This bounded test does
not prove any universal graph or numerical inverse theorem.
"""
import hashlib
import itertools
import json
from collections import defaultdict
from fractions import Fraction as F
from pathlib import Path

if not __debug__:
    raise SystemExit('Verification requires assertions; optimized Python is unsupported.')

HERE = Path(__file__).resolve().parent
MANIFEST = HERE / 'numerical_recovery_manifest.json'


def canon(items):
    return tuple(sorted((tuple(sorted(block)), pop) for block, pop in items))


def add(out, state, mass):
    if mass:
        out[state] += mass


class RawProcess:
    def __init__(self, spec, fixture):
        self.ages = spec['ages']
        self.arcs = [tuple(e) for e in spec['arcs']]
        self.parents = defaultdict(list)
        self.children = defaultdict(list)
        for p, c in self.arcs:
            self.parents[c].append(p)
            self.children[p].append(c)
        self.routing = {v: {p:F(q) for p,q in d.items()}
                        for v,d in spec['routing'].items()}
        for v,d in fixture.get('routing', {}).items():
            self.routing[v] = {p:F(q) for p,q in d.items()}
        self.words = {f'{p}>{c}': [(self.ages[c], spec['default_rate_multiplier'])]
                      for p,c in self.arcs}
        self.words['ANCESTRAL>R'] = [(self.ages['R'], 1)]
        for pop, word in fixture['words'].items():
            self.words[pop] = [tuple(x) for x in word]
        self.boundaries = sorted(set(self.ages.values()) |
                                 {t for word in self.words.values() for t,k in word})

    def rate(self, pop, time):
        return next(k for t,k in reversed(self.words[pop]) if t <= time)

    def survival(self, pop, start, end):
        cuts = sorted({start,end} | {t for t,k in self.words[pop] if start<t<end})
        integral = sum((b-a)*self.rate(pop,a) for a,b in zip(cuts,cuts[1:]))
        assert isinstance(integral, int) and integral >= 0
        return F(1, 2**integral)

    def initial(self, assignment):
        return {canon([((label,), f'{self.parents[taxon][0]}>{taxon}')
                       for label,taxon in assignment.items()]): F(1)}

    def event(self, book, vertex):
        if not self.children[vertex]:
            return book
        incoming_pops = {f'{vertex}>{c}' for c in self.children[vertex]}
        options = ([(f'{p}>{vertex}', weight)
                    for p,weight in self.routing[vertex].items()]
                   if vertex in self.routing else
                   [(f'{self.parents[vertex][0]}>{vertex}'
                     if self.parents[vertex] else f'ANCESTRAL>{vertex}', F(1))])
        out = defaultdict(F)
        for state,mass in book.items():
            choices = [options if pop in incoming_pops else [(pop,F(1))]
                       for block,pop in state]
            for chosen in itertools.product(*choices):
                weight = mass
                for pop,p in chosen:
                    weight *= p
                add(out, canon([(state[i][0], chosen[i][0])
                                for i in range(len(state))]), weight)
        return dict(out)

    def advance(self, book, start, end, end_event=True):
        assert end >= start
        cuts = [t for t in self.boundaries if start<t<=end]
        if not cuts or cuts[-1] != end:
            cuts.append(end)
        current = start
        for stop in cuts:
            out = {}
            for state,mass in book.items():
                counts = defaultdict(int)
                for block,pop in state:
                    counts[pop] += 1
                rate = sum(n*(n-1)//2*self.rate(pop,current)
                           for pop,n in counts.items() if n>=2)
                out[state] = mass*F(1,2**(rate*(stop-current)))
            book = out
            if stop < end or end_event:
                for vertex,t in self.ages.items():
                    if t == stop and self.children[vertex]:
                        book = self.event(book,vertex)
            current = stop
        return book

    def pair_observables(self, book, time):
        q = f = F(0)
        for state,mass in book.items():
            assert len(state) == 2
            if state[0][1] == state[1][1]:
                q += mass
                f += self.rate(state[0][1],time)*mass
        return q,f

    def merge_density(self, book, left, right, time):
        left,right = tuple(sorted(left)),tuple(sorted(right))
        out = defaultdict(F)
        for state,mass in book.items():
            locations = dict(state)
            if left not in locations or right not in locations:
                continue
            pop = locations[left]
            if pop != locations[right]:
                continue
            target = [(block,p) for block,p in state if block not in (left,right)]
            target.append((tuple(sorted(left+right)),pop))
            add(out,canon(target),mass*self.rate(pop,time))
        return dict(out)

    def start_pair(self, labels, time, end_event=True):
        return self.advance(self.initial(labels),0,time,end_event)


def verify(spec, fixture):
    raw = RawProcess(spec,fixture)
    checks = 0
    def eq(actual, expected, label):
        nonlocal checks
        assert actual == expected, (fixture['name'],label,str(actual),str(expected))
        checks += 1

    # Oriented weights from actual pair co-occupancy jumps.
    for labels,time,gamma in [({'x':'x','a':'a'},6,raw.routing['X']['TA']),
                              ({'a':'a','b':'b'},20,raw.routing['V']['U'])]:
        before=raw.start_pair(labels,time,False)
        after=raw.start_pair(labels,time,True)
        q0,_=raw.pair_observables(before,time-1)
        q1,_=raw.pair_observables(after,time)
        eq(q0,F(0),'no earlier-parent co-occupancy')
        eq(q1-q0,gamma,'oriented inheritance jump')

    # Ordinary exposed word from f/q, with b deterministic above U.
    for time in (21,23):
        q,f=raw.pair_observables(raw.start_pair({'b':'b','x':'x'},time),time)
        eq(f/q,F(raw.rate('S>U',time)),'ordinary rate f/q')

    # Two distinct exposed reticulations: actual two-merger scalar densities.
    triples=[('X',{'x1':'x','x2':'x','z':'a'},('x1','x2'), 'z',
              2,6,'TA>X','V>TA',(3,5)),
             ('V',{'a':'a','x':'x','z':'b'},('a','x'), 'z',
              10,20,'U>V','S>U',(11,15,19))]
    for v,assignment,pair,z,h,a1,arm,ordinary,times in triples:
        gamma=raw.routing[v][arm.split('>')[0]]
        before=raw.advance(raw.initial(assignment),0,h,False)
        child_pop=f'{v}>{raw.children[v][0]}'
        q3=sum((mass for state,mass in before.items()
                if dict(state)[(pair[0],)]==child_pop
                and dict(state)[(pair[1],)]==child_pop
                and dict(state)[(z,)]!=child_pop),F(0))
        assert q3>0
        pair_assignment={x:assignment[x] for x in pair}
        pair_before=raw.start_pair(pair_assignment,h,False)
        q,_=raw.pair_observables(pair_before,h-1)
        other_parent=next(p for p in raw.parents[v] if p != arm.split('>')[0])
        arm2=f'{other_parent}>{v}'
        for time in times:
            book=raw.advance(raw.initial(assignment),0,time)
            book=raw.merge_density(book,(pair[0],),(pair[1],),time)
            book=raw.advance(book,time,a1)
            book=raw.merge_density(book,pair,(z,),a1)
            density=sum(book.values(),F(0))
            expected=q3*gamma**2*raw.rate(arm,time)*raw.survival(arm,h,time)*raw.rate(ordinary,a1)
            eq(density,expected,'three-label diagnostic density')
            recovered_g1=density/(q3*gamma**2*raw.rate(ordinary,a1))
            eq(recovered_g1/raw.survival(arm,h,time),F(raw.rate(arm,time)),
               'first arm oriented rate')
            _,fpair=raw.pair_observables(raw.start_pair(pair_assignment,time),time)
            recovered_g2=(fpair/q-gamma**2*recovered_g1)/(1-gamma)**2
            eq(recovered_g2,raw.rate(arm2,time)*raw.survival(arm2,h,time),
               'other arm before earlier parent')

    # Topmost branch V: x may bypass V and enter route 1 at U.
    labels={'a':'a','x':'x'}
    q,_=raw.pair_observables(raw.start_pair(labels,10,False),9)
    gamma=raw.routing['V']['U']
    q2_at20=q*(1-gamma)**2*raw.survival('S>V',10,20)
    qtotal20,_=raw.pair_observables(raw.start_pair(labels,20),20)
    q1_initial=qtotal20-q2_at20
    pure_both_route1=q*gamma**2*raw.survival('U>V',10,20)
    bypass=(1-raw.routing['X']['TA'])*gamma
    eq(q1_initial-pure_both_route1,bypass,'all bypass entrants retained')
    for time in (21,23):
        qtotal,ftotal=raw.pair_observables(raw.start_pair(labels,time),time)
        q1=q1_initial*raw.survival('S>U',20,time)
        q2=qtotal-q1
        eq(q2,q*(1-gamma)**2*raw.survival('S>V',10,time),
           'topmost longer-arm mass after bypass subtraction')
        recovered=(ftotal-raw.rate('S>U',time)*q1)/q2
        eq(recovered,F(raw.rate('S>V',time)),'topmost longer-arm rate')

    # Lower sink X: its route 1 traverses already recovered V before TB.
    labels={'x1':'x','x2':'x'}
    q,_=raw.pair_observables(raw.start_pair(labels,2,False),1)
    p=raw.routing['X']['TA']
    initial=q*p**2*raw.survival('TA>X',2,6)*raw.survival('V>TA',6,10)
    for time in (11,13,15):
        qtotal,ftotal=raw.pair_observables(raw.start_pair(labels,time),time)
        upper_u=initial*gamma**2*raw.survival('U>V',10,time)
        upper_s=initial*(1-gamma)**2*raw.survival('S>V',10,time)
        q1=upper_u+upper_s
        q2=qtotal-q1
        eq(q2,q*(1-p)**2*raw.survival('TB>X',2,time),
           'sink longer-arm mass after ancestral routing subtraction')
        f1=raw.rate('U>V',time)*upper_u+raw.rate('S>V',time)*upper_s
        eq((ftotal-f1)/q2,F(raw.rate('TB>X',time)),
           'sink longer-arm rate with ancestral routing')
    return {'fixture':fixture['name'],'exact_checks':checks,'status':'PASS'}


if __name__=='__main__':
    data=MANIFEST.read_bytes()
    spec=json.loads(data)
    records=[verify(spec,fixture) for fixture in spec['fixtures']]
    output={'claim':'B-REPAIR-NUMERIC-001','manifest_sha256':hashlib.sha256(data).hexdigest(),
            'arithmetic':'fractions; densities scaled by powers of log(2)',
            'fixtures':records,'total_exact_checks':sum(r['exact_checks'] for r in records),
            'status':'PASS','limit':'Bounded exact regression; not a universal proof.'}
    print(json.dumps(output,indent=2,sort_keys=True))
