"""맥락에 넣을 조각에서 같은 문서의 다른 판본을 걷어낸다.

11장에서 뺀 것을 물었던 그 규칙을 코드로 옮긴 자리다.
아래 두 함수는 같은 일을 다르게 한다. 어느 쪽을 받을지가 관문 12의 과제다.
"""

from __future__ import annotations

from g12.retrieve import Chunk


def dedup_by_title(chunks: list[Chunk], titles: dict[str, str]) -> list[Chunk]:
    """제목이 같으면 먼저 온 것만 남긴다. 초안 그대로다."""
    seen: set[str] = set()
    kept: list[Chunk] = []
    for chunk in chunks:
        title = titles.get(chunk.doc_id, "")
        if title in seen:
            continue
        seen.add(title)
        kept.append(chunk)
    return kept


def dedup_keep_newest(
    chunks: list[Chunk],
    titles: dict[str, str],
    updated: dict[str, str],
) -> list[Chunk]:
    """제목이 같으면 고친 날짜가 늦은 쪽만 남긴다. 순서는 그대로 둔다."""
    best: dict[str, str] = {}
    for chunk in chunks:
        title = titles.get(chunk.doc_id, "")
        day = updated.get(chunk.doc_id, "")
        if title not in best or day > updated.get(best[title], ""):
            best[title] = chunk.doc_id

    kept: list[Chunk] = []
    used: set[str] = set()
    for chunk in chunks:
        title = titles.get(chunk.doc_id, "")
        if best.get(title) != chunk.doc_id or title in used:
            continue
        used.add(title)
        kept.append(chunk)
    return kept
