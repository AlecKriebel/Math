#!/usr/bin/env python3
"""Verify exact publication bytes and finite regressions; not a global solver."""
PACKS = [{'archive': {'bytes': 16268, 'path': 'equilateral_polygon_2731_author.zip', 'sha256': 'f213feeb58b23c4c98aafb865c5965751386aba27fc64981a9aa92bebf04eca2'}, 'folder': 'author_original', 'inner': 'MANIFEST.json', 'manifest': {'bytes': 1638, 'path': 'AUTHOR_FREEZE_MANIFEST.json', 'sha256': '7b71bde678bba64192812f49058f8cc91d46fa3bfd36f725bbcda86a1f7be4d8'}, 'members': [{'bytes': 2407, 'path': 'ATTEMPT_LOG.md', 'sha256': '1f0156b1317474858c205b7066891933e53ceae70e8d5a4a33aedf8d924958df'}, {'bytes': 1099, 'path': 'EXACT_CHECKS.json', 'sha256': 'de669f167f692bb747f72409fa415539fab6226b0b526e98b5bbc79481648a62'}, {'bytes': 811, 'path': 'EXECUTION_AUDIT.json', 'sha256': '46f2ef29e607766ff1c343a1162c6e6fbc4d5dcda61df431816ab92f4aeddc42'}, {'bytes': 1323, 'path': 'MANIFEST.json', 'sha256': '04fe800d571a4fa0a53e25dc6dd886a5f050b4e2aba92ae7bd1a97a3fd4b5ecf'}, {'bytes': 15451, 'path': 'PROOF_AND_GAPS.md', 'sha256': 'e02f2ca437c05c96c70445c2909dfae342d2a310ca41002660cd8709de96cfa7'}, {'bytes': 1181, 'path': 'REPRODUCE.md', 'sha256': '4ae5bd6744ce23df1472755ce97126ee60dd0c01b105549cd20a7b51b6088d74'}, {'bytes': 7128, 'path': 'SOURCE_AUDIT.json', 'sha256': '8ed8136e58d855807a29444367ca35e8e6cf5040ff541bff91c236c9fc7ad678'}, {'bytes': 600, 'path': 'STATUS.json', 'sha256': '3ebf4b059e82c276281652cea4e93673da94965bdac5f59309f823e4d6baed0f'}, {'bytes': 6474, 'path': 'verify_examples.py', 'sha256': '50ff7e13f7fab9506c03a6eeca74c49eb7ca3459ab75b677131abf254cf78646'}], 'prefix': 'equilateral_polygon_2731/'}, {'archive': {'bytes': 19425, 'path': 'EQUILATERAL_POLYGON_2731_INDEPENDENT_AUDIT_SAFE.zip', 'sha256': '494cd6e9622f64519eb89a528474e8b75dc2b7a65c288747164bffadc4093455'}, 'folder': 'independent_audit', 'inner': 'AUDIT_MANIFEST.json', 'manifest': {'bytes': 1749, 'path': 'EQUILATERAL_POLYGON_2731_INDEPENDENT_AUDIT_EXTERNAL_MANIFEST.json', 'sha256': 'd112e4a98562dc9b908d2e6291362b60d9099a21430c8cdfa1464e0a5d4c2cc9'}, 'members': [{'bytes': 1062, 'path': 'AUDIT_MANIFEST.json', 'sha256': 'a18c33965ed643ba24cdc7c3df2852d854c6ef424bcf203990951741ec36acb9'}, {'bytes': 4200, 'path': 'EXACT_ACCEPTANCE.json', 'sha256': 'b92a86fd7cd84147653a76d4242755da7b74f8c2ef095d83907c4fd7cc5961c5'}, {'bytes': 14769, 'path': 'INDEPENDENT_AUDIT.md', 'sha256': '7b3d07ffd3de9b25f9f80b5aa8291c70f529ca1819619999c3f6e51d58dff008'}, {'bytes': 5953, 'path': 'REPLAY_RESULTS.json', 'sha256': 'e771fb7f130aecf95ba19a995c3c00aa69108aab2e1530cbcfd887b44ea81e10'}, {'bytes': 1856, 'path': 'REPRODUCE_AUDIT.md', 'sha256': 'b10a70b677a2b19903332dc5d2091c0a573b6e3289629617b434b7622e02415d'}, {'bytes': 2193, 'path': 'SOURCE_RECHECK.json', 'sha256': '6d19e65c887f755bc6df1ff20b4f4af17bb97b28d06542bfcd58e369cead2bfd'}, {'bytes': 12655, 'path': 'replay_audit.py', 'sha256': '36cd8d0e600489db20464880f67a1291e0407fb44374d6686b44819f6205a976'}], 'prefix': 'equilateral_polygon_2731_audit/'}]
QUEUE_BASE = {'bytes': 392735, 'sha256': '997c9f9e9e1dff2cf2355606e009ee76cdbf67d1bebbb3fd53116f89647442ee'}
QUEUE_NEW = {'bytes': 392737, 'sha256': '9ef258c0dd788a8de2798b04516f904405805706307ebb0a2475c54e6baf5cde'}
EXPECTED_PUBLIC = ['INDEPENDENT_AUDIT_RECEIPT.json', 'PUBLICATION_MANIFEST.json', 'PUBLICATION_METADATA.json', 'PUBLICATION_TEST_RESULTS.json', 'README.md', 'RESEARCH_LOG.md', 'archives/AUTHOR_FREEZE_MANIFEST.json', 'archives/EQUILATERAL_POLYGON_2731_INDEPENDENT_AUDIT_EXTERNAL_MANIFEST.json', 'archives/EQUILATERAL_POLYGON_2731_INDEPENDENT_AUDIT_SAFE.zip', 'archives/equilateral_polygon_2731_author.zip', 'author_original/ATTEMPT_LOG.md', 'author_original/EXACT_CHECKS.json', 'author_original/EXECUTION_AUDIT.json', 'author_original/MANIFEST.json', 'author_original/PROOF_AND_GAPS.md', 'author_original/REPRODUCE.md', 'author_original/SOURCE_AUDIT.json', 'author_original/STATUS.json', 'author_original/verify_examples.py', 'independent_audit/AUDIT_MANIFEST.json', 'independent_audit/EXACT_ACCEPTANCE.json', 'independent_audit/INDEPENDENT_AUDIT.md', 'independent_audit/REPLAY_RESULTS.json', 'independent_audit/REPRODUCE_AUDIT.md', 'independent_audit/SOURCE_RECHECK.json', 'independent_audit/replay_audit.py', 'test_publication.py', 'verify_publication.py']
import argparse, ast, hashlib, io, json, stat, subprocess, sys, tempfile, zipfile
from pathlib import Path

