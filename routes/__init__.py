# Import all blueprints
from .events import events_bp
from .leveling import leveling_bp
from .rewards import rewards_bp

# __all__ is a special variable in Python that specifies what symbols to export
__all__ = ['events_bp', 'leveling_bp', 'rewards_bp']