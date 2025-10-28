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
        '_ga': 'GA1.1.154369471.1761663434',  # These may need updating
        '_fbp': 'fb.1.1674510785537.363500115',
        '_ga_7JZFJ14B0B': 'GS1.1.1674510784.1.1.1674510789.0.0.0',
        'source': config['source'],
        'region': config['region_code'],
        'language': config['language'],
        '_ga_TVZ1LG7BEB': 'GS1.1.1674930050.3.1.1674930171.0.0.0',
        'datadome': '2YalnPtsSiqxvGI6QeZ4T30Y4Br8layFS5fbc9TQRAdTCgTxYljaKoFbJxAa4qwH~sUO3cZdnIrVSPUkoMUP9nCDfDBnPdow5b8EMuIcnwyqnHvIpKIIodtv3B2EbpLI',  
        'session_key': '1b6mrforh4mfmveuzjnw6lbetntb0n3s',  
    }

    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        'Host': 'shop2game.com',
        'Origin': 'https://shop2game.com',
        'Referer': 'https://shop2game.com/app/100067/idlogin',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Chromium";v="107", "Not=A?Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
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
