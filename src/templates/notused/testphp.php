<?php
$total = 0;
$servername = "192.168.1.144";
$username = "root";
$password = "1234";
$dbname = "health";

$conn = new mysqli($servername, $username, $password, $dbname);

if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

$sql1 = "INSERT INTO heal (name, total) VALUES ('11', '2')";
$conn->query($sql1);
?>
