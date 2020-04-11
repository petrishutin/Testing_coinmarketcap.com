API_KEY: str = '829cd3be-5026-4e47-8250-5a835eb19744'  # get the kay at https://coinmarketcap.com/api/
LOG_TO_DB: bool = True  # Set True/1 to unable logging to database
USE_MOCK: bool = False  # Set True/1 to use mocks instead of sending request
NUMBER_OF_TREADS: int = 8
UTC_OFFSET: int = 3  # Set UTC offset in hours for your current location

# test limits
MAX_PERCENTILE: int = 450  # Upper limit of 80% latency in msec
MAX_TIME_OF_RESPONSE: int = 500  # Upper limit for time of response in msec
MIN_RPS: int = 5  # Lower limit of rps (responses per second)
MAX_SIZE_OF_RESPONSE: int = 10240  # Upper limit for size of response in bytes
