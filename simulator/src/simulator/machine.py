from enum import Enum


class State(Enum):
    IDLE = "IDLE"
    RUN = "RUN"
    HOLD = "HOLD"
    ALARM = "ALARM"


class Event(Enum):
    CYCLE_START = "CYCLE_START"
    FEED_HOLD = "FEED_HOLD"
    RESET = "RESET"
    ALARM = "ALARM"
    PROGRAM_END = "PROGRAM_END"


TRANSITIONS = {
    (State.IDLE, Event.CYCLE_START): State.RUN,
    (State.HOLD, Event.CYCLE_START): State.RUN,
    (State.RUN, Event.FEED_HOLD): State.HOLD,
    (State.IDLE, Event.RESET): State.IDLE,
    (State.RUN, Event.RESET): State.IDLE,
    (State.HOLD, Event.RESET): State.IDLE,
    (State.ALARM, Event.RESET): State.IDLE,
    (State.IDLE, Event.ALARM): State.ALARM,
    (State.RUN, Event.ALARM): State.ALARM,
    (State.HOLD, Event.ALARM): State.ALARM,
    (State.RUN, Event.PROGRAM_END): State.IDLE,
}


class Machine:
    def __init__(self):
        self.state = State.IDLE
        self.part_count = 0

    def handle(self, event: Event) -> State:
        new_state = TRANSITIONS.get((self.state, event))
        if new_state is None:
            return self.state
        if self.state is State.RUN and event is Event.PROGRAM_END:
            self.part_count += 1
        self.state = new_state
        return self.state
