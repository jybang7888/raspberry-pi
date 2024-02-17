<?php

$servername = "192.168.210.77";
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
$num1 = 0;
$c1 = 0;

$sql2 = "SELECT * FROM total_squat ORDER BY total DESC";
$result2 = $conn->query($sql2);
$count2 = 1;
$num2 = 0;
$c2 = 0;

$sql3 = "SELECT * FROM total_burpee ORDER BY total DESC";
$result3 = $conn->query($sql3);
$count3 = 1;
$num3 = 0;
$c3 = 0;

$str= "Total Ranking <hr><hr>";
echo "<span style='font-size: 25px'>$str</span>";

echo "<strong>Push up</strong> <hr>";
echo "&nbsp;&nbsp;&nbsp;Rank&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;Count&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;Name&nbsp;&nbsp;&nbsp;<hr>";      
if(isset($result1) && $result1->num_rows > 0){
	while($row = $result1->fetch_assoc()){
	    if($num1 != $row['total']){
		    printf("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;%d&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|", $count1);
		    $c1 = $count1;
	    }
	    else
	    printf("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;%d&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|", $c1);
	    printf("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;%02d&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|", $row['total']); 
            printf("&nbsp;&nbsp;&nbsp;%s", $row['name']);
            $num1 = $row['total'];
	   if($result1->num_rows != $count1)
		    echo "<br>";
	   else
		   echo "<hr>";
            $count1 = $count1 + 1;

	    }
	}
else{
	echo "No data about pushup. <hr>";
}

echo "<br><hr>";

echo "<strong>Squat</strong> <hr>";
echo "&nbsp;&nbsp;&nbsp;Rank&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;Count&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;Name&nbsp;&nbsp;&nbsp;<hr>";      
if(isset($result2) && $result2->num_rows > 0){
	while($row = $result2->fetch_assoc()){
	    if($num2 != $row['total']){
		    printf("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;%d&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|", $count2);
		    $c2 = $count2;
	    }
	    else
	    printf("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;%d&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|", $c2);
	    printf("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;%02d&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|", $row['total']); 
            printf("&nbsp;&nbsp;&nbsp;%s", $row['name']);
            $num2 = $row['total'];
	   if($result2->num_rows != $count2)
		    echo "<br>";
	   else
		   echo "<hr>";
            $count2 = $count2 + 1;

	    }
	}
else{
	echo "No data about squat. <hr>";
}

echo "<br><hr>";

echo "<strong>Burpee</strong> <hr>";
echo "&nbsp;&nbsp;&nbsp;Rank&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;Count&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;Name&nbsp;&nbsp;&nbsp;<hr>";      
if(isset($result3) && $result3->num_rows > 0){
	while($row = $result3->fetch_assoc()){
	    if($num3 != $row['total']){
		    printf("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;%d&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|", $count3);
		    $c3 = $count3;
	    }
	    else
	    printf("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;%d&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|", $c3);
	    printf("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;%02d&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|", $row['total']); 
            printf("&nbsp;&nbsp;&nbsp;%s", $row['name']);
            $num3 = $row['total'];
	   if($result3->num_rows != $count3)
		    echo "<br>";
	   else
		   echo "<hr>";
            $count3 = $count3 + 1;

	    }
	}
else{
	echo "No data about burpee. <hr>";
}

$conn->close();

?>
