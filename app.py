import datetime
from time import localtime

local_time = localtime()
print(local_time.strftime('%Y-%m-%d %H:%M:%S'))