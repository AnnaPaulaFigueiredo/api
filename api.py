from flask import Flask, jsonify, request
from google_play_scraper import reviews_all, Sort
from datetime import datetime
N_REVIEWS = 20000

# FUNCITONS
def get_reviews(app_id, lang, country, sort, n_reviews):

    all_reviews = []  
    
    while len(all_reviews) < n_reviews:
        
        result = reviews_all(
            app_id,
            sleep_milliseconds=0,
            lang=lang,
            country=country,
            sort=sort,
        )
        
        if not result:
            break
        
        all_reviews.extend(result)
 
        if len(all_reviews) >= n_reviews:
            break

    return all_reviews

def filter_by_year(reviews, year):
    return [review for review in reviews if review['at'].year == year]

def calculate_mean_score_by_month(data):
    mean_score_by_year_month = {}

    for item in data:
        year_month = item['at'].strftime("%Y-%m")
        if year_month not in mean_score_by_year_month:
            mean_score_by_year_month[year_month] = {'total': 0, 'count': 0}

        mean_score_by_year_month[year_month]['total'] += item['score']
        mean_score_by_year_month[year_month]['count'] += 1

    sorted_result = {}
    for year_month, info in sorted(mean_score_by_year_month.items(), key=lambda x: x[0], reverse=True):
        mean = round(info['total'] / info['count'], 2)
        sorted_result[year_month] = mean

    return sorted_result

# ROUTES
app = Flask(__name__)
@app.route('/api-playstore')
def homepage():
    return " A API está no ar - 200."

# Avaliações sem os comentários
@app.route('/api-playstore-score', methods=['GET'])
def get_score():
    
    link = request.args.get('link')
    link = link.split("=")[-1]

    year = request.args.get('ano', None)
   
    if not link:
        return jsonify({'error': 'Parâmetro "link" ausente na URL'}), 400

    app_reviews = get_reviews(app_id=link, lang='', country='', sort=Sort.NEWEST , n_reviews=N_REVIEWS)

    if year:
        app_reviews = filter_by_year(app_reviews, int(year))
    
    scores_json = [{"userName":item["userName"], "userImage":item["userImage"],
                    "score":item["score"], "at":item["at"]       
                    } for item in app_reviews]
    
    return jsonify(scores_json)

# Score mensal de avaliacoes
@app.route('/api-playstore-monthly-score', methods=['GET'])
def get_monthly_score():

    link = request.args.get('link')
    link = link.split("=")[-1]

    year = request.args.get('ano', None)
   
    if not link:
        return jsonify({'error': 'Parâmetro "link" ausente na URL'}), 400

    app_reviews = get_reviews(app_id=link, lang='', country='', sort=Sort.NEWEST , n_reviews=N_REVIEWS)

    if year:
        app_reviews = filter_by_year(app_reviews, int(year))

    scores_json = [{"score":item["score"], "at":item["at"]} for item in app_reviews]
    
    monthly_scores = calculate_mean_score_by_month(scores_json)

    return jsonify(monthly_scores)

# Reviews com o usuário e foto
@app.route('/api-playstore-reviews', methods=['GET'])
def get_data():
    link = request.args.get('link')
    link = link.split("=")[-1]

    year = request.args.get('ano', None)
   
    if not link:
        return jsonify({'error': 'Parâmetro "link" ausente na URL'}), 400

    app_reviews = get_reviews(app_id=link, lang='', country='', sort=Sort.NEWEST , n_reviews=N_REVIEWS)

    if year:
        app_reviews = filter_by_year(app_reviews, int(year))
   
    reviews_json = [{"userName":item["userName"], "userImage":item["userImage"], "content": item["content"], 
                     "score":item["score"], "thumbsUpCount":item["thumbsUpCount"],
                     "replyContent": item["replyContent"], "repliedAt": item["repliedAt"],"appVersion":item["appVersion"],
                     "at":item["at"]       
                    } for item in app_reviews]
    
    return jsonify(reviews_json)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

