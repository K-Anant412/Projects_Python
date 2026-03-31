def success_response(message, data=None, status_code=200):
    return {
            "Status":"Success",
            "Message":message,
            "Data":data
            }, status_code
    
    
def error_response(message, status_code=400, error_code=None):
    return {
            "Status":"Error",
            "Message":message,
            "Error code": error_code if error_code else "AIP error" 
            }, status_code
    
