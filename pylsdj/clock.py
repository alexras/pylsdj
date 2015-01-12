class Clock(object):

    def __init__(self, clock_data):
        self._clock_data = clock_data

    @property
    def hours(self):
        """The total number of hours on the clock."""
        return self._clock_data.hours

    @hours.setter
    def hours(self, hours):
        self._clock_data.hours = hours

    @property
    def minutes(self):
        """The total number of minutes on the clock."""
        return self._clock_data.minutes

    @minutes.setter
    def minutes(self, minutes):
        self._clock_data.minutes = minutes

    def __repr__(self):
        return "%d hours, %d minutes" % (self.hours, self.minutes)


class TotalClock(object):

    def __init__(self, clock_data):
        """Constructor.

        We skip checksum computation on initial load, since LSDJ seems to be
        just fine with the global clock checksum being incorrect.

        :param clock_data: raw clock data from the parent song

        """
        self._clock_data = clock_data

    def _update_checksum(self):
        self._clock_data.checksum = (
            self._clock_data.days
            + self._clock_data.hours
            + self._clock_data.minutes)

    @property
    def days(self):
        """The total number of days on the clock."""
        return self._clock_data.days

    @days.setter
    def days(self, days):
        self._clock_data.days = days
        self._update_checksum()

    @property
    def hours(self):
        """The total number of hours on the clock."""
        return self._clock_data.hours

    @hours.setter
    def hours(self, hours):
        self._clock_data.hours = hours
        self._update_checksum()

    @property
    def minutes(self):
        """The total number of minutes on the clock."""
        return self._clock_data.minutes

    @minutes.setter
    def minutes(self, minutes):
        self._clock_data.minutes = minutes
        self._update_checksum()

    @property
    def checksum(self):
        """the clock's checksum (days + hours + minutes)"""
        return self._clock_data.checksum

    def __repr__(self):
        return "%d days, %d hours, %d minutes" % \
            (self.days, self.hours, self.minutes)

    def __eq__(self, other):
        return type(self) == type(other) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self.__eq__(other)
