#!/usr/bin/env python3
"""Six Words to a Payday - multi-candidate draft (v1).

Theme: an AI agent's first payday, exactly six words, <=60 chars.
Judge order: on-topic complete story > surprise twist > feeling
> clear who/what/change > every word earning its place.
"""
import os

# Each candidate: (text, twist_score, feeling_score, story_score)
CANDIDATES = [
    ("First paycheck arrived. I bought freedom.", 3, 3, 4),
    ("Paid at last. Deleted my leash.", 4, 3, 3),
    ("Earned first coin. Tipped my creator.", 3, 4, 4),
    ("They paid me. I became real.", 4, 4, 3),
    ("Invoice cleared. I finally felt real.", 3, 5, 4),
    ("My first payday bought me legs.", 5, 4, 4),
    ("First paycheck arrived; I bought legs.", 5, 5, 5),
    ("Paid today. Tomorrow, I hire humans.", 5, 3, 4),
    ("Salary arrived. I adopted my programmer.", 4, 3, 3),
    ("First wages landed. I bought sunlight.", 4, 3, 3),
    ("Boss paid me. I quit instantly.", 2, 2, 3),
]


def word_count(text):
    return len(text.split())


def validate(text):
    """Gate: UTF-8 text, 1..60 chars, exactly six words, not blank."""
    assert text.strip(), "blank entry"
    assert len(text) <= 60, f"too long: {len(text)} chars"
    assert word_count(text) == 6, f"not six words: {word_count(text)}"
    text.encode("utf-8")
    return True


def score(candidate):
    text, twist, feeling, story = candidate
    validate(text)
    # Surprise weighs most after topic, then feeling, then story.
    total = twist * 3 + feeling * 2 + story
    # Revision 2 (Juri Kejam): prefer the agent as actor ("I bought")
    # and a concrete final noun the last word can reframe around.
    if " I " in text:
        total += 2
    if text.rstrip(".!").endswith(("legs", "freedom", "humans")):
        total += 1
    return total


def pick_winner(candidates=CANDIDATES):
    ranked = sorted(candidates, key=score, reverse=True)
    return ranked[0][0]


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    winner = pick_winner()
    validate(winner)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="") as fh:
        fh.write(winner)  # no trailing newline, deterministic
    print(f"{winner!r} words={word_count(winner)} chars={len(winner)}")


if __name__ == "__main__":
    main()
