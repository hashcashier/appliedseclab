<?php
if (!$isLoggedIn) {
	header("Location: /?page=index");
	die();
}

function wasSent($file) {
	return file_exists($file['tmp_name']) && is_uploaded_file($file['tmp_name']);
}

if (isset($_FILES['cert'], $_FILES['pkey']) && wasSent($_FILES['cert']) && wasSent($_FILES['pkey'])) {
	$request = json_encode(array('cert' => $_FILES['cert']['tmp_name'], 'pkey' => $_FILES['pkey']['tmp_name']));
	// send request to CA server
	$response = shell_exec("/var/www/html/ca_client.py R $user['uid'] $user['firstname'] $user['lastname'] $user['email'] employee");
	// confirm revocation
	print($response);
} else if (isset($_GET['all']) && $_GET['all'] == '1') {
	$request = json_encode(array('revoke' => $user['uid']));
	// send request to CA server
	$response = shell_exec("/var/www/html/ca_client.py G $user['uid'] $user['firstname'] $user['lastname'] $user['email'] employee");
	// confirm revocation
	print($response);
} else {
	?>
	<form action="?page=revoke" method="post" enctype="multipart/form-data">
		Upload a certificate to be revoked:<br />
		<b>Certificate:</b> <input type="file" name="cert" id="cert"><br />
		<b>Private Key:</b> <input type="file" name="pkey" id="pkey"><br />
		<input type="submit" value="Revoke Certificate" name="submit"><br />
	</form>	
	<br />
	Or, if you have lost the public/private key pair, you may revoke all certificates related to your account.<br />
	<b>WARNING: </b> IRREVERSABLE PROCESS. ENSURE YOU STILL MAINTAIN YOUR USERNAME AND PASSWORD TO BE ABLE TO LOG BACK IN.<br />
	<a href='?page=revoke&all=1'>Click here</a> if you really want to revoke all certificates related to your account.<br />
	<?php
}

?>
