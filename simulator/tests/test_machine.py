import pytest

from simulator.machine import Event, Machine, State


def test_new_machine_is_idle():
    machine = Machine()

    assert machine.state is State.IDLE
    assert machine.part_count == 0


@pytest.mark.parametrize(
    ("start", "event", "expected"),
    [
        (State.IDLE, Event.CYCLE_START, State.RUN),
        (State.IDLE, Event.FEED_HOLD, State.IDLE),
        (State.IDLE, Event.RESET, State.IDLE),
        (State.IDLE, Event.ALARM, State.ALARM),
        (State.IDLE, Event.PROGRAM_END, State.IDLE),
        (State.RUN, Event.CYCLE_START, State.RUN),
        (State.RUN, Event.FEED_HOLD, State.HOLD),
        (State.RUN, Event.RESET, State.IDLE),
        (State.RUN, Event.ALARM, State.ALARM),
        (State.RUN, Event.PROGRAM_END, State.IDLE),
        (State.HOLD, Event.CYCLE_START, State.RUN),
        (State.HOLD, Event.FEED_HOLD, State.HOLD),
        (State.HOLD, Event.RESET, State.IDLE),
        (State.HOLD, Event.ALARM, State.ALARM),
        (State.HOLD, Event.PROGRAM_END, State.HOLD),
        (State.ALARM, Event.CYCLE_START, State.ALARM),
        (State.ALARM, Event.FEED_HOLD, State.ALARM),
        (State.ALARM, Event.RESET, State.IDLE),
        (State.ALARM, Event.ALARM, State.ALARM),
        (State.ALARM, Event.PROGRAM_END, State.ALARM),
    ],
    ids=lambda value: value.name,
)
def test_transitions(start, event, expected):
    machine = Machine()
    machine.state = start

    assert machine.handle(event) is expected
    assert machine.state is expected


def test_part_counted_on_program_end():
    machine = Machine()

    machine.handle(Event.CYCLE_START)
    machine.handle(Event.PROGRAM_END)

    assert machine.part_count == 1


def test_reset_does_not_count_part():
    machine = Machine()

    machine.handle(Event.CYCLE_START)
    machine.handle(Event.RESET)

    assert machine.part_count == 0


def test_full_cycle_with_hold():
    machine = Machine()

    machine.handle(Event.CYCLE_START)
    machine.handle(Event.FEED_HOLD)
    machine.handle(Event.CYCLE_START)
    machine.handle(Event.PROGRAM_END)

    assert machine.state is State.IDLE
    assert machine.part_count == 1


def test_program_end_outside_run_does_not_count_part():
    machine = Machine()

    machine.handle(Event.PROGRAM_END)
    machine.handle(Event.CYCLE_START)
    machine.handle(Event.FEED_HOLD)
    machine.handle(Event.PROGRAM_END)

    assert machine.part_count == 0
