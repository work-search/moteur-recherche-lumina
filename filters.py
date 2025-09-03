def filter_explicit_content(results):
    explicit_keywords = [
        "sexe", "pornographie", "violence", "porno", "pucelle", "porn",
        "+18", "fuck", "Mia Khalifa", "arme", "gun", "god", "orgasme",
        "ejaculation", "feu", "bombe", "fusil", "cartel", "pistolet",
        "munition", "couteau", "violeur", "pedophile", "sex toys",
        "absu sexuel", "Nudité", "Érotique", "Drogue", "Suicide",
        "Terrorisme", "poki", "crazy game", "pute", "putain",
        "prostitué", "rencontre", "string", "fesse", "cul", "-18",
        "organe géniteur"
    ]
    filtered_results = []
    for result in results:
        if not any(keyword in result['title'].lower() or keyword in result['body'].lower() for keyword in explicit_keywords):
            filtered_results.append(result)
    return filtered_results
