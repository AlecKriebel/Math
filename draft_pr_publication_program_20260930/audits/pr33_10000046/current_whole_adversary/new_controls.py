"""New full-gate controls, independent of all existing matching implementations.

Exhaust all 3x3 graphs, enumerate their permutation objectives, Hall cuts and
rational doubly stochastic matrices; also enumerate unequal-mass transports.
These controls are finite falsifiers and do not decide the infinite 3D target.
"""
from collections import Counter
from fractions import Fraction as F
from itertools import product, permutations
from pathlib import Path
from copy import deepcopy
import hashlib, json, sqlite3, subprocess

HERE = Path(__file__).resolve().parent
AUDIT = HERE.parent
ROOT = HERE.parents[3]
CANDIDATE = AUDIT / 'reviewed_candidate'
count = 0
def check(ok, label):
    global count
    if not ok:
        raise AssertionError(label)
    count += 1
def sha(b):
    return hashlib.sha256(b).hexdigest()

def hall(edges, n, weighted=None):
    deficits=[]
    for bits in product((0,1), repeat=n):
        a={i for i,b in enumerate(bits) if b}
        neighbours={j for i,j in edges if i in a}
        if weighted:
            p,q=weighted
            deficit=sum(p[i] for i in a)-sum(q[j] for j in neighbours)
        else:
            deficit=len(a)-len(neighbours)
        deficits.append(deficit)
    return max(deficits)

