"""질의 결과를 잠깐 담아 두는 캐시.

관문 12의 디버깅 과제가 여기서 나온다. 이 파일에는 일부러 남겨 둔 결함이 있다.
고치는 것이 과제이므로 고쳐서 커밋하지 않는다. 어디가 왜 깨지는지는
test_cache.py 가 그대로 적어 둔다.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from g12.retrieve import Chunk, Index


@dataclass
class QueryCache:
    """같은 질의가 또 오면 전에 만든 결과를 그대로 내준다."""

    index: Index
    log: list[str] = field(default_factory=list)
    _store: dict[str, list[tuple[str, float]]] = field(default_factory=dict)

    def search(self, query: str, top_k: int = 3) -> list[tuple[str, float]]:
        key = query.strip().lower()
        if key in self._store:
            self.log.append(
                f"cache hit query={key!r} chunks={len(self.index.chunks)}"
            )
            return self._store[key]

        hits = [(c.chunk_id, round(s, 4)) for c, s in self.index.search(query, top_k)]
        self._store[key] = hits
        self.log.append(f"cache miss query={key!r} chunks={len(self.index.chunks)}")
        return hits

    def add_document(self, doc_id: str, text: str) -> int:
        """문서를 넣는다. 캐시는 건드리지 않는다."""
        return self.index.add_document(doc_id, text)


def first_hit(hits: list[tuple[str, float]]) -> Chunk | None:
    """맨 위 조각의 아이디만 꺼낸다. 없으면 None 이다."""
    if not hits:
        return None
    return hits[0][0]
