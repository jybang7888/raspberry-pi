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

$endtime = $_POST['currentTimeString'];
$starttime = clone $endtime;
$starttime -> modify('-1 minute');

$sql = "SELECT * FROM squat WHERE datetime > '$starttime' AND datetime < '$endtime'";

$result = $conn->query($sql);
if ($result->num_rows > 0) {
    while ($row = $result->fetch_assoc()) {
        if()
        $total++;
    }
}

$sql2 = "INSERT INTO heal (name, total) VALUES ('11', '$total')";
$conn->query($sql2);

$conn->close();
?>
