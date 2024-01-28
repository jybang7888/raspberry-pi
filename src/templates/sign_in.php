<?php
// 데이터베이스 연결 설정
$servername = "192.168.1.144";
$username = "root";
$password = "1234";
$dbname = "health";

$conn = new mysqli($servername, $username, $password, $dbname);

// 연결 확인
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

// 폼에서 전송된 사용자 이름과 비밀번호
$username = $_POST['username'];
$password = $_POST['password'];

// SQL 쿼리 작성
$sql = "SELECT * FROM userinfo WHERE name = '$username' AND password = '$password'";
$result = $conn->query($sql);

// 사용자 인증 확인

if ($result->num_rows > 0) {
    // 사용자 정보가 일치하는 경우
    // 여기에서 다음 페이지로 리디렉션하거나 필요한 작업을 수행할 수 있습니다.
    header("Location: count.html?username=$username");
    exit();
} else {
    // 사용자 정보가 일치하지 않는 경우
    header("Location: sign_in_wrong.html");
}

// 연결 종료
$conn->close();
?>
