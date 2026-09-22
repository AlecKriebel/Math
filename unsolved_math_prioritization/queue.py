#!/usr/bin/env python3
"""Versioned UnsolvedMath triage and research queue; Python 3.10+, stdlib only."""
import argparse, collections, csv, hashlib, json, math, pathlib, re, sqlite3, urllib.request
from datetime import datetime, timezone
ROOT = pathlib.Path(__file__).resolve().parent
REPO = 'ulamai/UnsolvedMath'
STATES = ['queued','exhausted','unreviewed','ready','in_progress','partial','blocked','deferred','candidate_result','independent_verification','verified_solved','already_solved','invalid','duplicate']
def now(): return datetime.now(timezone.utc).isoformat(timespec='seconds')
def source_url(p):
    if p.get('source_url'):return p['source_url']
    match=re.search(r'Source URL:\s*(https?://[^\s<>]+)',p.get('background') or '')
    return match.group(1).rstrip('.,') if match else ''
def digest(x): return hashlib.sha256(x.encode()).hexdigest()
def read(path, default): return json.loads(path.read_text()) if path.exists() else default
def write(path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix+'.tmp'); tmp.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n'); tmp.replace(path)
def connect():
    (ROOT/'cache').mkdir(exist_ok=True)
    db=sqlite3.connect(ROOT/'cache/catalog.sqlite')
    db.execute('CREATE TABLE IF NOT EXISTS records (key TEXT PRIMARY KEY, payload TEXT, report TEXT)')
    return db

def sync(args):
    old=read(ROOT/'manifest.json',{})
    old_catalog={x['id']:x for x in read(ROOT/'catalog.json',[])}
    if args.use_cache and not old: raise ValueError('Cannot establish provenance of unrecorded cache; sync without --use-cache')
    revision=args.revision
    if not revision:
        revision=json.load(urllib.request.urlopen('https://huggingface.co/api/datasets/'+REPO,timeout=60))['sha']
    if not re.fullmatch('[0-9a-f]{40}',revision): raise ValueError('Revision must be an immutable 40-character commit SHA')
    files={}
    for name in ['problems.json','research_results.json']:
        path=ROOT/'cache'/name; path.parent.mkdir(exist_ok=True)
        if not (args.use_cache and path.exists()):
            tmp=path.with_suffix('.download')
            with urllib.request.urlopen(f'https://huggingface.co/datasets/{REPO}/resolve/{revision}/{name}',timeout=120) as src, tmp.open('wb') as dst:
                while chunk:=src.read(1024*1024): dst.write(chunk)
            tmp.replace(path)
        h=hashlib.sha256()
        with path.open('rb') as f:
            while chunk:=f.read(1024*1024): h.update(chunk)
        files[name]={'sha256':h.hexdigest(),'bytes':path.stat().st_size}
        if args.use_cache and old and (old['revision']!=revision or old['files'][name]!=files[name]):
            raise ValueError('Cached files do not match recorded revision; run sync without --use-cache')
    problems=read(ROOT/'cache/problems.json',[]); reports=read(ROOT/'cache/research_results.json',{})
    if not isinstance(problems,list) or not problems or not isinstance(reports,dict): raise ValueError('Unexpected upstream schema')
    keys=[str(p['id']) for p in problems]
    if len(keys)!=len(set(keys)): raise ValueError('Duplicate upstream numeric id; resolve identity before import')
    counts=collections.Counter(p['problem_number'] for p in problems)
    for p in problems:
        if counts[p['problem_number']]>1 and p['problem_number'] in reports: p['_ambiguous_report']=True
    db=connect()
    with db:
        db.execute('DELETE FROM records')
        db.executemany('INSERT INTO records VALUES (?,?,?)',[(str(p['id']),json.dumps(p),json.dumps({} if p.get('_ambiguous_report') else reports.get(p['problem_number'],{}))) for p in problems])
    db.execute('CREATE TABLE IF NOT EXISTS metadata (revision TEXT)')
    db.execute('DELETE FROM metadata'); db.execute('INSERT INTO metadata VALUES (?)',(revision,)); db.commit()
    db.close()
    manifest={'dataset':REPO,'revision':revision,'files':files,'records':len(problems),'license':'CC-BY-4.0 (source materials retain their own terms)'}
    write(ROOT/'manifest.json',manifest)
    rank(None)
    current={x['id']:x for x in read(ROOT/'catalog.json',[]) if x['present']}
    changes={'at':now(),'from_revision':old.get('revision'),'to_revision':revision,
        'added':sorted(current.keys()-old_catalog.keys()),
        'removed':sorted(k for k,v in old_catalog.items() if v.get('present') and k not in current),
        'changed':sorted(k for k in current.keys() & old_catalog.keys() if current[k]['review_hash']!=old_catalog[k].get('review_hash'))}
    write(ROOT/'last_update.json',changes)
    with (ROOT/'update_history.jsonl').open('a') as f:f.write(json.dumps(changes)+'\n')
    print(f'Imported {len(problems)} problems at {revision}')

