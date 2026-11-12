"""Adapter: уніфікований інтерфейс банку, GlobalPay та навчального CryptoPay."""
from abc import ABC, abstractmethod
from decimal import Decimal, ROUND_HALF_UP

class PaymentProcessor(ABC):
    @abstractmethod
    def pay(self, account_identifier: str, amount: float) -> bool:
        pass

class InternalBankProcessor(PaymentProcessor):
    def pay(self, account_identifier: str, amount: float) -> bool:
        print(f'[InternalBank] Списання {amount:.2f} грн: {account_identifier}')
        return True

class GlobalPaySDK:
    """Навчальна імітація зовнішнього SDK; жодних реальних списань."""
    def charge_customer(self, user_email: str, cents_amount: int, currency: str) -> dict:
        print(f'[GlobalPay SDK] {user_email}: {cents_amount} коп., {currency}')
        return {'status': 'SUCCESS', 'tx_id': 'GP-DEMO-001'}

class GlobalPayAdapter(PaymentProcessor):
    def __init__(self, sdk: GlobalPaySDK):
        self.sdk = sdk

    def pay(self, account_identifier: str, amount: float) -> bool:
        kopecks = int((Decimal(str(amount)) * 100).quantize(Decimal('1'), rounding=ROUND_HALF_UP))
        result = self.sdk.charge_customer(account_identifier, kopecks, 'UAH')
        return result.get('status') == 'SUCCESS'

class CryptoPayService:
    """Навчальна імітація криптопровайдера; 'OK' означає відповідь демонстраційного SDK."""
    def send_crypto_invoice(self, wallet_address: str, uah_sum: float) -> str:
        print(f'[CryptoPay DEMO] Створено тестовий інвойс {wallet_address}: {uah_sum:.2f} грн')
        return 'OK'

class CryptoPayAdapter(PaymentProcessor):
    def __init__(self, crypto_service: CryptoPayService):
        self.crypto_service = crypto_service

    def pay(self, account_identifier: str, amount: float) -> bool:
        response = self.crypto_service.send_crypto_invoice(account_identifier, amount)
        return response == 'OK'  # За умовами задачі, не підтвердження блокчейн-транзакції.

class CheckoutService:
    def __init__(self, payment_processor: PaymentProcessor):
        self.payment_processor = payment_processor

    def checkout(self, customer_info: str, total_price: float) -> bool:
        if total_price <= 0:
            raise ValueError('Сума оплати має бути додатною')
        is_paid = self.payment_processor.pay(customer_info, total_price)
        print('Оплата пройшла (демо)' if is_paid else 'Помилка оплати')
        return is_paid

if __name__ == '__main__':
    print('--- ВНУТРІШНІЙ БАНК ---')
    CheckoutService(InternalBankProcessor()).checkout('UA-DEMO-ACCOUNT', 3500)
    print('\n--- GLOBALPAY ---')
    CheckoutService(GlobalPayAdapter(GlobalPaySDK())).checkout('customer@example.com', 3500)
    print('\n--- CRYPTOPAY ---')
    CheckoutService(CryptoPayAdapter(CryptoPayService())).checkout('demo-wallet', 3500)
