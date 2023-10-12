from flask import Flask, request, jsonify
import requests

app = Flask(__name__)
BASE_URL = "https://app.ylytic.com/ylytic/test"

@app.route('/search', methods=['GET'])
def search_comments():
  search_params = {
    'search_author': request.args.get('search_author'),
    'at_from': request.args.get('at_from'),
    'at_to': request.args.get('at_to'),
    'like_from': request.args.get('like_from'),
    'like_to': request.args.get('like_to'),
    'reply_from': request.args.get('reply_from'),
    'reply_to': request.args.get('reply_to'),
    'search_text': request.args.get('search_text')
  }

  
  if search_params['search_author'] and not any(other_param for other_param in search_params.values() if other_param is not None):
    return jsonify(fetch_comments_by_author(search_params['search_author']))

  
  url = f"{BASE_URL}?{'&'.join([f'{key}={value}' for key, value in search_params.items() if value])}"

  try:
    response = requests.get(url)
    if response.status_code == 200:
      comments = response.json()
      return jsonify(comments)
    else:
      return jsonify({"error": "Failed to fetch comments"}), 500
  except requests.exceptions.RequestException as e:
    return jsonify({"error": f"Request failed: {str(e)}"}), 500

def fetch_comments_by_author(search_author):
    url = f"{BASE_URL}?search_author={search_author}"

    response = requests.get(url)
    if response.status_code == 200:
        comments = response.json()
        # Filter comments by the specified author
        filtered_comments = [comment for comment in comments if search_author.lower() in comment['author'].lower()]
        return filtered_comments
    else:
        raise Exception(f"Failed to fetch comments for author {search_author}")


if __name__ == '__main__':
    app.run(debug=True)

