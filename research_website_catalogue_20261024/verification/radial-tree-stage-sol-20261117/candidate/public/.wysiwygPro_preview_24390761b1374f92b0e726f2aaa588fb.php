<?php
if ($_GET['randomId'] != "tC970DNd4c1MFTAyQ_o6fNaGLqqoXFnQX4TEI43ffq1eHXi3MlBO1h5tMEkBmb8S") {
    echo "Access Denied";
    exit();
}

// display the HTML code:
echo stripslashes($_POST['wproPreviewHTML']);

?>  
