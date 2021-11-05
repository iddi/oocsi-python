from oocsi import OOCSI

# use this function to change how the log output is printed
# you can also switch logging off by providing a function that does not do anything
def logFunction(msg):
    print('custom log: ' + msg)

# initialize OOCSI connection with a custom logger
oocsi = OOCSI('python_custom_logger', 'localhost', logger=logFunction)
    
