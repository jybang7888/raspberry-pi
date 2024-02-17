<?php

$servername = "192.168.210.77";
$username = "root";
$password = "1234";
$dbname = "health";

$conn = new mysqli($servername, $username, $password, $dbname);

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $username = $_POST['username'];
    $password = $_POST['password'];
    $password_check = $_POST['password_check'];
}

$sql1 = "SELECT * FROM userinfo WHERE username = '$username'";
$result = $conn->query($sql1);

if ($result->num_rows > 0) {
    header("Location: http://192.168.210.77:5000/sign_up_exist");
}
else {
    if ($password == $password_check && strlen($password) >= 4) {
        $sql = "INSERT INTO userinfo (username, password) VALUES ('$username', '$password')";
        $conn->query($sql);
        header("Location: http://192.168.210.77:5000/main");
    }
    else {
        header("Location: http://192.168.210.77:5000/sign_up_wrong");
    }
}

$conn->close();
?>
