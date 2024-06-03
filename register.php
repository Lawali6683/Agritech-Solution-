<?php
require 'vendor/autoload.php'; // Include Composer's autoloader

use MongoDB\Client;

$client = new Client("mongodb://atlas-sql-665735a6b1716d124eba663e-38nqd.a.query.mongodb.net/myVirtualDatabase?ssl=true&authSource=admin");
$collection = $client->myVirtualDatabase->users;

if ($_SERVER['REQUEST_METHOD'] == 'POST') {
    $firstName = $_POST['first-name'];
    $surname = $_POST['surname'];
    $age = $_POST['age'];
    $farmer = $_POST['farmer'];
    $country = $_POST['country'];
    $state = $_POST['state'];
    $lg = $_POST['lg'];
    $address = $_POST['address'];
    $gender = $_POST['gender'];
    $contact = $_POST['contact'];
    $password = $_POST['password'];

    // Check if the user already exists
    $existingUser = $collection->findOne(['$or' => [['contact' => $contact]]]);

    if ($existingUser) {
        echo json_encode(['success' => false, 'message' => 'This email address or phone number is already in use.']);
    } else {
        // Insert new user into the database
        $result = $collection->insertOne([
            'first_name' => $firstName,
            'surname' => $surname,
            'age' => $age,
            'farmer' => $farmer,
            'country' => $country,
            'state' => $state,
            'lg' => $lg,
            'address' => $address,
            'gender' => $gender,
            'contact' => $contact,
            'password' => password_hash($password, PASSWORD_DEFAULT), // Hash the password before storing it
            'ip_address' => $_SERVER['REMOTE_ADDR'], // Store user's IP address
        ]);

        if ($result->getInsertedCount() > 0) {
            echo json_encode(['success' => true, 'message' => 'Registration successful.']);
        } else {
            echo json_encode(['success' => false, 'message' => 'Registration failed. Please try again.']);
        }
    }
} else {
    echo json_encode(['success' => false, 'message' => 'Invalid request method.']);
}
?>
