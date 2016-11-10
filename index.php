<?php
error_reporting(-1);
ini_set('display_errors', 'On');
ini_set('file_uploads', 'On');
$mysql = new mysqli("localhost", "root", "onlyone!1", "imovies");
session_start();
$isLoggedIn = isset($_SESSION['uid']);
if ($isLoggedIn) {
	$uid = $_SESSION['uid'];
	$query = $mysql->query("SELECT * FROM users WHERE uid='$uid'");
	$user = $query->fetch_assoc();
}
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
			<a href="?page=profile">Profile</a> |
			<a href="?page=neucert">Request Certificate</a> |
			<a href="?page=revoke">Revoke Certificate</a> |
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
			case "profile":
				include("pages/profile.php");
				break;
			case "neucert":
				include("pages/neucert.php");
				break;
			case "revoke":
				include("pages/revoke.php");
				break;
			case "index":
			default:
				include("pages/index.php");
		}
		?>
		
	</body>
</html>
