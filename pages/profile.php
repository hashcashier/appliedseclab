<?php
$feedback = "";
if (!$isLoggedIn) {
	header("Location: /?page=index");
	die();
} else if (isset($_POST['fname'], $_POST['lname'], $_POST['email'])) {
	$fname = $_POST['fname'];
	$lname = $_POST['lname'];
	$email = $_POST['email'];
	if ($fname == "") {
		$feedback = "First Name Cannot Be Blank";
	} else if ($lname == "") {
		$feedback = "Last Name Cannot Be Blank";
	} else if ($email == "") {
		$feedback = "Email Cannot Be Blank";
	} else {
		$mysql->query("UPDATE users SET firstname='$fname', lastname='$lname', email='$email' WHERE uid='$uid'");
		$feedback = "Profile Updated";
	}
}
?>

<?=$feedback?>
<form action='?page=profile' method='POST' >
	First Name: <input type='text' name='fname' value='<?=isset($_POST['fname']) ? $_POST['fname'] : $user['firstname']?>'/> <br/>
	Last Name: <input type='test' name='lname' value='<?=isset($_POST['lname']) ? $_POST['lname'] : $user['lastname']?>'/> </br>
	Email: <input type='test' name='email' value='<?=isset($_POST['email']) ? $_POST['email'] : $user['email']?>'/> </br>
	<input type='submit' value='Save' />
</form>
