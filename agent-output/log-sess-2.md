# Project status recap and alignment check

**Session ID:** ses_fb773b2dfffeD4hh3GW7rw7OEB
**Created:** 8/28/2026, 3:25:49 PM
**Updated:** 9/2/2026, 1:16:42 AM

---

## User

let's make sure we are on the same page. summarize for me what the current project is about and where we're at

---

## Assistant

**Tool: read**

**Tool: glob**

---

## Assistant

**Tool: read**

**Tool: read**

**Tool: read**

**Tool: read**

---

## Assistant

**Tool: read**

---

## Assistant

We're aligned. Here's the picture:

**What this project is**
- A coaching workspace for your **Polygence take-home**: a Django + DRF + React mentor↔student matching app with a state-transition bug (accepted proposal that still has decline reasons).
- Goal: reproduce, understand, fix, and test the bug well enough to defend it in an interview — not a rewrite.

**Ground rules (from MISSION.md / NOTES.md)**
- I coach with Socratic questions; **you** run, reproduce, write the fix and tests. I never hand over the solution.
- Timebox: a few focused hours.

**Where we're at**
- The actual repo lives at `~/.local/share/opencode/repos/github.com/elspecal/polygence` (referenced as `repo` in opencode.json).
- Session 1 produced: `lessons/0001-meet-the-matching-app.html` (install `uv`, run the app, trace the happy path — no bug hunting yet) and `reference/architecture-map.html`.
- Planned next: **lesson 0002 — reproduce the inconsistent state** (exercise step 2).
- Environment note from last session: `uv` wasn't installed yet.

So: have you worked through lesson 0001 (got the app running locally), or should we pick up there?

---

## User

i'm done with lesson 1. `uv` is installed and i'm ready for lesson 2. let's continue!

---

## Assistant

**Tool: read**

**Tool: read**

---

## Assistant

Lesson 1's format is clear. Quick check of the shared assets so lesson 2 uses only styles that exist:

**Tool: read**

**Tool: read**

---

## Assistant

**Tool: read**

**Tool: read**

---

## Assistant

I have the full picture of the format and assets. Now I'll write lesson 0002 — reproduce the inconsistent state — keeping it Socratic (you predict, then try; the full sequence sits behind a "stuck?" hint, and the root cause stays hidden for lesson 3).

**Tool: write**

---

## Assistant

One markup fix — `<summary>` must be a direct child of `<details>`, not nested in the `<p>`:

**Tool: edit**

---

## Assistant

Now update the notes and cross-links:

**Tool: edit**

---

## Assistant

**Tool: edit**

---

## Assistant

**Tool: edit**

---

## Assistant

Quick sanity check that the new lesson HTML is well-formed:

**Tool: bash**

---

## Assistant

That's the checker mishandling self-closing `<meta />` tags, not a problem with the file — fixing the checker:

**Tool: bash**

---

## Assistant

Lesson 0002 is ready: **`lessons/0002-reproduce-the-inconsistent-state.html`** — open it in your browser. Also updated: the architecture map footer and `NOTES.md` (lesson 0001 marked done, `uv` noted as installed).

The shape of it:

1. **Translate first** — turn "Ops saw accepted proposals with decline reasons" into an exact `response` JSON shape, written in your notebook before anything else.
2. **Plan before you click** — three leading questions point you at the endpoints table and `ReviewStudent.jsx` behavior; you predict the click sequence *and* the resulting JSON.
3. **Run it** — seed fresh, execute your prediction, watch the network tab (one request won't be 2xx, yet the page won't care), verify at `/proposals`, and make it repeatable.
4. If stuck after 5 minutes, the full sequence is behind a **"Stuck? Open me"** hint.
5. There's also a **mirror experiment** (decline fully → then accept) that produces a different surprise — note how it differs from what Ops reported.

Per our ground rules I won't hand you the sequence or the why — the lesson asks, you answer. Start with the notebook question: what does "accepted with decline reasons" look like as that dict? When you've reproduced it, tell me what your request log showed and we'll debrief.

---

## User

i keep running into the term "notebook". i'm not sure what this refers to in this context. can you clarify the term? like what am i supposed to do when i see "Notebook first"?

---

## Assistant

"Notebook" = your own scratch notes, physical or digital — a plain text file is perfect (e.g. a `NOTES-2.md` anywhere you like). Nothing in the repo depends on it.

