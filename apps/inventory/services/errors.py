class InventoryError(Exception):
    pass

class InsufficientStock(InventoryError):
    def __init__(self, available: int, requested: int):
        super().__init__(f"Insufficient stock: available={available}, requested={requested}")
        self.available = available
        self.requested = requested
