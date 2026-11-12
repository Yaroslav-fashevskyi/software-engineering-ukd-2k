"""До рефакторингу: перевірки типів платіжних шлюзів у CheckoutService."""
class InternalBankGateway:
    def process_payment(self, account_number: str, amount: float) -> bool:
        print(f'[InternalBank] Оплата {amount:.2f} грн: {account_number}')
        return True

class GlobalPaySDK:
    def charge_customer(self, user_email: str, cents_amount: int, currency: str) -> dict:
        print(f'[GlobalPay] {user_email}: {cents_amount} коп., {currency}')
        return {'status': 'SUCCESS', 'tx_id': 'GP-DEMO-001'}

class CheckoutService:
    def __init__(self, payment_gateway):
        self.payment_gateway = payment_gateway

    def checkout(self, customer_account: str, total_price: float) -> bool:
        if isinstance(self.payment_gateway, InternalBankGateway):
            paid = self.payment_gateway.process_payment(customer_account, total_price)
        elif isinstance(self.payment_gateway, GlobalPaySDK):
            result = self.payment_gateway.charge_customer(customer_account, round(total_price * 100), 'UAH')
            paid = result.get('status') == 'SUCCESS'
        else:
            raise TypeError('Невідомий платіжний сервіс')
        print('Оплату проведено' if paid else 'Помилка оплати')
        return paid

if __name__ == '__main__':
    CheckoutService(InternalBankGateway()).checkout('UA-DEMO-ACCOUNT', 3500)
    CheckoutService(GlobalPaySDK()).checkout('customer@example.com', 3500)
