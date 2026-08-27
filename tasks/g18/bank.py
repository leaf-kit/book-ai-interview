"""질문 은행. 질문을 어디에 두고 언제 버리는가.

질문은 쓸수록 닳는다. 같은 질문을 열 번 쓰면 열 번째에는 답이 도는 중이다.
그래서 상태를 붙여 두고 조건이 되면 물러나게 한다. 사람 기억에 맡기지 않는다.
"""

from __future__ import annotations

from dataclasses import dataclass, field

NEW = "새 질문"
TRIAL = "시험 중"
MAIN = "본류"
RETIRED = "물러남"

TRIAL_RUNS = 3      # 시험 중에 이만큼 써 보고 본류로 올린다
WORN_OUT = 12       # 본류에서 이만큼 쓰면 닳은 것으로 본다


@dataclass
class BankedQuestion:
    text: str
    state: str = NEW
    runs: int = 0
    leaked: bool = False
    anchored: bool = True

    def use(self) -> None:
        """한 번 썼다고 적는다. 적어야 닳은 것을 셀 수 있다."""
        if self.state == RETIRED:
            return
        self.runs += 1
        if self.state == NEW:
            self.state = TRIAL
        elif self.state == TRIAL and self.runs >= TRIAL_RUNS:
            self.state = MAIN
        if self.should_retire():
            self.state = RETIRED

    def mark_leaked(self) -> None:
        """밖에 돌아다니는 것을 봤다. 실물에 붙은 질문은 유출돼도 덜 닳는다."""
        self.leaked = True
        if self.should_retire():
            self.state = RETIRED

    def should_retire(self) -> bool:
        if self.leaked and not self.anchored:
            return True
        return self.runs >= WORN_OUT


@dataclass
class Bank:
    questions: list[BankedQuestion] = field(default_factory=list)

    def add(self, text: str, anchored: bool = True) -> BankedQuestion:
        item = BankedQuestion(text=text, anchored=anchored)
        self.questions.append(item)
        return item

    def by_state(self, state: str) -> list[BankedQuestion]:
        return [q for q in self.questions if q.state == state]

    def in_rotation(self) -> list[BankedQuestion]:
        return [q for q in self.questions if q.state in (TRIAL, MAIN)]

    def health(self) -> dict[str, int]:
        """은행이 마르고 있는지 보는 표. 본류가 줄고 새 질문이 없으면 곧 빈다."""
        return {state: len(self.by_state(state))
                for state in (NEW, TRIAL, MAIN, RETIRED)}
