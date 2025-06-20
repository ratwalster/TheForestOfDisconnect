const express = require('express');
const bodyParser = require('body-parser');
const app = express();

app.use(bodyParser.urlencoded({ extended: true }));

// In-memory storage (replace with database for persistence)
let optIns = [];

app.get('/', (req, res) => {
    res.send('Opt-In Server for The Forest of Disconnect');
});

app.post('/submit-opt-in', (req, res) => {
    const { phone, consent } = req.body;

    if (consent && phone && phone.match(/^\+1[0-9]{10}$/)) {
        const optIn = { phone, timestamp: new Date(), consented: true };
        optIns.push(optIn);
        console.log('New opt-in:', optIn);
        res.status(200).send('Thank you for opting in! You may now close this page.');
    } else {
        res.status(400).send('Invalid input. Please provide a valid phone number and consent.');
    }
});

app.listen(3000, () => {
    console.log('Server running on port 3000');
});