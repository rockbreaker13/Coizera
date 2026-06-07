"""
This module is responsible for loading and playing sound effects.
"""

from importlib import resources
from logging import getLogger
from typing import Optional

from pygame import mixer


logger = getLogger(__name__)


ATTACK: Optional[mixer.Sound] = None
CRAFT: Optional[mixer.Sound] = None
HURT: Optional[mixer.Sound] = None
PICKUP: Optional[mixer.Sound] = None
SELECT: Optional[mixer.Sound] = None


def load_sfx():
    """
    Load all sound effects and prepare them for playback.
    """
    global ATTACK, CRAFT, HURT, PICKUP, SELECT

    if mixer.get_init() is None:
        logger.warn("Could not load sound effects, the pygame mixer wasn't initialized")

    ATTACK = mixer.Sound(resources.files("coizera.assets").joinpath("attack.wav"))
    CRAFT = mixer.Sound(resources.files("coizera.assets").joinpath("craft.wav"))
    HURT = mixer.Sound(resources.files("coizera.assets").joinpath("hurt.wav"))
    PICKUP = mixer.Sound(resources.files("coizera.assets").joinpath("pickup.wav"))
    SELECT = mixer.Sound(resources.files("coizera.assets").joinpath("select.wav"))
