# Impeccable review (critique + audit, Persuade/Experience surface): oldschool profile

Verdict: identity is strong and coherent (paper, receipt, folder, tickets) and the hierarchy reads in one pass. The main risks are mobile legibility of sub-12px SVG text, low-contrast muted text, and entrance animations that finish before below-fold cards are seen.

Basis: read of `variants/oldschool.md`, `gen/themes/oldschool.py` (grep of sizes, animation and filter lines, not a full read), and `previews/oldschool.png`. I did not render my own checks. Mobile numbers below are calculated from viewBox widths, not measured on a device.

## Content

1. Small text collapses on mobile (`project-1..4`, `link-*`, `lvc`, `desk`). The half-width cards are about 49% of a roughly 375px column, so about 180px for a card about 440px wide, a scale of about 0.41. That puts 12.5px log text near 5px, the 10.5px `cap` captions near 4px, and the 13px descriptions near 5px. Principle: readable at the size it ships. Change: in `gen/themes/oldschool.py` set a floor of 13px for anything meant to be read (the log at line 237-239, captions at line 111, project descriptions, "SIX MODULES" and "VALIDATED ON" sub-lines). Keep 10-11px only for decorative labels such as "No. 01". Cut the project description to one line of at most 38 characters, for example "gRPC client and server, one Protobuf contract". Stack the four project cards one per row on mobile if the README structure allows it. GitHub has no media queries, so the option that works for both sizes is making the cards taller with larger type.

2. Muted text contrast. The `MUT` grey sub-lines ("replay an immutable log", "docker compose up", "illustrative", "Source code, 6 modules", "Write to me") look about 3:1 or lower on `PAPER` in the preview. Principle: WCAG AA is 4.5:1 for text under 18px. Change: darken `MUT` text, not rules, to about `#5f574a` or darker. Check it with a contrast calculator against `PAPER`. Keep the current lighter grey for dotted leaders only.

3. Alt text omits the hero pull-quote. The visible line "If it can be deterministic, it should not be inference." is the strongest message on the page, but the hero alt (README line 2) does not carry it. Change: append "Tagline: if it can be deterministic, it should not be inference." to the hero alt. Also give the `link-code`/`link-paper` alts a purpose ("Open the source code on GitHub").

4. Link destinations mismatch the visible meaning. The `record` card (README line 28) and the hero both link to LinkedIn, but the record card shows metrics with no source. Change: leave the hero as is. For `record`, either keep the LinkedIn link and add a caption "Source: Getnet and Samsung SDS, internal metrics" inside the card (a 12px line under the tickets), or drop the link so the card is not a dead-end click.

5. The "2 days" ticket is red and the other three are black. It reads as emphasis, which is fine, but the other three metrics are equally strong. Change: keep red for "2 days" only if it stays the lead claim. Otherwise set all four to INK and keep red for the rule lines only. Low priority.

## Animations

1. Entrances play on image load, not on scroll. Cards below the fold (`record`, `desk`, `project-*`) finish before they are seen, so the choreography is lost and the stagger only adds delay. Change: cap total delay per card at 700ms (hero and `lvc` can keep their 1.4-1.5s print and log sequences). Do not extend durations on lower cards.

2. The event log in `lvc.svg` (line 240) scrolls with `9s linear infinite` right under text the reader is trying to read. Continuous motion beside body copy hurts reading. Change: use stepped rows, for example `steps(1)` per row with a 2.2s dwell and a 300ms `cubic-bezier(.22,1,.36,1)` slide, or stop after one loop. The row-by-row change also makes the "append-only" idea visible.

3. The terminal loop in `desk.svg` (lines 282-285) and the blinking cursors (`1.1s steps(1) infinite`, lines 52 and 289) are the correct kind of motion, but three infinite loops on a page add up. Change: keep the terminal loop, and limit the cursor to the hero and the terminal. If a card shows an unused cursor, remove it.

4. Reduced motion is handled (lines 58-60: fade at 300ms, loops stopped). Verify that the stopped state is a complete frame: the terminal loop keyframes (line 282-284) end at `opacity:0` at 95-100%, so with `animation:none` the lines must be visible by default. The preview is static, so this was not confirmed. Check by rendering with `prefers-reduced-motion: reduce` and animations on.

5. The photo "develop" fade (`dev`, 2.4s, delay 700ms) is a good touch. Keep the easing, but shorten to 1.6s so it ends while the receipt is still printing.

## GitHub integration

1. Weight. Each SVG is 91-111KB, 12 cards, roughly 1.2MB total, mostly the repeated `feTurbulence` grain filter (lines 71-77) and probably embedded fonts and the avatar. This is under the Camo ceiling but the grain filter is expensive to rasterize on mobile. Change: apply the grain `G` filter once per card on the largest sheet only, not on every `sheet()` call, or replace it with a pre-rendered 64px noise tile as a data-URI `<pattern>`. Target under 60KB per small card. Check the actual cause before changing anything (I did not inspect what dominates the byte size).

2. Dark/light. Every card brings its own dark desk, so both GitHub themes look the same. That is good for identity. The risk is the 6px `rx` corner showing GitHub's background as a light halo in light mode. Change: add a 1px `#0d0c0a` outline on the desk rect, or use `rx` 8 on all cards so corners match. Check a light-theme render.

3. Tap targets on mobile. `link-*` cards are about 180px wide and about 40px tall after scaling, which is workable. The project cards are taller and fine. No change needed, but keep `width="49%"` pairs wrapped in one `<p align="center">` so they stack predictably.

4. The alt text for project cards does not match the visible description (card says "OAuth2 resource server, RSA-signed JWT", alt says "stateless auth with Spring Security 6 and JWT"). Screen reader users get a different claim than sighted users. Change: copy the visible text into the alt.

5. Image-only layout with no text fallback: if images fail to load (Camo hiccup), the page is only alt text. Change: add one plain-text line at the end of the README with the three key links (paper, code, LinkedIn). It costs one line and covers failures and text-only browsers.

## Do not change

- Receipt hero with the numbered leader-dot list and the "APPROVED" stamp; it carries identity.
- Pull-quote "If it can be deterministic, it should not be inference."
- Manila folder + stamped "PRESENTED / PROCEEDINGS SOON" on the paper card; the honest status is good.
- Sequence: hero, paper, code and paper links, four projects, tools, record, contact. Lean and no endless scroll.
- Single typographic system: condensed serif display, monospace body, red as the only accent.
- Reduced-motion fallback structure and the `ease-out` easing constant.
- The "illustrative" tag on the event log; it keeps the demo honest.
