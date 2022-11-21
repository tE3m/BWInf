from sys import argv
from typing import TypedDict

# Minuten eines Arbeitstags
WORKDAY = 480
# Minuten eines Kalendertags
CALENDARDAY = 1440


def minutes_to_days(minuten: int) -> str:
    """
    Rechnet Minuten zu Tagen, Stunden und Minuten um

    :param minuten: die Anzahl umzurechnender Minuten
    :return: der formatierte String
    """
    tage = minuten // 1440
    stunden = (minuten // 60) % 24
    rest = minuten % 60
    return "{} Tage, {} Stunden und {} Minuten".format(tage, stunden, rest)


class Job:
    """
    Ein Auftrag
    """
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
            time_received=minutes_to_days(self.time_received),
            duration=minutes_to_days(self.duration))
        if self.time_started:
            return_str += "    Bearbeitungsbeginn: {time_started}\n    Wartezeit: {waiting_time}\n    Bearbeitungsende:" \
                          "{time_finished}\n ".format(time_started=minutes_to_days(self.time_started),
                                                      waiting_time=minutes_to_days(self.waiting_time),
                                                      time_finished=minutes_to_days(self.time_finished))
        return return_str

    @property
    def time_finished(self) -> int:
        """
        Berechnet die erwartete Endzeit des Auftrags

        :return: der Endzeitpunkt in Minuten
        """
        assert type(self.time_started) == int
        full_days = (self.duration // WORKDAY) * CALENDARDAY
        remainder = self.duration % WORKDAY
        if remainder > Workshop.remaining_working_minutes(self.time_started):
            remainder += 960
        return self.time_started + full_days + remainder

    @property
    def waiting_time(self) -> int:
        """
        Berechnet die Wartezeit des Auftrags

        :return: die Wartezeit in Minuten
        """
        assert type(self.time_started) == int
        return self.time_finished - self.time_received


class Workshop:
    """
    Eine Werkstatt
    """
    jobs: list[Job]
    current_time: int

    def __init__(self, path: str) -> None:
        with open(path, "r") as file:
            lines = file.readlines()
        self.jobs = [Job(*map(int, args.strip().split(" "))) for args in lines if args != "\n"]
        self.current_time = 0

    class Result(TypedDict):
        time_finished: int
        avg_waiting_time: int
        max_waiting_time: int

    def fifo(self) -> Result:
        """
        Simuliert die Arbeit nach dem First-In-First-Out-Prinzip

        :return: ein `dict` mit der Endzeit, der durchschnittlichen und der maximalen Wartezeit
        """
        # zurücksetzen der Simulationsumgebung
        self.reset_environment()
        # sortieren der Aufträge nach chronologischer Reihenfolge
        sorted_jobs = sorted(self.jobs, key=lambda x: x.time_received)
        for job in sorted_jobs:
            received = job.time_received
            if received >= self.current_time:
                # Liegt der Eingang in der Zukunft, beginnt die Arbeit bei Eingang des Auftrags
                job.time_started = received
            else:
                # Sonst wird sofort begeonnen
                job.time_started = self.current_time
            self.current_time = job.time_finished
        return {"time_finished": self.current_time,
                "avg_waiting_time": sum(job.waiting_time for job in self.jobs) // len(self.jobs),
                "max_waiting_time": max(self.jobs, key=lambda x: x.waiting_time).waiting_time
                }

    def sjn(self) -> Result:
        """
        Simuliert die Arbeit nach dem Shortest-Job-Next-Prinzip

        :return: ein `dict` mit der Endzeit, der durchschnittlichen und der maximalen Wartezeit
        """
        # zurücksetzen der Simulationsumgebung
        self.reset_environment()
        # sortieren der Aufträge nach chronologischer Reihenfolge
        sorted_jobs = sorted(self.jobs, key=lambda x: x.time_received)
        while sorted_jobs:
            # liegt aktuell nur ein Auftrag vor, wird dieser bearbeitet
            if self.current_time <= sorted_jobs[0].time_received < sorted_jobs[1].time_received:
                job = sorted_jobs.pop(0)
                self.current_time = job.time_received
            # sonst wird der kürzeste vorliegende Auftrag ausgewählt
            else:
                if self.current_time < sorted_jobs[0].time_received:
                    self.current_time = sorted_jobs[0].time_received
                job = min(filter(lambda x: x.time_received <= self.current_time, sorted_jobs),
                          key=lambda x: x.duration)
                sorted_jobs.remove(job)
            job.time_started = self.current_time
            self.current_time = job.time_finished
        return {"time_finished": self.current_time,
                "avg_waiting_time": sum(job.waiting_time for job in self.jobs) // len(self.jobs),
                "max_waiting_time": max(self.jobs, key=lambda x: x.waiting_time).waiting_time
                }

    @staticmethod
    def is_working_hours(time: int) -> bool:
        """
        Gibt zurück, ob der Zeitpunkt `time` innerhalb der Öffnungszeiten liegt

        :param time: der zu prüfende Zeitpunkt
        :return: Wahrheitswert, ob zu diesem Zeitpunkt geöffnet ist
        """
        return 540 <= (time % CALENDARDAY) < 1020

    @staticmethod
    def remaining_working_minutes(time: int) -> int:
        """
        Gibt die verbleibenden Arbeitsminuten am derzeitigen Tag zurück

        :return: die verbleibenden Arbeitsminuten am derzeitigen Tag
        """
        return 1020 - time % CALENDARDAY

    def reset_environment(self) -> None:
        """
        Setzt die Simulationsumgebung auf den Ausgangszustand zurück
        """
        self.current_time = 0
        for job in self.jobs:
            job.time_started = None


if __name__ == '__main__':
    workshop = Workshop(argv[1])
    fifo_result = workshop.fifo()
    print("FIFO")
    for k, v in fifo_result.items():
        print(k + ":", minutes_to_days(v))
    print("\nSJN")
    shortest_first_result = workshop.sjn()
    for k, v in shortest_first_result.items():
        print(k + ":", minutes_to_days(v))
