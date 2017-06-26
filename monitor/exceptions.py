
class InspectorException(Exception):
    def __init__(self, message=None):
        super(InspectorException, self).__init__(message)

class InstanceNotFoundException(Exception):
    def __init__(self, message=None):
        super(InstanceNotFoundException, self).__init__(message)

class HttpRequestException(Exception):
    def __init__(self, message=None):
        super(HttpRequestException, self).__init__(message)

