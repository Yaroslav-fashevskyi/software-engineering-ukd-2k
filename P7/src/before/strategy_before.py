"""До рефакторингу: алгоритми доставки у спільному методі."""
class DeliveryCalculator:
    def calculate_cost(self, delivery_type: str, weight_kg: float, distance_km: float) -> float:
        delivery_type = delivery_type.upper()
        if delivery_type == 'PICKUP':
            return 0.0
        elif delivery_type == 'COURIER':
            return round(70 + distance_km * 5 + weight_kg * 2.5, 2)
        elif delivery_type == 'EXPRESS':
            cost = 150 + distance_km * 10
            if weight_kg > 5:
                cost *= 1.3
            return round(cost, 2)
        raise ValueError(f'Невідомий тип доставки: {delivery_type}')

if __name__ == '__main__':
    calc = DeliveryCalculator()
    for kind in ('PICKUP', 'COURIER', 'EXPRESS'):
        print(f'{kind}: {calc.calculate_cost(kind, 6, 15):.2f} грн')
