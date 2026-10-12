import datetime,hashlib,json,pathlib,sys
R=pathlib.Path(__file__).resolve().parent
D=pathlib.Path('/Users/alec/.cache/codex-pr65-priority-20261004/status_family_20261004')
checks=[]
def check(name,ok):
    checks.append({'name':name,'passed':bool(ok)})
    if not ok: raise AssertionError(name)
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
check('provided2019_digest',sha(D/'hayman2019.pdf')=='1388a8c153a3eb16156d90542d1f00e4a6203b594566540c71c5f354238e14dc')
check('fresh_AAN_equals_retained',sha(D/'aan1999_fresh.pdf')==sha(D/'aan1999.pdf'))
check('fresh_HL2018v2_equals_retained',sha(D/'hayman2018v2_fresh.pdf')==sha(D/'hayman2018v2.pdf'))
pages=(D/'hayman2019.pdf.txt').read_text().split('\f')
check('288_pdf_text_pages_plus_empty_tail',len(pages)==289 and not pages[-1].strip())
check('2019_problem_and_update_start_pdf127', 'Problem 5.51' in pages[126] and 'Update 5.51' in pages[126])
check('2019_explicit_update_pdf128','I is constructed explicitly' in pages[127])
check('2019_cannot_copy_no_progress_to551','No progress on this problem' not in pages[126])
old=(D/'hayman2018v2.txt').read_text().split('\f')
check('2018v2_true_no_progress_pdf106','Update 5.51 No progress on this problem has been reported to us.' in old[105])
check('all_requested_renders_present',all((D/n).is_file() for n in ['HL2019-127.png','HL2019-128.png','HL2019-005.png','HL2018v2-106.png','AAN1999-09.png','AAN1999-10.png','AAN1999-11.png','AAN1999-12.png']))
verdict=json.loads((R/'VERDICT.json').read_text())
check('verdict_no_priority_promotion',verdict['novel_full_historical_resolution_clearance'] is False and verdict['worldwide_priority_established'] is False)
check('original_head_and_turns_preserved',verdict['head_reported_by_parent']=='5cc1602c05d79502defb07cec7027963149494d2' and verdict['original_proof_turns']==[2,5])
check('no_full_source_bodies_in_owned_repository_folder',not any(p.suffix.lower() in ['.pdf','.png','.jpg','.txt'] for p in R.iterdir() if p.is_file()))
stamp=datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='seconds')
print(json.dumps({'completed_utc':stamp,'checks':checks},indent=2))
with (R/'RESEARCH_LOG.md').open('a') as stream:
    stream.write('\n## '+stamp+' - 100% toward assigned status/explicitness audit\n\nFinished page-pinned REPORT, VERDICT and independent exact-target normalization. Validated source/version hashes, decisive update/page mapping, render availability, immutable head/turn metadata, adverse historical clearance and private-only full source handling. The assigned audit is complete; analytic correctness and worldwide priority remain expressly outside this family\'s clearance. No shared Git, index, PR, native editor or publication mutation. Manifest finalization follows as a metadata-only checkpoint.\n')
