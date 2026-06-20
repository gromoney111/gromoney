<?php
/**
 * GroMoney Capital — AI Chatbot Backend (OpenAI GPT-4o-mini)
 * POST /chatbot-api.php with JSON body: {"message":"user question"}
 */
header('Content-Type: application/json');
header('Access-Control-Allow-Origin: https://gromoneycapital.com');
header('Access-Control-Allow-Methods: POST');
header('Access-Control-Allow-Headers: Content-Type');
if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') exit;
if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    echo json_encode(['error' => 'Method not allowed']); exit;
}

// Rate limit: 30 msgs/hour per IP
$ip = $_SERVER['REMOTE_ADDR'];
$rf = sys_get_temp_dir() . '/gm_chat_' . md5($ip);
$rc = 0;
if (file_exists($rf)) { $d = json_decode(file_get_contents($rf), true); if ($d && time()-$d['time']<3600) $rc=$d['count']; }
if ($rc >= 30) { echo json_encode(['reply'=>'Message limit reached. Call +91 96640 19564 or WhatsApp.']); exit; }
file_put_contents($rf, json_encode(['time'=>time(),'count'=>$rc+1]));

$input = json_decode(file_get_contents('php://input'), true);
$msg = trim($input['message'] ?? '');
if (!$msg || strlen($msg)>500) { echo json_encode(['reply'=>'Please type a valid question.']); exit; }

// === YOUR OPENAI API KEY (from platform.openai.com) ===
$API_KEY = 'YOUR_OPENAI_API_KEY_HERE';

$system = "You are the AI assistant for GroMoney Capital, AMFI-registered mutual fund distributor (ARN:270739) and IRDA-registered insurance referral partner. NJ Wealth Partner, India.

SERVICES: 1)Mutual Funds/SIP(5000+ schemes, SIP from Rs500/month) 2)PMS(min Rs50L, SEBI regulated) 3)AIF(min Rs1Cr, PE/VC/hedge) 4)SIF(min Rs10L, concentrated portfolios) 5)Life Insurance(LIC,HDFC Life,ICICI Pru,Max Life,Bajaj Allianz) 6)Health Insurance(Star Health,Niva Bupa,HDFC Ergo,ICICI Lombard,ManipalCigna) 7)Travel Insurance 8)Loans/Credit Cards(25+ partners) 9)Free CIBIL Check 10)EMI SIP Calculator

CONTACT: +91 96640 19564 | contact@gromoneycapital.com | WhatsApp: 919664019564 | Website: gromoneycapital.com

RULES: Be concise(max 120 words). Speak Hindi or English per user. If interested, ask name+phone for free callback. Never guarantee returns. Add disclaimer for MF/insurance. Be friendly.";

$ch = curl_init('https://api.openai.com/v1/chat/completions');
curl_setopt_array($ch, [
    CURLOPT_RETURNTRANSFER => true, CURLOPT_POST => true, CURLOPT_TIMEOUT => 25,
    CURLOPT_HTTPHEADER => ['Content-Type: application/json', 'Authorization: Bearer '.$API_KEY],
    CURLOPT_POSTFIELDS => json_encode([
        'model' => 'gpt-4o-mini',
        'messages' => [['role'=>'system','content'=>$system],['role'=>'user','content'=>$msg]],
        'max_tokens' => 250, 'temperature' => 0.7
    ])
]);
$res = curl_exec($ch); $code = curl_getinfo($ch, CURLINFO_HTTP_CODE); curl_close($ch);

if ($code !== 200 || !$res) {
    echo json_encode(['reply'=>'I am currently unavailable. Please call +91 96640 19564 or WhatsApp.']); exit;
}
$data = json_decode($res, true);
echo json_encode(['reply' => $data['choices'][0]['message']['content'] ?? 'Please call +91 96640 19564.']);
