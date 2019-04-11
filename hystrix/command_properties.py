from __future__ import absolute_import
import logging

log = logging.getLogger(__name__)


class CommandProperties(object):
    """ Properties for instances of :class:`hystrix.command.Command`
    """

    # Default values

    # 10000 = 10 seconds (and default of 10 buckets so each bucket is 1
    # second)
    default_metrics_rolling_statistical_window = 10000

    # 10 buckets in a 10 second window so each bucket is 1 second
    default_metrics_rolling_statistical_window_buckets = 10

    # 20 requests in 10 seconds must occur before statistics matter
    default_circuit_breaker_request_volume_threshold = 20

    # 5000 = 5 seconds that we will sleep before trying again after tripping
    # the circuit
    default_circuit_breaker_sleep_window_in_milliseconds = 5000

    # 50 = if 50%+ of requests in 10 seconds are failures or latent when we
    # will trip the circuit
    default_circuit_breaker_error_threshold_percentage = 50

    # If ``False`` we want to allow traffic.
    default_circuit_breaker_force_open = False

    # If ``False`` ignore errors
    default_circuit_breaker_force_closed = False

    # 1000 = 1 second timeout
    default_execution_timeout_in_milliseconds = 1000

    # Whether a command should be executed in a separate thread or not
    default_execution_isolation_strategy = 0

    # Wheather a thread should interrupt on timeout.
    default_execution_isolation_thread_interrupt_on_timeout = True

    # Wheather rolling percentile should be enabled.
    default_metrics_rolling_percentile_enabled = True

    # Wheather request cache should be enabled
    default_request_cache_enabled = True

    # Default fallback isolation semaphore max concurrent requests
    default_fallback_isolation_semaphore_max_concurrent_requests = 10

    # Wheather fallback should be enabled
    default_fallback_enabled = True

    # Default execution isolation semaphore max concurrent requests
    default_execution_isolation_semaphore_max_concurrent_requests = 10

    # Wheather request log should be enabled
    default_request_log_enabled = True

    # Wheather circuit breaker should be enabled
    default_circuit_breaker_enabled = True

    # Default to 1 minute for
    # :class:`hystrix.rolling_percentile._rolling_percentile`
    default_metrics_rolling_percentile_window = 60000

    # Default to 6 buckets (10 seconds each in 60 second window)
    default_metrics_rolling_percentile_window_buckets = 6

    # Default to 100 values max per bucket
    default_metrics_rolling_percentile_bucket_size = 100

    # Default to 500ms as max frequency between allowing snapshots of health
    # (error percentage etc)
    default_metrics_health_snapshot_interval_in_milliseconds = 500

    def __init__(self, command_key, setter, property_prefix=None):
        self.command_key = command_key
        self.property_prefix = property_prefix

        # Whether circuit breaker should be enabled
        self._circuit_breaker_enabled = \
            self._property(
                self.property_prefix, self.command_key,
                'circuit_breaker.enabled',
                self.default_circuit_breaker_enabled,
                setter.circuit_breaker_enabled())

        # Number of requests that must be made within a statisticalWindow
        # before open/close decisions are made using stats
        self._circuit_breaker_request_volume_threshold = \
            self._property(
                self.property_prefix, self.command_key,
                'circuit_breaker.request_volume_threshold',
                self.default_circuit_breaker_request_volume_threshold,
                setter.circuit_breaker_request_volume_threshold())

        # Milliseconds after tripping circuit before allowing retry
        self._circuit_breaker_sleep_window_in_milliseconds = \
            self._property(
                self.property_prefix, self.command_key,
                'circuit_breaker.sleep_window_in_milliseconds',
                self.default_circuit_breaker_sleep_window_in_milliseconds,
                setter.circuit_breaker_sleep_window_in_milliseconds())

        # % of 'marks' that must be failed to trip the circuit
        self._circuit_breaker_error_threshold_percentage = \
            self._property(
                self.property_prefix, self.command_key,
                'circuit_breaker.error_threshold_percentage',
                self.default_circuit_breaker_error_threshold_percentage,
                setter.circuit_breaker_error_threshold_percentage())

        # A property to allow forcing the circuit open (stopping all requests)
        self._circuit_breaker_force_open = \
            self._property(
                self.property_prefix, self.command_key,
                'circuit_breaker.force_open',
                self.default_circuit_breaker_force_open,
                setter.circuit_breaker_force_open())

        # a property to allow ignoring errors and therefore never trip 'open'
        # (ie. allow all traffic through)
        self._circuit_breaker_force_closed = \
            self._property(
                self.property_prefix, self.command_key,
                'circuit_breaker.force_closed',
                self.default_circuit_breaker_force_closed,
                setter.circuit_breaker_force_closed())

        # Whether a command should be executed in a separate thread or not
        self._execution_isolation_strategy = \
            self._property(
                self.property_prefix, self.command_key,
                'execution.isolation.strategy',
                self.default_execution_isolation_strategy,
                setter.execution_isolation_strategy())

        # Timeout value in milliseconds for a command
        self._execution_timeout_in_milliseconds = \
            self._property(
                self.property_prefix, self.command_key,
                'execution.isolation.thread.timeout_in_milliseconds',
                self.default_execution_timeout_in_milliseconds,
                setter.execution_timeout_in_milliseconds())

        # execution_isolation_thread_pool_key_override

        # Number of permits for execution semaphore
        self._execution_isolation_semaphore_max_concurrent_requests = \
            self._property(
                self.property_prefix, self.command_key,
                'execution.isolation.semaphore.max_concurrent_requests',
                self.default_execution_isolation_semaphore_max_concurrent_requests,
                setter.execution_isolation_semaphore_max_concurrent_requests())

        # Number of permits for fallback semaphore
        self._fallback_isolation_semaphore_max_concurrent_requests = \
            self._property(
                self.property_prefix, self.command_key,
                'fallback.isolation.semaphore.max_concurrent_requests',
                self.default_fallback_isolation_semaphore_max_concurrent_requests,
                setter.fallback_isolation_semaphore_max_concurrent_requests())

        # Whether fallback should be attempted
        self._fallback_enabled = \
            self._property(
                self.property_prefix, self.command_key, 'fallback.enabled',
                self.default_fallback_enabled,
                setter.fallback_enabled())

        # Whether an underlying Future/Thread
        # (when runInSeparateThread == true) should be interrupted after a
        # timeout
        self._execution_isolation_thread_interrupt_on_timeout = \
            self._property(
                self.property_prefix, self.command_key,
                'execution.isolation.thread.interrupt_on_timeout',
                self.default_execution_isolation_thread_interrupt_on_timeout,
                setter.execution_isolation_thread_interrupt_on_timeout())

        #  Milliseconds back that will be tracked
        self._metrics_rolling_statistical_window_in_milliseconds = \
            self._property(
                self.property_prefix, self.command_key,
                'metrics.rolling_stats.time_in_milliseconds',
                self.default_metrics_rolling_statistical_window,
                setter.metrics_rolling_statistical_window_in_milliseconds())

        # number of buckets in the statisticalWindow
        self._metrics_rolling_statistical_window_buckets = \
            self._property(
                self.property_prefix, self.command_key,
                'metrics.rolling_stats.num_buckets',
                self.default_metrics_rolling_statistical_window_buckets,
                setter.metrics_rolling_statistical_window_buckets())

        # Whether monitoring should be enabled (SLA and Tracers)
        self._metrics_rolling_percentile_enabled = \
            self._property(
                self.property_prefix,
                self.command_key, 'metrics.rolling_percentile.enabled',
                self.default_metrics_rolling_percentile_enabled,
                setter.metrics_rolling_percentile_enabled())

        # Number of milliseconds that will be tracked in
        # :class:`hystrix.rolling_percentile.RollingPercentile`
        self._metrics_rolling_percentile_window_in_milliseconds = \
            self._property(
                self.property_prefix, self.command_key,
                'metrics.rolling_percentile.time_in_milliseconds',
                self.default_metrics_rolling_percentile_window,
                setter.metrics_rolling_percentile_window_in_milliseconds())

        # Number of buckets percentileWindow will be divided into
        self._metrics_rolling_percentile_window_buckets = \
            self._property(
                self.property_prefix, self.command_key,
                'metrics.rolling_percentile.num_buckets',
                self.default_metrics_rolling_percentile_window_buckets,
                setter.metrics_rolling_percentile_window_buckets())

        # How many values will be stored in each
        # :attr:`percentile_window_bucket`
        self._metrics_rolling_percentile_bucket_size = \
            self._property(
                self.property_prefix, self.command_key,
                'metrics.rolling_percentile.bucket_size',
                self.default_metrics_rolling_percentile_bucket_size,
                setter.metrics_rolling_percentile_bucket_size())

        # Time between health snapshots
        self._metrics_health_snapshot_interval_in_milliseconds = \
            self._property(
                self.property_prefix, self.command_key,
                'metrics.health_snapshot.interval_in_milliseconds',
                self.default_metrics_health_snapshot_interval_in_milliseconds,
                setter.metrics_health_snapshot_interval_in_milliseconds())

        # Whether command request logging is enabled
        self._request_log_enabled = \
            self._property(
                property_prefix, self.command_key, 'request_log.enabled',
                self.default_request_log_enabled,
                setter.request_log_enabled())

        # Whether request caching is enabled
        self._request_cache_enabled = \
            self._property(
                self.property_prefix, self.command_key,
                'request_cache.enabled',
                self.default_request_cache_enabled,
                setter.request_cache_enabled())

        # threadpool doesn't have a global override, only instance level
        # makes sense
        # self.execution_isolation_thread_pool_key_override = \
        #    as__property(
        #        DynamicStringProperty(
        #            '{`.command.{`.thread_pool_key_override'.format(
        #                self.property_prefix, self.command_key), None))

    def circuit_breaker_enabled(self):
        """ Whether to use a :class:`hystrix.CircuitBreaker` or not. If false no
        circuit-breaker logic will be used and all requests permitted.

        This is similar in effect to :class:`#circuitBreakerForceClosed()`
        except that continues tracking metrics and knowing whether it should be
        open/closed, this property results in not even instantiating a
        circuit-breaker.

        Returns:
            bool: ``True`` or ``False``
        """
        return self._circuit_breaker_enabled

    def circuit_breaker_error_threshold_percentage(self):
        """ Error percentage threshold (as whole number such as 50) at which
        point the circuit breaker will trip open and reject requests.

        It will stay tripped for the duration defined in
        :class:`#circuitBreakerSleepWindowInMilliseconds()`;

        The error percentage this is compared against comes from
        :class:`hystrix.CommandMetrics#getHealthCounts()`.

        Returns:
            int: Error percentage
        """
        return self._circuit_breaker_error_threshold_percentage

    def circuit_breaker_force_closed(self):
        """ If true the :class:`hystrix.CircuitBreaker#allowRequest()` will
        always return true to allow requests regardless of the error percentage
        from :class:`hystrix.CommandMetrics#getHealthCounts()`.

        The :class:`#circuitBreakerForceOpen()` property takes precedence so
        if it set to true this property does nothing.

        Returns:
            bool: ``True`` or ``False``
        """
        return self._circuit_breaker_force_closed

    def circuit_breaker_force_open(self):
        """ If true the :class:`hystrix.CircuitBreaker#allowRequest()` will
        always return false, causing the circuit to be open (tripped) and
        reject all requests.

        This property takes precedence over
        :class:`#circuitBreakerForceClosed()`;

        Returns:
            bool: ``True`` or ``False``
        """
        return self._circuit_breaker_force_open

    def circuit_breaker_request_volume_threshold(self):
        """ Minimum number of requests in the
        :class:`#metricsRollingStatisticalWindowInMilliseconds()` that must
        exist before the :class:`hystrix.CircuitBreaker` will trip.

        If below this number the circuit will not trip regardless of error
        percentage.

        Returns:
            int: Number of request
        """
        return self._circuit_breaker_request_volume_threshold

    def circuit_breaker_sleep_window_in_milliseconds(self):
        """ The time in milliseconds after a :class:`hystrix.CircuitBreaker`
        trips open that it should wait before trying requests again.

        Returns:
            int: Time in milliseconds
        """
        return self._circuit_breaker_sleep_window_in_milliseconds

    def execution_isolation_semaphore_max_concurrent_requests(self):
        """ Number of concurrent requests permitted to
        :class:`hystrix.Command#run()`. Requests beyond the concurrent limit
        will be rejected.

        Applicable only when:

            :class:`#executionIsolationStrategy()` == SEMAPHORE.

        Returns:
            int: Number of concurrent requests
        """
        return self._execution_isolation_semaphore_max_concurrent_requests

    def execution_isolation_strategy(self):
        """ What isolation strategy :class:`hystrix.Command#run()` will be
        executed with.

        If :class:`ExecutionIsolationStrategy#THREAD` then it will be executed
        on a separate thread and concurrent requests limited by the number of
        threads in the thread-pool.

        If :class:`ExecutionIsolationStrategy#SEMAPHORE` then it will be
        executed on the calling thread and concurrent requests limited by the
        semaphore count.

        Returns:
            bool: ``True`` or ``False``
        """
        return self._execution_isolation_strategy

    def execution_isolation_thread_interrupt_on_timeout(self):
        """ Whether the execution thread should attempt an interrupt
        (using :class:`Future#cancel`) when a thread times out.

        Applicable only when :class:`#executionIsolationStrategy()` == THREAD.

        Returns:
            bool: ``True`` or ``False``
        """
        return self._execution_isolation_thread_interrupt_on_timeout

    def execution_timeout_in_milliseconds(self):
        """ Time in milliseconds at which point the command will timeout and
        halt execution.

        If :class:`#executionIsolationThreadInterruptOnTimeout` == true and the
        command is thread-isolated, the executing thread will be interrupted.
        If the command is semaphore-isolated and a
        :class:`hystrix.ObservableCommand`, that command will get unsubscribed.

        Returns:
            int: Time in milliseconds
        """
        return self._execution_timeout_in_milliseconds

    def fallback_isolation_semaphore_max_concurrent_requests(self):
        """ Number of concurrent requests permitted to
        :class:`hystrix.Command#getFallback()`. Requests beyond the concurrent
        limit will fail-fast and not attempt retrieving a fallback.

        Returns:
            int: Number of concurrent requests
        """
        return self._fallback_isolation_semaphore_max_concurrent_requests

    def fallback_enabled(self):
        """ Whether :class:`hystrix.Command#getFallback()` should be attempted
        when failure occurs.

        Returns:
            bool: ``True`` or ``False``
        """
        return self._fallback_enabled

    def metrics_health_snapshot_interval_in_milliseconds(self):
        """ Time in milliseconds to wait between allowing health snapshots to
        be taken that calculate success and error percentages and affect
        :class:`hystrix.CircuitBreaker#isOpen()` status.

        On high-volume circuits the continual calculation of error percentage
        can become CPU intensive thus this controls how often it is
        calculated.

        Returns:
            int: Time in milliseconds
        """
        return self._metrics_health_snapshot_interval_in_milliseconds

    def metrics_rolling_percentile_bucket_size(self):
        """ Maximum number of values stored in each bucket of the rolling
        percentile. This is passed into :class:`hystrix.RollingPercentile`
        inside :class:`hystrix.CommandMetrics`.

        Returns:
            int: Maximum number of values stored in each bucket
        """
        return self._metrics_rolling_percentile_bucket_size

    def metrics_rolling_percentile_enabled(self):
        """ Whether percentile metrics should be captured using
        :class:`hystrix.RollingPercentile` inside
        :class:`hystrix.CommandMetrics`.

        Returns:
            bool: ``True`` or ``False``
        """
        return self._metrics_rolling_percentile_enabled

    def metrics_rolling_percentile_window_in_milliseconds(self):
        """ Duration of percentile rolling window in milliseconds. This is
        passed into :class:`hystrix.RollingPercentile` inside
        :class:`hystrix.CommandMetrics`.

        Returns:
            int: Milliseconds
        """
        return self._metrics_rolling_percentile_window_in_milliseconds

    def metrics_rolling_percentile_window_buckets(self):
        """ Number of buckets the rolling percentile window is broken into.
        This is passed into :class:`hystrix.RollingPercentile` inside
        :class:`hystrix.CommandMetrics`.

        Returns:
            int: Buckets
        """
        return self._metrics_rolling_percentile_window_buckets

    def metrics_rolling_statistical_window_in_milliseconds(self):
        """ Duration of statistical rolling window in milliseconds. This is
        passed into :class:`hystrix.RollingNumber` inside
        :class:`hystrix.CommandMetrics`.

        Returns:
            int: Milliseconds
        """
        return self._metrics_rolling_statistical_window_in_milliseconds

    def metrics_rolling_statistical_window_buckets(self):
        """ Number of buckets the rolling statistical window is broken into.
        This is passed into :class:`hystrix.RollingNumber` inside
        :class:`hystrix.CommandMetrics`.

        Returns:
            int: Buckets
        """
        return self._metrics_rolling_statistical_window_buckets

    def request_cache_enabled(self):
        """ Whether :class:`hystrix.Command.getCacheKey()` should be used with
        :class:`hystrix.RequestCache` to provide de-duplication functionality
        via request-scoped caching.

        Returns:
            bool: ``True`` or ``False``
        """
        return self._request_cache_enabled

    def request_log_enabled(self):
        """ Whether :class:`hystrix.command.Command` execution and events
        should be logged to :class:`hystrix.request.RequestLog`.

        Returns:
            bool: ``True`` or ``False``
        """
        return self._request_log_enabled

    def _property(self, property_prefix, command_key, instance_property,
                  default_value, setter_override_value=None):
        """ Get property from a networked plugin
        """

        # The setter override should take precedence over default_value
        if setter_override_value is not None:
            return setter_override_value
        else:
            return default_value

    @classmethod
    def setter(klass):
        """ Factory method to retrieve the default Setter """
        return klass.Setter()

    class Setter(object):
        """ Fluent interface that allows chained setting of properties

        That can be passed into a :class:`hystrix.command.Command` constructor
        to inject instance specific property overrides.

        Example::

            >>> CommandProperties.setter()
                    .with_execution_timeout_in_milliseconds(100)
                    .with_execute_command_on_separate_thread(True)
        """

        def __init__(self):
            self._circuit_breaker_enabled = None
            self._circuit_breaker_error_threshold_percentage = None
            self._circuit_breaker_force_closed = None
            self._circuit_breaker_force_open = None
            self._circuit_breaker_request_volume_threshold = None
            self._circuit_breaker_sleep_window_in_milliseconds = None
            self._execution_isolation_semaphore_max_concurrent_requests = None
            self._execution_isolation_strategy = None
            self._execution_isolation_thread_interrupt_on_timeout = None
            self._execution_timeout_in_milliseconds = None
            self._fallback_isolation_semaphore_max_concurrent_requests = None
            self._fallback_enabled = None
            self._metrics_health_snapshot_interval_in_milliseconds = None
            self._metrics_rolling_percentile_bucket_size = None
            self._metrics_rolling_percentile_enabled = None
            self._metrics_rolling_percentile_window_in_milliseconds = None
            self._metrics_rolling_percentile_window_buckets = None
            self._metrics_rolling_statistical_window_in_milliseconds = None
            self._metrics_rolling_statistical_window_buckets = None
            self._request_cache_enabled = None
            self._request_log_enabled = None

        def circuit_breaker_enabled(self):
            return self._circuit_breaker_enabled

        def circuit_breaker_error_threshold_percentage(self):
            return self._circuit_breaker_error_threshold_percentage

        def circuit_breaker_force_closed(self):
            return self._circuit_breaker_force_closed

        def circuit_breaker_force_open(self):
            return self._circuit_breaker_force_open

        def circuit_breaker_request_volume_threshold(self):
            return self._circuit_breaker_request_volume_threshold

        def circuit_breaker_sleep_window_in_milliseconds(self):
            return self._circuit_breaker_sleep_window_in_milliseconds

        def execution_isolation_semaphore_max_concurrent_requests(self):
            return self._execution_isolation_semaphore_max_concurrent_requests

        def execution_isolation_strategy(self):
            return self._execution_isolation_strategy

        def execution_isolation_thread_interrupt_on_timeout(self):
            return self._execution_isolation_thread_interrupt_on_timeout

        def execution_timeout_in_milliseconds(self):
            return self._execution_timeout_in_milliseconds

        def fallback_isolation_semaphore_max_concurrent_requests(self):
            return self._fallback_isolation_semaphore_max_concurrent_requests

        def fallback_enabled(self):
            return self._fallback_enabled

        def metrics_health_snapshot_interval_in_milliseconds(self):
            return self._metrics_health_snapshot_interval_in_milliseconds

        def metrics_rolling_percentile_bucket_size(self):
            return self._metrics_rolling_percentile_bucket_size

        def metrics_rolling_percentile_enabled(self):
            return self._metrics_rolling_percentile_enabled

        def metrics_rolling_percentile_window_in_milliseconds(self):
            return self._metrics_rolling_percentile_window_in_milliseconds

        def metrics_rolling_percentile_window_buckets(self):
            return self._metrics_rolling_percentile_window_buckets

        def metrics_rolling_statistical_window_in_milliseconds(self):
            return self._metrics_rolling_statistical_window_in_milliseconds

        def metrics_rolling_statistical_window_buckets(self):
            return self._metrics_rolling_statistical_window_buckets

        def request_cache_enabled(self):
            return self._request_cache_enabled

        def request_log_enabled(self):
            return self._request_log_enabled

        def with_circuit_breaker_enabled(self, value):
            self._circuit_breaker_enabled = value
            return self

        def with_circuit_breaker_error_threshold_percentage(self, value):
            self._circuit_breaker_error_threshold_percentage = value
            return self

        def with_circuit_breaker_force_closed(self, value):
            self._circuit_breaker_force_closed = value
            return self

        def with_circuit_breaker_force_open(self, value):
            self._circuit_breaker_force_open = value
            return self

        def with_circuit_breaker_request_volume_threshold(self, value):
            self._circuit_breaker_request_volume_threshold = value
            return self

        def with_circuit_breaker_sleep_window_in_milliseconds(self, value):
            self._circuit_breaker_sleep_window_in_milliseconds = value
            return self

        def with_execution_isolation_semaphore_max_concurrent_requests(self, value):
            self._execution_isolation_semaphore_max_concurrent_requests = value
            return self

        def with_execution_isolation_strategy(self, value):
            self._execution_isolation_strategy = value
            return self

        def with_execution_isolation_thread_interrupt_on_timeout(self, value):
            self._execution_isolation_thread_interrupt_on_timeout = value
            return self

        def with_execution_timeout_in_milliseconds(self, value):
            self._execution_timeout_in_milliseconds = value
            return self

        def with_fallback_isolation_semaphore_max_concurrent_requests(self, value):
            self._fallback_isolation_semaphore_max_concurrent_requests = value
            return self

        def with_fallback_enabled(self, value):
            self._fallback_enabled = value
            return self

        def with_metrics_health_snapshot_interval_in_milliseconds(self, value):
            self._metrics_health_snapshot_interval_in_milliseconds = value
            return self

        def with_metrics_rolling_percentile_bucket_size(self, value):
            self._metrics_rolling_percentile_bucket_size = value
            return self

        def with_metrics_rolling_percentile_enabled(self, value):
            self._metrics_rolling_percentile_enabled = value
            return self

        def with_metrics_rolling_percentile_window_in_milliseconds(self, value):
            self._metrics_rolling_percentile_window_in_milliseconds = value
            return self

        def with_metrics_rolling_percentile_window_buckets(self, value):
            self._metrics_rolling_percentile_window_buckets = value
            return self

        def with_metrics_rolling_statistical_window_in_milliseconds(self, value):
            self._metrics_rolling_statistical_window_in_milliseconds = value
            return self

        def with_metrics_rolling_statistical_window_buckets(self, value):
            self._metrics_rolling_statistical_window_buckets = value
            return self

        def with_request_cache_enabled(self, value):
            self._request_cache_enabled = value
            return self

        def with_request_log_enabled(self, value):
            self._request_log_enabled = value
            return self
