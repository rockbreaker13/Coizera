"""
This module provides a pub/sub or (publisher/subscriber) system
for dispatching and handling events.

Example:

"""

from __future__ import annotations
from typing import Any, Callable, Dict, Generic, List, Tuple, TypeVar

import inspect
import weakref
from logging import getLogger

T = TypeVar("T")
logger = getLogger(__name__)


class Topic(Generic[T]):
    """
    A strongly-typed topic token used for routing events to
    subscribers.
    """

    def __init__(self, name: str):
        self.name = name


Handler = Callable[[T], None]


class WeakSubscriber(Generic[T]):
    def __init__(self, handler: Handler[T]) -> None:
        if inspect.ismethod(handler):
            self.ref = weakref.WeakMethod(handler)
        else:
            self.ref = weakref.ref(handler)

    def get_handler(self) -> Handler[T] | None:
        return self.ref()


class GameEventBus:
    def __init__(self) -> None:
        self._routes: Dict[str, List[WeakSubscriber[Any]]] = dict()
        self._pending_events: List[Tuple[Topic[Any], Any]] = []

    def subscribe(self, topic: Topic[T], handler: Handler[T]) -> None:
        subscriber = WeakSubscriber(handler)
        if topic.name not in self._routes:
            self._routes[topic.name] = [subscriber]
        else:
            self._routes[topic.name].append(subscriber)

    def publish(self, topic: Topic[T], event_data: T) -> None:
        self._pending_events.append((topic, event_data))

    def on(self, topic: Topic[T]) -> Callable[[Handler[T]], Handler[T]]:
        def decorator(func: Handler[T]) -> Handler[T]:
            self.subscribe(topic, func)
            return func

        return decorator

    def dispatch(self) -> None:
        """Called once per frame to process the event queue."""
        events_to_process = self._pending_events
        self._pending_events = []

        for topic, event_data in events_to_process:
            if topic.name not in self._routes:
                continue

            alive_subscribers: List[WeakSubscriber[Any]] = []

            for subscriber in self._routes[topic.name]:
                handler = subscriber.get_handler()
                if handler is not None:
                    alive_subscribers.append(subscriber)
                    handler(event_data)

            self._routes[topic.name] = alive_subscribers

        def on(self, topic: Topic[T]) -> Callable[[Handler[T]], Handler[T]]:
            """
            Decorator to register a standalone function to a topic.
            WARNING: Do not use this on class instance methods.
            """
            def decorator(func: Handler[T]) -> Handler[T]:
                self.subscribe(topic, func)
                return func
            return decorator            

            
event_bus = GameEventBus()
