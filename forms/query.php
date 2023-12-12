<?php
// Database connection
$servername = "your_db_host";
$username = "your_db_username";
$password = "your_db_password";
$database = "your_db_name";

$conn = new mysqli($servername, $username, $password, $database);

// SQL query
$sql = "SELECT name, email FROM users";
$result = $conn->query($sql);
?>

<!DOCTYPE html>
<html>
<head>
    <title>SQL Query Example</title>
</head>
<body>
    <h1>User Information</h1>

    <?php
    if ($result->num_rows > 0) {
        echo "<ul>";
        while ($row = $result->fetch_assoc()) {
            echo "<li>" . $row["name"] . " - " . $row["email"] . "</li>";
        }
        echo "</ul>";
    } else {
        echo "No records found.";
    }
    ?>

    <!-- Close the database connection -->
    <?php $conn->close(); ?>
</body>
</html>
