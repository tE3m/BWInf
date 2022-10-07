from sys import argv

# Minuten eines Arbeitstags
WORKDAY = 480
# Minuten eines Kalendertags
CALENDARDAY = 1440


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
        today = Workshop.remaining_working_minutes(self.time_started)
        return self.time_started + self.duration - today


class Workshop:
    jobs: list[Job]
    current_time: int

    def __init__(self, path: str):
        with open(path, "r") as file:
            lines = file.readlines()
        self.jobs = [Job(*args.strip().split(" ")) for args in lines if args != "\n"]
        self.current_time = 0

    def fifo(self):
        sorted_jobs = sorted(self.jobs)
        for job in sorted_jobs:
            received = job.time_received
            if received > self.current_time:
                # Liegt der Eingang in der Zukunft, beginnt die Arbeit zum nächsten Zeitpunkt innerhalb der
                # Öffnungszeiten
                self.current_time = self.next_working_hours(received)

    @staticmethod
    def is_working_hours(time: int) -> bool:
        """
        Gibt zurück, ob der Zeitpunkt `time` innerhalb der Öffnungszeiten liegt

        :param time: der zu prüfende Zeitpunkt
        :return: Wahrheitswert, ob zu diesem Zeitpunkt geöffnet ist
        """
        return 540 <= (time % CALENDARDAY) < 1020

    def next_working_hours(self, time: int | None = None) -> int:
        """
        Gibt den nächsten Zeitpunkt zurück, zu dem die Werkstatt geöffnet hat.

        :param time: (optional) der zu prüfende Zeitpunkt. Wird kein Wert übergeben, wird die aktuelle Zeit geprüft
        :return: der nächste Zeitpunkt, zu dem die Werkstatt geöffnet hat
        """
        time = self.current_time if time is None else time
        assert time >= self.current_time
        return time if Workshop.is_working_hours(time) else (((time // CALENDARDAY) + 1) * CALENDARDAY) + 540

    @staticmethod
    def remaining_working_minutes(time: int) -> int:
        """
        Gibt die verbleibenden Arbeitsminuten am derzeitigen Tag zurück

        :return: die verbleibenden Arbeitsminuten am derzeitigen Tag
        """
        assert Workshop.is_working_hours(time)
        return 1020 - time % CALENDARDAY


if __name__ == '__main__':
    workshop = Workshop(argv[1])
