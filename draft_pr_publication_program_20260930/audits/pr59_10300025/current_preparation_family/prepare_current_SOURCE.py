"""Own SOURCE assembly only; no author/reviewer-code imports or Git calls."""
from pathlib import Path
import datetime
import hashlib
import json
import os

N=Path(__file__).absolute().parent
A=N.parent
O=A/'original_preparation_family'
S=O/'original'


def put(name,body):
    q=N/name;q.parent.mkdir(parents=True,exist_ok=True)
    with q.open('xb') as f:f.write(body if isinstance(body,bytes) else body.encode())
def dump(name,value):put(name,json.dumps(value,indent=2,sort_keys=True)+'\n')


def main():
    utc=datetime.datetime.now(datetime.timezone.utc).isoformat()
    idx=json.loads((O/'SCIENCE_INDEX.json').read_bytes())
    for name,z in idx.items():
        b=(S/name).read_bytes()
        if len(b)!=z['bytes'] or hashlib.sha256(b).hexdigest()!=z['sha256'] or hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()!=z['git_sha1']:raise ValueError('Original authentication join')
        put('original_archive/'+name,b)
    for name in ['KNOWN_RESULT.md','verify.py','verification.json','prior_report.json','source_provenance.json']:
        put('current/'+name,(S/name).read_bytes())
    put('current/review/INDEPENDENT_REVIEW.md','# Historical review, with operative qualification\n\nThe following is historical review text, not a new review by this preparer. Its20,173 controls are stored historical results; the fresh countable family did not replay that old checker. The later final-hash endorsement and both fresh universal proof reports supersede the dated turn\'s review-pending sentence. Current ROOT adjudication and exact limits are in ../../GLOBAL_QUALIFICATIONS.md.\n\n'+(S/'review/INDEPENDENT_REVIEW.md').read_text())
    attempt=json.loads((S/'attempt.json').read_bytes())
    attempt.update(status='already_solved',recommended_queue_status='already_solved',native_acceptance=False,paper_required=False,novel_result_claimed=False,substantive_attempts_used=1,substantive_attempt_limit=5,current_scientific_adjudication='PASS_LITERAL_KNOWN_RESULT_SCOPE',current_ROOT_scientific_receipt='../../ROOT_SCIENTIFIC_ADJUDICATION_20261003.json',current_SOURCE_preparation_adds_review_credit=0,actual_original_PR_diff_includes_QUEUE=True,shared_queue_modified_field_qualification='Original false field may refer to operator ownership; actual head diff includes QUEUE.md. Current preparation changes no native queue.',historical_geometric_intent_reconstructed=False)
    dump('current/attempt.json',attempt)
    turns=json.loads((S/'turns.json').read_bytes())
    if len(turns)!=1 or turns[0]['turn']!=1 or turns[0]['discovery_credit'] is not False:raise ValueError('Exact original budget')
    turns[0]['historical_remaining_gap']=turns[0]['remaining_gap']
    turns[0]['remaining_gap']='Later final-hash historical review and two fresh universal reviews supersede review pending for the literal condition. Historical toroidal/geometric intent remains unidentified and is not declared solved.'
    turns[0]['operative_qualification']='Annotated original single turn, not a new proof attempt or historical execution receipt.'
    dump('current/turns.json',turns)
    record=json.loads((S/'source_record.json').read_bytes())
    record.update(original_catalog_status=record['status'],status='already_solved',research_classification='ALREADY-SOLVED-LITERAL',research_summary='Literal common-topological-conjugacy per-element condition verified for all countable line-homeomorphism families, both orientations. Credited DKNP2013 finite increasing case; no novelty or earliest-priority claim. Stronger historical toroidal/geometric intent remains unidentified. No paper, native acceptance or publication by this SOURCE task.',operative_SOURCE_qualification='Annotated derivative of the archived unwrapped catalog problem object, not a new raw/SQL read. Original published:true refers to the catalog entry, not a paper. Raw original report is a present non-null object; original SQL report is non-NULL TEXT.')
    dump('current/source_record.json',record)
    put('INITIAL_SCOPE.md','# PR59 current SOURCE\n\n'+utc+' — Consolidate the ROOT-closed original and two fresh reviews into a lean already_solved1/5 partial-result packet. Both proof/report bodies and ROOT receipt read before synthesis. Preserve23 original scientific bodies exactly. No new mathematical review/attempt credit, native acceptance, paper, Git/remote or individual outreach. Broad countable-exhaustion mechanism overlap is disclosed.\n')
    put('RESEARCH_LOG.md','# PR59 current SOURCE research log\n\n'+utc+' — Preparation20%; new discovery0%; paper/publication0%. Read complete original proof, source/accounting fields, both complete fresh universal proof/report bodies and ROOT receipt. Archive23 exact joins verified; current math/code/raw-report unchanged. Metadata annotates superseded pending review and actual QUEUE diff. No author/reviewer code imported or executed by this preparer.\n')
    put('PREPARATION_FAILURES.md','# Actual source failures\n\nTwo initial here-document invocations failed before Python launch because zsh could not create its temporary file: tool chunks5afa29 and9e08da, both exit1. No child PID/UTC or completed capture resulted, and none is reconstructed. After the first failure a later workspace observation showed132648KiB available and the current folder was absent. A separate non-heredoc ordinary writer16753 at17:20:58.630323UTC created only the current folder. This source assembly is a later separate process. No evidence or other agent files were deleted.\n')
    print(json.dumps({'status':'INITIAL_CURRENT_SOURCE_ASSEMBLED','actual_pid':os.getpid(),'utc':utc,'archive_files':len(idx),'no_author_code_import_or_execution':True},indent=2))


if __name__=='__main__':main()
