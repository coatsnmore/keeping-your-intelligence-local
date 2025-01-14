import datetime

def greet_local_time():
    current_datetime = datetime.datetime.now()
    print("Local Time:", current_datetime.strftime("%Y-%m-%d %H:%M:%S"))

greet_local_time()