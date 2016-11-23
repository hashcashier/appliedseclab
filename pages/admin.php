<?php
if (!$isLoggedIn || !$isCertAuth || !$isAdmin) {
	header("Location: /?page=index");
	die();
}

?>#Issued, #Revoked, Current Serial:<br/><?php
$response = shell_exec("/var/www/html/admin_ca_client.py");
print($response);

// Poll CA Server
// Print Information
// 1. Number of issued certificates;
// 2. Number of revoked certificates;
// 3. Current serial number.

?>
