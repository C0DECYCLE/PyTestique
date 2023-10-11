import time
from typing import Dict, Optional


class PyTestiqueAnalytics:
    __timeDict: Dict[str, float]

    def __init__(self, name: str) -> None:
        self.__timeDict = {}

    def timeStart(self, name: str) -> None:
        self.__timeDict[name] = time.time()

    def timeStop(self, name: str) -> Optional[float]:
        if name in self.__timeDict:
            return time.time() - self.__timeDict[name]
        return None


class PyTestique:
    analytics: PyTestiqueAnalytics

    def __init__(self):
        self.analytics = PyTestiqueAnalytics()