def score(p,r,cfg):
    s=p.get('statement') or ''; text=(p.get('title','')+' '+s).lower()
    reasons=[]; holds=[]
    statuses=[p.get('status'),p.get('research_classification'),r.get('classification')]
    marker=(p.get('background') or '').split('<!-- LITERATURE-TRIAGE:BEGIN -->')
    if len(marker)>1:
        m=re.search(r'\*\*Status:\*\*\s*(\w+)',marker[-1])
        if m: statuses.append(m.group(1))
    if any(x in ['solved','SOLVED-IN-LITERATURE','SOLVED-BY-YOU'] for x in statuses): holds.append('upstream_resolution_claim')
    if p.get('statement_status') in ['unrecoverable','reconstructed_unverified']: holds.append('statement_repair_required')
    note=r.get('verification_note','')
    if re.search(r'status=(invalid_statement|context_only)',note): holds.append('invalid_or_context_only_report')
    if re.search(r'status=(full_solution|counterexample)',note): holds.append('prior_solution_claim_requires_audit')
    if len(s.strip())<45: holds.append('insufficient_statement_context')
    if p.get('_ambiguous_report'): holds.append('ambiguous_report_join')
    assessment=p.get('literature_assessment') or ''
    if re.search(r'unclear|does not (?:identify|isolate)|cannot be verified|malformed',assessment,re.I): holds.append('upstream_context_warning')
    if re.search(r'^(?:the (?:problem|conjecture|question) (?:is |was |has been )?(?:solved|proved|resolved)|solved\b)',assessment,re.I): holds.append('literature_resolution_claim')
    if p.get('published') is False: holds.append('unpublished')
    level=p.get('difficulty_level_id',3)
    # Low upstream levels frequently encode defaults or bad extractions; never grant a bonus.
    probability=cfg['base_probability']; impact=cfg['base_impact']
    signals={
        'computable_objects':r'\b(graph|graphs|matrix|matrices|polynomial|polynomials|finite group|finite groups|hypergraph|permutation|integer|integers)\b',
        'construction_or_counterexample':r'\b(construct|construction|counterexample|example of|does there exist|is there a)\b',
        'algorithmic_target':r'\b(algorithm|computable|decidable|enumerat|computational)\w*',
        'polynomial_algorithm':r'polynomial[ -]time|strongly polynomial',
        'broad_program':r'\b(classify all|classification of all|develop a theory|characterize all|characterise all)\b',
        'unbounded_asymptotic':r'\b(infinitely many|asymptotic|positive density)\b'
    }
    for name,pat in signals.items():
        if re.search(pat,text):
            probability*=cfg['multipliers'][name]; reasons.append(name)
    if level>=4:
        probability*=cfg['multipliers']['difficulty_'+str(level)]; impact=cfg['impact_by_high_difficulty'][str(level)];reasons.append('upstream_L'+str(level))
    if len(s)>6000: probability*=0.6;reasons.append('long_statement')
    probability=min(probability,0.15)
    validity=0.6 if p.get('statement_status') in ['exact','corrected_verified'] else 0.4
    return dict(impact=impact,p_solve=round(probability,6),p_valid_open=validity,
                reasons=reasons,holds=holds,statement_hash=digest(s),review_hash=digest(json.dumps([p,r],sort_keys=True)))

