<?php
// MySQL 서버 연결 정보
$servername = "192.168.1.144";
$username = "root";
$password = "1234";
$dbname = "health";

// MySQL 데이터베이스에 연결
$conn = new mysqli($servername, $username, $password, $dbname);

// 연결 확인


// 사용자로부터 얻은 데이터
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $name = $_POST['name'];
    $pass = $_POST['password'];
    $count = $_POST['count'];
    $date = $_POST['date'];
    $password_check = $_POST['password_check'];
    
}

// SQL 쿼리 작성
$sql = "INSERT INTO user_data (name, password, count, date) VALUES ('$name', '$pass', '$count', '0121')";
$conn->query($sql);
header("Location: index.html");

// 연결 종료
$conn->close();
?>
