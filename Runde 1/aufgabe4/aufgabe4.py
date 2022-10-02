from sys import argv


class Job:
    # Attribute
    time_received: int
    duration: int
    time_started: int | None

    def __init__(self, time_received: int, duration: int) -> None:
        # Initialisieren
        self.time_received = time_received
        self.duration = duration
        self.time_started = None

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
        return self.time_received < other.time_received

    @property
    def time_finished(self):
        assert type(self.time_started) == int
        # TODO Arbeitszeiten berücksichtigen
        return self.time_started + self.duration


class Workshop:
    jobs: list[Job]
    current_time: int

    def __init__(self, path: str):
        with open(path, "r") as file:
            lines = file.readlines()
        self.jobs = [Job(*args.strip().split(" ")) for args in lines if args != "\n"]
        self.current_time = 0

    @staticmethod
    def is_working_hours(time: int) -> bool:
        """
        Gibt zurück, ob der Zeitpunkt `time` innerhalb der Öffnungszeiten liegt

        :param time: der zu prüfende Zeitpunkt
        :return: Wahrheitswert, ob zu diesem Zeitpunkt geöffnet ist
        """
        return 540 <= (time % 1440) < 1020

    def next_working_hours(self, time: int | None = None) -> int:
        """
        Gibt den nächsten Zeitpunkt zurück, zu dem die Werkstatt geöffnet hat.

        :param time: (optional) der zu prüfende Zeitpunkt. Wird kein Wert übergeben, wird die aktuelle Zeit geprüft
        :return: der nächste Zeitpunkt, zu dem die Werkstatt geöffnet hat
        """
        time = self.current_time if time is None else time
        assert time >= self.current_time
        return time if Workshop.is_working_hours(time) else (((time // 1440) + 1) * 1440) + 540

    def remaining_working_minutes(self) -> int:
        """
        Gibt die verbleibenden Arbeitsminuten am derzeitigen Tag zurück

        :return: die verbleibenden Arbeitsminuten am derzeitigen Tag
        """
        assert Workshop.is_working_hours(self.current_time)
        return 1020 - self.current_time % 1440


if __name__ == '__main__':
    workshop = Workshop(argv[1])
