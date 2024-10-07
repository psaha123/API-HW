from flask import Flask, jsonify, request
from inspector import Inspector

app = Flask(__name__)

@app.route("/search", methods=["GET"])
def search():
    # Get query parameters
    restaurant_name = request.args.get('restaurant_name')
    cuisine = request.args.get('cuisine')
    zipcode = request.args.get('zipcode')
    limit = request.args.get('limit', default=10, type=int)

    # Retrieve inspections
    try:
        inspections = list(Inspector.get_inspections())
    except Exception as e:
        return jsonify({"error": "Failed to retrieve inspections", "details": str(e)}), 500

    # Filter results based on query parameters
    filtered_results = inspections

    if restaurant_name:
        filtered_results = [ins for ins in filtered_results if restaurant_name.lower() in ins.restaurant_name.lower()]
    
    if cuisine:
        filtered_results = [ins for ins in filtered_results if cuisine.lower() in ins.cuisine.lower()]

    if zipcode:
        filtered_results = [ins for ins in filtered_results if ins.zipcode == zipcode]  # Exact match for zipcode

    # Sort by restaurant_id
    filtered_results.sort(key=lambda x: x.restaurant_id)

    # Limit the results
    limited_results = filtered_results[:limit]

    # Prepare response data
    if not limited_results:
        return jsonify({"data": []}), 404  # No results found

    response_data = {
        "data": [ins.to_json() for ins in limited_results]
    }
    
    return jsonify(response_data)

if __name__ == "__main__":
    app.run(host="localhost", debug=True, port=8080)
