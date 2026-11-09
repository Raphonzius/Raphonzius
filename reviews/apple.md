# Apple design review: oldschool variant

**Verdict:** Strong purpose and craft: one coherent paper world, honest motion, real content. It loses on legibility at phone width, a few unlabeled link targets, and tracking/entrance details that are not tuned per size.
Files reviewed: `gen/themes/oldschool.py`, `variants/oldschool.md`, `previews/oldschool.png`, SVG sizes in `assets/oldschool/`.

## Content

1. **Text below ~14px collapses on mobile (Craft, Flexibility).** Cards render at ~0.41-0.45x on a phone, so 12-13px becomes ~5px. Worst cases:
   - `project()` description at 12.5px in a 420px card shown at 49% width. Set name 17, description 14, language 12.5. Rewrap each line to 40 characters or fewer (356px of usable width at 14px mono is about 42 chars). Example: "gRPC client and server on one shared" / "Protobuf contract." Drop the "(+ grpc-common, grpc-server)" style suffixes.
   - `record()` body at 13px, `textwrap.wrap(small, 21)`. Raise to 15px, wrap at 18. Shorten the copy so it stays at 5 lines or fewer: "Java 17 to 21, Spring Boot 3.5 to 4.1, with AI agents. Other squads: 2 sprints." / "a year saved on AWS at Samsung SDS (rightsizing, arm64)." / "SMS and WhatsApp messages a month, 4 countries." / "of subtasks routed to the cheapest mode at Getnet's Devin Enterprise."
   - `lvc()` sub-lines (12px), log (12.5px), labels (11.5px): raise to 13, 13 and 12.5. Remove the "Real sources" and "Multi-language" sub-lines if space is short. Simplicity means cutting, not shrinking.
2. **Links without a cue, and one mismatched target (Familiarity, Wayfinding).** `project()` has a red "→", but hero, lvc, desk and record have none. `desk.svg` links to `?tab=repositories`, which a reader does not expect from "Daily Tools". In `desk()`, add a last row on the slip: `txt(xl, y+70, "ALL REPOSITORIES →", "rd b cap", 12.5)`. On `record()`, add a caption at the top margin: "SHIPPED, IN NUMBERS · CV ON LINKEDIN →" (12.5px, `mu b cap`, y=m+22) and move the numbers down by 12px. Without it, the card has no heading and the LinkedIn target is a surprise.
3. **Direct labels (Wayfinding).** Change the "Connect" ticket label to "LinkedIn profile". Change "Write to me" to "Email Rafael". Add a "FEATURED · PERSONAL GITHUB" mini label above the project grid, either as a README `<sub>` line or in project-1 and project-2. Without it, readers cannot tell the four cards are a section.
4. **Ticket value is 6px from the edge (Craft).** In `link-code`, "github.com/tcc-modern-lvc-arch" at 15px ends about 404px of 420. Set `ticket()` value to size 14 (ends about 386) and keep 30px padding.
5. **Hero name crowds its label (Craft).** "HELLO THERE! I'M" (y=74) sits 8px above the cap height of the 46px name (y=114). Move the name to y=118, and the lines below to 142, 160 and rule 178. Start the item rows at y=210 and grow `H` by 4.

## Animations

1. **Stamps do not land (Delight, Response).** The docstring says "stamps land", but `stamp()` reuses `.f` (8px rise plus fade). Add a `.st` class with `@keyframes {sid}stamp{from{opacity:0;transform:scale(1.35)}to{opacity:1;transform:none}}`, 260ms, `cubic-bezier(.3,1.25,.4,1)` (a small overshoot is fine because a stamp has momentum), `transform-box:fill-box; transform-origin:center`. Apply it to the inner group in `stamp()`. Add `.st` to the reduced-motion fade rule.
2. **The reduced-motion rule misses the photo overlay (Reduced motion).** `hero()` polaroid overlay uses an inline `style="animation:dev 2.4s ..."` that the `.w,.f,.up` and `.cur,.loop` selectors do not match. Give it `class="loop"` so it stops, and set its final state (opacity 0) in the reduced-motion block.
3. **The event-store loop is a continuous linear scroll (Reduced motion, Craft).** `lvc` uses `9s linear infinite` (10px/s), which keeps the log from being read. Replace it with stepped movement: 4 steps of 22px, each 2.25s, with 420ms of `cubic-bezier(0.23,1,0.32,1)` movement and the rest held. Keyframes: `0%,18%{translateY(0)} 25%,43%{translateY(-22px)} 50%,68%{-44px} 75%,93%{-66px} 100%{-88px}`. Cycle stays near 0.11 Hz, which is below the 0.2 Hz oscillation band, but it is no longer constant motion.
4. **Below-the-fold entrances are spent before they are seen (Purpose).** CSS animations start when the image loads, not on scroll. `lvc`, `desk`, `record` and the projects play their 2-3s choreography off-screen. Keep the hero sequence. For all other cards, cut delays so each completes in 700ms or less (for example `D(80+i*40)` in `project()` and `record()`, 25ms steps in `row()` calls). The loops (log, terminal) carry the live feel.
5. **Hero print jank risk (Craft).** The 1500ms `print` translate moves a group containing the blurred shadow and feTurbulence filters, which can re-rasterize per frame. Add `will-change:transform` to the animated group and move the sheet filters out of it where possible. Keep the duration; the ease-out curve is right.

## GitHub integration

1. **Fonts embedded in every card cost about 1.15MB total (Craft, longevity).** Each SVG is 91-111KB, even the 84px-tall tickets. Subset per card in `lib.font()` to only the glyphs used (via `text=` for the Google subset or `pyftsubset --text`). Expect about 15-25KB per card, with faster Camo fetches and less first-paint flash. Keep the embedded fonts; system fonts would lose the Plex and Serif voice.
2. **Phone layout of the 49% pairs.** If mobile still reads small after the sizes above, test `<source media="(max-width:600px)">` in a `<picture>` to serve stacked variants. I did not verify that GitHub's sanitizer keeps `media` other than `prefers-color-scheme`, so treat it as untested. A safer fallback is to make `link-*` tickets 100% width and keep only the project grid at 49%.
3. **Tracking per size (Typography).** `.sf` applies -0.03em at every size. In the render, the all-caps "RAFAEL PEREIRA" (46px) is cramped and the 37px tagline loses its word gaps. Replace with per-size classes: caps display -0.01em; 58px numbers -0.025em; 46px mixed case -0.02em; 37px -0.015em with `word-spacing:.06em`. Keep mono labels at `.07em` caps and body at 0.
4. **Image alt text matches the visual cards (Wayfinding).** Alt texts already name targets for the hero and tickets. Add the destination to the hero and record alt text ("Opens LinkedIn"), so screen-reader users get the same cue as the new "→".

## Do not change

- Receipt hero concept, printer slot, leader dots and the "deterministic first" tagline.
- Self-contained dark desk backgrounds (they work in both GitHub themes with no `<picture>` needed).
- Paper material: gradient, static grain and soft shadow. Tint and depth are consistent across cards.
- Ease-out curve `cubic-bezier(0.23,1,0.32,1)` and the clip-path wipe for printed lines.
- Single blinking cursor per card (about 0.9 Hz, not near 0.2 Hz).
- Reduced-motion fade fallback and loops stopping on their final frame.
- Real CV numbers on `record`, "illustrative" label on the event store, and "PROCEEDINGS SOON" on the stamp.
- Project cards pointing only to personal repos, with the red "→" affordance.
