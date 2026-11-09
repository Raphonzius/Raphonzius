# taste review (tasteskill v2): oldschool variant

**Verdict:** The paper-world idea is right and the record card and the tagline are the only places where the page makes a claim and proves it. Everything else is dressing: kicker labels, numbered rows, stamps, a terminal, a tools list. It is built to be looked at, not read, and at phone width the 10-13px mono text is unreadable.

## Content

1. **Lead with the claim, not the form.** `hero.svg` (gen/themes/oldschool.py ~L128-185): the strongest line, "If it can be deterministic, it should not be inference.", is a side caption next to the polaroid. The receipt left of it restates the bio as a five-row list. Claim = the tagline; proof = record.svg. Change: make the tagline the hero headline at ~54px serif (current ~34px), on the receipt, and drop rows 01-05 to a single line "Java and Rust backends. gRPC. Event-driven. Open Finance and Pix at Getnet." Remove the numerals `01-05` (ordering that means nothing) and the `APPROVED` stamp (approved by whom?).
2. **Move record.svg directly under the hero.** It is the only evidence (2 days vs 2 sprints, USD 37k/yr, 670k+ msgs, 45%). Today it sits below four tutorial-grade repos and a tools list. Order: hero, record, lvc, projects, links. Raise the numeral size from ~60px to ~84px, body copy from ~12px to 15px, and cut each body to one sentence (e.g. "Java 17 to 21 and Spring Boot 4.1 in 2 days. Other squads took 2 sprints."). Rewrite card 4: "45% of subtasks routed to the cheapest mode" says nothing to a reader; use "45% of AI subtasks run on the cheapest model."
3. **Delete desk.svg ("Daily Tools" plus the whoami terminal).** It makes no claim; a tools list is the generic profile section. The Samsung SDS line and "Scout volunteer" are the only facts, and Samsung is already in the USD 37k card. Put "Java, Spring, Rust, Python, AWS, Podman" as one plain line under the hero receipt if wanted. This also removes ~100KB and one full-width block (lean).
4. **lvc.svg: cut the ornaments, fix the fake data.** Remove kicker/caption labels "SIX MODULES", "VALIDATED ON", "EVENT STORE · APPEND-ONLY" and the right-aligned "illustrative". The event-store log shows a named person ("Caio Prado") and invented timestamps; invented content is not proof. Replace the log with the real claim: one `.proto` serving Java, Python and Rust (show the three module names with their language, nothing else). Drop the "PRESENTED / PROCEEDINGS SOON" stamp: it says presented and not published in one box. Keep a single line "Full paper, Latinoware 2026. Proceedings forthcoming." Title at ~58px, body at 15px.
5. **Merge the link tickets and trim projects.** `link-code.svg` and `link-paper.svg` repeat the lvc card, whose whole area already links to the paper. Delete both and put the code link inside the README as one line of text under lvc.svg. Projects: remove `No. 01-04` (invented numbering), the black dot and arrow glyphs on each card, and the bottom grey tab. If poc-grpc, Demo-SpringSecurity6-JWT, spring-and-vue and cachyos-setup are tutorials, show only poc-grpc and cachyos-setup, as two cards each with name at 24px and one line of proof (what it runs, stars if any). Four equal cards imply four equal achievements.

## Animations

1. **The log scroll (`{sid}log` 9s linear infinite, ~L240) animates fake data.** Remove it along with finding 4. Removing it also removes the only infinite motion besides the cursor.
2. **Hero print-in is 1500ms, then polaroid develop 2.4s at 700ms delay (L162, L173).** Total ~3.1s before the page is still; too long for a profile people scan in 2s. Set print to 900ms ease-out, develop to 1400ms at 300ms. Keep the shared EASE_OUT.
3. **Stagger.** The `.w` wipe 620ms and `.f` rise 560ms are fine; cap the last delay in each card at 900ms (lvc rows start at 1400ms, L231). Remove the row-by-row terminal typing in desk.svg with the card.
4. **Cursor blink (`{sid}blink 1.1s steps(1)`)**: keep only in hero. Fine as is.
5. **Reduced motion**: the fallback at L59-60 is good, keep it. Also add `@media (prefers-reduced-motion)` already covered, no change.

## GitHub integration

1. **Text is too small at mobile width.** Cards are 860 wide; at ~380px they scale to 0.44, so 12.5px log text becomes ~5.5px and 10.5px captions ~4.6px. Rule: no text under 15 SVG px in any card, headlines 40px or more. This is why the type must go up and the secondary labels must go.
2. **Half-width cards at 49% shrink further to ~0.22 scale on mobile.** Either drop the two-column grid (project cards at 100% width, two cards) or redraw them at W=430 with 20px minimum text. Two stacked full-width cards beat four unreadable halves.
3. **Weight.** 12 SVGs total ~1.1MB, each 90-110KB, apparently from an embedded font repeated per file (link tickets at 91KB for two lines of text confirms it). Subset the fonts to used glyphs (woff2, latin only) in `lib.py`; target under 40KB per card. Deleting desk, link-code, link-paper cuts three files.
4. **Light/dark.** Cards carry their own dark desk, so `<picture>` is not needed; keep it that way. In light mode the `rx=6` dark rectangle on white reads as a heavy box; add 12px of transparent margin or a 1px border `#3a3630`.
5. **Alt text** is good; keep. Make the hero link target the paper or record, not LinkedIn, since LinkedIn already has its own ticket at the bottom.

## Do not change

- Receipt, manila folder and ticket metaphor, and the DESK/PAPER/RED palette.
- The record numerals in serif, the red first figure, the dotted perforation dividers.
- The tagline copy and the Top Cat polaroid with "São Paulo, Brazil".
- `prefers-reduced-motion` fallback (fade 300ms) and per-card unique ids (`{sid}`).
- English-only copy, descriptive alt texts, personal-GitHub-only projects, no contribution board.
