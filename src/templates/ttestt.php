<?php
    $servername = "192.168.1.144";
    $username = "root";
    $password = "1234";
    $dbname = "health";
    $conn = new mysqli($servername, $username, $password, $dbname);
    if ($conn->connect_error) {
        die("Connection failed: " . $conn->connect_error);
    }
    $starthours = $_POST['starthours'];
    $startminutes = $_POST['startminutes'];
    $startseconds = $_POST['startseconds'];
    $endhours = $_POST['endhours'];
    $endminutes = $_POST['endminutes'];
    $endseconds = $_POST['endseconds'];
    $year = $_POST['year'];
    $month = $_POST['month'];
    $day = $_POST['day'];
    
    $starthours = sprintf("%02d", $starthours);
    $startminutes = sprintf("%02d", $startminutes);
    $startseconds = sprintf("%02d", $startseconds);
    $endhours = sprintf("%02d", $endhours);
    $endminutes = sprintf("%02d", $endminutes);
    $endseconds = sprintf("%02d", $endseconds);
    $year = sprintf("%04d", $year);
    $month = sprintf("%02d", $month);
    $day = sprintf("%02d", $day);
    
    $endtime = $endhours . ':' . $endminutes . ':' . $endseconds;
    $starttime = $starthours . ':' . $startminutes . ':' . $startseconds;
    $date = $year . '-' . $month . '-' . $day;

    $sql = "SELECT * FROM squat WHERE datetime > '$starttime' AND datetime < '$endtime' AND state = 'down'";
    $result = mysqli_query($conn, $sql);
    $row_count = mysqli_num_rows($result);
    
    $sql1 = "INSERT INTO heal (name, date, time, total) VALUES ('jun', '$date', '$starttime', '$row_count')";
    $conn->query($sql1);
    
    header("localhost");

    mysqli_close($conn);
?>
