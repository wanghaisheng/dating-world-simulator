from enum import Enum
from src.i18n import t

class Month(Enum):
    JANUARY = 1
    FEBRUARY = 2
    MARCH = 3
    APRIL = 4
    MAY = 5
    JUNE = 6
    JULY = 7
    AUGUST = 8
    SEPTEMBER = 9
    OCTOBER = 10
    NOVEMBER = 11
    DECEMBER = 12

    def __str__(self) -> str:
        return str(self.value) 

    def __repr__(self) -> str:
        return str(self.value) 

class Year(int):
    def __add__(self, other: int) -> 'Year':
        return Year(int(self) + other)

class MonthStamp(int):
    """
    0年1月 = 0
    之后依次递增
    """
    def get_time_config(self):
        # Avoid circular import by importing locally
        from src.utils.config import CONFIG, GameMode
        try:
            # Check if CONFIG is loaded and has game.mode
            if hasattr(CONFIG, "game") and hasattr(CONFIG.game, "mode") and CONFIG.game.mode == GameMode.MODERN_ROMANCE.value:
                return {
                    "ticks_per_year": 8640, # 12 * 30 * 24
                    "ticks_per_month": 720, # 30 * 24
                    "ticks_per_day": 24,
                    "mode": "modern_romance"
                }
        except Exception:
            pass
        
        # Default / Cultivation mode
        return {
            "ticks_per_year": 12,
            "ticks_per_month": 1,
            "ticks_per_day": 0,
            "mode": "cultivation"
        }

    def get_month(self) -> Month:
        conf = self.get_time_config()
        ticks_per_year = conf["ticks_per_year"]
        ticks_per_month = conf["ticks_per_month"]
        
        # Calculate month based on config
        rem_year = self % ticks_per_year
        month_idx = rem_year // ticks_per_month
        month_value = month_idx + 1
        return Month(month_value if month_value <= 12 else 12)

    def get_year(self) -> Year:
        conf = self.get_time_config()
        return Year(self // conf["ticks_per_year"])

    def __add__(self, other: int) -> 'MonthStamp':
        return MonthStamp(int(self) + other)

def create_month_stamp(year: Year, month: Month) -> MonthStamp:
    """从年和月创建MonthStamp"""
    # Use a dummy instance to access get_time_config or duplicate logic
    # Duplicate logic to avoid instantiating MonthStamp with invalid value
    from src.utils.config import CONFIG, GameMode
    ticks_per_year = 12
    ticks_per_month = 1
    
    try:
        if hasattr(CONFIG, "game") and hasattr(CONFIG.game, "mode") and CONFIG.game.mode == GameMode.MODERN_ROMANCE.value:
            ticks_per_year = 8640
            ticks_per_month = 720
    except Exception:
        pass
        
    return MonthStamp(int(year) * ticks_per_year + (month.value - 1) * ticks_per_month)

def get_date_str(stamp: int) -> str:
    """将 MonthStamp (int) 转换为 'X年Y月' 格式"""
    ms = MonthStamp(stamp)
    conf = ms.get_time_config()
    
    if conf["mode"] == "modern_romance":
        # Format: Y年M月D日 H时
        year = ms.get_year()
        month = ms.get_month().value
        
        ticks_per_month = conf["ticks_per_month"]
        ticks_per_day = conf["ticks_per_day"]
        
        rem_month = stamp % ticks_per_month
        day = (rem_month // ticks_per_day) + 1
        hour = rem_month % ticks_per_day
        
        return f"{year}年{month}月{day}日 {hour:02d}:00"
    
    return t("date_format_year_month", year=ms.get_year(), month=ms.get_month().value)
