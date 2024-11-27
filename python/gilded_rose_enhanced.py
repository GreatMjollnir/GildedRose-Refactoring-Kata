
"""
    This module contains the implementation of the Gilded Rose inventory system with various item update strategies.

    Classes:
        Item: Represents an item in the inventory.
        ItemStrategy: Abstract base class for item update strategies.
        NormalItemStrategy: Strategy for updating normal items.
        AgedBrieStrategy: Strategy for updating "Aged Brie" items.
        SulfurasStrategy: Strategy for updating "Sulfuras" items.
        BackstagePassesStrategy: Strategy for updating "Backstage passes" items.
        ConjuredItemStrategy: Strategy for updating "Conjured" items.
        GildedRose: Manages the inventory and updates the quality of items using appropriate strategies.

"""
class Item:
    """
    A class representing an item in the Gilded Rose inventory.

    Attributes:
        name (str): The name of the item.
        sell_in (int): The number of days we have to sell the item.
        quality (int): The quality of the item.

    Methods:
        __repr__(): Returns a string representation of the item.
    """

    def __init__(self, name, sell_in, quality):
        """
        Initializes a new instance of the Item class.

        Args:
            name (str): The name of the item.
            sell_in (int): The number of days we have to sell the item.
            quality (int): The quality of the item.
        """
        self.name = name
        self.sell_in = sell_in
        self.quality = quality

    def __repr__(self):
        """
        Return a string representation of the object.

        The string representation includes the name, sell_in, and quality
        attributes of the object, formatted as "name, sell_in, quality".

        Returns:
            str: A string representation of the object.
        """
        return "%s, %s, %s" % (self.name, self.sell_in, self.quality)


class ItemStrategy:
    """
    A base class for item update strategies in the Gilded Rose inventory system.

    This class defines the interface for updating the quality of an item. 
    Subclasses must implement the `update_quality` method to provide specific 
    behavior for different types of items.

    Methods:
        update_quality(item):
            Abstract method to update the quality of the given item. 
            Must be implemented by subclasses.

    Raises:
        NotImplementedError: If the `update_quality` method is not implemented 
                             by a subclass.
    """
    def update_quality(self, item):
        raise NotImplementedError("Subclasses must implement this method")


class NormalItemStrategy(ItemStrategy):
    """
    Strategy for updating the quality and sell-in values of normal items.

    Methods:
        update_quality(item):
            Updates the quality and sell-in values of the given item.
            - Decreases the quality by 1 if it is greater than 0.
            - Decreases the sell-in value by 1.
            - If the sell-in value is less than 0 and the quality is greater than 0, decreases the quality by an additional 1.
    """
    def update_quality(self, item):

        # decrease quality and sell_in by 1
        item.quality -= 1
        item.sell_in -= 1

        # once the sell-by date has passed, quality degrades twice as fast
        if item.sell_in < 0 and item.quality > 0:
            item.quality -= 1

        # quality is never negative
        if item.quality < 0:
            item.quality = 0
        
        # quality is never more than 50
        if item.quality > 50:
            item.quality = 50


class AgedBrieStrategy(ItemStrategy):
    """
    Strategy for updating the quality and sell-in values of Aged Brie items.

    Aged Brie increases in quality the older it gets. The quality of an item is never more than 50.
    Once the sell-in date has passed, the quality increases twice as fast.

    Methods:
        update_quality(item): Updates the quality and sell-in values of the given item.
    """
    def update_quality(self, item):
        # aged-brie enhance quality with time:
        item.quality += 1
        item.sell_in -= 1
        
        # once the sell-by date has passed, quality enhances twice as fast
        if item.sell_in < 0 and item.quality < 50:
            item.quality += 1

        # quality is never negative
        if item.quality < 0:
            item.quality = 0
        
        # quality is never more than 50
        if item.quality > 50:
            item.quality = 50


class SulfurasStrategy(ItemStrategy):
    """
    Strategy for updating the quality of Sulfuras items.

    Sulfuras is a legendary item that does not change in quality or sell-in value.
    Therefore, the `update_quality` method does not perform any operations.

    Methods:
        update_quality(item): makes sure that Sulfuras quality is always 80 and sell_in is always 0.
    """
    def update_quality(self, item):
        item.quality = 80  # Sulfuras quality is always 80

