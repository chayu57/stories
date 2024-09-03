const http = require('http');
const https = require('https');

const server = http.createServer((req, res) => {
    if (req.url === '/getTimeStories' && req.method === 'GET') {
        https.get('https://time.com', (response) => {
            let data = '';
            
            response.on('data', (chunk) => {
                data += chunk;
            });
            
            response.on('end', () => {
                const stories = [];
                const regex = /<a href="(\/\d{4}\/\d{2}\/\d{2}\/.+?)".+?>(.+?)<\/a>/g;
                let match;
                
                while ((match = regex.exec(data)) !== null) {
                    if (stories.length < 6) {
                        stories.push({
                            title: match[2].trim(),
                            link: `https://time.com${match[1]}`
                        });
                    } else {
                        break;
                    }
                }
                
                res.writeHead(200, { 'Content-Type': 'application/json' });
                res.end(JSON.stringify(stories));
            });
        }).on('error', (err) => {
            res.writeHead(500, { 'Content-Type': 'text/plain' });
            res.end('Error fetching stories');
        });
    } else {
        res.writeHead(404, { 'Content-Type': 'text/plain' });
        res.end('Not Found');
    }
});

server.listen(3000, () => {
    console.log('Server is running on http://localhost:3000');
});

