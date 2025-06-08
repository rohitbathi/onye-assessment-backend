from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from main import parse_query, build_fhir_request

app = Flask(__name__)

# enable CORS for every route
# if your front-end runs on e.g. http://localhost:3000, list that here instead
CORS(
    app,
    # resources={r"/*": {"origins": ["http://localhost:3000"]}},
    origins="http://localhost:3000",
    supports_credentials=True,
)

PATIENTS = [
    {"name": "Anand",  "age": 55, "gender": "female", "condition": "diabetes"},
    {"name": "Billa",    "age": 60, "gender": "male",   "condition": "hypertension"},
    {"name": "Sarthak",  "age": 35, "gender": "female", "condition": "asthma"},
    {"name": "David Warner",   "age": 70, "gender": "male",   "condition": "diabetes"},
    {"name": "Evanka",    "age": 45, "gender": "female", "condition": "arthritis"},
    {"name": "Fatima",  "age": 28, "gender": "male",   "condition": "covid-19"},
    {"name": "Koushik",  "age": 40, "gender": "female", "condition": "cancer"},
    {"name": "Vignesh",  "age": 65, "gender": "male",   "condition": "heart disease"},
    {"name": "Pujith",    "age": 55, "gender": "female", "condition": "depression"},
    {"name": "Roja",   "age": 72, "gender": "male",   "condition": "arthritis"},
    {"name": "Samantha",   "age": 19, "gender": "male",   "condition": "obesity"},
]

def filter_patients(age_gt, conditions, gender):
    results = PATIENTS
    if age_gt is not None:
        results = [p for p in results if p["age"] > age_gt]
    if gender:
        results = [p for p in results if p["gender"] == gender]
    if conditions:
        results = [p for p in results if p["condition"] in conditions]
    return results

@app.route('/')
def index():
    return send_from_directory('web', 'index.html')

@app.route('/web/<path:filename>')
def web_static(filename):
    return send_from_directory('web', filename)

@app.route('/query', methods=['POST'])
def query():
    data = request.get_json(force=True)
    text = data.get('text', '')
    age_gt, conditions, gender = parse_query(text)
    fhir_request = build_fhir_request(age_gt, conditions, gender)
    patients = filter_patients(age_gt, conditions, gender)
    return jsonify({'fhir_request': fhir_request, 'patients': patients})

if __name__ == '__main__':
    app.run(debug=True, port=4000)