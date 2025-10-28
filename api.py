from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

REGION_CONFIG = {
    'IN': {'region_code': 'IN', 'language': 'en', 'source': 'mb'},
    'BD': {'region_code': 'BD', 'language': 'en', 'source': 'mb'},
    'PK': {'region_code': 'PK', 'language': 'en', 'source': 'mb'},
    'NA': {'region_code': 'NA', 'language': 'en', 'source': 'mb'},
    'SG': {'region_code': 'SG', 'language': 'en', 'source': 'mb'},
}

@app.route('/check', methods=['GET'])
def check_player():
    target_id = request.args.get('uid')
    region = request.args.get('region', 'PK').upper()

    if not target_id:
        return jsonify({"success": False, "message": "Missing 'uid' parameter"}), 400
    
    if region not in REGION_CONFIG:
        return jsonify({"success": False, "message": f"Unsupported region: {region}"}), 400

    config = REGION_CONFIG[region]

    cookies = {
        '_ga': 'GA1.1.139075504.1761660128',  # These may need updating
        '_fbp': 'fb.1.1674510785537.363500115',
        '_ga_7JZFJ14B0B': 'GS1.1.1674510784.1.1.1674510789.0.0.0',
        'source': config['source'],
        'region': config['region_code'],
        'language': config['language'],
        '_ga_TVZ1LG7BEB': 'GS1.1.1674930050.3.1.1674930171.0.0.0',
        'datadome': 'mufxkZpuhwX4xu31fozH8Jc8fee5HKVgM8w4lLblhgBy21FeGrYbmMiY_hQ0ew7vSg2RogHh~lksYxANoiEVqvtEVAg0csrmIY1w01gbm8EaGAVxnsiv0rxA3zTWPYbA',  
        'session_key': '6nau7ozh8mqztuy2pd7xnptah15lb0lj',  
    }

    headers = {
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive',
        'Origin': 'https://shop2game.com',
        'Referer': 'https://shop2game.com/app/100067/idlogin',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 11; Redmi Note 8)',
        'accept': 'application/json',
        'content-type': 'application/json',
        'sec-ch-ua': '"Chromium";v="107", "Not=A?Brand";v="24"',
        'sec-ch-ua-mobile': '?1',
        'sec-ch-ua-platform': '"Android"',
        'x-datadome-clientid': cookies['datadome'],  # Use the datadome from cookies
    }

    json_data = {
        'app_id': 100067,
        'login_id': target_id,
        'app_server_id': 0,
    }

    try:
        res = requests.post('https://shop2game.com/api/auth/player_id_login',
                            cookies=cookies, headers=headers, json=json_data)
        res.raise_for_status()

        player_data = res.json()
        if not player_data.get('nickname'):
            return jsonify({"success": False, "message": "ID not found"}), 404

        return jsonify({
            "uid": target_id,
            "nickname": player_data.get('nickname', 'N/A'),
            "region": player_data.get('region', region)
        })

    except requests.exceptions.RequestException as e:
        return jsonify({"success": False, "message": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
