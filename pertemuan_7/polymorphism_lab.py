class MobMinecraft:
    def __init__(self, name, health: int):
        self.name = name
        self.health = health

    def attack(self):
        return f"{self.name} attacks with a basic attack!"
    def health_status(self):
        return f"{self.name} has {self.health} health bar left."
class Skeleton(MobMinecraft):
    def attack(self):
        return f"{self.name} is territorial and shoots an arrow!"
    def health_status(self):
        return f"{self.name} has {self.health} health bar, so its weaker then you."
class Creeper(MobMinecraft):
    def attack(self):
        return f"Beware of {self.name}! It will jumpscare and explodes!"
    def health_status(self):
        return f"{self.name} has {self.health} health bar, its still weaker then you, but still dangerous."
def simulate_battle(mob):
    print(mob.attack())
    print(mob.health_status())

player = MobMinecraft("Steve", 100)
skeleton = Skeleton("Skeleton", 20)
creeper = Creeper("Creeper", 30)

simulate_battle(player)
simulate_battle(skeleton)
simulate_battle(creeper)