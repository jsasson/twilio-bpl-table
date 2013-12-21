from flask import Flask, request, redirect
import twilio.twiml
import httplib
import json
# from pudb import set_trace; set_trace()
 
app = Flask(__name__) 

teamNames = {
    "liverpool":"Liverpool",
    "mancity":"Manchester City",
    "manchestercity":"Manchester City",
    "arsenal":"Arsenal",
    "chelsea":"Chelsea",
    "everton":"Everton",
    "newcastle":"Newcastle United",
    "newcastleunited":"Newcastle United",
    "manutd":"Manchester United",
    "manchesterunited":"Manchester United",
    "tottenham":"Tottenham Hotspur",
    "tottenhamhotspur":"Tottenham Hotspur",
    "southampton":"Southampton",
    "stoke":"Stoke City",
    "stokecity":"Stoke City",
    "swansea":"Swansea City",
    "swanseacity":"Swansea City",
    "hull":"Hull City",
    "hullcity":"Hull City",
    "astonvilla":"Aston Villa",
    "norwich":"Norwich City",
    "norwichcity":"Norwich City",
    "cardiff":"Cardiff City",
    "cardiffcity":"Cardiff City",
    "westbrom":"West Bromwich Albion",
    "westbromwichalbion":"West Bromwich Albion",
    "westham":"West Ham United",
    "westhamunited":"West Ham United",
    "crystalpalace":"Crystal Palace",
    "fulham":"Fulham",
    "sunderland":"Sunderland"
}

@app.route("/", methods=['GET', 'POST'])
def checkTable():
         
    # Parse the text message and normalize the string to check against our dictionary
    team = request.values.get('Body', None)
    # team = "Arsenal"
    teamCheck = "".join(team.split()).lower()

    if teamCheck in teamNames:
        
        # Query API for place in table        
        tableAPIConnection = httplib.HTTPSConnection('api.statsfc.com')
        tableAPIConnection.connect()
        tableAPIConnection.request('GET',
            '/table.json?key=yp1ASodhq3Hl52vkRKZClwNHyHIADzhR0i9ywCoX&competition=premier-league')
        response = tableAPIConnection.getresponse()
        
        if response.status == httplib.OK:
            table = json.load(response)

            tablePlace = (item for item in table if (item['team'] == teamNames[teamCheck])).next()
            
            if tablePlace != None:
                message = "{name} currently stand in position {position} in this season of the Premier League.".format(name=tablePlace['team'], position=tablePlace['position'])
            else:
                message = "We could not find this team's place in the table, please try again later."
            
        else:
            message = "We were unable to retrieve the table, please try again later."

        tableAPIConnection.close()
    
    else:
        message = "We couldn't find the team you were looking for, please try again with a more common name"
 
    resp = twilio.twiml.Response()
    resp.message(message)
 
    # print message
 
if __name__ == "__main__":
    # checkTable()
    app.run(debug=True)
