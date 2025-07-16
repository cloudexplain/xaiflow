import http from 'http';
import fs from 'fs';
import path from 'path';
import { WebSocketServer } from 'ws';
import chokidar from 'chokidar';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const PORT = 3002;
const DEV_DIR = path.join(__dirname);
const BUNDLE_FILE = path.join(DEV_DIR, 'bundle.js');

// Create HTTP server
const server = http.createServer((req, res) => {
  const url = req.url === '/' ? '/dev-index.html' : req.url;
  const filePath = path.join(DEV_DIR, url);
  
  // Security check - only serve files from dev directory
  if (!filePath.startsWith(DEV_DIR)) {
    res.writeHead(404);
    res.end('Not found');
    return;
  }
  
  // Determine content type
  const ext = path.extname(filePath);
  const contentTypes = {
    '.html': 'text/html',
    '.js': 'application/javascript',
    '.css': 'text/css',
    '.json': 'application/json',
    '.map': 'application/json'
  };
  
  const contentType = contentTypes[ext] || 'text/plain';
  
  // Try to read and serve the file
  fs.readFile(filePath, (err, data) => {
    if (err) {
      res.writeHead(404);
      res.end('File not found');
      return;
    }
    
    res.writeHead(200, { 
      'Content-Type': contentType,
      'Cache-Control': 'no-cache' // Prevent caching during development
    });
    res.end(data);
  });
});

// Create WebSocket server for hot reload
const wss = new WebSocketServer({ 
  server,
  path: '/ws'
});

let clients = new Set();

wss.on('connection', (ws) => {
  clients.add(ws);
  console.log('🔌 Client connected for hot reload');
  
  ws.on('close', () => {
    clients.delete(ws);
    console.log('🔌 Client disconnected');
  });
});

// Function to notify all clients to reload
function notifyReload() {
  console.log('🔄 Notifying clients to reload...');
  clients.forEach(client => {
    if (client.readyState === 1) { // WebSocket.OPEN
      client.send('reload');
    }
  });
}

// Watch for bundle.js changes
const watcher = chokidar.watch(BUNDLE_FILE, {
  ignoreInitial: true
});

watcher.on('change', () => {
  console.log('📦 Bundle updated, triggering reload...');
  // Small delay to ensure file is fully written
  setTimeout(notifyReload, 100);
});

// Start server
server.listen(PORT, () => {
  console.log('🚀 Development server started!');
  console.log(`📱 Open: http://localhost:${PORT}`);
  console.log('🔥 Hot reload enabled');
  console.log('👀 Watching bundle.js for changes...');
  console.log('');
  console.log('To start development:');
  console.log('1. Run this server: node dev/dev-server.js');
  console.log('2. In another terminal: npm run dev:watch');
  console.log('3. Open http://localhost:3000 in your browser');
});

// Graceful shutdown
process.on('SIGINT', () => {
  console.log('\n🛑 Shutting down development server...');
  watcher.close();
  server.close();
  process.exit(0);
});
