class ChoreAllocationException(Exception):
    """Custom exception for errors during chore allocation."""
    def __init__(self, message="An error occurred during chore allocation"):
        self.message = message
        super().__init__(self.message)
