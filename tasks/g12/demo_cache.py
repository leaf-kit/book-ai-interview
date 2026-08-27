"""캐시가 낡은 답을 계속 내주는 장면을 그대로 찍는다.

관문 12의 디버깅 과제에서 지원자에게 보여 주는 로그가 이 출력이다.
고친 코드가 아니라 지금 코드를 돌린 것이다.
"""

from __future__ import annotations

from g12.cache import QueryCache, first_hit
from g12.retrieve import Index

POLICY = "환불 정책 결제일 기준 7일 이내 환불 가능 "
NOTICE = "환불 정책 개정 안내 결제일 기준 14일로 늘어납니다 "


def run() -> list[str]:
    cache = QueryCache(index=Index())
    cache.add_document("policy", POLICY * 60)

    out = []
    hits = cache.search("환불")
    out.append(cache.log[-1])
    out.append(f"top1 {first_hit(hits)}")

    cache.add_document("notice", NOTICE * 60)
    out.append("--- 개정 공지를 넣었다 ---")

    hits = cache.search("환불")
    out.append(cache.log[-1])
    out.append(f"top1 {first_hit(hits)}")
    return out


if __name__ == "__main__":
    for line in run():
        print(line)
