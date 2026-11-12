"""Factory Method: TXT, JSON, HTML, Markdown та CSV. Python 3.10+."""
import csv
import io
import json
from abc import ABC, abstractmethod
from datetime import datetime
from html import escape

class Order:
    def __init__(self, order_id: int, customer: str, discount_percent: float = 0.0):
        self.order_id = order_id
        self.customer = customer
        self.discount_percent = discount_percent
        self.items: list[dict] = []
        self.created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    def add_item(self, name: str, price: float, quantity: int = 1) -> None:
        if price < 0 or quantity < 1:
            raise ValueError('Ціна має бути невід’ємною, а кількість — додатною')
        self.items.append({'name': name, 'price': price, 'qty': quantity})

    def get_subtotal(self) -> float:
        return sum(i['price'] * i['qty'] for i in self.items)

    def get_total(self) -> float:
        return round(self.get_subtotal() * (1 - self.discount_percent / 100), 2)

class InvoiceExporter(ABC):
    @abstractmethod
    def export(self, order: Order) -> str:
        pass

class TextInvoiceExporter(InvoiceExporter):
    def export(self, order: Order) -> str:
        lines = ['=' * 40, f'ЧЕК #{order.order_id}', f'Клієнт: {order.customer}',
                 f'Час: {order.created_at}', '-' * 40]
        for i in order.items:
            lines.append(f"{i['name']} x{i['qty']} = {i['price'] * i['qty']:.2f} грн")
        lines.extend(['-' * 40, f'Сума: {order.get_subtotal():.2f} грн',
                      f'Знижка: {order.discount_percent}%',
                      f'ДО СПЛАТИ: {order.get_total():.2f} грн', '=' * 40])
        return '\n'.join(lines)

class JsonInvoiceExporter(InvoiceExporter):
    def export(self, order: Order) -> str:
        payload = {'document': 'INVOICE', 'invoice_number': order.order_id,
                   'client': order.customer, 'timestamp': order.created_at,
                   'lines': order.items, 'pricing': {'subtotal': order.get_subtotal(),
                   'discount_rate': order.discount_percent, 'final_amount': order.get_total()}}
        return json.dumps(payload, ensure_ascii=False, indent=2)

class HtmlInvoiceExporter(InvoiceExporter):
    def export(self, order: Order) -> str:
        rows = ''.join(f"<tr><td>{escape(i['name'])}</td><td>{i['qty']}</td><td>{i['price']*i['qty']:.2f} грн</td></tr>" for i in order.items)
        return (f"<div style='font-family:Arial;border:1px solid #333;padding:12px;width:340px'>"
                f"<h3>Рахунок #{order.order_id}</h3><p>Клієнт: {escape(order.customer)}</p>"
                f"<table border='1' width='100%' style='border-collapse:collapse'>"
                f"<tr><th>Товар</th><th>К-сть</th><th>Сума</th></tr>{rows}</table>"
                f"<p><b>До сплати: {order.get_total():.2f} грн</b></p></div>")

class MarkdownInvoiceExporter(InvoiceExporter):
    def export(self, order: Order) -> str:
        lines = [f'# Чек #{order.order_id}', f'**Клієнт:** {order.customer}',
                 f'**Дата:** {order.created_at}', '', '| Товар | К-сть | Сума |',
                 '| :--- | ---: | ---: |']
        for i in order.items:
            name = i['name'].replace('|', r'\|')
            lines.append(f"| {name} | {i['qty']} | {i['price']*i['qty']:.2f} грн |")
        lines.extend(['', f'**Знижка:** {order.discount_percent}%',
                      f'**Разом до сплати:** {order.get_total():.2f} грн'])
        return '\n'.join(lines)

class CsvInvoiceExporter(InvoiceExporter):
    def export(self, order: Order) -> str:
        output = io.StringIO(newline='')
        writer = csv.writer(output)
        writer.writerow(['Товар', 'Кількість', 'Ціна за одиницю', 'Сума'])
        for i in order.items:
            writer.writerow([i['name'], i['qty'], f"{i['price']:.2f}",
                             f"{i['price'] * i['qty']:.2f}"])
        writer.writerow(['Разом з урахуванням знижки', '', '', f'{order.get_total():.2f}'])
        return output.getvalue()

class InvoiceProcessingService(ABC):
    @abstractmethod
    def create_exporter(self) -> InvoiceExporter:
        """Фабричний метод: підкласи обирають конкретний експортер."""
        pass

    def process_and_print(self, order: Order) -> str:
        result = self.create_exporter().export(order)
        print(result)
        return result

class FastPosTerminalService(InvoiceProcessingService):
    def create_exporter(self) -> InvoiceExporter:
        return TextInvoiceExporter()

class ApiIntegrationService(InvoiceProcessingService):
    def create_exporter(self) -> InvoiceExporter:
        return JsonInvoiceExporter()

class EmailNotificationService(InvoiceProcessingService):
    def create_exporter(self) -> InvoiceExporter:
        return HtmlInvoiceExporter()

class MarkdownExportService(InvoiceProcessingService):
    def create_exporter(self) -> InvoiceExporter:
        return MarkdownInvoiceExporter()

class CsvExportService(InvoiceProcessingService):
    def create_exporter(self) -> InvoiceExporter:
        return CsvInvoiceExporter()

if __name__ == '__main__':
    order = Order(505, 'Міккі Маус', 15)
    order.add_item('Гітара', 4500, 1)
    order.add_item('Струни', 250, 2)
    for label, service in [('TXT', FastPosTerminalService()),
                           ('JSON', ApiIntegrationService()),
                           ('HTML', EmailNotificationService()),
                           ('MARKDOWN', MarkdownExportService()),
                           ('CSV', CsvExportService())]:
        print(f'\n--- {label} ---')
        service.process_and_print(order)