The point is *writing before looking/testing*. Each callout tells you which kind of entry to make:

- **"Notebook first"** — write your answer or prediction *before* reading the next paragraph or clicking anything. E.g. the JSON shape one: type out what you think the inconsistent dict looks like, from memory. Then compare with what the lesson/reality shows. The gap between your guess and reality is exactly what you learn from.
- **"For your notebook"** — record an observation you'll need later: the click sequence that reproduced the bug, the request log, odd things you noticed. These become your interview answers and test cases in later lessons.

Concretely, when you see "Notebook first," open your file and write 2–4 lines — a guess, a sketch, a JSON snippet, whatever form fits. Wrong guesses are fine and useful; blank page isn't. Then continue and check yourself.

Want me to create a starter `notebook.md` with the lesson 1 + 2 prompts laid out?

---

## User

nah, it's all clear now

---

## Assistant

Cool. Back to lesson 0002 then — first prompt: what does "accepted with decline reasons" look like as the `response` JSON? Write your guess, then work through the three planning questions.

---

## User

you suggest a mirror repro with decline fully, then accept saying a POST will replace the whole dict. however it doesn't work like that since if "value" is already present (not Null) the controller will respond with `{"error": "Response already recorded"}`. PATCH then will also respond with `{"error": "Reason already recorded"}` in case "reason" is present already. 

a mirror repro with click decline link -> back to inbox -> clicking accept link -> selecting a rating and submitting does produce a "mixed" dict with `{"value": "reject", "match_rating": X}`

---

## Assistant

Good catch — you're pushing back on the lesson's claim, so let's verify against the actual code instead of the map's summary. Checking the view and service now:

**Tool: bash**

---

## Assistant

**Tool: read**

**Tool: read**

**Tool: read**

---

## Assistant

Verified — you're right, and the lesson was wrong. The code:

- `views.py:27-28`: POST refuses with `"Response already recorded"` when `value` is present — so the second POST never gets through.
- `services/student_proposal.py:22-28`: the "replace the whole dict" in `update_response` only ever executes for a *first* decision. It can't erase anything in your mirror run.

So "POST replaces the dict, decline data vanishes" was a fiction — the real mechanism in your mirror result is the one you quoted yourself. Fixing the lesson callout, quiz Q5, and the map:

**Tool: edit**

---

## Assistant

**Tool: edit**

---

## Assistant

**Tool: edit**

---

## Assistant

**Tool: edit**

---

## Assistant

**Tool: edit**

---

## Assistant

All corrected. Summary of what changed:

- **Lesson 0002**: the "One more experiment" callout now says stop before the decline reason form, asks you to predict per-request outcomes, and adds the variant *with* reasons submitted. Quiz Q5 now has "the guard refused it" as the correct answer.
- **Architecture map**: POST row and services table no longer imply the replace can overwrite anything — it's only reachable while `value` is absent.

One nuance to pin down for your notebook. Your run produced `{"value": "reject", "match_rating": X}` because the decline reason form was **not** submitted — `reason` was never in the dict, so the PATCH guard you quoted let the accept-form's PATCH through. You predicted what the variant changes, I think — but run it anyway: submit decline reasons *first*, then accept link + rating, and watch which request dies and with what error.

Then the debrief question: you now have two mixed states — `{value: "accept", reason}` (Ops) and `{value: "reject", match_rating}` (yours). Write the one sentence they have in common. That sentence is the seed of lesson 3.

---

## User

both cases have in common that since the `review_student` controller in case of PATCH doesn't check "value" it allows a "mixed" dict to be produced

---

## Assistant

That's the mechanism, in your own words — exactly what the exercise asks for. Three things before we call it done:

1. **Sharpen "doesn't check value."** Check it *for what* — presence? validity? or something about the follow-up being written? A `reason` PATCH and a `match_rating` PATCH don't have the same relationship to the recorded decision. Rewrite your sentence so it says what the PATCH should have asked. (Sit with it; that question is the doorway to the fix, lesson 4.)
2. **The client's role.** Your request log had a request the server refused — and the flow continued anyway. Which component made that call, and would your repro survive without it? Add a second sentence covering that half. (You already wrote this down in the lesson-2 quiz.)
3. **Close the loop.** Run the variant: submit decline reasons first, *then* accept link + rating. One guard changes the outcome — which, and what lands in the dict?