def main():
    # Enumerate every integer matrix with rows/columns 3: rational DS matrices
    # denominator 3. We use no max-flow or matching implementation here.
    rows=[r for r in product(range(4),repeat=3) if sum(r)==3]
    matrices=[]
    for a,b in product(rows,repeat=2):
        c=tuple(3-a[j]-b[j] for j in range(3))
        if min(c)>=0:
            check(sum(c)==3,'last DS row total')
            matrices.append((a,b,c))
    perms=list(permutations(range(3)))
    graph_cases=0
    for bits in product((0,1),repeat=9):
        e={(i,j) for i in range(3) for j in range(3) if bits[3*i+j]}
        objective=max(sum((i,j) in e for i,j in enumerate(p)) for p in perms)
        check(objective==3-hall(e,3),'all-graph permutation/Hall equality')
        for c in matrices:
            check(sum(c[i][j] for i,j in e)<=3*objective,
                  'rational DS objective never exceeds best permutation')
        graph_cases+=1
    # Exhaust all 2x3 allowed relations with integer masses p=(3,3), q=(1,2,3).
    # All integral full transports have row 0 = a, row 1 = q-a.
    cap=(1,2,3)
    flows=[(a,tuple(cap[j]-a[j] for j in range(3)))
           for a in product(*(range(v+1) for v in cap)) if sum(a)==3]
    weighted_cases=0
    for bits in product((0,1),repeat=6):
        e={(i,j) for i in range(2) for j in range(3) if bits[3*i+j]}
        opt=max(sum(c[i][j] for i,j in e) for c in flows)
        check(opt==6-hall(e,2,weighted=((3,3),cap)),
              'all unequal-mass relations exact full-transport/Hall equality')
        weighted_cases+=1
    # Actual cardinality/union countercontrols.
    e={(0,0),(1,1)}
    check(hall(e,2)==0 and hall(e,2,((3,1),(1,3)))==2,
          'equal-label matching differs from weighted transport')
    identity={(i,i) for i in range(3)}
    check(hall(identity,3)==0,'union-neighbourhood identity graph perfect')
    intersection=set.intersection(*[{i} for i in range(3)])
    check(3-len(intersection)==3,'intersection substitution falsely loses all mass')
    # A different nearest-neighbour false marginal control at horizon four.
    # Two different two-step histories end at 0; cross-switch ++ and -- tails.
    fake={w:F(1,16) for w in product((-1,1),repeat=4)}
    for w in [(1,-1,1,1),(-1,1,-1,-1)]: fake[w]+=F(1,32)
    for w in [(1,-1,-1,-1),(-1,1,1,1)]: fake[w]-=F(1,32)
    check(all(m>=0 for m in fake.values()) and sum(fake.values())==1,'fake law valid')
    for t in range(5):
        got=Counter();true=Counter()
        for w,m in fake.items():got[sum(w[:t])]+=m;true[sum(w[:t])]+=F(1,16)
        check(got==true,'fake nearest-neighbour law has correct each-time marginal')
    check(fake[(1,-1,1,1)]==F(3,32)!=F(1,16),'full four-step cylinder law fails')
    # The probability of ++ after the specific +,- history is 3/8, not 1/4.
    check(fake[(1,-1,1,1)]/F(1,4)==F(3,8),'history-conditional increment law fails')
    # Moving events: fixed-prefix convergence is distinct from event N.
    moving=[]
    for n in range(1,9):
        w=list(product((0,1),repeat=n))
        paired=[(a,a[:-1]+(1-a[-1],)) for a in w]
        check(len({b for a,b in paired})==2**n,'moving-bit both word marginals uniform')
        check(all(a[:-1]==b[:-1] and a!=b for a,b in paired),'moving-event discontinuity')
        moving.append({'N':n,'fixed_prefix_below_N_mass':1,'event_at_N_mass':0})
    # Entire current candidate and dependency closure, not only a result exit code.
    m=json.loads((CANDIDATE/'MANIFEST.json').read_text())
    check(sha((CANDIDATE/'MANIFEST.json').read_bytes())=='19b7bd6152f9291814f321a38b7d1ab344da0c39ef060d5c030bbed84c32831c','exact assigned manifest')
    bound=[]
    for member in m['files']:
        raw=(CANDIDATE/member['path']).read_bytes()
        check(len(raw)==member['bytes'] and sha(raw)==member['sha256'],'current exact member')
        bound.append(member['path'])
    dependencies=json.loads((CANDIDATE/'CURRENT_PROOF_DEPENDENCIES.json').read_text())
    for member in dependencies['files']:
        raw=(AUDIT/member['path']).read_bytes()
        check(len(raw)==member['bytes'] and sha(raw)==member['sha256'],'exact dependency member')
        if member['path'].endswith('.json'):json.loads(raw)
    check(len(bound)==27 and len(dependencies['files'])==72,'whole current/dependency counts')
    # Original Git blobs and old hash scope remain bound to archives, not current.
    snap=json.loads((AUDIT/'snapshot_manifest.json').read_text())
    for item in snap['files']:
        raw=(AUDIT/'source_snapshot'/item['path']).read_bytes()
        git=subprocess.check_output(['git','show',snap['head']+':unsolved_math_prioritization/attempts/10000046/'+item['path']],cwd=ROOT)
        check(raw==git and sha(raw)==item['sha256'],'all exact Git original members')
    old=json.loads((CANDIDATE/'review/review_summary.json').read_text())
    check(old['reviewed_sha256']==sha((CANDIDATE/'ORIGINAL_PARTIAL.md').read_bytes()),'old verdict original archive only')
    check(old['reviewed_sha256']!=sha((CANDIDATE/'PARTIAL.md').read_bytes()),'edited bytes require this NEW verdict')
    # Fresh COMPLETE pinned upstream objects and actual SQLite TEXT provenance.
    records=json.loads((HERE/'inputs/problems.json').read_text())
    reports=json.loads((HERE/'inputs/research_results.json').read_text())
    chosen=[x for x in records if x['id']==10000046]
    check(len(chosen)==1 and sum(x['problem_number']=='AMR-099-0046' for x in records)==1,'unique source identity')
    raw=chosen[0];prior=reports['AMR-099-0046']
    augmented={**raw,'research_classification':prior['classification'],'research_summary':prior['result']+' Literature status: '+prior['status_literature']}
    check(augmented==json.loads((CANDIDATE/'source_record.json').read_text()),'whole imported payload equals fresh augmented record')
    check(prior==json.loads((CANDIDATE/'prior_report.json').read_text()),'complete separate report equality')
    ready=json.loads((CANDIDATE/'readiness.json').read_text())
    review_hash=sha(json.dumps([raw,prior],sort_keys=True).encode())
    check(review_hash==ready['review_hash'],'exact raw-plus-separate-prior review hash')
    check(sha(raw['statement'].encode())==ready['statement_hash'],'exact full statement hash')
    db=sqlite3.connect('file:'+str(ROOT/'unsolved_math_prioritization/cache/catalog.sqlite')+'?mode=ro',uri=True)
    db.execute('PRAGMA query_only=ON')
    row=db.execute('SELECT key,payload,report,typeof(key),typeof(payload),typeof(report) FROM records WHERE key=?',('10000046',)).fetchall();db.close()
    check(len(row)==1 and row[0][3:]==('text','text','text'),'real SQLite read-only TEXT identity')
    check(row[0][1]==json.dumps(raw) and row[0][2]==json.dumps(prior),'exact importer serialization')
    # New identity/provenance/ledger controls: catch changes with no finite-math effect.
    def source_bind(p,r,budget=1,turns=(1,)):
        return p==raw and r==prior and sha(json.dumps([p,r],sort_keys=True).encode())==review_hash and budget==1 and turns==(1,)
    check(source_bind(raw,prior),'source binding baseline')
    negatives=[]
    for field,value in [('id',10000047),('problem_number','AMR-099-0047'),('view_count',999),('statement','Synchronous only')]:
        p=deepcopy(raw);p[field]=value
        check(not source_bind(p,prior),'actual whole source mutation rejected');negatives.append(field)
    for r in (None,{},dict(prior,result='Solved')):
        check(not source_bind(raw,r),'missing/invented prior rejected');negatives.append('prior')
    check(not source_bind(raw,prior,budget=0),'reset budget rejected')
    check(not source_bind(raw,prior,turns=(1,2)),'invented turn rejected')
    ledger=[json.loads(s) for s in (CANDIDATE/'turns.jsonl').read_text().splitlines()]
    check([r['turn'] for r in ledger]==[1] and ready['budget']['used_substantive_attempts']==1 and ready['new_attempts']==0,'original1/5 and new0')
    # Header-derived prospective queue changes, all nonselected bytes preserved.
    q=(ROOT/'unsolved_math_prioritization/QUEUE.md').read_bytes()
    patch=json.loads((CANDIDATE/'CURRENT_QUEUE_PATCH.json').read_text())
    check(sha(q)==patch['whole_queue_preimage_sha256'],'current shared queue exact guarded preimage')
    def queue_candidate(data, instruction):
        if sha(data)!=instruction['whole_queue_preimage_sha256']:raise ValueError('whole preimage mismatch')
        lines=data.decode().splitlines(keepends=True)
        hs=[s for s in lines if s.startswith('| Rank |')]
        if len(hs)!=1:raise ValueError('ambiguous header')
        names=[s.strip() for s in hs[0].split('|')[1:-1]]
        if names!=instruction['header_names']:raise ValueError('header mismatch')
        rows=[i for i,s in enumerate(lines) if '10000046 / AMR-099-0046' in s]
        if len(rows)!=1 or lines[rows[0]]!=instruction['row_before']:raise ValueError('target preimage mismatch')
        before=lines[rows[0]].split('|');after=instruction['row_prospective'].split('|')
        if len(before)!=14 or len(after)!=14:raise ValueError('twelve-column row required')
        changed=[names[j-1] for j in range(1,13) if before[j]!=after[j]]
        if changed!=['Status','Turns','Findings']:raise ValueError('unapproved named field change')
        lines[rows[0]]=instruction['row_prospective'];return ''.join(lines).encode()
    new=queue_candidate(q,patch)
    check(sha(new)==patch['whole_queue_prospective_sha256'],'whole prospective queue byte equality')
    check(q.count(patch['row_before'].encode())==1 and new==q.replace(patch['row_before'].encode(),patch['row_prospective'].encode()),'all unrelated queue lines byte preserved')
    queue_negatives=[]
    for name,field,cell in [('chat_corruption','Chat',10),('doi_corruption','DOI',12),('rank_corruption','Rank',1)]:
        bad=deepcopy(patch);cells=bad['row_prospective'].split('|');cells[cell]=' CORRUPTION ';bad['row_prospective']='|'.join(cells)
        try:queue_candidate(q,bad)
        except ValueError:queue_negatives.append(name)
        else:raise AssertionError(name+' accepted')
    for name,bad in [('whole_queue_stale',q+b'\n'),('duplicate_target',q+patch['row_before'].encode())]:
        try:queue_candidate(bad,patch)
        except ValueError:queue_negatives.append(name)
        else:raise AssertionError(name+' accepted')
    # Refuse intentional change of prospective phase into fabricated accepted state.
    status=json.loads((CANDIDATE/'current_status.json').read_text())
    check(status['current_gate'].startswith('pending_NEW') and status['queue_status_proposed']=='unsolved' and not status['full_target_resolved'] and not status['four_dimensional_full_proof_independently_certified'],'honest prospective unsolved status')
    result={'pass':True,'checks':count,'all_3x3_graphs':graph_cases,'rational_DS_matrices':len(matrices),'weighted_2x3_graphs':weighted_cases,'integer_weighted_transports':len(flows),'current_members':len(bound),'dependency_members':len(dependencies['files']),'source_mutations':negatives,'queue_negative_controls':queue_negatives,'moving_event_controls':moving,'false_full_word_probability':'3/32 versus SRW1/16','actual_fresh_source_records':len(records),'review_hash':review_hash,'new_substantive_attempts':0,'scope':'Universal proof independently reconstructed; these are additional finite/tamper controls only. No 3D positivity or full4D proof asserted.'}
    (HERE/'NEW_CONTROLS_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
