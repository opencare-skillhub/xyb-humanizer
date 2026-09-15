# Audit Workflow

Use this when the user wants diagnosis before rewriting, or when running regression tests.

## Output dimensions
Score each 1–5:
- Naturalness
- Author voice
- AI Pattern（5 = AI 痕迹很少）
- Readability
- Information density
- Medical accuracy
- Evidence calibration
- Fear/urgency control
- Hope/hype control
- Meaning preservation

## Audit process
1. Identify high-confidence AI patterns.
2. Identify sentences that are merely formal, not necessarily AI-like.
3. Identify medical claims whose certainty may be overstated.
4. Identify emotional manipulation, fear, guilt, or artificial urgency.
5. Identify voice mismatches.
6. Propose the smallest useful set of edits.

## Output
```text
Humanization audit
Naturalness: x/5
Voice: x/5
AI-pattern: x/5
Medical accuracy: x/5
Evidence calibration: x/5
Fear control: x/5
Meaning preservation: x/5

Priority edits:
1. ...
2. ...
3. ...

Medical review needed:
- ...
```

Do not claim that a detector score proves authorship or humanization quality.
