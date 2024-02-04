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

$sql1 = "SELECT * FROM total_pushup WHERE name = '$name' ORDER BY date DESC, start_time DESC LIMIT $count";
$result1 = $conn->query($sql1);
$sql2 = "SELECT * FROM total_squat WHERE name = '$name' ORDER BY date DESC, start_time DESC LIMIT $count";
$result2 = $conn->query($sql2);
$sql3 = "SELECT * FROM total_burpee WHERE name = '$name' ORDER BY date DESC, start_time DESC LIMIT $count";
$result3 = $conn->query($sql3);
echo "Data of " .$name. "<hr><hr>";
    
if ($exercise == 'PushUp' or $exercise == 'Total Exercises'){
	if(isset($result1) && $result1->num_rows > 0){
	header("Location: http://192.168.1.144:5000/record");
	    while($row = $result1->fetch_assoc()){
	        echo "Date: ".$row['date']."<br>";
	        echo "Time: From ".$row['start_time']." to ".$row['end_time']."<br>";
	        echo "Total count: ".$row['total']."<hr>"; 
	    }
	}
	else{
	    echo "No data about pushup.";
	}
}
echo "<hr>";
if ($exercise == 'Squat' or $exercise == 'Total Exercises'){
	if(isset($result2) && $result2->num_rows > 0){
	    while($row = $result2->fetch_assoc()){
	        echo "Date: ".$row['date']."<br>";
	        echo "Time: From ".$row['start_time']." to ".$row['end_time']."<br>";
	        echo "Total count: ".$row['total']."<hr>"; 
	    }
	}
	else{
	    echo "No data about squat.";
	}
}
echo "<hr>";
if ($exercise == 'Burpee' or $exercise == 'Total Exercises'){
	if(isset($result3) && $result3->num_rows > 0){
	    while($row = $result3->fetch_assoc()){
	        echo "Date: ".$row['date']."<br>";
	        echo "Time: From ".$row['start_time']." to ".$row['end_time']."<br>";
	        echo "Total count: ".$row['total']."<hr>"; 
	    }
	}
	else{
	    echo "No data about Burpee.";
	}
}

$conn->close();

?>