**Tool: edit**

---

## Assistant

Notes updated — lesson 3 is now a consolidation session (your request log → code lines, two-sentence root cause, write-up draft), lesson 4 is the fix + tests you design. Bring me the sharpened sentence, the client-side sentence, and the variant result.

---

## User

1. PATCH should validate "value" against "reason"/"match_rating" but it doesn't currently
2. The `<ReviewStudent />` component swallows the error respond from the server. the repro wouldn't work if it'd surface the error and stop the review flow.
3. In case decline reason is already submitted, then submitting an additional accept + rating doesn't change the proposal dict since PATCH guards against that by checking whether "reason" is already present.

---

## Assistant

All three hold up — that's a complete root-cause picture, built from your own observations. Two refinements for the interview version, then lesson 3. Let me verify two frontend details so the consolidation lesson's code map is accurate:

**Tool: read**

**Tool: read**

---

## Assistant

Confirmed the last details (`MatchingFeedbackForm.jsx:22-25` sends `reason: {}` on accept; `api.js:36-43` maps `matchRating` → `match_rating`). Writing lesson 0003 — a consolidation lesson, since you've already done the discovering:

**Tool: write**

---

## Assistant

Now the cross-links and notes:

**Tool: edit**

---

## Assistant

**Tool: edit**

---

## Assistant

**Tool: bash**

---

## Assistant

All three correct — your root cause is on the record. One precision point to carry forward: "validate value against reason/match_rating" resolves to the pairing **reason ↔ reject, match_rating ↔ accept** — and note the frontend swallow is an *enabler*, not the hole: even a perfect frontend leaves the API able to merge a `reason` into a proposal with no decision at all. The durable guard lives server-side.

**Lesson 0003 is ready**: `lessons/0003-from-repro-to-root-cause.html`. It's consolidation, not discovery:

1. **Your request log, pinned to code** — the Ops repro as a 3-row table, each row stamped with the exact lines that decided it (`views.py:27-28`, `services/student_proposal.py:22-28` / `31-38`, `ReviewStudent.jsx:31-33`). Open each line yourself; annotate your log.
2. **The two-sentence root cause** — server hole + client enabler skeletons to fill and rewrite in your own words, no line numbers.
3. **Draft the write-up** — the four-beat deliverable (what Ops saw → minimal repro → root cause → acceptance criterion), with the criterion as a fill-in-the-blank you'll turn into a test next lesson.
4. Quiz, including the pairing and the "could the repro survive a fixed frontend?" question.

When your two sentences and acceptance criterion are in the notebook, say them to me — rehearsal before lesson 0004, where you design the guard and write the failing tests.

---

## User

i'm ready with the acceptance critera

---

## Assistant

Say it, then — paste your acceptance criterion, and while you're at it the two root-cause sentences from the same notebook page. I'll push back the way an interviewer would.

---

## User

### Root cause

Server: The `/api/review-student/<uuid>` controller upon PATCH checks whether a
reason is already recorded but fails to validate it against its corresponding
`value` type (`reject`). This creates the possibility of an accepted proposal
with decline reason.

Client: `<ReviewStudent />` swallows the `400`, "Response already recorded"
error and continues the review flow by rendering the `<FeedbackForm />`. This
allows the missing guard in the backend controller to produce an accepted
proposal with decline reason.

### Acceptance criteria

The bug is fixed if for any sequence of requests, the the `response` dict never
contains mixed states. 

---

## Assistant

Solid start — the client/server split is clean, and "for any sequence of requests" is exactly the right quantifier instinct. Now the pushes, the way an interviewer would:

1. **Your criterion uses the word it's supposed to define.** "Never contains mixed states" — what is mixed? A test can't assert a vibe. Rewrite it as an *allow-list*: enumerate the exact dict shapes that are legal, and declare everything else a bug. You already know all the pieces — the empty state, the decision-only state, and which follow-up may accompany which value.

2. **Where's `match_rating`?** Your server sentence covers `reason`↔`reject` only. Your own mirror run produced `{value: "reject", match_rating}` — run that dict through your criterion in your head. Does your wording fail it? It must, or your fix will leave half the bug alive.

3. **"Any sequence" — include the degenerate one.** No POST at all: a raw PATCH with `reason` onto a fresh proposal. Is `{reason: {...}}` with no `value` a "mixed state"? Your criterion has to rule that in or out explicitly — right now it's silent.

