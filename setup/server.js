const http = require('http');
const fs = require('fs');
const PORT = 5000;

function loadData(path) {
    try {
        const data = fs.readFileSync(path, 'utf8');
        return JSON.parse(data);
    } catch (err) {
        console.error(`Error reading file from disk: ${err}`);
        return null;
    }
}

const requestHandler = (req, res) => {
    res.setHeader('Content-Type', 'application/json');

    if (req.url === '/api/talent' && req.method === 'GET') {
        const data = loadData('talent.json');
        res.end(JSON.stringify(data || { error: 'Error loading data' }));
    } else if (req.url === '/api/team_records' && req.method === 'GET') {
        const data = loadData('team_records.json');
        res.end(JSON.stringify(data || { error: 'Error loading data' }));
    } else if (req.url === '/api/team_stats' && req.method === 'GET') {
        const data = loadData('team_stats.json');
        res.end(JSON.stringify(data || { error: 'Error loading data' }));
    } else if (req.url === '/api/adv_stats' && req.method === 'GET') {
        const data = loadData('adv_stats.json');
        res.end(JSON.stringify(data || { error: 'Error loading data' }));
    } else if (req.url === '/api/games' && req.method === 'GET') {
        const data = loadData('games.json');
        res.end(JSON.stringify(data || { error: 'Error loading data' }));
    } else {
        res.statusCode = 404;
        res.end(JSON.stringify({ error: 'Endpoint not Found' }));
    }
};

const server = http.createServer(requestHandler);

server.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});
