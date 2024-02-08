<?php
$servername = "192.168.1.249";
$username = "root";
$password = "1234";
$dbname = "health";

$conn = new mysqli($servername, $username, $password, $dbname);

if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

$sql1 = "SELECT * FROM total_pushup ORDER BY total DESC";
$result1 = $conn->query($sql1);
$count1 = 1;

$sql2 = "SELECT * FROM total_squat ORDER BY total DESC";
$result2 = $conn->query($sql2);
$count2 = 1;

$sql3 = "SELECT * FROM total_burpee ORDER BY total DESC";
$result3 = $conn->query($sql3);
$count3 = 1;

$str= "Daily Ranking <hr><hr>";
echo "<span style='font-size: 25px'>$str</span>";

if (1){
	echo "<strong>Push up</strong> <hr>";
  	echo "&nbsp;&nbsp;&nbsp;Rank&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;Name&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;Total count&nbsp;&nbsp;&nbsp;|<hr>";      
	if(isset($result1) && $result1->num_rows > 0){
	
	    while($row = $result1->fetch_assoc()){
            printf("%05d", $count1);
            printf("%5s", $row['name']);
            printf("%05d<br>", $row['total']); 
            $count1 = $count1 + 1;
	    }
	}
	else{
	    echo "No data about pushup. <hr>";
	}
}
echo "<br><hr>";


$conn->close();

?>
