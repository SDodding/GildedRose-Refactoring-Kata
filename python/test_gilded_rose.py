# -*- coding: utf-8 -*-
import unittest

from gilded_rose_refactored import Item, GildedRose


class GildedRoseTest(unittest.TestCase):
    def test_foo(self):
        items = [Item("foo", 0, 0)]
        gr = GildedRose(items)
        gr.update_quality()
        self.assertEqual("foo", items[0].name)

    def test_sell_by_passed(self):
        items = [
            Item("Old Item", 0, 5),
            Item("Medium Item", 1, 5),
            Item("New Item", 2, 5)
        ]
        gr = GildedRose(items)

        gr.update_quality()
        self.assertEqual(3, gr.items[0].quality, "Item is past sellby. Lose 2 quality")
        self.assertEqual(4, gr.items[1].quality, "Item is inside sellby. Lose 1 quality")
        self.assertEqual(4, gr.items[2].quality, "Item is inside sellby. Lose 1 quality")
        gr.update_quality()
        self.assertEqual(1, gr.items[0].quality, "Item is past sellby. Lose 2 quality")
        self.assertEqual(2, gr.items[1].quality, "Item is past sellby. Lose 2 quality")
        self.assertEqual(3, gr.items[2].quality, "Item is inside sellby. Lose 1 quality")
        gr.update_quality()
        self.assertEqual(0, gr.items[0].quality, "Item is past sellby. Lose 2 quality, but do not go below 0")
        self.assertEqual(0, gr.items[1].quality, "Item is past sellby. Lose 2 quality")
        self.assertEqual(1, gr.items[2].quality, "Item is past sellby. Lose 2 quality")

    def test_quality_min_constraint(self):
        items = [
            Item("Old Item", 0, 1),
            Item("Medium Item", 999, 1),
        ]
        gr = GildedRose(items)

        gr.update_quality()
        self.assertEqual(0, gr.items[0].quality, "Item quality cannot go below 0 when past sellby")
        self.assertEqual(0, gr.items[1].quality, "Item quality cannot go below 0 inside sellby")
        gr.update_quality()
        self.assertEqual(0, gr.items[0].quality, "Item quality cannot go below 0 when past sellby")
        self.assertEqual(0, gr.items[1].quality, "Item quality cannot go below 0 inside sellby")
        
    def test_quality_brie(self):
        items = [
            Item("Aged Brie", 1, 46),
        ]
        gr = GildedRose(items)

        gr.update_quality()
        self.assertEqual(47, gr.items[0].quality, "Brie quality increases by 1 inside sellby")
        gr.update_quality()
        self.assertEqual(49, gr.items[0].quality, "Brie quality increases by 2 outside sellby")
        gr.update_quality()
        self.assertEqual(50, gr.items[0].quality, "Brie quality increases by 2 outside sellby but does not go above 50")
        gr.update_quality()
        self.assertEqual(50, gr.items[0].quality, "Brie quality increases by 2 outside sellby but does not go above 50")

    def test_sulfuras_legendary_qualities(self):
        QUALITY_DESCR = "Sulfuras quality is constant"
        SELLIN_DESCR = "Sulfuras sell_in is constant"
        SULFURAS_QUALITY = 80

        items = [
            Item(name="Sulfuras, Hand of Ragnaros", sell_in=1, quality=SULFURAS_QUALITY),
            Item(name="Sulfuras, Hand of Ragnaros", sell_in=-1, quality=SULFURAS_QUALITY),
            Item(name="Sulfuras, Hand of Ragnaros", sell_in=90, quality=SULFURAS_QUALITY),
        ]
        gr = GildedRose(items)

        gr.update_quality()
        self.assertEqual(SULFURAS_QUALITY, gr.items[0].quality, QUALITY_DESCR)
        self.assertEqual(SULFURAS_QUALITY, gr.items[1].quality, QUALITY_DESCR)
        self.assertEqual(SULFURAS_QUALITY, gr.items[2].quality, QUALITY_DESCR)
        self.assertEqual(1, gr.items[0].sell_in, SELLIN_DESCR)
        self.assertEqual(-1, gr.items[1].sell_in, SELLIN_DESCR)
        self.assertEqual(90, gr.items[2].sell_in, SELLIN_DESCR)
        gr.update_quality()
        self.assertEqual(SULFURAS_QUALITY, gr.items[0].quality, QUALITY_DESCR)
        self.assertEqual(SULFURAS_QUALITY, gr.items[1].quality, QUALITY_DESCR)
        self.assertEqual(SULFURAS_QUALITY, gr.items[2].quality, QUALITY_DESCR)
        self.assertEqual(1, gr.items[0].sell_in, SELLIN_DESCR)
        self.assertEqual(-1, gr.items[1].sell_in, SELLIN_DESCR)
        self.assertEqual(90, gr.items[2].sell_in, SELLIN_DESCR)

    def test_backstage_pass(self):
        items = [
            Item(name="Backstage passes to a TAFKAL80ETC concert", sell_in=1, quality=20),
            Item(name="Backstage passes to a TAFKAL80ETC concert", sell_in=11, quality=30),
            Item(name="Backstage passes to a TAFKAL80ETC concert", sell_in=6, quality=40)
        ]
        gr = GildedRose(items)

        gr.update_quality()
        self.assertEqual(23, gr.items[0].quality, "Quality increases by 3 for days < 5 and >= 0.")
        self.assertEqual(31, gr.items[1].quality, "Quality incrases by 1 for days >= 10")
        self.assertEqual(42, gr.items[2].quality, "Quality incrases by 2 for days < 10")
        gr.update_quality()
        self.assertEqual(0, gr.items[0].quality, "Quality is 0 after the concert")
        self.assertEqual(33, gr.items[1].quality, "Quality incrases by 2 for days == 10")
        self.assertEqual(45, gr.items[2].quality, "Quality incrases by 3 for days == 5 and >= 0.")
        gr.update_quality()
        self.assertEqual(0, gr.items[0].quality, "Quality is 0 after the concert")
        self.assertEqual(35, gr.items[1].quality, "Quality incrases by 2 for days <= 10")
        self.assertEqual(48, gr.items[2].quality, "Quality incrases by 3 for days <= 5")
        gr.update_quality()
        self.assertEqual(0, gr.items[0].quality, "Quality is 0 after the concert")
        self.assertEqual(37, gr.items[1].quality, "Quality incrases by 2 for days <= 10")
        self.assertEqual(50, gr.items[2].quality, "Quality incrases by 3 for days <= 5 and >= 0 but cannot go above 50")

    def test_conjured_items(self):
        items = [
            Item(name="Conjured Mana Cake", sell_in=1, quality=4),
            Item(name="Conjured Mana Cake", sell_in=2, quality=40)
        ]
        gr = GildedRose(items)

        gr.update_quality()
        self.assertEqual(2, gr.items[0].quality, "Conjured quality drops twice as fast as normal within sellby")
        self.assertEqual(38, gr.items[1].quality, "Conjured quality drops twice as fast as normal within sellby")
        gr.update_quality()
        self.assertEqual(0, gr.items[0].quality, "Conjured quality drops twice as fast as normal within sellby")
        self.assertEqual(36, gr.items[1].quality, "Conjured quality drops twice as fast as normal within sellby")
        gr.update_quality()
        self.assertEqual(0, gr.items[0].quality, "Conjured quality does not go below 0")
        self.assertEqual(32, gr.items[1].quality, "Conjured quality drops twice as fast outside sellby")


if __name__ == '__main__':
    unittest.main()
