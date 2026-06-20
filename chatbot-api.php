<?php
/**
 * GroMoney Capital — AI Chatbot Backend (Google Gemini Pro)
 * POST /chatbot-api.php with JSON body: {"message":"user question"}
 * GET  /chatbot-api.php?test=1 to verify setup
 */
header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: POST, GET, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type');
if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') exit;

// Read API key from secure file
$keyFile = __DIR__ . '/chatbot-key.txt';
$API_KEY = file_exists($keyFile) ? trim(file_get_contents($keyFile)) : '';

// TEST MODE: visit /chatbot-api.php?test=1 to check setup
if ($_SERVER['REQUEST_METHOD'] === 'GET' && isset($_GET['test'])) {
    $checks = [];
    $checks['key_file_exists'] = file_exists($keyFile);
    $checks['key_length'] = strlen($API_KEY);
    $checks['key_starts_with'] = substr($API_KEY, 0, 6);
    $checks['php_version'] = phpversion();
    $checks['curl_installed'] = function_exists('curl_init');
    if (!empty($API_KEY)) {
        $testUrl = 'https://generativelanguage.googleapis.com/v1beta/models?key=' . $API_KEY;
        $ch = curl_init($testUrl);
        curl_setopt_array($ch, [CURLOPT_RETURNTRANSFER=>true, CURLOPT_TIMEOUT=>10, CURLOPT_SSL_VERIFYPEER=>false]);
        $r = curl_exec($ch);
        $checks['curl_error'] = curl_error($ch) ?: 'none';
        $checks['http_code'] = curl_getinfo($ch, CURLINFO_HTTP_CODE);
        curl_close($ch);
        $checks['api_works'] = ($checks['http_code'] === 200);
    }
    echo json_encode($checks, JSON_PRETTY_PRINT); exit;
}

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    echo json_encode(['error' => 'Method not allowed']); exit;
}

// Rate limit: 30 msgs/hour per IP
$ip = $_SERVER['REMOTE_ADDR'];
$rf = sys_get_temp_dir() . '/gm_chat_' . md5($ip);
$rc = 0;
if (file_exists($rf)) { $d = json_decode(file_get_contents($rf), true); if ($d && time()-$d['time']<3600) $rc=$d['count']; }
if ($rc >= 30) { echo json_encode(['reply'=>'Message limit reached. Please call +91 96640 19564 or WhatsApp.']); exit; }
file_put_contents($rf, json_encode(['time'=>time(),'count'=>$rc+1]));

$input = json_decode(file_get_contents('php://input'), true);
$msg = trim($input['message'] ?? '');
if (!$msg || strlen($msg) > 500) { echo json_encode(['reply'=>'Please type a valid question.']); exit; }

if (empty($API_KEY)) {
    echo json_encode(['reply'=>'Chatbot setup incomplete. Please call +91 96640 19564.']); exit;
}

$systemPrompt = "You are the AI assistant for GroMoney Capital, AMFI-registered mutual fund distributor (ARN:270739) and IRDA-registered insurance referral partner. NJ Wealth Partner, India.

SERVICES: 1)Mutual Funds/SIP(5000+ schemes, SIP from Rs500/month) 2)PMS(min Rs50L, SEBI regulated) 3)AIF(min Rs1Cr, PE/VC/hedge) 4)SIF(min Rs10L, concentrated portfolios) 5)Life Insurance(LIC,HDFC Life,ICICI Pru,Max Life,Bajaj Allianz) 6)Health Insurance(Star Health,Niva Bupa,HDFC Ergo,ICICI Lombard,ManipalCigna) 7)Travel Insurance 8)Loans/Credit Cards(25+ partners) 9)Free CIBIL Check 10)EMI SIP Calculator

CONTACT: Phone +91 96640 19564 | Email contact@gromoneycapital.com | WhatsApp 919664019564 | Website gromoneycapital.com

RULES: Be concise (max 120 words). Speak Hindi or English based on user language. If user shows interest, ask for name and phone for free callback. Never guarantee returns. Add disclaimer for MF/insurance. Be friendly and helpful. Recommend relevant GroMoney services.";

// Gemini API endpoint (using gemini-2.5-flash - latest free model)
$url = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key=' . $API_KEY;

$payload = json_encode([
    'system_instruction' => ['parts' => [['text' => $systemPrompt]]],
    'contents' => [['parts' => [['text' => $msg]]]],
    'generationConfig' => [
        'maxOutputTokens' => 300,
        'temperature' => 0.7
    ]
]);

$ch = curl_init($url);
curl_setopt_array($ch, [
    CURLOPT_RETURNTRANSFER => true,
    CURLOPT_POST => true,
    CURLOPT_TIMEOUT => 30,
    CURLOPT_SSL_VERIFYPEER => false,
    CURLOPT_HTTPHEADER => ['Content-Type: application/json'],
    CURLOPT_POSTFIELDS => $payload
]);

$res = curl_exec($ch);
$err = curl_error($ch);
$code = curl_getinfo($ch, CURLINFO_HTTP_CODE);
curl_close($ch);

if ($err) {
    echo json_encode(['reply' => 'Connection error. Please call +91 96640 19564 or WhatsApp.']); exit;
}

if ($code !== 200) {
    echo json_encode(['reply' => 'I am currently unavailable. Please call +91 96640 19564 or WhatsApp.']); exit;
}

$data = json_decode($res, true);
$reply = $data['candidates'][0]['content']['parts'][0]['text'] ?? null;

if ($reply) {
    echo json_encode(['reply' => $reply]);
} else {
    echo json_encode(['reply' => 'I am currently unavailable. Please call +91 96640 19564 or WhatsApp.']);
}
