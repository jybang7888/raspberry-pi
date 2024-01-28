<?php

$servername = "192.168.1.144";
$username = "root";
$password = "1234";
$dbname = "health";

$conn = new mysqli($servername, $username, $password, $dbname);

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $username = $_POST['username'];
    $password = $_POST['password'];
}

$sql = "INSERT INTO userinfo (username, password) VALUES ('$username', '$password')";
$conn->query($sql);
header("Location: http://192.168.1.144/main.html");

$conn->close();
?>
