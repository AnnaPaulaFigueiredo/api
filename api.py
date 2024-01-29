from flask import Flask, jsonify, request
from google_play_scraper import reviews_all, Sort

# FUNCITONS
def filter_by_year(json_list, years):
    filtered_list = []
    for item in json_list:
        at_year = item.get("at").year
        if at_year in years:
            filtered_list.append(item)
    return filtered_list

# ROUTES
app = Flask(__name__)
@app.route('/api-playstore')
def homepage():
    return "A api está no ar."

@app.route('/api-playstore-reviews', methods=['GET'])
def get_data():
    
    link = request.args.get('link')
    link = link.split("=")[-1]
   
    if not link:
        return jsonify({'error': 'Parâmetro "link" ausente na URL'}), 400
    
    app_reviews = reviews_all(link, lang='pt', country='br', sort=Sort.NEWEST)
    app_reviews = filter_by_year(app_reviews, [2024, 2023] )
    reviews_json = [{"content": item["content"], "replyContent": item["replyContent"], "year":item["at"].year} for item in app_reviews]
 
    return jsonify(reviews_json)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
