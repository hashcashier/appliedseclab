<?php
error_reporting(-1);
ini_set('display_errors', 'On');
ini_set('file_uploads', 'On');
$mysql = new mysqli("localhost", "root", "onlyone!1", "imovies");
session_start();

function hasValidCert() {
	if (!isset($_SERVER['SSL_CLIENT_M_SERIAL'])
       || !isset($_SERVER['SSL_CLIENT_V_END'])
       || !isset($_SERVER['SSL_CLIENT_VERIFY'])
       || $_SERVER['SSL_CLIENT_VERIFY'] !== 'SUCCESS'
       || !isset($_SERVER['SSL_CLIENT_I_DN'])
       || !isset($_SERVER['SSL_CLIENT_S_DN'])) {
		return false;
    }
 
	if ($_SERVER['SSL_CLIENT_V_REMAIN'] <= 0) {
		return false;
	}
	return true;
}

//print($_SERVER['SSL_CLIENT_M_SERIAL']."<br>");
//print($_SERVER['SSL_CLIENT_V_END']."<br>");
//print($_SERVER['SSL_CLIENT_VERIFY']."<br/>");
//print($_SERVER['SSL_CLIENT_I_DN']."<br>");
//print($_SERVER['SSL_CLIENT_S_DN']."<br>");
//print($_SERVER['SSL_CLIENT_V_REMAIN']."<br>");
//print($_SERVER['SSL_CLIENT_S_DN_CN']."<br>");
//print($_SERVER['SSL_CLIENT_S_DN_Email']."<br>");
//print($_SERVER['SSL_CLIENT_S_DN_OU']."<br>");
//print(json_encode($_SERVER)."<br>");

$isLoggedIn = isset($_SESSION['uid']);
$isCertAuth = $isLoggedIn && isset($_SESSION['cert']) && $_SESSION['cert'] == '1';
$isAdmin = $isLoggedIn && isset($_SESSION['admin']) && $_SESSION['admin'] == '1';

if (!$isLoggedIn && hasValidCert()) {
	
	$uid = $_SERVER['SSL_CLIENT_S_DN_CN'];
	$email = $_SERVER['SSL_CLIENT_S_DN_Email'];

	print("Authenticated via Certificate.<br/>");
	print("If you are not redirected then refresh the page.<br/>");
	print("$uid, If you continue to see this after refresh, then your certificate is not valid. Have you changed your email? ($email)</br>");
	
	$result = $mysql->query("SELECT * FROM users WHERE uid='$uid' AND email='$email'");
	if ($result && $result->num_rows == 1) {
		$_SESSION['uid'] = $uid;
		$_SESSION['cert'] = '1';
		if ($_SERVER['SSL_CLIENT_S_DN_OU'] == "admin") {
			$_SESSION['admin'] = '1';
		}
	}
	
	if (isset($_SESSION['uid'])) {
		header("Location: /?page=index");
	}
	die();
} else if ($isLoggedIn && $isCertAuth) {
	if (!hasValidCert() || $_SESSION['uid'] != $_SERVER['SSL_CLIENT_S_DN_CN']) {
		session_destroy();
		header("Location: /?page=index");
		die();
	}
}

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
		if ($isAdmin) {
			?>
			<a href="?page=admin">Admin</a> |
			<?php
		}
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
		$page = isset($_GET['page']) ? $_GET['page'] : '';
		switch ($page) {
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
			case "admin":
				include("pages/admin.php");
				break;
			case "index":
			default:
				include("pages/index.php");
		}
		?>
		
	</body>
</html>
