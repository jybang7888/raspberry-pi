<?php
$servername = "192.168.1.144";
$username = "root";
$password = "1234";
$dbname = "health";

$conn = new mysqli($servername, $username, $password, $dbname);

if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

$name = $_GET['name'];
$exercise = $_GET['exercise'];
$count = $_GET['count'];

$sql2 = "SELECT * FROM total_pushup WHERE name = '$name' LIMIT '$count'";
$result2 = $conn->query($sql2);

if(isset($result2) && $result2->num_rows > 0){
    echo "Data of " .$name. "<hr><hr>";
    $dataRows = array();
    while($row = $result2->fetch_assoc()){
        $dataRows[] = $row;
    }
    $dataRows = array_reverse($dataRows);
    while($row = $result2->fetch_assoc()){
        echo "Date: ".$row['date']."<br>";
        echo "Time: From ".$row['start_time']." to ".$row['end_time']."<br>";
        echo "Total count: ".$row['total']."<hr>"; 
    }
}
else{
    echo "No data about pushup.";
}
$conn->close();

?>