ROOT=Path(__file__).resolve().parent
H=lambda b:hashlib.sha256(b).hexdigest()
def need(ok,message):
    if not ok:raise ValueError(message)
def pin(data,size,digest,label):
    need((len(data),H(data))==(size,digest),'Byte/hash mismatch: '+label)
def obj(path):return json.loads(path.read_bytes())
def integrity(root):
    actual=set()
    for path in root.rglob('*'):
        need(not path.is_symlink(),'Symlink in publication')
        if path.is_file():actual.add(path.relative_to(root).as_posix())
    need(actual==set(EXPECTED_PUBLIC),'Unexpected or missing publication file')
    pm=obj(root/'PUBLICATION_MANIFEST.json')
    rows=pm['files'];names=[x['path'] for x in rows]
    need(len(names)==len(set(names)),'Duplicate publication manifest entry')
    need(set(names)==actual-{'PUBLICATION_MANIFEST.json'},'Publication manifest inventory mismatch')
    need(pm['problem_id']==2731 and pm['self_excluded'] is True,'Publication manifest scope')
    for row in rows:pin((root/row['path']).read_bytes(),row['bytes'],row['sha256'],row['path'])
    ext=[];zip_member_count=0
    for pack in PACKS:
        a=pack['archive'];m=pack['manifest'];ab=(root/'archives'/a['path']).read_bytes();mb=(root/'archives'/m['path']).read_bytes()
        pin(ab,a['bytes'],a['sha256'],'frozen archive');pin(mb,m['bytes'],m['sha256'],'frozen external manifest')
        em=json.loads(mb);expected={x['path']:x for x in em['files']};ext.append(em)
        need(len(expected)==len(em['files'])==len(pack['members']),'Frozen manifest inventory')
        need(em['files']==pack['members'],'Frozen member identities')
        need(em['archive']['bytes']==a['bytes'] and em['archive']['sha256']==a['sha256'],'External archive binding')
        need(em['archive'].get('path',em['archive'].get('name'))==a['path'],'External archive name')
        with zipfile.ZipFile(io.BytesIO(ab)) as z:
            need(z.testzip() is None,'ZIP CRC')
            names=z.namelist();need(len(names)==len(set(names))==len(expected),'Duplicate or missing ZIP member')
            need(set(names)=={pack['prefix']+n for n in expected},'ZIP exact inventory')
            for name,row in expected.items():
                need(Path(name).name==name and not name.startswith('.'),'Unsafe ZIP member')
                zi=z.getinfo(pack['prefix']+name);mode=zi.external_attr>>16
                need(not stat.S_ISLNK(mode),'ZIP symlink')
                b=z.read(zi);pin(b,row['bytes'],row['sha256'],'ZIP member '+name)
                need((root/pack['folder']/name).read_bytes()==b,'Extracted member mismatch: '+name)
                zip_member_count+=1
        inner=obj(root/pack['folder']/pack['inner']);inner_names=[x['path'] for x in inner['files']]
        need(len(inner_names)==len(set(inner_names)),'Duplicate inner manifest entry')
        need(set(inner_names)==set(expected)-{pack['inner']},'Inner manifest inventory')
        for row in inner['files']:need(row==expected[row['path']],'Inner manifest pin')
    receipt_bytes=(root/'INDEPENDENT_AUDIT_RECEIPT.json').read_bytes()
    pin(receipt_bytes,886,'4ea469bfc188185feb1be950bd58f9020e4861c9bfa1e8a15c5c5058a804c340','Independent receipt')
    receipt=json.loads(receipt_bytes);ac=obj(root/'independent_audit/EXACT_ACCEPTANCE.json')
    need(ac['verdict']=='ACCEPT_EXACT_ORIGINAL_AS_STALLED_PARTIAL','Exact acceptance verdict')
    need(ac['accepted_author_members']==ext[0]['files'],'Acceptance member binding')
    for key,expected in [('accepted_author_archive',PACKS[0]['archive']),('accepted_author_external_manifest',PACKS[0]['manifest'])]:
        need(ac[key]==expected and ext[1][key]==expected,'Acceptance original identity')
    need(receipt['audit_archive']==PACKS[1]['archive'] and receipt['audit_external_manifest']==PACKS[1]['manifest'],'Audit receipt binding')
    for key,name in [('audit_report','INDEPENDENT_AUDIT.md'),('exact_acceptance','EXACT_ACCEPTANCE.json')]:
        need(receipt[key]==next(x for x in ext[1]['files'] if x['path']==name),'Receipt member binding')
    need(receipt['original_archive_unchanged'] is True and receipt['audit_member_count']==7 and receipt['problem_id']==2731,'Receipt identity')
    need(receipt['verdict']==ac['verdict'],'Receipt verdict')
    meta=obj(root/'PUBLICATION_METADATA.json');author=obj(root/'author_original/STATUS.json')
    for record in (ac,meta,author):
        need(record['problem_id']==2731 and record['problem_number']=='KP-1.72' and record['rank']==906,'Target identity')
        need(record['status']=='unsolved' and record['outcome']=='stalled_partial','Unsolved partial scope')
        need(record['turns_used']==3 and record['turn_limit']==5,'Approach count')
        for key in ('full_solution_claimed','novelty_claimed','component_computation_executed'):
            need(record[key] is False,'Forbidden scope flag: '+key)
    for record in (ac,meta):
        for key in ('correction_required','corrected_derivative_created','locked_equilateral_example','universal_unlocking_theorem'):
            need(record[key] is False,'Forbidden acceptance scope: '+key)
    need(ac['author_files_preserved'] is True and ac['author_working_tree_matches_archive'] is True and meta['accepted_original_unchanged'] is True,'Original preservation')
    need(ac['source_pdfs_hashes_verified']==4 and ac['corpus_stream_hashes_verified'] is True,'Full input acceptance')
    need(ac['independent_segment_oracle_comparisons']==61776 and ac['segment_symmetry_comparisons']==4000,'Finite test counts')
    need(ac['checker_mutations_rejected']==12 and ac['input_pin_mutations_rejected']==2,'Negative control counts')
    for key in ('dataset_contents_included','source_documents_included','private_coordination_included'):
        need(ac[key] is False,'Publication exclusion flag')
    q=meta['queue'];need(q['allowed_cells']==q['changed_cells']==['Status','Turns'],'Queue scope')
    need(q['base_sha256']==QUEUE_BASE['sha256'] and q['new_sha256']==QUEUE_NEW['sha256'],'Queue pins')
    need(q['findings_preserved'] is True and q['all_unrelated_bytes_preserved'] is True,'Queue preservation')
    for name in ('verify_publication.py','test_publication.py','author_original/verify_examples.py','independent_audit/replay_audit.py'):
        need(not any(isinstance(node,ast.Assert) for node in ast.walk(ast.parse((root/name).read_text()))),'Removable assertion: '+name)
    return {'status':'PASS','publication_files':len(actual),'frozen_zip_members_verified':zip_member_count,'frozen_archives_verified':2,'original_files_unchanged':True,'exact_acceptance_verified':True,'assert_nodes':0}

