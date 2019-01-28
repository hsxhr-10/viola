from viola.epoll import Epoll
import time


class EventsEmptyException(Exception):
    pass


class EventLoop(object):
    """A epoll-based event loop. Use edge trigger mode of epoll"""
    # Constant of EventLoop
    READ = Epoll.READ
    WRITE = Epoll.WRITE
    ERROR = Epoll.ERROR
    ET = Epoll.ET

    @classmethod
    def instance(cls, scheduler):
        """Singleton mode"""
        if not hasattr(cls, "_instance"):
            cls._instance = cls(scheduler)
        return cls._instance

    def __init__(self, scheduler):
        self.epoll = Epoll()
        self.handlers = {}
        self.scheduler = scheduler

    def add_handler(self, fd, events, handler):
        """
        Register listen fd to epoll and add handler
        Addition of EventLoop.ERROR for events
        """
        if not events:
            raise EventsEmptyException
        self.epoll.register(fd, events | EventLoop.ERROR)
        self.handlers[fd] = handler
        # print("[add_handler]", self.handlers)

    def remove_handler(self, fd):
        """Unregister listen fd from epoll and remove handler"""
        self.epoll.unregister(fd)
        self.handlers.pop(fd)
        # print("[remove_handler]", self.handlers)

    def update_handler(self, fd, events):
        """Update interested event of fd"""
        if not events:
            raise EventsEmptyException
        self.epoll.modify(fd, events | EventLoop.ERROR)
        # print("[update_handler]", self.handlers)

    def start(self):
        while True:
            poll_timeout = 0.2
            now = time.time()
            while self.scheduler.tasks and \
                    (self.scheduler.tasks[0].deadline <= now):
                self.scheduler.tasks[0].callback()
                self.scheduler.tasks.popleft()

            # Priority run task if interval less than `timeout`
            if self.scheduler.tasks:
                interval = self.scheduler.tasks[0].deadline - now
                poll_timeout = min(interval, poll_timeout)

            events = self.epoll.poll(poll_timeout)
            for fd, event in events:
                # Run `_handler_event` of httpserver module
                self.handlers[fd](fd, event)

    def stop(self):
        pass
