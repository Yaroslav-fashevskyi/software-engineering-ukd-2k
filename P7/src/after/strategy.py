"""Strategy: тарифи доставки з можливістю заміни алгоритму під час роботи."""
from abc import ABC, abstractmethod

class ShippingStrategy(ABC):
    @abstractmethod
    def calculate(self, weight_kg: float, distance_km: float) -> float:
        pass

class PickupStrategy(ShippingStrategy):
    def calculate(self, weight_kg: float, distance_km: float) -> float:
        return 0.0

class CourierStrategy(ShippingStrategy):
    def calculate(self, weight_kg: float, distance_km: float) -> float:
        return round(70 + distance_km * 5 + weight_kg * 2.5, 2)

class ExpressDeliveryStrategy(ShippingStrategy):
    def calculate(self, weight_kg: float, distance_km: float) -> float:
        cost = 150 + distance_km * 10
        if weight_kg > 5:
            cost *= 1.3
        return round(cost, 2)

class PostMachineStrategy(ShippingStrategy):
    def calculate(self, weight_kg: float, distance_km: float) -> float:
        if weight_kg > 10:
            raise ValueError('Посилка занадто важка для поштомата (макс. 10 кг)')
        return 50.0

class OrderShippingContext:
    def __init__(self, strategy: ShippingStrategy):
        self._strategy = strategy

    def set_strategy(self, strategy: ShippingStrategy) -> None:
        self._strategy = strategy

    def calculate_delivery_cost(self, weight_kg: float, distance_km: float) -> float:
        if weight_kg < 0 or distance_km < 0:
            raise ValueError('Вага та відстань не можуть бути від’ємними')
        return self._strategy.calculate(weight_kg, distance_km)

if __name__ == '__main__':
    context = OrderShippingContext(CourierStrategy())
    for name, strategy in [('Кур’єр', CourierStrategy()),
                           ('Експрес', ExpressDeliveryStrategy()),
                           ('Самовивіз', PickupStrategy()),
                           ('Поштомат', PostMachineStrategy())]:
        context.set_strategy(strategy)
        print(f'{name}: {context.calculate_delivery_cost(6, 15):.2f} грн')
    try:
        context.calculate_delivery_cost(12, 15)
    except ValueError as err:
        print(f'Перевірка обмеження: {err}')
