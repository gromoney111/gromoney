<?php
/**
 * GroMoney Capital — Stock API Proxy
 * Hides the IndianAPI key from client-side JavaScript
 * Usage: /api-proxy.php?stock=Reliance
 */

header('Content-Type: application/json');
header('Access-Control-Allow-Origin: https://gromoneycapital.com');
header('Cache-Control: public, max-age=21600');

// Rate limiting: max 50 requests per hour per IP
$ip = $_SERVER['REMOTE_ADDR'];
$rateLimitFile = sys_get_temp_dir() . '/gm_rate_' . md5($ip);
$requests = 0;
if (file_exists($rateLimitFile)) {
    $data = json_decode(file_get_contents($rateLimitFile), true);
    if ($data && time() - $data['time'] < 3600) {
        $requests = $data['count'];
    }
}
if ($requests >= 50) {
    http_response_code(429);
    echo json_encode(['error' => 'Rate limit exceeded']);
    exit;
}
file_put_contents($rateLimitFile, json_encode(['time' => time(), 'count' => $requests + 1]));

// Validate input
$stock = isset($_GET['stock']) ? trim($_GET['stock']) : '';
if (empty($stock) || strlen($stock) > 50) {
    http_response_code(400);
    echo json_encode(['error' => 'Invalid stock name']);
    exit;
}

// Whitelist allowed stocks
$allowed = ['Reliance','TCS','Infosys','SBI','ICICI Bank','Bharti Airtel','ITC','Tata Motors','HDFC Bank','Wipro','HCL Tech','Bajaj Finance','Kotak Bank','Axis Bank','Maruti Suzuki','Sun Pharma','Titan','Asian Paints','Adani Ports','L&T'];
if (!in_array($stock, $allowed)) {
    http_response_code(403);
    echo json_encode(['error' => 'Stock not allowed']);
    exit;
}

// API KEY — hidden from browser
$apiKey = 'sk-live-UATPt3yUVUwWAb82y1wOxJaspUvY1fbZEsdKpJa2';

$url = 'https://stock.indianapi.in/stock?name=' . urlencode($stock);
$ch = curl_init();
curl_setopt($ch, CURLOPT_URL, $url);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
curl_setopt($ch, CURLOPT_HTTPHEADER, ['X-Api-Key: ' . $apiKey]);
curl_setopt($ch, CURLOPT_TIMEOUT, 10);
$response = curl_exec($ch);
$httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
curl_close($ch);

if ($httpCode !== 200 || !$response) {
    http_response_code(502);
    echo json_encode(['error' => 'API unavailable']);
    exit;
}

$data = json_decode($response, true);
if ($data) {
    echo json_encode([
        'name' => $data['companyName'] ?? $stock,
        'price' => $data['currentPrice'] ?? null,
        'change' => $data['percentChange'] ?? 0
    ]);
} else {
    echo $response;
}
?>
