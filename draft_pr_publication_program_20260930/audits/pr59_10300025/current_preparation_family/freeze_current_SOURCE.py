"""SOURCE-only fixed-index preparation; ROOT custody helpers remain unexecuted."""
from pathlib import Path
import os
import ast
from current_custody_common import N, ref, load, dump, now, need, write_new


def main():
    need(__debug__,'Guard execution required')
    for name in ['INDEX.json','READY.json','ROOT_MANIFEST.json']:
        need(not (N/name).exists() and not (N/name).is_symlink(),'Fresh absent-only index/ready/manifest')
    for p in N.glob('*.py'):ast.parse(p.read_bytes(),filename=p.name)
    attempts=load(N/'current/attempt.json')
    attempts['historical_independent_assertions_passed_qualification']='The20173 count is stored historical evidence, not a replay by the fresh countable reviewer or this preparer.'
    attempts['fresh_review_counts_imported_from_ROOT_receipt']={'countable_exact_assertions':45577,'asymmetric_exact_assertions':5185,'actual_original_author_reproduction':6665}
    (N/'current/attempt.json').write_bytes(dump(attempts))
    (N/'REPORT.md').write_text('# PR59 operative current SOURCE report\n\nQualified disposition already_solved; original budget1/5, one discovery_credit:false turn, no paper. Exact literal theorem survives both fresh universal proof reviews, with both orientations, one common h, all pairs and separate finite element constants. Credited DKNP2013 finite increasing case is sufficient for the historical closed co-oriented formulation. Countable-extension novelty, earliest priority, a uniform group constant and a stronger toroidal/geometric intent are not established.\n\nThis preparation read the complete original proof and both complete fresh proofs/reports plus genuine ROOT adjudication. Their broad exhaustion-mechanism overlap and exact primary-reading limitations are disclosed globally. Root-science writer10500 at17:12:34UTC is actual; current SOURCE/root closure and native acceptance remain unperformed here.\n\nAll23 original science bodies are exact in original_archive. Current proof/code/verification/prior-report/source-provenance bodies are exact copies; current attempt/turn/source-record and PR summary are explicitly annotated derivatives. Dated pending review is superseded for the literal scope. Original QUEUE diff conflicts with old only-attempt wording; source/metadata qualification retains that fact without editing native files. The present non-null raw report object and non-NULL SQL TEXT are inherited actual accounting facts, not placeholders; current annotated catalog fields are not passed off as new raw/SQL values.\n\nThree prior immutable families (140/58/22) and six actual ROOT CAP4 sets are bound in place, full logical bodies/modes/topology and prelaunch/streams checked, with no bulk external copies. This assembly adds no mathematical-review credit, proof turn or discovery. Mathematical checkers are not imported/executed; finite prior counts remain diagnostics, not universal proof certification. Original archive/source families remain unchanged. Two temporary-file failures before launch are recorded; later source writes/checks are separate actual operations.\n\nPreparation100%, novel-discovery0%, publication0%. Current ROOT-only absent-manifest closer and separate reader are source proposals, unexecuted. No ROOT personal approval of this new source, future PID/time, native/Git/index/ref/remote/PR, paper/DOI or outside individual communication is claimed.\n')
    log=N/'RESEARCH_LOG.md'
    log.write_text(log.read_text()+'\n'+now()+' — SOURCE preparation100%; new discovery0%; paper/publication0%. External binder21333 validated245 completed body/mode refs,17 exact directories and6 actual CAP4 sets in place. All23 archive/current mathematical byte joins retained; operative scope/accounting/readiness globally qualified. Own custody helpers syntax parsed only. Preparing fixed0444/0755 source domain and absent-manifest ROOT proposals; no author or adversarial math replay, native/Git/remote or contact.\n')
    for p in N.rglob('*'):
        need(not p.is_symlink(),'No symlinks in own source')
        if p.is_file():os.chmod(p,0o444)
        elif p.is_dir():os.chmod(p,0o755)
    os.chmod(N,0o755)
    rows=[ref(p) for p in sorted(N.rglob('*')) if p.is_file()]
    dirs=[{'path':str(p),'full_mode_07777':'0755'} for p in [N]+sorted(p for p in N.rglob('*') if p.is_dir())]
    index={'schema':'pr59-current-fixed-source-index/v1','files':rows,'directories':dirs,'literal_index_ready_future_manifest_exclusions':['INDEX.json','READY.json','ROOT_MANIFEST.json'],'source_only':True,'ROOT_custody_or_native_acceptance_claimed':False}
    write_new(N/'INDEX.json',dump(index))
    ready={'schema':'pr59-current-SOURCE-ready/v1','utc':now(),'actual_SOURCE_freezer_pid':os.getpid(),'INDEX':ref(N/'INDEX.json'),'prepared_files':len(rows)+2,'directories':len(dirs),'prepared_payload_bytes':sum(z['bytes'] for z in rows),'original_science_files':23,'status':'already_solved','original_budget':'1/5','new_attempts_or_review_credit':0,'paper':False,'native_acceptance':False,'ROOT_MANIFEST_expected_literal_absent':True,'ROOT_helpers_executed':False,'SOURCE_preparation_percent':100,'novel_discovery_percent':0,'stronger_toroidal_geometric_intent_unidentified':True,'publication_or_DOI':False}
    write_new(N/'READY.json',dump(ready))
    print(dump({'status':'CURRENT_SOURCE_READY_ONLY','actual_pid':os.getpid(),'utc':now(),'INDEX':ref(N/'INDEX.json'),'READY':ref(N/'READY.json'),'prepared_files':len(rows)+2,'directories':len(dirs),'source_payload_bytes':sum(z['bytes'] for z in rows),'no_mathematical_checker_or_ROOT_custody_execution':True}).decode(),end='')


if __name__=='__main__':main()
