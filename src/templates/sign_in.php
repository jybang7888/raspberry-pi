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

$sql = "SELECT * FROM userinfo WHERE name = '$username' AND password = '$password'";
$result = $conn->query($sql);

if ($result->num_rows > 0) {
    // 사용자 정보가 일치하는 경우
    header("Location: http://192.168.1.144:5000/count.html?username=$username");
    exit();
} else {
    // 사용자 정보가 일치하지 않는 경우
    header("Location: http://192.168.1.144:5000/sign_in_wrong");
}

// 연결 종료
$conn->close();
?>
