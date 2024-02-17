<?php
$servername = "192.168.210.77";
$username = "root";
$password = "1234";
$dbname = "health";

$conn = new mysqli($servername, $username, $password, $dbname);

if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

$username = $_POST['username'];
$password = $_POST['password'];
$exercise = $_POST['exercise'];
$date1 = $_POST['date1'];
$date2 = $_POST['date2'];

$sql = "SELECT * FROM userinfo WHERE username = '$username' AND password = '$password'";
$result = $conn->query($sql);

if ($result->num_rows > 0) {
    header("Location: record_show.php?name=$username&exercise=$exercise&date1=$date1&date2=$date2");
    exit;
} else {
    header("Location: http://192.168.210.77:5000/record_wrong");
}

$conn->close();
?>
