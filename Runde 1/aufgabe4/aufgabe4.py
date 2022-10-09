from functools import cached_property
from sys import argv

# Minuten eines Arbeitstags
WORKDAY = 480
# Minuten eines Kalendertags
CALENDARDAY = 1440


def minuten_zu_tagen(minuten: int) -> str:
    tage = minuten // 1440
    stunden = (minuten // 60) % 24
    rest = minuten % 60
    return "{} Tage, {} Stunden und {} Minuten".format(tage, stunden, str(rest).zfill(2))


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
        return_str = "Auftrag:\n    Eingangszeit: {time_received}\n    Dauer: {duration}\n".format(
            time_received=minuten_zu_tagen(self.time_received),
            duration=minuten_zu_tagen(self.duration))
        if self.time_started:
            return_str += "    Bearbeitungsbeginn: {time_started}\n    Verzögerung: {delay}\n    Bearbeitungsende: " \
                          "{time_finished}\n ".format(time_started=minuten_zu_tagen(self.time_started),
                                                      delay=minuten_zu_tagen(self.time_started - self.time_received),
                                                      time_finished=minuten_zu_tagen(self.time_finished))
        return return_str

    def __lt__(self, other) -> bool:
        assert type(other) == Job
        return self.time_received < other.time_received

    # TODO Performance vs privates Attribut und einmalige Berechnung prüfen
    # TODO Abweichung von erwarteter Arbeitszeit einberechnen
    # TODO derzeitige Berechnung testen
    @cached_property
    def time_finished(self) -> int:
        assert type(self.time_started) == int
        full_days = (self.duration // WORKDAY) * CALENDARDAY
        remainder = self.duration % WORKDAY
        if remainder > Workshop.remaining_working_minutes(self.time_started):
            remainder += 960
        return self.time_started + full_days + remainder


class Workshop:
    jobs: list[Job]
    current_time: int

    def __init__(self, path: str):
        with open(path, "r") as file:
            lines = file.readlines()
        self.jobs = [Job(*map(int, args.strip().split(" "))) for args in lines if args != "\n"]
        self.current_time = 0

    def fifo(self):
        sorted_jobs = sorted(self.jobs)
        for job in sorted_jobs:
            received = job.time_received
            if received >= self.current_time:
                # Liegt der Eingang in der Zukunft, beginnt die Arbeit zum nächsten Zeitpunkt innerhalb der
                # Öffnungszeiten
                job.time_started = received
            else:
                job.time_started = self.current_time
            print(job)
            self.current_time = job.time_finished

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
    workshop.fifo()
