<?php
if (!$isLoggedIn || !$isCertAuth || !$isAdmin) {
	header("Location: /?page=index");
	die();
}

$request = json_encode(array('stats' => 1));
$response = shell_exec("/var/www/html/dummy.sh $request");
print($response);

// Poll CA Server
// Print Information
// 1. Number of issued certificates;
// 2. Number of revoked certificates;
// 3. Current serial number.

?>
