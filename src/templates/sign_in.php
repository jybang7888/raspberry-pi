<?php
$servername = "192.168.1.144";
$username = "root";
$password = "1234";
$dbname = "health";

$conn = new mysqli($servername, $username, $password, $dbname);

if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

$username = $_POST['username'];
$password = $_POST['password'];

$sql = "SELECT * FROM userinfo WHERE username = '$username' AND password = '$password'";
$result = $conn->query($sql);

if ($result->num_rows > 0) {
    header("Location: http://192.168.1.144:5000/count?username=$username");
    exit();
} else {
    header("Location: http://192.168.1.144:5000/sign_in");
}

$conn->close();
?>
