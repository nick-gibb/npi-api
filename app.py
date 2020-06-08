import flask
import pandas as pd

app = flask.Flask(__name__)
app.config["DEBUG"] = True

filepath = "https://raw.githubusercontent.com/jajsmith/COVID19NonPharmaceuticalInterventions/master/npi_canada.csv"
# Read NPI Canada CSV (U of T group)
df = pd.read_csv(filepath,parse_dates=['start_date', 'end_date']).drop(columns='Unnamed: 0')
# df = pd.read_csv("https://raw.githubusercontent.com/jajsmith/COVID19NonPharmaceuticalInterventions/master/npi_canada.csv",
#                    parse_dates=['start_date', 'end_date']).drop(columns='Unnamed: 0')

# If the region field is blank, it applies to all Canada
# May want to leave this null?
df["region"].fillna('All', inplace=True)

# If subregion blank, it applies to all cities
# May want to leave this null?
df["subregion"].fillna('All', inplace=True)

# Fix minor typos
df= df.replace({'country' : { 'Canda' : 'Canada', 'Canada ' : 'Canada'}})

# Should not have null values in intervention category (?)
df.intervention_category.fillna('Unclassified', inplace=True)

# Too much text in this column for API
del df['source_full_text']
del df['end_source_full_text']

df['start_date'] = df['start_date'].dt.strftime('%Y-%m-%d')
df['end_date'] = df['end_date'].dt.strftime('%Y-%m-%d')

@app.route('/', methods=['GET'])
def home():
    return '''<h1>NPI API</h1>
<p>A prototype API for NPIs in Canada.</p>'''

@app.route('/api/stringency/date-range/<start_date>/<end_date>', methods=['GET'])
def byday(start_date, end_date):
    json_res = df[(df['start_date']>start_date) & (df['end_date']<end_date)].to_json(date_format='iso', orient='records')
    return json_res


@app.route('/api/stringency/actions/<place>/<date>', methods=['GET'])
def byplace(place, date):
    json_res = df[((df['region']==place) | (df['subregion']==place)) & ((df['start_date']==date) | (df['end_date']==date))].to_json(date_format='iso', orient='records')
    return json_res

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')