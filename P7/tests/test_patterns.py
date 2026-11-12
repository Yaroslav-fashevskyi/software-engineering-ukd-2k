import csv
import io
import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src' / 'after'))
from factory_method import (Order, FastPosTerminalService, ApiIntegrationService,
                            EmailNotificationService, MarkdownExportService, CsvExportService)
from strategy import (OrderShippingContext, PickupStrategy, CourierStrategy,
                      ExpressDeliveryStrategy, PostMachineStrategy)
from adapter import (CheckoutService, InternalBankProcessor, GlobalPayAdapter,
                     GlobalPaySDK, CryptoPayAdapter, CryptoPayService)

class TestFactoryMethod(unittest.TestCase):
    def setUp(self):
        self.order = Order(1, 'Тест', 10)
        self.order.add_item('Гітара', 1000, 2)

    def test_formats(self):
        self.assertIn('1800.00', FastPosTerminalService().create_exporter().export(self.order))
        data = json.loads(ApiIntegrationService().create_exporter().export(self.order))
        self.assertEqual(data['pricing']['final_amount'], 1800)
        self.assertIn('<table', EmailNotificationService().create_exporter().export(self.order))
        self.assertIn('| Гітара |', MarkdownExportService().create_exporter().export(self.order))
        csv_rows = list(csv.reader(io.StringIO(CsvExportService().create_exporter().export(self.order))))
        self.assertEqual(csv_rows[-1][-1], '1800.00')

class TestStrategy(unittest.TestCase):
    def test_tariffs_and_switch(self):
        context = OrderShippingContext(PickupStrategy())
        self.assertEqual(context.calculate_delivery_cost(6, 15), 0)
        context.set_strategy(CourierStrategy())
        self.assertEqual(context.calculate_delivery_cost(6, 15), 160)
        context.set_strategy(ExpressDeliveryStrategy())
        self.assertEqual(context.calculate_delivery_cost(6, 15), 390)
        context.set_strategy(PostMachineStrategy())
        self.assertEqual(context.calculate_delivery_cost(10, 15), 50)
        with self.assertRaises(ValueError):
            context.calculate_delivery_cost(10.1, 15)

class TestAdapter(unittest.TestCase):
    def test_gateways(self):
        self.assertTrue(CheckoutService(InternalBankProcessor()).checkout('demo', 10))
        self.assertTrue(CheckoutService(GlobalPayAdapter(GlobalPaySDK())).checkout('demo@example.com', 10.01))
        self.assertTrue(CheckoutService(CryptoPayAdapter(CryptoPayService())).checkout('wallet', 10))
        with self.assertRaises(ValueError):
            CheckoutService(InternalBankProcessor()).checkout('demo', 0)

if __name__ == '__main__':
    unittest.main()