def require_cache():
    path=ROOT/'cache/catalog.sqlite'; manifest=read(ROOT/'manifest.json',{})
    if not path.exists() or not manifest: raise ValueError('Source cache missing; run sync --revision <manifest SHA> first')
    db=sqlite3.connect(path)
    try:
        revision=db.execute('SELECT revision FROM metadata').fetchone()
        count=db.execute('SELECT count(*) FROM records').fetchone()[0]
        if revision!=(manifest['revision'],) or count!=manifest['records']:raise ValueError('Cache/manifest mismatch; run sync')
    finally: db.close()

def rank(args):
    require_cache()
    cfg=read(ROOT/'policy.json',{}); reviews=read(ROOT/'assessments.json',{}); state=read(ROOT/'state.json',{})
    previous={x['id']:x for x in read(ROOT/'catalog.json',[])}
    db=connect(); rows=[]; seen={}
    for key,raw,report in db.execute('SELECT key,payload,report FROM records ORDER BY key'):
        p=json.loads(raw); r=json.loads(report); a=score(p,r,cfg)
        fingerprint=digest(re.sub(r'\s+',' ',p.get('statement','')).strip())
        duplicate=seen.get(fingerprint) if len(p.get('statement',''))>=45 else None
        seen.setdefault(fingerprint,key)
        if duplicate:a['holds'].append('possible_duplicate_of:'+duplicate)
        review=reviews.get(key,{}); local=state.get(key,{})
        stale=bool(review and review.get('review_hash')!=a['review_hash'])
        if stale:a['holds'].append('assessment_stale')
        if review and not stale:
            for field in ['impact','p_solve','p_valid_open']:
                if field in review:
                    value=review[field]
                    if not isinstance(value,(int,float)) or not math.isfinite(value) or not (0<=value<=1 if field.startswith('p_') else 0<value<=10):raise ValueError('Invalid review score: '+key+' '+field)
                    a[field]=value
            a['reasons'].append('individual_desk_review')
            a['holds']+=review.get('holds',[])
            for hold,evidence in review.get('clear_holds',{}).items():
                if not evidence:raise ValueError('Hold clearance needs evidence')
                a['holds']=[h for h in a['holds'] if h!=hold]
        local_stale=bool(local and local.get('review_hash')!=a['review_hash'])
        if local_stale:a['holds'].append('status_review_stale')
        is_v2=cfg.get('turn_limit')==5
        if is_v2 and (not review or review.get('review_policy')!=cfg['version']):a['holds'].append('five_turn_desk_review_required')
        if cfg.get('exclusion_policy')=='exclude_open_and_resolved' and p.get('status')=='open':a['holds'].append('open_excluded_by_user')
        if review.get('route')=='large_search':a['holds'].append('large_exhaustive_search')
        if is_v2 and review.get('route') not in ['proof','hybrid']:a['holds'].append('no_concrete_proof_route')
        if is_v2 and review.get('decision')!='candidate':a['holds'].append('not_selected_for_five_turn_attempt')
        a['holds']=list(dict.fromkeys(a['holds']))
        default_status=('queued' if review.get('decision')=='candidate' else 'deferred' if review.get('decision') in ['defer','exclude'] else 'unreviewed') if is_v2 else 'unreviewed'
        local_status=local.get('status',default_status)
        turns=local.get('turns_used',0)
        eligible=not a['holds'] and local_status in ['queued','unreviewed','ready'] and turns<cfg.get('turn_limit',1000000)
        proposed=p.get('proposed_year')
        reference_year=cfg.get('age_reference_year',2026)
        age=reference_year-proposed if isinstance(proposed,int) and 1600<=proposed<=reference_year else None
        age_multiplier=1.0
        if cfg.get('age_modifier') and age is not None:
            age_multiplier+=cfg['age_modifier']['maximum_bonus']*min(1,math.log1p(age)/math.log1p(cfg['age_modifier']['saturation_years']))
        base_impact=a['impact'];a['impact']=round(min(10,base_impact*age_multiplier),6)
        value=a['impact']*a['p_solve']*a['p_valid_open']
        rows.append(dict(id=key,problem_number=p['problem_number'],title=p.get('title',''),category=(p.get('category') or {}).get('display_name','Unknown'),
            source_url=source_url(p),upstream_status=p.get('status'),local_status=local_status,
            present=True,eligible=eligible,difficulty=p.get('difficulty_level_id'),proposed_year=proposed,age_years=age,age_multiplier=round(age_multiplier,6),base_impact=base_impact,route=review.get('route'),desk_decision=review.get('decision'),desk_note=review.get('note',''),turns_used=turns,turn_limit=cfg.get('turn_limit'),assessment='desk_review' if review and not stale else 'automatic',
            ev=round(value,8),ev_low=round(a['impact']*a['p_solve']*0.2*max(0,a['p_valid_open']-0.2),8),ev_high=round(a['impact']*min(1,a['p_solve']*3)*min(1,a['p_valid_open']+0.2),8),policy_version=cfg['version'],policy_hash=digest(json.dumps(cfg,sort_keys=True)),**a))
    db.close()
    current_ids=seen_ids(rows)
    for key,p in previous.items():
        if key not in current_ids:
            p.update(present=False,eligible=False,local_status=state.get(key,{}).get('status',p['local_status']));p['holds']=list(set(p['holds']+['removed_upstream']));rows.append(p)
    rows.sort(key=lambda x:(not x['eligible'],-x['ev'],x['id']))
    for i,x in enumerate([x for x in rows if x['eligible']],1):x['rank']=i
    for x in rows:
        if not x['eligible']:x['rank']=None
    write(ROOT/'catalog.json',rows)
    fields=['rank','id','problem_number','title','category','ev','ev_low','ev_high','impact','p_solve','p_valid_open','assessment','local_status','upstream_status','eligible','present','holds','reasons','source_url','difficulty','proposed_year','age_years','age_multiplier','base_impact','route','desk_decision','desk_note','turns_used','turn_limit']
    with (ROOT/'ranking.csv').open('w',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=fields,extrasaction='ignore');writer.writeheader()
        for x in rows:writer.writerow({**x,'holds':'; '.join(x['holds']),'reasons':'; '.join(x['reasons'])})
    top=[x for x in rows if x['eligible']]
    if cfg.get('turn_limit')!=5:top=top[:100]
    lines=['# Prioritized research queue','',f"Source: `{read(ROOT/'manifest.json',{}).get('revision','unknown')}`. Policy: `{cfg['version']}`.",'',
        '**Provisional expected-value ranking. Probabilities are subjective planning assumptions, not measured AI success rates.**',
        f"Budget per problem: {cfg['budget']}. No problem is cleared for research until the readiness checks are recorded.",'',
        f"{len(rows):,} tracked; {sum(x['eligible'] for x in rows):,} eligible for triage; {sum(bool(x['holds']) for x in rows):,} with review holds.",'',
        '| Rank | ID / code | Problem | EV | Difficulty | Proposed | Status | Turns |','|---:|---|---|---:|---:|---:|---|---:|']
    for x in top:lines.append(f"| {x['rank']} | {x['id']} / {x['problem_number']} | {x['title'].replace('|','/')} | {x['ev']:.4f} | {x['difficulty']} | {x['proposed_year'] or 'unknown'} | {x['local_status']} | {x['turns_used']}/{x['turn_limit'] or '—'} |")
    attempted=[x for x in rows if x['id'] in state]
    if attempted:
        lines+=['','## Attempt history','','| ID | Problem | Status | Turns |','|---|---|---|---:|']
        for x in attempted:lines.append(f"| {x['id']} | {x['title'].replace('|','/')} | {x['local_status']} | {x.get('turns_used',state[x['id']].get('turns_used',0))}/{cfg.get('turn_limit','—')} |")
    lines+=['','Equal scores are ties; numeric ID order has no mathematical significance. Scores are subjective priorities, not guarantees of a solution.','Full list: [ranking.csv](ranking.csv). Holds and every score component: [catalog.json](catalog.json).',
        'Individual reasoning and next experiments: [SHORTLIST.md](SHORTLIST.md).']
    (ROOT/'QUEUE.md').write_text('\n'.join(lines)+'\n')
    counts=collections.Counter(h.split(':')[0] for x in rows for h in x['holds'])
    write(ROOT/'summary.json',{'records':len(rows),'eligible':sum(x['eligible'] for x in rows),'holds':dict(counts),'assessed':len(reviews)})
    detail=['# Individual candidate assessments','',
        f"These are desk assessments, not verified readiness decisions. All success estimates are subjective and low-confidence. {len(reviews):,} records have stored individual assessments; the highest-ranked 100 are expanded here. See ranking.csv for every short review.",
        'The live order is in [QUEUE.md](QUEUE.md); these notes include demotions and review holds as well as promising candidates.','']
    for x in sorted([x for x in rows if x['id'] in reviews],key=lambda x:(bool(x['holds']),-x['ev'],x['id']))[:100]:
        a=reviews[x['id']]
        detail += [f"## {x['id']} — {x['title']}",'',
            f"Code: `{x['problem_number']}`. EV: {x['ev']:.4f}; sensitivity range {x['ev_low']:.4f}–{x['ev_high']:.4f}. Impact {x['impact']}/10; assumed full-solution probability {100*x['p_solve']:.2f}%; validity/open/novelty prior {100*x['p_valid_open']:.0f}%.",'',
            '**Why this priority:** '+a.get('rationale','Not recorded'),'',
            '**Exact remaining gap:** '+a.get('remaining_gap','Not recorded'),'',
            '**First check or experiment:** '+a.get('first_experiment','Not recorded'),'',
            '**Holds:** '+('; '.join(x['holds']) or 'None detected; readiness review still required.'),'',
            '**Sources:** '+', '.join(f'[{i+1}]({url})' for i,url in enumerate(a.get('sources',[]))),'']
    (ROOT/'SHORTLIST.md').write_text('\n'.join(detail)+'\n')
    print(f'Ranked {len(rows)} records; {len(top)} shown in QUEUE.md')
