# -*- coding: utf-8 -*-

class DefaultBehaviour(object):
    MIN_QUALITY = 0
    MAX_QUALITY = 50

    def __init__(self, item):
        self.item = item

    def update_sell_in(self, amount=-1):
        self.item.sell_in += amount

    def apply_quality_constraints(self):
        if self.item.quality < self.MIN_QUALITY:
            self.item.quality = self.MIN_QUALITY
        elif self.item.quality > self.MAX_QUALITY:
            self.item.quality = self.MAX_QUALITY

    def update_quality(self, amount=-1):
        self.item.quality += amount
        self.apply_quality_constraints()

    def tick(self):
        self.update_sell_in()

        quality_change = -1 
        if self.item.sell_in < 0:
            quality_change *= 2
        self.update_quality(quality_change)

class BrieBehaviour(DefaultBehaviour):
    def tick(self):
        self.update_sell_in()

        quality_change = 1
        if self.item.sell_in < 0:
            quality_change *= 2

        self.update_quality(quality_change)

class BackstageBehaviour(DefaultBehaviour):
    def tick(self):
        self.update_sell_in()

        quality_change = 1
        if self.item.sell_in < 5:
            quality_change = 3
        elif self.item.sell_in < 10:
            quality_change = 2
        self.update_quality(quality_change)

        if self.item.sell_in < 0:
            self.item.quality = 0

class SulfurasBehaviour(DefaultBehaviour):
    def tick(self):
        pass

class ConjuredBehaviour(DefaultBehaviour):
    def tick(self):
        self.update_sell_in()

        quality_change = -2
        if self.item.sell_in < 0:
            quality_change *= 2
        self.update_quality(quality_change)

class ItemBehaviourFactory(object):
    mappings = {
        "Aged Brie": BrieBehaviour,
        "Sulfuras, Hand of Ragnaros": SulfurasBehaviour,
        "Backstage passes to a TAFKAL80ETC concert": BackstageBehaviour,
        "Conjured Mana Cake": ConjuredBehaviour
    }

    @classmethod
    def create(cls, item):
        if item.name in cls.mappings:
            return cls.mappings[item.name](item)

        return DefaultBehaviour(item)

class GildedRose(object):

    def __init__(self, items):
        self.items = items

    def update_quality(self):
        for item in self.items:
            item_behaviour = ItemBehaviourFactory.create(item)
            item_behaviour.tick()

class Item:
    def __init__(self, name, sell_in, quality):
        self.name = name
        self.sell_in = sell_in
        self.quality = quality

    def __repr__(self):
        return "%s, %s, %s" % (self.name, self.sell_in, self.quality)
