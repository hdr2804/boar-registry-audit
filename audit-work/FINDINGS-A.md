# FINDINGS-A — Independent audit of the BOAR / LabRat research record (poidh #1520)

Scope: `boar-research/`, `boar-bench/`, `labrat-boar-fork/` clones + the four DEVICE-FINAL
judgment files and two trace files from HF dataset `r4topunk/boar-traces` (sha256 of all six
downloaded files match `boar-research/TRACES.tsv` exactly — verified before use).
All findings below are NEW relative to the 14 rival claims listed in the tasking.
Working files: `audit-work/recompute_u.py` (+ `recompute_u.out`), `audit-work/fm-demo/`.

---

## 1. One judged measurement is pasted as the "result" of three different experiments — including one that ran 0 judge calls

**Statement.** Registry rows X-120 (DENSECHUNK), X-143 (DENSECHUNK-ST) and X-144
(DENSECHUNK-ST2) all carry the identical result `+0.017 (−0.000…+0.035)`, but that number
was produced by exactly one run — DENSECHUNK-ST2's Opus L2 judging. X-143's own verdict
says "FAIL at step 0 … 0 judge calls" and X-120 was a deterministic gate with `judge: none`
on a different item set, so neither could have produced a judged paired CI.

**Why it matters.** The registry is the public evidence base for "387 documented
experiments". If result fields are copied across rows, a reader cannot tell which
experiment actually measured what — and the dense-chunk retrieval lever (a real candidate
improvement: step-0 reach 67 → 108 contexts) appears to have three convergent measurements
behind it when it has one.

**Evidence.**
- `boar-research/data/experiments.json`: X-120 `result` = `+0.017 (−0.000…+0.035)`,
  `judge` = "none (deterministic gate)", `n` = "32 in-pack v0.2…"; X-143 `result` identical,
  `verdict_detail` = "closed: FAIL at step 0 (G2 no-harm; G1 and G3 PASS); 0 judge calls";
  X-144 `result` identical, `verdict_detail` = "not decided at MDE 0.03 (Opus L2 Δ CI through 0)".
  All three cite the same fact F-1122 and the same source row, `CLOSED.md:70`.
- `boar-research/rnd/research/coordinator/CLOSED.md` row R46 attributes the number solely
  to ST2: "Opus paired Δ +0.017 (−0.000…+0.035) raw … (180 public self-test items, 4B cut 7,
  Haiku L1 then Opus L2 N=4 both orders (720 Opus))".
- Verified by script: grouping all 387 rows by identical `result` string (≥25 chars) →
  13 groups covering 32 rows (see finding 2).

**Tag: VERIFIED** (registry JSON + CLOSED.md read directly; grouping script run over
`data/experiments.json`).

---

## 2. The headline counts (387 experiments / 215 no-gain) count registry rows, not independent experiments — single screens are split into multiple rows

**Statement.** CLOSED.md row R1 is ONE four-model closed-book screen (Qwen3.5-4B, Gemma 4
E4B, Qwen3.5-9B, Ministral 8B; one fact, F-512; one combined result string
`0.437/0.495/0.488/0.457 vs 0.487`), yet it became two separate registry experiments —
X-028 (G4E4B) and X-033 (Q35) — each carrying the full four-model result and each counted
as a separate "not-detected" experiment (both therefore inside the 215 no-gain count).
The same pattern recurs: X-076 (MOESCREEN) and X-077 (MOESCREEN-gemma4) are one screen
re-rowed per model with byte-identical result text (the per-model Δs, +0.007 and +0.018,
are arithmetic on the same three numbers: 0.603−0.596 and 0.613−0.596). In total, 13 groups
of rows (32 of 387 rows) share an identical result string with at least one other row.

**Why it matters.** "387 documented experiments, 215 without a gain" is the bounty's
headline scale claim. Row-splitting one screen into per-model rows inflates both numbers
and, because the split rows share one verdict, double-counts the same evidence in the
no-gain tally. (Some identical-result groups are legitimate staged arms/addenda — e.g.
DEEPTHINK-V02 + its addendum — but the screen splits are presented as independent
experiments with independent questions and stop rules.)

