from __future__ import absolute_import
import logging

import six

from atomos.multiprocessing.atomic import AtomicLong

from hystrix.metrics import Metrics
from hystrix.event_type import EventType
from hystrix.rolling_number import (RollingNumber, RollingNumberEvent,
                                    ActualTime)

log = logging.getLogger(__name__)


class CommandMetricsMetaclass(type):
    """ Metaclass for :class:`CommandMetrics`

    Return a cached or create the :class:`CommandMetrics` instance for a given
    :class:`hystrix.command.Command` name.

    This ensures only 1 :class:`CommandMetrics` instance per
    :class:`hystrix.command.Command` name.
    """

    __instances__ = dict()
    __blacklist__ = ('CommandMetrics', 'CommandMetricsMetaclass')

    def __new__(cls, name, bases, attrs):

        # Do not use cache for black listed classes.
        if name in cls.__blacklist__:
            return super(CommandMetricsMetaclass, cls).__new__(cls, name,
                                                               bases, attrs)

        # User defined class name or create a default.
        command_metrics_key = attrs.get('command_metrics_key') or \
            '{}CommandMetrics'.format(name)

        # Check for CommandMetrics class instance
        if command_metrics_key not in cls.__instances__:
            new_class = super(CommandMetricsMetaclass, cls).__new__(cls,
                                                                    command_metrics_key,
                                                                    bases,
                                                                    attrs)
            setattr(new_class, 'command_metrics_key', command_metrics_key)
            cls.__instances__[command_metrics_key] = new_class

        return cls.__instances__[command_metrics_key]


class CommandMetrics(six.with_metaclass(CommandMetricsMetaclass, Metrics)):
    """ Used by :class:`hystrix.command.Command` to record metrics.
    """
    command_metrics_key = None

    # TODO: Review default value None here
    def __init__(self, command_metrics_key=None, group_key=None,
                 pool_key=None, properties=None, event_notifier=None):
        counter = RollingNumber(
            properties.metrics_rolling_statistical_window_in_milliseconds(),
            properties.metrics_rolling_statistical_window_buckets())
        super(CommandMetrics, self).__init__(counter)
        self.properties = properties
        self.actual_time = ActualTime()
        self.group_key = group_key
        self.event_notifier = event_notifier
        self.health_counts_snapshot = None
        self.last_health_counts_snapshot = AtomicLong(value=self.actual_time.current_time_in_millis())

    def mark_success(self, duration):
        """ Mark success incrementing counter and emiting event

        When a :class:`hystrix.command.Command` successfully completes it will
        call this method to report its success along with how long the
        execution took.

        Args:
            duration: Command duration
        """

        # TODO: Why this receive a parameter and do nothing with it?
        self.event_notifier.mark_event(EventType.SUCCESS, self.command_metrics_key)
        self.counter.increment(RollingNumberEvent.SUCCESS)

    def mark_failure(self, duration):
        """ Mark failure incrementing counter and emiting event

        When a :class:`hystrix.command.Command` fail to completes it will
        call this method to report its failure along with how long the
        execution took.

        Args:
            duration: Command duration
        """

        # TODO: Why this receive a parameter and do nothing with it?
        self.event_notifier.mark_event(EventType.FAILURE, self.command_metrics_key)
        self.counter.increment(RollingNumberEvent.FAILURE)

    def mark_timeout(self, duration):
        """ Mark timeout incrementing counter and emiting event

        When a :class:`hystrix.command.Command` times out (fails to complete)
        it will call this method to report its failure along with how long the
        command waited (this time should equal or be very close to the timeout
        value).

        Args:
            duration: Command duration
        """

        # TODO: Why this receive a parameter and do nothing with it?
        self.event_notifier.mark_event(EventType.TIMEOUT, self.command_metrics_key)
        self.counter.increment(RollingNumberEvent.TIMEOUT)

    def mark_bad_request(self, duration):
        """ Mark bad request incrementing counter and emiting event

        When a :class:`hystrix.command.Command` is executed and triggers a
        :class:`hystrix.BadRequestException` during its execution it willi
        call this method to report its failure along with how long the
        command waited (this time should equal or be very close to the timeout
        value).

        Args:
            duration: Command duration
        """

        # TODO: Why this receive a parameter and do nothing with it?
        self.event_notifier.mark_event(EventType.BAD_REQUEST, self.command_metrics_key)
        self.counter.increment(RollingNumberEvent.BAD_REQUEST)

    def health_counts(self):
        """ Health counts

        Retrieve a snapshot of total requests, error count and error percentage.

        Returns:
            instance: :class:`hystrix.command_metrics.HealthCounts`
         """
        # we put an interval between snapshots so high-volume commands don't
        # spend too much unnecessary time calculating metrics in very small time periods
        last_time = self.last_health_counts_snapshot.get()
        current_time = ActualTime().current_time_in_millis()
        if (current_time - last_time) >= self.properties.metrics_health_snapshot_interval_in_milliseconds() or self.health_counts_snapshot is None:
            if self.last_health_counts_snapshot.compare_and_set(last_time, current_time):
                # Our thread won setting the snapshot time so we will
                # proceed with generating a new snapshot
                # losing threads will continue using the old snapshot
                success = self.counter.rolling_sum(RollingNumberEvent.SUCCESS)
                failure = self.counter.rolling_sum(RollingNumberEvent.FAILURE)
                timeout = self.counter.rolling_sum(RollingNumberEvent.TIMEOUT)
                thread_pool_rejected = self.counter.rolling_sum(RollingNumberEvent.THREAD_POOL_REJECTED)
                semaphore_rejected = self.counter.rolling_sum(RollingNumberEvent.SEMAPHORE_REJECTED)
                short_circuited = self.counter.rolling_sum(RollingNumberEvent.SHORT_CIRCUITED)
                total_count = failure + success + timeout + thread_pool_rejected + short_circuited + semaphore_rejected
                error_count = failure + timeout + thread_pool_rejected + short_circuited + semaphore_rejected
                error_percentage = 0

                if total_count > 0:
                    error_percentage = int(error_count / total_count * 100)

                self.health_counts_snapshot = HealthCounts(total_count, error_count, error_percentage)

        return self.health_counts_snapshot


class HealthCounts(object):
    """ Number of requests during rolling window.

    Number that failed (failure + success + timeout + thread pool rejected +
    short circuited + semaphore rejected).

    Error percentage;
    """
    def __init__(self, total, error, error_percentage):
        self._total_count = total
        self._error_count = error
        self._error_percentage = error_percentage

    def total_requests(self):
        """ Total reqeust

        Returns:
            int: Returns total request count.
        """
        return self._total_count

    def error_count(self):
        """ Error count

        Returns:
            int: Returns error count.
        """
        return self._error_count

    def error_percentage(self):
        """ Error percentage

        Returns:
            int: Returns error percentage.
        """
        return self._error_percentage
