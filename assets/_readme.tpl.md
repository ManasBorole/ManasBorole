{{board}}

Most of what I build sits underneath AI products, in the parts that tend to break once real users show up. Lately that has mostly been voice agents and LLM routing.

Right now I am a software engineer at a UK RegTech fintech, and on the side I am teaching AI phone agents when to stop talking.

[Portfolio](https://manasos.vercel.app) &nbsp;&#183;&nbsp; [LinkedIn](https://linkedin.com/in/manasborole) &nbsp;&#183;&nbsp; [Email](mailto:manasborole0712@gmail.com)

<sub>Most of my day-to-day work is in private codebases, so this page covers the things I built on my own.</sub>

## Multiplexer

An LLM gateway that learns, per request, which of 13 models to call. LinUCB scores each request on cost, latency and quality, a judge grades the answer, and the grade feeds back into the router. When a model fails, the next healthy one answers.

{{atc}}

The panel above replays 500 requests from its benchmark. On the Balanced setting it keeps about three quarters of the flagship's quality for under 5% of the cost. Most of the work went into designing the reward function.

{{video:mx}}

[Try it](https://multiplexer-routes.vercel.app) &nbsp;&#183;&nbsp; [Source](https://github.com/ManasBorole/Multiplexer) &nbsp;&#183;&nbsp; <sub>TypeScript, Next.js, OpenRouter, Upstash</sub>

## Christopher

A language tutor you talk to out loud, in 183 languages. Speech goes straight from the browser to OpenAI's Realtime API over WebRTC, so replies come back fast enough to feel like a conversation. It grades pronunciation from the audio itself. Speech-to-text tends to clean up mispronounced words, so grading from a transcript would miss most mistakes.

{{postcards}}

The tricky part was turn-taking. It waits for 550 ms of silence before deciding you have finished, which is long enough for a learner to hunt for a word without being interrupted.

{{video:ch}}

[Try it](https://christopherai.vercel.app) &nbsp;&#183;&nbsp; [Source](https://github.com/ManasBorole/Christopher) &nbsp;&#183;&nbsp; <sub>WebRTC, OpenAI Realtime, React</sub>

## Building now

### Backchannel

Voice agents rarely fail on what they say. They fail on when: jumping in before the caller finishes, talking over them, or leaving a silence that feels like a dropped call. Backchannel finds those moments in calls on Vapi, to the millisecond, and works out which turn-taking settings would have prevented them, with the evidence attached.

{{backchannel}}

<details>
<summary>How it works, and where it stands</summary>
<br>

- Speech is detected on the caller and agent channels separately, with my own wrapper around Silero VAD, so overlaps and gaps are measured from the audio rather than guessed from a transcript.
- A simulator of Vapi's own endpointing predicts when the agent would have started speaking, for any recorded call and any configuration. That means thousands of settings can be tested offline for free instead of paying for trial calls.
- The best candidates are confirmed with paired real replays, then rolled out to a small share of calls first.
- The live demo is a fictional clinic with AI receptionists answering the phone. You can call it and then see the diagnosis of your own call, with the problem moments marked on a timeline and the suggested fix.

Done so far: the architecture and spec, a voice-detection layer that catches the start of speech within 18 ms at 60 to 150 times real time, the web-call pipeline, and durable background jobs. Next come the detectors and the endpointing simulator.

The targets I am holding myself to: simulator timing within 150 ms median error, published; detectors at 0.85 precision or better on hand-labelled turns; and before-and-after numbers on 50+ calls.

<sub>TypeScript, Next.js, Vapi, Silero VAD (ONNX), Vercel Workflow, Neon Postgres, Cloudflare R2</sub>
</details>

Everyone measures how fast voice agents respond. Almost nobody measures whether they let you finish, and being cut off mid-sentence is the moment a caller decides they are talking to a machine. <sub>In active development, built in public. Live demo coming soon.</sub>

### Odyssey

An agent that turns a team's messages, emails and CRM webhooks into writes on live HubSpot and Xero accounts, but only after a person approves them.

{{customs}}

Agents don't fail because they aren't smart enough. They fail because nobody will give them write access. So I built the permission layer first: one approval queue for every trigger, an allowlist that blocks hallucinated or injected writes, idempotency keys so a retry never writes twice, and per-user OAuth with encrypted tokens and signed webhooks.

[Try it](https://odysseylabs.vercel.app) &nbsp;&#183;&nbsp; <sub>Next.js, TypeScript, Anthropic and OpenAI, HubSpot, Xero, Prisma</sub>

## Also built

<table>
<tr>
<td width="50%"><a href="https://manasos.vercel.app"><img src="https://raw.githubusercontent.com/ManasBorole/ManasBorole/main/assets/projects/kazumi-thumb.png" width="100%" alt="Kazumi"></a><br>Kazumi, an AI wellbeing platform. I was tech lead for a team of five.</td>
<td width="50%"><a href="https://github.com/ManasBorole/CryptChain"><img src="https://raw.githubusercontent.com/ManasBorole/ManasBorole/main/assets/projects/cryptchain-thumb.png" width="100%" alt="CryptChain"></a><br>CryptChain, a blockchain in plain Java with SHA-256 and proof-of-work, written from scratch.</td>
</tr>
<tr>
<td width="50%"><a href="https://manasos.vercel.app"><img src="https://raw.githubusercontent.com/ManasBorole/ManasBorole/main/assets/projects/credit-thumb.png" width="100%" alt="Credit score classifier"></a><br>A random-forest credit score classifier, 85%+ accurate across tiers.</td>
<td width="50%"><a href="https://manasos.vercel.app"><img src="https://raw.githubusercontent.com/ManasBorole/ManasBorole/main/assets/projects/music-thumb.png" width="100%" alt="Music recommender"></a><br>A music recommender built on the Spotify API.</td>
</tr>
</table>

## How I work

Ship it, or it isn't real. A demo nobody uses is a nicer way of not finishing.<br>
Measure first. Guessing at bottlenecks spends a week to save a millisecond.<br>
Small systems age well. Fewer moving parts, fewer 3am pages.<br>
Own the whole thing, including the parts nobody else wants.

## How I got here

{{passes}}

<details>
<summary>The full timeline</summary>
<br>

| | | |
|---|---|---|
| 2020 | B.Tech in CS (AI/ML), Sandip University | Graduated 2024 with a CGPA of 8.27. Ran hackathons with SUAISA. |
| 2022 | Founder, B&B Fashion | Ran a real business end to end and learned what shipping costs. |
| 2023 | Co-founder, Gullak | One of two founding engineers on an investing platform in Nashik. |
| 2024 | Software Development Engineer, IQCPL | Built the certification and audit backend for 20+ clients in Pune. Cut auditor coordination by about 30%. |
| 2026 | Shipped Odyssey, Multiplexer and Christopher | All three are live with public demos. |
| 2026 | Software engineer, UK RegTech fintech (remote) | Closed 7 unauthenticated endpoints and put 450+ tests behind the flows. |
| Next | A company of my own | |

</details>

## What I use

| | |
|---|---|
| AI | LLM agents, tool calling, Anthropic and OpenAI SDKs, LLM-as-judge evals, contextual bandits, semantic caching |
| Agent safety | Human approval steps, prompt-injection defence, server-side allowlists, fail-closed auth, idempotent writes |
| Voice | WebRTC, OpenAI Realtime, Vapi, Silero VAD, turn-taking and endpointing |
| Backend | Python, Django, FastAPI, Node.js, Java with Spring Boot, outbox and retry workers, circuit breakers, webhook reconciliation |
| Data | PostgreSQL, Prisma, Neon, Redis, append-only audit trails |
| Frontend | TypeScript, React, Next.js, Tailwind, Zustand |
| Security | OAuth 2.0, OIDC, RBAC, row-level security, multi-tenancy, KMS encryption |
| Testing | Vitest, Playwright, pytest, GitHub Actions |

## Say hi

{{arrivals}}

If you are working on something similar, or want to talk about any of these projects, send me an email or message me on LinkedIn.

[Email](mailto:manasborole0712@gmail.com) &nbsp;&#183;&nbsp; [LinkedIn](https://linkedin.com/in/manasborole) &nbsp;&#183;&nbsp; [Portfolio](https://manasos.vercel.app)
