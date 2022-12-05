from abc import ABC, abstractmethod

class LoadUnstructured(ABC):
    @abstractmethod
    def get(self):
        pass


