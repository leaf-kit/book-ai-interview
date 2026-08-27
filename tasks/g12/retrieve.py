"""문서를 조각으로 나누고 질의에 가까운 조각을 찾아 주는 최소 검색기.

이 파일이 이 책의 과제 코드베이스 출발점이다. 관문마다 조금씩 자란다.
바깥 의존성을 쓰지 않는다. 받아서 바로 돌려 볼 수 있어야 하기 때문이다.
"""

from __future__ import annotations

import math
import re
from collections import Counter
from dataclasses import dataclass, field

TOKEN = re.compile(r"[0-9a-zA-Z가-힣]+")


def tokenize(text: str) -> list[str]:
    return [t.lower() for t in TOKEN.findall(text)]


@dataclass(frozen=True)
class Chunk:
    doc_id: str
    index: int
    text: str

    @property
    def chunk_id(self) -> str:
        return f"{self.doc_id}#{self.index}"


def split(doc_id: str, text: str, size: int = 120, overlap: int = 20) -> list[Chunk]:
    """글자 수로 자른다. 겹치는 길이만큼 뒤로 물러나며 자른다."""
    if size <= 0:
        raise ValueError("size must be positive")
    if not 0 <= overlap < size:
        raise ValueError("overlap must be in [0, size)")

    body = text.strip()
    if not body:
        return []

    step = size - overlap
    chunks: list[Chunk] = []
    start = 0
    while start < len(body):
        piece = body[start : start + size]
        chunks.append(Chunk(doc_id=doc_id, index=len(chunks), text=piece))
        start += step
    return chunks


@dataclass
class Index:
    chunks: list[Chunk] = field(default_factory=list)
    _df: Counter = field(default_factory=Counter)

    def add(self, chunk: Chunk) -> None:
        self.chunks.append(chunk)
        for term in set(tokenize(chunk.text)):
            self._df[term] += 1

    def add_document(self, doc_id: str, text: str, **kwargs) -> int:
        pieces = split(doc_id, text, **kwargs)
        for piece in pieces:
            self.add(piece)
        return len(pieces)

    def idf(self, term: str) -> float:
        total = len(self.chunks)
        if total == 0:
            return 0.0
        return math.log((total + 1) / (self._df[term] + 1)) + 1.0

    def score(self, query: str, chunk: Chunk) -> float:
        q_terms = tokenize(query)
        if not q_terms:
            return 0.0
        counts = Counter(tokenize(chunk.text))
        length = sum(counts.values()) or 1
        return sum((counts[t] / length) * self.idf(t) for t in q_terms)

    def search(self, query: str, top_k: int = 3) -> list[tuple[Chunk, float]]:
        if top_k <= 0:
            return []
        scored = [(c, self.score(query, c)) for c in self.chunks]
        hits = [(c, s) for c, s in scored if s > 0.0]
        hits.sort(key=lambda pair: (-pair[1], pair[0].chunk_id))
        return hits[:top_k]
