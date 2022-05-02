from app import app

# NOT FOUND ERROR
@app.errorhandler(404)
def not_found_error(error):
    return "That resource cannot be found on our servers"


# INTERNAL SERVER ERROR
@app.errorhandler(500)
def intrenal_server_error(error):
    return "There was an error with the server. Please contact the system administrator for assistance" 