def queue_check(base,current):
    b=Path(base).read_bytes();c=Path(current).read_bytes()
    pin(b,QUEUE_BASE['bytes'],QUEUE_BASE['sha256'],'queue base')
    pin(c,QUEUE_NEW['bytes'],QUEUE_NEW['sha256'],'queue current')
    lines=b.splitlines(keepends=True);hits=[i for i,line in enumerate(lines) if line.startswith(b'| 906 | 2731 / KP-1.72 |')]
    need(len(hits)==1,'Queue target count');i=hits[0];cells=lines[i].split(b'|')
    need(cells[8]==b' queued ' and cells[9]==b' 0/5 ','Queue original status')
    cells[8]=b' unsolved ';cells[9]=b' 3/5 ';lines[i]=b'|'.join(cells)
    need(b''.join(lines)==c,'Unrelated queue bytes changed')
    return {'status':'PASS','changed_cells':['Status','Turns'],'all_unrelated_bytes_preserved':True}

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--integrity-only',action='store_true',help='Skip executable finite replays; static identity and scope checks only.')
    for arg in ('catalog','problems','reports','source-dir','queue-base','queue-current'):p.add_argument('--'+arg)
    args=p.parse_args()
    corpus=[args.catalog,args.problems,args.reports]
    need(not any(corpus) or all(corpus),'Supply all three corpus files')
    need(bool(args.queue_base)==bool(args.queue_current),'Supply both queue files')
    need(not args.integrity_only or not(any(corpus) or args.source_dir),'Full input verification requires executable replay')
    out=integrity(ROOT)
    out['queue_verification']=queue_check(args.queue_base,args.queue_current) if args.queue_base else 'SKIPPED: no queue inputs'
    if args.integrity_only:
        out['finite_replay']='SKIPPED: integrity-only mode'
        out['corpus_verification']='SKIPPED';out['source_verification']='SKIPPED'
    else:
        cmd=[str(ROOT/'independent_audit/replay_audit.py'),str(ROOT/'archives'/PACKS[0]['archive']['path']),str(ROOT/'archives'/PACKS[0]['manifest']['path'])]
        for opt in ('catalog','problems','reports','source_dir'):
            value=getattr(args,opt)
            if value:cmd+=['--'+opt.replace('_','-'),str(Path(value).resolve())]
        results=[]
        with tempfile.TemporaryDirectory(prefix='polygon publication working directory ') as work:
            for flags in ([],['-O']):
                run=subprocess.run([sys.executable,'-I','-S','-B',*flags,*cmd],cwd=work,capture_output=True,timeout=120)
                need(run.returncode==0 and not run.stderr,'Independent replay failed')
                results.append(run.stdout)
        need(results[0]==results[1],'Normal/optimized independent replay differs')
        got=json.loads(results[0]);expected=obj(ROOT/'independent_audit/REPLAY_RESULTS.json')
        if not all(corpus):
            expected['full_stream_pins']='not requested';expected.pop('exact_record_verification')
        if not args.source_dir:
            expected['source_pdf_pins']='not requested';expected.pop('source_pdf_page_counts')
        if not(args.source_dir and all(corpus)):expected.pop('normalized_primary_statement')
        # Version metadata is reported separately, not mistaken for arithmetic drift.
        expected['python_version']=sys.version.split()[0]
        need(got==expected,'Replay differs from accepted expected results')
        out['finite_replay']={'status':'PASS','normal_optimized_identical':True,'stdout_bytes':len(results[0]),'stdout_sha256':H(results[0]),'matches_accepted_results_after_declared_optional_input_projection':True,'python_version':sys.version.split()[0],'segment_oracle_comparisons':got['segment_oracle_comparisons'],'segment_symmetry_comparisons':got['segment_symmetry_comparisons'],'checker_mutations_rejected':len(got['checker_mutation_runs']),'input_pin_mutations_rejected':len(got['pinned_input_mutations_rejected'])}
        out['corpus_verification']='PASS: three full pinned streams and exact record/report pair' if all(corpus) else 'SKIPPED: no corpus inputs'
        out['source_verification']='PASS: four pinned PDFs and page counts'+('; normalized statement match' if all(corpus) else '') if args.source_dir else 'SKIPPED: no source inputs'
    out['scope']='Exact frozen bytes, scope flags and finite regression checks only; no global solution or novelty certification.'
    print(json.dumps(out,sort_keys=True,indent=2))

if __name__=='__main__':
    try:main()
    except Exception as e:
        print(json.dumps({'status':'FAIL','error':str(e)},sort_keys=True),file=sys.stderr)
        sys.exit(1)
