<?php
    $servername = "192.168.210.77";
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
    $name = $_GET['username'];

    $starthours = sprintf("%02d", $starthours);
    $startminutes = sprintf("%02d", $startminutes);
    $startseconds = sprintf("%02d", $startseconds);
    $endhours = sprintf("%02d", $endhours);
    $endminutes = sprintf("%02d", $endminutes);
    $endseconds = sprintf("%02d", $endseconds);
    
    $endtime = $endhours . ':' . $endminutes . ':' . $endseconds;
    $starttime = $starthours . ':' . $startminutes . ':' . $startseconds;
    $date = date("Y-m-d");

    $sql = "SELECT * FROM squat WHERE datetime > '$starttime' AND datetime < '$endtime' AND state = 'up'";
    $result = mysqli_query($conn, $sql);
    $row_count = mysqli_num_rows($result);
    
    $sql1 = "INSERT INTO total_squat (name, date, start_time, end_time, total) VALUES ('$name', '$date', '$starttime', '$endtime', '$row_count')";
    $conn->query($sql1);

    $sql2 = "DELETE FROM total_squat WHERE end_time = '00:00:00'";
    $conn->query($sql2);

        if($endtime == '00:00:00'){
	    $str = "Squat Data <hr><hr>";
            echo "<span style='font-size: 25px'>$str</span>";
            echo "Since the save button is activated too early, your data is not recorded.";
        }
        else{
            $str = "Squat Data <hr><hr>";
            echo "<span style='font-size: 25px'>$str</span>";
            echo "USER: ".$name."<hr>";
            echo "Date: ".$date."<br>";
            echo "Time: From ".$starttime." to ".$endtime."<br>";
            echo "Total: ".$row_count."<hr>";
        }
    
    header("localhost");

    mysqli_close($conn);
?>
