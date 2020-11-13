
import json

from PotionStepNode import PotionStepNode


class PotionRecipe:

    def __init__(self):
        self.recipe = []
        self.name = ""
        self.description = ""

    @staticmethod
    def load_from_json(json_file_path):
        pr = PotionRecipe()
        with open(json_file_path) as json_file:
            potion_data = json.load(json_file)
        if potion_data is None:
            return None
        print(potion_data)
        potion_recipe = potion_data["recipe"]
        if potion_recipe is None:
            return None
        for ingredient in potion_recipe:
            if type(ingredient) is str:
                pr.recipe.append(ingredient.lower())
            elif type(ingredient) is dict:
                times = ingredient["times"]
                if times is None:
                    times = 1
                ingredient_name = ingredient["name"]
                if ingredient_name is None or type(ingredient_name) is not str:
                    continue
                ingredient_name = ingredient_name.lower()
                for index in range(times):
                    pr.recipe.append(ingredient_name)
        if potion_data["name"] is not None:
            pr.name = potion_data["name"]
        if potion_data["description"] is not None:
            pr.description = potion_data["description"]
        return pr

    def get_tree_path(self):
        path = []
        for step in self.recipe:
            path.append((step, PotionStepNode()))
        path[-1][1].set_potion(self.name)
        return path
