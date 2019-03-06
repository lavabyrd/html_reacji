from flask import Flask, request
import pprint
from slackclient import SlackClient
import os
from htmlslacker import HTMLSlacker
from html import unescape

# This `app` represents your existing Flask app
app = Flask(__name__)

token = os.environ.get("TOKEN")
otoken = os.environ.get("OTOKEN")

sc = SlackClient(otoken)


# An example of one of your Flask app's routes
@app.route("/slack/events", methods=["POST"])
def events():
    """[Events endpoint]
	
	Returns:
	[JSON] -- [see below]
	{'api_app_id': 'AFASMUM29',
	'authed_users': ['U6MSBGWKA'],
	'event': {'event_ts': '1551864394.000800',
		'item':     {'channel': 'C6MSBGZT2',
				'ts': '1551827851.000400',
				'type': 'message'},
		'item_user': 'U6MSBGWKA',
		'reaction': 'grin',
		'type': 'reaction_added',
		'user': 'U6MSBGWKA'},
	'event_id': 'EvGPMHQQCQ',
	{'api_app_id': 'AGQ0RBQV9',
	'event_time': 1551864394,
	'team_id': 'T6MSBGW8Y',
	'token': 'wDRs2ebJd2hIyNit264WPf6v',
	'authed_users': ['UGPBUJ8F2'],
	'type': 'event_callback'}
	127.0.0.1 - - [06/Mar/2019 09:26:35] "POST /slack/events HTTP/1.1" 200 -
	'event': {'event_ts': '1551864394.000800',
		'item': {'channel': 'C6MSBGZT2',
				'ts': '1551827851.000400',
				'type': 'message'},
		'item_user': 'U6MSBGWKA',
		'reaction': 'grin',
		'type': 'reaction_added',
		'user': 'U6MSBGWKA'},
	'event_id': 'EvGPMHQQL8',
	'event_time': 1551864394,
	'team_id': 'T6MSBGW8Y',
	'token': 'KUNjubfs7VQJVwkOpPlrBcRF',
	'type': 'event_callback'}
	"""

    event = request.get_json()
    # if event['challenge'] == True:
    # 	return event['challenge']
    if event["event"]["reaction"] == "keyboard":
        text = sc.api_call(
            "conversations.history",
            channel=event["event"]["item"]["channel"],
            latest=event["event"]["item"]["ts"],
            limit=1,
            inclusive="true",
        )
        out1 = unescape(text["messages"][0]["text"])
        sc.api_call(
            "chat.update",
            channel=event["event"]["item"]["channel"],
            text=HTMLSlacker(out1).get_output(),
            ts=event["event"]["item"]["ts"],
            as_user="true",
        )
    else:
        print("nope")

    return ""
