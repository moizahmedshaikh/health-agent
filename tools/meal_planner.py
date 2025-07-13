from typing import TypedDict, List
from agents import function_tool

class DailyMeal(TypedDict):
    day: str
    breakfast: str
    lunch: str
    dinner: str


@function_tool
def generate_meal_planner(diet_type: str) -> List[DailyMeal]:
    """Generate a 7-day static meal plan based on diet type"""

    vegetarian_meals = [
        {"day": "Monday", "breakfast": "Oatmeal with fruits", "lunch": "Chickpea salad", "dinner": "Vegetable stir fry"},
        {"day": "Tuesday", "breakfast": "Fruit smoothie", "lunch": "Lentil soup", "dinner": "Grilled tofu"},
        {"day": "Wednesday", "breakfast": "Avocado toast", "lunch": "Quinoa salad", "dinner": "Veggie curry with rice"},
        {"day": "Thursday", "breakfast": "Greek yogurt with honey", "lunch": "Paneer wrap", "dinner": "Veg biryani"},
        {"day": "Friday", "breakfast": "Banana pancakes", "lunch": "Mixed veg pasta", "dinner": "Mushroom risotto"},
        {"day": "Saturday", "breakfast": "Chia pudding", "lunch": "Grilled veggies sandwich", "dinner": "Spinach lasagna"},
        {"day": "Sunday", "breakfast": "Peanut butter toast", "lunch": "Veg burger", "dinner": "Baked sweet potatoes"}
    ]

    diabetic_meals = [
        {"day": "Monday", "breakfast": "Boiled eggs with multigrain toast", "lunch": "Grilled chicken salad", "dinner": "Steamed fish with veggies"},
        {"day": "Tuesday", "breakfast": "Low-fat yogurt with berries", "lunch": "Quinoa and veggie bowl", "dinner": "Tofu stir fry"},
        {"day": "Wednesday", "breakfast": "Oats with cinnamon", "lunch": "Spinach & turkey wrap", "dinner": "Grilled salmon and greens"},
        {"day": "Thursday", "breakfast": "Chia pudding with almonds", "lunch": "Baked beans with quinoa", "dinner": "Chicken soup and salad"},
        {"day": "Friday", "breakfast": "Egg white omelet", "lunch": "Zucchini noodles", "dinner": "Cauliflower rice with tofu"},
        {"day": "Saturday", "breakfast": "Smoothie with unsweetened almond milk", "lunch": "Brown rice with dal", "dinner": "Veg stew"},
        {"day": "Sunday", "breakfast": "Cottage cheese with berries", "lunch": "Grilled paneer salad", "dinner": "Lentil curry"}
    ]

    keto_meals = [
        {"day": "Monday", "breakfast": "Scrambled eggs with avocado", "lunch": "Chicken Caesar salad", "dinner": "Grilled steak with buttered broccoli"},
        {"day": "Tuesday", "breakfast": "Cheese omelet", "lunch": "Zoodles with pesto", "dinner": "Baked salmon with asparagus"},
        {"day": "Wednesday", "breakfast": "Bulletproof coffee", "lunch": "Egg salad lettuce wraps", "dinner": "Stuffed bell peppers"},
        {"day": "Thursday", "breakfast": "Chia seed pudding (unsweetened)", "lunch": "Tuna salad", "dinner": "Bunless burger with veggies"},
        {"day": "Friday", "breakfast": "Coconut flour pancakes", "lunch": "Grilled chicken thighs", "dinner": "Zucchini lasagna"},
        {"day": "Saturday", "breakfast": "Boiled eggs with cheese", "lunch": "Keto soup", "dinner": "Keto pizza"},
        {"day": "Sunday", "breakfast": "Almond butter smoothie", "lunch": "Shrimp salad", "dinner": "Cauliflower mac and cheese"}
    ]

    balanced_meals = [
        {"day": "Monday", "breakfast": "Boiled egg and toast", "lunch": "Grilled chicken wrap", "dinner": "Rice and beans"},
        {"day": "Tuesday", "breakfast": "Fruit bowl with yogurt", "lunch": "Grilled fish with salad", "dinner": "Whole wheat pasta"},
        {"day": "Wednesday", "breakfast": "Peanut butter toast", "lunch": "Chicken biryani (low oil)", "dinner": "Veg pulao"},
        {"day": "Thursday", "breakfast": "Milk with cereal", "lunch": "Paneer tikka with naan", "dinner": "Chapati with sabzi"},
        {"day": "Friday", "breakfast": "Banana smoothie", "lunch": "Veg wrap", "dinner": "Rice with chicken curry"},
        {"day": "Saturday", "breakfast": "Cheese sandwich", "lunch": "Shawarma plate", "dinner": "Veg noodles"},
        {"day": "Sunday", "breakfast": "Multigrain paratha", "lunch": "Daal chawal", "dinner": "Chapati with keema"}
    ]

    diet = diet_type.lower()

    if "vegetarian" in diet:
        return vegetarian_meals 
    elif "diabetic" in diet:
        return diabetic_meals
    elif "keto" in diet:
        return keto_meals
    else:
        return balanced_meals