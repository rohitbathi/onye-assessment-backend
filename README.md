# AI FHIR Backend

This project contains a small example script that converts natural language
queries into simulated FHIR API requests. It uses `spaCy` to extract
simple entities like age, conditions and gender from the input text.

## Setup

Install the required dependencies and download the spaCy model:

```bash
pip install spacy flask flask-cors
python -m spacy download en_core_web_sm
```

## Running the script

Run the program and enter a query when prompted:

```bash
python main.py
```

The script prints a simulated FHIR `Patient` search request based on the
entities it finds in your query.

## Running the web demo

1. **Start the Flask server** (serves both API and static files):

    ```bash
    python server.py
    ```

2. **Open the web UI**:

    Visit [http://localhost:5000/](http://localhost:5000/) in your browser.

    - The web interface is served from the `web` folder by Flask.
    - All static assets (like `style.css` and `script.js`) are loaded from `/web/`.
    - Enter a query in the text box and click "Submit".
    - The generated FHIR request and simulated patient results will be displayed in a table and bar chart.

**Note:**  
CORS is configured to allow both `http://localhost:5000` and `http://127.0.0.1:5000` for API requests. For best results, use the same hostname (either `localhost` or `127.0.0.1`) in both your browser and the Flask server.

## Example mappings

| Input text                                   | FHIR request                                   |
|----------------------------------------------|------------------------------------------------|
| `Show me all diabetic patients over 50`      | `/Patient?age=gt50&condition.code=diabetes`    |
| `List hypertensive male patients over 40`    | `/Patient?age=gt40&gender=male&condition.code=hypertension` |
| `Asthmatic female patients over 30`          | `/Patient?age=gt30&gender=female&condition.code=asthma` |
| `Find male patients over 65 with diabetes`   | `/Patient?age=gt65&gender=male&condition.code=diabetes` |
| `Patients over 20 with asthma or hypertension` | `/Patient?age=gt20&condition.code=asthma&condition.code=hypertension` |
