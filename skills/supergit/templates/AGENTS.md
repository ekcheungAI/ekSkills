# <project> — agent rules

> Read this before editing anything in this repository.

## Git: library, rooms, ship

1. The main folder of this project is a **library**: read-only. Never edit, stash, reset or clean it. Work in a **room** started from the latest library, never from a stale local copy.
2. Rooms are opened with `supergit start <slug>` and closed with `supergit finish`. `supergit ship` (branch + PR) is the only push path. No agent pushes main.
3. `ship` runs in the background. Never wait on a build in the foreground, and never end a turn with "say the word and I'll push" when a grant already exists — ask for the grant at the start instead.
4. Every reply that touches git, the database or deployments ends with **Done / Waiting / You decide**.
5. When a phrase is ambiguous, run `supergit status` first and put the interpretation under "You decide". Never guess.
6. A worker or sub-agent never ships, merges, finishes or abandons. The parent does, once, after reading the real diff.
7. Database migrations are applied only through `supergit migrate`, one file at a time, with the file's timestamp as the version. Merging a PR never applies one.
8. Before removing anything — a room, a branch, a table — there is a backup (a rescue branch, an in-database copy) and the reply says how to recover.

## Verification

Run the project's own checks before shipping. State what was run and what it showed; never claim a check that did not run.
