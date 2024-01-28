<?php
    $servername = "192.168.1.144";
    $username = "root";
    $password = "1234";
    $dbname = "health";
    $conn = new mysqli($servername, $username, $password, $dbname);
    if ($conn->connect_error) {
        die("Connection failed: " . $conn->connect_error);
    }
    $name = $_POST['username'];
    $hours = $_POST['hours'];
    $minutes = $_POST['minutes'];
    $seconds = $_POST['seconds'];

    $hours = sprintf("%02d", $hours);
    $minutes = sprintf("%02d", $minutes);
    $seconds = sprintf("%02d", $seconds);

    $endtime = $hours . ':' . $minutes . ':' . $seconds;
    $starttime = clone $endtime;
    $starttime -> modify('-1 minute');

    $sql = "SELECT * FROM squat WHERE datetime > '$starttime' AND datetime < '$endtime'";
    $result = mysqli_query($conn, $sql);
    $row_count = mysqli_num_rows($result);
    
    $sql1 = "INSERT INTO heal (name, total) VALUES ('$name', '$row_count')";
    $conn->query($sql1);
    
    header("localhost");

    mysqli_close($conn);
?>