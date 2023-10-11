import time
from typing import Dict, Optional


class PyTestiqueAnalytics:
    __times: Dict[str, float]

    def __init__(self, name: str) -> None:
        self.__times = {}

    def timeStart(self, name: str) -> None:
        self.__times[name] = time.time()

    def timeStop(self, name: str) -> Optional[float]:
        if name in self.__times:
            return time.time() - self.__times[name]
        return None


class PyTestique:
    analytics: PyTestiqueAnalytics

    def __init__(self):
        self.analytics = PyTestiqueAnalytics()
