"""Full private executable replay, nested bindings and read-only queue projection."""
import datetime, difflib, hashlib, json, pathlib, subprocess, sys, time

HERE=pathlib.Path(__file__).resolve().parent
ROOT=HERE.parents[3]
ORIGINAL='421c6aa90eace49c8659f9a96e83c24fe1b5b901'
PKG='unsolved_math_prioritization/attempts/6600013'
QUEUE='unsolved_math_prioritization/QUEUE.md'
P=HERE/'.private/original'/PKG
sha=lambda b:hashlib.sha256(b).hexdigest()
utc=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat()
git=lambda *a:subprocess.check_output(['git',*a],cwd=ROOT)

def binding_checks():
    entries=[]
    for f in sorted(P.rglob('*MANIFEST.json')):
        j=json.loads(f.read_text())
        if f.name=='SOURCE_MANIFEST.json':continue
        for e in j['files']:
            b=(f.parent/e['path']).read_bytes()
            entries.append({'manifest':str(f.relative_to(P)),'path':e['path'],'bytes':len(b),'sha256':sha(b),'match':len(b)==e['bytes'] and sha(b)==e['sha256']})
    remote=json.loads((P/'final_review/REMOTE_BINDING.json').read_text());author=[]
    for e in remote['files']:
        b=(P/e['path']).read_bytes();blob=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
        author.append({'path':e['path'],'original_blob':git('rev-parse',f'{ORIGINAL}:{PKG}/{e["path"]}').decode().strip(),'bound_blob':e['sha'],'computed_blob':blob,'size':len(b),'match':len(b)==e['size'] and blob==e['sha']})
    review=json.loads((P/'final_review/REVIEW_MANIFEST.json').read_text())
    author_paths={e['path'] for e in remote['files']};review_paths={'final_review/'+e['path'] for e in review['files']}|{'final_review/REVIEW_MANIFEST.json'}
    snap=json.loads((HERE.parent/'snapshot_manifest.json').read_text());snapshot=[]
    for e in snap['files']:
        b=(HERE.parent/'snapshot'/e['path']).read_bytes()
        snapshot.append({'path':e['path'],'bytes':len(b),'sha256':sha(b),'match':sha(b)==e['sha256'] and len(b)==e['bytes'] and b==git('show',f'{ORIGINAL}:{e["path"]}')})
    publication=json.loads((P/'PUBLICATION_MANIFEST.json').read_text())
    assert publication['author_manifest_sha256']==sha((P/'FINAL_FROZEN_MANIFEST.json').read_bytes())
    assert publication['review_manifest_sha256']==sha((P/'final_review/REVIEW_MANIFEST.json').read_bytes())
    assert len(author_paths)==44 and len(review_paths)==9
    assert all(e['match'] for e in entries+author+snapshot)
    states=[]
    for k in range(1,6):
        state=json.loads((P/f'TURN_{k}_STATE.json').read_text())
        ledger=[json.loads(s) for s in (P/f'TURN_{k}_LEDGER.jsonl').read_text().splitlines()]
        states.append({'turn':k,'state':state,'ledger_entries':len(ledger),'ledger':ledger})
    result={'utc':utc(),'nested_bindings':entries,'nested_bindings_count':len(entries),'author_historical_and_final_entries':sum(e['manifest'].startswith('TURN_') or e['manifest']=='FINAL_FROZEN_MANIFEST.json' for e in entries),'author_Git_bindings':author,'preserved_original_author_count':len(author_paths),'preserved_original_review_count':len(review_paths),'snapshot_bindings':snapshot,'state_and_ledger_data':states,'publication_cross_links_match':True}
    (HERE/'PACKAGE_BINDING_RECEIPT.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'binding_count':len(entries),'author_manifest_entries':result['author_historical_and_final_entries'],'author_files':44,'review_files':9,'all_58_snapshot_preserved':True}),flush=True)

def run_replays():
    outdir=HERE/'replays';outdir.mkdir(exist_ok=True);receipts=[]
    jobs=[(f'verify_turn{k}',f'verify_turn{k}.py',[],f'TURN_{k}_CHECKS.json') for k in range(1,6)]
    jobs += [('author_all','REPLAY_ALL.py',[],None),('historical_independent','final_review/independent_checks.py',[],'final_review/INDEPENDENT_CHECKS.json'),('historical_review','final_review/verify_review.py',['--author',str(P)],None),('public_review','verify_review.py',[],None)]
    jobs += [(f'helper_{name}',f'{name}.py',[],None) for name in ['cochain_images','cyclic_cover','quadratic_rotation','rational_linear','rectangular_complex','thue_morse_language']]
    for label,path,args,expected in jobs:
        script=P/path;start=utc();clock=time.monotonic();cmd=[sys.executable,str(script),*args]
        r=subprocess.run(cmd,cwd=P,capture_output=True)
        (outdir/f'{label}.stdout').write_bytes(r.stdout);(outdir/f'{label}.stderr').write_bytes(r.stderr)
        receipt={'label':label,'script':path,'script_sha256':sha(script.read_bytes()),'argv':cmd,'start_utc':start,'end_utc':utc(),'elapsed_seconds':time.monotonic()-clock,'exit':r.returncode,'stdout_bytes':len(r.stdout),'stdout_sha256':sha(r.stdout),'stderr_bytes':len(r.stderr),'stderr_sha256':sha(r.stderr)}
        if expected:
            b=(P/expected).read_bytes();receipt.update(expected=expected,expected_sha256=sha(b),byte_exact=r.stdout==b)
        if label in ['author_all','historical_review','public_review']:
            receipt['parsed_stdout']=json.loads(r.stdout)
            assert receipt['parsed_stdout']['primary_source_pdfs_verified']==0
        receipts.append(receipt)
        (HERE/'REPLAY_RECEIPTS.json').write_text(json.dumps({'runtime':sys.executable,'runtime_version':sys.version,'utc':utc(),'jobs':receipts},indent=2)+'\n')
        assert r.returncode==0 and r.stderr==b'',receipt
        assert receipt.get('byte_exact',True),receipt
        print(json.dumps({'completed':label,'exit':r.returncode,'stdout_bytes':len(r.stdout),'byte_exact':receipt.get('byte_exact')}),flush=True)
    assert len(receipts)==15
    return receipts

def queue_projection():
    head=git('rev-parse','HEAD').decode().strip();main=git('show',f'{head}:{QUEUE}');work=(ROOT/QUEUE).read_bytes();frozen=git('show',f'{ORIGINAL}:{QUEUE}')
    lines=main.splitlines(keepends=True);idx=next(i for i,s in enumerate(lines) if b'6600013 / AMR-065-0013' in s);old=lines[idx]
    assert b'| 407 |' in old
    target=old.replace(b'| queued | 0/5 |',b'| unsolved | 5/5 |')
    # If parent already processed it during audit, the projection remains idempotent.
    assert b'| unsolved | 5/5 |' in target
    lines[idx]=target;projected=b''.join(lines)
    (HERE/'.private/QUEUE_projected.md').write_bytes(projected)
    (HERE/'QUEUE_PROJECTION.diff').write_text(''.join(difflib.unified_diff(main.decode().splitlines(True),projected.decode().splitlines(True),fromfile='current-main/QUEUE.md',tofile='read-only-projection/QUEUE.md')))
    current_map={s.split(b'|')[2].strip():s for s in main.splitlines() if s.startswith(b'| ') and b' / ' in s}
    frozen_map={s.split(b'|')[2].strip():s for s in frozen.splitlines() if s.startswith(b'| ') and b' / ' in s}
    differences=[k.decode() for k in current_map if k!=b'6600013 / AMR-065-0013' and frozen_map.get(k)!=current_map[k]]
    projected_lines=projected.splitlines(keepends=True)
    assert len(projected_lines)==len(main.splitlines(keepends=True))
    assert all(a==b for i,(a,b) in enumerate(zip(main.splitlines(keepends=True),projected_lines)) if i!=idx)
    result={'utc':utc(),'main_head':head,'main_queue_sha256':sha(main),'worktree_queue_sha256':sha(work),'worktree_matches_main':work==main,'original_queue_sha256':sha(frozen),'projection_sha256':sha(projected),'row_rank':407,'line_one_based':idx+1,'current_target_row':old.decode().rstrip(),'projected_target_row':target.decode().rstrip(),'every_other_mainline_byte_preserved':True,'stale_original_non_target_rows_changed':differences,'projection_written_to_shared_queue':False,'services_checked':False}
    inventory=json.loads((HERE.parents[2]/'inventory.json').read_text())
    # Existing inventory is documentary evidence only; no hosting-service action/check here.
    result['prior_inventory_records']=[x for x in inventory.get('queue',inventory.get('drafts',inventory.get('prs',[]))) if x.get('number') in [384,383]]
    if not result['prior_inventory_records']:
        def scan(v):
            if isinstance(v,list):
                for a in v:yield from scan(a)
            elif isinstance(v,dict):
                if v.get('number') in [384,383]:yield v
                else:
                    for a in v.values():yield from scan(a)
        result['prior_inventory_records']=list(scan(inventory))
    (HERE/'QUEUE_RECEIPT.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'queue_main_head':head,'worktree_matches_main':work==main,'stale_original_non_target_rows':len(differences),'projection_target_only':True}),flush=True)

if __name__=='__main__':
    binding_checks();run_replays();queue_projection()
