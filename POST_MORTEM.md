## Description

Ops has seen proposal records that look accepted but also contain decline
reasons. That should never happen.

Additionally to the original report it turns out that the mirror state is also
possible where a declined proposal contains a match rating as well as a proposal
with no decision but only a follow-up rating/reason. Note though that the last
one is not reproduceable from the frontend only via a direct request against
the server.

## Steps to reproduce

1. Click accept link ->
   `<ReviewStudent />` fires GET, POST in paralell ->
   `response` dict is has `value: "accept"`.
2. Get back to inbox, click decline link ->
   another pair of GET, POST ->
   `response` dict still has `value: "accept"`.
3. Select decline reason ->
   PATCH request ->
   `response` dict has `value: "accept"` and `reason: <selected_reason>`.

## Root cause

Server: The `/api/review-student/<uuid>` controller upon the follow-up PATCH
checks whether a reason is already recorded but fails to validate the `value`
type (`reject`<->`reason`, `accept`<->`match_rating`). This creates the
possibility of an accepted proposal with decline reason.

Client: `<ReviewStudent />` swallows the `400`, "Response already recorded"
error upon a second POST against an active proposal and continues the review
flow and renders the `<FeedbackForm />`. This allows the missing guard in the
backend controller to produce an accepted proposal with decline reason.

## Acceptance criteria of a fix

The bug is eliminated if for any sequence of requests, the `response` dict with
`reason` must also have its `value` set to `reject` and one with `match_rating`
must also have its `value` set to `accept`.

## Lessons

The test case, `ReviewStudentPatchTestCase`, already have a test,
`test_records_decline_reason()`, which treats the inconsistent state in
`response` dict as accepted outcome.

A requirement recording that the allowed decision-follow-up states are
accept<->match rating and decline<->reason could've led to a test that
would've surfaced the bug earlier.

After the bug is eliminated tests should assert that the server responds with
`400`, and a relevant error message upon a PATCH with `reason` against an
accepted proposal or a PATCH with `match_rating` against a rejected proposal.

## Plan

1. Inroduce a new guard in the `/api/review-student/uuid:current/` controller in
   `views.py` that validates that `response/value` conforms to the
   `accept`<->`match_rating` and `decline`<->`reason` allowed states.
2. Modify current and introduce new tests that cover the acceptance criteria.
3. Make `<ReviewStudent />` surface the server error that it currently swallows.
4. Discover ways to modify the somewhat rough UX resulting from #3.
