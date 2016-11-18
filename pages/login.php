<?php
$feedback = "";
if (isset($_POST['uid'], $_POST['pwd'])) {
	$uid = $_POST['uid'];
	$pwd = $_POST['pwd'];
	if ($uid == "") {
		$feedback = "Missing username.";
	} else if ($pwd == "") {
		$feedback = "Missing password.";
	} else {
		$pwd = sha1($pwd);
		$result = $mysql->query("SELECT * FROM users WHERE uid='$uid' AND pwd='$pwd'");
		if (!$result || $result->num_rows == 0) {
			$feedback = "Incorrect credentials.";
		} else {
			$_SESSION['uid'] = $uid;
			header("Location: /?page=index");
			die();
		}
	}
}
?>

<?=$feedback?> <br/>
<form action='?page=login' method='POST' >
	Username: <input type='text' name='uid'/> <br/>
	Password: <input type='password' name='pwd'/> </br>
	<input type='submit' value='Login' />
</form>
