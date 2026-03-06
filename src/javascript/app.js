const express = require('express');
const helmet = require('helmet');
const rateLimit = require('express-rate-limit');
const app = express();

// ✅ Headers de sécurité
app.use(helmet());

// ✅ V11 CORRIGÉ : Validation Content-Type
app.use((req, res, next) => {
    if (['POST', 'PUT'].includes(req.method)) {
        if (!req.headers['content-type']?.includes('application/json')) {
            return res.status(415).json({ error: "Content-Type doit être application/json" });
        }
    }
    next();
});

app.use(express.json({ limit: '10kb' }));

// ✅ V7 CORRIGÉ : Rate limiting global
app.use(rateLimit({ windowMs: 15 * 60 * 1000, max: 100 }));

// ✅ V9 CORRIGÉ : Logging connexions
app.post('/login', (req, res) => {
    console.log(`[${new Date().toISOString()}] Tentative: ${req.body.username}`);
    const user = authenticate(req.body);
    if (user) console.log(`[${new Date().toISOString()}] Succès: ${user.id}`);
    res.json({ token: generateToken(user) });
});

// ✅ V10 CORRIGÉ : Pas de stack trace
app.use((err, req, res, next) => {
    console.error(err);
    res.status(500).json({ error: "Une erreur est survenue" });
});

module.exports = app;
