"""
Cấu hình cho AdsPower Automation
"""
import os
from typing import Optional
try:
    from pydantic_settings import BaseSettings
except ImportError:
    from pydantic import BaseSettings


class AdsPowerConfig(BaseSettings):
    """Cấu hình cho AdsPower API"""
    
    # AdsPower Local API settings
    adspower_api_url: str = "http://127.0.0.1:50325"
    adspower_api_key: Optional[str] = None
    
    # Browser settings
    browser_timeout: int = 30000  # 30 seconds
    page_timeout: int = 30000     # 30 seconds
    navigation_timeout: int = 60000  # 60 seconds
    
    # Logging settings
    log_level: str = "INFO"
    log_file: str = "adspower_automation.log"
    
    # Default browser settings
    headless: bool = False
    viewport_width: int = 1920
    viewport_height: int = 1080
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# Global config instance
config = AdsPowerConfig()
