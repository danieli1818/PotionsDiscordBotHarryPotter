

from Tree import Tree

from os import listdir
from os.path import dirname, abspath


class PotionStepNode:

    def __init__(self, color=None, potion=None):
        self.potion = potion
        self.color = color

    def set_potion(self, potion):
        self.potion = potion

    def set_color(self, color):
        self.color = color

    def has_color(self):
        return self.color is not None

    def get_potion(self):
        return self.potion


def load_potions_recipes_tree():
    from PotionRecipe import PotionRecipe
    tree = Tree()
    potions_files_paths = [dirname(abspath(__file__)) + "\\PotionsRecipes\\" + f for f in listdir(dirname(abspath(__file__)) + "\\PotionsRecipes")]
    print(potions_files_paths)
    for potion_file_path in potions_files_paths:
        current_potion_recipe = PotionRecipe.load_from_json(potion_file_path)
        tree.add_path(current_potion_recipe.get_tree_path(), on_child_exist_function)
    return tree


def on_child_exist_function(prev_info, current_info):
    if not prev_info.has_color() and current_info.has_color():
        return current_info
    else:
        return prev_info
