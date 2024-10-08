from flask import Flask, jsonify, request, abort
from inspector import Inspector

app = Flask(__name__)
@app.route("/search", methods=["GET"])

def search():
    if not request.args:
        abort(501)
        
    restaurant_name = request.args.get('restaurant_name')
    zipcode = request.args.get('zipcode')
    cuisine = request.args.get('cuisine')
    limit = request.args.get('limit', default=10, type=int)

    try:
        inspections = list(Inspector.get_inspections())
    except Exception as e:
        return jsonify({"error": "Failed to retrieve inspections", "details": str(e)}), 500

    filtered_results = inspections
    if restaurant_name:
        filtered_results = [ins for ins in filtered_results if restaurant_name.lower() in ins.restaurant_name.lower()]

    if zipcode:
        filtered_results = [ins for ins in filtered_results if ins.zipcode == zipcode]
    
    if cuisine:
        filtered_results = [ins for ins in filtered_results if cuisine.lower() in ins.cuisine.lower()]

    filtered_results.sort(key=lambda x: x.restaurant_id)
    limited_results = filtered_results[:limit]

    if not limited_results:
        return jsonify({"data": []}), 404

    return jsonify(format_response(limited_results))

if __name__ == "__main__":
    app.run(host="localhost", debug=True, port=8080)
