"""До рефакторингу: формування чеків через умовні оператори."""
import json
from datetime import datetime
from html import escape

class Order:
    def __init__(self, order_id, customer, discount_percent=0.0):
        self.order_id = order_id
        self.customer = customer
        self.discount_percent = discount_percent
        self.items = []
        self.created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    def add_item(self, name, price, quantity=1):
        self.items.append({'name': name, 'price': price, 'qty': quantity})

    def get_subtotal(self):
        return sum(i['price'] * i['qty'] for i in self.items)

    def get_total(self):
        return round(self.get_subtotal() * (1 - self.discount_percent / 100), 2)

class InvoiceManager:
    def export_invoice(self, order, export_type):
        export_type = export_type.upper()
        if export_type == 'TXT':
            lines = [f'ЧЕК #{order.order_id}', f'Клієнт: {order.customer}']
            for i in order.items:
                lines.append(f"{i['name']} x{i['qty']}: {i['price']*i['qty']:.2f} грн")
            lines.append(f'До сплати: {order.get_total():.2f} грн')
            return '\n'.join(lines)
        elif export_type == 'JSON':
            return json.dumps({'invoice_number': order.order_id, 'client': order.customer,
                               'lines': order.items, 'total': order.get_total()}, ensure_ascii=False, indent=2)
        elif export_type == 'HTML':
            rows = ''.join(f"<tr><td>{escape(i['name'])}</td><td>{i['qty']}</td><td>{i['price']*i['qty']:.2f} грн</td></tr>" for i in order.items)
            return (f"<div style='border:1px solid #333;padding:12px'><h3>Чек #{order.order_id}</h3>"
                    f"<p>Клієнт: {escape(order.customer)}</p><table border='1'><tr><th>Товар</th><th>К-сть</th><th>Сума</th></tr>{rows}</table>"
                    f"<b>До сплати: {order.get_total():.2f} грн</b></div>")
        raise ValueError(f'Невідомий формат: {export_type}')

if __name__ == '__main__':
    order = Order(101, 'Міккі Маус', 10)
    order.add_item('Гітара', 4500, 1)
    order.add_item('Струни', 250, 2)
    manager = InvoiceManager()
    for fmt in ('TXT', 'JSON', 'HTML'):
        print(f'\n--- {fmt} ---')
        print(manager.export_invoice(order, fmt))