def seen_ids(rows): return {x['id'] for x in rows}

def show(args):
    db=connect();row=db.execute('SELECT payload,report FROM records WHERE key=?',(args.id,)).fetchone()
    if not row:raise ValueError('Unknown ID (run sync to restore cache)')
    print(json.dumps({'review_hash':digest(json.dumps([json.loads(row[0]),json.loads(row[1])],sort_keys=True)),'problem':json.loads(row[0]),'prior_research':json.loads(row[1])},ensure_ascii=False,indent=2))

def status(args):
    require_cache()
    catalog={x['id']:x for x in read(ROOT/'catalog.json',[])}
    if args.id not in catalog:raise ValueError('Unknown problem ID')
    row=catalog[args.id];state=read(ROOT/'state.json',{});prior=state.get(args.id,{})
    evidence=read(pathlib.Path(args.evidence),{}) if args.evidence else {}
    if args.status in ['ready','in_progress'] and prior.get('turns_used',0)>=read(ROOT/'policy.json',{}).get('turn_limit',1000000):
        raise ValueError('Five-turn budget exhausted; move to the next problem')
    if args.status in ['ready','in_progress','verified_solved'] and evidence.get('review_hash')!=row['review_hash']:
        raise ValueError('Evidence must contain current review_hash; inspect show output and re-review changed source')
    if args.status in ['ready','in_progress']:
        required=['exact_claim','primary_sources','literature_checked_at','success_test','budget','prior_attempt_gap','duplicate_check']
        if [h for h in row['holds'] if h!='status_review_stale'] or not row['present']:raise ValueError('Resolve review holds before starting')
        if not all(evidence.get(k) for k in required):raise ValueError('Readiness evidence required: '+', '.join(required))
    if args.status=='verified_solved':
        if row['holds'] or not row['present'] or prior.get('review_hash')!=row['review_hash'] or prior.get('status')!='independent_verification' or not all(evidence.get(k) for k in ['proof_artifact','independent_review','novelty_check','exact_claim']):
            raise ValueError('Requires independent_verification state plus proof_artifact, independent_review, novelty_check, exact_claim')
    event=dict(at=now(),id=args.id,status=args.status,note=args.note,evidence=evidence,statement_hash=row['statement_hash'],review_hash=row['review_hash'],turns_used=prior.get('turns_used',0))
    state[args.id]=event;write(ROOT/'state.json',state)
    with (ROOT/'history.jsonl').open('a') as f:f.write(json.dumps(event,ensure_ascii=False)+'\n')
    rank(None)

