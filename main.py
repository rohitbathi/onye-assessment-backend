import spacy

nlp = spacy.load("en_core_web_sm")

CONDITION_KEYWORDS = {
    "diabetes":       {"diabetes", "diabetic"},
    "hypertension":   {"hypertension", "hypertensive"},
    "asthma":         {"asthma", "asthmatic"},
    "arthritis":      {"arthritis", "arthritic"},
    "cancer":         {"cancer", "malignancy"},
    "covid-19":       {"covid-19", "covid19", "coronavirus"},
    "heart disease":  {"heart disease", "cardiovascular disease", "cardiac"},
    "depression":     {"depression", "depressive"},
    "obesity":        {"obesity", "obese"},
}

GENDER_KEYWORDS = {"male", "female"}


def parse_query(text: str):
    doc = nlp(text)
    age_gt = None
    gender = None
    conditions = set()

    for token in doc:
        if token.like_num:
            try:
                value = int(token.text)
            except ValueError:
                continue
            prefix = text[max(0, token.idx - 15) : token.idx].lower()
            if any(k in prefix for k in ["over", "greater than", "older than"]):
                age_gt = value
        lemma = token.lemma_.lower()
        if lemma in GENDER_KEYWORDS:
            gender = lemma
        for cond, keywords in CONDITION_KEYWORDS.items():
            if lemma in keywords:
                conditions.add(cond)

    return age_gt, sorted(conditions), gender


def build_fhir_request(age_gt, conditions, gender):
    params = []
    if age_gt is not None:
        params.append(f"age=gt{age_gt}")
    if gender:
        params.append(f"gender={gender}")
    for c in conditions:
        params.append(f"condition.code={c}")
    if not params:
        return "/Patient"
    return "/Patient?" + "&".join(params)


def main():
    text = input("Enter query: ")
    age_gt, conditions, gender = parse_query(text)
    request = build_fhir_request(age_gt, conditions, gender)
    print("FHIR request:", request)


if __name__ == "__main__":
    main()