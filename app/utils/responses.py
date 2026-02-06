from flask import jsonify

def api_response(
    success: bool,
    data=None, 
    error=None, 
    total_items=None, 
    pagination=None,
    status_code=200) -> tuple[jsonify, int]:
    
    payload = {"success": success}
    
    if total_items is not None:
        payload["total_items"] = total_items
    
    if pagination is not None:
        payload["pagination"] = pagination
        
    if data is not None:
        payload["data"] = data
        
    if error is not None:
        payload["error"] = error
    
    return jsonify(payload), status_code
        