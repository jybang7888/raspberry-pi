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

$twoDimArray1 = array();
$twoDimArray2 = array();
$twoDimArray3 = array();

$rows = 3;
$cols = 3;

// 2차원 배열에 빈 배열을 추가하여 초기화
for ($i = 0; $i < $rows; $i++) {
    $twoDimArray[$i] = array();
}

// 예시: 값을 추가하기 전에 2차원 배열 출력
echo "<pre>";
print_r($twoDimArray);
echo "</pre>";

// 나중에 값을 넣을 위치를 지정한 후 값을 할당
$twoDimArray[0][0] = 1;
$twoDimArray[0][1] = 2;
$twoDimArray[0][2] = 3;
$twoDimArray[1][0] = 4;
$twoDimArray[1][1] = 5;
$twoDimArray[1][2] = 6;
$twoDimArray[2][0] = 7;
$twoDimArray[2][1] = 8;
$twoDimArray[2][2] = 9;

// 값이 할당된 2차원 배열 출력
echo "<pre>";
print_r($twoDimArray);
echo "</pre>";









if(isset($result1) && $result1->num_rows > 0){
    while($row = $result1->fetch_assoc()){
        echo "Date: ".$row['date']."<br>";
        echo "Time: From ".$row['start_time']." to ".$row['end_time']."<br>";
        echo "Total count: ".$row['total']."<hr>"; 
    }
}
else{
    echo "No data about pushup.";
}
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

header("Location: http://192.168.1.144:5000/record?name=$name&exercise=$exercise&");
$conn->close();
?>
