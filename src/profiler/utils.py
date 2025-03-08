from typing import Literal

from profiler.state import State

def check_completion(state: State) -> Literal["complete", "continue"]:
    return "complete" if state.complete else "continue"