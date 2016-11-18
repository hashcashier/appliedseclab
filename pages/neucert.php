<?php
if (!$isLoggedIn) {
	header("Location: /?page=index");
	die();
}
$confirm = isset($_GET['confirm']) ? $_GET['confirm'] : 0;

if ($confirm == '1') {
	$request = json_encode(array(
		'username' => $user['uid'],
		'fullname' => $user['firstname'].' '.$user['lastname'],
		'email' => $user['email']));
	// send request to CA server
	$response = shell_exec("/var/www/html/dummy.sh $request");
	// Print resulting certificate contents and offer PKCS#12 download
	print nl2br($response);
} else {
	?>
	Your user details are as follows: <br />
	<b>First Name:</b> <?=$user['firstname']?> <br/>
	<b>Last Name:</b> <?=$user['lastname']?> </br>
	<b>Email:</b> <?=$user['email']?></br>
	
	If you wish to make any corrections. Please refer to your profile page. <br />
	
	Otherwise, <a href='?page=neucert&confirm=1'>Click here</a> to request a new certificate with this user information.
	<?php
}
?>
