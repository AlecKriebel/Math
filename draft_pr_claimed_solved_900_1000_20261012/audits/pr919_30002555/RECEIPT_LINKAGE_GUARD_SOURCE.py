def verify_receipt_links(a, publication, merge, accepted, tracker=None, native=None):
    """Fail on stale/cross-target local receipts before downstream writes."""
    def need(ok, label):
        if not ok:
            raise RuntimeError('PR919 receipt linkage: '+label)
    def read(name):
        return json.loads((a/name).read_text())
    head = '704685791ec0053dc0a52590fdef49ed4aae61d9'
    need(accepted.get('accepted') is True and accepted.get('original_pr_head') == head
         and len(accepted.get('full_package_reviews', [])) >= 2, 'exact acceptance')
    freeze_raw = (a/'publication/PREPUBLICATION_FREEZE.json').read_bytes()
    pin = hashlib.sha256(freeze_raw).hexdigest()
    freeze = json.loads(freeze_raw)
    need(pin == accepted.get('freeze_sha256') and freeze['original_pr_head'] == head
         and freeze['pr'] == 919 and freeze['problem_id'] == '30002555'
         and freeze['files'] == accepted['files'], 'accepted frozen target')
    live_head = head
    if (a/'ACCEPTANCE_INTEGRATION_ADDENDUM.json').exists():
        integration = read('ACCEPTANCE_INTEGRATION_ADDENDUM.json')
        need(integration.get('accepted') is True and integration['original_audited_head'] == head,
             'integration acceptance')
        live_head = integration['integrated_head']
    need(merge.get('number') == 919 and merge.get('state') == 'MERGED'
         and merge.get('headRefOid') == live_head, 'merged PR/head')
    merged = merge['mergeCommit']['oid']
    ident = publication.get('id')
    need(type(ident) is int and ident > 0 and publication.get('state') == 'published'
         and publication.get('doi') == '10.5281/zenodo.'+str(ident)
         and publication.get('record_url') == 'https://zenodo.org/records/'+str(ident),
         'published ID/DOI/record')
    intent = read('publication/ZENODO_PUBLISH_INTENT.json')
    need(intent.get('action') == 'publish' and intent.get('pr') == 919
         and intent['accepted_freeze_sha256'] == pin and intent['merged_commit'] == merged,
         'publication intent/accepted freeze/merge')
    descriptor_raw = (a/'publication/zenodo-deposit.json').read_bytes()
    need(hashlib.sha256(descriptor_raw).hexdigest() == intent['descriptor_sha256']
         == freeze['files']['zenodo-deposit.json']['sha256'], 'exact descriptor')
    descriptor = json.loads(descriptor_raw)
    expected = []
    for item in descriptor['files']:
        record = freeze['files'][item['path']]
        data = (a/'publication'/item['path']).read_bytes()
        need(len(data) == record['bytes'] and hashlib.sha256(data).hexdigest() == record['sha256'],
             'current accepted upload bytes')
        expected.append({'name':item['name'], 'size':record['bytes'], 'sha256':record['sha256']})
    need(len(expected) == 2 and publication['files'] == expected, 'published file fingerprints')
    stage = read('publication/ZENODO_STAGE.json')
    inspected = read('publication/ZENODO_INSPECT.json')
    need(stage.get('id') == ident and stage['files'] == expected, 'staged record/files')
    need(inspected.get('id') == ident and inspected.get('doi') == publication['doi']
         and inspected.get('state') == 'published' and inspected['files'] == expected,
         'published readback ID/DOI/files')
    if tracker is not None:
        need(tracker.get('confirmed') is True and tracker.get('readback_matches') is True
             and tracker.get('pr') == 919 and tracker.get('problem_id') == '30002555'
             and tracker.get('original_pr_head') == head and tracker.get('merged_head') == live_head
             and tracker.get('merge_commit') == merged and tracker.get('accepted_freeze_sha256') == pin
             and tracker.get('doi') == publication['doi'] and tracker.get('zenodo_record_id') == ident,
             'tracker target/head/freeze/DOI')
        need(tracker.get('spreadsheet_id') == '1ZljUv5Q98jNXLoHK8WjwrkzSm3dhHC1-7LElcOU7y20'
             and tracker.get('gid') == 1254632077 and tracker.get('tab_title') == 'Math Puzzles'
             and len(tracker['row']) == 4 and tracker['row'][2] == 'https://doi.org/'+publication['doi']
             and read('TRACKER_READBACK.json').get('values') == [tracker['row']],
             'tracker destination/exact row readback')
    if native is not None:
        need(tracker is not None and native.get('push_confirmed') is True, 'native/tracker confirmation')
        event = native['published_event']
        need(event.get('id') == '30002555' and event.get('pr') == 919
             and event.get('doi') == publication['doi'] and event.get('original_pr_head') == head
             and event.get('accepted_freeze_sha256') == pin and event.get('merged_commit') == merged
             and event.get('zenodo_record_id') == ident
             and event['evidence']['tracker_range'] == tracker['updated_range'],
             'native target/head/freeze/DOI/tracker')


