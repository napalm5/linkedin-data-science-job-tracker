from abc import ABC, abstractmethod

class ExportResults(ABC):
    @abstractmethod
    def put(self):
        pass

