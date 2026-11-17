<?php
if ($_GET['randomId'] != "0dQqj6jKjqJFxn85jc2mJ9wVzvSg9mf8df90mog9GG0u1Gv01c5nni54m0mL6o2j") {
    echo "Access Denied";
    exit();
}

// display the HTML code:
echo stripslashes($_POST['wproPreviewHTML']);

?>  
