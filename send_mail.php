<?php
/**
 * OmniMatrix Technologies - Contact & RFQ Mailer Handler
 * Handles contact form submissions from omnimatrixs.com
 */

header('Content-Type: application/json; charset=UTF-8');

// Allow only POST requests
if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    echo json_encode(['status' => 'error', 'message' => 'Method Not Allowed']);
    exit;
}

// 1. Anti-Spam Honeypot Check
if (!empty($_POST['website_hp'])) {
    // Bot detected, silently exit with success
    echo json_encode(['status' => 'success', 'message' => 'Thank you for your enquiry.']);
    exit;
}

// 2. Sanitize and Extract Input
$name    = isset($_POST['name']) ? trim(strip_tags($_POST['name'])) : '';
$email   = isset($_POST['email']) ? trim(filter_var($_POST['email'], FILTER_SANITIZE_EMAIL)) : '';
$phone   = isset($_POST['phone']) ? trim(strip_tags($_POST['phone'])) : '';
$service = isset($_POST['service']) ? trim(strip_tags($_POST['service'])) : 'General Enquiry';
$message = isset($_POST['message']) ? trim(strip_tags($_POST['message'])) : '';

// 3. Validation
if (empty($name) || empty($email) || empty($message)) {
    http_response_code(400);
    echo json_encode(['status' => 'error', 'message' => 'Please fill in all required fields (Name, Email, Message).']);
    exit;
}

if (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
    http_response_code(400);
    echo json_encode(['status' => 'error', 'message' => 'Please provide a valid email address.']);
    exit;
}

// 4. Email Configuration
$to = 'info@omnimatrixs.com, omnimatrixtechnologies@gmail.com';
$email_subject = "New RFQ / Enquiry from " . $name . " [" . $service . "]";

// 5. Build HTML Email Body
$body = '
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif; background-color: #f8fafc; color: #1e293b; padding: 20px; }
        .email-container { max-width: 600px; margin: 0 auto; background: #ffffff; border-radius: 8px; border: 1px solid #e2e8f0; overflow: hidden; box-shadow: 0 4px 12px rgba(0,0,0,0.05); }
        .header { background: #0b152d; color: #ffffff; padding: 24px; text-align: center; }
        .header h2 { margin: 0; color: #00d4ff; font-size: 20px; }
        .header p { margin: 6px 0 0; font-size: 13px; color: #94a3b8; }
        .content { padding: 28px; }
        .field-group { margin-bottom: 18px; border-bottom: 1px solid #f1f5f9; padding-bottom: 12px; }
        .field-group:last-child { border-bottom: none; }
        .label { font-size: 11px; text-transform: uppercase; letter-spacing: 0.8px; color: #64748b; font-weight: 700; margin-bottom: 4px; }
        .value { font-size: 15px; color: #0f172a; font-weight: 500; }
        .message-box { background: #f8fafc; padding: 16px; border-radius: 6px; border-left: 4px solid #00d4ff; font-size: 14px; line-height: 1.6; white-space: pre-line; }
        .footer { background: #f1f5f9; padding: 14px 28px; text-align: center; font-size: 12px; color: #64748b; }
    </style>
</head>
<body>
    <div class="email-container">
        <div class="header">
            <h2>OmniMatrix Technologies</h2>
            <p>New Website Enquiry / Request for Quotation</p>
        </div>
        <div class="content">
            <div class="field-group">
                <div class="label">Full Name</div>
                <div class="value">' . htmlspecialchars($name, ENT_QUOTES, 'UTF-8') . '</div>
            </div>
            <div class="field-group">
                <div class="label">Work Email</div>
                <div class="value"><a href="mailto:' . htmlspecialchars($email, ENT_QUOTES, 'UTF-8') . '">' . htmlspecialchars($email, ENT_QUOTES, 'UTF-8') . '</a></div>
            </div>
            <div class="field-group">
                <div class="label">Phone / WhatsApp</div>
                <div class="value">' . (!empty($phone) ? htmlspecialchars($phone, ENT_QUOTES, 'UTF-8') : 'Not provided') . '</div>
            </div>
            <div class="field-group">
                <div class="label">Area of Interest / Service</div>
                <div class="value">' . htmlspecialchars($service, ENT_QUOTES, 'UTF-8') . '</div>
            </div>
            <div class="field-group">
                <div class="label">Project Specifications / Message</div>
                <div class="message-box">' . nl2br(htmlspecialchars($message, ENT_QUOTES, 'UTF-8')) . '</div>
            </div>
        </div>
        <div class="footer">
            Submitted via omnimatrixs.com on ' . date('d M Y, H:i T') . ' (IP: ' . $_SERVER['REMOTE_ADDR'] . ')
        </div>
    </div>
</body>
</html>
';

// 6. Headers
$headers  = "MIME-Version: 1.0\r\n";
$headers .= "Content-type: text/html; charset=UTF-8\r\n";
$headers .= "From: OmniMatrix Website <no-reply@omnimatrixs.com>\r\n";
$headers .= "Reply-To: " . $name . " <" . $email . ">\r\n";
$headers .= "X-Mailer: PHP/" . phpversion();

// 7. Send Mail
$mail_sent = @mail($to, $email_subject, $body, $headers);

if ($mail_sent) {
    echo json_encode([
        'status' => 'success',
        'message' => 'Thank you for reaching out to OmniMatrix Technologies. Your enquiry has been received and an engineering specialist will contact you shortly.'
    ]);
} else {
    // If mail function fails on server, provide clear message
    http_response_code(500);
    echo json_encode([
        'status' => 'error',
        'message' => 'Unable to send message at this moment. Please contact us directly at info@omnimatrixs.com or call +91 9008344055.'
    ]);
}