**Evidence.**
- `boar-research/rnd/research/coordinator/CLOSED.md` §"4B side" row 1 (single table row,
  four models, one result, label "not detected at MDE 0.055 (57, 1 seed)"), vs
  `data/experiments.json` X-028 and X-033: different `question` texts (Gemma E4B vs
  Qwen3.5-4B), identical `result`, identical `fact_ids` [F-512], identical
  `registry_public` pointer `CLOSED.md:16`, same date 2026-10-05.
- `data/facts.json` F-512: a single fact whose claim text names all four models together.
- X-076/X-077 in `data/experiments.json` + CLOSED.md rows 17/18 (same screen numbers).
- Grouping script over `data/experiments.json` (identical `result` strings ≥25 chars):
  13 groups, 32 rows — incl. CV×4 (X-007/025/026/027), SC×3 (X-009/020/021),
  DEEPROUTE×3 (X-067/083/105), FTDATA×4 (X-068/069/070/072), GROUNDED-DOSE B/C (X-401/402).

**Tag: VERIFIED** (counts and string identity computed from the published JSON; the
"one screen" reading is confirmed by CLOSED.md's own single-row treatment of R1).

---

## 3. 54 of the 387 registry results are explicitly not re-verified — including 17 adopted (shipped) levers

**Statement.** `data/experiments.json` flags 54 rows `result_verified = false`; its own
notes say those result texts come from the 2026-10-13 ledger audit "and [were] not
re-verified for this publication; render it as 'as recorded'". 17 of the 57 `adopted`
verdicts — i.e. levers that shipped in the app — are in the unverified set.

**Why it matters.** The adopted set is the positive half of the research's conclusions
("what worked"). For 17 of those 57, the publication itself disclaims verification of the
recorded result; an outside reader cannot distinguish a re-checked number from a
transcription of an internal ledger.

**Evidence.**
- `boar-research/data/experiments.json`, top-level `notes[0]` (quoted above) and per-row
  `result_verified` field. Counted by script: 54 false of 387; by verdict —
  adopted 17, closed 13, tooling 11, measurement 9, open 4.
- Unverified adopted codes include AR (X-002, arithmetic calculator shipped in cut 3),
  CUT3DEV, CUT4-KVFIX, CUT4-INSTANT-FRAG, DETMAX, HAIKUJUDGE, PARJUDGE, OPUSSHARD, KVQ8,
  CUT5-LITE, VENUEGPS-2, SC-S6, VG-S, VG-L0, INSTSUBJ, CUT3-CONFIRM, CUT3-VGAR-L1.

**Tag: VERIFIED** (field counted directly; the disclaimer is the publication's own text).

---

## 4. Preregistration is mostly unverifiable from the public record: 122 of 137 "sha256-frozen" claims give no public pointer, and all 387 hypotheses are null in the registry

**Statement.** 137 registry rows claim preregistration status "yes, sha256-frozen", but only
15 of them include a `where_public` pointer to the frozen criterion; for the other 122 the
public record offers no way to check that the rule was frozen before the run. Separately,
every one of the 387 rows ships with `hypothesis: null` (the notes disclose the hypothesis
text "lives only in the criterion file (not extracted in this pass)").

**Why it matters.** The record's credibility rests heavily on frozen rules ("judged against
its frozen rule" is the headline methodology). For ~89% of the frozen claims, the freeze is
an assertion, not a checkable artifact, in the very files published for verification.

**Evidence.**
- Counted by script over `data/experiments.json` `preregistered` objects:
  status containing "sha256-frozen" = 137 rows; `where_public` non-null = 15.
- `hypothesis` is null for 387/387 rows (counted); `notes[1]` in the same file discloses why.
- Example: X-002 `preregistered = {"status": "yes, sha256-frozen", "where_public": null}`.

**Tag: VERIFIED** (counts); the significance judgment is INFERRED.

---

## 5. The "215 ended without a gain" figure is a selective subset of the registry's own verdicts

**Statement.** 215 equals exactly closed (187) + not-detected (28). It excludes the 10
`parity` rows, which the registry's own verdict glossary defines as "an equivalence …,
not a gain", and it includes the duplicated screen rows of finding 2 (X-028 and X-033 are
both inside the 215). Under the registry's own definitions, experiments that ended without
a gain number at least 225 (closed + not-detected + parity), before any de-duplication.

**Why it matters.** The 215 is quoted (in the bounty text and the publication) as the
count of experiments that "ended without a gain". The parity rows are precisely
experiments that ended, deliberately, without a gain — omitting them makes the
experime
...[truncated 10301 chars]