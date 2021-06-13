# -*- coding: utf-8 -*-

class DefaultBehaviour(object):
    MIN_QUALITY = 0
    MAX_QUALITY = 50

    def __init__(self, item):
        self.item = item

    def update_sell_in(self, delta=-1):
        self.item.sell_in += delta

    def apply_quality_constraints(self):
        if self.item.quality < self.MIN_QUALITY:
            self.item.quality = self.MIN_QUALITY
        elif self.item.quality > self.MAX_QUALITY:
            self.item.quality = self.MAX_QUALITY

    def update_quality(self, delta=-1):
        self.item.quality += delta
        self.apply_quality_constraints()

    def apply_quality_behaviour(self):
        quality_delta = -1 
        if self.item.sell_in < 0:
            quality_delta *= 2
        self.update_quality(quality_delta)

    def tick(self):
        self.update_sell_in()
        self.apply_quality_behaviour() 

class BrieBehaviour(DefaultBehaviour):
    def apply_quality_behaviour(self):
        quality_delta = 1
        if self.item.sell_in < 0:
            quality_delta *= 2

        self.update_quality(quality_delta)

class BackstageBehaviour(DefaultBehaviour):
    QUALITY_THRESH_TEN_DAYS = 10
    QUALITY_THRESH_FIVE_DAYS = 5

    def apply_quality_behaviour(self):
        if self.item.sell_in < 0:
            self.item.quality = 0
            return

        quality_delta = 1
        if self.item.sell_in < self.QUALITY_THRESH_FIVE_DAYS:
            quality_delta = 3
        elif self.item.sell_in < self.QUALITY_THRESH_TEN_DAYS:
            quality_delta = 2
        self.update_quality(quality_delta)

class SulfurasBehaviour(DefaultBehaviour):
    def tick(self):
        pass

class ConjuredBehaviour(DefaultBehaviour):
    def apply_quality_behaviour(self):
        quality_delta = -2
        if self.item.sell_in < 0:
            quality_delta *= 2
        self.update_quality(quality_delta)

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
