from decimal import Decimal
from okx.Trade import TradeAPI
from okx.Account import AccountAPI

class OkxTrade:
    def __init__(self):
        self.long_input_pct = Decimal(0)
        self.short_input_pct = Decimal(0)
        self.trade_api: TradeAPI = None
        self.account_api: AccountAPI = None
        self.config_id: int = -1