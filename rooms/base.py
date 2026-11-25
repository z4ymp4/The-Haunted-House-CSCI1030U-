"""Room base class. Every room inherits from this (Member 1)."""


class Room:
    room_id = "room"
    title = "A Room"
    reward_keys = []    # given automatically when --start-room skips this room
    reward_items = []

    def __init__(self, settings):
        self.settings = settings

    def play(self, ctx, player):
        """Run the room using ctx.say / ctx.ask. Return True if cleared."""
        raise NotImplementedError

    def to_dict(self):
        return {}

    def from_dict(self, data):
        pass

    def finish(self, player):
        if self.room_id not in player.rooms_completed:
            player.rooms_completed.append(self.room_id)
        return True

    def give_rewards(self, player):
        for key in self.reward_keys:
            player.add_key(key)
        for item in self.reward_items:
            player.add_item(item)