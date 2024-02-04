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

$sql2 = "SELECT * FROM total_squat WHERE name = '$username'";
$result2 = $conn->query($sql2);

if(isset($result2) && $result2->num_rows > 0){
    while($row = $result2->fetch_assoc()){
        echo "Date: ".$row['date']."<br>";
        echo "Time: From ".$row['starttime']." to ".$row['endtime']."<br>";
        echo "Total count: ".$row['total']."<hr>"; 
    }
}
else{
    echo "No data about squat.";
}

?>
