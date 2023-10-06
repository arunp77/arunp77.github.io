<?php
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $name = $_POST["name"];
    $email = $_POST["email"];
    $subject = $_POST["subject"];
    $message = $_POST["message"];

    $to = "arunp77@gmail.com"; // Your email address
    $subject = "Contact Form Submission: $subject";
    $headers = "From: $email\r\n";
    $headers .= "Reply-To: $email\r\n";
    
    $mailBody = "Name: $name\n";
    $mailBody .= "Email: $email\n";
    $mailBody .= "Subject: $subject\n\n";
    $mailBody .= "Message:\n$message";

    if (mail($to, $subject, $mailBody, $headers)) {
        echo "success"; // You can customize this response message
    } else {
        echo "error"; // You can customize this response message
    }
}
?>
