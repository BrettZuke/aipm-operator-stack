# Skills index

Install them all once:

```bash
cp -R skills/* ~/.claude/skills/
rm -f ~/.claude/skills/INDEX.md
```

304 skills. **21 of them exist nowhere else**, and with one exception they are the entire
video toolchain: captions, overlay cards, motion design, HyperFrames, Remotion, FFmpeg.
That was the real gap.

The other 24 also appear in
[aipm-skill-pack](https://github.com/BrettZuke/aipm-skill-pack) or
[ai-partner-method-claude-starter](https://github.com/BrettZuke/ai-partner-method-claude-starter),
byte for byte. They are duplicated here on purpose so one command installs everything you
need for a creator client, rather than three commands and a mental note about which pack
held what.

Install those two packs anyway. Between them they carry another 70-odd skills, including
`client-brand`, `seo-maps`, and the wider design and SEO sets that are outside this
fulfilment path but useful once a client asks for them.

---

## Phase 1: onboarding and brand voice

| Skill | Use it when |
|---|---|
| `analyze-creator` | Fast read on one account: what they post, what works, how often |
| `avoid-ai-writing` | Every piece of copy before it reaches the client. Non-negotiable |
| `stop-slop` | Deeper rewrite when copy already sounds like a robot wrote it |
| `brand` | Turning the voice document into a usable brand system: colour, type, tone |

## Phase 2: research and intelligence

| Skill | Use it when |
|---|---|
| `spy` | Pulling a competitor's viral outliers and transcribing the hooks |
| `scraper` | A page fights back and the normal scrape fails |
| `content-audit` | Judging an existing content library: what is working, what to stop |
| `script` | Turning a research finding into a written piece |

## Phase 4: content

| Skill | Use it when |
|---|---|
| `viral-hook-creator` | Writing hooks by hand, or improving what the scripter produced |
| `viral` | The wider viral-content patterns |
| `viral-tiktok-content` | Short-form specifically, platform conventions included |
| `content-director` | Deciding the content strategy rather than writing one piece |
| `ugc-content-creator` | UGC-style content, where it reads as a customer not a brand |
| `carousel-builder` | Instagram and LinkedIn carousels, rendered to finished slides |
| `copywriting` | General conversion copy |
| `creative-copywriting-master` | When straight copy is not landing and it needs an angle |
| `ogilvy-copywriting` | Long-form and direct response. Read before writing a sales page |
| `copy-editing` | Tightening a draft that is already right in substance |

## Phase 5: VSL, funnel and video

| Skill | Use it when |
|---|---|
| `high-end-visual-design` | Every page build. Load before you write markup |
| `frontend-design` | Building the components themselves |
| `design-review` | Reviewing a page before it goes live |
| `page-cro` | The page is live and not converting |
| `premium-funnel-page` | Opt-in, VSL and post-booking pages specifically |
| `lead-magnet-builder` | Building the thing people opt in for |

### Video

| Skill | Use it when |
|---|---|
| `general-video` | The starting point when you are not sure which video skill fits |
| `ffmpeg-video-editor` | Natural language to an FFmpeg command: cut, convert, compress, resize |
| `ffmpeg` | The deeper FFmpeg reference |
| `auto-captions` | Fastest route to captions on a clip |
| `embedded-captions` | Burning captions into the file itself |
| `cinematic-caption` | Hero pieces. Scales the words that carry the claim, places them with depth |
| `talking-head-recut` | Graphic overlay cards on a talking-head video, synced to transcript |
| `motion-design` | Timing, easing and choreography. Read before animating anything |
| `motion-graphics` | Building the graphics |
| `hyperframes` | The overlay and render engine. Start here |
| `hyperframes-core` | The core rendering model |
| `hyperframes-cli` | Driving it from the command line |
| `hyperframes-media` | Video, image and audio handling |
| `hyperframes-animation` | Animating the overlays |
| `hyperframes-keyframes` | Keyframe-level control |
| `hyperframes-creative` | The creative patterns and worked looks |
| `hyperframes-registry` | The component registry |
| `remotion`, `remotion-best-practices`, `remotion-motion-graphics` | React-based compositions, the primary engine for graphics work |

The seven-stage pipeline that ties these together is in [`../video-system/`](../video-system/).
Read `video-system/README.md` before using the video skills individually.

## Phase 6 and ongoing

| Skill | Use it when |
|---|---|
| `sales-call-analyzer` | Mining call transcripts for content ideas and objections |

---

## The rest of the library

The 166 skills below came with the environment and are not part of the six-phase
path. They are here because you asked for everything. Scan the list once so you know what
exists, then reach for one when its job comes up.

| Skill | What it does |
|---|---|
| `agent-reach` | > |
| `ai-regression-testing` | Regression testing strategies for AI-assisted development |
| `aiw-stack` | | |
| `android-clean-architecture` | Clean Architecture patterns for Android and Kotlin Multiplatform projects , module structure, dependency rules |
| `api-design` | REST API design patterns including resource naming, status codes, pagination, filtering, error responses, vers |
| `apple-scroll-hero` | Build an Apple-style scroll-scrub hero section where a video plays forward frame by frame as the user scrolls, |
| `autoplan` | | |
| `backend-patterns` | Backend architecture patterns, API design, database optimization, and server-side best practices for Node.js,  |
| `banner-design` | Design banners for social media, ads, website heroes, creative assets, and print |
| `benchmark` | | |
| `benchmark-models` | | |
| `bencium-ux-designer` | Create distinctive, production-grade frontend interfaces with high design quality |
| `browse` | | |
| `business-council` | >- |
| `canary` | | |
| `careful` | | |
| `cmo` | > |
| `codex` | | |
| `coding-standards` | Universal coding standards, best practices, and patterns for TypeScript, JavaScript, React, and Node.js develo |
| `compose-multiplatform-patterns` | Compose Multiplatform and Jetpack Compose patterns for KMP projects , state management, navigation, theming, p |
| `configure-ecc` | Interactive installer for Everything Claude Code , guides users through selecting and installing skills and ru |
| `context-restore` | | |
| `context-save` | | |
| `continuous-learning` | Automatically extract reusable patterns from Claude Code sessions and save them as learned skills for future u |
| `continuous-learning-v2` | Instinct-based learning system that observes sessions via hooks, creates atomic instincts with confidence scor |
| `coo` | > |
| `copy` | > |
| `cpp-coding-standards` | C++ coding standards based on the C++ Core Guidelines (isocpp.github.io) |
| `cpp-testing` | Use only when writing/updating/fixing C++ tests, configuring GoogleTest/CTest, diagnosing failing or flaky tes |
| `cso` | | |
| `css-animation` | Generates self-contained HTML/CSS animations of app features for walkthroughs, demos, and onboarding |
| `daily-intel` | A daily content-intelligence briefing for your niche, delivered to Telegram |
| `design` | Comprehensive design skill: brand identity, design tokens, UI styling, logo generation (55 styles, Gemini AI), |
| `design-consultation` | | |
| `design-html` | | |
| `design-loop` | Autonomous multi-page site builder using a baton-passing loop pattern |
| `design-motion-principles` | Expert motion and interaction design auditor based on Emil Kowalski, Jakub Krehel, and Jhey Tompkins' techniqu |
| `design-shotgun` | | |
| `design-system` | Token architecture, component specifications, and slide generation |
| `design-taste-frontend` | Senior UI/UX Engineer |
| `devex-review` | | |
| `distinctive-frontend` | Create visually distinctive, high-impact frontend interfaces that avoid generic AI aesthetics |
| `django-patterns` | Django architecture patterns, REST API design with DRF, ORM best practices, caching, signals, middleware, and  |
| `django-tdd` | Django testing strategies with pytest-django, TDD methodology, factory_boy, mocking, coverage, and testing Dja |
| `django-verification` | Verification loop for Django projects: migrations, linting, tests with coverage, security scans, and deploymen |
| `document-release` | | |
| `e2e-testing` | Playwright E2E testing patterns, Page Object Model, configuration, CI/CD integration, artifact management, and |
| `eval-harness` | Formal evaluation framework for Claude Code sessions implementing eval-driven development (EDD) principles |
| `faceless-explainer` | turn arbitrary text , an article, notes, a topic, a brief , into a faceless explainer video, up to ~3 min (swe |
| `find-skills` | Helps users discover and install agent skills when they ask questions like "how do I do X", "find a skill for  |
| `first-business` | > |
| `freeze` | | |
| `frontend-patterns` | Frontend development patterns for React, Next.js, state management, performance optimization, and UI best prac |
| `frontend-slides` | Create stunning, animation-rich HTML presentations from scratch or by converting PowerPoint files |
| `full-output-enforcement` | Overrides default LLM truncation behavior |
| `golang-patterns` | Idiomatic Go patterns, best practices, and conventions for building robust, efficient, and maintainable Go app |
| `golang-testing` | Go testing patterns including table-driven tests, subtests, benchmarks, fuzzing, and test coverage |
| `graphify` | Use for any question about a codebase, its architecture, file relationships, or project content , especially w |
| `gstack` | | |
| `gstack-openclaw-ceo-review` | Use when asked to review a plan, challenge a proposal, run a CEO review, poke holes in an approach, think bigg |
| `gstack-openclaw-investigate` | Use when asked to debug, fix a bug, investigate an error, or do root cause analysis, and when users report err |
| `gstack-openclaw-office-hours` | Use when asked to brainstorm, evaluate whether an idea is worth building, run office hours, or think through a |
| `gstack-openclaw-retro` | Weekly engineering retrospective |
| `gstack-upgrade` | | |
| `guard` | | |
| `head-of-development` | > |
| `head-of-strategy` | > |
| `health` | | |
| `idea-hacker` | Turn one idea into a full week of content |
| `impeccable` | Use when the user wants to design, redesign, shape, critique, audit, polish, clarify, distill, harden, optimiz |
| `industrial-brutalist-ui` | Raw mechanical interfaces fusing Swiss typographic print with military terminal aesthetics |
| `interface-design` | This skill is for interface design , dashboards, admin panels, apps, tools, and interactive products |
| `investigate` | | |
| `iterative-retrieval` | Pattern for progressively refining context retrieval to solve the subagent context problem |
| `java-coding-standards` | Java coding standards for Spring Boot services: naming, immutability, Optional usage, streams, exceptions, gen |
| `kotlin-coroutines-flows` | Kotlin Coroutines and Flow patterns for Android and KMP , structured concurrency, Flow operators, StateFlow, e |
| `kotlin-exposed-patterns` | JetBrains Exposed ORM patterns including DSL queries, DAO pattern, transactions, HikariCP connection pooling,  |
| `kotlin-ktor-patterns` | Ktor server patterns including routing DSL, plugins, authentication, Koin DI, kotlinx.serialization, WebSocket |
| `kotlin-patterns` | Idiomatic Kotlin patterns, best practices, and conventions for building robust, efficient, and maintainable Ko |
| `kotlin-testing` | Kotlin testing patterns with Kotest, MockK, coroutine testing, property-based testing, and Kover coverage |
| `land-and-deploy` | | |
| `laravel-patterns` | Laravel architecture patterns, routing/controllers, Eloquent ORM, service layers, queues, events, caching, and |
| `laravel-tdd` | Test-driven development for Laravel with PHPUnit and Pest, factories, database testing, fakes, and coverage ta |
| `laravel-verification` | Verification loop for Laravel projects: env checks, linting, static analysis, tests with coverage, security sc |
| `learn` | | |
| `libre-uiux` | Grand orchestrator for comprehensive UI/UX , coordinates design mastery, accessibility, performance, and testi |
| `llm-council` | Run any question, idea, or decision through a council of 5 AI advisors who independently analyze it, peer-revi |
| `make-interfaces-feel-better` | > |
| `make-pdf` | | |
| `mcp-server-patterns` | Build MCP servers with Node/TypeScript SDK , tools, resources, prompts, Zod validation, stdio vs Streamable HT |
| `media-use` | Agent Media OS , resolve any media need (BGM, SFX, image, icon) into a frozen local file + ledger record |
| `meta-rate-limiter` | Manage Meta (Facebook/Instagram) ads API calls without ever hitting rate limits |
| `minimalist-ui` | Clean editorial-style interfaces |
| `music-to-video` | Use when the user has a music track (an audio file, or a video to pull audio from) and wants a beat-synced Hyp |
| `my-lead-magnet-system` |  |
| `office-hours` | | |
| `open-gstack-browser` | | |
| `pair-agent` | | |
| `perl-patterns` | Modern Perl 5.36+ idioms, best practices, and conventions for building robust, maintainable Perl applications. |
| `perl-testing` | Perl testing patterns using Test2::V0, Test::More, prove runner, mocking, coverage with Devel::Cover, and TDD  |
| `plan-ceo-review` | | |
| `plan-design-review` | | |
| `plan-devex-review` | | |
| `plan-eng-review` | | |
| `plan-tune` | | |
| `plankton-code-quality` | Write-time code quality enforcement using Plankton , auto-formatting, linting, and Claude-powered fixes on eve |
| `pr-to-video` | turn a GitHub pull request (a PR URL like github.com/<owner>/<repo>/pull/<N>, an <owner>/<repo>#<N> ref, or 't |
| `product-launch-video` | turn a product or marketing URL, pasted script, or brief into a product launch video, including SaaS promos, f |
| `project-guidelines-example` | Example project-specific skill template based on a real production application. |
| `python-patterns` | Pythonic idioms, PEP 8 standards, type hints, and best practices for building robust, efficient, and maintaina |
| `python-testing` | Python testing strategies using pytest, TDD methodology, fixtures, mocking, parametrization, and coverage requ |
| `qa` | | |
| `qa-only` | | |
| `react-best-practices` | React and Next.js performance optimization guidelines from Vercel Engineering |
| `redesign-existing-projects` | Upgrades existing websites and apps to premium quality |
| `remotion-to-hyperframes` | 'Port an existing Remotion (React) composition to HyperFrames HTML |
| `repurpose` | > |
| `retro` | | |
| `review` | | |
| `rust-patterns` | Idiomatic Rust patterns, ownership, error handling, traits, concurrency, and best practices for building safe, |
| `rust-testing` | Rust testing patterns including unit tests, integration tests, async testing, property-based testing, mocking, |
| `scale` | > |
| `sdr` | > |
| `seo-audit` | Full website SEO audit with parallel subagent delegation |
| `seo-backlinks` | Backlink profile analysis: referring domains, anchor text distribution, toxic link detection, competitor gap a |
| `seo-cluster` | > |
| `seo-competitor-pages` | > |
| `seo-content` | > |
| `seo-dataforseo` | > |
| `seo-drift` | > |
| `seo-firecrawl` | > |
| `seo-google` | > |
| `seo-hreflang` | > |
| `seo-image-gen` | AI image generation for SEO assets: OG/social preview images, blog hero images, schema images, product photogr |
| `seo-images` | > |
| `seo-local` | > |
| `seo-page` | > |
| `seo-plan` | > |
| `seo-programmatic` | > |
| `seo-sitemap` | > |
| `seo-sxo` | > |
| `seo-technical` | > |
| `setup-browser-cookies` | | |
| `setup-deploy` | | |
| `ship` | | |
| `skill-stocktake` | Use when auditing Claude skills and commands for quality |
| `slides` | Create strategic HTML presentations with Chart.js, design tokens, responsive layouts, copywriting formulas, an |
| `slideshow` | > |
| `springboot-patterns` | Spring Boot architecture patterns, REST API design, layered services, data access, caching, async processing,  |
| `springboot-tdd` | Test-driven development for Spring Boot using JUnit 5, Mockito, MockMvc, Testcontainers, and JaCoCo |
| `springboot-verification` | Verification loop for Spring Boot projects: build, static analysis, tests with coverage, security scans, and d |
| `stitch-design-taste` | Semantic Design System Skill for Google Stitch |
| `strategic-compact` | Suggests manual context compaction at logical intervals to preserve context through task phases rather than ar |
| `task-observer` | > |
| `tdd-workflow` | Use this skill when writing new features, fixing bugs, or refactoring code |
| `transcreation` | Transcreation skill for multilingual content |
| `ui-styling` | Create beautiful, accessible user interfaces with shadcn/ui components (built on Radix UI + Tailwind), Tailwin |
| `ui-ux-pro-max` | UI/UX design intelligence for web and mobile |
| `unfreeze` | | |
| `verification-loop` | A comprehensive verification system for Claude Code sessions. |
| `viral-reel-generator` | Write short-form video scripts (TikTok, Reels, Shorts) with strict visual-to-audio sync and "anti-slop" writin |
| `watch` | Watch a video (URL or local path) |
| `web-design-guidelines` | Review UI code for Web Interface Guidelines compliance |
| `website-builder-setup` | Install the full AI website builder stack , UI/UX Pro Max, Framer Motion animations, and 21st.dev components |
| `website-to-video` | Capture a general website/URL and turn it into a HyperFrames video (site tour, showcase, or social clip from t |
| `wiki-brain` | Turn Claude Code into a knowledge base that compounds |

---

## Added from the starter kit and skill pack

Merged in when the student repos were consolidated. Engineering discipline, research,
and content production.

| Skill | Use it when |
|---|---|
| `asr-transcribe-to-text` | Transcribes audio and video files to text using Qwen3-ASR |
| `brainstorming` | You MUST use this before any creative work - creating features, building components, adding functionality, or ... |
| `capture-screen` | Programmatic screenshot capture on macOS |
| `cli-demo-generator` | Generates professional animated CLI demos as GIFs using VHS terminal recordings |
| `client-brand` | Create or update a saved brand file for one of the user's clients (local business or online coach) at ~/.claud... |
| `competitors-analysis` | Analyze competitor repositories with evidence-based approach |
| `debugging-network-issues` | Evidence-driven investigation for network, streaming, and protocol-layer bugs |
| `deep-research` | | Generate format-controlled research reports with evidence tracking, citations, source governance, and multi-... |
| `dispatching-parallel-agents` | Use when facing 2+ independent tasks that can be worked on without shared state or sequential dependencies |
| `editorial-luxury-site` | Build a premium "Editorial Luxury" one-page site, the fancy showpiece kind (sticky photo hero the page scrolls... |
| `excel-automation` | Create, parse, and control Excel files on macOS |
| `executing-plans` | Use when you have a written implementation plan to execute in a separate session with review checkpoints |
| `fact-checker` | Verifies factual claims in documents using web search and official sources, then proposes corrections with use... |
| `finishing-a-development-branch` | Use when implementation is complete, all tests pass, and you need to decide how to integrate the work - guides... |
| `github-contributor` | Strategic guide for becoming an effective GitHub contributor |
| `github-ops` | Provides comprehensive GitHub operations using gh CLI and GitHub API |
| `llm-icon-finder` | Finding and accessing AI/LLM model brand icons from lobe-icons library |
| `macos-cleaner` | Analyze and reclaim macOS disk space through intelligent cleanup recommendations |
| `product-analysis` | Multi-path parallel product analysis with cross-model test-time compute scaling |
| `prompt-optimizer` | Transform vague prompts into precise, well-structured specifications using EARS (Easy Approach to Requirements... |
| `qa-expert` | This skill should be used when establishing comprehensive QA testing processes for any software project |
| `receiving-code-review` | Use when receiving code review feedback, before implementing suggestions, especially if feedback seems unclear... |
| `repomix-safe-mixer` | Safely package codebases with repomix by automatically detecting and removing hardcoded credentials before pac... |
| `repomix-unmixer` | Extracts files from repomix-packed repositories, restoring original directory structures from XML/Markdown/JSO... |
| `requesting-code-review` | Use when completing tasks, implementing major features, or before merging to verify work meets requirements |
| `skill-creator` | Create new skills, modify and improve existing skills, and measure skill performance |
| `skill-reviewer` | Reviews and improves Claude Code skills against official best practices |
| `skills-search` | This skill should be used when users want to search, discover, install, or manage Claude Code skills from the ... |
| `slides-creator` | Narrative-first slide deck creation |
| `subagent-driven-development` | Use when executing implementation plans with independent tasks in the current session |
| `systematic-debugging` | Use when encountering any bug, test failure, or unexpected behavior, before proposing fixes |
| `teams-channel-post-writer` | Creates educational Teams channel posts for internal knowledge sharing about Claude Code features, tools, and ... |
| `test-driven-development` | Use when implementing any feature or bugfix, before writing implementation code |
| `transcript-fixer` | Corrects speech-to-text transcription errors using dictionary rules and AI-powered analysis |
| `twitter-reader` | Fetch Twitter/X post content including long-form Articles with full images and metadata |
| `ui-designer` | Extract design systems from reference UI images and generate implementation-ready UI design prompts |
| `using-git-worktrees` | Use when starting feature work that needs isolation from current workspace or before executing implementation ... |
| `using-superpowers` | Use when starting any conversation - establishes how to find and use skills, requiring Skill tool invocation b... |
| `verification-before-completion` | Use when about to claim work is complete, fixed, or passing, before committing or creating PRs - requires runn... |
| `video-comparer` | This skill should be used when comparing two videos to analyze compression results or quality differences |
| `writing-plans` | Use when you have a spec or requirements for a multi-step task, before touching code |
| `writing-skills` | Use when creating new skills, editing existing skills, or verifying skills work before deployment |
| `youtube-downloader` | Download YouTube videos and HLS streams (m3u8) from platforms like Mux, Vimeo, etc |

---

## Marketing skills (open source)

49 skills from open source projects, mostly Corey Haines' marketing pack. This is
the set that maps directly onto the work: finding clients, writing the outreach, building
the offer, and making the site convert. See [ATTRIBUTION.md](../ATTRIBUTION.md).

| Skill | Use it when |
|---|---|
| `ab-testing` | When the user wants to plan, design, or implement an A/B test or experiment, or build a growth experiment... |
| `ad-creative` | When the user wants to generate, iterate, or scale ad creative — headlines, descriptions, primary text, o... |
| `ads` | When the user wants help with paid advertising campaigns on Google Ads, Meta (Facebook/Instagram), Linked... |
| `ai-seo` | When the user wants to optimize content for AI search engines, get cited by LLMs, or appear in AI-generat... |
| `analytics` | When the user wants to set up, improve, or audit analytics tracking and measurement |
| `aso` | When the user wants to audit or optimize an App Store or Google Play listing |
| `attribution` | When the user wants to figure out which marketing actually drives conversions and revenue, choose or inte... |
| `churn-prevention` | When the user wants to reduce churn, build cancellation flows, set up save offers, recover failed payment... |
| `co-marketing` | When the user wants to find co-marketing partners, plan joint campaigns, or brainstorm partnership opport... |
| `cold-email` | Write B2B cold emails and follow-up sequences that get replies |
| `community-marketing` | Build and leverage online communities to drive product growth and brand loyalty |
| `competitor-profiling` | When the user wants to research, profile, or analyze competitors from their URLs |
| `competitors` | When the user wants to create competitor comparison or alternative pages for SEO and sales enablement |
| `content-strategy` | When the user wants to plan a content strategy, decide what content to create, or figure out what topics ... |
| `cro` | When the user wants to optimize, improve, or increase conversions on any marketing page or form — includi... |
| `customer-research` | When the user wants to conduct, analyze, or synthesize customer research |
| `directory-submissions` | When the user wants to submit their product to startup, SaaS, AI, agent, MCP, no-code, or review director... |
| `emails` | When the user wants to create or optimize an email sequence, drip campaign, automated email flow, or life... |
| `events` | When the user wants to plan, run, sponsor, speak at, or get pipeline from events — webinars, conferences,... |
| `free-tools` | When the user wants to plan, evaluate, or build a free tool for marketing purposes — lead generation, SEO... |
| `hallmark` | Anti-AI-slop design skill for greenfield pages, audits, redesigns, and design extraction from URLs or scr... |
| `image` | When the user wants to create, generate, edit, or optimize images for marketing — blog heroes, social gra... |
| `influencer-marketing` | When the user wants to run influencer, creator, or ambassador partnerships to promote their product — fin... |
| `launch` | When the user wants to plan a product launch, feature announcement, or release strategy |
| `lead-magnets` | When the user wants to create, plan, or optimize a lead magnet for email capture or lead generation |
| `marketing-council` | When the user wants multiple expert perspectives on a marketing question — a simulated board of advisors ... |
| `marketing-ideas` | When the user needs marketing ideas, inspiration, or strategies for their SaaS or software product |
| `marketing-loops` | When the user wants to set up a recurring, self-running marketing workflow — a repeatable loop an AI agen... |
| `marketing-plan` | When the user needs a comprehensive marketing plan for a client, a company they advise, or their own product |
| `marketing-psychology` | When the user wants to apply psychological principles, mental models, or behavioral science to marketing |
| `offers` | When the user wants to design, construct, or improve an offer — the thing they actually sell — including ... |
| `onboarding` | When the user wants to optimize post-signup onboarding, user activation, first-run experience, or time-to... |
| `paywalls` | When the user wants to create or optimize in-app paywalls, upgrade screens, upsell modals, or feature gates |
| `planning-with-files` | Persistent file-based planning for multi-step AI-agent work |
| `popups` | When the user wants to create or optimize popups, modals, overlays, slide-ins, or banners for conversion ... |
| `pricing` | When the user wants help with pricing decisions, packaging, or monetization strategy |
| `product-marketing` | When the user wants to create or update their product marketing context document |
| `programmatic-seo` | When the user wants to create SEO-driven pages at scale using templates and data |
| `prospecting` | When the user wants to find, qualify, and build a list of prospects to reach out to — across B2B SaaS, ge... |
| `public-relations` | When the user wants help with public relations, earned media, press coverage, journalist outreach, or med... |
| `referrals` | When the user wants to create, optimize, or analyze a referral program, affiliate program, or word-of-mou... |
| `revops` | When the user wants help with revenue operations, lead lifecycle management, or marketing-to-sales handof... |
| `sales-enablement` | When the user wants to create sales collateral, pitch decks, one-pagers, objection handling docs, or demo... |
| `schema` | When the user wants to add, fix, or optimize schema markup and structured data on their site |
| `signup` | When the user wants to optimize signup, registration, account creation, or trial activation flows |
| `site-architecture` | When the user wants to plan, map, or restructure their website's page hierarchy, navigation, URL structur... |
| `sms` | When the user wants to plan, build, or optimize SMS or MMS marketing — including welcome flows, abandoned... |
| `social` | When the user wants help creating, scheduling, or optimizing social media content for LinkedIn, Twitter/X... |
| `video` | When the user wants to create, generate, or produce video content using AI tools or programmatic frameworks |
