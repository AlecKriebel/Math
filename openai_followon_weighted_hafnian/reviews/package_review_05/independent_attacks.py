"""Bounded independent attacks on current v5 implementation and reproducer."""
from pathlib import Path
from fractions import Fraction as F
from itertools import combinations, product
from collections import Counter
from functools import lru_cache
import datetime, hashlib, json, subprocess, sys

HERE = Path(__file__).resolve().parent
E = HERE / "extracted"
sys.path.insert(0, str(E / "code"))
import gadget as g
import sampling as s

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def independent_count(graph, removed=()):
    """Pair the least surviving vertex, independently of reference helper."""
    edges = frozenset(graph.edges)
    @lru_cache(None)
    def visit(vertices):
        if not vertices:
            return 1
        if len(vertices) % 2:
            return 0
        a, rest = vertices[0], vertices[1:]
        return sum(visit(tuple(x for x in rest if x != b))
                   for b in rest if (min(a,b), max(a,b)) in edges)
    return visit(tuple(v for v in range(graph.order) if v not in removed))

def main():
    reports = {"timestamp_utc": datetime.datetime.now(datetime.timezone.utc).isoformat()}
    signatures=[]
    for weight in [65, 66, 85, 127, 128, 129, 255]:
        gadget = g.integer_gadget(weight)
        observed=tuple(independent_count(gadget.graph, removed)
                       for removed in [(), (0,1), (0,), (1,)])
        assert observed == (weight,1,0,0)
        assert gadget.graph.order == 4*weight.bit_length()-2
        signatures.append({"weight":weight,"observed":observed})
    reports["additional_signatures"]=signatures
    # Nonbipartite original support, every fiber, and shared terminal orientations.
    values=[F(2,3),F(1,2),F(3,2),F(1),F(2),F(1,3)]
    pairs=list(combinations(range(4),2))
    matrix=[[F(0) for _ in range(4)] for _ in range(4)]
    for (a,b),v in zip(pairs,values):matrix[a][b]=matrix[b][a]=v
    expansion=g.expand_rational_matrix(matrix)
    fibers=Counter(expansion.project(m) for m in g.enumerate_perfect_matchings(expansion.graph))
    expected={}
    for m in g.enumerate_perfect_matchings(g.Graph(4,tuple(pairs))):
        canonical=tuple(sorted(m));w=1
        for edge in m:w*=expansion.integer_weights[edge]
        expected[canonical]=w
    assert dict(fibers)==expected
    assert sum(fibers.values())==g.exact_hafnian(matrix)*expansion.denominator**2
    assert independent_count(expansion.graph)==sum(fibers.values())
    # Certificate rejection (duplicate vertices, incomplete and foreign edges).
    good=next(g.enumerate_perfect_matchings(expansion.graph))
    malformed=[good[:-1], good+(good[0],), good+((0,expansion.graph.order+3),)]
    for m in malformed:
        try:expansion.project(m)
        except ValueError:pass
        else:raise AssertionError("Malformed projection certificate accepted")
    reports["rational_nonbipartite_fibers"]={"D":expansion.denominator,"expanded_order":expansion.graph.order,"count":sum(fibers.values()),"fibers":[{"matching":k,"count":v} for k,v in sorted(fibers.items())],"invalid_certificates_rejected":3}
    # Integrate actual imperative K4 sampler with arbitrary nonnegative failed
    # estimates, not only the zero failures of the packaged suite.
    graph=s.Graph.make(range(4),pairs);eta=F(1,2);par=s.parameters(4,eta)
    target=s.uniform_law(graph);law_results=[]
    for failure_mode in ["zero","huge","tiny","mixed"]:
        law={};executions=0
        for fails in product([False,True],repeat=3):
            mass=par.call_failure**sum(fails)*(1-par.call_failure)**(3-sum(fails))
            estimates=[]
            for i,failed in enumerate(fails):
                if not failed: estimates.append(1+(-1 if i%2 else 1)*par.relative_error)
                elif failure_mode=="zero": estimates.append(F(0))
                elif failure_mode=="huge": estimates.append(F(1<<256))
                elif failure_mode=="tiny": estimates.append(F(1,1<<256))
                else: estimates.append([F(0),F(1<<256),F(1,1<<256)][i])
            for draw in range(1<<par.bits_per_draw):
                iterator=iter(estimates);stats=s.Stats()
                result=s.sample_perfect_matching(graph,eta,lambda *_: next(iterator),s.exact_witness,lambda _:draw,stats)
                assert result in target
                assert stats.count_calls<=par.call_cap and stats.witness_calls<=par.call_cap+1
                assert stats.random_bits<=par.pairs*par.bits_per_draw
                law[result]=law.get(result,F(0))+mass/F(1<<par.bits_per_draw)
                executions+=1
        assert sum(law.values())==1
        tv=s.total_variation(law,target)
        bound=par.pairs*par.relative_error/(1-par.relative_error)+par.call_cap*par.call_failure+F(par.call_cap,1<<par.bits_per_draw)
        assert tv<=bound<eta
        law_results.append({"failure_mode":failure_mode,"TV":str(tv),"bound":str(bound),"executions":executions})
    reports["arbitrary_failed_estimate_laws"]=law_results
    # Fixed-bit mass lost by tiny probabilities, internal zeros preserved.
    w=(F(1,1<<4096),F(0),F(1<<4096),F(0),F(1,1<<4096))
    q=tuple(x/sum(w) for x in w);dy=s.rounded_probabilities(w,11)
    tv=sum(abs(a-b) for a,b in zip(q,dy))/2
    assert dy[1]==dy[3]==0 and sum(dy)==1 and tv<F(len(w)-1,1<<11)
    reports["tiny_rounding"]={"bits":11,"zero_outcomes_preserved":True,"TV_below_boundary_budget":True}
    # Pertinent receipt overwrite boundaries, while original bytes stay intact.
    manifest=json.loads((E/"PAYLOAD_SHA256.json").read_bytes())
    initial={p:sha(E/p) for p in manifest};initial["PAYLOAD_SHA256.json"]=sha(E/"PAYLOAD_SHA256.json")
    symlink=E/"review05-symlink-alias";hardlink=E/"review05-hardlink-alias"
    symlink.symlink_to(E/"main.tex");hardlink.hardlink_to(E/"paper.pdf")
    paths=["main.tex","PAYLOAD_SHA256.json",symlink.name,hardlink.name,"absent-parent/receipt.json","data"]
    boundaries=[]
    try:
        for path in paths:
            cmd=[sys.executable,"reproduce.py","--output",path]
            r=subprocess.run(cmd,cwd=E,capture_output=True,text=True)
            assert r.returncode!=0
            assert all(sha(E/p)==h for p,h in initial.items())
            boundaries.append({"command":cmd,"returncode":r.returncode,"stderr":r.stderr})
    finally:
        symlink.unlink();hardlink.unlink()
    reports["receipt_boundary_rejections"]=boundaries
    reports["payload_bytes_intact"]=True
    reports["limits"]="Bounded finite falsification attempts support the proof; do not certify upstream FPRAS or universal priority absence."
    (HERE/"INDEPENDENT_ATTACKS.json").write_text(json.dumps(reports,indent=2)+"\n")
    print(json.dumps({"status":"passed","signatures":len(signatures),"arbitrary_failed_laws":len(law_results),"boundary_rejections":len(boundaries)}))

if __name__ == "__main__":main()
