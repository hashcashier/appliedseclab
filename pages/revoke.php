<?php
if (!$isLoggedIn) {
	header("Location: /?page=index");
	die();
}

function wasSent($file) {
	return file_exists($file['tmp_name']) && is_uploaded_file($file['tmp_name']);
}

if (isset($_FILES['cert'], $_FILES['pkey']) && wasSent($_FILES['cert']) && wasSent($_FILES['pkey'])) {
	// send request to CA server
	$response = shell_exec("/var/www/html/bash/ca_client.py R $uid {$_FILES['cert']['tmp_name']} {$_FILES['pkey']['tmp_name']}");
	// confirm revocation
	print($response);
} else if (isset($_GET['pkcs12'] && wasSent($_FILES['pkcs12'])) {
	// send request to CA server
	$response = shell_exec("/var/www/html/bash/ca_client.py RP $uid {$_FILES['pkcs12']['tmp_name']}");
	// confirm revocation
	print($response);
} else if (isset($_GET['all']) && $_GET['all'] == '1') {
	// send request to CA server
	$response = shell_exec("/var/www/html/bash/ca_client.py RA {$user['uid']}");
	// confirm revocation
	print($response);
} else {
	?>
	<form action="?page=revoke" method="post" enctype="multipart/form-data">
		Upload a certificate, private key pair to be revoked:<br />
		<b>Certificate:</b> <input type="file" name="cert" id="cert"><br />
		<b>Private Key:</b> <input type="file" name="pkey" id="pkey"><br />
		<input type="submit" value="Revoke Certificate" name="submit"><br />
	</form>	
	Or, </br>
	<form action="?page=revoke" method="post" enctype="multipart/form-data">
		Upload a PKCS12 archive to be revoked:<br />
		<b>PKCS12 Archive:</b> <input type="file" name="pkcs12" id="cert"><br />
		<input type="submit" value="Revoke Certificate" name="submit"><br />
	</form>	
	<br />
	Or, if you have lost the public/private key pair, you may revoke all certificates related to your account.<br />
	<b>WARNING: </b> IRREVERSABLE PROCESS. ENSURE YOU STILL MAINTAIN YOUR USERNAME AND PASSWORD TO BE ABLE TO LOG BACK IN.<br />
	<a href='?page=revoke&all=1'>Click here</a> if you really want to revoke all certificates related to your account.<br />
	<?php
}

?>
