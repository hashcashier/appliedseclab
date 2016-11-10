<?php
if (!$isLoggedIn) {
	header("Location: /?page=index");
	die();
}

if (isset($_FILES['cert'], $_FILES['pkey'])) {
	// send request to CA server
	// wait for response
	// confirm revocation
} else if (isset($_GET['all'] && $_GET['all'] == '1') {
	$request = json_encode(array('username' => $uid));
	// send request to CA server
	// wait for response
	// confirm revocation
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