Revise the criterion against those three and repost. If it survives, lesson 0004 is turning it into failing tests.

**Tool: edit**

---

## Assistant

Notes updated. Revise and repost when ready.

---

## User

### Root cause

Server: The `/api/review-student/<uuid>` controller upon PATCH checks whether a
reason is already recorded but fails to validate the `value` type
(`reject`<->`reason`, `accept`<->`match_rating`). This creates the possibility
of an accepted proposal with decline reason.

Client: `<ReviewStudent />` swallows the `400`, "Response already recorded"
error and continues the review flow by rendering the `<FeedbackForm />`. This
allows the missing guard in the backend controller to produce an accepted
proposal with decline reason.

### Acceptance criteria

The bug is fixed if for any sequence of requests, the `response` dict can only
ever be in two possible shapes:

- accept:

```json
{
  "value": "accept",
  "match_rating": <0-10>
}
```

- decline:

```json
{
  "value": "reject",
  "reason": {
    <chosen_reason>: true | string
  }
}
```

This means that bare `reason` or `match_rating` without `value`, `reason` with
`accept` and `match_rating` with `reject` are all disallowed states. 

---

## Assistant

The pairing is in, the degenerate case is covered, and it reads like an invariant now — "two shapes, everything else disallowed" is the right mental model. But run your own allow-list against real traffic before an interviewer does:

1. **Mentor accepts, never submits a rating** — POST accept, closes the tab. Final dict: `{value: "accept", recorded_at}`. Legal or not? Your allow-list demands `match_rating`, so it calls this a bug — but that's ordinary traffic, and it's also exactly where your Ops repro *starts*. Follow-up data can't be mandatory.

2. **Every real dict carries `recorded_at`** — `update_response` writes it and nothing removes it. Your key-exact shapes fail every state the app has ever produced. So decide what the invariant is actually about: an exhaustive key list, or *coexistence rules* (which keys may accompany which `value`)?

3. **Scope check** — `<chosen_reason>: true | string` and `<0-10>` pin down the *payload schemas*. If a decline reason contained some extra key, or a rating arrived as a string, would that be *this* bug's regression? The missing check you found enforces consistency between decision and follow-up — payload validation is a different concern. Keep the criterion about what the value check should guarantee, or your test will be testing two bugs at once.

One more pass — I think v3 is the one that survives. Then we open lesson 0004: failing tests first.

**Tool: edit**

---

## Assistant

V3 when ready.

---

## User

### Root cause

Server: The `/api/review-student/<uuid>` controller upon PATCH checks whether a
reason is already recorded but fails to validate the `value` type
(`reject`<->`reason`, `accept`<->`match_rating`). This creates the possibility
of an accepted proposal with decline reason.

Client: `<ReviewStudent />` swallows the `400`, "Response already recorded"
error and continues the review flow by rendering the `<FeedbackForm />`. This
allows the missing guard in the backend controller to produce an accepted
proposal with decline reason.

### Acceptance criteria

The bug is fixed if for any sequence of requests, the `respond` dict with
`reason` must also have its `value` set to `reject` and one with `match_rating`
must also have its `value` set to `accept`. 

---

## Assistant

Criterion v3 survives all three pushes — coexistence rules, optional follow-ups, degenerate case implicitly covered. One typo for the final write-up: "`respond` dict" → `response`. Let me check the house test style before writing lesson 0004:

**Tool: bash**

---

## Assistant

**Tool: read**

**Tool: read**

---

## Assistant

House style confirmed — and there's a landmine worth building the lesson around: `test_review_student.py:58-68` PATCHes `{"reason": ..., "match_rating": 3}` onto a **rejected** proposal and asserts *both* land. The repo's own test suite blesses exactly the mixed state your criterion forbids. That's interview gold. Writing lesson 0004:

**Tool: write**

---

## Assistant

**Tool: edit**

---

## Assistant

**Tool: edit**

---

## Assistant

**Tool: read**

---

## Assistant

**Tool: edit**

---

## Assistant

**Tool: bash**

---

## Assistant

Criterion accepted — that sentence is your fix spec. **Lesson 0004 is ready**: `lessons/0004-design-the-fix-test-first.html`, the final lesson.

What's inside:

