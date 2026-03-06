const express = require('express');
const router = express.Router();
const cors = require('cors');
const rateLimit = require('express-rate-limit');
const { body, validationResult } = require('express-validator');

// ✅ V12 CORRIGÉ : CORS restrictif
const corsOptions = {
    origin: ['https://neobank.fr', 'https://app.neobank.fr'],
    methods: ['GET', 'POST', 'PUT'],
    allowedHeaders: ['Content-Type', 'Authorization']
};
router.use(cors(corsOptions));

// ✅ V7 CORRIGÉ : Rate limiting login
const loginLimiter = rateLimit({
    windowMs: 15 * 60 * 1000,
    max: 5,
    message: { error: "Trop de tentatives, réessayez dans 15 minutes" },
    headers: true
});
router.use('/login', loginLimiter);

// ✅ V6 CORRIGÉ : Whitelist champs modifiables
const ALLOWED_FIELDS = ['email', 'phone', 'address'];

router.put('/user/profile', async (req, res) => {
    const userId = req.user.id;
    const safeUpdate = {};
    ALLOWED_FIELDS.forEach(field => {
        if (req.body[field] !== undefined) safeUpdate[field] = req.body[field];
    });
    await db.users.update(userId, safeUpdate);
    res.json({ message: 'Profil mis à jour' });
});

// ✅ V5 CORRIGÉ : Protection XSS
router.post('/transfer', [
    body('description').trim().escape().isLength({ max: 200 }),
    body('amount').isFloat({ min: 0.01 }),
    body('to_account').isUUID()
], async (req, res) => {
    const errors = validationResult(req);
    if (!errors.isEmpty()) return res.status(400).json({ error: "Données invalides" });

    const { to_account, amount, description } = req.body;
    const transfer = await db.transfers.create({
        from_account: req.user.account_id,
        to_account, amount, description
    });
    res.json(transfer);
});

module.exports = router;
