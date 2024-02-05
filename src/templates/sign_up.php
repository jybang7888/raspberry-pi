<?php

$servername = "192.168.1.249";
$username = "root";
$password = "1234";
$dbname = "health";

$conn = new mysqli($servername, $username, $password, $dbname);

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $username = $_POST['username'];
    $password = $_POST['password'];
    $password_check = $_POST['password_check'];
}

if ($password == $password_check) {
    $sql = "INSERT INTO userinfo (username, password) VALUES ('$username', '$password')";
    $conn->query($sql);
    header("Location: http://192.168.1.249:5000/main");
}
else {
    header("Location: http://192.168.1.249:5000/sign_up_wrong");
}

$conn->close();
?>
