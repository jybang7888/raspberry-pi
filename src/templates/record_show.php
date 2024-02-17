<?php
$servername = "192.168.210.77";
$username = "root";
$password = "1234";
$dbname = "health";

$conn = new mysqli($servername, $username, $password, $dbname);

if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

$name = $_GET['name'];
$exercise = $_GET['exercise'];
$date1 = $_GET['date1'];
$date2 = $_GET['date2'];

$sql1 = "SELECT * FROM total_pushup WHERE name = '$name' AND date >= '$date1' AND date <= '$date2' ORDER BY date DESC, start_time DESC";
$result1 = $conn->query($sql1);
$sql2 = "SELECT * FROM total_squat WHERE name = '$name' AND date >= '$date1' AND date <= '$date2' ORDER BY date DESC, start_time DESC";
$result2 = $conn->query($sql2);
$sql3 = "SELECT * FROM total_burpee WHERE name = '$name' AND date >= '$date1' AND date <= '$date2' ORDER BY date DESC, start_time DESC";
$result3 = $conn->query($sql3);

$str= "Exercise Data of " .$name. "<hr><hr>";
echo "<span style='font-size: 25px'>$str</span>";

if ($exercise == 'PushUp' or $exercise == 'Total Exercises'){
	echo "<strong>Push up</strong> <hr>";
	if(isset($result1) && $result1->num_rows > 0){
	
	    while($row = $result1->fetch_assoc()){
	        echo "Date: ".$row['date']."<br>";
	        echo "Time: From ".$row['start_time']." to ".$row['end_time']."<br>";
	        echo "Total count: ".$row['total']."<hr>"; 
	    }
	}
	else{
	    echo "No data about pushup. <hr>";
	}
}
echo "<br><hr>";
if ($exercise == 'Squat' or $exercise == 'Total Exercises'){
	echo "<strong>Squat</strong> <hr>";	
	if(isset($result2) && $result2->num_rows > 0){
	    while($row = $result2->fetch_assoc()){
	        echo "Date: ".$row['date']."<br>";
	        echo "Time: From ".$row['start_time']." to ".$row['end_time']."<br>";
	        echo "Total count: ".$row['total']."<hr>"; 
	    }
	}
	else{
	    echo "No data about squat.<hr>";
	}
}
echo "<br><hr>";
if ($exercise == 'Burpee' or $exercise == 'Total Exercises'){
	echo "<strong>Burpee</strong> <hr>";	
	if(isset($result3) && $result3->num_rows > 0){
	    while($row = $result3->fetch_assoc()){
	        echo "Date: ".$row['date']."<br>";
	        echo "Time: From ".$row['start_time']." to ".$row['end_time']."<br>";
	        echo "Total count: ".$row['total']."<hr>"; 
	    }
	}
	else{
	    echo "No data about Burpee.<hr>";
	}
}

$conn->close();

?>
