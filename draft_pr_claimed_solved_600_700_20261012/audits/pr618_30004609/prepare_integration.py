#!/usr/bin/env python3
"""Prepare or push a scoped update to the existing PR without changing checkout.

Remote main is preserved; only this target's attempt and one queue row change.
The existing PR head is retained as a second parent, enabling a non-force push.
"""
import argparse,datetime,hashlib,json,os,pathlib,subprocess,tempfile
A=pathlib.Path(__file__).resolve().parent
REPO=A.parents[2]
PREFIX='unsolved_math_prioritization/attempts/30004609/'
ORIGINAL='cae273cb692bde0a0a73790c3840af8c7eb1eed7'
SCOPE='draft_pr_claimed_solved_600_700_20261012/audits/pr618_30004609'
def git(*args,env=None,input=None):
    return subprocess.check_output(['git',*args],cwd=REPO,env=env,input=input)
def sha(data):return hashlib.sha256(data).hexdigest()
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--doi',required=True);ap.add_argument('--push',action='store_true');args=ap.parse_args()
    assert args.doi.startswith('10.5281/zenodo.') and args.doi.removeprefix('10.5281/zenodo.').isdigit()
    assert git('branch','--show-current').decode().strip()=='main'
    meta=json.loads(subprocess.check_output(['gh','pr','view','618','--json','state,isDraft,headRefOid,headRefName'],cwd=REPO))
    assert meta['state']=='OPEN'
    head=meta['headRefOid'];qpath='unsolved_math_prioritization/QUEUE.md'
    # Never reconstruct over an unreviewed concurrent edit. A later retry may
    # accept only this helper's exact, already-replayed and successfully pushed
    # commit for the same DOI; every other head requires a fresh scoped audit.
    approved_heads={ORIGINAL}
    receipt_path=A/'INTEGRATION_RECEIPT.json'
    if receipt_path.is_file():
        previous=json.loads(receipt_path.read_text())
        if previous.get('pushed') is True and previous.get('doi')==args.doi:
            approved_heads.add(previous['integration_commit'])
    assert head in approved_heads,'unreviewed PR head; stop without overwriting concurrent edits'
    oldqueue=git('show',head+':'+qpath).decode()
    oldrows=[l for l in oldqueue.splitlines() if '| 30004609 / OWR-4990374-015 |' in l]
    assert len(oldrows)==1 and oldrows[0].split('|')[8].strip()=='claimed_solved','live scope gate'
    git('fetch','origin','main')
    base=git('rev-parse','refs/remotes/origin/main').decode().strip()
    # Refuse unknown pre-existing target files on main rather than overwrite work.
    existing=git('ls-tree','-r','--name-only',base,'--',PREFIX).decode().splitlines()
    assert not existing,('target already exists on remote main',existing)
    queue=git('show',base+':'+qpath)
    rows=queue.decode().splitlines(keepends=True)
    matches=[i for i,row in enumerate(rows) if '| 30004609 / OWR-4990374-015 |' in row]
    assert len(matches)==1
    i=matches[0];before=rows[i].rstrip('\n');cells=before.split('|')
    assert cells[8].strip()=='queued','unexpected remote target status'
    cells[8]=' claimed_solved ';cells[9]=' 2/5 '
    cells[11]=f' Accepted full characteristic-zero supersolvability proof; extensively AI-assisted, unrefereed preprint {args.doi}; earlier methods and Ferudun matching result credited, no exhaustive first-priority claim. '
    after='|'.join(cells);rows[i]=after+'\n';newqueue=''.join(rows).encode()
    assert queue.replace((before+'\n').encode(),(after+'\n').encode(),1)==newqueue
    now=datetime.datetime.now(datetime.timezone.utc).isoformat()
    native=A/'native/unsolved_math_prioritization/attempts/30004609'
    out=A/'tmp/integration/unsolved_math_prioritization/attempts/30004609'
    out.mkdir(parents=True,exist_ok=True)
    original_doc=json.loads((native/'PUBLICATION_MANIFEST.json').read_text())
    names=[e['path'] for e in original_doc['files']]
    files={name:(native/name).read_bytes() for name in names}
    notice=f'Current publication assessment ({now}): the full theorem has passed fresh mathematical and priority reviews and two sequential whole-package adversarial reviews. The unrefereed, extensively AI-assisted preprint and exact supporting archive are published at https://doi.org/{args.doi}. Ferudun\'s matching October-12 preprint and the earlier tree/pruning/rank-three results are credited. No exhaustive first-priority or independent-development claim is made. The original October-4 author files remain immutable in independent-audit/inputs/author.zip; historical prose below is superseded by the current paper and priority report.\n\n'
    for name in ['README.md','SOURCE_AUDIT.md']:
        files[name]=(notice+files[name].decode()).encode()
    status=json.loads(files['STATUS.json']);status.update(status='claimed_solved',publication_status='published_unrefereed_preprint',doi=args.doi,current_priority_assessment=notice.strip(),historical_author_packet='independent-audit/inputs/author.zip');files['STATUS.json']=(json.dumps(status,indent=2)+'\n').encode()
    files['RESEARCH_LOG.md']+=f'\n## {now} — accepted preprint publication\n\n{notice}Best-guess completion of full theorem and this publication workflow: 100%; human peer review remains unclaimed. The proof and diagnostic code are unchanged.\n'.encode()
    pub=f'# Accepted unrefereed preprint\n\n{notice}The current paper, supporting ZIP, exact deposit metadata and review receipts are under `{SCOPE}/publication/` and the surrounding audit folder. The DOI is https://doi.org/{args.doi}. The frozen historical author/audit packet is reproduced by `independent-audit/verify_audit.py`; the current attempt is checked by `verify_publication.py`.\n\nCurrent source/priority assessment:\n\n'+(A/'publication/CURRENT_PRIORITY_AND_STATUS.md').read_text()
    files['PUBLICATION.md']=pub.encode()
    wrapper=files['verify_publication.py'].decode()
    start=wrapper.index("    inputs=json.loads(")
    end=wrapper.index("    q=ROOT.parents[1]",start)
    wrapper=wrapper[:start]+"    # Historical author hashes are checked against the immutable author.zip\n    # by the independent audit; current files are covered by this inventory.\n"+wrapper[end:]
    wrapper=wrapper.replace("        assert digest(data)==doc['queue_patch']['after_sha256'] and len(data)==doc['queue_patch']['after_bytes'], 'queue bytes mismatch'\n",'')
    wrapper=wrapper.replace("hits=[l for l in rows if '| 644 | 30004609 /' in l]","hits=[l for l in rows if '| 30004609 / OWR-4990374-015 |' in l]")
    files['verify_publication.py']=wrapper.encode()
    doc=dict(original_doc);doc['files']=[{'path':name,'bytes':len(data),'sha256':sha(data)} for name,data in sorted(files.items())]
    doc.update(base_commit=base,publication_doi=args.doi,historical_candidate_commit=ORIGINAL)
    doc['queue_patch']={'path':qpath,'before_sha256':sha(queue),'after_sha256':sha(newqueue),'before_bytes':len(queue),'after_bytes':len(newqueue),'before_row':before,'after_row':after,'changed_cells':['Status','Turns','Findings'],'all_other_bytes_unchanged':True,'runtime_validation':'Only this row is validated; unrelated queue rows may subsequently evolve.'}
    files['PUBLICATION_MANIFEST.json']=(json.dumps(doc,indent=2)+'\n').encode()
    for name,data in files.items():
        dest=out/name;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(data)
    (out.parents[1]/'QUEUE.md').write_bytes(newqueue)
    python=REPO/'draft_pr_claimed_solved_600_700_20261012/tooling/math-venv/bin/python'
    replay=subprocess.check_output([str(python),str(out/'verify_publication.py')],cwd=out)
    with tempfile.TemporaryDirectory(prefix='pr618-integration-index-') as td:
        env=os.environ.copy();env['GIT_INDEX_FILE']=str(pathlib.Path(td)/'index');git('read-tree',base,env=env)
        for name,data in {qpath:newqueue,**{PREFIX+name:data for name,data in files.items()}}.items():
            oid=git('hash-object','-w','--stdin',input=data).decode().strip()
            git('update-index','--add','--cacheinfo','100644,'+oid+','+name,env=env)
        tree=git('write-tree',env=env).decode().strip()
        changed=git('diff','--name-only',base,tree).decode().splitlines()
        assert all(p==qpath or p.startswith(PREFIX) for p in changed)
        commit=git('commit-tree',tree,'-p',base,'-p',head,input=b'Accept PR618 published supersolvability proof with current attribution and scoped queue update\n').decode().strip()
    receipt={'prepared_utc':now,'main_base':base,'existing_pr_head':head,'integration_commit':commit,'changed_paths':changed,'queue_only_target_row_changed':True,'proof_sha256_unchanged':sha(files['PROOF.md'])==sha((native/'PROOF.md').read_bytes()),'current_attempt_replay':json.loads(replay),'doi':args.doi,'shared_checkout_and_index_untouched':True,'pushed':False}
    if args.push:
        live=json.loads(subprocess.check_output(['gh','pr','view','618','--json','state,headRefOid'],cwd=REPO));assert live['state']=='OPEN' and live['headRefOid']==head
        git('push','origin',commit+':refs/heads/'+meta['headRefName']);receipt['pushed']=True
    (A/'INTEGRATION_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps(receipt,indent=2))
if __name__=='__main__':main()
