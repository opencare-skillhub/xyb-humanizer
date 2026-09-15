# Voice Profile System

The Humanizer supports a user-defined voice profile. A voice profile is a writing specification, not a personality impersonation.

## Priority
When multiple profiles exist:
1. User explicitly requested style in the current prompt.
2. Project-specific VOICE.md / voice profile.
3. Named profile such as `voice-sam.md`.
4. Default Xiaoyibao voice.
5. Generic humanization rules.

## Recommended files
```text
references/
├── voice-sam.md
├── voice-profile.md
└── voices/
    ├── project.md
    └── community.md
```

## Build your own voice
Provide 5–10 pieces of writing that you genuinely like. Ideally include different contexts: one long article, one short post, one explanatory passage, and one opinion/analysis piece.

The profile should describe patterns, not copy sentences.

Capture:
- tone
- sentence rhythm
- paragraph length
- vocabulary
- level of technicality
- directness
- use of first person
- use of humor
- preferred transitions
- how conclusions are written
- words/phrases you avoid
- how uncertainty is expressed
- how strongly you state opinions

## Voice extraction prompt
Use:

"Analyze these writing samples and create a reusable voice profile. Describe stable stylistic patterns rather than copying distinctive sentences. Separate tone, syntax, rhythm, vocabulary, structure, stance, uncertainty, and things to avoid. Do not infer personal biography or identity that is not explicitly present."

## Voice validation
After creating a profile, test it on 3 unseen texts.

Ask a blind reviewer:
- Does the output sound like the same author?
- Did the style survive without copying phrases?
- Did the model add personality that was not in the samples?
- Did it make the writing more uniform?

If the last answer is yes, the profile is too prescriptive.