def record_turn(args):
    require_cache()
    cfg=read(ROOT/'policy.json',{});limit=cfg.get('turn_limit',5)
    state=read(ROOT/'state.json',{});prior=state.get(args.id,{})
    catalog={x['id']:x for x in read(ROOT/'catalog.json',[])}
    if args.id not in catalog:raise ValueError('Unknown ID')
    row=catalog[args.id]
    if prior.get('status') not in ['in_progress','partial']:raise ValueError('Start a reviewed attempt before recording a turn')
    if row['holds'] or prior.get('review_hash')!=row['review_hash']:raise ValueError('Source changed or unresolved review hold')
    count=prior.get('turns_used',0)
    if count>=limit:raise ValueError('Turn budget exhausted')
    count+=1
    result='candidate_result' if args.outcome=='candidate' else ('exhausted' if count>=limit else 'in_progress')
    event={**prior,'at':now(),'id':args.id,'status':result,'note':args.note,'turns_used':count,'event':'proof_attempt_turn'}
    state[args.id]=event;write(ROOT/'state.json',state)
    with (ROOT/'history.jsonl').open('a') as f:f.write(json.dumps(event,ensure_ascii=False)+'\n')
    rank(None)

def assess(args):
    require_cache()
    catalog={x['id']:x for x in read(ROOT/'catalog.json',[])}
    if args.id not in catalog:raise ValueError('Unknown ID')
    entry=read(pathlib.Path(args.file),{})
    if entry.get('review_hash')!=catalog[args.id]['review_hash']:raise ValueError('Assessment must supply matching current review_hash; do not reuse stale files')
    if not all(entry.get(k) for k in ['rationale','remaining_gap','first_experiment','sources']):
        raise ValueError('Assessment needs rationale, remaining_gap, first_experiment, sources')
    for field in ['p_solve','p_valid_open','impact']:
        v=entry.get(field)
        if not isinstance(v,(int,float)) or not math.isfinite(v) or not (0<=v<=1 if field.startswith('p_') else 0<v<=10):raise ValueError('Invalid '+field)
    if any(not v for v in entry.get('clear_holds',{}).values()):raise ValueError('Clearance requires evidence')
    entry.update(reviewed_at=now(),statement_hash=catalog[args.id]['statement_hash'],review_hash=catalog[args.id]['review_hash'])
    assessments=read(ROOT/'assessments.json',{});assessments[args.id]=entry;write(ROOT/'assessments.json',assessments)
    with (ROOT/'assessment_history.jsonl').open('a') as f:f.write(json.dumps({'id':args.id,**entry})+'\n')
    rank(None)

def main():
    parser=argparse.ArgumentParser(description=__doc__);sub=parser.add_subparsers(dest='command',required=True)
    s=sub.add_parser('sync');s.add_argument('--revision');s.add_argument('--use-cache',action='store_true');s.set_defaults(func=sync)
    s=sub.add_parser('rank');s.set_defaults(func=rank)
    s=sub.add_parser('turn');s.add_argument('id');s.add_argument('--note',required=True);s.add_argument('--outcome',choices=['continue','candidate'],default='continue');s.set_defaults(func=record_turn)
    s=sub.add_parser('assess');s.add_argument('id');s.add_argument('--file',required=True);s.set_defaults(func=assess)
    s=sub.add_parser('show');s.add_argument('id');s.set_defaults(func=show)
    s=sub.add_parser('status');s.add_argument('id');s.add_argument('status',choices=STATES);s.add_argument('--note',required=True);s.add_argument('--evidence');s.set_defaults(func=status)
    args=parser.parse_args();args.func(args)
if __name__=='__main__': main()