1. **Criterion → test matrix** — every clause becomes a row; 400 rows must also assert the dict is unchanged, and there's a row sending the *exact* body the frontend sends (you'll see why when you write the guard).
2. **Audit the existing suite** — hold every existing test against your criterion. I flagged one conflict in chat already (`test_review_student.py:58-68`); your job is to check *all* of them, decide what the blessed-mixed-state test should assert instead, and revise it. The write-up point: the suite didn't miss the bug, it *blessed* it — the rule was never specified.
3. **Write tests → watch them fail red, for the right reason.**
4. **Design the guard** — where it lives (house pattern), what it refuses, and the falsy-`{}` trap posed as questions, not answers.
5. **Implement → green → manual close-out**: rerun both lesson-0002 repro recipes; they should be dead.
6. The frontend-hardening scoping decision, a 5-question quiz, and the finish line: assemble the write-up, then rehearse the 5-minute interview walkthrough with me.

Report back with your matrix and red failures — especially the guard-design answers.

---

## User

i implemented the tests. they failed as expected. then i implemented the guards as well as the change on the frontend so that is surfaces the server error now. i'm not sure about the matrix you ask me for. could you please give me an example that shows the pattern you have in mind?

---

## Assistant

One quick check so the example uses the right default state — reading the model:

**Tool: read**

---

## Assistant

The matrix isn't an extra artifact — it's a coverage checklist. One row = one test, in three beats: **arrange** (the "State before" column), **act** (the "Request" column), **assert** (the "Expected" column: status code *and* resulting dict). Here's one full row as a test, house style — the degenerate row:

```python
class ReviewStudentPatchGuardTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.mentor = Mentor.objects.create(name="Alex", email="alex@example.com")
        self.mentor_request = MentorRequest.objects.create(student_name="Jamie")
        self.proposal = StudentProposal.objects.create(
            mentor=self.mentor, mentor_request=self.mentor_request
        )

    def test_rejects_rating_without_decision(self):
        response = self.client.patch(
            f"/api/review-student/{self.proposal.uuid}/",
            {"match_rating": 7},
            format="json",
        )

        self.assertEqual(response.status_code, 400)
        self.proposal.refresh_from_db()
        self.assertEqual(self.proposal.response, {})
```

How the columns map:

- **"State before: fresh proposal"** → `setUp`. Shared state goes in `setUp` (like the house classes do); a one-off state goes inside the test itself.
- **"Request: PATCH match_rating"** → the `client.patch` call.
- **"Expected: 400, dict unchanged"** → the two assertions. `refresh_from_db()` is what makes the second one honest — you're re-reading what's actually in the DB, not trusting the in-memory object.

What I had in mind for you: go through the lesson's table row by row, and for each row name the test that covers it and check it asserts *all three beats*. If your tests only assert status codes, add the dict assertions — a 400 that silently wrote half the payload would pass a status-only test. And if any row has no test (the frontend-contract row is the usual miss), write it.

Meanwhile — guard and frontend change implemented, nice. Two status questions: did the full suite go green *including the existing test you revised*, and have you rerun both repro recipes from your notebook to confirm they're dead?

**Tool: edit**

---

## Assistant

Notes updated. Answer the two status questions when you've checked, and if any matrix row turns out uncovered, show me which one.

---

## User

yes, i added a test for each row in the table and everything is green now including all the existing ones. reran all repros. they're dead for good

---

## Assistant

All four MISSION success criteria are now met except one: *defending it*. So — mock interview, right now.

Walk me through it, unprompted, in your own words: the state transition, the bug, the fix, the tests. Under five minutes. I'll interrupt the way an interviewer would — expect "why there and not in the service?", "what does your criterion NOT cover?", and "why did you change an existing test?"

Two small things before you submit, in this order: `git diff` review of the repo (smallest change that satisfies the criterion, revised test is honest, no stray debug code), then the write-up assembly from lesson 0004's finish line — including the one-sentence justification for hardening the frontend.

**Tool: edit**

---

## Assistant

Notes updated. Take it away whenever you're ready.

---

## User

