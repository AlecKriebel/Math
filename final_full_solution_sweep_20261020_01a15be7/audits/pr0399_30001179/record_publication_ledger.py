#!/usr/bin/env python3
"""PR399 verify public DOI/bytes, fresh full dedup, intent, one append, unique readback."""
import argparse
import json
import re
import subprocess
import uuid
from ops_binding import *
from publication_live_gates import collect
from verify_published_files import verify_live


def desired_row(identifier):
    return [
        '30001179 / OWR-3392-005: Generation of Free Product Systems by Tensor Subsystems',
        '', 'https://doi.org/10.5281/zenodo.'+str(identifier),
        TITLE+' — Alec Kriebel (ORCID 0009-0001-9320-500X), v1.0 (2026-10-21). '
        'Unrefereed preprint. An analytic continuous pointed free product system E of separable complex '
        'Hilbert spaces has maximal tensor core F equal to decreasing finite-word Fock space; '
        'its closed free hull is K, all finite words, and K is proper in E at every t>0 via a nonzero '
        'ordinal grade-omega sector. Associativity, an explicit continuous field including time zero, '
        'positive-time local triviality, and continuity of structure maps and inverses are proved. '
        'The stated field convention is part of the theorem; arbitrary stronger regularity is not asserted. '
        'This answers the universal generation clause negatively in the scalar specialization; the shared '
        'generation clause of OWR-3392-004 / 30001178 is the same target, while its cocycle clauses and '
        'OWR-3392-006 / 30001180 forward recovery remain distinct. No general cocycle, recovery or '
        'classification theorem claimed. Classical Fock, Gaussian and Radon-Nikodym inputs are credited. '
        'Bounded actual primary-source comparison found no authenticated earlier exact negative construction; '
        'the named in-preparation manuscript and unpublished/unrecorded talk bodies remain unrecovered. '
        'No worldwide novelty, historical firstness or still-open-in-2026 claim. '
        'PDF and editable-source/verification ZIP preserve all eleven originals and scoped historical audits. '
        'Finite replay supplements the analytic infinite-dimensional proof and does not certify it. '
        'Extensive AI involvement in research planning, proof development and reconstruction, computation, '
        'literature investigation, writing and adversarial verification. No formal independent human peer '
        'review or proof-assistant certification; internal AI audits are not human peer review. '
        'Primary source: https://publications.mfo.de/bitstream/handle/mfo/3111/OWR_2009_09.pdf?isAllowed=y&sequence=1 '
        '(printed pages 528–530; DOI 10.4171/OWR/2009/09). '
        'Record: https://zenodo.org/records/'+str(identifier)+'. '
        'PR: https://github.com/AlecKriebel/Math/pull/399.'
    ]


def gws(action,params,body=None):
    command=['gws','sheets','spreadsheets','values',action,'--params',json.dumps(params)]
    if body is not None:
        command+=['--json',json.dumps(body,ensure_ascii=False)]
    run=subprocess.run(command,capture_output=True,text=True)
    if run.returncode:
        raise RuntimeError('GWS failed; inspect saved intent/live sheet before retry: '+run.stderr[:700])
    return json.loads(run.stdout)


def read(label,operation):
    value=gws('get',{'spreadsheetId':SHEET,'range':"'Math Puzzles'!A:AQ",'valueRenderOption':'FORMATTED_VALUE'})
    atomic_json(PRIVATE/(label+'_'+operation+'.json'),value)
    return schema_rows(value)


def matches(rows,identifier,family_ids=()):
    found=[]
    for i,row in enumerate(rows[1:],2):
        is_target=target_in_row(row,identifier,family_ids)
        if PATTERN.search(' '.join(row)) or is_target:found.append((i,row))
    return found


