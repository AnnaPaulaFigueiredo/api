from flask import Flask, jsonify, request
from google_play_scraper import reviews_all, Sort

app = Flask(__name__)

@app.route('/api-playstore')
def homepage():
    return "A api está no ar."

@app.route('/api-playstore-reviews')
def get_data():

    link = request.args.get('link')
    link = link.split("=")[-1]
    
    if not link:
        return jsonify({'error': 'Parâmetro "link" ausente na URL'}), 400
    
    app_reviews = reviews_all(link, lang='pt', country='br', sort=Sort.NEWEST)
    reviews_json = [{"content": item["content"], "replyContent": item["replyContent"]} for item in app_reviews]
 
    return jsonify(reviews_json)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
