<?php
$mysql = new mysqli("localhost", "root", "onlyone!1", "imovies");
session_start();
$isLoggedIn = isset($_SESSION['uid']);
?>
<html>
	<head>
		<title>iMovies Certificate Authority</title>
	</head>
	<body>
		<a href="?page=index">Home</a> | 
		<?php
		// Header menu bar
		if ($isLoggedIn) {
			?>
			<a href="?page=logout">Logout</a>
			<?php
		} else {
			?>
			<a href="?page=login">Login</a>
			<?php
		}
		?>
		<br/>
		
		<?php
		// Page selector
		switch ($_GET['page']) {
			case "login":
				include("pages/login.php");
				break;
			case "logout":
				include("pages/logout.php");
				break;
			case "index":
			default:
				include("pages/index.php");
		}
		?>
		
	</body>
</html>
