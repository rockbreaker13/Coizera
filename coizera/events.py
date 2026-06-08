from dataclasses import dataclass
from coizera.pubsub import Topic

@dataclass
class PlayerTakesDamage:
    damage: int

@dataclass
class PlayerPicksUpItem:
    item_name: str

@dataclass
class ScreenShake:
    intensity: float

PLAYER_TAKES_DAMAGE = Topic[PlayerTakesDamage]("player:takes_damage")
PLAYER_PICKS_UP_ITEM = Topic[PlayerPicksUpItem]("player:picks_up_item")
SCREEN_SHAKE = Topic[ScreenShake]("screen:shake")
