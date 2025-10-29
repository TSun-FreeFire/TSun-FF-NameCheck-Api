from flask import Flask, request, Response
import requests
import json
import datetime

app = Flask(__name__)

def get_combined_data(uid, ban_key="saeed"):
    namecheck_url = f"https://ffinfo.tsunstudio.pw/get?uid={uid}"
    bancheck_url = f"https://bancheckbackend.tsunstudio.pw/bancheck?key={ban_key}&uid={uid}"

    namecheck_response = requests.get(namecheck_url)
    bancheck_response = requests.get(bancheck_url)

    print(f"Namecheck Raw Response: {namecheck_response.text}")
    print(f"Bancheck Raw Response: {bancheck_response.text}")

    namecheck_data = namecheck_response.json()
    bancheck_data = bancheck_response.json()

    combined_data = {
        "nickname": namecheck_data.get("AccountInfo", {}).get("AccountName"),
        "uid": namecheck_data.get("SocialInfo", {}).get("accountId"),
        "AccountLevel": namecheck_data.get("AccountInfo", {}).get("AccountLevel"),
        "region": namecheck_data.get("AccountInfo", {}).get("AccountRegion"),
        "AccountLastLogin": namecheck_data.get("AccountInfo", {}).get("AccountLastLogin"),
        "status": bancheck_data.get("status"),
        "is_banned": bancheck_data.get("is_banned"),
        "Last_Login": "", # Placeholder, will be calculated later
        "credits": bancheck_data.get("credits")
    }
    
    if combined_data["AccountLastLogin"]:
        timestamp = int(combined_data["AccountLastLogin"])
        last_login_date = datetime.datetime.fromtimestamp(timestamp)
        combined_data["AccountLastLogin"] = last_login_date.strftime('%Y-%m-%d')

        today = datetime.datetime.now()
        diff = today - last_login_date

        years = diff.days // 365
        remaining_days = diff.days % 365
        months = remaining_days // 30  # Approximate months
        days = remaining_days % 30

        combined_data["Last_Login"] = f"{years} Year {months} Months And {days} Days Ago"

    return combined_data

@app.route('/bancheck', methods=['GET'])
def bancheck():
    uid = request.args.get('uid')
    if not uid:
        return Response(json.dumps({"error": "UID is required"}, indent=2, sort_keys=False), mimetype='application/json'), 400
    
    # Default values for ban_key, as it is not part of the /bancheck endpoint
    ban_key = "saeed"

    result = get_combined_data(uid, ban_key)
    return Response(json.dumps(result, indent=2, sort_keys=False), mimetype='application/json')

if __name__ == '__main__':
    app.run(debug=True)
