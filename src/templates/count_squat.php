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
    
    $sql1 = "INSERT INTO total_squat (name, date, starttime, endtime, total) VALUES ('$name', '$date', '$starttime', '$endtime', '$row_count')";

    $conn->query($sql1);

    $sql2 = "SELECT * FROM squat WHERE name = '$name'";
    $result2 = $conn->query($sql2);
    if(isset($result2) && $result2->num_rows > 0){
        echo "Data of " .$name. "<hr><hr>";
        while($row = $result2->fetch_assoc()){
            echo "Date: ".$row['datetime']."<br>";
            echo "State: ".$row['state']."<hr>"; 
        }
    }
    else{
        echo "No data about squat.";
    }
    header("localhost");

    mysqli_close($conn);
?>