class BackstagePassesStrategy(ItemStrategy):
    """
    Strategy for updating the quality and sell_in values of Backstage Passes items.

    Backstage Passes increase in quality as their sell_in value approaches:
    - Quality increases by 1 when there are more than 10 days left.
    - Quality increases by 2 when there are 10 days or less.
    - Quality increases by 3 when there are 5 days or less.
    - Quality drops to 0 after the concert (sell_in < 0).

    Attributes:
        None

    Methods:
        update_quality(item):
            Updates the quality and sell_in values of the given item according to the rules for Backstage Passes.
    """
    def update_quality(self, item):
        
        # time passes
        item.sell_in -= 1
        
        # backstage passes enhance quality with time
        if item.quality < 50:
            item.quality += 1
            
            # when 10 days or less left, quality enhances twice as fast
            if item.sell_in < 10:
                item.quality += 1
            
            # when 5 days or less left, quality enhances thrice as fast
            if item.sell_in < 5:
                item.quality += 1
       
        # quality drops to 0 after the concert 
        if item.sell_in < 0:
            item.quality = 0
        
        # quality is never negative
        if item.quality < 0:
            item.quality = 0
        
        # quality is never more than 50
        if item.quality > 50:
            item.quality = 50


class ConjuredItemStrategy(ItemStrategy):
    """
    Strategy for updating the quality and sell_in values of 'Conjured' items in the Gilded Rose inventory system.

    Conjured items degrade in quality twice as fast as normal items. This strategy decreases the quality by 2 each day.
    If the sell_in value is less than 0, the quality decreases by an additional 2 each day.

    Methods:
        update_quality(item):
            Updates the quality and sell_in values of the given item according to the rules for Conjured items.
    """
    def update_quality(self, item):
        # works like normal items but degrades twice as fast

        # decrease quality and sell_in by 1
        item.quality -= 2
        item.sell_in -= 1

        # once the sell-by date has passed, quality degrades twice as fast
        if item.sell_in < 0 and item.quality > 0:
            item.quality -= 2

        # quality is never negative
        if item.quality < 0:
            item.quality = 0
        
        # quality is never more than 50
        if item.quality > 50:
            item.quality = 50



class GildedRose:
    """
    GildedRose class that manages a collection of items and updates their quality
    based on specific strategies for different types of items.

    Attributes:
        items (list): A list of items to be managed.
        strategies (dict): A dictionary mapping item names to their respective
                           quality update strategies.

    Methods:
        update_quality():
            Updates the quality of all items in the collection using their
            respective strategies.
    """

    def __init__(self, items):
        """
        Initializes the GildedRose class with a list of items and their corresponding update strategies.

        Args:
            items (list): A list of item objects to be managed by the GildedRose class.

        Attributes:
            items (list): Stores the list of items.
            strategies (dict): A dictionary mapping item names to their corresponding update strategy objects.
                - "Aged Brie": Uses AgedBrieStrategy.
                - "Sulfuras, Hand of Ragnaros": Uses SulfurasStrategy.
                - "Backstage passes to a TAFKAL80ETC concert": Uses BackstagePassesStrategy.
                - "Conjured": Uses ConjuredItemStrategy.
        """
        self.items = items
        self.strategies = {
            "Aged Brie": AgedBrieStrategy(),
            "Sulfuras, Hand of Ragnaros": SulfurasStrategy(),
            "Backstage passes to a TAFKAL80ETC concert": BackstagePassesStrategy(),
            "Conjured": ConjuredItemStrategy()
        }

    def update_quality(self):
        """
        Updates the quality of all items in the inventory using their respective strategies.

        Iterates through each item in the inventory and applies the appropriate strategy
        to update its quality. If an item does not have a specific strategy, the default
        NormalItemStrategy is used.

        Returns:
            None
        """
        for item in self.items:
            strategy = self.strategies.get(item.name, NormalItemStrategy())
            strategy.update_quality(item)


# Example usage
if __name__ == "__main__":
    # Example usage of the GildedRose class
    # Create a list of items
    items = [
        Item(name="Aged Brie", sell_in=2, quality=0),
        Item(name="Sulfuras, Hand of Ragnaros", sell_in=0, quality=80),
        Item(name="Backstage passes to a TAFKAL80ETC concert", sell_in=15, quality=20),
        Item(name="Conjured Mana Cake", sell_in=3, quality=6),
        Item(name="+5 Dexterity Vest", sell_in=10, quality=20)
    ]

    # Create a GildedRose instance with the list of items
    gilded_rose = GildedRose(items)
    
    # Update the quality of the items
    gilded_rose.update_quality()
    
    # Print the updated items
    for item in items:
        print(item)