let's start then:
Ops reported that accepted proposals sometimes contain decline reasons. while investigating the bug it turnd out that the mirror case is also possible where declined proposals contain match ratings. and even proposals with no decision yet can contain follow-ups although that is only reproducable by direct PATCH requests, not from the frontend.
the server and client works in tandem to produce the bug. the server does not guard against a follow-up that is inconsistent with the decision and although it does guard against a second decision POST against an active proposal the frontend swallows that error and thus allows the bug from the missing guard against the PATCH to manifest.
i added a guard that makes sure that a PATCH with reason can only be accapted against an declined proposal and a PATCH with rating can only be accapted against an accapted proposal.
a test already existed that produced the reported inconsistent state and it asserted that is should be allowd which shows that restricting the state of the response dict was not specified. i modified that test such that it is now expects a 400 response with error. i also covered with tests all possible cases derived from the accaptend criteria.

---

## Assistant

Strong content — mirror case volunteered unprompted, the direct-PATCH nuance is precisely scoped, and the existing-test story lands. That's a pass on substance. Now the interruptions, the way an interviewer would:

1. **You skipped the state transition.** You went from "Ops reported" straight to root cause — I don't yet know what a proposal's states *are*. Give me 30 seconds on the happy-path flow first: the email links, the two requests, the one shared dict. The bug story needs that anchor before it means anything.

2. **"Why in the view and not the service?"** You told me *what* you added, not *where* or *why there*. Preempt the question.

3. **"What was the trickiest detail?"** Interviewers ask this to see if you actually got your hands dirty. You have a great answer sitting in your notebook — something the accept form sends that a naive guard would break.

4. **"What happens if two PATCHes arrive at the same time?"** Think about the order your guard runs in versus the save. Is check-then-act atomic here? If not — is that in scope for this fix, and how would you say so out loud without sounding like you're dodging?

And a delivery note: the write-up is a written deliverable — slow down on it. You've typed "accapted" four times in this walkthrough alone; typos in a take-home cost more than they should.

Answer the four, then assemble the write-up.

**Tool: edit**

---

## Assistant

**Tool: edit**

---

## Assistant

Take the four interruptions one at a time — flow first.

---

## User

1. 
  1. click accept link -> GET, POST fired -> response dict have `value: "accept"`.
  2. get back to inbox, click decline link -> GET, POST fired again -> response dict still has `value: "accept".
  3. select decline reason on the feedback form -> PATCH fired -> response dict now has `value: "accept"` and `reason: <selected_reason>`
2. i added the missing gurad in views.py as that is consistent with the existing pattern used in the code base: the service only mutates state after the guards inside the view allow.
3. checking that `reason` is not null instead of checking whether it's falsy would break a happy path as the frontend sets reaon to an empty dict inside of the body of a PATCH with match rating follow-up to an accepted proposal.
4. i have not checked but i suspect that two PATCHes with different follow-ups at the same time could produce the bug. i do think fixing that would require more labor than the current scope allows.

---

## Assistant

2 and 3 are crisp, defensible answers — guard location with the house-pattern justification, and the falsy war story with the exact reason it matters. Two refinements and one final rep:

1. **Your flow opens mid-story.** You walked the *bug* sequence, but an interviewer needs the clean path first: fresh proposal → accept or decline link → POST records `value` → feedback form PATCHes the paired follow-up → dict ends consistent. One sentence. *Then* the interleaving you described, where step 2 should be named precisely: the second POST **400s with "Response already recorded" and ReviewStudent swallows it** — that refusal is half your root cause; don't let it go unnamed in your own walkthrough.

4. **Run your suspicion against your own new guard — line by line.** Two PATCHes, different follow-ups, same proposal. For each request: what state does it *read*, and which guard fires? Compare that trace pre-fix versus post-fix. Your intuition was correct for the old code — does it still hold? Then the out-loud framing: check-then-act vs atomic, what tool Django offers if the scope demanded it (`select_for_update` is the phrase to have ready), and what class of race remains even then.

Answer those two and the rehearsal is done — assemble the write-up.

**Tool: edit**

---

## Assistant

Trace it and give me the final answer.

---

## User

1. the expected user flow is one from the following two:
  - Mentor clicks accept link in a fresh proposal inside thier inbox -> a POST request is fired with the decision -> the service records it -> Mentor rates student -> a PATCH request is fired -> the service pairs the rating with the decision in the proposal
  - Mentor clicks accept link in a fresh proposal inside thier inbox -> a POST request is fired with the decision -> the service records it -> Mentor rates student -> a PATCH request is fired -> the service pairs the rating with the decision in the proposal 

---

## Assistant

---

