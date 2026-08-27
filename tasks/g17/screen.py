"""서류를 도구에 시키고 그 결과를 사람이 되짚는 자리.

도구가 매긴 순위는 후보일 뿐이다. 누구를 부를지는 사람이 고른다.
그래서 이 코드가 내놓는 값 중 제일 중요한 것은 순위가 아니라
컷 아래에서 사람이 되살린 건수다. 그게 0 이면 아무도 안 보고 있는 것이다.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from g16.resume import questions_for


@dataclass(frozen=True)
class Application:
    label: str
    lines: tuple[str, ...]


@dataclass
class Screening:
    cut: int = 2
    revived: list[str] = field(default_factory=list)

    def score(self, app: Application) -> int:
        """물을 게 적은 이력서를 위로 올린다. 물을 게 없다는 건 이미 답이 적혀 있다는 뜻이다."""
        return -sum(len(questions_for(line)) for line in app.lines)

    def rank(self, apps: tuple[Application, ...]) -> list[Application]:
        return sorted(apps, key=lambda a: (self.score(a), a.label), reverse=True)

    def below_cut(self, apps: tuple[Application, ...]) -> list[Application]:
        return self.rank(apps)[self.cut:]

    def revive(self, label: str) -> None:
        """컷 아래를 사람이 읽고 다시 올린 것. 이 목록이 비어 있으면 검증을 안 한 것이다."""
        self.revived.append(label)

    def audited(self) -> bool:
        return bool(self.revived)


APPS: tuple[Application, ...] = (
    Application("가", ("검색 정확도를 0.58에서 0.71로 개선", "지연을 800에서 210밀리초로")),
    Application("나", ("사내 문서 검색 서비스 개발 담당", "성능 최적화 수행")),
    Application("다", ("검색 파이프라인 구축 참여", "Python, 웹 프레임워크, 캐시 활용")),
    Application("라", ("청크를 세 번 바꿨고 두 번째가 나빠서 되돌림", "평가 목록 20개 작성")),
)
