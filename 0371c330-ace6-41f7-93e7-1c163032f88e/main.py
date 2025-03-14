from surmount.base_class import Strategy, TargetAllocation
from surmount.data import OHLCV
from surmount.logging import log

class TradingStrategy(Strategy):
    # Assuming a simplified model where the purchase price is reset at each instance creation
    # For a real scenario, this information should be dynamically managed and persistent
    purchase_price = None  # Placeholder for purchase price tracking
    
    @property
    def assets(self):
        return ["SPY"]
    
    @property
    def interval(self):
        return "1day"  # Adjust based on the desired trading frequency
    
    def run(self, data):
        # Extracting the latest close price
        ohlcv_data = data["ohlcv"]
        latest_close_price = ohlcv_data[-1]["SPY"]["close"]
        
        # Initial allocation with no action
        allocation = {"SPY": 0}
        
        if self.purchase_price is None:
            # If there's no purchase price recorded, consider buying
            allocation["SPY"] = 1  # 100% of the capital allocated to buying SPY
            self.purchase_price = latest_close_price  # Update the purchase price
            log("Initiating a position in SPY")
        else:
            # Calculate price changes
            up_move_threshold = self.purchase_price * 1.01  # 1% up from the purchase price
            down_move_threshold = self.purchase_price * 0.99  # 1% down from the purchase price
            
            if latest_close_price >= up_move_threshold:
                # Sell if the price is 1% up from the purchase price
                allocation["SPY"] = 0  # Selling off SPY
                self.purchase_price = None  # Reset the purchase price tracking
                log("Selling SPY, as the price moved up by 1% or more")
            elif latest_close_price <= down_move_threshold:
                # Buy if the price is 1% down from the last purchase price
                allocation["SPY"] = 1  # 100% of the capital allocated to buying SPY
                self.purchase_price = latest_close_price  # Update the purchase price
                log("Buying additional SPY, as the price moved down by 1% or more")
            else:
                # No trading action if price changes are within the threshold
                log("No trading action required")
        
        return TargetAllocation(allocation)