# Free Fire NickName Checker API

A Flask-based API for checking Free Fire player details, including nickname, region, ban status, and ban period, with multi-region support (PK, BD, IND, NA, SG).

## Installation

Clone the repository and install dependencies:

```
git clone TSun-FreeFire/TSun-FF-NameCheck-Api.git
cd TSun-FF-NameCheck-Api
pip install flask requests
```

## Usage

Run the app locally:

```
python app.py
```

Access the endpoint: `http://yourlink/check?uid={uid}&region={pk}`

Example response:
```
{
  "success": true,
  "nickname": "PlayerName",
  "region": "PK",
  "is_banned": false,
  "ban_period": 0,
  "message": "Player found and data retrieved successfully."
}```
```

## Technologies

- Python 3.x
- Flask for the web framework[5].
- Requests for API calls.

## Features

- Multi-region support for Free Fire servers.
- Ban status checking via Garena API.
- Error handling for invalid UIDs or regions.

## Contributing

Fork the repo, create a branch, and submit a pull request[2].

## License

MIT License[2].
