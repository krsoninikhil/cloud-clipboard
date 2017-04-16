#SERVER_URI = 'http://localhost:8000/'
SERVER_URI = 'http://cloudcb.herokuapp.com/'

def show_error(req, error):
    print(
        "Errors: %s" % error,
        "Request: %s" % req.__dict__,
        "This seems unusual. Please file a bug report with above details",
        "at https://github.com/krsoninikhil/cloud-clipboard/issues"
    )

