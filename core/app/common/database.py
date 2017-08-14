import motor.motor_tornado


def init_motor_client():
    """
    Initializes an asynchronous Motor client.
    
    It is recommended to use this function only once,
    thus reusing the same client for every request.
    :return: Motor client
    """
    conn = motor.motor_tornado.MotorClient('mongo', 27017)

    return conn.newsp
