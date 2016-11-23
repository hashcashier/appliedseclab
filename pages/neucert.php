<?php
if (!$isLoggedIn) {
	header("Location: /?page=index");
	die();
}
$confirm = isset($_GET['confirm']) ? $_GET['confirm'] : 0;
$download = isset($_GET['down']) ? $_GET['down'] : 0;

if ($confirm == '1') {
	$request = json_encode(array(
		'uname' => $user['uid'],
		'CN' => $user['firstname'].' '.$user['lastname'],
		'emailAddress' => $user['email']));
	// send request to CA server
	//print("/var/www/html/ca_client.py G {$user['uid']} {$user['firstname']} {$user['lastname']} {$user['email']} employee"."<br>");
	$response = shell_exec("/var/www/html/bash/ca_client.py G {$user['uid']} {$user['email']} employee");
	// Print resulting certificate contents and offer PKCS#12 download
	header("Location: /?page=neucert&down=1");
	die();
} else if($download == '1') {
	?>
	Error..
	<?php
	
	// TODO: Delete file at some point in time..
	$file = "/var/www/html/bash/client/{$uid}cert.p12";
	if (file_exists($file)) {
		ob_clean();
		header('Content-Description: File Transfer');
		header('Content-Type: application/octet-stream');
		header('Content-Disposition: attachment; filename="'.basename($file).'"');
		header('Expires: 0');
		header('Cache-Control: must-revalidate');
		header('Pragma: public');
		header('Content-Length: ' . filesize($file));
		readfile($file);
	}
	
	die();
	
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