def append_verified(expected_head,identifier):
    require_release_clearance()
    # Never trust old saved booleans: make a new read-only actual public download
    # and DOI200 inspection before the last full-account/full-sheet gate.
    public=verify_live(identifier)
    if (public.get('record')!=identifier or public.get('all_public_file_bytes_match_reviewed') is not True
            or public.get('doi_resolution',{}).get('status')!=200
            or public.get('release_manifest_sha256')!=RELEASE_SHA):
        raise RuntimeError('Fresh public DOI/files verification incomplete')
    resolution=public['doi_resolution']
    destination=doi_destination_evidence(identifier,resolution.get('status'),resolution.get('resolved_url'))
    evidence=resolution.get('destination_verified')
    if (not isinstance(evidence,dict) or evidence!=destination
            or type(evidence.get('record')) is not int or type(evidence.get('status')) is not int):
        raise RuntimeError('Fresh exact DOI destination evidence absent or inconsistent')
    gate,acceptance=collect('before_ledger',expected_head,identifier,allow_target_row=True)
    family_ids=gate.get('expected_identity_record_ids',[identifier])
    operation=uuid.uuid4().hex
    row=desired_row(identifier)
    before=read('ledger_before_append',operation)
    if digest(before)!=gate['ledger_sha256']:
        raise RuntimeError('Full sheet changed since fresh gate; recollect/reconcile before append')
    doi='10.5281/zenodo.'+str(identifier)
    # Independently inspect every returned cell before exemptions or mutation.
    for value in before:row_identity_names(value)
    doi_rows=[r for r in before[1:] if target_in_row(r,identifier,family_ids)]
    if len(doi_rows)>1 or (doi_rows and doi_rows[0]!=row):
        raise RuntimeError('Existing DOI appears in a different or duplicate full-sheet row; no append')
    found=matches(before,identifier,family_ids)
    # Broad prior distinct-model rows are allowed only through the exact root
    # reconciliation; target identity/DOI rows must still be unique and exact.
    recon=json.loads((AUDIT/'ROOT_PREPUBLICATION_LEAD_RECONCILIATION.json').read_text())
    known={v['values_sha256'] for v in recon['ledger_leads']}
    if any(digest(r) in known for r in doi_rows):
        raise RuntimeError('Current target DOI/row contradicts a root non-target ledger exemption; no append')
    found=[(i,r) for i,r in found if digest(r) not in known]
    intent=AUDIT/'LEDGER_APPEND_INTENT.json'
    appended=False
    if found:
        if len(found)!=1 or found[0][1]!=row:
            raise RuntimeError('Existing target/DOI row differs or is duplicated; no append')
        row_number=found[0][0]
    else:
        if intent.exists():
            raise RuntimeError('Prior append intent has no exact visible row; reconcile without blind retry')
        require_release_clearance()
        fresh(gate['started_utc'])
        intent_json(intent,{'timestamp':stamp(),'pr':399,'spreadsheet_id':SHEET,'range':"'Math Puzzles'!A:D",
            'row':row,'before_rows':len(before),'before_sha256':digest(before),'operation':operation,
            'gate_receipt':gate['receipt'],'public_verification_sha256':sha((AUDIT/'ZENODO_PUBLIC_FILE_VERIFICATION.json').read_bytes()),
            'uncertain_outcome_rule':'Read current full sheet for exact DOI/result before any retry; never blindly append twice.'})
        response=gws('append',{'spreadsheetId':SHEET,'range':"'Math Puzzles'!A:D",'valueInputOption':'RAW',
                      'insertDataOption':'INSERT_ROWS','includeValuesInResponse':True},
                     {'majorDimension':'ROWS','values':[row]})
        atomic_json(AUDIT/'LEDGER_APPEND_RESPONSE.json',response)
        updates=response['updates']
        if (updates['updatedRows']!=1 or updates['updatedColumns']!=4 or updates['updatedData']['values']!=[row]):
            raise RuntimeError('Unexpected append outcome; inspect live sheet, no retry')
        appended,row_number=True,None
    after=read('ledger_after_append',operation)
    for value in after:row_identity_names(value)
    # Target DOI rows are never filtered by any non-target digest, including
    # readback after a provider boundary. Exact target identity has precedence.
    found=[(i,r) for i,r in matches(after,identifier,family_ids) if digest(r) not in known
           or target_in_row(r,identifier,family_ids)]
    if len(found)!=1 or found[0][1]!=row or (row_number is not None and row_number!=found[0][0]):
        raise RuntimeError('Target row readback/uniqueness mismatch; no retry')
    doi='10.5281/zenodo.'+str(identifier)
    if sum(target_in_row(r,identifier,family_ids) for r in after)!=1:
        raise RuntimeError('DOI is duplicated anywhere in full sheet')
    if appended and (len(after)!=len(before)+1 or after[:-1]!=before or after[-1]!=row):
        raise RuntimeError('Append readback changed other sheet rows; reconcile without retry')
    receipt={'timestamp':stamp(),'pr':399,'status':'verified','row_number':found[0][0],
        'spreadsheet_id':SHEET,'sheet_gid':1254632077,'doi':doi,'values':row,'new_row':appended,
        'unique_target_and_DOI':True,'read_back_exact':True,'ledger_rows_before':len(before),
        'ledger_rows_after':len(after),'gate_receipt':gate['receipt'],'operation':operation}
    atomic_json(AUDIT/'LEDGER_PUBLICATION_VERIFICATION.json',receipt)
    return receipt


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--expected-pr-head',required=True)
    parser.add_argument('--deposit-id',type=int,required=True)
    args=parser.parse_args()
    print(json.dumps(append_verified(args.expected_pr_head,args.deposit_id),indent=2))


if __name__=='__main__':
    main()
