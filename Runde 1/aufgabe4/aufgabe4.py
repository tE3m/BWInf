from sys import argv


class Job:
    # Attribute
    _time_received: int
    _duration: int
    _time_started: int

    def __init__(self, time_received: int, duration: int) -> None:
        # Initialisieren
        self._time_received = time_received
        self._duration = duration
        self._time_started = None

    def __repr__(self) -> str:
        return "Job(time_received: {time_received}, duration: {duration}, time_started: {time_started})".format(
            time_received=self.time_received, duration=self.duration, time_started=self.time_started)

    def __str__(self) -> str:
        return "Auftrag:\n    Eingangszeit: {time_received}\n    Dauer: {duration}\n    Bearbeitungsbeginn: " \
               " {time_started}".format(time_received=self.time_received,
                                        duration=self.duration,
                                        time_started=self.time_started)

    def __lt__(self, other) -> bool:
        assert type(other) == Job
        return self._time_received < other.time_received

    @property
    def time_received(self) -> int:
        return self._time_received

    @property
    def duration(self) -> int:
        return self._duration

    @property
    def time_started(self) -> int:
        return self._time_started

    @time_started.setter
    def time_started(self, time_started) -> None:
        self._time_started = time_started


class Workshop:
    jobs: list[Job]

    def __init__(self, path: str):
        with open(path, "r") as file:
            lines = file.readlines()
        self.jobs = sorted([Job(*args.strip().split(" ")) for args in lines if args != "\n"])


if __name__ == '__main__':
    workshop = Workshop(argv[1])
