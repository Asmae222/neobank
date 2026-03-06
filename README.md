# NeoBank Digital - Projet Sécurisé

## Structure du projet
```
neobank/
├── .github/workflows/      # Pipeline CI/CD
│   └── security_pipeline.yml
├── src/
│   ├── python/             # Services Python FastAPI
│   │   ├── accounts_service.py
│   │   ├── auth_service.py
│   │   └── database.py
│   └── javascript/         # Services Node.js Express
│       ├── payments_service.js
│       └── app.js
├── tests/
│   └── test_security.py    # Tests de sécurité
├── requirements.txt
├── package.json
├── .env.example
├── .gitignore
└── README.md
```

## Vulnérabilités corrigées

| ID  | Vulnérabilité            | Statut  |
|-----|--------------------------|---------|
| V1  | Injection SQL            | ✅ Corrigé |
| V2  | JWT sans expiration      | ✅ Corrigé |
| V3  | IDOR                     | ✅ Corrigé |
| V4  | Secrets en dur           | ✅ Corrigé |
| V5  | XSS Stored               | ✅ Corrigé |
| V6  | Mass Assignment          | ✅ Corrigé |
| V7  | Absence rate limiting    | ✅ Corrigé |
| V8  | Dépendances vulnérables  | ✅ Corrigé |
| V9  | Logging insuffisant      | ✅ Corrigé |
| V10 | Stack trace exposée      | ✅ Corrigé |
| V11 | Validation Content-Type  | ✅ Corrigé |
| V12 | CORS trop permissif      | ✅ Corrigé |

## Installation
```bash
# Python
pip install -r requirements.txt

# Node.js
npm install

# Variables d'environnement
cp .env.example .env
# Remplir les valeurs dans .env
```

## Lancer les tests
```bash
pytest tests/test_security.py -v
```
