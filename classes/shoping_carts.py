# 3. Класс для управления корзиной покупок
from classes.users import Admin
from classes.users import Customer

class ShoppingCart:
    """
    Класс, представляющий корзину покупок.
    """
    def __init__(self, customer: Customer, admin: Admin):
        self.items = []
        self.customer = customer
        self.admin = admin

    def add_item(self, product, quantity, admin: Admin):
        """
        Добавляет продукт в корзину.
        """
        self.items.append({"Продукт": product, "количество": quantity})
        self.admin = admin

    def remove_item(self, product_name, admin: Admin):
        """
        Удаляет продукт из корзины по имени.
        """
        self.items = [item for item in self.items if item["Продукт"].name != product_name]
        self.admin = admin

    def get_total(self):
        """
        Возвращает общую стоимость продуктов в корзине.
        """
        total = sum(item["Продукт"].price * item["количество"] for item in self.items)
        return total

    def get_details(self):
        """
        Возвращает детализированную информацию о содержимом корзины и общей стоимости.
        """
        details = f"Покупатель {self.customer.username} приобрёл:\n"
        for item in self.items:
            details += f"{item['Продукт'].get_details()}, Количество: {item['количество']}\n"
        details += f"На общую сумму: {self.get_total()} руб\n"
        details += f"Зарегистрировал покупки пользователь {self.admin.username}"
        return details
